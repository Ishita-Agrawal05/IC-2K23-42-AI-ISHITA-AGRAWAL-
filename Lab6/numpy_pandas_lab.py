"""Lab 6: NumPy and Pandas examples."""

from __future__ import annotations

import numpy as np
import pandas as pd


def numpy_demo() -> None:
    array = np.array([[1, 2, 3], [4, 5, 6]])
    print("NumPy array:\n", array)
    print("Mean of all values:", array.mean())
    print("Row sums:", array.sum(axis=1))


def pandas_demo() -> None:
    df = pd.DataFrame(
        {
            "student": ["A", "B", "C", "D"],
            "math": [85, 90, 78, 88],
            "science": [80, 92, 75, 89],
        }
    )
    print("\nPandas DataFrame:\n", df)
    print("\nGrouped average:\n", df[["math", "science"]].mean())
    print("\nTop math scores:\n", df.nlargest(2, "math"))


def main() -> None:
    numpy_demo()
    pandas_demo()


if __name__ == "__main__":
    main()
