"""Coherence and naturalness features — designed to catch LLM-specific failure modes."""

from __future__ import annotations

import logging
import math
from collections import Counter, defaultdict
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from music21.stream import Score

logger = logging.getLogger(__name__)


def extract_coherence_features(score: Score) -> dict:
    """Extract coherence/naturalness features from a music21 Score.

    These features target failure modes specific to LLM-generated music:
    rhythmic monotony, random-walk melodies, missing rests, aimless harmony.

    Returns a dict with keys:
        note_density, rest_ratio, pitch_class_entropy, interval_entropy,
        melodic_autocorrelation, phrase_length_regularity,
        strong_beat_consonance, rhythmic_independence
    """
    features: dict = {}

    # --- note_density ---
    try:
        features["note_density"] = _note_density(score)
    except Exception:
        logger.debug("note_density extraction failed", exc_info=True)
        features["note_density"] = None

    # --- rest_ratio ---
    try:
        features["rest_ratio"] = _rest_ratio(score)
    except Exception:
        logger.debug("rest_ratio extraction failed", exc_info=True)
        features["rest_ratio"] = None

    # --- pitch_class_entropy ---
    try:
        features["pitch_class_entropy"] = _pitch_class_entropy(score)
    except Exception:
        logger.debug("pitch_class_entropy extraction failed", exc_info=True)
        features["pitch_class_entropy"] = None

    # --- interval_entropy ---
    try:
        features["interval_entropy"] = _interval_entropy(score)
    except Exception:
        logger.debug("interval_entropy extraction failed", exc_info=True)
        features["interval_entropy"] = None

    # --- melodic_autocorrelation ---
    try:
        features["melodic_autocorrelation"] = _melodic_autocorrelation(score)
    except Exception:
        logger.debug("melodic_autocorrelation extraction failed", exc_info=True)
        features["melodic_autocorrelation"] = None

    # --- phrase_length_regularity ---
    try:
        features["phrase_length_regularity"] = _phrase_length_regularity(score)
    except Exception:
        logger.debug("phrase_length_regularity extraction failed", exc_info=True)
        features["phrase_length_regularity"] = None

    # --- strong_beat_consonance ---
    try:
        features["strong_beat_consonance"] = _strong_beat_consonance(score)
    except Exception:
        logger.debug("strong_beat_consonance extraction failed", exc_info=True)
        features["strong_beat_consonance"] = None

    # --- rhythmic_independence ---
    try:
        features["rhythmic_independence"] = _rhythmic_independence(score)
    except Exception:
        logger.debug("rhythmic_independence extraction failed", exc_info=True)
        features["rhythmic_independence"] = None

    # --- groove_consistency (MusPy-compatible) ---
    try:
        features["groove_consistency"] = _groove_consistency(score)
    except Exception:
        logger.debug("groove_consistency extraction failed", exc_info=True)
        features["groove_consistency"] = None

    return features


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _note_density(score) -> float:
    """Notes per quarter-note beat, averaged across parts."""
    total_notes = 0
    total_beats = 0.0

    for part in score.parts:
        notes = list(part.recurse().getElementsByClass("Note"))
        total_notes += len(notes)
        dur = float(part.duration.quarterLength)
        if dur > 0:
            total_beats += dur

    if total_beats == 0:
        return 0.0

    # Average density: total notes / total beats across all parts
    return total_notes / total_beats


def _rest_ratio(score) -> float:
    """Fraction of total beat-time occupied by rests (averaged across parts).

    A score with no rests returns 0. Real music typically has 5-25% rests.
    LLM music often has 0%.
    """
    rest_beats = 0.0
    total_beats = 0.0

    for part in score.parts:
        part_dur = float(part.duration.quarterLength)
        if part_dur <= 0:
            continue
        total_beats += part_dur

        rests = list(part.recurse().getElementsByClass("Rest"))
        for r in rests:
            rest_beats += float(r.duration.quarterLength)

    return rest_beats / total_beats if total_beats > 0 else 0.0


