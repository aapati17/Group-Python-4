<template>
  <main>
    <h1>Metric Calculator</h1>

    <div class="input-container">
      <label for="github-url">Enter GitHub Repository URL:</label>
      <input type="text" id="github-url" v-model="githubUrl" placeholder="https://github.com/user/repository" />
    </div>

    <div class="input-container">
      <label for="upload-file">Upload a ZIP Project:</label>
      <input type="file" id="upload-file" @change="handleFileUpload" accept=".zip" />
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
          <input type="checkbox" id="defscore" value="Defect Score" v-model="selectedMetrics" />
          <label for="defscore">Defect Score</label>
        </div>
      </div>
    </div>

    <button @click="submitData">Submit</button>
  </main>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const githubUrl = ref('');
    const uploadedFile = ref(null);
    const selectedMetrics = ref([]);

    const handleFileUpload = (event) => {
      uploadedFile.value = event.target.files[0];
    };

    const submitData = () => {
      console.log('GitHub URL:', githubUrl.value);
      console.log('Uploaded File:', uploadedFile.value);
      console.log('Selected Metrics:', selectedMetrics.value);
    };

    return {
      githubUrl,
      uploadedFile,
      selectedMetrics,
      handleFileUpload,
      submitData
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

input[type="text"],
input[type="file"] {
  display: block;
  width: 100%;
  padding: 10px;
  font-size: 16px;
  margin-bottom: 15px;
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