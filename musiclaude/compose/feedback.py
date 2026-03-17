"""Feedback loop for iterative composition improvement."""

import json
import logging
import os
from datetime import datetime

from musiclaude.compose.validate import validate_composition

logger = logging.getLogger(__name__)


def format_critique_for_llm(validation_result: dict) -> str:
    """Format validation results into a prompt-friendly critique for the LLM.

    Primary signal: feature profile comparison (percentile-based, ranked by importance).
    Secondary signals: XGBoost predictions, distribution anomaly scoring.
    """
    lines = []

    # --- PRIMARY: Feature profile feedback (ranked improvement instructions) ---
    profile_feedback = validation_result.get("profile_feedback")
    if profile_feedback:
        lines.append(profile_feedback)

    # --- SECONDARY: XGBoost quality signal (for reference) ---
    quality = validation_result.get("quality")
    if quality:
        rating = quality.get("predicted_rating")
        prob = quality.get("good_probability", 0)
        if rating:
            lines.append(f"\n**XGBoost reference:** predicted rating {rating:.1f}/5.0, P(good) = {prob:.0%}")

    # --- SECONDARY: Distribution anomaly signal ---
    anomaly = validation_result.get("anomaly")
    if anomaly:
        status = "ANOMALOUS" if anomaly.is_anomalous else "normal"
        lines.append(f"**Distribution check:** {status} (score: {anomaly.score:.2f})")

    # --- Structural/distribution critiques ---
    critiques = validation_result.get("critiques", [])
    if critiques:
        lines.append("\n**Additional issues:**")
        for i, c in enumerate(critiques, 1):
            lines.append(f"{i}. {c}")

    # If no profile, fall back to key metrics dump
    if not profile_feedback:
        features = validation_result.get("features", {})
        if features:
            lines.append("\n**Key metrics:**")
            for k in ["chord_vocabulary_size", "dynamics_count", "melodic_range",
                       "rhythmic_variety", "rest_ratio", "pitch_class_entropy"]:
                v = features.get(k)
                if v is not None:
                    lines.append(f"- {k}: {v:.3f}" if isinstance(v, float) else f"- {k}: {v}")

    return "\n".join(lines)


def log_revision(
    output_dir: str,
    iteration: int,
    filepath: str,
    validation_result: dict,
):
    """Log a revision attempt to the output directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Serialize anomaly report if present
    anomaly = validation_result.get("anomaly")
    anomaly_data = None
    if anomaly:
        anomaly_data = {
            "score": anomaly.score,
            "is_anomalous": anomaly.is_anomalous,
            "top_deviations": dict(
                sorted(
                    anomaly.feature_deviations.items(),
                    key=lambda x: abs(x[1]),
                    reverse=True,
                )[:10]
            ),
        }

    # Strip non-serializable quality fields
    quality = validation_result.get("quality")
    quality_data = None
    if quality:
        quality_data = {
            k: v for k, v in quality.items()
            if k not in ("anomaly_report",)
        }

    # Save features (excluding non-serializable values) for delta comparison
    features_data = None
    raw_features = validation_result.get("features")
    if raw_features:
        features_data = {
            k: v for k, v in raw_features.items()
            if isinstance(v, (int, float, type(None))) and k != "filepath"
        }

    log_entry = {
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "filepath": filepath,
        "passes": validation_result["passes"],
        "quality": quality_data,
        "anomaly": anomaly_data,
        "features": features_data,
        "num_critiques": len(validation_result.get("critiques", [])),
        "critiques": validation_result.get("critiques", []),
    }

    log_path = os.path.join(output_dir, "revision_log.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    logger.info(f"Iteration {iteration}: passes={log_entry['passes']}, critiques={log_entry['num_critiques']}")


def run_feedback_loop(
    musicxml_path: str,
    output_dir: str,
    classifier_path: str | None = None,
    regressor_path: str | None = None,
    distribution_scorer_path: str | None = None,
    profile_path: str | None = None,
    quality_threshold: float = 0.5,
    max_iterations: int = 5,
) -> dict:
    """Run the validation-feedback loop on a composition.

    This validates the composition, logs results, and returns critique
    for the LLM to use in revision. The actual LLM call happens in the
    Claude Code skill — this just provides the assessment infrastructure.

    Returns dict with:
        - passes: bool
        - critique_text: str (formatted for LLM)
        - validation: full validation result
        - iteration: current iteration number
    """
    # Determine iteration number and previous features from existing log
    log_path = os.path.join(output_dir, "revision_log.jsonl")
    iteration = 0
    previous_features = None
    if os.path.exists(log_path):
        with open(log_path) as f:
            entries = [json.loads(line) for line in f if line.strip()]
            iteration = len(entries)
            # Get features from the last iteration for delta comparison
            if entries:
                previous_features = entries[-1].get("features")

    if iteration >= max_iterations:
        return {
            "passes": False,
            "critique_text": f"Maximum iterations ({max_iterations}) reached. Accepting current version.",
            "validation": None,
            "iteration": iteration,
        }

    validation = validate_composition(
        musicxml_path,
        classifier_path=classifier_path,
        regressor_path=regressor_path,
        distribution_scorer_path=distribution_scorer_path,
        profile_path=profile_path,
        previous_features=previous_features,
        quality_threshold=quality_threshold,
    )

    log_revision(output_dir, iteration, musicxml_path, validation)

    critique_text = format_critique_for_llm(validation)

    return {
        "passes": validation["passes"],
        "critique_text": critique_text,
        "validation": validation,
        "iteration": iteration,
    }
