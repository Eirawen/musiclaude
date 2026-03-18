"""Orchestration feature extraction from music21 Score objects."""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from music21.stream import Score

logger = logging.getLogger(__name__)


def extract_orchestration_features(score: Score) -> dict:
    """Extract orchestration features from a music21 Score.

    Returns a dict with keys:
        instrument_names, instrument_count, voice_crossing_count,
        avg_range_utilization, doubling_score
    """
    features: dict = {}

    # --- instrument_names & instrument_count ---
    try:
        names = _instrument_names(score)
        features["instrument_names"] = ", ".join(names) if names else ""
        features["instrument_count"] = len(names)
    except Exception:
        logger.debug("instrument extraction failed", exc_info=True)
        features["instrument_names"] = None
        features["instrument_count"] = None

    # --- voice_crossing_count ---
    try:
        features["voice_crossing_count"] = _voice_crossing_count(score)
    except Exception:
        logger.debug("voice crossing extraction failed", exc_info=True)
        features["voice_crossing_count"] = None

    # --- avg_range_utilization ---
    try:
        features["avg_range_utilization"] = _avg_range_utilization(score)
    except Exception:
        logger.debug("range utilization extraction failed", exc_info=True)
        features["avg_range_utilization"] = None

    # --- doubling_score ---
    try:
        features["doubling_score"] = _doubling_score(score)
    except Exception:
        logger.debug("doubling score extraction failed", exc_info=True)
        features["doubling_score"] = None

    return features


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _instrument_names(score) -> list[str]:
    """Get distinct instrument names from score parts."""
    names: list[str] = []
    seen: set[str] = set()

    for part in score.parts:
        inst = part.getInstrument(returnDefault=True)
        name = inst.partName or inst.instrumentName or str(part.partName) or "Unknown"
        if name not in seen:
            seen.add(name)
            names.append(name)

    return names


def _voice_crossing_count(score) -> int:
    """Count voice crossings between adjacent parts.

    A crossing occurs when a note in a lower part (by part order) sounds
    higher than a note in the upper part at the same offset.
    """
    parts = list(score.parts)
    if len(parts) < 2:
        return 0

    crossings = 0

    for i in range(len(parts) - 1):
        upper_part = parts[i]
        lower_part = parts[i + 1]

        # Build offset -> midi maps for each part
        upper_notes = _offset_midi_map(upper_part)
        lower_notes = _offset_midi_map(lower_part)

        # Check shared offsets
        common_offsets = set(upper_notes.keys()) & set(lower_notes.keys())
        for offset in common_offsets:
            upper_lowest = min(upper_notes[offset])
            lower_highest = max(lower_notes[offset])
            if lower_highest > upper_lowest:
                crossings += 1

    return crossings


def _offset_midi_map(part) -> dict[float, list[int]]:
    """Build a mapping from offset to list of MIDI pitches sounding at that offset."""
    result: dict[float, list[int]] = defaultdict(list)
    for note in part.recurse().getElementsByClass("Note"):
        offset = float(note.offset + note.activeSite.offset if note.activeSite else note.offset)
        result[offset].append(note.pitch.midi)
    return dict(result)


def _avg_range_utilization(score) -> float | None:
    """Average across parts of (actual range / comfortable instrument range).

    Skips parts where the instrument's comfortable range is not available.
    """
    utilizations: list[float] = []

    for part in score.parts:
        inst = part.getInstrument(returnDefault=True)

        # Get instrument range if available
        try:
            low = inst.lowestNote
            high = inst.highestNote
            if low is None or high is None:
                continue
            instrument_range = high.midi - low.midi
            if instrument_range <= 0:
                continue
        except (AttributeError, TypeError):
            continue

        # Get actual range used in this part
        notes = list(part.recurse().getElementsByClass("Note"))
        if not notes:
            continue

        midi_vals = [n.pitch.midi for n in notes]
        actual_range = max(midi_vals) - min(midi_vals)
        utilizations.append(actual_range / instrument_range)

    return sum(utilizations) / len(utilizations) if utilizations else None


def _doubling_score(score) -> float:
    """Fraction of sampled beat offsets where 2+ parts play the same pitch class.

    Samples at every quarter-note beat from offset 0 to the score duration.
    """
    parts = list(score.parts)
    if len(parts) < 2:
        return 0.0

    try:
        total_beats = int(score.duration.quarterLength)
    except Exception:
        return 0.0

    if total_beats <= 0:
        return 0.0

    # Build pitch-class sets per part per beat
    part_beat_pcs: list[dict[int, set[int]]] = []
    for part in parts:
        beat_pcs: dict[int, set[int]] = defaultdict(set)
        for note in part.recurse().getElementsByClass("Note"):
            try:
                note_offset = float(
                    note.offset + note.activeSite.offset
                    if note.activeSite
                    else note.offset
                )
            except Exception:
                continue
            # A note sounds from its offset to offset + duration
            start_beat = int(note_offset)
            end_beat = int(note_offset + float(note.duration.quarterLength))
            pc = note.pitch.pitchClass
            for beat in range(max(0, start_beat), min(total_beats, end_beat + 1)):
                beat_pcs[beat].add(pc)
        part_beat_pcs.append(dict(beat_pcs))

    doubled_beats = 0
    sampled_beats = 0

    for beat in range(total_beats):
        sampled_beats += 1
        # Collect all pitch classes across parts at this beat
        all_pcs: list[int] = []
        for pbd in part_beat_pcs:
            pcs = pbd.get(beat, set())
            all_pcs.extend(pcs)

        # Check if any pitch class appears from 2+ different parts
        if len(all_pcs) != len(set(all_pcs)):
            doubled_beats += 1

    return doubled_beats / sampled_beats if sampled_beats > 0 else 0.0
