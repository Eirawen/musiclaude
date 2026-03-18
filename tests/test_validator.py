"""Tests for the structural validator."""

import pytest
from music21 import stream, note, chord, meter, key, tempo, dynamics

from rachmaniclaude.validator.structural import validate_score, ValidationResult


def _make_valid_score():
    """Create a minimal valid score."""
    s = stream.Score()
    p = stream.Part()
    m = stream.Measure(number=1)
    m.append(meter.TimeSignature("4/4"))
    m.append(key.KeySignature(0))
    m.append(note.Note("C4", quarterLength=1))
    m.append(note.Note("D4", quarterLength=1))
    m.append(note.Note("E4", quarterLength=1))
    m.append(note.Note("F4", quarterLength=1))
    p.append(m)
    s.append(p)
    return s


class TestValidator:
    def test_valid_score(self):
        score = _make_valid_score()
        result = validate_score(score)
        assert result.is_valid

    def test_empty_score(self):
        s = stream.Score()
        result = validate_score(s)
        assert not result.is_valid
        assert any("no parts" in e.lower() for e in result.errors)

    def test_no_notes(self):
        s = stream.Score()
        p = stream.Part()
        m = stream.Measure(number=1)
        m.append(meter.TimeSignature("4/4"))
        p.append(m)
        s.append(p)

        result = validate_score(s)
        assert not result.is_valid
        assert any("no notes" in e.lower() for e in result.errors)

    def test_missing_time_sig_warning(self):
        s = stream.Score()
        p = stream.Part()
        m = stream.Measure(number=1)
        m.append(note.Note("C4", quarterLength=1))
        m.append(note.Note("D4", quarterLength=1))
        m.append(note.Note("E4", quarterLength=1))
        m.append(note.Note("F4", quarterLength=1))
        p.append(m)
        s.append(p)

        result = validate_score(s)
        assert any("time signature" in w.lower() for w in result.warnings)

    def test_missing_key_sig_warning(self):
        s = stream.Score()
        p = stream.Part()
        m = stream.Measure(number=1)
        m.append(meter.TimeSignature("4/4"))
        m.append(note.Note("C4", quarterLength=4))
        p.append(m)
        s.append(p)

        result = validate_score(s)
        assert any("key signature" in w.lower() for w in result.warnings)

    def test_summary_format(self):
        result = ValidationResult()
        assert result.summary() == "VALID"

        result.add_error("Test error")
        assert "INVALID" in result.summary()
        assert "ERROR: Test error" in result.summary()

        result.add_warning("Test warning")
        assert "WARNING: Test warning" in result.summary()
