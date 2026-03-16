"""Structural feature extraction from music21 Score objects."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from music21.stream import Score

logger = logging.getLogger(__name__)


def extract_structural_features(score: Score) -> dict:
    """Extract structural features from a music21 Score.

    Returns a dict with keys:
        num_parts, total_duration_beats, dynamics_count,
        tempo_count, time_sig_complexity, num_sections
    """
    features: dict = {}

    # --- num_parts ---
    try:
        features["num_parts"] = len(score.parts)
    except Exception:
        logger.debug("num_parts extraction failed", exc_info=True)
        features["num_parts"] = None

    # --- total_duration_beats ---
    try:
        features["total_duration_beats"] = float(score.duration.quarterLength)
    except Exception:
        logger.debug("total_duration_beats extraction failed", exc_info=True)
        features["total_duration_beats"] = None

    # --- dynamics_count ---
    try:
        dynamics = list(score.recurse().getElementsByClass("Dynamic"))
        features["dynamics_count"] = len(dynamics)
    except Exception:
        logger.debug("dynamics_count extraction failed", exc_info=True)
        features["dynamics_count"] = None

    # --- tempo_count ---
    try:
        tempos = list(score.recurse().getElementsByClass("MetronomeMark"))
        features["tempo_count"] = len(tempos)
    except Exception:
        logger.debug("tempo_count extraction failed", exc_info=True)
        features["tempo_count"] = None

    # --- time_sig_complexity ---
    try:
        features["time_sig_complexity"] = _time_sig_complexity(score)
    except Exception:
        logger.debug("time_sig_complexity extraction failed", exc_info=True)
        features["time_sig_complexity"] = None

    # --- num_sections ---
    try:
        features["num_sections"] = _num_sections(score)
    except Exception:
        logger.debug("num_sections extraction failed", exc_info=True)
        features["num_sections"] = None

    return features


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _is_compound(numerator: int) -> bool:
    """A meter is compound if the numerator is divisible by 3 and > 3."""
    return numerator > 3 and numerator % 3 == 0


def _time_sig_complexity(score) -> float:
    """Determine time signature complexity.

    Returns:
        1.0 if all time signatures are compound,
        0.0 if all are simple,
        0.5 if mixed.
    """
    time_sigs = list(score.recurse().getElementsByClass("TimeSignature"))
    if not time_sigs:
        return 0.0  # default to simple if no explicit time sig

    compound_flags = [_is_compound(ts.numerator) for ts in time_sigs]

    if all(compound_flags):
        return 1.0
    elif any(compound_flags):
        return 0.5
    else:
        return 0.0


def _num_sections(score) -> int:
    """Count section markers (RehearsalMark and RepeatBracket objects)."""
    count = 0

    rehearsal_marks = list(score.recurse().getElementsByClass("RehearsalMark"))
    count += len(rehearsal_marks)

    # RepeatBracket (first/second ending brackets) as section indicators
    try:
        from music21 import spanner

        for sp in score.recurse().getElementsByClass("Spanner"):
            if isinstance(sp, spanner.RepeatBracket):
                count += 1
    except Exception:
        pass

    # Also check for RepeatMark objects (segno, coda, etc.)
    try:
        repeat_marks = list(score.recurse().getElementsByClass("RepeatMark"))
        count += len(repeat_marks)
    except Exception:
        pass

    return count
