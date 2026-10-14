"""Lab 3: data preprocessing example."""

from __future__ import annotations

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def build_sample_data() -> pd.DataFrame:
    data = {
        "age": [25, 30, None, 40, 22, 35, None, 28],
        "income": [50000, 65000, 70000, None, 55000, 80000, 72000, 61000],
        "city": ["New York", "Paris", "London", "Paris", "New York", "London", None, "Paris"],
        "gender": ["F", "M", "F", "M", "F", "M", "F", "M"],
        "purchase": [1, 0, 1, 0, 1, 1, 0, 1],
    }
    return pd.DataFrame(data)


def preprocess_data() -> pd.DataFrame:
    df = build_sample_data()

    numeric_cols = ["age", "income"]
    categorical_cols = ["city", "gender"]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols),
        ]
    )

    transformed = preprocessor.fit_transform(df)
    print("Transformed feature matrix shape:", transformed.shape)
    return df


def main() -> None:
    df = build_sample_data()
    print("Original data:\n", df)
    print("\nMissing values before cleaning:\n", df.isnull().sum())

    cleaned = df.copy()
    cleaned["age"] = cleaned["age"].fillna(cleaned["age"].median())
    cleaned["income"] = cleaned["income"].fillna(cleaned["income"].median())
    cleaned["city"] = cleaned["city"].fillna(cleaned["city"].mode()[0])

    print("\nCleaned data:\n", cleaned)
    print("\nMissing values after cleaning:\n", cleaned.isnull().sum())

    print("\nPreprocessing pipeline demo:")
    preprocess_data()


if __name__ == "__main__":
    main()
