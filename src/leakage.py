
import pandas as pd
import numpy as np

from sklearn.metrics import normalized_mutual_info_score


def encode_column(series):

    # Handle numerical columns
    if pd.api.types.is_numeric_dtype(series):

        values = pd.to_numeric(series, errors="coerce")

        median = values.median()

        if pd.isna(median):
            return np.zeros(len(values), dtype=int)

        values = values.fillna(median)

        if values.nunique() > 10:

            encoded = pd.qcut(
                values,
                q=10,
                labels=False,
                duplicates="drop"
            )

            return encoded.to_numpy()

        return values.to_numpy()

    # Handle categorical columns
    return pd.factorize(
        series.fillna("MISSING")
    )[0]


def detect_leakage(df, target):

    findings = []

    if target not in df.columns:
        raise ValueError("Target column not found.")

    target_values = encode_column(df[target])

    for col in df.columns:

        if col == target:
            continue

        if df[col].nunique(dropna=True) <= 1:
            continue

        feature_values = encode_column(df[col])

        score = normalized_mutual_info_score(
            target_values,
            feature_values
        )

        if score >= 0.85:

            findings.append({
                "feature": col,
                "score": round(float(score), 3),
                "warning": "Potential leakage or strong association"
            })

    return findings
