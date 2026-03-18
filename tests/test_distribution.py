"""Tests for the distribution-based anomaly scorer."""

import numpy as np
import pandas as pd
import pytest
import tempfile
import os

from rachmaniclaude.classifier.distribution import DistributionScorer, DISTRIBUTION_FEATURES


@pytest.fixture
def normal_features_df():
    """Create a DataFrame of 'normal' music features for fitting."""
    np.random.seed(42)
    n = 200

    data = {}
    # Generate plausible distributions for each feature
    data["chord_vocabulary_size"] = np.random.normal(8, 3, n).clip(1, 20)
    data["pct_extended_chords"] = np.random.beta(2, 5, n)
    data["harmonic_rhythm"] = np.random.normal(3, 1.5, n).clip(0.5, 12)
    data["key_stability"] = np.random.beta(8, 2, n)
    data["modulation_count"] = np.random.poisson(1, n)
    data["cadence_count_authentic"] = np.random.poisson(3, n)
    data["cadence_count_half"] = np.random.poisson(4, n)
    data["cadence_count_plagal"] = np.random.poisson(1, n)
    data["avg_interval_size"] = np.random.normal(3, 1, n).clip(0.5, 10)
    data["pct_stepwise"] = np.random.beta(5, 2, n)
    data["melodic_range"] = np.random.normal(18, 6, n).clip(3, 48)
    data["pct_rising"] = np.random.beta(3, 3, n)
    data["pct_falling"] = np.random.beta(3, 3, n)
    data["pct_static"] = np.random.beta(1, 10, n)
    data["rhythmic_variety"] = np.random.normal(5, 2, n).clip(1, 15)
    data["repetition_density"] = np.random.beta(2, 5, n)
    data["num_parts"] = np.random.choice([1, 2, 3, 4], n, p=[0.3, 0.3, 0.2, 0.2])
    data["total_duration_beats"] = np.random.normal(64, 32, n).clip(8, 256)
    data["dynamics_count"] = np.random.poisson(5, n)
    data["tempo_count"] = np.random.poisson(1, n).clip(0, 5)
    data["time_sig_complexity"] = np.random.choice([0.0, 0.5, 1.0], n, p=[0.7, 0.1, 0.2])
    data["instrument_count"] = np.random.choice([1, 2, 3, 4], n, p=[0.3, 0.3, 0.2, 0.2])
    data["voice_crossing_count"] = np.random.poisson(2, n)
    data["doubling_score"] = np.random.beta(2, 5, n)
    data["note_density"] = np.random.normal(1.2, 0.4, n).clip(0.1, 4)
    data["rest_ratio"] = np.random.beta(2, 8, n)
    data["pitch_class_entropy"] = np.random.normal(2.8, 0.3, n).clip(0, 3.58)
    data["interval_entropy"] = np.random.normal(3.0, 0.5, n).clip(0, 5)
    data["melodic_autocorrelation"] = np.random.normal(0.4, 0.2, n).clip(-1, 1)
    data["phrase_length_regularity"] = np.random.beta(2, 5, n)
    data["strong_beat_consonance"] = np.random.beta(8, 2, n)
    data["rhythmic_independence"] = np.random.beta(3, 3, n)

    return pd.DataFrame(data)


class TestDistributionScorer:
    def test_fit(self, normal_features_df):
        scorer = DistributionScorer()
        stats = scorer.fit(normal_features_df)

        assert stats["n_samples"] == 200
        assert stats["n_features"] > 20
        assert scorer._is_fitted

    def test_score_normal(self, normal_features_df):
        scorer = DistributionScorer()
        scorer.fit(normal_features_df)

        # Score a sample from the same distribution — should be normal
        sample = normal_features_df.iloc[0].to_dict()
        report = scorer.score_features(sample)

        assert report.score >= 0
        assert isinstance(report.is_anomalous, bool)
        assert isinstance(report.feature_deviations, dict)

    def test_score_anomalous(self, normal_features_df):
        scorer = DistributionScorer()
        scorer.fit(normal_features_df)

        # Create obviously anomalous features (LLM failure modes)
        anomalous = {
            "chord_vocabulary_size": 1,       # way too low
            "pct_extended_chords": 0.0,
            "harmonic_rhythm": 50,            # way too slow
            "key_stability": 0.2,             # very atonal
            "modulation_count": 0,
            "cadence_count_authentic": 0,
            "cadence_count_half": 0,
            "cadence_count_plagal": 0,
            "avg_interval_size": 12,          # all octave leaps
            "pct_stepwise": 0.0,
            "melodic_range": 48,              # 4 octaves
            "pct_rising": 0.5,
            "pct_falling": 0.5,
            "pct_static": 0.0,
            "rhythmic_variety": 1,            # all same duration
            "repetition_density": 0.0,
            "num_parts": 1,
            "total_duration_beats": 8,        # very short
            "dynamics_count": 0,
            "tempo_count": 0,
            "time_sig_complexity": 0.0,
            "instrument_count": 1,
            "voice_crossing_count": 0,
            "doubling_score": 0.0,
            "note_density": 0.1,              # way too sparse
            "rest_ratio": 0.0,                # no rests at all
            "pitch_class_entropy": 0.5,       # stuck on few notes
            "interval_entropy": 0.5,          # repetitive intervals
            "melodic_autocorrelation": -0.5,  # anti-structured
            "phrase_length_regularity": 3.0,  # very irregular
            "strong_beat_consonance": 0.1,    # lots of dissonance
            "rhythmic_independence": 0.0,
        }

        report = scorer.score_features(anomalous)

        # Should have high deviations for many features
        extreme_deviations = [
            f for f, z in report.feature_deviations.items() if abs(z) > 2
        ]
        assert len(extreme_deviations) > 5

        # Should generate critiques
        assert len(report.critiques) > 0

    def test_save_load(self, normal_features_df):
        scorer = DistributionScorer()
        scorer.fit(normal_features_df)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "scorer.joblib")
            scorer.save(path)
            assert os.path.exists(path)

            loaded = DistributionScorer.load(path)
            assert loaded._is_fitted

            # Should produce same results
            sample = normal_features_df.iloc[0].to_dict()
            r1 = scorer.score_features(sample)
            r2 = loaded.score_features(sample)
            assert r1.score == pytest.approx(r2.score)

    def test_critiques_are_actionable(self, normal_features_df):
        scorer = DistributionScorer()
        scorer.fit(normal_features_df)

        # LLM-like score: no rests, low pitch variety, no dynamics
        llm_features = normal_features_df.iloc[0].to_dict()
        llm_features["rest_ratio"] = 0.0
        llm_features["pitch_class_entropy"] = 0.5
        llm_features["note_density"] = 4.0
        llm_features["dynamics_count"] = 0
        llm_features["rhythmic_variety"] = 1

        report = scorer.score_features(llm_features)

        # Check that critiques mention specific issues
        all_text = " ".join(report.critiques).lower()
        # At least some of these should be flagged
        assert "rest" in all_text or "density" in all_text or "pitch" in all_text

    def test_unfitted_raises(self):
        scorer = DistributionScorer()
        with pytest.raises(RuntimeError, match="not been fitted"):
            scorer.score_features({"note_density": 1.0})
