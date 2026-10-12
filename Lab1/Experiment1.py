"""Lab 1: AI environment and package verification."""

import importlib.util
import platform
import sys


def check_package(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def main() -> None:
    print("=== AI Environment Check ===")
    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")

    packages = ["numpy", "pandas", "matplotlib", "seaborn", "sklearn", "jupyter"]
    print("\nPackage availability:")
    for package in packages:
        status = "installed" if check_package(package) else "not installed"
        print(f"  - {package}: {status}")


if __name__ == "__main__":
    main()
