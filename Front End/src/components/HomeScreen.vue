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
      <label>Select Metric to Calculate:</label>
      <div class="radio-group">
        <input type="radio" id="lcom4" value="LCOM4" v-model="selectedMetric" />
        <label for="lcom4">LCOM4</label>
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
    const selectedMetric = ref('');
    const handleFileUpload = (event) => {
      uploadedFile.value = event.target.files[0];
    };
    const submitData = () => {
      console.log('GitHub URL:', githubUrl.value);
      console.log('Uploaded File:', uploadedFile.value);
      console.log('Selected Metric:', selectedMetric.value);
    };
    return {
      githubUrl,
      uploadedFile,
      selectedMetric,
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
.radio-group {
  display: flex;
  align-items: center;
  margin-top: 10px;
}
.radio-group input {
  margin-right: 10px;
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