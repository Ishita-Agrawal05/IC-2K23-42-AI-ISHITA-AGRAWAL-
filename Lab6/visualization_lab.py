"""Lab 7: visualization example with Matplotlib and Seaborn."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def build_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "course": ["AI", "ML", "DL", "NLP", "CV"],
            "students": [120, 150, 200, 180, 210],
            "marks": [78, 82, 88, 84, 90],
        }
    )


def main() -> None:
    df = build_data()
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="course", y="students", palette="deep")
    plt.title("Student Enrollment by Course")
    plt.tight_layout()
    plt.savefig(output_dir / "course_enrollment.png")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="marks", y="students", s=120)
    plt.title("Marks vs Students")
    plt.tight_layout()
    plt.savefig(output_dir / "marks_vs_students.png")

    print("Plots saved to:", output_dir)
    print(df)


if __name__ == "__main__":
    main()
