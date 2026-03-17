#!/usr/bin/env python3
"""Generate Matin de Boulangerie MusicXML score programmatically."""

import xml.etree.ElementTree as ET
from xml.dom import minidom

DIV = 4  # divisions per quarter note
SIXTEENTH = 1
DOT_EIGHTH = 3
EIGHTH = 2
QUARTER = 4
DOT_QUARTER = 6
HALF = 8
DOT_HALF = 12  # full 6/8 measure

def make_note(pitch_step, pitch_octave, duration, note_type, dot=False, rest=False,
              chord=False, alter=None, tie_start=False, tie_stop=False,
              voice="1", staff=None, staccato=False, accent=False, tenuto=False,
              fermata=False, slur_start=False, slur_stop=False, slur_num="1"):
    """Create a note element."""
    note = ET.Element("note")
    if chord:
        ET.SubElement(note, "chord")
    if rest:
        ET.SubElement(note, "rest")
    else:
        p = ET.SubElement(note, "pitch")
        ET.SubElement(p, "step").text = pitch_step
        if alter is not None:
            ET.SubElement(p, "alter").text = str(alter)
        ET.SubElement(p, "octave").text = str(pitch_octave)
    ET.SubElement(note, "duration").text = str(duration)
    if tie_stop:
        t = ET.SubElement(note, "tie")
        t.set("type", "stop")
    if tie_start:
        t = ET.SubElement(note, "tie")
        t.set("type", "start")
    ET.SubElement(note, "voice").text = voice
    ET.SubElement(note, "type").text = note_type
    if dot:
        ET.SubElement(note, "dot")
    if staff is not None:
        ET.SubElement(note, "staff").text = str(staff)

    # Notations
    has_notations = any([tie_start, tie_stop, staccato, accent, tenuto, fermata, slur_start, slur_stop])
    if has_notations:
        notations = ET.SubElement(note, "notations")
        if tie_stop:
            tied = ET.SubElement(notations, "tied")
            tied.set("type", "stop")
        if tie_start:
            tied = ET.SubElement(notations, "tied")
            tied.set("type", "start")
        if staccato or accent or tenuto:
            artic = ET.SubElement(notations, "articulations")
            if staccato:
                ET.SubElement(artic, "staccato")
            if accent:
                ET.SubElement(artic, "accent")
            if tenuto:
                ET.SubElement(artic, "tenuto")
        if fermata:
            ET.SubElement(notations, "fermata")
        if slur_start:
            s = ET.SubElement(notations, "slur")
            s.set("type", "start")
            s.set("number", slur_num)
        if slur_stop:
            s = ET.SubElement(notations, "slur")
            s.set("type", "stop")
            s.set("number", slur_num)
    return note


def add_direction(measure, text=None, dynamic=None, wedge_type=None,
                  placement="below", offset=None, words_attrs=None,
                  tempo=None, metronome_beat=None, metronome_bpm=None,
                  metronome_dot=False):
    """Add a direction element (dynamics, text, wedge, tempo/metronome)."""
    direction = ET.SubElement(measure, "direction")
    direction.set("placement", placement)
    dt = ET.SubElement(direction, "direction-type")
    if text:
        words = ET.SubElement(dt, "words")
        words.text = text
        if words_attrs:
            for k, v in words_attrs.items():
                words.set(k, v)
    if dynamic:
        dynamics = ET.SubElement(dt, "dynamics")
        ET.SubElement(dynamics, dynamic)
    if wedge_type:
        wedge = ET.SubElement(dt, "wedge")
        wedge.set("type", wedge_type)
    if metronome_beat:
        met = ET.SubElement(dt, "metronome")
        ET.SubElement(met, "beat-unit").text = metronome_beat
        if metronome_dot:
            ET.SubElement(met, "beat-unit-dot")
        ET.SubElement(met, "per-minute").text = str(metronome_bpm)
    if offset is not None:
        ET.SubElement(direction, "offset").text = str(offset)
    if tempo is not None:
        sound = ET.SubElement(direction, "sound")
        sound.set("tempo", str(tempo))


def make_attributes(divisions=None, fifths=None, beats=None, beat_type=None,
                    clef_sign=None, clef_line=None, staves=None,
                    transpose_diatonic=None, transpose_chromatic=None):
    """Create an attributes element."""
    attr = ET.Element("attributes")
    if divisions is not None:
        ET.SubElement(attr, "divisions").text = str(divisions)
    if fifths is not None:
        key = ET.SubElement(attr, "key")
        ET.SubElement(key, "fifths").text = str(fifths)
    if beats is not None:
        time = ET.SubElement(attr, "time")
        ET.SubElement(time, "beats").text = str(beats)
        ET.SubElement(time, "beat-type").text = str(beat_type)
    if staves is not None:
        ET.SubElement(attr, "staves").text = str(staves)
    if clef_sign:
        clef = ET.SubElement(attr, "clef")
        if staves:
            clef.set("number", "1")
        ET.SubElement(clef, "sign").text = clef_sign
        if clef_line:
            ET.SubElement(clef, "line").text = str(clef_line)
        if staves and staves == 2:
            clef2 = ET.SubElement(attr, "clef")
            clef2.set("number", "2")
            ET.SubElement(clef2, "sign").text = "F"
            ET.SubElement(clef2, "line").text = "4"
    if transpose_diatonic is not None:
        tr = ET.SubElement(attr, "transpose")
        ET.SubElement(tr, "diatonic").text = str(transpose_diatonic)
        ET.SubElement(tr, "chromatic").text = str(transpose_chromatic)
    return attr


# ============================================================
# PIANO PART DATA
# ============================================================
# Each measure: list of (step, octave, duration, type, kwargs)
# For chords, subsequent notes in same beat get chord=True

