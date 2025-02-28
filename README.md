# Group-Python-4
SER 516 Project Repository

Team Members:
	- Aum Jitendra Garasia (@agarasia)
	- Aniket Patil (@aapati17)
	- Satyam Shekhar (@sshekh30)
	- Uma Maheshwar Reddy N (@unallami) 

# Prerequisites

- Docker Desktop
- A public GitHub repository for which you want to measure metrics
- An existing FireBase Project and its serviceAccountKey.json (Click [here ](https://arizonastateu-my.sharepoint.com/:v:/g/personal/aapati17_sundevils_asu_edu/EeWlv-MwbWRGuI7MoUIg_S8BB5QoxINDK-MLAbTtZ7Loqw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DIdogA) for video guide)

# Instruction to run the app 

For MAC / Windows:-
 - Paste the ServiceAccountKey.json in root directory of the project
 - Start the terminal and go to the path location where the project is stored
 - Run ```docker-compose up -—build```
 - once built, open browser and go to ```https://localhost:5173```

## Prerequisites

Before running the script, make sure you have the following setup / installed:

-Firebase project Setup:
[Link to setup FireBase project](https://arizonastateu-my.sharepoint.com/:v:/g/personal/aapati17_sundevils_asu_edu/EeWlv-MwbWRGuI7MoUIg_S8BB5QoxINDK-MLAbTtZ7Loqw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DIdogA)

-Docker Desktop / Hub

### step 1:

*goto group-Python-4*

### step 2: Open the App:
Launch the web app in your browser, Access it via a URL provided above.

### Step 3: Choose a Metric
Select a metric from the dropdown or selection panel (e.g., LCOMHS, LCOM4, **Defect Score**). Once you select a metric, the app will filter the data accordingly.

#### Defect Score Details

When you select the **Defect Score** checkbox, the app will prompt you to input the Tags and their respective weights. This step is necessary because GitHub issues do not have built-in support to determine the severity of reported issues automatically. Instead, the app relies on your input to assign weights to the tags, which in turn are used to calculate the defect severity.

##### Tags
- **Purpose:**  
  The tags you enter correspond directly to the labels you assign to issues on GitHub.  
- **Example:**  
  For instance, if you label an issue as "bug", you should input the tag **bug** here.
- **Visual Guide:**  

  ![Tags on Github Issues](resources/TagExample.png)

##### Weight
- **Definition:**  
  The weight is a numerical value that represents the severity of the tag.  
- **Usage:**  
  A tag like **bug** might have a weight of **1**, whereas a **critical** tag could have a higher weight, such as **5**.
- **Impact:**  
  These weights are used by the app to calculate a weighted defect score, allowing you to assess both the quantity and severity of issues.

#### How to Use in the App
1. **Select Metric:** From the metric options, choose **Defect Score**.
2. **Input Tags & Weights:** When prompted, enter the relevant GitHub issue tags along with their corresponding weights.
3. **View Results:** The app calculates and displays the defect score over time, enabling you to monitor and compare the severity of issues in your codebase.


### step 4: View the Chart:
Once both the metric(s) selected, the app computes the chart data. It pulls historical and current values for the chosen metric and class. The main dataset shows your scores over time.

### step 5: Benchmark Display:
A second dataset representing the benchmark is overlaid on the chart. This is displayed as a dotted line (or another style, depending on your settings) across the timeline, allowing you to compare your score against the benchmark.

### step 6: Interact with the Chart:
You can hover over data points to see detailed timestamps and score values. The last data point is highlighted with a different color and larger radius, so you know it represents the most recent score.

### step 7: Review & Compare:
Use the visual comparison between your actual data (solid line) and the benchmark (dotted line) to quickly assess how your current performance stacks up against your target or industry standard.

### step 8: Adjust Selections as Needed:
If you want to see different metrics or classes, simply update your selections. The chart will automatically refresh with the new data.
