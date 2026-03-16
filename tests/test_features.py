"""Tests for feature extraction modules."""

import pytest
from music21 import converter, stream, note, chord, meter, key, tempo, dynamics


def _make_simple_score():
    """Create a simple C major score with one part for testing."""
    s = stream.Score()
    p = stream.Part()
    m1 = stream.Measure(number=1)
    m1.append(meter.TimeSignature("4/4"))
    m1.append(key.KeySignature(0))
    m1.append(tempo.MetronomeMark(number=120))
    m1.append(dynamics.Dynamic("mf"))
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


def _make_two_part_score():
    """Create a two-part score for orchestration tests."""
    s = stream.Score()

    p1 = stream.Part()
    m1 = stream.Measure(number=1)
    m1.append(meter.TimeSignature("4/4"))
    m1.append(note.Note("E5", quarterLength=1))
    m1.append(note.Note("D5", quarterLength=1))
    m1.append(note.Note("C5", quarterLength=1))
    m1.append(note.Note("B4", quarterLength=1))
    p1.append(m1)
    s.append(p1)

    p2 = stream.Part()
    m2 = stream.Measure(number=1)
    m2.append(meter.TimeSignature("4/4"))
    m2.append(note.Note("C4", quarterLength=1))
    m2.append(note.Note("B3", quarterLength=1))
    m2.append(note.Note("A3", quarterLength=1))
    m2.append(note.Note("G3", quarterLength=1))
    p2.append(m2)
    s.append(p2)

    return s


class TestHarmonicFeatures:
    def test_basic_extraction(self):
        from musiclaude.features.harmonic import extract_harmonic_features

        score = _make_simple_score()
        features = extract_harmonic_features(score)

        assert "chord_vocabulary_size" in features
        assert "pct_extended_chords" in features
        assert "harmonic_rhythm" in features
        assert "key_stability" in features
        assert "modulation_count" in features
        assert "cadence_count_authentic" in features

    def test_key_stability_in_key(self):
        from musiclaude.features.harmonic import extract_harmonic_features

        # All notes in C major scale — should have high key stability
        score = _make_simple_score()
        features = extract_harmonic_features(score)

        if features["key_stability"] is not None:
            assert features["key_stability"] >= 0.8


class TestMelodicFeatures:
    def test_basic_extraction(self):
        from musiclaude.features.melodic import extract_melodic_features

        score = _make_simple_score()
        features = extract_melodic_features(score)

        assert "avg_interval_size" in features
        assert "pct_stepwise" in features
        assert "melodic_range" in features
        assert "pct_rising" in features
        assert "pct_falling" in features
        assert "pct_static" in features
        assert "rhythmic_variety" in features
        assert "repetition_density" in features

    def test_stepwise_motion(self):
        from musiclaude.features.melodic import extract_melodic_features

        # C D E F G A B C is all stepwise
        score = _make_simple_score()
        features = extract_melodic_features(score)

        assert features["pct_stepwise"] == 1.0
        assert features["avg_interval_size"] <= 2.0

    def test_melodic_range(self):
        from musiclaude.features.melodic import extract_melodic_features

        score = _make_simple_score()
        features = extract_melodic_features(score)

        # C4 to C5 = 12 semitones
        assert features["melodic_range"] == 12

    def test_contour(self):
        from musiclaude.features.melodic import extract_melodic_features

        # All ascending: C D E F G A B C
        score = _make_simple_score()
        features = extract_melodic_features(score)

        assert features["pct_rising"] == 1.0
        assert features["pct_falling"] == 0.0
        assert features["pct_static"] == 0.0

    def test_rhythmic_variety(self):
        from musiclaude.features.melodic import extract_melodic_features

        score = _make_simple_score()
        features = extract_melodic_features(score)

        # All quarter notes = 1 unique duration
        assert features["rhythmic_variety"] == 1


class TestStructuralFeatures:
    def test_basic_extraction(self):
        from musiclaude.features.structural import extract_structural_features

        score = _make_simple_score()
        features = extract_structural_features(score)

        assert features["num_parts"] == 1
        assert features["total_duration_beats"] == 8.0
        assert features["dynamics_count"] == 1
        assert features["tempo_count"] == 1
        assert features["time_sig_complexity"] == 0.0  # 4/4 is simple

    def test_compound_time(self):
        from musiclaude.features.structural import extract_structural_features

        s = stream.Score()
        p = stream.Part()
        m = stream.Measure(number=1)
        m.append(meter.TimeSignature("6/8"))
        m.append(note.Note("C4", quarterLength=3))
        p.append(m)
        s.append(p)

        features = extract_structural_features(s)
        assert features["time_sig_complexity"] == 1.0


class TestOrchestrationFeatures:
    def test_basic_extraction(self):
        from musiclaude.features.orchestration import extract_orchestration_features

        score = _make_two_part_score()
        features = extract_orchestration_features(score)

        assert "instrument_names" in features
        assert "instrument_count" in features
        assert "voice_crossing_count" in features
        assert "doubling_score" in features

    def test_no_voice_crossings(self):
        from musiclaude.features.orchestration import extract_orchestration_features

        # Upper part is always higher than lower part
        score = _make_two_part_score()
        features = extract_orchestration_features(score)

        assert features["voice_crossing_count"] == 0


class TestFullExtraction:
    def test_extract_features_returns_all_keys(self):
        from musiclaude.features.extract import extract_features_from_file
        import tempfile
        import os

        score = _make_simple_score()

        with tempfile.NamedTemporaryFile(suffix=".musicxml", delete=False) as f:
            score.write("musicxml", f.name)
            tmp_path = f.name

        try:
            features = extract_features_from_file(tmp_path)
            assert features is not None
            assert "filepath" in features
            assert "chord_vocabulary_size" in features
            assert "avg_interval_size" in features
            assert "num_parts" in features
            assert "instrument_count" in features
        finally:
            os.unlink(tmp_path)
