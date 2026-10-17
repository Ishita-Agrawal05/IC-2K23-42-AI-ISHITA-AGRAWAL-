"""Lab 4: advanced preprocessing and feature preparation."""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [21, 25, 29, 35, 42, 45, None, 30],
            "income": [20000, 26000, 29000, 41000, 50000, 61000, 43000, None],
            "city": ["Dhaka", "Chottogram", "Sylhet", "Dhaka", "Khulna", "Rajshahi", "Dhaka", "Chottogram"],
            "student": ["yes", "no", "yes", "no", "yes", "no", "yes", "no"],
            "target": [0, 1, 1, 0, 1, 1, 0, 0],
        }
    )


def build_pipeline() -> Pipeline:
    numeric_features = ["age", "income"]
    categorical_features = ["city", "student"]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return Pipeline(
        steps=[
            (
                "preprocessor",
                ColumnTransformer(
                    transformers=[
                        ("numeric", numeric_transformer, numeric_features),
                        ("categorical", categorical_transformer, categorical_features),
                    ]
                ),
            )
        ]
    )


def main() -> None:
    df = build_dataset()
    print("Original dataset:\n", df)
    print("\nMissing values before preprocessing:\n", df.isnull().sum())

    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    pipeline = build_pipeline()
    X_train_prepared = pipeline.fit_transform(X_train)
    X_test_prepared = pipeline.transform(X_test)

    print("\nPrepared train matrix shape:", X_train_prepared.shape)
    print("Prepared test matrix shape:", X_test_prepared.shape)
    print("\nFeature preparation complete.")


if __name__ == "__main__":
    main()
