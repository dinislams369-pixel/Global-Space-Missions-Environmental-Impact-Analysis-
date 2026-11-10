 # 🚀 Global Space Missions: Environmental Impact Analysis and Prediction

**An Introduction to Data Science project** using Python, exploratory data analysis, machine learning classification, and an interactive Streamlit dashboard.

This project explores a supplied dataset of 3,000 space-mission records from 2000 to 2025. It examines mission activity, countries, mission types, budgets, success rates, technologies, launch sites, and the dataset's existing environmental-impact labels.

> **Important interpretation note:** `Environmental Impact` is a categorical label supplied in the dataset. It is not a measured greenhouse-gas emissions value. The notebook's best tested classifier, Logistic Regression, achieved 35.50% accuracy on the held-out test set. This is weak performance, so the model should not be treated as a reliable prediction system.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Dataset](#dataset)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Data Science Workflow](#data-science-workflow)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Machine Learning](#machine-learning)
- [Model Results](#model-results)
- [Interactive Dashboard](#interactive-dashboard)
- [Installation](#installation)
- [Run the Dashboard](#run-the-dashboard)
- [Open the Notebook](#open-the-notebook)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

Space exploration involves missions carried out by different countries using different mission types, launch sites, satellite categories, and technologies. This project applies data science methods to explore patterns in a structured space-mission dataset.

The repository contains:

1. A Jupyter Notebook documenting data inspection, preprocessing, exploratory analysis, and machine learning experiments.
2. A CSV dataset used by the notebook and dashboard.
3. A Streamlit web application for interactive data exploration and visualization.

The dashboard is descriptive. It helps users explore the supplied records; it does not provide a validated environmental-impact prediction service.

## Objectives

- Understand and inspect a structured dataset of global space missions.
- Check data types, missing values, and duplicate records.
- Perform exploratory data analysis (EDA).
- Visualize mission distributions, trends, budgets, success rates, technologies, and launch sites.
- Examine correlations among numerical variables.
- Prepare numerical and categorical features for machine learning.
- Train and compare classification algorithms for the existing `Environmental Impact` label.
- Present dataset patterns through an interactive dashboard.

## Dataset

**File:** `data/Global_Space_Exploration_Dataset.csv`

| Property | Description |
|---|---|
| Dataset name | Global Space Exploration Dataset |
| Records | 3,000 |
| Columns | 12 |
| Year range | 2000-2025 |
| Target column | `Environmental Impact` |
| Target categories | Low, Medium, High |

### Dataset columns

| Column | Description |
|---|---|
| `Country` | Country associated with the mission |
| `Year` | Mission year |
| `Mission Name` | Mission name or description |
| `Mission Type` | Mission category, such as Manned or Unmanned |
| `Launch Site` | Launch location |
| `Satellite Type` | Satellite category |
| `Budget (in Billion $)` | Mission budget in billions of dollars |
| `Success Rate (%)` | Mission success rate percentage |
| `Technology Used` | Technology associated with the mission |
| `Environmental Impact` | Existing categorical label: Low, Medium, or High |
| `Collaborating Countries` | Countries participating in the mission |
| `Duration (in Days)` | Mission duration in days |

The dataset is included as supplied for this academic project. Confirm the dataset's original source and redistribution terms before reusing it in another project.

## Technology Stack

| Technology | Use |
|---|---|
| Python | Main programming language |
| Jupyter Notebook | Analysis and model experimentation |
| Pandas | Data loading and manipulation |
| NumPy | Numerical operations |
| Matplotlib | Visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Preprocessing, classification, and evaluation |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts |
| Git and GitHub | Version control and project hosting |

## Repository Structure

```text
Global-Space-Missions-Environmental-Impact-Analysis/
│
├── app/
│   └── app.py
│
├── data/
│   └── Global_Space_Exploration_Dataset.csv
│
├── notebooks/
│   └── Global_Space_Mission.ipynb
│
├── screenshots/
│   ├── 01-overview-dashboard.png
│   ├── 02-countries-and-technology.png
│   ├── 03-mission-analysis.png
│   ├── 04-data-explorer.png
│   ├── 05-countries-and-technology-filtered.png
│   └── 06-overview-filtered.png
│
├── docs/
│   └── Dashboard documentation PDFs
│
├── README.md
├── requirements.txt
└── .gitignore
```

### Folder descriptions

- `app/`: Streamlit dashboard source code.
- `data/`: CSV dataset used by the project.
- `notebooks/`: Jupyter Notebook containing the data science workflow.
- `screenshots/`: Dashboard screenshots showing the Overview, Countries & Technology, Mission Analysis, Data Explorer, and filtered dashboard views.
- `docs/`: Dashboard documentation PDF files and supporting project documents. Keep the final, clearly named PDF here and remove obsolete draft copies when you have confirmed which version is final.
- `requirements.txt`: Python packages required to run the notebook and dashboard.
- `.gitignore`: Excludes virtual environments, caches, and local secrets.

## Data Science Workflow

The project follows these stages:

1. **Data loading:** Read the CSV dataset using Pandas.
2. **Data inspection:** Review the first records, dimensions, columns, data types, and descriptive statistics.
3. **Data quality checks:** Examine missing values and duplicate records.
4. **Target analysis:** Explore the distribution of Low, Medium, and High impact labels.
5. **Exploratory data analysis:** Study categorical and numerical variables using charts.
6. **Correlation analysis:** Examine linear correlations among selected numerical variables.
7. **Feature and target selection:** Use all columns except `Environmental Impact` as input features and use `Environmental Impact` as the target.
8. **Train-test split:** Divide records into 80% training and 20% testing subsets, using stratification and `random_state=42`.
9. **Preprocessing:** Impute missing numerical values using the median and scale them; impute categorical values using the most frequent value and apply one-hot encoding.
10. **Model training and evaluation:** Train four classifiers and compare their test accuracy and classification performance.
11. **Dashboard development:** Build interactive visualizations and filtered record exploration using Streamlit and Plotly.

## Exploratory Data Analysis

The notebook explores:

- Environmental-impact category distribution.
- Country-wise mission distribution.
- Mission-type and satellite-type distributions.
- Launch-site and technology usage.
- Numerical feature distributions.
- Box plots and scatter plots.
- Relationships between mission attributes and impact labels.
- Correlation heatmap for selected numerical variables.

Numerical variables include `Year`, `Budget (in Billion $)`, `Success Rate (%)`, and `Duration (in Days)`.

## Machine Learning

### Target

`Environmental Impact`

The three target classes are:

- Low
- Medium
- High

### Input features

All dataset columns other than `Environmental Impact` are used as input features in the notebook's experiment.

### Preprocessing

**Numerical pipeline**
- Median imputation.
- Standard scaling.

**Categorical pipeline**
- Most-frequent-value imputation.
- One-hot encoding with unknown categories ignored.

The numerical and categorical transformations are combined using a Scikit-learn `ColumnTransformer` and pipeline.

### Algorithms evaluated

1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
4. K-Nearest Neighbors (KNN)

## Model Results

The notebook reports the following accuracy values on the 600-record test set:

| Model | Test accuracy |
|---|---:|
| Logistic Regression | 35.50% |
| Decision Tree | 33.67% |
| Random Forest | 33.67% |
| K-Nearest Neighbors | 34.50% |

Logistic Regression achieved the highest accuracy among the four tested models. Its classification report and confusion matrix are included in the notebook.

**Interpretation:** 35.50% accuracy is weak performance. The best result in this experiment does not establish that the classifier is reliable. Do not use it for real-world environmental, scientific, operational, or policy decisions.

## Interactive Dashboard

Run the Streamlit application to explore the dataset through four sections.

### Overview
- KPI cards for mission count, country count, average success rate, average budget, and High-label share.
- Environmental-impact distribution.
- Mission activity over time.
- Mission types by impact label.
- Countries with the most missions.

### Countries & Technology
- Country comparisons by impact category.
- Technology usage.
- Leading launch sites.
- Satellite-type distribution.

### Mission Analysis
- Mission budget versus success rate.
- Average success rate by mission type.
- Budget distributions by impact label.
- Mission-duration distributions by mission type.

### Data Explorer
- Search mission records by mission name, country, launch site, or technology.
- Inspect filtered records.
- Download filtered records as CSV.
- Review dataset quality information.

All dashboard charts and tables respond to the sidebar filters.

### Dashboard screenshots and documentation

The `screenshots/` folder contains six captured views of the dashboard, including the main sections and examples of filtered results.

The `docs/` folder contains PDF documentation for the dashboard. For a clean final submission, keep the approved final PDF and give it a clear filename such as `Global_Space_Missions_Dashboard_Documentation.pdf`. If multiple draft PDFs are retained, label them clearly as drafts or versions.

## Installation

### Prerequisites

- Python 3.10 or later.
- pip.
- Jupyter Notebook or JupyterLab (optional, for the notebook).

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username:

```bash
git clone https://github.com/YOUR-USERNAME/Global-Space-Missions-Environmental-Impact-Analysis.git
cd Global-Space-Missions-Environmental-Impact-Analysis
```

Alternatively, download the repository ZIP from GitHub and open the extracted folder in a terminal.

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Dashboard

Run this command from the repository root directory:

```bash
python -m streamlit run app/app.py
```

Open the local URL printed in the terminal, usually:

```text
http://localhost:8501
```

The dashboard expects the dataset at:

```text
data/Global_Space_Exploration_Dataset.csv
```

Keep the folder and filename exactly as shown.

## Open the Notebook

From the repository root, start Jupyter:

```bash
jupyter notebook
```

Open:

```text
notebooks/Global_Space_Mission.ipynb
```

The notebook's dataset-loading cells have been adjusted to read the CSV from `../data/Global_Space_Exploration_Dataset.csv` when the notebook is run with `notebooks/` as its working directory.

## Limitations

- Environmental-impact values are predefined categories in the supplied dataset, not measured emissions.
- The tested classifiers achieved low accuracy.
- Correlation does not prove causation.
- The analysis reflects the supplied dataset and should not be generalized to all real-world space missions.
- The dashboard is intended for descriptive exploration, not validated prediction.

## Future Improvements

- Replace or supplement the dataset with independently verified mission data.
- Add measured launch emissions, fuel consumption, and other environmental indicators.
- Investigate feature quality and class balance.
- Apply cross-validation and hyperparameter tuning.
- Evaluate additional models and validate performance before considering a prediction feature.
- Deploy the dashboard online.

## Author

**Din Islam Sheikh**  
B.Tech, Computer Science and Engineering  
Assam Downtown University  
Course: Introduction to Data Science

## Academic Use and Dataset Attribution

This repository was assembled for an academic data science project. Add the dataset source citation and any applicable dataset license or usage terms here when confirmed. No software license is granted by this README alone.
