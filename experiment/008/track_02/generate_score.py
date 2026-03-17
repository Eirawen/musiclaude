#!/usr/bin/env python3
"""Generate Matin de Boulangerie MusicXML score programmatically."""

import xml.etree.ElementTree as ET
from xml.dom import minidom

# Constants
DIVISIONS = 4  # per quarter note
# In 6/8: dotted quarter = 6 divisions, full measure = 12 divisions
MEASURE_DURATION = 12  # 6/8 = two dotted quarters = 12 divisions

def make_note(pitch_step, pitch_octave, duration, note_type, dot=False, rest=False,
              chord=False, alter=0, tie_start=False, tie_stop=False, staff=None,
              voice=None, stem=None, accidental=None, backup=False):
    """Create a note element."""
    note_el = ET.Element("note")
    if chord:
        ET.SubElement(note_el, "chord")
    if rest:
        ET.SubElement(note_el, "rest")
    else:
        pitch = ET.SubElement(note_el, "pitch")
        ET.SubElement(pitch, "step").text = pitch_step
        if alter != 0:
            ET.SubElement(pitch, "alter").text = str(alter)
        ET.SubElement(pitch, "octave").text = str(pitch_octave)
    ET.SubElement(note_el, "duration").text = str(duration)
    if tie_stop:
        tie = ET.SubElement(note_el, "tie")
        tie.set("type", "stop")
    if tie_start:
        tie = ET.SubElement(note_el, "tie")
        tie.set("type", "start")
    if voice:
        ET.SubElement(note_el, "voice").text = str(voice)
    ET.SubElement(note_el, "type").text = note_type
    if dot:
        ET.SubElement(note_el, "dot")
    if stem:
        ET.SubElement(note_el, "stem").text = stem
    if staff:
        ET.SubElement(note_el, "staff").text = str(staff)
    if accidental:
        ET.SubElement(note_el, "accidental").text = accidental
    notations = None
    if tie_start or tie_stop:
        notations = ET.SubElement(note_el, "notations")
        if tie_stop:
            tied = ET.SubElement(notations, "tied")
            tied.set("type", "stop")
        if tie_start:
            tied = ET.SubElement(notations, "tied")
            tied.set("type", "start")
    return note_el

def add_direction(measure, text=None, dynamic=None, tempo=None, wedge=None,
                  placement="above", staff=None, words_attr=None):
    """Add a direction element to a measure."""
    direction = ET.SubElement(measure, "direction")
    direction.set("placement", placement)
    dt = ET.SubElement(direction, "direction-type")
    if text:
        words = ET.SubElement(dt, "words")
        if words_attr:
            for k, v in words_attr.items():
                words.set(k, v)
        words.text = text
    if dynamic:
        dynamics = ET.SubElement(dt, "dynamics")
        ET.SubElement(dynamics, dynamic)
    if wedge:
        w = ET.SubElement(dt, "wedge")
        w.set("type", wedge)
    if tempo:
        sound = ET.SubElement(direction, "sound")
        # tempo in quarter notes per minute; dotted-quarter=72 means quarter=108
        sound.set("tempo", str(tempo))
    if staff:
        ET.SubElement(direction, "staff").text = str(staff)

def add_backup(measure, duration):
    backup = ET.SubElement(measure, "backup")
    ET.SubElement(backup, "duration").text = str(duration)

def add_forward(measure, duration, voice=None, staff=None):
    fwd = ET.SubElement(measure, "forward")
    ET.SubElement(fwd, "duration").text = str(duration)
    if voice:
        ET.SubElement(fwd, "voice").text = str(voice)
    if staff:
        ET.SubElement(fwd, "staff").text = str(staff)

def add_attributes(measure, divisions=None, key_fifths=None, key_mode=None,
                   time_beats=None, time_type=None, clef_sign=None, clef_line=None,
                   clef_sign2=None, clef_line2=None, staves=None, clef_number=None):
    attr = ET.SubElement(measure, "attributes")
    if divisions is not None:
        ET.SubElement(attr, "divisions").text = str(divisions)
    if key_fifths is not None:
        key = ET.SubElement(attr, "key")
        ET.SubElement(key, "fifths").text = str(key_fifths)
        if key_mode:
            ET.SubElement(key, "mode").text = key_mode
    if time_beats is not None:
        time = ET.SubElement(attr, "time")
        ET.SubElement(time, "beats").text = str(time_beats)
        ET.SubElement(time, "beat-type").text = str(time_type)
    if staves is not None:
        ET.SubElement(attr, "staves").text = str(staves)
    if clef_sign:
        clef = ET.SubElement(attr, "clef")
        if clef_number:
            clef.set("number", str(clef_number))
        else:
            clef.set("number", "1")
        ET.SubElement(clef, "sign").text = clef_sign
        ET.SubElement(clef, "line").text = str(clef_line)
    if clef_sign2:
        clef2 = ET.SubElement(attr, "clef")
        clef2.set("number", "2")
        ET.SubElement(clef2, "sign").text = clef_sign2
        ET.SubElement(clef2, "line").text = str(clef_line2)

# ============================================================
# PIANO PART: note/chord helpers for concise writing
# ============================================================