def _entropy(counts: Counter) -> float:
    """Shannon entropy in bits from a Counter of discrete events."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    ent = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)
    return ent


def _pitch_class_entropy(score) -> float:
    """Shannon entropy of pitch class distribution (0-11).

    Max entropy = log2(12) ≈ 3.58 (uniform across all 12 pitch classes).
    Very low = stuck on few notes. Very high = atonal/random.
    Typical tonal music: 2.5-3.2 bits.
    """
    pc_counts: Counter = Counter()
    for n in score.recurse().getElementsByClass("Note"):
        pc_counts[n.pitch.pitchClass] += 1
    return _entropy(pc_counts)


def _interval_entropy(score) -> float:
    """Shannon entropy of melodic interval distribution (in semitones, signed).

    Measures variety of melodic motion. Low = repetitive intervals.
    High = varied/unpredictable movement.
    """
    interval_counts: Counter = Counter()

    for part in score.parts:
        notes = list(part.recurse().getElementsByClass("Note"))
        for i in range(len(notes) - 1):
            semitones = notes[i + 1].pitch.midi - notes[i].pitch.midi
            # Clamp to reasonable range to avoid sparse histogram
            semitones = max(-24, min(24, semitones))
            interval_counts[semitones] += 1

    return _entropy(interval_counts)


def _melodic_autocorrelation(score) -> float | None:
    """Autocorrelation of the melody at a 1-measure lag.

    Measures whether the melody has structural self-similarity (motifs,
    sequences, repetition at the phrase level) vs. random walk.

    Returns correlation coefficient in [-1, 1]. Higher = more structured.
    Real music: typically 0.2-0.7. Random: ~0.0.
    """
    # Use the first part (typically melody)
    parts = list(score.parts)
    if not parts:
        return None

    notes = list(parts[0].recurse().getElementsByClass("Note"))
    if len(notes) < 8:
        return None

    midi_seq = np.array([n.pitch.midi for n in notes], dtype=float)

    # Determine lag in notes: approximate 1 measure worth
    measures = list(parts[0].getElementsByClass("Measure"))
    if measures:
        # Average notes per measure
        notes_per_measure = len(notes) / max(len(measures), 1)
        lag = max(1, int(round(notes_per_measure)))
    else:
        lag = 4  # fallback: assume 4 notes per measure

    if lag >= len(midi_seq):
        return None

    # Normalized autocorrelation at the given lag
    x = midi_seq - midi_seq.mean()
    variance = np.dot(x, x)
    if variance == 0:
        return 1.0  # constant pitch = perfectly "autocorrelated"

    autocorr = np.dot(x[:-lag], x[lag:]) / variance
    return float(autocorr)


def _phrase_length_regularity(score) -> float | None:
    """Coefficient of variation of phrase lengths (lower = more regular).

    Detects phrase structure by looking for longer notes or rests that
    mark phrase boundaries. Returns CV of inter-boundary distances.

    Real music: typically 0.0-0.5 (regular phrases).
    Random/LLM: often > 1.0 or None (no detectable phrases).
    """
    parts = list(score.parts)
    if not parts:
        return None

    # Use first part
    elements = list(parts[0].recurse().getElementsByClass(["Note", "Rest"]))
    if len(elements) < 4:
        return None

    # Heuristic: a phrase boundary is a rest >= 1 beat, or a note >= 2 beats
    # (long note often marks end of phrase)
    boundary_offsets: list[float] = []
    for elem in elements:
        is_rest = elem.isRest
        dur = float(elem.duration.quarterLength)
        if is_rest and dur >= 1.0:
            offset = float(elem.offset)
            if elem.activeSite:
                offset += float(elem.activeSite.offset)
            boundary_offsets.append(offset)
        elif not is_rest and dur >= 2.0:
            offset = float(elem.offset + elem.duration.quarterLength)
            if elem.activeSite:
                offset += float(elem.activeSite.offset)
            boundary_offsets.append(offset)

    if len(boundary_offsets) < 2:
        return None

    # Compute inter-boundary gaps
    boundary_offsets.sort()
    gaps = np.diff(boundary_offsets)
    gaps = gaps[gaps > 0]  # filter zero-width gaps

    if len(gaps) < 2:
        return None

    mean_gap = float(np.mean(gaps))
    if mean_gap == 0:
        return None

    cv = float(np.std(gaps) / mean_gap)
    return cv


def _strong_beat_consonance(score) -> float | None:
    """Fraction of strong beats where the sounding notes form a consonant interval.

    Strong beats = beat 1 and beat 3 in 4/4, beat 1 in 3/4, etc.
    Consonant = unison, 3rd, 4th, 5th, 6th, octave (semitones: 0,3,4,5,7,8,9,12).

    Checks all pairs of simultaneously sounding notes at strong beat positions.
    """
    CONSONANT_INTERVALS = {0, 3, 4, 5, 7, 8, 9, 12}

    parts = list(score.parts)
    if len(parts) < 2:
        return None

    # Determine strong beat offsets from the first part
    strong_offsets: set[float] = set()
    for part in parts[:1]:
        for measure in part.getElementsByClass("Measure"):
            ts = measure.getContextByClass("TimeSignature")
            measure_offset = float(measure.offset)
            if ts is None:
                # Default: beats 1 and 3 of 4/4
                strong_offsets.add(measure_offset)
                strong_offsets.add(measure_offset + 2.0)
            else:
                # Beat 1 is always strong
                strong_offsets.add(measure_offset)
                beat_dur = float(ts.beatDuration.quarterLength)
                num_beats = ts.numerator
                # In 4/4: beat 3 is strong. In 3/4: only beat 1.
                if num_beats == 4:
                    strong_offsets.add(measure_offset + 2 * beat_dur)
                elif num_beats >= 6:
                    # Compound: strong on 1 and 4
                    strong_offsets.add(measure_offset + 3 * beat_dur)

    if not strong_offsets:
        return None

    # Build offset->midi maps per part
    def _notes_at_offsets(part) -> dict[float, list[int]]:
        result: dict[float, list[int]] = defaultdict(list)
        for n in part.recurse().getElementsByClass("Note"):
            n_offset = float(n.offset)
            if n.activeSite:
                n_offset += float(n.activeSite.offset)
            n_end = n_offset + float(n.duration.quarterLength)
            for sb in strong_offsets:
                if n_offset <= sb < n_end:
                    result[sb].append(n.pitch.midi)
        return dict(result)

    part_maps = [_notes_at_offsets(p) for p in parts]

    consonant_count = 0
    total_count = 0

    for sb in sorted(strong_offsets):
        # Gather all sounding pitches across parts
        all_midi: list[int] = []
        for pm in part_maps:
            all_midi.extend(pm.get(sb, []))

        if len(all_midi) < 2:
            continue

        # Check all pairs
        total_count += 1
        all_consonant = True
        for i in range(len(all_midi)):
            for j in range(i + 1, len(all_midi)):
                ivl = abs(all_midi[i] - all_midi[j]) % 12
                if ivl not in CONSONANT_INTERVALS:
                    all_consonant = False
                    break
            if not all_consonant:
                break

        if all_consonant:
            consonant_count += 1

    return consonant_count / total_count if total_count > 0 else None


def _groove_consistency(score) -> float | None:
    """Consistency of rhythmic onset patterns across consecutive measures.

    Matches MusPy's groove_consistency metric: builds a binary onset vector
    per measure (quantized to 16th notes), then computes 1 minus the average
    Hamming distance between consecutive measures.

    Returns 0.0-1.0. Higher = more consistent groove.
    """
    SUBDIVISIONS_PER_BEAT = 4  # 16th note resolution

    parts = list(score.parts)
    if not parts:
        return None

    # Use first (melody) part
    part = parts[0]
    measures = list(part.getElementsByClass("Measure"))
    if len(measures) < 2:
        return None

    # Build onset vectors per measure
    groove_patterns: list[list[bool]] = []
    for measure in measures:
        ts = measure.getContextByClass("TimeSignature")
        if ts is None:
            beats_per_measure = 4
        else:
            beats_per_measure = ts.numerator * (4 / ts.denominator)

        slots = int(beats_per_measure * SUBDIVISIONS_PER_BEAT)
        if slots <= 0:
            continue

        pattern = [False] * slots
        for n in measure.recurse().getElementsByClass("Note"):
            pos = int(round(float(n.offset) * SUBDIVISIONS_PER_BEAT))
            if 0 <= pos < slots:
                pattern[pos] = True

        groove_patterns.append(pattern)

    if len(groove_patterns) < 2:
        return None

    # Compute average normalized Hamming distance between consecutive measures
    total_dist = 0.0
    n_pairs = 0
    for i in range(len(groove_patterns) - 1):
        a, b = groove_patterns[i], groove_patterns[i + 1]
        # Handle measures of different lengths (time sig changes)
        min_len = min(len(a), len(b))
        if min_len == 0:
            continue
        mismatches = sum(a[j] != b[j] for j in range(min_len))
        total_dist += mismatches / min_len
        n_pairs += 1

    if n_pairs == 0:
        return None

    return 1.0 - (total_dist / n_pairs)


def _rhythmic_independence(score) -> float | None:
    """Measures how independently the parts move rhythmically.

    Computes the fraction of beats where parts have DIFFERENT onset patterns.
    0.0 = all parts in lockstep (homorhythmic). 1.0 = completely independent.

    Real music varies (chorale ≈ 0.1, fugue ≈ 0.7).
    LLM music that copies rhythms across parts will score near 0.
    """
    parts = list(score.parts)
    if len(parts) < 2:
        return None

    try:
        total_beats = int(score.duration.quarterLength)
    except Exception:
        return None

    if total_beats <= 0:
        return None

    # For each part, build a set of beat positions where onsets occur
    part_onset_sets: list[set[int]] = []
    for part in parts:
        onsets: set[int] = set()
        for n in part.recurse().getElementsByClass("Note"):
            offset = float(n.offset)
            if n.activeSite:
                offset += float(n.activeSite.offset)
            # Quantize to nearest beat
            beat = int(round(offset))
            if 0 <= beat < total_beats:
                onsets.add(beat)
        part_onset_sets.append(onsets)

    # Compare all pairs of parts
    independent_beats = 0
    total_comparisons = 0

    for i in range(len(part_onset_sets)):
        for j in range(i + 1, len(part_onset_sets)):
            for beat in range(total_beats):
                total_comparisons += 1
                has_i = beat in part_onset_sets[i]
                has_j = beat in part_onset_sets[j]
                if has_i != has_j:
                    independent_beats += 1

    return independent_beats / total_comparisons if total_comparisons > 0 else None
