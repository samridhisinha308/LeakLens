import pandas as pd
import numpy as np
def analyze_dataset(df):
    results = {}
    # Basic dataset information
    results["rows"] = df.shape[0]
    results["columns"] = df.shape[1]
    # Missing values
    results["missing_values"] = (
        df.isnull().sum().to_dict()
    )
    # Duplicate rows
    results["duplicate_rows"] = int(
        df.duplicated().sum()
    )
    # Duplicate columns
    results["duplicate_columns"] = [
        col for col in df.columns
        if df.columns.tolist().count(col) > 1
    ]
    # Constant columns
    results["constant_columns"] = [
        col for col in df.columns
        if df[col].nunique(dropna=False) <= 1
    ]

    # Numerical columns
    results["numerical_columns"] = (
        df.select_dtypes(include=np.number).columns.tolist()
    )
    # Categorical columns
    results["categorical_columns"] = (
        df.select_dtypes(include=["object", "category"]).columns.tolist()
    )
    # High Cardinality Detection
    results["high_cardinality_columns"] = []

    for col in results["categorical_columns"]:

        unique_count = df[col].nunique(dropna=True)

        if unique_count > 20:
            results["high_cardinality_columns"].append({
                "column": col,
                "unique_values": int(unique_count),
                "total_rows": len(df)
            })

    # Memory usage
    results["memory_usage"] = round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    )

    # Outlier Detection using IQR
    results["outliers"] = {}

    for col in results["numerical_columns"]:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower_limit = Q1 - 1.5 * IQR
        upper_limit = Q3 + 1.5 * IQR

        outliers = df[
            (df[col] < lower_limit) |
            (df[col] > upper_limit)
        ][col]

        results["outliers"][col] = {
            "count": int(len(outliers)),
            "values": outliers.tolist()
        }

    return results
