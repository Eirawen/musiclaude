"""Train quality classifier on extracted musical features."""

import argparse
import logging
import os

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, f1_score, classification_report,
    mean_squared_error, r2_score
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

# Columns to exclude from features
NON_FEATURE_COLS = {"filepath", "rating", "n_ratings", "instrument_names", "basename"}


def _detect_device() -> str:
    """Detect whether GPU is available for XGBoost."""
    try:
        info = xgb.build_info()
        if info.get("USE_CUDA"):
            logger.info("GPU detected — using CUDA for XGBoost training")
            return "cuda"
    except Exception:
        pass
    logger.info("No GPU detected — using CPU for XGBoost training")
    return "cpu"


def load_and_prepare(csv_path: str, min_ratings: int = 3) -> tuple[pd.DataFrame, pd.Series]:
    """Load features CSV and prepare for training.

    Filters out unrated scores and those with too few ratings.
    Returns feature matrix X and target series y (rating).
    """
    df = pd.read_csv(csv_path)

    # Filter: must have rating > 0 and enough ratings for reliability
    if "rating" not in df.columns:
        raise ValueError("CSV must contain a 'rating' column. Did you join with PDMX.csv?")

    df = df[df["rating"] > 0]
    if "n_ratings" in df.columns:
        df = df[df["n_ratings"] >= min_ratings]

    logger.info(f"Training on {len(df)} scored samples")

    feature_cols = [c for c in df.columns if c not in NON_FEATURE_COLS]
    # Drop columns that are all NaN
    X = df[feature_cols].apply(pd.to_numeric, errors='coerce')
    X = X.dropna(axis=1, how='all')
    y = df["rating"]

    # Align indices after filtering
    mask = X.notna().all(axis=1)
    X = X[mask]
    y = y.loc[X.index]

    return X, y


def train_binary_classifier(X: pd.DataFrame, y: pd.Series, threshold: float = 4.0, device: str | None = None):
    """Train binary classifier: good (rating >= threshold) vs not good."""
    if device is None:
        device = _detect_device()

    y_binary = (y >= threshold).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
    )

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
        device=device,
        tree_method="hist",
    )

    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger.info(f"Binary classifier — Accuracy: {acc:.3f}, F1: {f1:.3f}")
    logger.info(f"\n{classification_report(y_test, y_pred, target_names=['not good', 'good'])}")

    return model, {"accuracy": acc, "f1": f1, "feature_names": list(X.columns)}


def train_regressor(X: pd.DataFrame, y: pd.Series, device: str | None = None):
    """Train regression model to predict continuous rating."""
    if device is None:
        device = _detect_device()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        device=device,
        tree_method="hist",
    )

    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    y_pred = model.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)
    logger.info(f"Regressor — RMSE: {rmse:.3f}, R²: {r2:.3f}")

    return model, {"rmse": rmse, "r2": r2, "feature_names": list(X.columns)}


def plot_feature_importance(model, feature_names: list, output_path: str, title: str = "Feature Importance"):
    """Plot and save feature importance chart."""
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1]

    # Top 20 features
    n_show = min(20, len(feature_names))

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(
        range(n_show),
        importance[indices[:n_show]][::-1],
        align="center",
    )
    ax.set_yticks(range(n_show))
    ax.set_yticklabels([feature_names[i] for i in indices[:n_show]][::-1])
    ax.set_xlabel("Importance")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Saved feature importance plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Train music quality classifier")
    parser.add_argument("--features", required=True, help="Path to features CSV")
    parser.add_argument("--output", default="models", help="Output directory for models")
    parser.add_argument("--threshold", type=float, default=4.0, help="Rating threshold for binary classification")
    parser.add_argument("--min-ratings", type=int, default=3, help="Minimum number of ratings per score")
    parser.add_argument("--cpu", action="store_true", help="Force CPU even if GPU is available")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    os.makedirs(args.output, exist_ok=True)

    device = "cpu" if args.cpu else _detect_device()

    X, y = load_and_prepare(args.features, min_ratings=args.min_ratings)

    # Binary classifier
    clf, clf_metrics = train_binary_classifier(X, y, threshold=args.threshold, device=device)
    clf_path = os.path.join(args.output, "quality_classifier.joblib")
    joblib.dump({"model": clf, "metrics": clf_metrics}, clf_path)
    plot_feature_importance(
        clf, clf_metrics["feature_names"],
        os.path.join(args.output, "classifier_importance.png"),
        title="Binary Classifier Feature Importance"
    )

    # Regressor
    reg, reg_metrics = train_regressor(X, y, device=device)
    reg_path = os.path.join(args.output, "quality_regressor.joblib")
    joblib.dump({"model": reg, "metrics": reg_metrics}, reg_path)
    plot_feature_importance(
        reg, reg_metrics["feature_names"],
        os.path.join(args.output, "regressor_importance.png"),
        title="Rating Regressor Feature Importance"
    )

    # Distribution scorer (anomaly detection — works even on LLM-generated music)
    from musiclaude.classifier.distribution import DistributionScorer

    # Fit on ALL features (not just rated ones) — we want the full distribution
    all_df = pd.read_csv(args.features)
    scorer = DistributionScorer()
    scorer_stats = scorer.fit(all_df)
    scorer_path = os.path.join(args.output, "distribution_scorer.joblib")
    scorer.save(scorer_path)
    logger.info(
        f"Distribution scorer fitted on {scorer_stats['n_samples']} samples, "
        f"{scorer_stats['n_features']} features"
    )

    logger.info(f"Models saved to {args.output}/")


if __name__ == "__main__":
    main()
