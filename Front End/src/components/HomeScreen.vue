<template>
  <main>
    <h1>Metric Calculator</h1>

    <div class="input-container">
      <label for="github-url">Enter GitHub Repository URL:</label>
      <input type="text" id="github-url" v-model="githubUrl" placeholder="https://github.com/user/repository" />
      <p v-if="errorMessages.githubUrl" class="error">{{ errorMessages.githubUrl }}</p>
    </div>

    <div class="input-container">
      <label for="upload-file">Upload a ZIP Project:</label>
      <input type="file" id="upload-file" @change="handleFileUpload" accept=".zip" />
      <p v-if="errorMessages.uploadedFile" class="error">{{ errorMessages.uploadedFile }}</p>
    </div>

    <div class="input-container">
      <label>Select Metrics to Calculate:</label>
      <div class="checkbox-group">
        <div class="checkbox-item">
          <input type="checkbox" id="lcom4" value="LCOM4" v-model="selectedMetrics" />
          <label for="lcom4">LCOM4</label>
        </div>
        <div class="checkbox-item">
          <input type="checkbox" id="lcomhs" value="LCOMHS" v-model="selectedMetrics" />
          <label for="lcomhs">LCOMHS</label>
        </div>
        <div class="checkbox-item">
            <input type="checkbox" id="defectscore" value="Defect Score" v-model="selectedMetrics" />
            <label for="defectscore">Defect Score</label>
          </div>
      </div>
    </div>

    <button @click="submitData" @click.prevent="goToOutputView">Submit</button>
  </main>
</template>

<script>
import { ref } from 'vue';
import JSZip from 'jszip';
import axios from 'axios';

export default {
  setup() {
    const githubUrl = ref('');
    const uploadedFile = ref(null);
    const selectedMetrics = ref([]);
    const errorMessages = ref({
      githubUrl: '',
      uploadedFile: ''
    });

    const isValidGitHubUrl = (url) => {
      const regex = /^https:\/\/github\.com\/[\w-]+\/[\w-]+\/$/;
      return regex.test(url);
    };

    const checkGitHubRepoExists = async () => {
      if (!isValidGitHubUrl(githubUrl.value)) {
        errorMessages.value.githubUrl = "Invalid GitHub URL format.";
        return false;
      }

      const repoPath = githubUrl.value.replace("https://github.com/", "");
      const apiUrl = `https://api.github.com/repos/${repoPath}languages`;

      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          errorMessages.value.githubUrl = "GitHub repository does not exist.";
          return false;
        }
        const files = await response.json();
        const keys = Object.keys(files);

        if (!keys.includes("Java")) {
          errorMessages.value.githubUrl = "The repository does not have a Java project.";
          return false;
        }

        errorMessages.value.githubUrl = "";
        return true;
      } catch (error) {
        errorMessages.value.githubUrl = "Error connecting to GitHub.";
        return false;
      }
    };

    const isValidZipFile = (file) => {
      const validTypes = ["application/zip", "application/x-zip-compressed"];
      return file && validTypes.includes(file.type);
    };

    const isFileSizeValid = (file) => {
      const MAX_SIZE_MB = 10;
      return file && file.size <= MAX_SIZE_MB * 1024 * 1024;
    };

    const checkJavaProjectStructure = async (file) => {
      const zip = new JSZip();
      const zipContent = await zip.loadAsync(file);
      const files = Object.keys(zipContent.files);

      const hasJavaFiles = files.some(file => file.endsWith('.java'));
      const hasBuildFiles = files.includes("pom.xml") || files.includes("build.gradle");

      if (!hasJavaFiles && !hasBuildFiles) {
        errorMessages.value.uploadedFile = "Invalid Java project structure.";
        return false;
      }

      errorMessages.value.uploadedFile = "";
      return true;
    };

    const handleFileUpload = async (event) => {
      uploadedFile.value = event.target.files[0];
      errorMessages.value.uploadedFile = "";

      if (uploadedFile.value) {
        if (!isValidZipFile(uploadedFile.value)) {
          errorMessages.value.uploadedFile = "Invalid file type. Please upload a ZIP file.";
          return;
        }

        if (!isFileSizeValid(uploadedFile.value)) {
          errorMessages.value.uploadedFile = "File is too large. Maximum allowed size is 10MB.";
          return;
        }

        const isValidStructure = await checkJavaProjectStructure(uploadedFile.value);
        if (!isValidStructure) {
          return;
        }
      }
    };

    const sendDataToBackend = async () => {
      let sourceType = "";
      let sourceLink = "";
      let file = null;
      if (githubUrl.value) {
        sourceType = "git";
        sourceLink = githubUrl.value;
      } else {
        sourceType = "zip";
        file = uploadedFile.value;
        console.log(uploadedFile.value);
      }

      const list = JSON.parse(JSON.stringify(selectedMetrics.value));
      let metrics = list.join(", ");

      const formData = new FormData();
      formData.append("sourceType", sourceType);
      formData.append("sourceLink", sourceLink);
      if (file) {
        formData.append("file", file);
      }
      formData.append("metrics", metrics);

      try {
        const req = await axios.post('http://localhost:8080/sample', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Access-Control-Allow-Origin': '*',
          'mode': 'cors'
        }
      });
      } catch (error) {
        console.error("Error sending data to backend:", error);
      }
    };

    const submitData = async () => {
      let isValid = true;
      errorMessages.value.githubUrl = '';
      errorMessages.value.uploadedFile = '';

      if (githubUrl.value) {
        isValid = await checkGitHubRepoExists();
      } else if (uploadedFile.value) {
        if (!isValidZipFile(uploadedFile.value)) {
          errorMessages.value.uploadedFile = "Invalid file type. Please upload a ZIP file.";
          isValid = false;
        }

        if (!isFileSizeValid(uploadedFile.value)) {
          errorMessages.value.uploadedFile = "File is too large. Maximum allowed size is 10MB.";
          isValid = false;
        }

        const isValidStructure = await checkJavaProjectStructure(uploadedFile.value);
        if (!isValidStructure) {
          isValid = false;
        }
      } else {
        errorMessages.value.githubUrl = "Please provide either a GitHub link or upload a ZIP file.";
        isValid = false;
      }

      if (isValid) {
        console.log("Validation passed. Proceeding with submission.");
        sendDataToBackend();
      }
    };

    return {
      githubUrl,
      uploadedFile,
      selectedMetrics,
      errorMessages,
      handleFileUpload,
      submitData
    };
  },
  methods: {
    goToOutputView() {
      // Emit event to parent to switch to OutputView
      this.$emit('switch-to-OutputView');
    }
  }
};
</script>

<style scoped>
main {
  text-align: center;
  padding: 40px 20px;
}

.input-container {
  margin: 20px auto;
  width: 80%;
  max-width: 500px;
  text-align: left;
}

label {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="file"] {
  display: block;
  width: 100%;
  padding: 10px;
  font-size: 16px;
  margin-bottom: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
