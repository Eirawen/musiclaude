"""Structural and music theory validation for MusicXML scores."""

import logging
from dataclasses import dataclass, field

from music21 import converter, stream, note, chord, meter, key, interval, pitch

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of validating a MusicXML score."""
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.is_valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def summary(self) -> str:
        lines = []
        if self.is_valid:
            lines.append("VALID")
        else:
            lines.append("INVALID")
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARNING: {w}")
        return "\n".join(lines)


def validate_file(filepath: str) -> ValidationResult:
    """Validate a MusicXML file for structural correctness."""
    result = ValidationResult()

    try:
        score = converter.parse(filepath)
    except Exception as e:
        result.add_error(f"Failed to parse MusicXML: {e}")
        return result

    return validate_score(score)


def validate_score(score) -> ValidationResult:
    """Validate a music21 Score object."""
    result = ValidationResult()

    _check_has_parts(score, result)
    _check_has_notes(score, result)
    _check_time_signatures(score, result)
    _check_measure_durations(score, result)
    _check_key_signature(score, result)
    _check_note_ranges(score, result)
    _check_parallel_fifths_octaves(score, result)
    _check_voice_leading(score, result)

    return result


def _check_has_parts(score, result: ValidationResult):
    """Check that score has at least one part."""
    if not score.parts or len(score.parts) == 0:
        result.add_error("Score has no parts/instruments.")


def _check_has_notes(score, result: ValidationResult):
    """Check that score has at least some notes."""
    notes = list(score.recurse().getElementsByClass(['Note', 'Chord']))
    if len(notes) == 0:
        result.add_error("Score contains no notes or chords.")
    elif len(notes) < 4:
        result.add_warning(f"Score has very few notes ({len(notes)}). May be incomplete.")


def _check_time_signatures(score, result: ValidationResult):
    """Check for valid time signatures."""
    time_sigs = list(score.recurse().getElementsByClass('TimeSignature'))
    if not time_sigs:
        result.add_warning("No explicit time signature found.")
        return

    for ts in time_sigs:
        if ts.numerator <= 0 or ts.denominator <= 0:
            result.add_error(f"Invalid time signature: {ts.ratioString}")
        if ts.numerator > 24:
            result.add_warning(f"Unusual time signature: {ts.ratioString}")


def _check_measure_durations(score, result: ValidationResult):
    """Check that measures have correct durations for their time signature."""
    for part in score.parts:
        for measure in part.getElementsByClass('Measure'):
            ts = measure.getContextByClass('TimeSignature')
            if ts is None:
                continue
            expected = ts.barDuration.quarterLength
            actual = measure.duration.quarterLength
            # Allow pickup measures (shorter) and final measures
            if actual > expected + 0.01:
                result.add_warning(
                    f"Part '{part.partName}' measure {measure.number}: "
                    f"duration {actual} exceeds time signature {ts.ratioString} ({expected} beats)."
                )


def _check_key_signature(score, result: ValidationResult):
    """Check for key signature presence."""
    key_sigs = list(score.recurse().getElementsByClass('KeySignature'))
    if not key_sigs:
        result.add_warning("No key signature found.")


def _check_note_ranges(score, result: ValidationResult):
    """Check notes are within reasonable instrument ranges."""
    for part_obj in score.parts:
        inst = part_obj.getInstrument()
        if inst is None:
            continue

        try:
            low = inst.lowestNote
            high = inst.highestNote
        except (AttributeError, TypeError):
            continue

        if low is None or high is None:
            continue

        for n in part_obj.recurse().getElementsByClass('Note'):
            if n.pitch < low.pitch if hasattr(low, 'pitch') else False:
                result.add_warning(
                    f"Note {n.nameWithOctave} in '{part_obj.partName}' is below "
                    f"instrument range (lowest: {low})."
                )
                break  # One warning per part is enough
            if n.pitch > high.pitch if hasattr(high, 'pitch') else False:
                result.add_warning(
                    f"Note {n.nameWithOctave} in '{part_obj.partName}' is above "
                    f"instrument range (highest: {high})."
                )
                break


def _check_parallel_fifths_octaves(score, result: ValidationResult):
    """Check for parallel fifths and octaves between parts (basic check)."""
    parts = score.parts
    if len(parts) < 2:
        return

    count_fifths = 0
    count_octaves = 0

    # Only check first two parts as a basic heuristic
    try:
        p1_notes = list(parts[0].recurse().getElementsByClass('Note'))
        p2_notes = list(parts[1].recurse().getElementsByClass('Note'))
    except Exception:
        return

    # Align by offset
    p1_by_offset = {}
    for n in p1_notes:
        p1_by_offset.setdefault(n.offset, []).append(n)
    p2_by_offset = {}
    for n in p2_notes:
        p2_by_offset.setdefault(n.offset, []).append(n)

    common_offsets = sorted(set(p1_by_offset.keys()) & set(p2_by_offset.keys()))

    prev_interval_semitones = None
    for offset in common_offsets:
        n1 = p1_by_offset[offset][0]
        n2 = p2_by_offset[offset][0]
        try:
            ivl = interval.Interval(n2, n1)
            semitones = abs(ivl.semitones) % 12
        except Exception:
            prev_interval_semitones = None
            continue

        if prev_interval_semitones is not None:
            if semitones == 7 and prev_interval_semitones == 7:
                count_fifths += 1
            elif semitones == 0 and prev_interval_semitones == 0:
                count_octaves += 1

        prev_interval_semitones = semitones

    if count_fifths > 3:
        result.add_warning(f"Found {count_fifths} instances of parallel fifths between top two parts.")
    if count_octaves > 3:
        result.add_warning(f"Found {count_octaves} instances of parallel octaves between top two parts.")


def _check_voice_leading(score, result: ValidationResult):
    """Basic voice leading checks."""
    for part_obj in score.parts:
        notes = list(part_obj.recurse().getElementsByClass('Note'))
        large_leaps = 0
        for i in range(1, len(notes)):
            try:
                ivl = interval.Interval(notes[i-1], notes[i])
                if abs(ivl.semitones) > 12:
                    large_leaps += 1
            except Exception:
                continue

        if large_leaps > 5:
            result.add_warning(
                f"Part '{part_obj.partName}' has {large_leaps} leaps larger than an octave. "
                "Consider smoother voice leading."
            )
