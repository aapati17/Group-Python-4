<template>
  <main>
    <h1>Metric Calculator</h1>

    <div class="input-container">
      <label for="github-url">Enter GitHub Repository URL:</label>
      <input type="text" id="github-url" v-model="githubUrl" placeholder="https://github.com/user/repository" />
      <p v-if="errorMessages.githubUrl" class="error">{{ errorMessages.githubUrl }}</p>
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
import axios from 'axios';

export default {
  setup() {
    const githubUrl = ref('');
    const selectedMetrics = ref([]);
    const errorMessages = ref({ githubUrl: '' });

    const isValidGitHubUrl = (url) => {
      const regex = /^https:\/\/github\.com\/[\w-]+\/[\w-]+\/?$/;
      return regex.test(url);
    };

    const checkGitHubRepoExists = async () => {
      if (!isValidGitHubUrl(githubUrl.value)) {
        errorMessages.value.githubUrl = "Invalid GitHub URL format.";
        return false;
      }

      const repoPath = githubUrl.value.replace("https://github.com/", "");
      const apiUrl = `https://api.github.com/repos/${repoPath}/languages`;

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

    const sendDataToBackend = async () => {
      const sourceType = "git";
      const githubLink = githubUrl.value;

      const list = JSON.parse(JSON.stringify(selectedMetrics.value));
      let metrics = list.join(", ");

      const formData = new FormData();
      formData.append("sourceType", sourceType);
      formData.append("githubLink", githubLink);
      formData.append("metrics", metrics);

      try {
        await axios.post('http://localhost:8080/sample', formData, {
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
      errorMessages.value.githubUrl = '';

      let isValid = await checkGitHubRepoExists();
      if (isValid) {
        console.log("Validation passed. Proceeding with submission.");
        sendDataToBackend();
      }
    };

    return {
      githubUrl,
      selectedMetrics,
      errorMessages,
      submitData
    };
  },
  methods: {
    goToOutputView() {
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

input[type="text"] {
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