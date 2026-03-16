"""Predict quality scores for MusicXML files using trained models."""

import logging
import os

import joblib
import numpy as np
import pandas as pd
from music21 import converter

from musiclaude.features.extract import extract_features_from_file
from musiclaude.classifier.distribution import DistributionScorer, AnomalyReport

logger = logging.getLogger(__name__)


class QualityPredictor:
    """Predicts music quality using trained XGBoost models + distribution scoring.

    Combines two signals:
    1. XGBoost classifier/regressor — predicts rating based on PDMX training data
    2. DistributionScorer — flags features that deviate from what normal music looks like

    The distribution scorer is particularly valuable for LLM-generated music,
    which may have different failure modes than human-composed music.
    """

    def __init__(
        self,
        classifier_path: str,
        regressor_path: str | None = None,
        distribution_scorer_path: str | None = None,
    ):
        clf_data = joblib.load(classifier_path)
        self.classifier = clf_data["model"]
        self.clf_features = clf_data["metrics"]["feature_names"]

        self.regressor = None
        self.reg_features = None
        if regressor_path:
            reg_data = joblib.load(regressor_path)
            self.regressor = reg_data["model"]
            self.reg_features = reg_data["metrics"]["feature_names"]

        self.distribution_scorer: DistributionScorer | None = None
        if distribution_scorer_path and os.path.exists(distribution_scorer_path):
            self.distribution_scorer = DistributionScorer.load(distribution_scorer_path)

    def predict_from_features(self, features: dict) -> dict:
        """Predict quality from a pre-extracted feature dict.

        Returns dict with:
            - is_good: bool (XGBoost binary prediction)
            - good_probability: float (XGBoost probability of "good")
            - predicted_rating: float (XGBoost regression, if available)
            - anomaly_score: float (distribution scorer, if available)
            - is_anomalous: bool (distribution scorer, if available)
            - anomaly_report: AnomalyReport (distribution scorer, if available)
        """
        result = {}

        # Signal 1: XGBoost binary classification
        clf_df = pd.DataFrame([features])[self.clf_features]
        clf_df = clf_df.apply(pd.to_numeric, errors='coerce').fillna(0)
        result["is_good"] = bool(self.classifier.predict(clf_df)[0])
        result["good_probability"] = float(self.classifier.predict_proba(clf_df)[0][1])

        # Signal 1b: XGBoost regression
        if self.regressor:
            reg_df = pd.DataFrame([features])[self.reg_features]
            reg_df = reg_df.apply(pd.to_numeric, errors='coerce').fillna(0)
            result["predicted_rating"] = float(np.clip(self.regressor.predict(reg_df)[0], 0, 5))

        # Signal 2: Distribution-based anomaly scoring
        if self.distribution_scorer:
            report = self.distribution_scorer.score_features(features)
            result["anomaly_score"] = report.score
            result["is_anomalous"] = report.is_anomalous
            result["anomaly_report"] = report

        return result

    def predict_file(self, filepath: str) -> dict | None:
        """Extract features and predict quality for a MusicXML file."""
        features = extract_features_from_file(filepath)
        if features is None:
            return None
        return self.predict_from_features(features)

    def get_feature_deficiencies(self, features: dict, reference_stats: dict | None = None) -> list[str]:
        """Identify specific feature deficiencies for feedback.

        Returns human-readable critiques based on feature values.
        """
        critiques = []

        # Harmonic critiques
        vocab = features.get("chord_vocabulary_size", 0)
        if vocab is not None and vocab < 4:
            critiques.append(
                f"Low harmonic variety — only {vocab} unique chord types. "
                "Consider using more diverse chord qualities (add 7ths, suspensions, or modal interchange)."
            )

        pct_ext = features.get("pct_extended_chords", 0)
        if pct_ext is not None and pct_ext < 0.05:
            critiques.append(
                "Very few extended chords. Adding some 7ths or 9ths would increase harmonic richness."
            )

        key_stab = features.get("key_stability", 0)
        if key_stab is not None and key_stab < 0.6:
            critiques.append(
                f"Low key stability ({key_stab:.0%}). Too many out-of-key notes — "
                "either establish the key more clearly or frame modulations intentionally."
            )

        # Melodic critiques
        stepwise = features.get("pct_stepwise", 0)
        if stepwise is not None and stepwise > 0.95:
            critiques.append(
                "Melody is almost entirely stepwise motion. Add some leaps for interest."
            )
        elif stepwise is not None and stepwise < 0.3:
            critiques.append(
                f"Too many melodic leaps ({1-stepwise:.0%}). More stepwise motion would improve singability."
            )

        mel_range = features.get("melodic_range", 0)
        if mel_range is not None and mel_range < 5:
            critiques.append(
                f"Melodic range is very narrow ({mel_range} semitones). Expand the range for more expressiveness."
            )
        elif mel_range is not None and mel_range > 36:
            critiques.append(
                f"Melodic range is very wide ({mel_range} semitones / {mel_range // 12} octaves). "
                "Consider narrowing for more practical performance."
            )

        # Structural critiques
        dyn = features.get("dynamics_count", 0)
        if dyn is not None and dyn == 0:
            critiques.append("No dynamics markings. Adding dynamics would greatly improve expressiveness.")

        tempo = features.get("tempo_count", 0)
        if tempo is not None and tempo == 0:
            critiques.append("No tempo marking found. Add a tempo indication.")

        rhythmic = features.get("rhythmic_variety", 0)
        if rhythmic is not None and rhythmic < 3:
            critiques.append(
                f"Low rhythmic variety — only {rhythmic} unique note durations. "
                "Use more varied rhythms for interest."
            )

        # Voice crossing
        crossings = features.get("voice_crossing_count", 0)
        if crossings is not None and crossings > 10:
            critiques.append(
                f"Excessive voice crossings ({crossings}). Review part writing for proper voice leading."
            )

        return critiques
