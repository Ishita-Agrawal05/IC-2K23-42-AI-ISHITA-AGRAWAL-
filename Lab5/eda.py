"""Lab 5: exploratory data analysis example."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def build_sample_sales_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
            "sales": [1200, 1500, 1700, 1600, 2100, 2500, 2750, 2600],
            "profit": [200, 320, 400, 390, 540, 680, 760, 720],
            "marketing": [100, 150, 200, 180, 260, 300, 340, 330],
        }
    )


def run_eda() -> pd.DataFrame:
    df = build_sample_sales_data()
    print("Summary statistics:\n", df.describe())
    print("\nCorrelation matrix:\n", df[["sales", "profit", "marketing"]].corr())

    plt.figure(figsize=(10, 4))
    sns.barplot(data=df, x="month", y="sales")
    plt.title("Monthly Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="marketing", y="sales")
    plt.title("Marketing vs Sales")
    plt.tight_layout()
    plt.show()

    return df


def main() -> None:
    df = run_eda()
    print("\nInsights:")
    print(f"- Maximum sales: {df['sales'].max()}")
    print(f"- Average profit: {df['profit'].mean():.2f}")
    print(f"- Strongest positive relationship: {df[['sales', 'profit', 'marketing']].corr().iloc[0, 1]:.2f}")


if __name__ == "__main__":
    main()