def piano_measure_arpeggiate(measure, bass_notes, treble_notes, m_num):
    """Write a standard 6/8 arpeggiated accompaniment pattern.
    bass_notes: list of (step, octave, alter) for beats 1,2 of bass
    treble_notes: list of (step, octave, alter) for 6 eighth notes in treble
    """
    # Voice 1 = treble (staff 1), Voice 2 = bass (staff 2)
    # Treble: 6 eighth notes
    for i, (s, o, a) in enumerate(treble_notes):
        n = make_note(s, o, 2, "eighth", voice="1", staff=1, stem="up", alter=a)
        measure.append(n)

    add_backup(measure, 12)

    # Bass: typically dotted-quarter + dotted-quarter or similar
    for i, (s, o, a, dur, ntype, dot) in enumerate(bass_notes):
        n = make_note(s, o, dur, ntype, dot=dot, voice="2", staff=2, stem="down", alter=a)
        measure.append(n)


def piano_rh_note(s, o, dur, ntype, dot=False, alter=0, chord=False,
                  tie_start=False, tie_stop=False, acc=None):
    return make_note(s, o, dur, ntype, dot=dot, voice="1", staff=1,
                     stem="up", alter=alter, chord=chord,
                     tie_start=tie_start, tie_stop=tie_stop, accidental=acc)

def piano_lh_note(s, o, dur, ntype, dot=False, alter=0, chord=False,
                  tie_start=False, tie_stop=False, acc=None):
    return make_note(s, o, dur, ntype, dot=dot, voice="2", staff=2,
                     stem="down", alter=alter, chord=chord,
                     tie_start=tie_start, tie_stop=tie_stop, accidental=acc)

def cl_note(s, o, dur, ntype, dot=False, alter=0, chord=False,
            tie_start=False, tie_stop=False, rest=False, acc=None):
    return make_note(s, o, dur, ntype, dot=dot, voice="1", alter=alter,
                     chord=chord, tie_start=tie_start, tie_stop=tie_stop,
                     rest=rest, accidental=acc)

# ============================================================
# BUILD SCORE
# ============================================================

