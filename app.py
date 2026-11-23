
import streamlit as st
import pandas as pd
import plotly.express as px

from src.analyzer import analyze_dataset
from src.leakage import detect_leakage


st.set_page_config(
    page_title="LeakLens | Dataset Auditor",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0B1120;
    color: #E2E8F0;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Main headings */
h1, h2, h3 {
    color: #F1F5F9 !important;
    font-weight: 700 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #172554, #1E293B);
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 12px;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
    border: 1px solid #38BDF8;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background-color: #172033;
    border: 1px dashed #38BDF8;
    border-radius: 12px;
    padding: 15px;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 10px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Horizontal divider */
hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div style="
    padding: 25px 30px;
    border-radius: 15px;
    background: linear-gradient(120deg, #172554, #1E40AF);
    border: 1px solid #3B82F6;
    margin-bottom: 25px;
">
    <h1 style="color: white; margin: 0; font-size: 38px;">
        🔍 LeakLens
    </h1>
    <p style="color: #BFDBFE; font-size: 17px; margin-top: 8px;">
        Intelligent Dataset Auditor & Data Leakage Detector
    </p>
    <p style="color: #DBEAFE; font-size: 14px; margin-bottom: 0;">
        Discover hidden data quality issues. Detect suspicious patterns.
        Build better ML datasets.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:

    st.markdown("""
    <h2 style="color:#38BDF8;">🔍 LeakLens</h2>
    <p style="color:#94A3B8;">Dataset Intelligence Platform</p>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📌 About LeakLens")

    st.write(
        "LeakLens analyzes datasets, identifies data quality "
        "issues and detects suspicious feature-target relationships."
    )

    st.divider()

    st.markdown("### 🛠️ Technology Stack")

    st.markdown("""
    - Python
    - Pandas & NumPy
    - Scikit-learn
    - Streamlit
    - Plotly
    """)

    st.divider()

    st.markdown("### 📊 Analysis Modules")

    st.markdown("""
    - Dataset Overview
    - Missing Values
    - Duplicate Detection
    - Outlier Detection
    - High Cardinality
    - Leakage Detection
    - Dataset Health Score
    - Audit Reports
    """)

    st.divider()

    st.caption("LeakLens | Built with Python")
    st.caption("Version 1.0")


uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if df.empty or len(df.columns) == 0:
            st.error("The uploaded CSV file is empty.")
            st.stop()

        st.success("Dataset uploaded successfully!")

        # Dataset overview
        results = analyze_dataset(df)

        st.header("1. Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Rows", results["rows"])
        col2.metric("Total Columns", results["columns"])
        col3.metric("Duplicate Rows", results["duplicate_rows"])
        col4.metric("Memory Usage", f'{results["memory_usage"]} KB')

        # Dataset preview
        st.header("2. Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Interactive Data Visualizations
        st.header("📊  Interactive Data Visualizations")

        numerical_cols = results["numerical_columns"]
        categorical_cols = results["categorical_columns"]

        chart_col1, chart_col2 = st.columns(2)

        # Numerical Distribution
        with chart_col1:

            st.subheader("Numerical Distribution")

            if numerical_cols:

                selected_num = st.selectbox(
                    "Select Numerical Column",
                    numerical_cols,
                    key="num_chart"
                )

                fig = px.histogram(
                    df,
                    x=selected_num,
                    title=f"Distribution of {selected_num}",
                    color_discrete_sequence=["#38BDF8"]
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("No numerical columns available.")

        # Categorical Distribution
        with chart_col2:

            st.subheader("Categorical Distribution")

            if categorical_cols:

                selected_cat = st.selectbox(
                    "Select Categorical Column",
                    categorical_cols,
                    key="cat_chart"
                )

                category_counts = (
                    df[selected_cat]
                    .fillna("Missing")
                    .astype(str)
                    .value_counts()
                    .head(15)
                    .reset_index()
                )

                category_counts.columns = [
                    "Category", "Count"
                ]

                fig = px.bar(
                    category_counts,
                    x="Category",
                    y="Count",
                    title=f"Distribution of {selected_cat}",
                    color_discrete_sequence=["#818CF8"]
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info("No categorical columns available.")


        # Data quality analysis
        st.header("3. Data Quality Analysis")

        missing = results["missing_values"]
        missing_df = pd.DataFrame({
            "Column": list(missing.keys()),
            "Missing Values": list(missing.values())
        })

        missing_df = missing_df[
            missing_df["Missing Values"] > 0
        ]

        if not missing_df.empty:
            st.warning("Missing values detected!")
            fig = px.bar(
                missing_df,
                x="Column",
                y="Missing Values",
                title="Missing Values by Column"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("No missing values found!")

        if results["constant_columns"]:
            st.warning(
                f'Constant columns: {results["constant_columns"]}'
            )
        else:
            st.success("No constant columns found!")

        st.write(
            f'**Duplicate rows:** {results["duplicate_rows"]}'
        )

        # Outlier Detection
        st.header("4. Outlier Detection")

        outlier_data = results["outliers"]

        if outlier_data:
            outlier_rows = []

            for column, details in outlier_data.items():
                outlier_rows.append({
                    "Column": column,
                    "Outlier Count": details["count"],
                    "Outlier Values": str(details["values"])
                })

            outlier_df = pd.DataFrame(outlier_rows)

            st.dataframe(
                outlier_df,
                use_container_width=True
            )

            total_outliers = sum(
                item["count"] for item in outlier_data.values()
            )

            st.metric("Total Potential Outliers", total_outliers)

        else:
            st.info("No numerical columns available for outlier detection.")

        
        # High Cardinality Detection
        st.header("5. High Cardinality Detection")

        high_cardinality = results["high_cardinality_columns"]

        if high_cardinality:

            high_cardinality_df = pd.DataFrame(high_cardinality)

            st.warning(
                "High cardinality columns detected!"
            )

            st.dataframe(
                high_cardinality_df,
                use_container_width=True
            )

        else:
            st.success(
                "No high cardinality columns detected!"
            )


        # Potential leakage detection
        st.header("4. Data Leakage Detection")

        target = st.selectbox(
            "Select your target column",
            options=df.columns.tolist()
        )

        if st.button("Detect Potential Leakage"):

            if df[target].nunique(dropna=True) < 2:
                st.warning(
                    "The selected target needs at least two distinct values."
                )
            else:
                findings = detect_leakage(df, target)

                if findings:
                    st.warning(
                        "Potential leakage or unusually strong "
                        "feature-target association detected."
                    )
                    st.dataframe(
                        pd.DataFrame(findings),
                        use_container_width=True
                    )
                else:
                    st.success(
                        "No suspicious high-association features detected."
                    )

        # Dataset health score
        st.header("5. Dataset Health Score")

        total_cells = df.shape[0] * df.shape[1]

        missing_count = int(df.isnull().sum().sum())

        missing_rate = (
            missing_count / total_cells
            if total_cells > 0 else 0
        )

        duplicate_rate = (
            results["duplicate_rows"] / len(df)
            if len(df) > 0 else 0
        )

        constant_rate = (
            len(results["constant_columns"]) / len(df.columns)
            if len(df.columns) > 0 else 0
        )

        health_score = max(
            0,
            round(
                100
                - (missing_rate * 40)
                - (duplicate_rate * 30)
                - (constant_rate * 30)
            )
        )

        st.metric("Dataset Health Score", f"{health_score}/100")
        st.progress(health_score / 100)

        st.caption(
            "This is a heuristic score based on missing values, "
            "duplicate rows and constant columns. It is not a "
            "formal measure of model readiness."
        )


        # Detailed Audit Report
        st.header("6. Detailed Audit Report")

        report_lines = [
            "========================================",
            "          LEAKLENS AUDIT REPORT",
            "========================================",
            "",
            "1. DATASET OVERVIEW",
            f"Total Rows: {results['rows']}",
            f"Total Columns: {results['columns']}",
            f"Duplicate Rows: {results['duplicate_rows']}",
            f"Memory Usage: {results['memory_usage']} KB",
            "",
            "2. MISSING VALUES"
        ]

        for col, count in results["missing_values"].items():
            report_lines.append(f"{col}: {count}")

        report_lines.extend([
            "",
            "3. CONSTANT COLUMNS",
            str(results["constant_columns"]),
            "",
            "4. HIGH CARDINALITY COLUMNS"
        ])

        for item in results["high_cardinality_columns"]:
            report_lines.append(
                f"{item['column']}: {item['unique_values']} unique values"
            )

        report_lines.extend([
            "",
            "5. OUTLIER ANALYSIS"
        ])

        for col, details in results["outliers"].items():
            report_lines.append(
                f"{col}: {details['count']} outliers"
            )
            report_lines.append(
                f"Outlier Values: {details['values']}"
            )

        report_lines.extend([
            "",
            "6. DATASET HEALTH SCORE",
            f"Health Score: {health_score}/100",
            "",
            "Note: Health score is a heuristic indicator, "
            "not a formal measure of model readiness.",
            "",
            "========================================",
            "       END OF AUDIT REPORT",
            "========================================"
        ])

        report = "\n".join(report_lines)

        st.download_button(
            label="📥 Download Detailed Audit Report",
            data=report,
            file_name="LeakLens_Detailed_Audit_Report.txt",
            mime="text/plain"
        )
    except Exception as e:
        st.error(f"Unable to analyze this CSV: {e}")