# SER 516 Group-Python-4

## Software Quality Metrics Calculator

  

### Table of Contents

1. [Introduction](#introduction)

2. [Project Overview](#project-overview)

3. [Fixes](#fixes)

4. [Setting up and Running the Project](#setting-up-and-running-the-project)

5. [How to use the Web-App](#how-to-use-the-web-app)

6. [Contributors](#contributors)

  

---

  

### Introduction

  

Welcome to the documentation for the SER 516 Group_Python_4 project - Software Quality Metrics Calculator. This project is aimed at computing and retaining those computations of Software Quality Metrics *(in this case, LCOM4, LCOMHS and Defect score)* for any GitHub Public Repository that has Java code. This tool can help user to maintain software quality for projects at all scale.

  

___

  

### Project Overview

  

The Software Quality Metrics Calculator is a two-part project:

  

-  **Frontend:** A Vue-based web application that serves as the user interface for the Metrics Calculator. It provides an interactive environment for users to provide details about the GitHub repository and the metrics they want to calculate, and display the calculated metrics with all the previous data.

  

-  **Backend:** A Python application built using FastAPI for communication between Frontend and Backend, and MongoDB for retaining the computed data. It contains the core logic for computing, routing and storing the results of computations.

  

___

  

### Fixes

  

- Readme and Documentation revised to explain the usage and prerequisites of the project.

- Benchmarks are no longer forced on to the user.

- Added cards for showing current metric values.

- UI overhaul of the results page.

---

  

### Setting up and Running the Project

  

Before we start setting up the project, we would need the following:

- Docker Desktop / Hub

- A public GitHub repository for which you want to measure metrics

  
  

To run the project, follow these steps:

- Go to the Terminal and redirect to the root directory of this project.

- Run this Docker command to build the application:

```

docker-compose up --build

```

- Once built, you can open a web browser and go to the URL below:

```

http://localhost:5173

```

  

___

  

### How to use the Web-App

  

Once the URL is loaded, you would be greeted with the landing page shown below:

![image](https://github.com/user-attachments/assets/7e8b781d-49b6-46b6-a422-8f7145c2a907)

  
  

Now, to compute your metrics, you have to follow 4 steps:

  

- [Validate your GitHub URL](#validate-your-github-url)

- [Select one or more metrics to calculate](#select-one-or-more-metrics-to-calculate)

- [Set the benchmark scores for the selected metrics (OPTIONAL)](#set-the-benchmark-scores-for-the-selected-metrics-optional)

- [Submit the data](#submit-the-data)

#### Validate your GitHub URL

- Copy and Paste your GitHub repository URL into the textbox

![image](https://github.com/user-attachments/assets/5d24b4d9-c354-490c-b3b1-ae90490cb746)

- There are two ways to validate your input, either by pressing `return` key or by clicking on the **Validate your URL** button below the textbox highlighted above.

  

#### Do's and Don'ts:

  

Do's:

- Please use the URL of GitHub repository which is **Public** and contains some **Java** code (be it a singular class or a full maven or gradle project).

![image](https://github.com/user-attachments/assets/baddaabf-85a2-42a5-9f60-9aa3e0648887)

  

Don'ts:

- Do not use the URL of a **Private** GitHub repository.

  

![image](https://github.com/user-attachments/assets/2f549089-e483-4693-9f8b-e1d11a8f99a6)

This repository has URL: https://github.com/agarasia/ser515

  

![image](https://github.com/user-attachments/assets/5dbeeb98-afe0-4843-8cc9-984e1cd0211d)

  

**Reason:** The GitHub REST API would return a `404` error

  

- Do not use the URL of a GitHub repository (be it Public OR Private) that does **NOT** contain Java code.

  
  

![image](https://github.com/user-attachments/assets/1113e8b9-a77e-4e96-94be-fd4ad7b625a9)

  

Note that unless and until you see the message `Valid GitHub repository`, the options for metrics are *NOT VISIBLE*.

![image](https://github.com/user-attachments/assets/f275db6f-8fa7-44d2-9d8d-aae0c5c0c7cb)

  
  

#### Select one or more metrics to calculate:

Now that you have a valid GitHub URL and it is validated, you would now see that the checkboxes for metrics are clickable.

![image](https://github.com/user-attachments/assets/ea8aa9f4-b857-4908-820e-fe91df4dbc9b)

  
  

You can click on one or more metrics (say for instance, you want to calculate LCOM4 and Defect Score) simply by clicking on the corresponding checkboxes.

![image](https://github.com/user-attachments/assets/e81514ab-89f1-41f2-8a9a-db315135bdac)

  
  

**Additional Instructions for Defect Score Calculation**

  

When you select the **Defect Score** checkbox, the app will prompt you to input the Tags and their respective weights. This step is necessary because GitHub issues do not have built-in support to determine the severity of reported issues automatically. Instead, the app relies on your input to assign weights to the tags, which in turn are used to calculate the defect severity.

  
  

##### Tags

  

-  **Purpose:**

The tags you enter correspond directly to the labels you assign to issues on GitHub.

  

-  **Example:**

For instance, if you label an issue as "bug", you should input the tag **bug** here.

  

-  **Visual Guide:**

![Tags on Github Issues](resources/TagExample.png)

  

##### Weight

  

-  **Definition:**

The weight is a numerical value that represents the severity of the tag.

  

-  **Usage:**

A tag like **bug** might have a weight of **1**, whereas a **critical** tag could have a higher weight, such as **5**.

  

-  **Impact:**

These weights are used by the app to calculate a weighted defect score, allowing you to assess both the quantity and severity of issues.

  

#### How to Use in the App

  

**Input Tags & Weights:** When prompted, enter the relevant GitHub issue tags along with their corresponding weights as illustrated below. Then, Click **+ Add Tag** button.

![image](https://github.com/user-attachments/assets/056e7af8-f850-49bd-ae9b-f18831998bff)

  

Your custom defect tag would now be displayed below the **+ Add Tag** button.

  

![image](https://github.com/user-attachments/assets/d6669b4b-5b7c-41de-9420-9bea325a4f87)

  

#### Submit the data

Once all the metrics you need are selected, just click on **Calculate** button.

![image](https://github.com/user-attachments/assets/8655fb30-dc28-4da8-a304-89391c217b12)

  
  

The Computation can take longer depending on the number of Java files as well as their sizes. The text on the Submit Data button will change to '*LOADING....*'.

  

DO NOT click on Submit multiple times.

<br>

  

#### Set the benchmark scores for the selected metrics (OPTIONAL)

  

Once the computations are Done and you are about to see the visualized data for your metrics, you can also set the benchmarks and/or decide if you want to compare against the computed data. As you can see the number fields are pre-populated, these benchmarks are fetched from the MongoDB database.

  

You would also notice that under the LCOM4 benchmark, the show benchmark checkbox is unticked, this means that I do not want to compare my results for LCOM4 against benchmarks. You can do the same if you selected, say all the metrics i.e. LCOM4, LCOMHS and Defect Score; and do not want to compare the results for LCOMHS and Defect Score. You can simply uncheck the checkbox and the charts would not have the benchmark scores' line in the chart.

  

Additionally, you can also do something as a mix of the two, say I want to set a new benchmark score for LCOM4 but do not want to see the benchmark in the chart. I can type a new benchmark score within the textbox but still keep the checkbox unchecked.

  

![image](https://github.com/user-attachments/assets/389b923b-fddc-49d2-83e3-d83ba0a8fc97)

  
  

Once the *Apply/Continue* button is clicked, the results would be shown for the metrics within 2 graphs. One for the LCOM metrics (LCOM4 and LCOMHS), and other for the Defect Score. For current Metric values cards will show the data like below.

![image](https://github.com/user-attachments/assets/972463d1-bab7-4ace-b992-c09209259e10)
  

![image](https://github.com/user-attachments/assets/0a7e8d1e-1bd5-4c94-8c21-d011ba440cb8)

  

![image](https://github.com/user-attachments/assets/4ed35575-8580-4800-af13-cf9b6d6dc6b9)

Since LCOM4 and LCOMHS are computed for each class, there is an option to select which class do you want to observe using the dropdown.

  

![image](https://github.com/user-attachments/assets/c580ed1b-48ae-4b3b-933e-32c24ec82442)

For defect score, a number of values are illustrated; which are:

- Total number of Defects

- Weighted Average Density of Defects

- Maximum and Minimum Severity of the Defects

- Standard Deviation Density of the Weighted Average Density

  

You can hover over data points to see detailed timestamps and score values. The last data point is highlighted with a different color and larger radius, so you know it represents the most recent score.

___

  

### Contributors

  

This project is a collaborative effort by the SER 516 Group-Python-4 team. If you have any questions or need assistance, please reach out to one of the team members-

- Aniket Patil (@aapati17)

- Aum Jitendra Garasia (@agarasia)

- Satyam Shekhar (@sshekh30)

- Uma Maheshwar Reddy N (@unallami)

  

---
