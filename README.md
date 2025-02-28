
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
- An existing FireBase Project and its serviceAccountKey.json (video guide for setup given below)

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

### step 3: Choose a Metric:
Look for a dropdown or selection panel where you can choose a metric *(e.g., LCOMHS, LCOM4, Defect Score)*. When you select a metric, the app will use that value to filter the data.

### step 4: View the Chart:
Once both the metric(s) selected, the app computes the chart data. It pulls historical and current values for the chosen metric and class. The main dataset shows your scores over time.

### step 4: Benchmark Display:
A second dataset representing the benchmark is overlaid on the chart. This is displayed as a dotted line (or another style, depending on your settings) across the timeline, allowing you to compare your score against the benchmark.

### step 5: Interact with the Chart:
You can hover over data points to see detailed timestamps and score values. The last data point is highlighted with a different color and larger radius, so you know it represents the most recent score.

### step 6: Review & Compare:
Use the visual comparison between your actual data (solid line) and the benchmark (dotted line) to quickly assess how your current performance stacks up against your target or industry standard.

### step 7: Adjust Selections as Needed:
If you want to see different metrics or classes, simply update your selections. The chart will automatically refresh with the new data.
