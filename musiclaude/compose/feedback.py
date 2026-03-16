"""Feedback loop for iterative composition improvement."""

import json
import logging
import os
from datetime import datetime

from musiclaude.compose.validate import validate_composition

logger = logging.getLogger(__name__)


def format_critique_for_llm(validation_result: dict) -> str:
    """Format validation results into a prompt-friendly critique for the LLM.

    Returns a markdown-formatted string describing what needs improvement.
    Combines XGBoost quality predictions, distribution anomaly scoring,
    and structural validation into a single actionable report.
    """
    lines = []

    # --- XGBoost quality signal ---
    quality = validation_result.get("quality")
    if quality:
        rating = quality.get("predicted_rating")
        prob = quality.get("good_probability", 0)
        if rating:
            lines.append(f"**Predicted rating: {rating:.1f}/5.0** (probability of 'good': {prob:.0%})")
        else:
            lines.append(f"**Probability of 'good' quality: {prob:.0%}**")

    # --- Distribution anomaly signal ---
    anomaly = validation_result.get("anomaly")
    if anomaly:
        status = "ANOMALOUS" if anomaly.is_anomalous else "normal"
        lines.append(f"**Distribution check: {status}** (anomaly score: {anomaly.score:.2f})")

    # --- Combined critiques ---
    critiques = validation_result.get("critiques", [])
    if critiques:
        lines.append("\n**Issues to address:**")
        for i, c in enumerate(critiques, 1):
            lines.append(f"{i}. {c}")

    # --- Key metrics ---
    features = validation_result.get("features", {})
    if features:
        lines.append("\n**Key metrics:**")
        highlight_keys = [
            # Harmonic
            "chord_vocabulary_size", "pct_extended_chords", "key_stability",
            # Melodic
            "avg_interval_size", "pct_stepwise", "melodic_range",
            # Structural
            "rhythmic_variety", "dynamics_count", "num_parts",
            # Coherence (new — these are the LLM-specific signals)
            "note_density", "rest_ratio", "pitch_class_entropy",
            "interval_entropy", "melodic_autocorrelation",
        ]
        for k in highlight_keys:
            v = features.get(k)
            if v is not None:
                if isinstance(v, float):
                    lines.append(f"- {k}: {v:.3f}")
                else:
                    lines.append(f"- {k}: {v}")

    # --- Feature deviation highlights (from distribution scorer) ---
    if anomaly and anomaly.feature_deviations:
        extreme = sorted(
            anomaly.feature_deviations.items(),
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:5]
        if any(abs(z) > 1.5 for _, z in extreme):
            lines.append("\n**Most unusual features (z-score from normal):**")
            for feat, z in extreme:
                if abs(z) > 1.5:
                    direction = "above" if z > 0 else "below"
                    lines.append(f"- {feat}: {z:+.1f} ({direction} normal)")

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

    log_entry = {
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "filepath": filepath,
        "passes": validation_result["passes"],
        "quality": quality_data,
        "anomaly": anomaly_data,
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
    # Determine iteration number from existing log
    log_path = os.path.join(output_dir, "revision_log.jsonl")
    iteration = 0
    if os.path.exists(log_path):
        with open(log_path) as f:
            iteration = sum(1 for _ in f)

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
