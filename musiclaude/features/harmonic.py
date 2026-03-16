"""Harmonic feature extraction from music21 Score objects."""

from __future__ import annotations

import logging
import math
from collections import Counter
from typing import TYPE_CHECKING

from music21 import analysis, roman

if TYPE_CHECKING:
    from music21.stream import Score

logger = logging.getLogger(__name__)


def extract_harmonic_features(score: Score) -> dict:
    """Extract harmonic features from a music21 Score.

    Returns a dict with keys:
        chord_vocabulary_size, pct_extended_chords, harmonic_rhythm,
        cadence_count_authentic, cadence_count_half, cadence_count_deceptive,
        cadence_count_plagal, key_stability, modulation_count
    """
    features: dict = {}

    # Pre-compute shared resources
    try:
        detected_key = score.analyze("key")
    except Exception:
        detected_key = None

    try:
        chordified = score.chordify()
    except Exception:
        chordified = None

    # --- chord_vocabulary_size & pct_extended_chords ---
    try:
        features.update(_chord_vocabulary_features(chordified))
    except Exception:
        logger.debug("chord vocabulary extraction failed", exc_info=True)
        features.setdefault("chord_vocabulary_size", None)
        features.setdefault("pct_extended_chords", None)

    # --- harmonic_rhythm ---
    try:
        features["harmonic_rhythm"] = _harmonic_rhythm(chordified)
    except Exception:
        logger.debug("harmonic rhythm extraction failed", exc_info=True)
        features["harmonic_rhythm"] = None

    # --- cadence counts ---
    try:
        cadences = _cadence_counts(chordified, detected_key)
        features["cadence_count_authentic"] = cadences.get("authentic", 0)
        features["cadence_count_half"] = cadences.get("half", 0)
        features["cadence_count_deceptive"] = cadences.get("deceptive", 0)
        features["cadence_count_plagal"] = cadences.get("plagal", 0)
    except Exception:
        logger.debug("cadence detection failed", exc_info=True)
        features["cadence_count_authentic"] = None
        features["cadence_count_half"] = None
        features["cadence_count_deceptive"] = None
        features["cadence_count_plagal"] = None

    # --- key_stability ---
    try:
        features["key_stability"] = _key_stability(score, detected_key)
    except Exception:
        logger.debug("key stability extraction failed", exc_info=True)
        features["key_stability"] = None

    # --- modulation_count ---
    try:
        features["modulation_count"] = _modulation_count(score)
    except Exception:
        logger.debug("modulation count extraction failed", exc_info=True)
        features["modulation_count"] = None

    return features


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _chord_vocabulary_features(chordified) -> dict:
    """Count unique chord types and percentage of extended chords."""
    if chordified is None:
        return {"chord_vocabulary_size": None, "pct_extended_chords": None}

    chords = list(chordified.recurse().getElementsByClass("Chord"))
    if not chords:
        return {"chord_vocabulary_size": 0, "pct_extended_chords": 0.0}

    extended_keywords = {"seventh", "ninth", "eleventh", "thirteenth"}
    chord_names: set[str] = set()
    extended_count = 0

    for ch in chords:
        name = ch.commonName
        chord_names.add(name)
        name_lower = name.lower()
        if any(kw in name_lower for kw in extended_keywords) or len(ch.pitches) >= 4:
            extended_count += 1

    return {
        "chord_vocabulary_size": len(chord_names),
        "pct_extended_chords": extended_count / len(chords) if chords else 0.0,
    }


def _harmonic_rhythm(chordified) -> float | None:
    """Average number of quarter-note beats between chord changes."""
    if chordified is None:
        return None

    chords = list(chordified.recurse().getElementsByClass("Chord"))
    if len(chords) < 2:
        return None

    change_offsets: list[float] = []
    prev_pitches: tuple | None = None

    for ch in chords:
        current_pitches = tuple(sorted(p.midi for p in ch.pitches))
        if prev_pitches is not None and current_pitches != prev_pitches:
            change_offsets.append(ch.offset)
        prev_pitches = current_pitches

    if len(change_offsets) < 2:
        return None

    gaps = [
        change_offsets[i + 1] - change_offsets[i]
        for i in range(len(change_offsets) - 1)
    ]
    return sum(gaps) / len(gaps) if gaps else None


def _cadence_counts(chordified, detected_key) -> dict:
    """Count cadence patterns using roman numeral analysis."""
    counts = {"authentic": 0, "half": 0, "deceptive": 0, "plagal": 0}

    if chordified is None or detected_key is None:
        return counts

    chords = list(chordified.recurse().getElementsByClass("Chord"))
    if len(chords) < 2:
        return counts

    # Convert chords to roman numerals (best-effort)
    numerals: list[str] = []
    for ch in chords:
        try:
            rn = roman.romanNumeralFromChord(ch, detected_key)
            numerals.append(rn.romanNumeral)
        except Exception:
            numerals.append("")

    # Scan consecutive pairs
    for i in range(len(numerals) - 1):
        prev_rn = numerals[i].upper().strip()
        curr_rn = numerals[i + 1].upper().strip()

        if prev_rn == "V" and curr_rn == "I":
            counts["authentic"] += 1
        elif curr_rn == "V":
            counts["half"] += 1
        elif prev_rn == "V" and curr_rn == "VI":
            counts["deceptive"] += 1
        elif prev_rn == "IV" and curr_rn == "I":
            counts["plagal"] += 1

    return counts


def _key_stability(score, detected_key) -> float | None:
    """Fraction of notes belonging to the detected key's scale."""
    if detected_key is None:
        return None

    scale_pitches = set()
    try:
        for p in detected_key.getScale().pitches:
            scale_pitches.add(p.pitchClass)
    except Exception:
        return None

    if not scale_pitches:
        return None

    notes = list(score.recurse().getElementsByClass("Note"))
    if not notes:
        return None

    in_key = sum(1 for n in notes if n.pitch.pitchClass in scale_pitches)
    return in_key / len(notes)


def _modulation_count(score) -> int:
    """Estimate modulation count by analyzing key in 4-measure windows."""
    try:
        measures = list(score.parts[0].getElementsByClass("Measure"))
    except Exception:
        return 0

    if len(measures) < 4:
        return 0

    ks = analysis.discrete.KrumhanslSchmuckler()
    window_size = 4
    prev_key = None
    changes = 0

    for i in range(0, len(measures) - window_size + 1, window_size):
        try:
            excerpt = score.measures(i + 1, i + window_size)
            result = ks.getSolution(excerpt)
            current_key = str(result)
        except Exception:
            current_key = None

        if prev_key is not None and current_key is not None and current_key != prev_key:
            changes += 1
        if current_key is not None:
            prev_key = current_key

    return changes
