# Classifier Gotchas

## PDMX ratings are popularity-biased

MuseScore ratings correlate with views, favorites, and genre popularity. A mediocre anime piano cover may outrate a well-arranged original piece. The classifier will learn some of this bias.

**Mitigation:** Feature importance analysis will reveal if the model is learning "popular genres" vs "musical quality." If genre-proxy features dominate, consider controlling for genre.

## Class imbalance in binary classification

If most rated scores are ≥ 4.0 stars, the binary classifier will have class imbalance. Current code uses `stratify=y_binary` in train_test_split to ensure balanced splits. May need SMOTE or class weights if imbalance is severe (> 80/20).

## GPU model saved, CPU inference

Models trained on GPU can be loaded and used for prediction on CPU. XGBoost handles this transparently but emits a warning about "mismatched devices." This is cosmetic, not functional.

## Feature name ordering matters for prediction

The predictor uses `clf_metrics["feature_names"]` to select and order columns from the feature dict. If a feature is missing from the dict, it gets filled with 0. If feature names change between training and prediction, predictions will be garbage.
