"""Validate and assess quality of generated compositions."""

import logging
import os

from music21 import converter

from musiclaude.validator.structural import validate_score, ValidationResult
from musiclaude.features.extract import extract_features_from_file
from musiclaude.classifier.predict import QualityPredictor
from musiclaude.classifier.distribution import DistributionScorer

logger = logging.getLogger(__name__)


def validate_composition(
    filepath: str,
    classifier_path: str | None = None,
    regressor_path: str | None = None,
    distribution_scorer_path: str | None = None,
    quality_threshold: float = 0.5,
) -> dict:
    """Full validation pipeline for a generated composition.

    Combines three assessment layers:
    1. Structural validation (is the MusicXML well-formed and music-theory-valid?)
    2. XGBoost quality prediction (does it match patterns of highly-rated music?)
    3. Distribution anomaly scoring (does it look like real music, not LLM artifacts?)

    Returns dict with:
        - structural_validation: ValidationResult
        - features: dict of extracted features (if structural validation passes)
        - quality: dict with XGBoost predictions (if classifier available)
        - anomaly: AnomalyReport (if distribution scorer available)
        - critiques: list of specific improvement suggestions
        - passes: bool - whether the composition meets quality threshold
    """
    result = {
        "structural_validation": None,
        "features": None,
        "quality": None,
        "anomaly": None,
        "critiques": [],
        "passes": False,
    }

    # Step 1: Structural validation
    structural = validate_score(converter.parse(filepath))
    result["structural_validation"] = structural

    if not structural.is_valid:
        result["critiques"].append(
            "Score has structural errors that must be fixed first: "
            + "; ".join(structural.errors)
        )
        return result

    # Step 2: Feature extraction
    features = extract_features_from_file(filepath)
    if features is None:
        result["critiques"].append("Failed to extract features from score.")
        return result
    result["features"] = features

    critiques = []

    # Step 3: Quality prediction (XGBoost — if classifier available)
    if classifier_path and os.path.exists(classifier_path):
        predictor = QualityPredictor(
            classifier_path, regressor_path, distribution_scorer_path
        )
        quality = predictor.predict_from_features(features)
        result["quality"] = quality

        # XGBoost-based critiques
        critiques.extend(predictor.get_feature_deficiencies(features))

        # Distribution anomaly critiques
        anomaly_report = quality.get("anomaly_report")
        if anomaly_report:
            result["anomaly"] = anomaly_report
            critiques.extend(anomaly_report.critiques)

        # Pass requires BOTH signals to be positive
        xgb_passes = quality.get("good_probability", 0) >= quality_threshold
        anomaly_ok = not quality.get("is_anomalous", False)
        result["passes"] = xgb_passes and anomaly_ok

        if not xgb_passes:
            prob = quality.get("good_probability", 0)
            critiques.insert(0, f"XGBoost quality score ({prob:.0%}) below threshold ({quality_threshold:.0%}).")
        if not anomaly_ok:
            score = quality.get("anomaly_score", 0)
            critiques.insert(0, f"Distribution scorer flagged this as anomalous (score: {score:.2f}).")

    elif distribution_scorer_path and os.path.exists(distribution_scorer_path):
        # No classifier but have distribution scorer — use it standalone
        scorer = DistributionScorer.load(distribution_scorer_path)
        anomaly_report = scorer.score_features(features)
        result["anomaly"] = anomaly_report
        critiques.extend(anomaly_report.critiques)
        result["passes"] = not anomaly_report.is_anomalous

    else:
        # No models available — pass if structurally valid
        result["passes"] = structural.is_valid

    # Add structural warnings as mild critiques
    for w in structural.warnings:
        critiques.append(f"[structural] {w}")

    result["critiques"] = critiques
    return result
