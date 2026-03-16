"""Melodic feature extraction from music21 Score objects."""

from __future__ import annotations

import logging
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from music21.stream import Score

logger = logging.getLogger(__name__)


def extract_melodic_features(score: Score) -> dict:
    """Extract melodic features from a music21 Score.

    Returns a dict with keys:
        avg_interval_size, pct_stepwise, melodic_range,
        pct_rising, pct_falling, pct_static,
        rhythmic_variety, repetition_density
    """
    features: dict = {}

    # --- interval-based features ---
    try:
        interval_feats = _interval_features(score)
        features.update(interval_feats)
    except Exception:
        logger.debug("interval feature extraction failed", exc_info=True)
        for key in (
            "avg_interval_size",
            "pct_stepwise",
            "pct_rising",
            "pct_falling",
            "pct_static",
        ):
            features[key] = None

    # --- melodic_range ---
    try:
        features["melodic_range"] = _melodic_range(score)
    except Exception:
        logger.debug("melodic range extraction failed", exc_info=True)
        features["melodic_range"] = None

    # --- rhythmic_variety ---
    try:
        features["rhythmic_variety"] = _rhythmic_variety(score)
    except Exception:
        logger.debug("rhythmic variety extraction failed", exc_info=True)
        features["rhythmic_variety"] = None

    # --- repetition_density ---
    try:
        features["repetition_density"] = _repetition_density(score)
    except Exception:
        logger.debug("repetition density extraction failed", exc_info=True)
        features["repetition_density"] = None

    return features


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _interval_features(score) -> dict:
    """Compute interval statistics across all parts."""
    intervals: list[int] = []  # signed semitone intervals

    for part in score.parts:
        notes = list(part.recurse().getElementsByClass("Note"))
        for i in range(len(notes) - 1):
            semitones = notes[i + 1].pitch.midi - notes[i].pitch.midi
            intervals.append(semitones)

    if not intervals:
        return {
            "avg_interval_size": 0.0,
            "pct_stepwise": 0.0,
            "pct_rising": 0.0,
            "pct_falling": 0.0,
            "pct_static": 0.0,
        }

    total = len(intervals)
    abs_intervals = [abs(s) for s in intervals]

    stepwise = sum(1 for a in abs_intervals if a <= 2)
    rising = sum(1 for s in intervals if s > 0)
    falling = sum(1 for s in intervals if s < 0)
    static = sum(1 for s in intervals if s == 0)

    return {
        "avg_interval_size": sum(abs_intervals) / total,
        "pct_stepwise": stepwise / total,
        "pct_rising": rising / total,
        "pct_falling": falling / total,
        "pct_static": static / total,
    }


def _melodic_range(score) -> int:
    """Total range in semitones across entire score."""
    notes = list(score.recurse().getElementsByClass("Note"))
    if not notes:
        return 0
    midi_values = [n.pitch.midi for n in notes]
    return max(midi_values) - min(midi_values)


def _rhythmic_variety(score) -> int:
    """Number of unique duration quarterLength values."""
    notes = list(score.recurse().getElementsByClass("Note"))
    durations = {n.duration.quarterLength for n in notes}
    return len(durations)


def _repetition_density(score) -> float:
    """Approximate fraction of measures that repeat earlier measures within each part.

    Two measures are considered near-repeats if they share the same sequence
    of MIDI pitch values (ignoring rhythm).
    """
    repeated = 0
    total = 0

    for part in score.parts:
        measures = list(part.getElementsByClass("Measure"))
        seen_signatures: set[tuple[int, ...]] = set()

        for measure in measures:
            notes = list(measure.recurse().getElementsByClass("Note"))
            sig = tuple(n.pitch.midi for n in notes)

            # Skip empty measures from the comparison
            if not sig:
                continue

            total += 1
            if sig in seen_signatures:
                repeated += 1
            else:
                seen_signatures.add(sig)

    return repeated / total if total > 0 else 0.0
