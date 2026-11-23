# 🔍 LeakLens – Intelligent Dataset Auditor & Data Leakage Detector

LeakLens is a Python-based dataset auditing tool designed to help users identify data quality issues and potential data leakage before using datasets for Machine Learning.

It provides an interactive dashboard where users can upload CSV files, explore dataset characteristics, detect anomalies, and generate detailed audit reports.
## 🖥️ Dashboard Preview

![LeakLens Dashboard](assets/dashboard.png)

## 🚀 Features

- **Dataset Overview:** View total rows, columns, duplicate rows, and memory usage.
- **Dataset Preview:** Explore uploaded CSV data directly through the dashboard.
- **Missing Value Detection:** Identify missing values across dataset columns.
- **Duplicate Detection:** Find duplicate records in the dataset.
- **Constant Column Detection:** Identify columns containing only one unique value.
- **High Cardinality Detection:** Flag categorical columns with a large number of unique values.
- **Outlier Detection:** Identify unusual numerical values.
- **Data Visualization:** Explore numerical and categorical data through interactive charts.
- **Data Leakage Screening:** Identify suspiciously strong feature-target associations using Normalized Mutual Information (NMI).
- **Dataset Health Score:** Get a heuristic indicator of overall dataset quality.
- **Audit Report Generation:** Download a detailed dataset audit report.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| Scikit-learn | Mutual information-based analysis |
| Streamlit | Interactive web dashboard |
| Plotly | Data visualization |

## 📁 Project Structure

```text
LeakLens/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│
├── sample_data/
│
└── src/
    ├── __init__.py
    ├── analyzer.py
    └── leakage.py
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/samridhisinha308/LeakLens.git
```

### 2. Navigate to the project folder

```bash
cd LeakLens
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## 📊 How It Works

1. Upload a CSV dataset.
2. LeakLens analyzes its structure and data quality.
3. Explore missing values, duplicates, outliers, and other potential issues.
4. Select a target column to screen for suspicious feature-target associations.
5. Review the dataset health score.
6. Download the detailed audit report.

## ⚠️ Important Note

LeakLens is designed as a preliminary dataset auditing and screening tool.

A high feature-target association does not automatically prove data leakage. Similarly, the dataset health score is a heuristic indicator and should not be treated as a formal measure of model readiness.

## 🔮 Future Improvements

- Support for additional dataset formats.
- More advanced data leakage detection techniques.
- Automated data cleaning suggestions.
- Detailed visual audit summaries.
- Machine Learning-based anomaly detection.

## 👩‍💻 Author

**Samridhi Sinha**

B.Tech – Computer Science & Engineering (AI & ML)

---

*Built with Python, curiosity, and a focus on better Machine Learning workflows.*