def build_score():
    score = ET.Element("score-partwise")
    score.set("version", "4.0")

    # Work
    work = ET.SubElement(score, "work")
    ET.SubElement(work, "work-title").text = "Matin de Boulangerie"

    # Identification
    ident = ET.SubElement(score, "identification")
    creator = ET.SubElement(ident, "creator")
    creator.set("type", "composer")
    creator.text = "Claude"

    # Part list
    part_list = ET.SubElement(score, "part-list")

    # Clarinet
    sp1 = ET.SubElement(part_list, "score-part")
    sp1.set("id", "P1")
    ET.SubElement(sp1, "part-name").text = "Clarinet in Bb"
    ET.SubElement(sp1, "part-abbreviation").text = "Cl."
    si1 = ET.SubElement(sp1, "score-instrument")
    si1.set("id", "P1-I1")
    ET.SubElement(si1, "instrument-name").text = "Clarinet in Bb"
    transpose1 = ET.SubElement(sp1, "transpose")
    ET.SubElement(transpose1, "diatonic").text = "-1"
    ET.SubElement(transpose1, "chromatic").text = "-2"

    # Piano
    sp2 = ET.SubElement(part_list, "score-part")
    sp2.set("id", "P2")
    ET.SubElement(sp2, "part-name").text = "Piano"
    ET.SubElement(sp2, "part-abbreviation").text = "Pno."

    # ============================================================
    # CLARINET PART (P1) — written in G major (1 sharp)
    # Sounding: whole step lower. Written D4-B5 = sounding C4-A5
    # ============================================================
    p1 = ET.SubElement(score, "part")
    p1.set("id", "P1")

    # --- Section I: mm. 1-16, Clarinet rests ---
    for m in range(1, 17):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m))
        if m == 1:
            add_attributes(meas, divisions=4, key_fifths=1, key_mode="major",
                          time_beats=6, time_type=8, clef_sign="G", clef_line=2,
                          clef_number=1)
            # Tempo marking
            add_direction(meas, text="Dolce, ♩.= 72", tempo=108)
        # Full measure rest
        r = make_note(None, None, 12, "whole", rest=True, voice="1")
        meas.append(r)

    # --- Section II: mm. 17-28, Clarinet enters ---
    # Primary motif: ascending stepwise G4-A4-B4-C5-D5 (written)
    section2_cl = {
        17: [("G", 4, 6, "quarter", True, 0), ("A", 4, 4, "quarter", False, 0), ("B", 4, 2, "eighth", False, 0)],
        18: [("C", 5, 6, "quarter", True, 0), ("D", 5, 4, "quarter", False, 0), ("C", 5, 2, "eighth", False, 0)],
        19: [("B", 4, 4, "quarter", False, 0), ("A", 4, 4, "quarter", False, 0), ("G", 4, 4, "quarter", False, 0)],
        20: [("A", 4, 12, "half", True, 0)],  # dotted half = suspension
        21: [("B", 4, 6, "quarter", True, 0), ("C", 5, 4, "quarter", False, 0), ("D", 5, 2, "eighth", False, 0)],
        22: [("E", 5, 6, "quarter", True, 0), ("D", 5, 4, "quarter", False, 0), ("C", 5, 2, "eighth", False, 0)],
        23: [("B", 4, 4, "quarter", False, 0), ("A", 4, 2, "eighth", False, 0), ("G", 4, 4, "quarter", False, 0), ("A", 4, 2, "eighth", False, 0)],
        24: [("B", 4, 12, "half", True, 0)],
        25: [("A", 4, 6, "quarter", True, 0), ("B", 4, 4, "quarter", False, 0), ("C", 5, 2, "eighth", False, 0)],
        26: [("D", 5, 6, "quarter", True, 0), ("C", 5, 6, "quarter", True, 0)],
        27: [("B", 4, 4, "quarter", False, 0), ("A", 4, 4, "quarter", False, 0), ("G", 4, 4, "quarter", False, 0)],
        28: [("A", 4, 8, "half", False, 0), ("G", 4, 4, "quarter", False, 0)],
    }

    for m in range(17, 29):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m))
        if m == 17:
            add_direction(meas, text="espressivo")
            add_direction(meas, dynamic="mp")
        notes = section2_cl.get(m, [])
        for s, o, dur, ntype, dot, alt in notes:
            n = cl_note(s, o, dur, ntype, dot=dot, alter=alt)
            meas.append(n)

    # --- Section III: mm. 29-48, Conversation ---
    section3_cl = {
        29: [("G", 4, 6, "quarter", True, 0), ("A", 4, 2, "eighth", False, 0), ("B", 4, 2, "eighth", False, 0), ("C", 5, 2, "eighth", False, 0)],
        30: [("D", 5, 6, "quarter", True, 0), ("C", 5, 2, "eighth", False, 0), ("B", 4, 2, "eighth", False, 0), ("A", 4, 2, "eighth", False, 0)],
        31: [("G", 4, 4, "quarter", False, 0), ("E", 4, 4, "quarter", False, 0), ("D", 4, 4, "quarter", False, 0)],
        32: [("E", 4, 12, "half", True, 0)],
        33: [("rest", 0, 6, "quarter", True, 0), ("A", 4, 2, "eighth", False, 0), ("B", 4, 2, "eighth", False, 0), ("C", 5, 2, "eighth", False, 0)],
        34: [("D", 5, 4, "quarter", False, 0), ("E", 5, 4, "quarter", False, 0), ("D", 5, 2, "eighth", False, 0), ("C", 5, 2, "eighth", False, 0)],
        35: [("B", 4, 6, "quarter", True, 0), ("A", 4, 6, "quarter", True, 0)],
        36: [("G", 4, 8, "half", False, 0), ("rest", 0, 4, "quarter", False, 0)],
        # D minor excursion
        37: [("A", 4, 6, "quarter", True, 0), ("B", 4, 2, "eighth", False, -1), ("C", 5, 2, "eighth", False, 0), ("D", 5, 2, "eighth", False, 0)],
        38: [("E", 5, 4, "quarter", False, 0), ("D", 5, 4, "quarter", False, 0), ("C", 5, 2, "eighth", False, 0), ("B", 4, 2, "eighth", False, -1)],
        39: [("A", 4, 6, "quarter", True, 0), ("G", 4, 2, "eighth", False, 0), ("A", 4, 2, "eighth", False, 0), ("B", 4, 2, "eighth", False, -1)],
        40: [("A", 4, 12, "half", True, 0)],
        41: [("rest", 0, 6, "quarter", True, 0), ("G", 4, 2, "eighth", False, 0), ("A", 4, 2, "eighth", False, 0), ("B", 4, 2, "eighth", False, 0)],
        42: [("C", 5, 6, "quarter", True, 0), ("D", 5, 4, "quarter", False, 0), ("E", 5, 2, "eighth", False, 0)],
        43: [("F", 5, 4, "quarter", False, 0, True), ("E", 5, 4, "quarter", False, 0), ("D", 5, 4, "quarter", False, 0)],
        44: [("C", 5, 6, "quarter", True, 0), ("B", 4, 6, "quarter", True, 0)],
        45: [("A", 4, 4, "quarter", False, 0), ("B", 4, 4, "quarter", False, 0), ("C", 5, 4, "quarter", False, 0)],
        46: [("D", 5, 6, "quarter", True, 0), ("E", 5, 2, "eighth", False, 0), ("F", 5, 2, "eighth", False, 0, True), ("E", 5, 2, "eighth", False, 0)],
        47: [("D", 5, 4, "quarter", False, 0), ("C", 5, 4, "quarter", False, 0), ("B", 4, 2, "eighth", False, 0), ("A", 4, 2, "eighth", False, 0)],
        48: [("G", 4, 12, "half", True, 0)],
    }

    for m in range(29, 49):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m))
        if m == 29:
            add_direction(meas, text="con moto, ♩.= 76", tempo=114)
            add_direction(meas, dynamic="mf")
        if m == 37:
            add_direction(meas, dynamic="mp")
            add_direction(meas, text="poco dim.")
        if m == 41:
            add_direction(meas, dynamic="mf")
        if m == 45:
            add_direction(meas, wedge="crescendo")
        if m == 48:
            add_direction(meas, wedge="stop")

        notes_data = section3_cl.get(m, [])
        for item in notes_data:
            if len(item) == 6:
                s, o, dur, ntype, dot, alt = item
                is_sharp = False
            else:
                s, o, dur, ntype, dot, alt, is_sharp = item
            if s == "rest":
                n = cl_note(s, o, dur, ntype, dot=dot, rest=True)
            else:
                acc = None
                if alt == -1:
                    acc = "natural"  # Bb (natural in context of G major with F#)
                elif is_sharp if len(item) == 7 else False:
                    acc = "sharp"
                n = cl_note(s, o, dur, ntype, dot=dot, alter=alt, acc=acc)
            meas.append(n)

    # --- Section IV: mm. 49-64, Walking Home (Ab major) ---
    # Key change: Ab major has 4 flats. For Bb clarinet, written key = Bb major (2 flats)
    section4_cl = {
        49: [("C", 5, 6, "quarter", True, 0), ("D", 5, 4, "quarter", False, 0), ("E", 5, 2, "eighth", False, -1)],
        50: [("F", 5, 6, "quarter", True, 0), ("E", 5, 4, "quarter", False, -1), ("D", 5, 2, "eighth", False, 0)],
        51: [("C", 5, 4, "quarter", False, 0), ("B", 4, 4, "quarter", False, -1), ("C", 5, 4, "quarter", False, 0)],
        52: [("D", 5, 12, "half", True, 0)],
        53: [("E", 5, 6, "quarter", True, -1), ("F", 5, 4, "quarter", False, 0), ("G", 5, 2, "eighth", False, 0)],
        54: [("A", 5, 4, "quarter", False, -1), ("G", 5, 4, "quarter", False, 0), ("F", 5, 2, "eighth", False, 0), ("E", 5, 2, "eighth", False, -1)],
        55: [("F", 5, 6, "quarter", True, 0), ("E", 5, 2, "eighth", False, -1), ("D", 5, 2, "eighth", False, 0), ("C", 5, 2, "eighth", False, 0)],
        56: [("D", 5, 8, "half", False, 0), ("C", 5, 4, "quarter", False, 0)],
        57: [("E", 5, 6, "quarter", True, -1), ("F", 5, 6, "quarter", True, 0)],
        58: [("G", 5, 4, "quarter", False, 0), ("A", 5, 4, "quarter", False, -1), ("B", 5, 2, "eighth", False, -1), ("A", 5, 2, "eighth", False, -1)],
        59: [("G", 5, 6, "quarter", True, 0), ("F", 5, 4, "quarter", False, 0), ("E", 5, 2, "eighth", False, -1)],
        60: [("F", 5, 12, "half", True, 0)],
        61: [("E", 5, 6, "quarter", True, -1), ("D", 5, 4, "quarter", False, 0), ("C", 5, 2, "eighth", False, 0)],
        62: [("D", 5, 6, "quarter", True, 0), ("C", 5, 4, "quarter", False, 0), ("B", 4, 2, "eighth", False, 0)],
        63: [("C", 5, 4, "quarter", False, 0), ("D", 5, 4, "quarter", False, 0), ("E", 5, 4, "quarter", False, 0)],
        64: [("D", 5, 12, "half", True, 0)],
    }

    for m in range(49, 65):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m))
        if m == 49:
            # Key change to Bb major written (= Ab major sounding)
            attr = ET.SubElement(meas, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-2"
            ET.SubElement(key, "mode").text = "major"
            add_direction(meas, text="Largamente, ♩.= 80", tempo=120)
            add_direction(meas, dynamic="f")
        if m == 49:
            add_direction(meas, wedge="crescendo")
        if m == 52:
            add_direction(meas, wedge="stop")
        if m == 53:
            add_direction(meas, wedge="crescendo")
        if m == 56:
            add_direction(meas, wedge="stop")
        if m == 57:
            add_direction(meas, wedge="crescendo")
        if m == 60:
            add_direction(meas, wedge="stop")
            add_direction(meas, dynamic="ff")
        if m == 61:
            add_direction(meas, wedge="diminuendo")
        if m == 64:
            add_direction(meas, wedge="stop")

        notes_data = section4_cl.get(m, [])
        for s, o, dur, ntype, dot, alt in notes_data:
            acc = None
            if alt == -1:
                acc = "flat"
            n = cl_note(s, o, dur, ntype, dot=dot, alter=alt, acc=acc)
            meas.append(n)

    # --- Section V: mm. 65-80, Clarinet rests (mostly), brief appearance at m.72-74 ---
    for m in range(65, 81):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m))
        if m == 65:
            # Return to G major written (F major sounding)
            attr = ET.SubElement(meas, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "1"
            ET.SubElement(key, "mode").text = "major"
            add_direction(meas, text="Come un ricordo, ♩.= 69", tempo=104)
            add_direction(meas, dynamic="pp")
        if m == 80:
            # Final barline
            barline = ET.SubElement(meas, "barline")
            barline.set("location", "right")
            ET.SubElement(barline, "bar-style").text = "light-heavy"
        # Rests for clarinet in section V
        r = make_note(None, None, 12, "whole", rest=True, voice="1")
        meas.append(r)

    # ============================================================
    # PIANO PART (P2) — concert pitch, F major (1 flat)
    # ============================================================
    p2 = ET.SubElement(score, "part")
    p2.set("id", "P2")

    # Helper: write a measure with RH and LH content
    def write_piano_measure(meas_num, rh_notes, lh_notes, attrs=None,
                           directions_before=None, directions_mid=None):
        meas = ET.SubElement(p2, "measure")
        meas.set("number", str(meas_num))

        if attrs:
            attrs(meas)

        if directions_before:
            for d in directions_before:
                d(meas)

        # RH voice 1
        rh_dur = 0
        for item in rh_notes:
            meas.append(item)
            if item.find("chord") is None and item.find("rest") is not None:
                dur_el = item.find("duration")
                if dur_el is not None:
                    rh_dur += int(dur_el.text)
            elif item.find("chord") is None:
                dur_el = item.find("duration")
                if dur_el is not None:
                    rh_dur += int(dur_el.text)

        add_backup(meas, 12)

        # LH voice 2
        for item in lh_notes:
            meas.append(item)

        return meas

    # ---- SECTION I: mm 1-16, Piano solo, F major ----
    # Pastoral ostinato: lilting 6/8 arpeggio pattern

    # Standard ostinato pattern function
    def ost_rh(notes_list):
        """RH: 6 eighth notes for 6/8"""
        result = []
        for s, o, a in notes_list:
            result.append(piano_rh_note(s, o, 2, "eighth", alter=a))
        return result

    def ost_lh_dq(n1, n2):
        """LH: two dotted quarters"""
        s1, o1, a1 = n1
        s2, o2, a2 = n2
        return [
            piano_lh_note(s1, o1, 6, "quarter", dot=True, alter=a1),
            piano_lh_note(s2, o2, 6, "quarter", dot=True, alter=a2),
        ]

    # m.1: F major - F C A C A C
    m = ET.SubElement(p2, "measure")
    m.set("number", "1")
    add_attributes(m, divisions=4, key_fifths=-1, key_mode="major",
                  time_beats=6, time_type=8, clef_sign="G", clef_line=2,
                  clef_sign2="F", clef_line2=4, staves=2)
    add_direction(m, text="Dolce", staff="1")
    add_direction(m, dynamic="pp", staff="1")
    add_direction(m, tempo=108, text="♩.= 72", staff="1")
    # RH: F4 A4 C5 A4 C5 A4
    for s, o, a in [("F",4,0),("A",4,0),("C",5,0),("A",4,0),("C",5,0),("A",4,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    # LH: F3 dotted quarter, F2 dotted quarter
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("F", 2, 6, "quarter", dot=True))

    # m.2: Fmaj7
    m = ET.SubElement(p2, "measure")
    m.set("number", "2")
    for s, o, a in [("F",4,0),("A",4,0),("E",5,0),("A",4,0),("E",5,0),("C",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("C", 3, 6, "quarter", dot=True))

    # m.3: Bb/F
    m = ET.SubElement(p2, "measure")
    m.set("number", "3")
    for s, o, a in [("F",4,0),("B",4,-1),("D",5,0),("B",4,-1),("D",5,0),("B",4,-1)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("F", 2, 6, "quarter", dot=True))

    # m.4: Fadd9
    m = ET.SubElement(p2, "measure")
    m.set("number", "4")
    for s, o, a in [("F",4,0),("A",4,0),("G",4,0),("C",5,0),("A",4,0),("G",4,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("C", 3, 6, "quarter", dot=True))

    # m.5: F
    m = ET.SubElement(p2, "measure")
    m.set("number", "5")
    add_direction(m, wedge="crescendo", staff="1")
    for s, o, a in [("F",4,0),("A",4,0),("C",5,0),("A",4,0),("C",5,0),("F",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("F", 2, 6, "quarter", dot=True))

    # m.6: C/E
    m = ET.SubElement(p2, "measure")
    m.set("number", "6")
    for s, o, a in [("E",4,0),("G",4,0),("C",5,0),("G",4,0),("C",5,0),("E",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("E", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("C", 3, 6, "quarter", dot=True))

    # m.7: Dm7
    m = ET.SubElement(p2, "measure")
    m.set("number", "7")
    for s, o, a in [("D",4,0),("F",4,0),("A",4,0),("C",5,0),("A",4,0),("F",4,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("D", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("A", 2, 6, "quarter", dot=True))

    # m.8: Bbmaj7
    m = ET.SubElement(p2, "measure")
    m.set("number", "8")
    add_direction(m, wedge="stop", staff="1")
    add_direction(m, dynamic="mp", staff="1")
    for s, o, a in [("B",4,-1),("D",5,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("B", 2, 6, "quarter", dot=True, alter=-1))
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))

    # m.9: F
    m = ET.SubElement(p2, "measure")
    m.set("number", "9")
    for s, o, a in [("F",4,0),("A",4,0),("C",5,0),("A",4,0),("C",5,0),("A",4,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("C", 3, 6, "quarter", dot=True))

    # m.10: Fadd9
    m = ET.SubElement(p2, "measure")
    m.set("number", "10")
    for s, o, a in [("F",4,0),("G",4,0),("A",4,0),("C",5,0),("G",4,0),("A",4,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("C", 3, 6, "quarter", dot=True))

    # m.11: Bb
    m = ET.SubElement(p2, "measure")
    m.set("number", "11")
    for s, o, a in [("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1),("D",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("B", 2, 6, "quarter", dot=True, alter=-1))
    m.append(piano_lh_note("F", 3, 6, "quarter", dot=True))

    # m.12: Gm7
    m = ET.SubElement(p2, "measure")
    m.set("number", "12")
    for s, o, a in [("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("G", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("D", 3, 6, "quarter", dot=True))

    # m.13: Am7
    m = ET.SubElement(p2, "measure")
    m.set("number", "13")
    add_direction(m, wedge="crescendo", staff="1")
    for s, o, a in [("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("A", 2, 6, "quarter", dot=True))
    m.append(piano_lh_note("E", 3, 6, "quarter", dot=True))

    # m.14: Dm
    m = ET.SubElement(p2, "measure")
    m.set("number", "14")
    for s, o, a in [("D",4,0),("F",4,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("D", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("A", 2, 6, "quarter", dot=True))

    # m.15: Gm7
    m = ET.SubElement(p2, "measure")
    m.set("number", "15")
    for s, o, a in [("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("G", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("D", 3, 6, "quarter", dot=True))

    # m.16: C7sus4 -> C7
    m = ET.SubElement(p2, "measure")
    m.set("number", "16")
    add_direction(m, wedge="stop", staff="1")
    # C7sus4 first half
    for s, o, a in [("C",4,0),("F",4,0),("B",4,-1)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    # C7 second half
    for s, o, a in [("C",4,0),("E",4,0),("B",4,-1)]:
        m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
    add_backup(m, 12)
    m.append(piano_lh_note("C", 3, 6, "quarter", dot=True))
    m.append(piano_lh_note("G", 2, 6, "quarter", dot=True))

    # ---- SECTION II: mm 17-28, Clarinet enters ----
    sec2_piano = {
        17: (
            [("F",4,0),("A",4,0),("C",5,0),("G",4,0),("A",4,0),("C",5,0)],
            [("F",3,0), ("C",3,0)]
        ),
        18: (
            [("F",4,0),("A",4,0),("E",5,0),("A",4,0),("C",5,0),("E",5,0)],
            [("F",3,0), ("C",3,0)]
        ),
        19: (
            [("D",4,0),("F",4,0),("A",4,0),("G",4,0),("B",4,-1),("D",5,0)],
            [("D",3,0), ("G",3,0)]
        ),
        20: (
            [("B",4,-1),("D",5,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)],
            [("B",2,-1), ("F",3,0)]
        ),
        21: (
            [("A",4,0),("C",5,0),("E",5,0),("C",5,0),("E",5,0),("G",5,0)],
            [("A",2,0), ("E",3,0)]
        ),
        22: (
            [("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)],
            [("G",3,0), ("D",3,0)]
        ),
        23: (
            [("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("G",4,0),("E",4,0)],
            [("C",3,0), ("G",2,0)]
        ),
        24: (
            [("F",4,0),("A",4,0),("C",5,0),("G",4,0),("A",4,0),("C",5,0)],
            [("F",3,0), ("C",3,0)]
        ),
        25: (
            [("F",4,0),("G",4,0),("A",4,0),("C",5,0),("A",4,0),("G",4,0)],
            [("F",3,0), ("C",3,0)]
        ),
        26: (
            [("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1),("D",5,0)],
            [("B",2,-1), ("F",3,0)]
        ),
        27: (
            [("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("G",4,0),("E",4,0)],
            [("C",3,0), ("G",2,0)]
        ),
        28: (
            [("F",4,0),("A",4,0),("C",5,0),("A",4,0),("F",4,0),("A",4,0)],
            [("F",3,0), ("C",3,0)]
        ),
    }

    for mn in range(17, 29):
        m = ET.SubElement(p2, "measure")
        m.set("number", str(mn))
        if mn == 17:
            add_direction(m, dynamic="mp", staff="1")
        rh_pat, lh_roots = sec2_piano[mn]
        for s, o, a in rh_pat:
            m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(piano_lh_note(s1, o1, 6, "quarter", dot=True, alter=a1))
        m.append(piano_lh_note(s2, o2, 6, "quarter", dot=True, alter=a2))

    # ---- SECTION III: mm 29-48, Conversation ----
    sec3_piano = {
        29: ([("F",4,0),("A",4,0),("C",5,0),("A",4,0),("C",5,0),("F",5,0)], [("F",3,0),("C",3,0)]),
        30: ([("E",4,0),("G",4,0),("C",5,0),("G",4,0),("C",5,0),("E",5,0)], [("C",3,0),("G",2,0)]),
        31: ([("D",4,0),("F",4,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)], [("D",3,0),("A",2,0)]),
        32: ([("B",4,-1),("D",5,0),("F",5,0),("A",4,0),("D",5,0),("F",5,0)], [("B",2,-1),("F",3,0)]),
        33: ([("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0),("C",5,0)], [("A",2,0),("E",3,0)]),
        34: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("A",4,0),("F",4,0)], [("D",3,0),("A",2,0)]),
        35: ([("G",4,0),("B",4,-1),("D",5,0),("B",4,-1),("D",5,0),("G",5,0)], [("G",3,0),("D",3,0)]),
        36: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("G",4,0),("E",4,0)], [("C",3,0),("G",2,0)]),
        # D minor excursion
        37: ([("D",4,0),("F",4,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)], [("D",3,0),("A",2,0)]),
        38: ([("G",4,0),("B",4,-1),("D",5,0),("B",4,-1),("D",5,0),("G",5,0)], [("G",3,0),("D",3,0)]),
        39: ([("A",4,0),("C",5,0),("E",5,0),("G",4,0, ),("C",5,0),("E",5,0)], [("A",2,0),("E",3,0)]),
        40: ([("D",4,0),("F",4,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)], [("D",3,0),("A",2,0)]),
        41: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("A",4,0),("F",4,0)], [("D",3,0),("A",2,0)]),
        42: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        43: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("E",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),
        44: ([("F",4,0),("A",4,0),("C",5,0),("A",4,0),("C",5,0),("F",5,0)], [("F",3,0),("C",3,0)]),
        45: ([("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1),("D",5,0)], [("B",2,-1),("F",3,0)]),
        46: ([("A",4,0),("C",5,0),("E",5,0),("C",5,0),("E",5,0),("A",5,0)], [("A",2,0),("E",3,0)]),
        47: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        48: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("G",4,0),("E",4,0)], [("C",3,0),("G",2,0)]),
    }

    for mn in range(29, 49):
        m = ET.SubElement(p2, "measure")
        m.set("number", str(mn))
        if mn == 29:
            add_direction(m, text="con moto", staff="1")
            add_direction(m, dynamic="mf", staff="1")
        if mn == 37:
            add_direction(m, dynamic="mp", staff="1")
        if mn == 41:
            add_direction(m, dynamic="mf", staff="1")
        if mn == 45:
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 48:
            add_direction(m, wedge="stop", staff="1")
        rh_pat, lh_roots = sec3_piano[mn]
        for s, o, a in rh_pat:
            m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(piano_lh_note(s1, o1, 6, "quarter", dot=True, alter=a1))
        m.append(piano_lh_note(s2, o2, 6, "quarter", dot=True, alter=a2))

    # ---- SECTION IV: mm 49-64, Walking Home, Ab major ----
    sec4_piano = {
        49: ([("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("E",5,-1),("A",5,-1)], [("A",3,-1),("E",3,-1)]),
        50: ([("A",4,-1),("C",5,0),("E",5,-1),("G",4,0),("C",5,0),("E",5,-1)], [("A",3,-1),("E",3,-1)]),
        51: ([("D",4,-1),("F",4,0),("A",4,-1),("F",4,0),("A",4,-1),("D",5,-1)], [("D",3,-1),("A",3,-1)]),
        52: ([("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("A",4,-1),("C",5,0)], [("A",2,-1),("E",3,-1)]),
        53: ([("B",4,-1),("D",5,-1),("F",5,0),("D",5,-1),("B",4,-1),("D",5,-1)], [("B",2,-1),("F",3,0)]),
        54: ([("E",4,-1),("G",4,0),("B",4,-1),("D",5,-1),("B",4,-1),("G",4,0)], [("E",3,-1),("B",2,-1)]),
        55: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),
        56: ([("F",4,0),("A",4,-1),("C",5,0),("A",4,-1),("F",4,0),("A",4,-1)], [("F",3,0),("C",3,0)]),
        57: ([("D",4,-1),("F",4,0),("A",4,-1),("C",5,0),("A",4,-1),("F",4,0)], [("D",3,-1),("A",2,-1)]),
        58: ([("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("E",5,-1),("A",5,-1)], [("A",3,-1),("E",3,-1)]),
        59: ([("B",4,-1),("D",5,-1),("F",5,0),("D",5,-1),("F",5,0),("B",5,-1)], [("B",2,-1),("F",3,0)]),
        60: ([("E",4,-1),("G",4,0),("B",4,-1),("D",5,0),("B",4,-1),("G",4,0)], [("E",3,-1),("B",2,-1)]),
        61: ([("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("E",5,-1),("A",5,-1)], [("A",3,-1),("E",3,-1)]),
        62: ([("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("A",4,-1)], [("F",3,0),("C",3,0)]),
        63: ([("D",4,-1),("F",4,0),("B",4,-1),("D",5,-1),("B",4,-1),("F",4,0)], [("D",3,-1),("B",2,-1)]),
        64: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("E",4,0),("G",4,0)], [("C",3,0),("G",2,0)]),
    }

    for mn in range(49, 65):
        m = ET.SubElement(p2, "measure")
        m.set("number", str(mn))
        if mn == 49:
            attr = ET.SubElement(m, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-4"
            ET.SubElement(key, "mode").text = "major"
            add_direction(m, text="Largamente", staff="1")
            add_direction(m, dynamic="f", staff="1")
        if mn == 53:
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 56:
            add_direction(m, wedge="stop", staff="1")
        if mn == 57:
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 60:
            add_direction(m, wedge="stop", staff="1")
            add_direction(m, dynamic="ff", staff="1")
        if mn == 61:
            add_direction(m, wedge="diminuendo", staff="1")
        if mn == 64:
            add_direction(m, wedge="stop", staff="1")
            add_direction(m, dynamic="mf", staff="1")

        rh_pat, lh_roots = sec4_piano[mn]
        for s, o, a in rh_pat:
            m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(piano_lh_note(s1, o1, 6, "quarter", dot=True, alter=a1))
        m.append(piano_lh_note(s2, o2, 6, "quarter", dot=True, alter=a2))

    # ---- SECTION V: mm 65-80, Alone Again, return to F major ----
    sec5_piano = {
        65: ([("F",4,0),("A",4,0),("C",5,0),("A",4,0),("C",5,0),("A",4,0)], [("F",3,0),("F",2,0)]),
        66: ([("F",4,0),("A",4,0),("E",5,0),("A",4,0),("E",5,0),("C",5,0)], [("F",3,0),("C",3,0)]),
        67: ([("F",4,0),("B",4,-1),("D",5,0),("B",4,-1),("D",5,0),("B",4,-1)], [("F",3,0),("F",2,0)]),
        68: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("G",4,0),("A",4,0)], [("F",3,0),("C",3,0)]),
        69: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("A",4,0),("F",4,0)], [("D",3,0),("A",2,0)]),
        70: ([("G",4,0),("B",4,0),("D",5,0),("F",5,0),("D",5,0),("B",4,0)], [("G",3,0),("D",3,0)]),  # G7/B natural
        71: ([("B",4,-1),("D",5,0),("F",5,0),("A",4,0),("D",5,0),("F",5,0)], [("B",2,-1),("F",3,0)]),
        # m.72: clarinet melody appears in piano RH (F-G-A-Bb-C ascending)
        72: ([("F",4,0),("G",4,0),("A",4,0),("B",4,-1),("C",5,0),("A",4,0)], [("A",2,0),("E",3,0)]),
        73: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("A",4,0),("G",4,0)], [("F",3,0),("C",3,0)]),
        74: ([("D",4,0),("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0)], [("D",3,0),("A",2,0)]),
        75: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        76: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("G",4,0),("E",4,0)], [("C",3,0),("G",2,0)]),
        77: ([("B",4,-1),("D",5,0),("F",5,0),("A",4,0),("D",5,0),("F",5,0)], [("B",2,-1),("F",3,0)]),
        78: ([("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0),("C",5,0)], [("A",2,0),("E",3,0)]),
        79: ([("G",4,0),("B",4,-1),("D",5,0),("A",4,0),("C",5,0),("E",5,0)], [("G",3,0),("C",3,0)]),
        # m.80: Fadd9 final chord — unresolved
        80: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("G",4,0),("A",4,0)], [("F",3,0),("F",2,0)]),
    }

    for mn in range(65, 81):
        m = ET.SubElement(p2, "measure")
        m.set("number", str(mn))
        if mn == 65:
            attr = ET.SubElement(m, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-1"
            ET.SubElement(key, "mode").text = "major"
            add_direction(m, text="Come un ricordo", staff="1")
            add_direction(m, dynamic="pp", staff="1")
        if mn == 72:
            add_direction(m, text="la melodia", staff="1",
                         words_attr={"font-style": "italic"})
        if mn == 77:
            add_direction(m, text="morendo", staff="1")
        if mn == 79:
            add_direction(m, text="rit.", staff="1")
        if mn == 80:
            barline = ET.SubElement(m, "barline")
            barline.set("location", "right")
            ET.SubElement(barline, "bar-style").text = "light-heavy"

        rh_pat, lh_roots = sec5_piano[mn]
        for s, o, a in rh_pat:
            m.append(piano_rh_note(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(piano_lh_note(s1, o1, 6, "quarter", dot=True, alter=a1))
        m.append(piano_lh_note(s2, o2, 6, "quarter", dot=True, alter=a2))

    return score


def write_musicxml(score, filepath):
    """Write score to MusicXML file with proper declaration."""
    rough = ET.tostring(score, encoding="unicode")
    dom = minidom.parseString(rough)

    # Build the output manually for proper XML declaration + DOCTYPE
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">')

    # Get the root element's serialization without the xml declaration
    root_str = dom.documentElement.toprettyxml(indent="  ")
    # Remove the extra xml declaration if minidom adds one
    if root_str.startswith("<?xml"):
        root_str = root_str.split("?>", 1)[1].lstrip("\n")

    lines.append(root_str)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Written to {filepath}")


if __name__ == "__main__":
    score = build_score()
    write_musicxml(score, "/home/khaled/musiclaude/experiment/008/track_02/score.musicxml")
    print("Done generating score.")
