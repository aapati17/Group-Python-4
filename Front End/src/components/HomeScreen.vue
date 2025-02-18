<template>
  <main>
    <h1>Metric Calculator</h1>

    <!-- Show Input Form if OutputView is Hidden -->
    <div v-if="!showOutput">
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

    <!-- Tag Input Box for Defect Score -->
    <div class="input-container" v-if="selectedMetrics.includes('Defect Score')">
      <label>Defect Score Inputs:</label>
      <h4>Please add in format "label" : "score", no gap</h4>
      <div class="tag-input">
        <input
          type="text"
          v-model="tagInput"
          @keyup.enter="addTag"
          placeholder="Add input and press Enter"
        />
        <div class="tags">
          <span v-for="(tag, index) in defectScoreTags" :key="index" class="tag">
            {{ tag }}
            <span class="remove-tag" @click="removeTag(index)">×</span>
          </span>
        </div>
      </div>
    </div>

    <button @click="submitData">Submit</button>
    </div>

    <!-- Show Output Screen After Validation -->
    <OutputView v-if="showOutput" @goBack="showFormAgain" />
  </main>
</template>

<script>
import { ref, watch } from 'vue';
import axios from 'axios';
import OutputView from './OutputView.vue';

export default {
  components: {
    OutputView
  },
  setup() {
    const githubUrl = ref('');
    const selectedMetrics = ref([]);
    const errorMessages = ref({ githubUrl: '' });
    const showOutput = ref(false); // Controls OutputView visibility

    // Tag Input State
    const tagInput = ref('');
    const defectScoreTags = ref([]);

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

    const submitData = async () => {
      errorMessages.value.githubUrl = '';

      let isValid = await checkGitHubRepoExists();
      if (isValid) {
        console.log("Validation passed. Proceeding to OutputView.");
        showOutput.value = true;
      }
    };


    const showFormAgain = () => {
      showOutput.value = false;
    };

    // Tag Input Methods
    const addTag = () => {
      if (tagInput.value.trim() !== '') {
        defectScoreTags.value.push(tagInput.value.trim());
        tagInput.value = '';
      }
    };

    const removeTag = (index) => {
      defectScoreTags.value.splice(index, 1);
    };

    return {
      githubUrl,
      selectedMetrics,
      errorMessages,
      submitData,
      showOutput,
      showFormAgain,
      tagInput,
      defectScoreTags,
      addTag,
      removeTag
    };
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

.tag-input {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tag {
  background-color: #e0e0e0;
  padding: 5px 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.remove-tag {
  cursor: pointer;
  font-weight: bold;
  color: red;
}
</style>