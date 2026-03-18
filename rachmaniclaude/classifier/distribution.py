"""Distribution-based anomaly scoring for generated music.

Instead of predicting ratings (which suffers from distribution shift between
human-composed PDMX scores and LLM-generated music), this module learns what
"normal" music looks like from PDMX feature distributions and flags generated
music that deviates significantly.

Two approaches:
1. Mahalanobis distance — parametric, interpretable, tells you WHICH features are off
2. Isolation Forest — non-parametric, handles non-Gaussian features better
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

import joblib
import numpy as np
import pandas as pd
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler

logger = logging.getLogger(__name__)

# Features used for distribution scoring (numeric, meaningful for "normalcy")
# Excludes identifiers and string columns
DISTRIBUTION_FEATURES = [
    # Harmonic
    "chord_vocabulary_size",
    "pct_extended_chords",
    "harmonic_rhythm",
    "key_stability",
    "modulation_count",
    "cadence_count_authentic",
    "cadence_count_half",
    "cadence_count_plagal",
    # Melodic
    "avg_interval_size",
    "pct_stepwise",
    "melodic_range",
    "pct_rising",
    "pct_falling",
    "pct_static",
    "rhythmic_variety",
    "repetition_density",
    # Structural
    "num_parts",
    "total_duration_beats",
    "dynamics_count",
    "tempo_count",
    "time_sig_complexity",
    # Orchestration
    "instrument_count",
    "voice_crossing_count",
    "doubling_score",
    # Coherence
    "note_density",
    "rest_ratio",
    "pitch_class_entropy",
    "interval_entropy",
    "melodic_autocorrelation",
    "phrase_length_regularity",
    "strong_beat_consonance",
    "rhythmic_independence",
]


@dataclass
class AnomalyReport:
    """Report from distribution-based anomaly scoring."""

    score: float  # 0.0 = normal, higher = more anomalous
    is_anomalous: bool
    feature_deviations: dict[str, float] = field(default_factory=dict)
    critiques: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f"Anomaly score: {self.score:.2f} ({'ANOMALOUS' if self.is_anomalous else 'normal'})"]
        if self.critiques:
            lines.append("Deviations from normal music:")
            for c in self.critiques:
                lines.append(f"  - {c}")
        return "\n".join(lines)


class DistributionScorer:
    """Scores music by how much its features deviate from learned distributions.

    Fits on PDMX feature data. Then for new (generated) music, reports:
    - Overall anomaly score
    - Per-feature z-scores (which features are unusual)
    - Human-readable critiques for the most deviant features
    """

    def __init__(self):
        self.scaler: RobustScaler | None = None
        self.feature_names: list[str] = []
        self.medians: np.ndarray | None = None
        self.iqrs: np.ndarray | None = None
        self.isolation_forest: IsolationForest | None = None
        self.feature_ranges: dict[str, tuple[float, float]] = {}  # (p5, p95) per feature
        self._is_fitted = False

    def fit(self, df: pd.DataFrame, feature_cols: list[str] | None = None) -> dict:
        """Fit the scorer on PDMX feature data.

        Args:
            df: DataFrame with feature columns (from extract pipeline)
            feature_cols: which columns to use (defaults to DISTRIBUTION_FEATURES)

        Returns:
            dict with fit statistics
        """
        if feature_cols is None:
            feature_cols = [c for c in DISTRIBUTION_FEATURES if c in df.columns]

        self.feature_names = feature_cols
        X = df[feature_cols].apply(pd.to_numeric, errors="coerce")

        # Drop rows with too many NaNs (>50% missing)
        X = X.dropna(thresh=len(feature_cols) // 2)
        # Fill remaining NaNs with median
        X = X.fillna(X.median())

        if len(X) < 10:
            raise ValueError(f"Need at least 10 samples to fit, got {len(X)}")

        # Store robust statistics for per-feature deviation scoring
        self.medians = X.median().values
        self.iqrs = X.apply(lambda c: c.quantile(0.75) - c.quantile(0.25)).values
        # Avoid zero IQR
        self.iqrs = np.where(self.iqrs == 0, 1.0, self.iqrs)

        # Store percentile ranges for human-readable context
        for i, col in enumerate(feature_cols):
            p5 = float(X[col].quantile(0.05))
            p95 = float(X[col].quantile(0.95))
            self.feature_ranges[col] = (p5, p95)

        # Fit RobustScaler for the isolation forest
        self.scaler = RobustScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Fit Isolation Forest
        self.isolation_forest = IsolationForest(
            n_estimators=200,
            contamination=0.1,  # expect ~10% of PDMX is low-quality
            random_state=42,
        )
        self.isolation_forest.fit(X_scaled)

        self._is_fitted = True

        stats = {
            "n_samples": len(X),
            "n_features": len(feature_cols),
            "feature_names": feature_cols,
            "median_values": {col: float(self.medians[i]) for i, col in enumerate(feature_cols)},
        }
        logger.info(f"DistributionScorer fitted on {len(X)} samples, {len(feature_cols)} features")
        return stats

    def score_features(self, features: dict) -> AnomalyReport:
        """Score a single set of features against the fitted distribution.

        Args:
            features: dict from extract_features_from_file()

        Returns:
            AnomalyReport with anomaly score, per-feature deviations, and critiques
        """
        if not self._is_fitted:
            raise RuntimeError("DistributionScorer has not been fitted. Call fit() first.")

        # Build feature vector, filling missing with median
        values = []
        for i, col in enumerate(self.feature_names):
            val = features.get(col)
            if val is None or (isinstance(val, float) and np.isnan(val)):
                values.append(self.medians[i])
            else:
                values.append(float(val))

        x = np.array(values).reshape(1, -1)

        # Per-feature z-scores (using robust stats: deviation from median / IQR)
        z_scores = (x[0] - self.medians) / self.iqrs
        feature_deviations = {
            col: float(z_scores[i]) for i, col in enumerate(self.feature_names)
        }

        # Isolation Forest anomaly score
        # sklearn returns negative scores for anomalies, positive for normal
        x_scaled = self.scaler.transform(x)
        if_score = -self.isolation_forest.score_samples(x_scaled)[0]
        # Normalize: 0 = normal, higher = more anomalous
        # Typical IF scores: ~0.4-0.5 for normal, >0.5 for anomaly
        anomaly_score = float(if_score)
        is_anomalous = bool(self.isolation_forest.predict(x_scaled)[0] == -1)

        # Generate human-readable critiques for extreme deviations
        critiques = self._generate_critiques(features, z_scores)

        return AnomalyReport(
            score=anomaly_score,
            is_anomalous=is_anomalous,
            feature_deviations=feature_deviations,
            critiques=critiques,
        )

    def _generate_critiques(self, features: dict, z_scores: np.ndarray) -> list[str]:
        """Generate critiques for features that deviate significantly from normal."""
        critiques = []
        THRESHOLD = 2.0  # flag features > 2 IQRs from median

        critique_templates = {
            "note_density": {
                "high": "Note density ({val:.1f} notes/beat) is unusually high. "
                        "Normal range: {low:.1f}-{high:.1f}. Add rests and held notes for breathing room.",
                "low": "Note density ({val:.1f} notes/beat) is unusually low. "
                       "Normal range: {low:.1f}-{high:.1f}. The score feels sparse — add more melodic activity.",
            },
            "rest_ratio": {
                "low": "Almost no rests ({val:.0%} of total duration). "
                       "Normal music has {low:.0%}-{high:.0%} rests. "
                       "Add rests between phrases for natural breathing.",
                "high": "Too many rests ({val:.0%} of total duration). "
                        "Normal range: {low:.0%}-{high:.0%}. The score feels fragmented.",
            },
            "pitch_class_entropy": {
                "low": "Pitch variety is very low (entropy={val:.2f} bits). "
                       "Normal: {low:.2f}-{high:.2f}. The melody is stuck on too few notes.",
                "high": "Pitch distribution is unusually uniform (entropy={val:.2f} bits). "
                        "Normal: {low:.2f}-{high:.2f}. This sounds atonal — establish a tonal center.",
            },
            "interval_entropy": {
                "low": "Melodic intervals are very repetitive (entropy={val:.2f} bits). "
                       "Normal: {low:.2f}-{high:.2f}. Use more varied interval sizes.",
                "high": "Melodic intervals are unusually scattered (entropy={val:.2f} bits). "
                        "Normal: {low:.2f}-{high:.2f}. The melody feels random — use more stepwise motion.",
            },
            "melodic_autocorrelation": {
                "low": "Melody has no detectable structure (autocorrelation={val:.2f}). "
                       "Normal: {low:.2f}-{high:.2f}. Use recurring motifs and sequences.",
            },
            "phrase_length_regularity": {
                "high": "Phrase lengths are very irregular (CV={val:.2f}). "
                        "Normal: {low:.2f}-{high:.2f}. Use more consistent phrase lengths (4 or 8 bars).",
            },
            "strong_beat_consonance": {
                "low": "Too much dissonance on strong beats ({val:.0%} consonant). "
                       "Normal: {low:.0%}-{high:.0%}. Resolve dissonances or move them to weak beats.",
            },
            "rhythmic_independence": {
                "low": "Parts move in near-lockstep (independence={val:.2f}). "
                       "Normal: {low:.2f}-{high:.2f}. Give parts more rhythmic variety.",
            },
            "chord_vocabulary_size": {
                "low": "Only {val:.0f} unique chord types. "
                       "Normal: {low:.0f}-{high:.0f}. Add more harmonic variety.",
            },
            "key_stability": {
                "low": "Key stability is low ({val:.0%} in-key). "
                       "Normal: {low:.0%}-{high:.0%}. Too many accidentals — clarify the tonality.",
            },
        }

        for i, col in enumerate(self.feature_names):
            z = z_scores[i]
            if abs(z) < THRESHOLD:
                continue

            val = features.get(col)
            if val is None:
                continue

            p5, p95 = self.feature_ranges.get(col, (0, 0))
            direction = "high" if z > 0 else "low"

            if col in critique_templates and direction in critique_templates[col]:
                template = critique_templates[col][direction]
                critiques.append(template.format(val=val, low=p5, high=p95))
            else:
                # Generic critique
                critiques.append(
                    f"{col} = {val} is {'above' if z > 0 else 'below'} normal range "
                    f"({p5:.2f} - {p95:.2f}), z-score: {z:+.1f}"
                )

        return critiques

    def save(self, path: str):
        """Save the fitted scorer to disk."""
        joblib.dump(
            {
                "scaler": self.scaler,
                "feature_names": self.feature_names,
                "medians": self.medians,
                "iqrs": self.iqrs,
                "isolation_forest": self.isolation_forest,
                "feature_ranges": self.feature_ranges,
            },
            path,
        )
        logger.info(f"DistributionScorer saved to {path}")

    @classmethod
    def load(cls, path: str) -> DistributionScorer:
        """Load a fitted scorer from disk."""
        data = joblib.load(path)
        scorer = cls()
        scorer.scaler = data["scaler"]
        scorer.feature_names = data["feature_names"]
        scorer.medians = data["medians"]
        scorer.iqrs = data["iqrs"]
        scorer.isolation_forest = data["isolation_forest"]
        scorer.feature_ranges = data["feature_ranges"]
        scorer._is_fitted = True
        return scorer
