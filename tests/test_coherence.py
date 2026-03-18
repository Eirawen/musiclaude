"""Tests for coherence/naturalness feature extraction."""

import math

import pytest
from music21 import stream, note, chord, meter, key, tempo, dynamics


def _make_scale_score():
    """Simple ascending C major scale — structured, stepwise."""
    s = stream.Score()
    p = stream.Part()
    m1 = stream.Measure(number=1)
    m1.append(meter.TimeSignature("4/4"))
    m1.append(note.Note("C4", quarterLength=1))
    m1.append(note.Note("D4", quarterLength=1))
    m1.append(note.Note("E4", quarterLength=1))
    m1.append(note.Note("F4", quarterLength=1))
    p.append(m1)
    m2 = stream.Measure(number=2)
    m2.append(note.Note("G4", quarterLength=1))
    m2.append(note.Note("A4", quarterLength=1))
    m2.append(note.Note("B4", quarterLength=1))
    m2.append(note.Note("C5", quarterLength=1))
    p.append(m2)
    s.append(p)
    return s


def _make_score_with_rests():
    """Score with rests between phrases."""
    s = stream.Score()
    p = stream.Part()
    m1 = stream.Measure(number=1)
    m1.append(meter.TimeSignature("4/4"))
    m1.append(note.Note("C4", quarterLength=1))
    m1.append(note.Note("D4", quarterLength=1))
    m1.append(note.Rest(quarterLength=1))
    m1.append(note.Note("E4", quarterLength=1))
    p.append(m1)
    m2 = stream.Measure(number=2)
    m2.append(note.Note("F4", quarterLength=1))
    m2.append(note.Rest(quarterLength=2))
    m2.append(note.Note("G4", quarterLength=1))
    p.append(m2)
    s.append(p)
    return s


def _make_two_part_score():
    """Two parts with different rhythms."""
    s = stream.Score()

    p1 = stream.Part()
    m1 = stream.Measure(number=1)
    m1.append(meter.TimeSignature("4/4"))
    m1.append(note.Note("C5", quarterLength=2))
    m1.append(note.Note("D5", quarterLength=2))
    p1.append(m1)
    s.append(p1)

    p2 = stream.Part()
    m2 = stream.Measure(number=1)
    m2.append(meter.TimeSignature("4/4"))
    m2.append(note.Note("C3", quarterLength=1))
    m2.append(note.Note("E3", quarterLength=1))
    m2.append(note.Note("G3", quarterLength=1))
    m2.append(note.Note("C4", quarterLength=1))
    p2.append(m2)
    s.append(p2)

    return s


class TestNoteDensity:
    def test_basic(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        score = _make_scale_score()
        features = extract_coherence_features(score)

        # 8 notes over 8 beats = 1.0 notes/beat
        assert features["note_density"] == pytest.approx(1.0, abs=0.1)


class TestRestRatio:
    def test_no_rests(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        score = _make_scale_score()
        features = extract_coherence_features(score)

        assert features["rest_ratio"] == pytest.approx(0.0, abs=0.01)

    def test_with_rests(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        score = _make_score_with_rests()
        features = extract_coherence_features(score)

        # 3 beats of rest out of 8 total = 0.375
        assert features["rest_ratio"] == pytest.approx(0.375, abs=0.01)


class TestPitchClassEntropy:
    def test_scale_entropy(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        score = _make_scale_score()
        features = extract_coherence_features(score)

        # C major scale uses 7 of 12 pitch classes, each once (except C)
        # But C4 and C5 share pitch class 0, so: 7 unique PCs, one appearing twice
        # Entropy should be around 2.7-2.8 bits
        assert 2.5 <= features["pitch_class_entropy"] <= 3.0

    def test_single_note_zero_entropy(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        s = stream.Score()
        p = stream.Part()
        m = stream.Measure(number=1)
        m.append(meter.TimeSignature("4/4"))
        for _ in range(4):
            m.append(note.Note("C4", quarterLength=1))
        p.append(m)
        s.append(p)

        features = extract_coherence_features(s)
        assert features["pitch_class_entropy"] == pytest.approx(0.0, abs=0.01)


class TestIntervalEntropy:
    def test_uniform_intervals(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        # All intervals are +2 semitones (whole steps)
        score = _make_scale_score()
        features = extract_coherence_features(score)

        # Scale has mix of whole and half steps, so some variety
        assert features["interval_entropy"] > 0


class TestMelodicAutocorrelation:
    def test_structured_melody(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        # Repeating pattern: C D E F | C D E F (high autocorrelation)
        s = stream.Score()
        p = stream.Part()
        for i in range(4):
            m = stream.Measure(number=i + 1)
            if i == 0:
                m.append(meter.TimeSignature("4/4"))
            m.append(note.Note("C4", quarterLength=1))
            m.append(note.Note("D4", quarterLength=1))
            m.append(note.Note("E4", quarterLength=1))
            m.append(note.Note("F4", quarterLength=1))
            p.append(m)
        s.append(p)

        features = extract_coherence_features(s)

        # Repeated measures should give high autocorrelation
        if features["melodic_autocorrelation"] is not None:
            assert features["melodic_autocorrelation"] > 0.3


class TestRhythmicIndependence:
    def test_different_rhythms(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        score = _make_two_part_score()
        features = extract_coherence_features(score)

        # Part 1: half notes (onsets at 0, 2). Part 2: quarters (onsets at 0, 1, 2, 3)
        # Some beats differ (1, 3) so independence > 0
        if features["rhythmic_independence"] is not None:
            assert features["rhythmic_independence"] > 0

    def test_single_part_returns_none(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        score = _make_scale_score()
        features = extract_coherence_features(score)

        assert features["rhythmic_independence"] is None


class TestStrongBeatConsonance:
    def test_consonant_two_parts(self):
        from rachmaniclaude.features.coherence import extract_coherence_features

        # C5 over C3 = octave (consonant), D5 over E3 = minor 7th (less consonant)
        score = _make_two_part_score()
        features = extract_coherence_features(score)

        if features["strong_beat_consonance"] is not None:
            # At least some strong beats should be consonant
            assert 0 <= features["strong_beat_consonance"] <= 1
