"""Tests for classifier training and prediction modules."""

import os
import tempfile

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_features_csv():
    """Create a sample features CSV for testing."""
    np.random.seed(42)
    n = 100

    data = {
        "filepath": [f"score_{i}.musicxml" for i in range(n)],
        "chord_vocabulary_size": np.random.randint(2, 15, n),
        "pct_extended_chords": np.random.uniform(0, 0.5, n),
        "harmonic_rhythm": np.random.uniform(1, 8, n),
        "key_stability": np.random.uniform(0.5, 1.0, n),
        "modulation_count": np.random.randint(0, 5, n),
        "avg_interval_size": np.random.uniform(1, 6, n),
        "pct_stepwise": np.random.uniform(0.3, 0.9, n),
        "melodic_range": np.random.randint(5, 36, n),
        "pct_rising": np.random.uniform(0.2, 0.6, n),
        "pct_falling": np.random.uniform(0.2, 0.6, n),
        "rhythmic_variety": np.random.randint(2, 10, n),
        "num_parts": np.random.randint(1, 6, n),
        "total_duration_beats": np.random.uniform(16, 256, n),
        "dynamics_count": np.random.randint(0, 20, n),
        "tempo_count": np.random.randint(0, 5, n),
        "rating": np.random.uniform(1.0, 5.0, n),
        "n_ratings": np.random.randint(3, 100, n),
    }

    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        df.to_csv(f, index=False)
        return f.name


class TestTraining:
    def test_load_and_prepare(self, sample_features_csv):
        from musiclaude.classifier.train import load_and_prepare

        X, y = load_and_prepare(sample_features_csv)

        assert len(X) > 0
        assert len(y) > 0
        assert len(X) == len(y)
        assert "filepath" not in X.columns
        assert "rating" not in X.columns

    def test_train_binary_classifier(self, sample_features_csv):
        from musiclaude.classifier.train import load_and_prepare, train_binary_classifier

        X, y = load_and_prepare(sample_features_csv)
        model, metrics = train_binary_classifier(X, y)

        assert model is not None
        assert "accuracy" in metrics
        assert "f1" in metrics
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["f1"] <= 1

    def test_train_regressor(self, sample_features_csv):
        from musiclaude.classifier.train import load_and_prepare, train_regressor

        X, y = load_and_prepare(sample_features_csv)
        model, metrics = train_regressor(X, y)

        assert model is not None
        assert "rmse" in metrics
        assert "r2" in metrics
        assert metrics["rmse"] >= 0

    def test_full_pipeline(self, sample_features_csv):
        from musiclaude.classifier.train import (
            load_and_prepare,
            train_binary_classifier,
            train_regressor,
            plot_feature_importance,
        )
        import joblib

        X, y = load_and_prepare(sample_features_csv)
        clf, clf_metrics = train_binary_classifier(X, y)
        reg, reg_metrics = train_regressor(X, y)

        with tempfile.TemporaryDirectory() as tmpdir:
            clf_path = os.path.join(tmpdir, "clf.joblib")
            joblib.dump({"model": clf, "metrics": clf_metrics}, clf_path)

            reg_path = os.path.join(tmpdir, "reg.joblib")
            joblib.dump({"model": reg, "metrics": reg_metrics}, reg_path)

            assert os.path.exists(clf_path)
            assert os.path.exists(reg_path)

            # Test plot generation
            plot_path = os.path.join(tmpdir, "importance.png")
            plot_feature_importance(clf, clf_metrics["feature_names"], plot_path)
            assert os.path.exists(plot_path)


class TestPrediction:
    def test_predict_from_features(self, sample_features_csv):
        from musiclaude.classifier.train import (
            load_and_prepare,
            train_binary_classifier,
            train_regressor,
        )
        from musiclaude.classifier.predict import QualityPredictor
        import joblib

        X, y = load_and_prepare(sample_features_csv)
        clf, clf_metrics = train_binary_classifier(X, y)
        reg, reg_metrics = train_regressor(X, y)

        with tempfile.TemporaryDirectory() as tmpdir:
            clf_path = os.path.join(tmpdir, "clf.joblib")
            reg_path = os.path.join(tmpdir, "reg.joblib")
            joblib.dump({"model": clf, "metrics": clf_metrics}, clf_path)
            joblib.dump({"model": reg, "metrics": reg_metrics}, reg_path)

            predictor = QualityPredictor(clf_path, reg_path)

            # Create a sample feature dict
            sample = X.iloc[0].to_dict()
            result = predictor.predict_from_features(sample)

            assert "is_good" in result
            assert "good_probability" in result
            assert "predicted_rating" in result
            assert 0 <= result["good_probability"] <= 1
            assert 0 <= result["predicted_rating"] <= 5

    def test_get_feature_deficiencies(self, sample_features_csv):
        from musiclaude.classifier.train import load_and_prepare, train_binary_classifier
        from musiclaude.classifier.predict import QualityPredictor
        import joblib

        X, y = load_and_prepare(sample_features_csv)
        clf, clf_metrics = train_binary_classifier(X, y)

        with tempfile.TemporaryDirectory() as tmpdir:
            clf_path = os.path.join(tmpdir, "clf.joblib")
            joblib.dump({"model": clf, "metrics": clf_metrics}, clf_path)

            predictor = QualityPredictor(clf_path)

            # Test with deliberately bad features
            bad_features = {
                "chord_vocabulary_size": 2,
                "pct_extended_chords": 0.01,
                "key_stability": 0.4,
                "pct_stepwise": 0.2,
                "melodic_range": 3,
                "dynamics_count": 0,
                "tempo_count": 0,
                "rhythmic_variety": 1,
                "voice_crossing_count": 15,
            }
            critiques = predictor.get_feature_deficiencies(bad_features)

            assert len(critiques) > 0
            assert any("harmonic" in c.lower() for c in critiques)
            assert any("dynamics" in c.lower() for c in critiques)
