<template>
  <div class="output-container">
    <!-- Back Button (Top Left) -->
    <button class="back-button" @click="goBack">←</button>

    <h1>Output View</h1>

    <div class="table-container">
      <table class="output-table">
        <thead>
          <tr>
            <th>Class</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in tableData" :key="index">
            <td>{{ row.class }}</td>
            <td>{{ row.score }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <button class="btn btn-outline-dark" @click="downloadPDF">Export</button>
  </div>
</template>

<script>
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

export default {
  name: 'OutputView',
  data() {
    return {
      tableData: [
        { class: 'Class 1', score: 85 },
        { class: 'Class 2', score: 90 },
        { class: 'Class 3', score: 78 },
        { class: 'Class 4', score: 88 },
        { class: 'Class 5', score: 92 },
        { class: 'Class 6', score: 80 },
        { class: 'Class 7', score: 76 },
        { class: 'Class 8', score: 89 },
        { class: 'Class 9', score: 84 },
        { class: 'Class 10', score: 91 }
      ]
    }
  },
  methods: {
    downloadPDF() {
      const doc = new jsPDF();
      doc.text("Class Scores", 14, 20);
      const head = [['Class', 'Score']];
      const body = this.tableData.map(row => [row.class, row.score]);
      autoTable(doc, { head: head, body: body, startY: 30 });
      doc.save("table_data.pdf");
    },
    goBack() {
      this.$emit('goBack'); // Emit event to notify HomeScreen to show input form again
    }
  }
}
</script>

<style scoped>
.output-container {
  position: relative;
  text-align: center;
  padding: 20px;
}

/* Back Button Style */
.back-button {
  position: absolute;
  top: 10px;
  left: 20px; /* Keep it at the top left */
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}

.back-button:hover {
  color: #007bff;
}

.table-container {
  text-align: center;
  margin-top: 20px;
}

.output-table {
  width: 50%;
  margin: 0 auto;
  border-collapse: collapse;
  border: 1px solid #ccc;
}

.output-table th,
.output-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}

.output-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

button {
  margin-top: 20px;
  padding: 10px 500px;
  font-size: 16px;
  cursor: pointer;
}
</style>