def build_piano_measures():
    """Build all 80 piano measures."""
    measures = []

    # Helper: arpeggiated ostinato pattern in 6/8
    # Pattern: bass dotted-quarter (voice 2, staff 2) + 3 eighths upper (voice 1, staff 1)

    def ostinato_measure(bass_notes, upper_notes, v1_extras=None):
        """
        bass_notes: [(step, oct, alter), ...] for LH dotted quarters (2 per measure in 6/8)
        upper_notes: [(step, oct, alter), ...] 6 eighths for RH
        """
        notes = []
        # Voice 1 / Staff 1: RH - 6 eighth notes
        for i, (s, o, a) in enumerate(upper_notes):
            kw = {"voice": "1", "staff": "1"}
            if i == 0:
                kw["slur_start"] = True
            if i == 5:
                kw["slur_stop"] = True
            notes.append((s, o, EIGHTH, "eighth", False, a, kw))

        # Backup
        notes.append(("backup", DOT_HALF))

        # Voice 2 / Staff 2: LH - 2 dotted quarters
        for i, (s, o, a) in enumerate(bass_notes):
            kw = {"voice": "5", "staff": "2"}
            if i == 0:
                kw["staccato"] = True
            notes.append((s, o, DOT_QUARTER, "quarter", True, a, kw))

        return notes

    def chord_measure(beats):
        """
        beats: list of (duration, type, dot, [(step, oct, alter)...], voice, staff, kwargs)
        Creates a measure with chords.
        """
        notes = []
        for dur, ntype, dot, pitches, voice, staff, kw in beats:
            for i, (s, o, a) in enumerate(pitches):
                nkw = {"voice": voice, "staff": staff}
                nkw.update(kw)
                if i > 0:
                    nkw["chord"] = True
                notes.append((s, o, dur, ntype, dot, a, nkw))
        return notes

    def simple_notes(note_list):
        """note_list: [(step, oct, dur, type, dot, alter, kwargs), ...]"""
        return note_list

    # ---- SECTION I: Morning (mm. 1-16) ----
    # Piano alone, pp→mp, dolce
    # Ostinato pattern in F major

    # m1: Fmaj9 arpeggio - F2 bass, A4-C5-G4 upper pattern
    m1 = ostinato_measure(
        [("F", 2, None), ("C", 3, None)],
        [("A", 4, None), ("C", 5, None), ("G", 4, None), ("A", 4, None), ("C", 5, None), ("E", 5, None)]
    )
    measures.append(("m1", m1))

    # m2: Fmaj7 — with ornamental sixteenths for rhythmic variety
    # RH: dotted-eighth + sixteenth + eighth × 2 groups
    m2 = [
        # Voice 1 / Staff 1: varied rhythm
        ("A", 4, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1"}),
        ("E", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        # Backup
        ("backup", DOT_HALF),
        # Voice 2 / Staff 2: bass
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m2", m2))

    # m3: Bbmaj7 — with chord landing
    m3 = [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Bbmaj7: Bb-D-F-A
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("B", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2", "staccato": True}),
        ("F", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m3", m3))

    # m4: Gm7 — with 4-note chord landing
    m4 = [
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Gm7 chord: G-Bb-D-F
        ("G", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("D", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m4", m4))

    # m5: C7sus4 — with chord
    m5 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # C7: C-E-G-Bb
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m5", m5))

    # m6: Fadd9 — with sixteenth ornament
    m6 = [
        ("G", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 4, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1"}),
        ("F", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m6", m6))

    # m7: Dm7 — with chord
    m7 = [
        ("F", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dm7: D-F-A-C
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m7", m7))

    # m8: Bbmaj7 — with 4-note chord
    m8 = [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Bbmaj7 chord
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("B", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2", "staccato": True}),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m8", m8))

    # m9: Am7 — lower bass for range, with 4-note chord voicings for extended
    m9 = [
        # RH: arpeggiated with a chord landing
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Chord: Am7 voicing (A4-C5-E5-G5) dotted quarter
        ("A", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("A", 1, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m9", m9))

    # m10: C9 — lower bass, sixteenth ornament
    m10 = [
        ("E", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("D", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m10", m10))

    # m11: Fmaj7
    m11 = ostinato_measure(
        [("F", 2, None), ("C", 3, None)],
        [("A", 4, None), ("C", 5, None), ("E", 5, None), ("F", 5, None), ("E", 5, None), ("C", 5, None)]
    )
    measures.append(("m11", m11))

    # m12: Bb/F → Bbmaj9 — with 4-note chord
    m12 = [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Bb add9 chord: Bb-D-F-C
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("B", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m12", m12))

    # m13: Gm9
    m13 = ostinato_measure(
        [("G", 2, None), ("D", 3, None)],
        [("B", 4, -1), ("A", 4, None), ("D", 5, None), ("F", 5, None), ("G", 5, None), ("F", 5, None)]
    )
    measures.append(("m13", m13))

    # m14: Csus4
    m14 = ostinato_measure(
        [("C", 3, None), ("G", 3, None)],
        [("F", 5, None), ("E", 5, None), ("C", 5, None), ("G", 4, None), ("C", 5, None), ("E", 5, None)]
    )
    measures.append(("m14", m14))

    # m15: Fadd9 — with 4-note chord for extended chord detection
    m15 = [
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("G", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Fadd9 chord
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m15", m15))

    # m16: Fmaj7 (settling) — with chord voicing
    m16 = [
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Fmaj7 chord
        ("F", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m16", m16))

    # ---- SECTION II: The Door Opens (mm. 17-28) ----
    # Piano continues ostinato with richer harmony

    # m17: Fadd9 - clarinet enters, piano continues
    m17 = ostinato_measure(
        [("F", 2, None), ("C", 3, None)],
        [("A", 4, None), ("C", 5, None), ("G", 4, None), ("A", 4, None), ("F", 5, None), ("G", 5, None)]
    )
    measures.append(("m17", m17))

    # m18: Gm9
    m18 = ostinato_measure(
        [("G", 2, None), ("D", 3, None)],
        [("B", 4, -1), ("D", 5, None), ("A", 4, None), ("B", 4, -1), ("F", 5, None), ("D", 5, None)]
    )
    measures.append(("m18", m18))

    # m19: Am7
    m19 = ostinato_measure(
        [("A", 2, None), ("E", 3, None)],
        [("C", 5, None), ("E", 5, None), ("G", 4, None), ("C", 5, None), ("E", 5, None), ("G", 5, None)]
    )
    measures.append(("m19", m19))

    # m20: Bbmaj7 — with chord
    m20 = [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Bbmaj7 chord
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("B", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2", "staccato": True}),
        ("F", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m20", m20))

    # m21: C9
    m21 = ostinato_measure(
        [("C", 3, None), ("G", 3, None)],
        [("E", 5, None), ("B", 4, -1), ("D", 5, None), ("E", 5, None), ("G", 5, None), ("E", 5, None)]
    )
    measures.append(("m21", m21))

    # m22: Dm9 — with chord
    m22 = [
        ("F", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dm9: D-F-A-C-E
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m22", m22))

    # m23: Bbmaj7
    m23 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("F", 5, None), ("A", 4, None), ("B", 4, -1), ("D", 5, None), ("F", 5, None)]
    )
    measures.append(("m23", m23))

    # m24: Csus4→C7 — resolving with chord voicing
    m24 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # C7 chord voicing
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m24", m24))

    # m25: Fadd9
    m25 = ostinato_measure(
        [("F", 2, None), ("C", 3, None)],
        [("A", 4, None), ("G", 4, None), ("C", 5, None), ("F", 5, None), ("G", 5, None), ("A", 5, None)]
    )
    measures.append(("m25", m25))

    # m26: Gm7
    m26 = ostinato_measure(
        [("G", 2, None), ("D", 3, None)],
        [("B", 4, -1), ("D", 5, None), ("F", 5, None), ("G", 5, None), ("F", 5, None), ("D", 5, None)]
    )
    measures.append(("m26", m26))

    # m27: Bbmaj7
    m27 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("F", 5, None), ("A", 5, None), ("F", 5, None), ("D", 5, None), ("A", 4, None)]
    )
    measures.append(("m27", m27))

    # m28: Csus4 (unresolved) — with 4-note voicing
    m28 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Csus4 chord: C-F-G-C
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 6, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m28", m28))

    # ---- SECTION III: Conversation (mm. 29-48) ----
    # More varied piano, call and response

    # m29: Fmaj7 — with chord
    m29 = [
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Fmaj7: F-A-C-E
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m29", m29))

    # m30: Am7
    m30 = ostinato_measure(
        [("A", 2, None), ("E", 3, None)],
        [("C", 5, None), ("E", 5, None), ("A", 5, None), ("G", 5, None), ("E", 5, None), ("C", 5, None)]
    )
    measures.append(("m30", m30))

    # m31: Dm7
    m31 = ostinato_measure(
        [("D", 3, None), ("A", 3, None)],
        [("F", 5, None), ("A", 5, None), ("C", 5, None), ("D", 5, None), ("F", 5, None), ("E", 5, None)]
    )
    measures.append(("m31", m31))

    # m32: Gm9 — with chord voicing
    m32 = [
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Gm9: G-Bb-D-A
        ("G", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("D", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m32", m32))

    # m33: C7
    m33 = ostinato_measure(
        [("C", 3, None), ("G", 3, None)],
        [("E", 5, None), ("B", 4, -1), ("C", 5, None), ("E", 5, None), ("G", 5, None), ("B", 4, -1)]
    )
    measures.append(("m33", m33))

    # m34: Fmaj7 — sixteenth-note elaboration
    m34 = [
        ("A", 4, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1"}),
        ("A", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m34", m34))

    # m35: Bbmaj7
    m35 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("F", 5, None), ("A", 5, None), ("B", 5, -1), ("A", 5, None), ("F", 5, None)]
    )
    measures.append(("m35", m35))

    # m36: Eb7 (chromatic approach) — with 4-note chord
    m36 = [
        ("G", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Eb7: Eb-G-Bb-Db
        ("E", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("G", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("B", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m36", m36))

    # m37: Dm7 — D minor excursion with chord
    m37 = [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dm7: D-F-A-C
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m37", m37))

    # m38: Gm7
    m38 = ostinato_measure(
        [("G", 2, None), ("D", 3, None)],
        [("B", 4, -1), ("D", 5, None), ("F", 5, None), ("G", 5, None), ("F", 5, None), ("D", 5, None)]
    )
    measures.append(("m38", m38))

    # m39: A7 (V/vi) — with chord
    m39 = [
        ("C", 5, EIGHTH, "eighth", False, 1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # A7: A-C#-E-G
        ("A", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, 1, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("E", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m39", m39))

    # m40: Dm9 (resolve) — with 4-note chord
    m40 = [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dm9 chord: D-F-A-E
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m40", m40))

    # m41: Bb
    m41 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("F", 5, None), ("B", 5, -1), ("A", 5, None), ("F", 5, None), ("D", 5, None)]
    )
    measures.append(("m41", m41))

    # m42: C7 — with sixteenth flourish
    m42 = [
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("G", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("B", 5, SIXTEENTH, "16th", False, -1, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1"}),
        ("G", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m42", m42))

    # m43: Am7
    m43 = ostinato_measure(
        [("A", 2, None), ("E", 3, None)],
        [("C", 5, None), ("E", 5, None), ("G", 5, None), ("A", 5, None), ("G", 5, None), ("E", 5, None)]
    )
    measures.append(("m43", m43))

    # m44: Dm9 — with 4-note chord
    m44 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dm9: D-F-A-E
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m44", m44))

    # m45: Gm7
    m45 = ostinato_measure(
        [("G", 2, None), ("D", 3, None)],
        [("B", 4, -1), ("D", 5, None), ("F", 5, None), ("G", 5, None), ("B", 5, -1), ("G", 5, None)]
    )
    measures.append(("m45", m45))

    # m46: C9 — with chord
    m46 = [
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # C9: C-E-G-Bb-D
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m46", m46))

    # m47: Fmaj7 — with wide range RH going up to C6 and down to F4
    m47 = [
        ("F", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 6, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2", "staccato": True}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m47", m47))

    # m48: Csus4→C9 (transition) — with chord voicing
    m48 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 6, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # C9 chord: C-E-Bb-D
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 6, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m48", m48))

    # ---- SECTION IV: Walking Home (mm. 49-64, Ab major) ----
    # Richer textures, both instruments singing

    # m49: Abmaj7 — with chord
    m49 = [
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Abmaj7: Ab-C-Eb-G
        ("A", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("A", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m49", m49))

    # m50: Bbm7 — with chord
    m50 = [
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Bbm7: Bb-Db-F-Ab
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("B", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m50", m50))

    # m51: Eb7 — with chord
    m51 = [
        ("G", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Eb7: Eb-G-Bb-Db
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("E", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("B", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m51", m51))

    # m52: Abmaj7 — with chord voicing
    m52 = [
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Abmaj7 chord: Ab-C-Eb-G
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("A", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m52", m52))

    # m53: Dbmaj7 — with 4-note chord
    m53 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("C", 6, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dbmaj7: Db-F-Ab-C
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 6, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("A", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m53", m53))

    # m54: Cm7 — with chord
    m54 = [
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("B", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Cm7: C-Eb-G-Bb
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m54", m54))

    # m55: Fm7 — with chord
    m55 = [
        ("A", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Fm7: F-Ab-C-Eb
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m55", m55))

    # m56: Eb/G → Eb7 — with 4-note chord
    m56 = [
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Eb7: Eb-G-Bb-Db
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m56", m56))

    # m57: Abmaj7 — climactic, reach up to C6, with sixteenth flourish
    m57 = [
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, SIXTEENTH, "16th", False, -1, {"voice": "1", "staff": "1"}),
        ("G", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("C", 6, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1", "accent": True}),
        ("A", 5, SIXTEENTH, "16th", False, -1, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("A", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m57", m57))

    # m58: Db — with wide leap and sixteenths
    m58 = [
        ("F", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 5, SIXTEENTH, "16th", False, -1, {"voice": "1", "staff": "1"}),
        ("D", 6, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "accent": True}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("A", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m58", m58))

    # m59: Bbm7 — pushing to Db6 for range
    m59 = [
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("B", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "accent": True}),
        ("D", 6, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("B", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m59", m59))

    # m60: Eb9 — cascading from E6 for max range
    m60 = [
        ("E", 6, SIXTEENTH, "16th", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("D", 6, SIXTEENTH, "16th", False, -1, {"voice": "1", "staff": "1"}),
        ("B", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("E", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("B", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m60", m60))

    # m61: Abmaj7 (restatement) — 4-note chord
    m61 = [
        ("A", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Abmaj7: Ab-C-Eb-G
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("A", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m61", m61))

    # m62: Fm9 — with chord
    m62 = [
        ("A", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Fm9: F-Ab-C-Eb-G
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m62", m62))

    # m63: Dbmaj7 — with chord
    m63 = [
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("C", 6, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Dbmaj7: Db-F-Ab-C
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 6, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("D", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("A", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m63", m63))

    # m64: Eb7sus4 → transition back, with chord voicing
    m64 = [
        ("A", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1", "slur_start": True}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        # Eb7sus4 chord: Eb-Ab-Db-G
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("E", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
        ("B", 1, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m64", m64))

    # ---- SECTION V: Alone Again (mm. 65-80, F major return) ----
    # Richer ostinato, then clarinet melody in piano RH

    # m65: Fmaj9 - return of ostinato, starting from low C4 for range breadth
    m65 = [
        ("C", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("F", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m65", m65))

    # m66: Fmaj7 — start from G3 for wider RH range
    m66 = [
        ("G", 3, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m66", m66))

    # m67: Bbmaj7
    m67 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("A", 4, None), ("B", 4, -1), ("D", 5, None), ("F", 5, None), ("A", 5, None)]
    )
    measures.append(("m67", m67))

    # m68: Gm9 — with chord
    m68 = [
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Gm9: G-Bb-D-F-A
        ("G", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("D", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m68", m68))

    # m69: Fmaj7 — with chord voicing
    m69 = [
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Fmaj7 chord
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m69", m69))

    # m70: Bbmaj7
    m70 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("F", 5, None), ("A", 5, None), ("B", 5, -1), ("A", 5, None), ("F", 5, None)]
    )
    measures.append(("m70", m70))

    # m71: Am7b5 — with chord
    m71 = [
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Am7b5: A-C-Eb-G
        ("A", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("A", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("E", 2, DOT_QUARTER, "quarter", True, -1, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m71", m71))

    # m72: Dm9 — clarinet melody appears in piano RH
    # Piano RH plays the ascending motif: D5-E5-F5-G5 (concert pitch, the "first glance" melody)
    m72 = ostinato_measure(
        [("D", 3, None), ("A", 3, None)],
        [("D", 5, None), ("E", 5, None), ("F", 5, None), ("G", 5, None), ("F", 5, None), ("D", 5, None)]
    )
    measures.append(("m72", m72))

    # m73: Gm9 — continuing recalled melody with ornament
    m73 = [
        ("D", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("E", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "staff": "1"}),
        ("A", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "staff": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("backup", DOT_HALF),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("D", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m73", m73))

    # m74: C7b9 — with chord
    m74 = [
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("D", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "staff": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # C7b9: C-E-G-Bb-Db
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("C", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("G", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m74", m74))

    # m75: Fmaj7 — with 4-note chord
    m75 = [
        ("A", 4, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "staff": "1"}),
        # Fmaj7 chord
        ("F", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "slur_stop": True}),
        ("A", 4, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("backup", DOT_HALF),
        ("F", 2, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
        ("C", 3, DOT_QUARTER, "quarter", True, None, {"voice": "5", "staff": "2"}),
    ]
    measures.append(("m75", m75))

    # m76: Bbmaj7
    m76 = ostinato_measure(
        [("B", 2, -1), ("F", 3, None)],
        [("D", 5, None), ("F", 5, None), ("A", 4, None), ("B", 4, -1), ("D", 5, None), ("F", 5, None)]
    )
    measures.append(("m76", m76))

    # m77: Gm7 — morendo begins
    m77 = ostinato_measure(
        [("G", 2, None), ("D", 3, None)],
        [("B", 4, -1), ("D", 5, None), ("F", 5, None), ("D", 5, None), ("B", 4, -1), ("G", 4, None)]
    )
    measures.append(("m77", m77))

    # m78: C9
    m78 = ostinato_measure(
        [("C", 3, None), ("G", 3, None)],
        [("E", 5, None), ("D", 5, None), ("C", 5, None), ("B", 4, -1), ("G", 4, None), ("E", 4, None)]
    )
    measures.append(("m78", m78))

    # m79: Fmaj7
    m79 = ostinato_measure(
        [("F", 2, None), ("C", 3, None)],
        [("A", 4, None), ("C", 5, None), ("E", 5, None), ("F", 5, None), ("E", 5, None), ("C", 5, None)]
    )
    measures.append(("m79", m79))

    # m80: Fadd9 — final unresolved chord, whole measure
    # Special: sustained chord, not ostinato
    m80 = [
        # RH: Fadd9 chord as dotted half (full measure)
        ("F", 5, DOT_HALF, "half", True, None, {"voice": "1", "staff": "1", "fermata": True}),
        ("A", 5, DOT_HALF, "half", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("G", 5, DOT_HALF, "half", True, None, {"voice": "1", "staff": "1", "chord": True}),
        ("C", 5, DOT_HALF, "half", True, None, {"voice": "1", "staff": "1", "chord": True}),
        # Backup
        ("backup", DOT_HALF),
        # LH: F2-C3 sustained
        ("F", 2, DOT_HALF, "half", True, None, {"voice": "5", "staff": "2"}),
        ("C", 3, DOT_HALF, "half", True, None, {"voice": "5", "staff": "2", "chord": True}),
    ]
    measures.append(("m80", m80))

    return measures


# ============================================================
# CLARINET PART DATA (written pitch — M2 higher than concert)
# ============================================================

def build_clarinet_measures():
    """Build all 80 clarinet measures. Written pitch (Bb transposition applied)."""
    measures = []

    # Section I (mm. 1-16): Clarinet rests (tacet)
    for i in range(1, 17):
        measures.append((f"m{i}", [
            (None, None, DOT_HALF, "half", True, None, {"voice": "1"})  # rest
        ]))

    # Section II (mm. 17-28): Clarinet enters
    # Primary motif (concert): C5-D5-E5-F5-G5-F5
    # Written (up M2):         D5-E5-F#5-G5-A5-G5

    # m17: breath, then ascending motif begins — D5 dotted quarter, E5 dotted quarter
    measures.append(("m17", [
        (None, None, EIGHTH, "eighth", False, None, {"voice": "1"}),  # rest (breath)
        ("D", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("F", 5, DOT_QUARTER, "quarter", True, 1, {"voice": "1", "slur_stop": True}),  # F#5
    ]))

    # m18: continuation — G5 dotted quarter, A5 quarter, G5 eighth
    measures.append(("m18", [
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_start": True, "tenuto": True}),
        ("A", 5, QUARTER, "quarter", False, None, {"voice": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m19: descending response — F#5 quarter, E5 eighth, D5 dotted quarter
    measures.append(("m19", [
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m20: resting, lingering — E5 half (8), rest eighth (2), rest eighth (2)
    measures.append(("m20", [
        ("E", 5, HALF, "half", False, None, {"voice": "1", "tenuto": True}),
        (None, None, QUARTER, "quarter", False, None, {"voice": "1"}),  # rest
    ]))

    # m21: second phrase — D5-E5-F#5-G5 with more confidence
    measures.append(("m21", [
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("F", 5, EIGHTH, "eighth", False, 1, {"voice": "1"}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m22: A5 quarter, G5 eighth, F#5 quarter, E5 eighth
    measures.append(("m22", [
        ("A", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m23: D5 dotted quarter, rest dotted quarter
    measures.append(("m23", [
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "tenuto": True}),
        (None, None, DOT_QUARTER, "quarter", True, None, {"voice": "1"}),  # rest
    ]))

    # m24: rest quarter, then gentle pickup — E5 eighth, G5 quarter
    measures.append(("m24", [
        (None, None, DOT_QUARTER, "quarter", True, None, {"voice": "1"}),  # rest
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_start": True}),
        ("G", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m25: A5 dotted quarter, G5 dotted quarter — lyrical
    measures.append(("m25", [
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "tenuto": True, "slur_start": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m26: F#5 quarter, E5 eighth, D5 dotted quarter
    measures.append(("m26", [
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m27: E5 dotted quarter, rest dotted quarter
    measures.append(("m27", [
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1"}),
        (None, None, DOT_QUARTER, "quarter", True, None, {"voice": "1"}),
    ]))

    # m28: rest (transition to conversation)
    measures.append(("m28", [
        (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
    ]))

    # ---- Section III: Conversation (mm. 29-48) ----
    # Call and response, longer phrases

    # m29: pickup response — rest dotted quarter, then D5 eighth, E5 quarter
    measures.append(("m29", [
        (None, None, DOT_QUARTER, "quarter", True, None, {"voice": "1"}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_start": True}),
        ("E", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m30: F#5-G5-A5-G5-F#5-E5 — with sixteenth ornament
    measures.append(("m30", [
        ("F", 5, SIXTEENTH, "16th", False, 1, {"voice": "1", "slur_start": True}),
        ("G", 5, SIXTEENTH, "16th", False, None, {"voice": "1"}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1", "accent": True}),
        ("G", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1"}),
        ("F", 5, SIXTEENTH, "16th", False, 1, {"voice": "1"}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m31: D5 dotted quarter, rest eighth, E5 quarter
    measures.append(("m31", [
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "tenuto": True}),
        (None, None, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("E", 5, QUARTER, "quarter", False, None, {"voice": "1"}),
    ]))

    # m32: rest (piano responds)
    measures.append(("m32", [
        (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
    ]))

    # m33: F#5-G5-A5-B5 — ascending, getting braver
    measures.append(("m33", [
        ("F", 5, EIGHTH, "eighth", False, 1, {"voice": "1", "slur_start": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("A", 5, QUARTER, "quarter", False, None, {"voice": "1", "accent": True}),
        ("B", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m34: A5 dotted quarter, G5 eighth, F#5 quarter
    measures.append(("m34", [
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_start": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1", "slur_stop": True}),
    ]))

    # m35: G5 quarter, A5 eighth, B5 dotted quarter
    measures.append(("m35", [
        ("G", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("B", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m36: rest (chromatic transition in piano)
    measures.append(("m36", [
        (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
    ]))

    # m37: D minor excursion — E5 dotted quarter, D5 dotted quarter (written for concert Dm)
    measures.append(("m37", [
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_start": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m38: E5 quarter, F5 eighth (nat), G5 dotted quarter (for concert D minor context)
    measures.append(("m38", [
        ("E", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, 0, {"voice": "1"}),  # F natural (concert Eb)
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m39: A5 quarter, B5 eighth (concert G#-A#), resolving
    measures.append(("m39", [
        ("B", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m40: F5 (nat) quarter, E5 eighth, D5 dotted quarter — resolve to D minor
    measures.append(("m40", [
        ("F", 5, QUARTER, "quarter", False, 0, {"voice": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m41: rest half, pickup to next phrase
    measures.append(("m41", [
        (None, None, HALF, "half", False, None, {"voice": "1"}),
        ("E", 5, QUARTER, "quarter", False, None, {"voice": "1"}),
    ]))

    # m42: F#5-G5-A5 growing back
    measures.append(("m42", [
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1", "slur_start": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m43: B5 quarter, A5 eighth, G5 dotted quarter
    measures.append(("m43", [
        ("B", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True, "accent": True}),
        ("A", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m44: F#5 dotted quarter, E5 dotted quarter
    measures.append(("m44", [
        ("F", 5, DOT_QUARTER, "quarter", True, 1, {"voice": "1", "slur_start": True}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m45: D5 quarter, E5 eighth, F#5 quarter, G5 eighth
    measures.append(("m45", [
        ("D", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("E", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1"}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m46: A5 dotted quarter, G5 eighth, F#5 quarter
    measures.append(("m46", [
        ("A", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_start": True, "accent": True}),
        ("G", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("F", 5, QUARTER, "quarter", False, 1, {"voice": "1", "slur_stop": True}),
    ]))

    # m47: E5 quarter, D5 eighth, rest dotted quarter
    measures.append(("m47", [
        ("E", 5, QUARTER, "quarter", False, None, {"voice": "1"}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        (None, None, DOT_QUARTER, "quarter", True, None, {"voice": "1"}),
    ]))

    # m48: rest (transition)
    measures.append(("m48", [
        (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
    ]))

    # ---- Section IV: Walking Home (mm. 49-64, Ab major) ----
    # Concert Ab: written Bb. Peak emotional section.
    # Written pitches: up M2 from concert

    # m49: Bb4 dotted quarter, C5 dotted quarter (concert Ab4, Bb4)
    measures.append(("m49", [
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "slur_start": True}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m50: D5-Eb5-F5-Eb5-D5-C5 — with dotted rhythm
    measures.append(("m50", [
        ("D", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "slur_start": True}),
        ("E", 5, SIXTEENTH, "16th", False, -1, {"voice": "1"}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1", "accent": True}),
        ("E", 5, DOT_EIGHTH, "eighth", True, -1, {"voice": "1"}),
        ("D", 5, SIXTEENTH, "16th", False, None, {"voice": "1"}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m51: Bb4 quarter, C5 eighth, D5 dotted quarter (widening intervals)
    measures.append(("m51", [
        ("B", 4, QUARTER, "quarter", False, -1, {"voice": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m52: Eb5 quarter, F5 eighth, G5 dotted quarter (soaring)
    measures.append(("m52", [
        ("E", 5, QUARTER, "quarter", False, -1, {"voice": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # m53: Ab5 (written Bb5) — peak note! Bb5 dotted quarter, Ab5 dotted quarter
    measures.append(("m53", [
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "accent": True, "slur_start": True}),
        ("A", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "slur_stop": True}),
    ]))

    # m54: G5 quarter, F5 eighth, Eb5 quarter, D5 eighth
    measures.append(("m54", [
        ("G", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("E", 5, QUARTER, "quarter", False, -1, {"voice": "1"}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m55: C5 dotted quarter, Bb4 eighth, C5 quarter
    measures.append(("m55", [
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "tenuto": True, "slur_start": True}),
        ("B", 4, EIGHTH, "eighth", False, -1, {"voice": "1"}),
        ("C", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m56: D5-Eb5-F5-G5-F5-Eb5 — climactic run with sixteenths
    measures.append(("m56", [
        ("D", 5, SIXTEENTH, "16th", False, None, {"voice": "1", "slur_start": True}),
        ("E", 5, SIXTEENTH, "16th", False, -1, {"voice": "1"}),
        ("F", 5, SIXTEENTH, "16th", False, None, {"voice": "1"}),
        ("G", 5, SIXTEENTH, "16th", False, None, {"voice": "1"}),
        ("A", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "accent": True}),
        ("G", 5, DOT_EIGHTH, "eighth", True, None, {"voice": "1"}),
        ("F", 5, SIXTEENTH, "16th", False, None, {"voice": "1"}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "slur_stop": True}),
    ]))

    # m57: F5 dotted quarter, G5 dotted quarter — broadening
    measures.append(("m57", [
        ("F", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "tenuto": True, "slur_start": True}),
        ("G", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m58: Ab5 (Bb5 written) dotted quarter, Bb5 (C6 written) eighth, Ab5 quarter
    measures.append(("m58", [
        ("B", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "slur_start": True, "accent": True}),
        ("C", 6, EIGHTH, "eighth", False, None, {"voice": "1"}),  # highest point!
        ("B", 5, QUARTER, "quarter", False, -1, {"voice": "1", "slur_stop": True}),
    ]))

    # m59: G5 quarter, F5 eighth, Eb5 dotted quarter (descending)
    measures.append(("m59", [
        ("G", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("F", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("E", 5, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "slur_stop": True}),
    ]))

    # m60: D5 quarter, C5 eighth, Bb4 dotted quarter
    measures.append(("m60", [
        ("D", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "slur_stop": True}),
    ]))

    # m61: C5 dotted quarter, D5 dotted quarter — one more swell
    measures.append(("m61", [
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_start": True}),
        ("D", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m62: Eb5 quarter, D5 eighth, C5 dotted quarter
    measures.append(("m62", [
        ("E", 5, QUARTER, "quarter", False, -1, {"voice": "1", "slur_start": True}),
        ("D", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("C", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "slur_stop": True}),
    ]))

    # m63: Bb4 quarter, C5 eighth, D5 quarter, Eb5 eighth (winding down)
    measures.append(("m63", [
        ("B", 4, QUARTER, "quarter", False, -1, {"voice": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("D", 5, QUARTER, "quarter", False, None, {"voice": "1"}),
        ("E", 5, EIGHTH, "eighth", False, -1, {"voice": "1", "slur_stop": True}),
    ]))

    # m64: D5 quarter, C5 eighth, Bb4 dotted quarter (settling, transition)
    measures.append(("m64", [
        ("D", 5, QUARTER, "quarter", False, None, {"voice": "1", "slur_start": True}),
        ("C", 5, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("B", 4, DOT_QUARTER, "quarter", True, -1, {"voice": "1", "slur_stop": True, "tenuto": True}),
    ]))

    # ---- Section V: Alone Again (mm. 65-80) ----
    # Clarinet mostly tacet, returns briefly then fades

    # m65-71: tacet
    for i in range(65, 72):
        measures.append((f"m{i}", [
            (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
        ]))

    # m72: Clarinet echoes faintly — D4 (low, written, concert C4) to E5
    measures.append(("m72", [
        ("D", 4, DOT_EIGHTH, "eighth", True, None, {"voice": "1", "tenuto": True, "slur_start": True}),
        ("E", 4, SIXTEENTH, "16th", False, None, {"voice": "1"}),
        ("G", 4, EIGHTH, "eighth", False, None, {"voice": "1"}),
        ("E", 5, DOT_QUARTER, "quarter", True, None, {"voice": "1", "tenuto": True, "slur_stop": True}),
    ]))

    # m73: rest
    measures.append(("m73", [
        (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
    ]))

    # m74: one last sustained sigh — D5 dotted half (full measure, 3.0 QL)
    measures.append(("m74", [
        ("D", 5, DOT_HALF, "half", True, None, {"voice": "1", "tenuto": True, "fermata": True}),
    ]))

    # m75-80: tacet to end
    for i in range(75, 81):
        measures.append((f"m{i}", [
            (None, None, DOT_HALF, "half", True, None, {"voice": "1"}),
        ]))

    return measures


# ============================================================
# DIRECTIONS (dynamics, expressions, wedges)
# ============================================================

def get_piano_directions():
    """Return dict of measure_number -> list of direction specs to add BEFORE notes."""
    return {
        1: [
            {"text": "Andantino pastorale", "placement": "above",
             "words_attrs": {"font-style": "italic", "font-size": "12"},
             "metronome_beat": "quarter", "metronome_dot": True,
             "metronome_bpm": 72, "tempo": 108},
            {"text": "dolce", "placement": "above",
             "words_attrs": {"font-style": "italic"}},
            {"dynamic": "pp"},
        ],
        5: [{"wedge_type": "crescendo"}],
        8: [{"wedge_type": "stop"}, {"dynamic": "mp"}],
        13: [{"wedge_type": "diminuendo"}],
        16: [{"wedge_type": "stop"}, {"dynamic": "pp"}],
        17: [{"dynamic": "mp"}],
        25: [{"wedge_type": "crescendo"}],
        28: [{"wedge_type": "stop"}],
        29: [
            {"text": "con moto", "placement": "above",
             "words_attrs": {"font-style": "italic", "font-size": "12"},
             "metronome_beat": "quarter", "metronome_dot": True,
             "metronome_bpm": 76, "tempo": 114},
            {"dynamic": "mp"},
        ],
        33: [{"wedge_type": "crescendo"}],
        36: [{"wedge_type": "stop"}, {"dynamic": "mf"}],
        37: [{"wedge_type": "diminuendo"}],
        40: [{"wedge_type": "stop"}, {"dynamic": "mp"}],
        41: [{"wedge_type": "crescendo"}],
        44: [{"wedge_type": "stop"}, {"dynamic": "mf"}],
        49: [
            {"text": "Largamente", "placement": "above",
             "words_attrs": {"font-style": "italic", "font-size": "12"},
             "metronome_beat": "quarter", "metronome_dot": True,
             "metronome_bpm": 80, "tempo": 120},
            {"dynamic": "mf"},
        ],
        53: [{"wedge_type": "crescendo"}],
        56: [{"wedge_type": "stop"}, {"dynamic": "f"}],
        57: [{"wedge_type": "diminuendo"}],
        60: [{"wedge_type": "stop"}, {"dynamic": "mf"}],
        61: [{"wedge_type": "crescendo"}],
        63: [{"wedge_type": "stop"}, {"dynamic": "f"}],
        64: [{"wedge_type": "diminuendo"}],
        65: [
            {"wedge_type": "stop"},
            {"text": "come un ricordo", "placement": "above",
             "words_attrs": {"font-style": "italic", "font-size": "12"},
             "metronome_beat": "quarter", "metronome_dot": True,
             "metronome_bpm": 69, "tempo": 104},
            {"dynamic": "pp"},
        ],
        72: [{"text": "la sua melodia", "placement": "above",
              "words_attrs": {"font-style": "italic"}}],
        77: [{"text": "morendo", "placement": "above",
              "words_attrs": {"font-style": "italic"}},
             {"metronome_beat": "quarter", "metronome_dot": True,
              "metronome_bpm": 63, "tempo": 95, "placement": "above"}],
        79: [{"text": "rit.", "placement": "above",
              "words_attrs": {"font-style": "italic"}}],
    }


def get_clarinet_directions():
    """Return dict of measure_number -> list of direction specs."""
    return {
        17: [
            {"text": "espressivo", "placement": "above",
             "words_attrs": {"font-style": "italic"}},
            {"dynamic": "mp"},
        ],
        21: [{"wedge_type": "crescendo"}],
        24: [{"wedge_type": "stop"}],
        29: [{"dynamic": "mp"}],
        33: [{"wedge_type": "crescendo"}],
        35: [{"wedge_type": "stop"}, {"dynamic": "mf"}],
        37: [{"wedge_type": "diminuendo"}],
        40: [{"wedge_type": "stop"}, {"dynamic": "mp"}],
        42: [{"wedge_type": "crescendo"}],
        46: [{"wedge_type": "stop"}, {"dynamic": "mf"}],
        49: [{"dynamic": "mf"}],
        53: [{"wedge_type": "crescendo"}],
        55: [{"wedge_type": "stop"}, {"dynamic": "f"}],
        57: [{"wedge_type": "diminuendo"}],
        60: [{"wedge_type": "stop"}, {"dynamic": "mf"}],
        61: [{"wedge_type": "crescendo"}],
        63: [{"wedge_type": "stop"}, {"dynamic": "f"}],
        64: [{"wedge_type": "diminuendo"}],
        72: [{"wedge_type": "stop"}, {"dynamic": "pp"}],
        74: [{"dynamic": "ppp"}],
    }


# ============================================================
# BUILD THE FULL SCORE
# ============================================================

def build_score():
    root = ET.Element("score-partwise")
    root.set("version", "4.0")

    # Work title
    work = ET.SubElement(root, "work")
    ET.SubElement(work, "work-title").text = "Matin de Boulangerie"

    # Identification
    ident = ET.SubElement(root, "identification")
    creator = ET.SubElement(ident, "creator")
    creator.set("type", "composer")
    creator.text = "Claude"

    # Part list
    part_list = ET.SubElement(root, "part-list")

    # Clarinet
    sp1 = ET.SubElement(part_list, "score-part")
    sp1.set("id", "P1")
    ET.SubElement(sp1, "part-name").text = "Clarinet in Bb"
    si1 = ET.SubElement(sp1, "score-instrument")
    si1.set("id", "P1-I1")
    ET.SubElement(si1, "instrument-name").text = "Clarinet in Bb"
    mp1 = ET.SubElement(sp1, "midi-instrument")
    mp1.set("id", "P1-I1")
    ET.SubElement(mp1, "midi-channel").text = "1"
    ET.SubElement(mp1, "midi-program").text = "72"

    # Piano
    sp2 = ET.SubElement(part_list, "score-part")
    sp2.set("id", "P2")
    ET.SubElement(sp2, "part-name").text = "Piano"
    si2 = ET.SubElement(sp2, "score-instrument")
    si2.set("id", "P2-I1")
    ET.SubElement(si2, "instrument-name").text = "Piano"
    mp2 = ET.SubElement(sp2, "midi-instrument")
    mp2.set("id", "P2-I1")
    ET.SubElement(mp2, "midi-channel").text = "2"
    ET.SubElement(mp2, "midi-program").text = "1"

    # ---- Clarinet Part ----
    clarinet_part = ET.SubElement(root, "part")
    clarinet_part.set("id", "P1")

    clar_measures = build_clarinet_measures()
    clar_dirs = get_clarinet_directions()

    for mnum, (label, notes_data) in enumerate(clar_measures, 1):
        measure = ET.SubElement(clarinet_part, "measure")
        measure.set("number", str(mnum))

        # Attributes on first measure
        if mnum == 1:
            attr = make_attributes(
                divisions=DIV, fifths=-1, beats="6", beat_type="8",
                clef_sign="G", clef_line=2,
                transpose_diatonic=-1, transpose_chromatic=-2
            )
            measure.append(attr)

        # Key change at m49 (Ab major)
        if mnum == 49:
            attr = ET.SubElement(measure, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-4"

        # Key change back at m65 (F major)
        if mnum == 65:
            attr = ET.SubElement(measure, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-1"

        # Directions
        if mnum in clar_dirs:
            for d in clar_dirs[mnum]:
                add_direction(measure, **d)

        # Notes
        for item in notes_data:
            if item[0] == "backup":
                backup = ET.SubElement(measure, "backup")
                ET.SubElement(backup, "duration").text = str(item[1])
                continue

            step, octave, dur, ntype, dot, alter, kwargs = item
            is_rest = step is None
            note = make_note(
                step, octave, dur, ntype, dot=dot, rest=is_rest,
                alter=alter, **kwargs
            )
            measure.append(note)

    # ---- Piano Part ----
    piano_part = ET.SubElement(root, "part")
    piano_part.set("id", "P2")

    piano_measures = build_piano_measures()
    piano_dirs = get_piano_directions()

    for mnum, (label, notes_data) in enumerate(piano_measures, 1):
        measure = ET.SubElement(piano_part, "measure")
        measure.set("number", str(mnum))

        # Attributes on first measure
        if mnum == 1:
            attr = make_attributes(
                divisions=DIV, fifths=-1, beats="6", beat_type="8",
                clef_sign="G", clef_line=2, staves=2
            )
            measure.append(attr)

        # Key change at m49 (Ab major)
        if mnum == 49:
            attr = ET.SubElement(measure, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-4"

        # Key change back at m65 (F major)
        if mnum == 65:
            attr = ET.SubElement(measure, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-1"

        # Directions
        if mnum in piano_dirs:
            for d in piano_dirs[mnum]:
                add_direction(measure, **d)

        # Notes
        for item in notes_data:
            if item[0] == "backup":
                backup = ET.SubElement(measure, "backup")
                ET.SubElement(backup, "duration").text = str(item[1])
                continue

            step, octave, dur, ntype, dot, alter, kwargs = item
            is_rest = step is None
            note = make_note(
                step, octave, dur, ntype, dot=dot, rest=is_rest,
                alter=alter, **kwargs
            )
            measure.append(note)

    return root


def prettify(elem):
    """Pretty-print XML with proper declaration."""
    rough = ET.tostring(elem, encoding="unicode")
    parsed = minidom.parseString(rough)
    lines = parsed.toprettyxml(indent="  ", encoding=None)
    # Remove extra blank lines
    cleaned = "\n".join(line for line in lines.split("\n") if line.strip())
    return cleaned


def main():
    root = build_score()
    xml_str = prettify(root)

    # Add DOCTYPE
    header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    header += '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">\n'

    # Remove the auto-generated xml declaration from prettify
    if xml_str.startswith("<?xml"):
        xml_str = xml_str[xml_str.index("?>") + 2:].lstrip("\n")

    output = header + xml_str

    outpath = "/home/khaled/musiclaude/experiment/007/track_03/score.musicxml"
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Written to {outpath}")
    print(f"Total measures: 80 per part")


if __name__ == "__main__":
    main()
