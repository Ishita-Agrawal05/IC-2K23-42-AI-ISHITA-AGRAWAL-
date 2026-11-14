# Lab 7 - Explainable AI and Adversarial Robustness

This lab builds a small digit-classification application with the scikit-learn
digits dataset. It demonstrates pixel-level feature importance, linear-model
interpretability, PCA, FGSM adversarial examples, and a saved visualization
dashboard. It uses dependencies already listed in the repository's
`requirements.txt`.

## Run

From the repository root:

```bash
python3 Lab7/explainable_digits.py
```

The dashboard is saved to `Lab7/outputs/explainability_dashboard.png`.

## Interpretation and limitations

- Permutation importance measures the change in test accuracy after shuffling
  each pixel feature.
- The coefficient map visualizes how this linear classifier weights pixels
  for its predicted class. It is not a causal explanation.
- PCA compresses the 64 input pixels to 20 components; the lab compares its
  classifier accuracy with the full-pixel classifier.
- FGSM uses the linear classifier's cross-entropy gradient to generate
  adversarial images and reports accuracy and attack success rate.
- This is a lightweight image-classification application, not a CNN. Grad-CAM
  and ResNet require a convolutional neural network and are not implemented
  here; the coefficient map should not be described as Grad-CAM.