"""Lab 7: explainable digit classification and adversarial robustness."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def fgsm_attack(
    model: LogisticRegression, images: np.ndarray, labels: np.ndarray, epsilon: float
) -> np.ndarray:
    """Perturb normalized images in the direction that increases cross-entropy."""
    scores = model.decision_function(images)
    scores -= scores.max(axis=1, keepdims=True)
    probabilities = np.exp(scores)
    probabilities /= probabilities.sum(axis=1, keepdims=True)

    label_indices = np.searchsorted(model.classes_, labels)
    probabilities[np.arange(len(labels)), label_indices] -= 1.0
    input_gradient = probabilities @ model.coef_
    return np.clip(images + epsilon * np.sign(input_gradient), 0.0, 1.0)


def save_dashboard(
    output_path: Path,
    image: np.ndarray,
    adversarial_image: np.ndarray,
    predicted_label: int,
    adversarial_label: int,
    importance: np.ndarray,
    class_weights: np.ndarray,
    cumulative_variance: np.ndarray,
    accuracy_summary: tuple[float, float, float, float],
) -> None:
    figure, axes = plt.subplots(2, 3, figsize=(14, 8))
    figure.suptitle("Explainable AI and Adversarial Robustness: Digits", fontsize=14)

    axes[0, 0].imshow(image.reshape(8, 8), cmap="gray_r", vmin=0, vmax=1)
    axes[0, 0].set_title(f"Original (prediction: {predicted_label})")
    axes[0, 0].axis("off")
    axes[0, 1].imshow(adversarial_image.reshape(8, 8), cmap="gray_r", vmin=0, vmax=1)
    axes[0, 1].set_title(f"FGSM (prediction: {adversarial_label})")
    axes[0, 1].axis("off")

    importance_plot = axes[0, 2].imshow(importance.reshape(8, 8), cmap="magma")
    axes[0, 2].set_title("Permutation feature importance")
    axes[0, 2].set_xlabel("Pixel column")
    axes[0, 2].set_ylabel("Pixel row")
    figure.colorbar(importance_plot, ax=axes[0, 2], fraction=0.046)

    weight_limit = np.abs(class_weights).max()
    weights_plot = axes[1, 0].imshow(
        class_weights.reshape(8, 8),
        cmap="coolwarm",
        vmin=-weight_limit,
        vmax=weight_limit,
    )
    axes[1, 0].set_title(f"Linear-model pixel weights (class {predicted_label})")
    axes[1, 0].set_xlabel("Pixel column")
    axes[1, 0].set_ylabel("Pixel row")
    figure.colorbar(weights_plot, ax=axes[1, 0], fraction=0.046)

    axes[1, 1].plot(
        np.arange(1, len(cumulative_variance) + 1),
        cumulative_variance,
        marker=".",
        color="#236b5b",
    )
    axes[1, 1].set_title("PCA cumulative explained variance")
    axes[1, 1].set_xlabel("Number of components")
    axes[1, 1].set_ylabel("Variance retained")
    axes[1, 1].set_ylim(0, 1.02)
    axes[1, 1].grid(alpha=0.25)

    axes[1, 2].axis("off")
    full_accuracy, pca_accuracy, adversarial_accuracy, attack_success_rate = accuracy_summary
    axes[1, 2].text(
        0.04,
        0.92,
        "Test-set summary\n\n"
        f"Full-pixel accuracy: {full_accuracy:.3f}\n"
        f"PCA accuracy: {pca_accuracy:.3f}\n"
        f"FGSM accuracy: {adversarial_accuracy:.3f}\n"
        f"Attack success rate: {attack_success_rate:.3f}",
        va="top",
        fontsize=12,
        linespacing=1.8,
    )

    figure.tight_layout()
    figure.savefig(output_path, dpi=160)
    plt.close(figure)


def main() -> None:
    digits = load_digits()
    images = digits.data.astype(np.float64) / 16.0
    labels = digits.target
    x_train, x_test, y_train, y_test = train_test_split(
        images,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    model = LogisticRegression(max_iter=2000)
    model.fit(x_train, y_train)
    original_predictions = model.predict(x_test)
    original_accuracy = accuracy_score(y_test, original_predictions)

    pca = PCA(n_components=20, random_state=42)
    x_train_pca = pca.fit_transform(x_train)
    x_test_pca = pca.transform(x_test)
    pca_model = LogisticRegression(max_iter=2000)
    pca_model.fit(x_train_pca, y_train)
    pca_accuracy = accuracy_score(y_test, pca_model.predict(x_test_pca))

    epsilon = 0.20
    x_adversarial = fgsm_attack(model, x_test, y_test, epsilon)
    adversarial_predictions = model.predict(x_adversarial)
    adversarial_accuracy = accuracy_score(y_test, adversarial_predictions)
    originally_correct = original_predictions == y_test
    attack_success_rate = np.mean(
        adversarial_predictions[originally_correct] != y_test[originally_correct]
    )

    importance_result = permutation_importance(
        model,
        x_test,
        y_test,
        scoring="accuracy",
        n_repeats=3,
        random_state=42,
        n_jobs=-1,
    )
    importance = importance_result.importances_mean
    top_pixels = np.argsort(importance)[::-1][:5]

    sample_index = int(np.flatnonzero(originally_correct)[0])
    predicted_label = int(original_predictions[sample_index])
    adversarial_label = int(adversarial_predictions[sample_index])
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "explainability_dashboard.png"

    save_dashboard(
        output_path,
        x_test[sample_index],
        x_adversarial[sample_index],
        predicted_label,
        adversarial_label,
        importance,
        model.coef_[predicted_label],
        np.cumsum(pca.explained_variance_ratio_),
        (original_accuracy, pca_accuracy, adversarial_accuracy, attack_success_rate),
    )

    print("Lab 7: Explainable AI and Adversarial Robustness")
    print(f"Dataset: sklearn digits ({len(images)} images, 8x8 pixels, 10 classes)")
    print(f"Train/test sizes: {len(x_train)}/{len(x_test)}")
    print(f"Logistic regression test accuracy: {original_accuracy:.3f}")
    print(f"PCA (20 components) test accuracy: {pca_accuracy:.3f}")
    print(f"Variance retained by 20 PCA components: {pca.explained_variance_ratio_.sum():.3f}")
    print(f"FGSM epsilon: {epsilon:.2f}")
    print(f"FGSM adversarial accuracy: {adversarial_accuracy:.3f}")
    print(f"Attack success rate on originally correct images: {attack_success_rate:.3f}")
    print("Most important pixels (row, column; mean accuracy drop):")
    for pixel_index in top_pixels:
        row, column = divmod(int(pixel_index), 8)
        print(f"  ({row}, {column}): {importance[pixel_index]:.4f}")
    print(f"Dashboard saved to: {output_path}")
    print("Note: this linear model uses pixel weights, not CNN Grad-CAM or ResNet.")


if __name__ == "__main__":
    main()