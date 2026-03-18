#!/usr/bin/env python3
"""Generate Matin de Boulangerie MusicXML score v2 — addresses feedback:
- Add articulations (staccato, tenuto, accent, legato slurs)
- More rhythmic variety (16th notes, dotted eighths, ties)
- More extended chords (7ths, 9ths, sus4)
- Wider melodic range
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

DIVISIONS = 4

def make_note(pitch_step, pitch_octave, duration, note_type, dot=False, rest=False,
              chord=False, alter=0, tie_start=False, tie_stop=False, staff=None,
              voice=None, stem=None, accidental=None, articulation=None,
              slur_start=False, slur_stop=False):
    """Create a note element with optional articulation and slur."""
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
    # Notations: ties, articulations, slurs
    needs_notations = (tie_start or tie_stop or articulation or slur_start or slur_stop)
    if needs_notations:
        notations = ET.SubElement(note_el, "notations")
        if tie_stop:
            tied = ET.SubElement(notations, "tied")
            tied.set("type", "stop")
        if tie_start:
            tied = ET.SubElement(notations, "tied")
            tied.set("type", "start")
        if articulation:
            artic = ET.SubElement(notations, "articulations")
            ET.SubElement(artic, articulation)
        if slur_start:
            slur = ET.SubElement(notations, "slur")
            slur.set("type", "start")
        if slur_stop:
            slur = ET.SubElement(notations, "slur")
            slur.set("type", "stop")
    return note_el

def add_direction(measure, text=None, dynamic=None, tempo=None, wedge=None,
                  placement="above", staff=None, words_attr=None):
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
        sound.set("tempo", str(tempo))
    if staff:
        ET.SubElement(direction, "staff").text = str(staff)

def add_backup(measure, duration):
    backup = ET.SubElement(measure, "backup")
    ET.SubElement(backup, "duration").text = str(duration)

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

def rh(s, o, dur, ntype, dot=False, alter=0, chord=False, tie_start=False,
       tie_stop=False, acc=None, artic=None, slur_start=False, slur_stop=False):
    return make_note(s, o, dur, ntype, dot=dot, voice="1", staff=1,
                     stem="up", alter=alter, chord=chord,
                     tie_start=tie_start, tie_stop=tie_stop, accidental=acc,
                     articulation=artic, slur_start=slur_start, slur_stop=slur_stop)

def lh(s, o, dur, ntype, dot=False, alter=0, chord=False, tie_start=False,
       tie_stop=False, acc=None, artic=None, slur_start=False, slur_stop=False):
    return make_note(s, o, dur, ntype, dot=dot, voice="2", staff=2,
                     stem="down", alter=alter, chord=chord,
                     tie_start=tie_start, tie_stop=tie_stop, accidental=acc,
                     articulation=artic, slur_start=slur_start, slur_stop=slur_stop)

def cl(s, o, dur, ntype, dot=False, alter=0, rest=False, acc=None, artic=None,
       tie_start=False, tie_stop=False, slur_start=False, slur_stop=False):
    return make_note(s, o, dur, ntype, dot=dot, voice="1", alter=alter,
                     rest=rest, accidental=acc, articulation=artic,
                     tie_start=tie_start, tie_stop=tie_stop,
                     slur_start=slur_start, slur_stop=slur_stop)

def build_score():
    score = ET.Element("score-partwise")
    score.set("version", "4.0")

    work = ET.SubElement(score, "work")
    ET.SubElement(work, "work-title").text = "Matin de Boulangerie"

    ident = ET.SubElement(score, "identification")
    creator = ET.SubElement(ident, "creator")
    creator.set("type", "composer")
    creator.text = "Claude"

    part_list = ET.SubElement(score, "part-list")

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

    sp2 = ET.SubElement(part_list, "score-part")
    sp2.set("id", "P2")
    ET.SubElement(sp2, "part-name").text = "Piano"
    ET.SubElement(sp2, "part-abbreviation").text = "Pno."

    # ============================================================
    # CLARINET PART (P1) — written in G major (1 sharp)
    # Written D4-B5 = sounding C4-A5
    # v2: wider range, more rhythmic variety, articulations
    # ============================================================
    p1 = ET.SubElement(score, "part")
    p1.set("id", "P1")

    # --- Section I: mm. 1-16, Clarinet rests ---
    for m_num in range(1, 17):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 1:
            add_attributes(meas, divisions=4, key_fifths=1, key_mode="major",
                          time_beats=6, time_type=8, clef_sign="G", clef_line=2,
                          clef_number=1)
            add_direction(meas, text="Dolce, ♩.= 72", tempo=108)
        meas.append(make_note(None, None, 12, "whole", rest=True, voice="1"))

    # --- Section II: mm. 17-28, Clarinet enters ---
    # v2: slurs for legato phrasing, tenuto on long notes, wider range
    section2_cl = [
        # m17: primary motif, ascending stepwise with slur
        (17, [
            ("G", 4, 6, "quarter", True, 0, False, None, True, False),   # slur start
            ("A", 4, 3, "eighth", True, 0, False, None, False, False),   # dotted eighth
            ("B", 4, 1, "16th", False, 0, False, None, False, False),    # 16th
            ("C", 5, 2, "eighth", False, 0, False, None, False, True),   # slur stop
        ]),
        # m18
        (18, [
            ("D", 5, 6, "quarter", True, 0, False, "tenuto", True, False),
            ("C", 5, 4, "quarter", False, 0, False, None, False, False),
            ("B", 4, 2, "eighth", False, 0, False, None, False, True),
        ]),
        # m19
        (19, [
            ("A", 4, 4, "quarter", False, 0, False, None, True, False),
            ("G", 4, 4, "quarter", False, 0, False, None, False, False),
            ("F", 4, 2, "eighth", False, 0, False, None, False, False),  # F# written = E sounding, expanded range down
            ("G", 4, 2, "eighth", False, 0, False, None, False, True),
        ]),
        # m20: suspension
        (20, [
            ("A", 4, 12, "half", True, 0, False, "tenuto", False, False),
        ]),
        # m21
        (21, [
            ("B", 4, 3, "eighth", True, 0, False, None, True, False),
            ("C", 5, 1, "16th", False, 0, False, None, False, False),
            ("D", 5, 2, "eighth", False, 0, False, None, False, False),
            ("E", 5, 4, "quarter", False, 0, False, None, False, False),
            ("D", 5, 2, "eighth", False, 0, False, None, False, True),
        ]),
        # m22
        (22, [
            ("E", 5, 6, "quarter", True, 0, False, "tenuto", True, False),
            ("D", 5, 3, "eighth", True, 0, False, None, False, False),
            ("C", 5, 1, "16th", False, 0, False, None, False, False),
            ("B", 4, 2, "eighth", False, 0, False, None, False, True),
        ]),
        # m23
        (23, [
            ("A", 4, 4, "quarter", False, 0, False, None, True, False),
            ("G", 4, 2, "eighth", False, 0, False, None, False, False),
            ("F", 4, 4, "quarter", False, 0, False, None, False, False),  # F# written
            ("G", 4, 2, "eighth", False, 0, False, None, False, True),
        ]),
        # m24
        (24, [
            ("A", 4, 12, "half", True, 0, False, "tenuto", False, False),
        ]),
        # m25
        (25, [
            ("G", 4, 3, "eighth", True, 0, False, None, True, False),
            ("A", 4, 1, "16th", False, 0, False, None, False, False),
            ("B", 4, 2, "eighth", False, 0, False, None, False, False),
            ("C", 5, 4, "quarter", False, 0, False, None, False, False),
            ("D", 5, 2, "eighth", False, 0, False, None, False, True),
        ]),
        # m26
        (26, [
            ("E", 5, 6, "quarter", True, 0, False, "tenuto", False, False),
            ("D", 5, 6, "quarter", True, 0, False, None, False, False),
        ]),
        # m27
        (27, [
            ("C", 5, 4, "quarter", False, 0, False, None, True, False),
            ("B", 4, 4, "quarter", False, 0, False, None, False, False),
            ("A", 4, 4, "quarter", False, 0, False, None, False, True),
        ]),
        # m28
        (28, [
            ("G", 4, 8, "half", False, 0, False, "tenuto", False, False),
            ("F", 4, 4, "quarter", False, 0, False, None, False, False),  # F# written
        ]),
    ]

    for m_num, notes in section2_cl:
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 17:
            add_direction(meas, text="espressivo")
            add_direction(meas, dynamic="mp")
        for s, o, dur, ntype, dot, alt, is_rest, artic, sl_start, sl_stop in notes:
            if is_rest or s == "rest":
                meas.append(cl(s, o, dur, ntype, dot=dot, rest=True))
            else:
                meas.append(cl(s, o, dur, ntype, dot=dot, alter=alt, artic=artic,
                              slur_start=sl_start, slur_stop=sl_stop))

    # --- Section III: mm. 29-48, Conversation ---
    # v2: more varied rhythms, articulations, wider leaps at emotional moments
    section3_cl = [
        (29, [
            ("G", 4, 6, "quarter", True, 0, None, True, False),
            ("A", 4, 2, "eighth", False, 0, None, False, False),
            ("B", 4, 1, "16th", False, 0, None, False, False),
            ("C", 5, 1, "16th", False, 0, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (30, [
            ("E", 5, 6, "quarter", True, 0, "tenuto", True, False),
            ("D", 5, 2, "eighth", False, 0, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, False),
            ("B", 4, 2, "eighth", False, 0, None, False, True),
        ]),
        (31, [
            ("A", 4, 4, "quarter", False, 0, None, True, False),
            ("G", 4, 2, "eighth", False, 0, None, False, False),
            ("E", 4, 4, "quarter", False, 0, None, False, False),
            ("D", 4, 2, "eighth", False, 0, None, False, True),
        ]),
        (32, [
            ("E", 4, 12, "half", True, 0, "tenuto", False, False),
        ]),
        (33, [
            ("rest", 0, 6, "quarter", True, 0, None, False, False),
            ("A", 4, 2, "eighth", False, 0, None, True, False),
            ("B", 4, 1, "16th", False, 0, None, False, False),
            ("C", 5, 1, "16th", False, 0, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (34, [
            ("E", 5, 4, "quarter", False, 0, None, True, False),
            ("F", 5, 3, "eighth", True, 0, None, False, False),  # F#5 written, dotted eighth
            ("E", 5, 1, "16th", False, 0, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (35, [
            ("B", 4, 6, "quarter", True, 0, "tenuto", True, False),
            ("A", 4, 6, "quarter", True, 0, None, False, True),
        ]),
        (36, [
            ("G", 4, 8, "half", False, 0, None, False, False),
            ("rest", 0, 4, "quarter", False, 0, None, False, False),
        ]),
        # D minor excursion (m37-40)
        (37, [
            ("A", 4, 6, "quarter", True, 0, None, True, False),
            ("B", 4, 2, "eighth", False, -1, None, False, False),  # Bb written = natural in key
            ("C", 5, 2, "eighth", False, 0, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (38, [
            ("E", 5, 3, "eighth", True, 0, None, True, False),
            ("D", 5, 1, "16th", False, 0, None, False, False),
            ("C", 5, 4, "quarter", False, 0, None, False, False),
            ("B", 4, 2, "eighth", False, -1, None, False, False),
            ("A", 4, 2, "eighth", False, 0, None, False, True),
        ]),
        (39, [
            ("G", 4, 6, "quarter", True, 0, "tenuto", True, False),
            ("A", 4, 3, "eighth", True, 0, None, False, False),
            ("B", 4, 1, "16th", False, -1, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (40, [
            ("A", 4, 12, "half", True, 0, "tenuto", False, False),
        ]),
        (41, [
            ("rest", 0, 4, "quarter", False, 0, None, False, False),
            ("G", 4, 2, "eighth", False, 0, None, True, False),
            ("A", 4, 2, "eighth", False, 0, None, False, False),
            ("B", 4, 2, "eighth", False, 0, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (42, [
            ("D", 5, 6, "quarter", True, 0, None, True, False),
            ("E", 5, 4, "quarter", False, 0, None, False, False),
            ("F", 5, 2, "eighth", False, 0, None, False, True),  # F#5 written
        ]),
        (43, [
            ("G", 5, 4, "quarter", False, 0, "accent", False, False),  # High G5! wider range
            ("F", 5, 3, "eighth", True, 0, None, True, False),  # F#5
            ("E", 5, 1, "16th", False, 0, None, False, False),
            ("D", 5, 4, "quarter", False, 0, None, False, True),
        ]),
        (44, [
            ("C", 5, 6, "quarter", True, 0, "tenuto", False, False),
            ("B", 4, 6, "quarter", True, 0, None, False, False),
        ]),
        (45, [
            ("A", 4, 3, "eighth", True, 0, None, True, False),
            ("B", 4, 1, "16th", False, 0, None, False, False),
            ("C", 5, 4, "quarter", False, 0, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, False),
            ("E", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (46, [
            ("F", 5, 6, "quarter", True, 0, "tenuto", True, False),  # F#5
            ("E", 5, 2, "eighth", False, 0, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (47, [
            ("D", 5, 3, "eighth", True, 0, None, True, False),
            ("C", 5, 1, "16th", False, 0, None, False, False),
            ("B", 4, 4, "quarter", False, 0, None, False, False),
            ("A", 4, 2, "eighth", False, 0, None, False, False),
            ("G", 4, 2, "eighth", False, 0, None, False, True),
        ]),
        (48, [
            ("G", 4, 12, "half", True, 0, "tenuto", False, False),
        ]),
    ]

    for m_num, notes in section3_cl:
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 29:
            add_direction(meas, text="con moto, ♩.= 76", tempo=114)
            add_direction(meas, dynamic="mf")
        if m_num == 37:
            add_direction(meas, dynamic="mp")
            add_direction(meas, text="poco dim.")
        if m_num == 41:
            add_direction(meas, dynamic="mf")
        if m_num == 45:
            add_direction(meas, wedge="crescendo")
        if m_num == 48:
            add_direction(meas, wedge="stop")

        for item in notes:
            s, o, dur, ntype, dot, alt, artic, sl_start, sl_stop = item
            if s == "rest":
                meas.append(cl(s, o, dur, ntype, dot=dot, rest=True))
            else:
                acc = None
                if alt == -1:
                    acc = "natural"
                meas.append(cl(s, o, dur, ntype, dot=dot, alter=alt, acc=acc,
                              artic=artic, slur_start=sl_start, slur_stop=sl_stop))

    # --- Section IV: mm. 49-64, Walking Home (Ab major) ---
    # Clarinet written key: Bb major (2 flats). Wider range, more expressive.
    section4_cl = [
        (49, [
            ("C", 5, 6, "quarter", True, 0, None, True, False),
            ("D", 5, 3, "eighth", True, 0, None, False, False),
            ("E", 5, 1, "16th", False, -1, None, False, False),
            ("F", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (50, [
            ("G", 5, 6, "quarter", True, 0, "tenuto", True, False),
            ("F", 5, 4, "quarter", False, 0, None, False, False),
            ("E", 5, 2, "eighth", False, -1, None, False, True),
        ]),
        (51, [
            ("D", 5, 4, "quarter", False, 0, None, True, False),
            ("C", 5, 2, "eighth", False, 0, None, False, False),
            ("B", 4, 4, "quarter", False, -1, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (52, [
            ("D", 5, 12, "half", True, 0, "tenuto", False, False),
        ]),
        (53, [
            ("E", 5, 3, "eighth", True, -1, None, True, False),
            ("F", 5, 1, "16th", False, 0, None, False, False),
            ("G", 5, 4, "quarter", False, 0, None, False, False),
            ("A", 5, 2, "eighth", False, -1, None, False, False),
            ("G", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (54, [
            ("A", 5, 6, "quarter", True, -1, "accent", False, False),  # High Ab5! peak
            ("G", 5, 3, "eighth", True, 0, None, True, False),
            ("F", 5, 1, "16th", False, 0, None, False, False),
            ("E", 5, 2, "eighth", False, -1, None, False, True),
        ]),
        (55, [
            ("F", 5, 6, "quarter", True, 0, "tenuto", True, False),
            ("E", 5, 2, "eighth", False, -1, None, False, False),
            ("D", 5, 2, "eighth", False, 0, None, False, False),
            ("C", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (56, [
            ("D", 5, 8, "half", False, 0, "tenuto", False, False),
            ("C", 5, 4, "quarter", False, 0, None, False, False),
        ]),
        (57, [
            ("E", 5, 6, "quarter", True, -1, None, True, False),
            ("F", 5, 3, "eighth", True, 0, None, False, False),
            ("G", 5, 1, "16th", False, 0, None, False, False),
            ("A", 5, 2, "eighth", False, -1, None, False, True),
        ]),
        (58, [
            ("B", 5, 6, "quarter", True, -1, "accent", False, False),  # Bb5! highest point
            ("A", 5, 3, "eighth", True, -1, None, True, False),
            ("G", 5, 1, "16th", False, 0, None, False, False),
            ("F", 5, 2, "eighth", False, 0, None, False, True),
        ]),
        (59, [
            ("G", 5, 6, "quarter", True, 0, "tenuto", True, False),
            ("F", 5, 4, "quarter", False, 0, None, False, False),
            ("E", 5, 2, "eighth", False, -1, None, False, True),
        ]),
        (60, [
            ("F", 5, 12, "half", True, 0, "tenuto", False, False),
        ]),
        (61, [
            ("E", 5, 6, "quarter", True, -1, None, True, False),
            ("D", 5, 3, "eighth", True, 0, None, False, False),
            ("C", 5, 1, "16th", False, 0, None, False, False),
            ("B", 4, 2, "eighth", False, -1, None, False, True),
        ]),
        (62, [
            ("C", 5, 6, "quarter", True, 0, "tenuto", True, False),
            ("B", 4, 4, "quarter", False, -1, None, False, False),
            ("A", 4, 2, "eighth", False, 0, None, False, True),
        ]),
        (63, [
            ("B", 4, 4, "quarter", False, -1, None, True, False),
            ("C", 5, 4, "quarter", False, 0, None, False, False),
            ("D", 5, 4, "quarter", False, 0, None, False, True),
        ]),
        (64, [
            ("D", 5, 8, "half", False, 0, "tenuto", False, False),
            ("rest", 0, 4, "quarter", False, 0, None, False, False),
        ]),
    ]

    for m_num, notes in section4_cl:
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 49:
            attr = ET.SubElement(meas, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "-2"
            ET.SubElement(key, "mode").text = "major"
            add_direction(meas, text="Largamente, ♩.= 80", tempo=120)
            add_direction(meas, dynamic="f")
        if m_num == 53:
            add_direction(meas, wedge="crescendo")
        if m_num == 56:
            add_direction(meas, wedge="stop")
        if m_num == 57:
            add_direction(meas, wedge="crescendo")
        if m_num == 60:
            add_direction(meas, wedge="stop")
            add_direction(meas, dynamic="ff")
        if m_num == 61:
            add_direction(meas, wedge="diminuendo")
        if m_num == 64:
            add_direction(meas, wedge="stop")

        for item in notes:
            s, o, dur, ntype, dot, alt, artic, sl_start, sl_stop = item
            if s == "rest":
                meas.append(cl(s, o, dur, ntype, dot=dot, rest=True))
            else:
                acc = None
                if alt == -1:
                    acc = "flat"
                meas.append(cl(s, o, dur, ntype, dot=dot, alter=alt, acc=acc,
                              artic=artic, slur_start=sl_start, slur_stop=sl_stop))

    # --- Section V: mm. 65-80, Clarinet rests ---
    for m_num in range(65, 81):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 65:
            attr = ET.SubElement(meas, "attributes")
            key = ET.SubElement(attr, "key")
            ET.SubElement(key, "fifths").text = "1"
            ET.SubElement(key, "mode").text = "major"
            add_direction(meas, text="Come un ricordo, ♩.= 69", tempo=104)
            add_direction(meas, dynamic="pp")
        if m_num == 80:
            barline = ET.SubElement(meas, "barline")
            barline.set("location", "right")
            ET.SubElement(barline, "bar-style").text = "light-heavy"
        meas.append(make_note(None, None, 12, "whole", rest=True, voice="1"))

    # ============================================================
    # PIANO PART (P2) — concert pitch, F major (1 flat)
    # v2: more extended chords, staccato bass, articulations
    # ============================================================
    p2 = ET.SubElement(score, "part")
    p2.set("id", "P2")

    def write_piano_m(m_num, rh_notes, lh_notes, attrs_fn=None, dirs=None):
        """Write a piano measure with RH (voice 1, staff 1) and LH (voice 2, staff 2)."""
        meas = ET.SubElement(p2, "measure")
        meas.set("number", str(m_num))
        if attrs_fn:
            attrs_fn(meas)
        if dirs:
            for d in dirs:
                d(meas)
        for n in rh_notes:
            meas.append(n)
        add_backup(meas, 12)
        for n in lh_notes:
            meas.append(n)
        return meas

    # Section I: mm 1-16, Piano solo, F major
    # v2: staccato on bass notes, more chord variety

    # m.1: F major
    def m1_attrs(meas):
        add_attributes(meas, divisions=4, key_fifths=-1, key_mode="major",
                      time_beats=6, time_type=8, clef_sign="G", clef_line=2,
                      clef_sign2="F", clef_line2=4, staves=2)

    write_piano_m(1,
        [rh("F",4,2,"eighth"), rh("A",4,2,"eighth"), rh("C",5,2,"eighth"),
         rh("A",4,2,"eighth"), rh("C",5,2,"eighth"), rh("A",4,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("F",2,6,"quarter",dot=True,artic="staccato")],
        attrs_fn=m1_attrs,
        dirs=[
            lambda m: add_direction(m, text="Dolce", staff="1"),
            lambda m: add_direction(m, dynamic="pp", staff="1"),
            lambda m: add_direction(m, tempo=108, text="♩.= 72", staff="1"),
        ])

    # m.2: Fmaj7
    write_piano_m(2,
        [rh("F",4,2,"eighth"), rh("A",4,2,"eighth"), rh("E",5,2,"eighth"),
         rh("A",4,2,"eighth"), rh("E",5,2,"eighth"), rh("C",5,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("C",3,6,"quarter",dot=True)])

    # m.3: Bb/F
    write_piano_m(3,
        [rh("F",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth"),
         rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth"), rh("F",5,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("F",2,6,"quarter",dot=True)])

    # m.4: Fadd9
    write_piano_m(4,
        [rh("F",4,2,"eighth"), rh("G",4,2,"eighth"), rh("A",4,2,"eighth"),
         rh("C",5,2,"eighth"), rh("G",4,2,"eighth"), rh("A",4,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("C",3,6,"quarter",dot=True)])

    # m.5: F
    write_piano_m(5,
        [rh("F",4,2,"eighth"), rh("A",4,2,"eighth"), rh("C",5,2,"eighth"),
         rh("A",4,2,"eighth"), rh("C",5,2,"eighth"), rh("F",5,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("F",2,6,"quarter",dot=True)],
        dirs=[lambda m: add_direction(m, wedge="crescendo", staff="1")])

    # m.6: C/E with 7th
    write_piano_m(6,
        [rh("E",4,2,"eighth"), rh("G",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1),
         rh("C",5,2,"eighth"), rh("E",5,2,"eighth"), rh("G",4,2,"eighth")],
        [lh("E",3,6,"quarter",dot=True,artic="staccato"), lh("C",3,6,"quarter",dot=True)])

    # m.7: Dm9
    write_piano_m(7,
        [rh("D",4,2,"eighth"), rh("F",4,2,"eighth"), rh("A",4,2,"eighth"),
         rh("C",5,2,"eighth"), rh("E",5,2,"eighth"), rh("A",4,2,"eighth")],
        [lh("D",3,6,"quarter",dot=True,artic="staccato"), lh("A",2,6,"quarter",dot=True)])

    # m.8: Bbmaj7
    write_piano_m(8,
        [rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth"), rh("A",4,2,"eighth"),
         rh("F",4,2,"eighth"), rh("A",4,2,"eighth"), rh("D",5,2,"eighth")],
        [lh("B",2,6,"quarter",dot=True,alter=-1,artic="staccato"), lh("F",3,6,"quarter",dot=True)],
        dirs=[
            lambda m: add_direction(m, wedge="stop", staff="1"),
            lambda m: add_direction(m, dynamic="mp", staff="1"),
        ])

    # m.9: Fsus4
    write_piano_m(9,
        [rh("F",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1), rh("C",5,2,"eighth"),
         rh("F",4,2,"eighth"), rh("A",4,2,"eighth"), rh("C",5,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("C",3,6,"quarter",dot=True)])

    # m.10: Fadd9
    write_piano_m(10,
        [rh("F",4,2,"eighth"), rh("G",4,2,"eighth"), rh("A",4,2,"eighth"),
         rh("C",5,2,"eighth"), rh("G",4,2,"eighth"), rh("A",4,2,"eighth")],
        [lh("F",3,6,"quarter",dot=True,artic="staccato"), lh("C",3,6,"quarter",dot=True)])

    # m.11: Bb6
    write_piano_m(11,
        [rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth"), rh("G",5,2,"eighth"),
         rh("D",5,2,"eighth"), rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth")],
        [lh("B",2,6,"quarter",dot=True,alter=-1,artic="staccato"), lh("F",3,6,"quarter",dot=True)])

    # m.12: Gm9
    write_piano_m(12,
        [rh("G",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth"),
         rh("F",5,2,"eighth"), rh("A",5,2,"eighth"), rh("D",5,2,"eighth")],
        [lh("G",3,6,"quarter",dot=True,artic="staccato"), lh("D",3,6,"quarter",dot=True)])

    # m.13: Am7
    write_piano_m(13,
        [rh("A",4,2,"eighth"), rh("C",5,2,"eighth"), rh("E",5,2,"eighth"),
         rh("G",5,2,"eighth"), rh("E",5,2,"eighth"), rh("C",5,2,"eighth")],
        [lh("A",2,6,"quarter",dot=True,artic="staccato"), lh("E",3,6,"quarter",dot=True)],
        dirs=[lambda m: add_direction(m, wedge="crescendo", staff="1")])

    # m.14: Dm7
    write_piano_m(14,
        [rh("D",4,2,"eighth"), rh("F",4,2,"eighth"), rh("A",4,2,"eighth"),
         rh("C",5,2,"eighth"), rh("A",4,2,"eighth"), rh("D",5,2,"eighth")],
        [lh("D",3,6,"quarter",dot=True,artic="staccato"), lh("A",2,6,"quarter",dot=True)])

    # m.15: Gm7
    write_piano_m(15,
        [rh("G",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1), rh("D",5,2,"eighth"),
         rh("F",5,2,"eighth"), rh("D",5,2,"eighth"), rh("B",4,2,"eighth",alter=-1)],
        [lh("G",3,6,"quarter",dot=True,artic="staccato"), lh("D",3,6,"quarter",dot=True)])

    # m.16: C9sus4 -> C9
    write_piano_m(16,
        [rh("C",4,2,"eighth"), rh("F",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1),
         rh("D",5,2,"eighth"), rh("E",4,2,"eighth"), rh("B",4,2,"eighth",alter=-1)],
        [lh("C",3,6,"quarter",dot=True,artic="staccato"), lh("G",2,6,"quarter",dot=True)],
        dirs=[lambda m: add_direction(m, wedge="stop", staff="1")])

    # Section II: mm 17-28
    sec2_piano_data = {
        17: ([("F",4,0),("A",4,0),("C",5,0),("G",4,0),("A",4,0),("C",5,0)], [("F",3,0),("C",3,0)]),
        18: ([("F",4,0),("A",4,0),("E",5,0),("G",4,0),("C",5,0),("E",5,0)], [("F",3,0),("C",3,0)]),
        19: ([("D",4,0),("F",4,0),("A",4,0),("G",4,0),("B",4,-1),("D",5,0)], [("D",3,0),("G",3,0)]),
        20: ([("B",4,-1),("D",5,0),("A",4,0),("F",4,0),("A",4,0),("D",5,0)], [("B",2,-1),("F",3,0)]),
        21: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),
        22: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        23: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),
        24: ([("F",4,0),("A",4,0),("C",5,0),("G",4,0),("A",4,0),("C",5,0)], [("F",3,0),("C",3,0)]),
        25: ([("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),
        26: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0),("F",5,0)], [("B",2,-1),("F",3,0)]),
        27: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("E",4,0)], [("C",3,0),("G",2,0)]),
        28: ([("F",4,0),("A",4,0),("C",5,0),("G",4,0),("A",4,0),("F",4,0)], [("F",3,0),("C",3,0)]),
    }

    for mn in range(17, 29):
        m = ET.SubElement(p2, "measure")
        m.set("number", str(mn))
        if mn == 17:
            add_direction(m, dynamic="mp", staff="1")
        rh_pat, lh_roots = sec2_piano_data[mn]
        for s, o, a in rh_pat:
            m.append(rh(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(lh(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(lh(s2, o2, 6, "quarter", dot=True, alter=a2))

    # Section III: mm 29-48
    sec3_piano_data = {
        29: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0)], [("F",3,0),("C",3,0)]),
        30: ([("E",4,0),("G",4,0),("C",5,0),("E",5,0),("G",4,0),("C",5,0)], [("C",3,0),("G",2,0)]),
        31: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("A",4,0),("F",4,0)], [("D",3,0),("A",2,0)]),
        32: ([("B",4,-1),("D",5,0),("F",5,0),("A",4,0),("D",5,0),("F",5,0)], [("B",2,-1),("F",3,0)]),
        33: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),
        34: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),
        35: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        36: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("E",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),
        37: ([("D",4,0),("F",4,0),("A",4,0),("D",5,0),("F",4,0),("A",4,0)], [("D",3,0),("A",2,0)]),
        38: ([("G",4,0),("B",4,-1),("D",5,0),("G",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        39: ([("A",4,0),("C",5,0),("E",5,0),("G",4,0),("C",5,0),("E",5,0)], [("A",2,0),("E",3,0)]),
        40: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("A",4,0),("D",5,0)], [("D",3,0),("A",2,0)]),
        41: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),
        42: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),
        43: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),
        44: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0)], [("F",3,0),("C",3,0)]),
        45: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),
        46: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),
        47: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        48: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("E",4,0)], [("C",3,0),("G",2,0)]),
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
        rh_pat, lh_roots = sec3_piano_data[mn]
        for s, o, a in rh_pat:
            m.append(rh(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(lh(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(lh(s2, o2, 6, "quarter", dot=True, alter=a2))

    # Section IV: mm 49-64, Ab major
    sec4_piano_data = {
        49: ([("A",4,-1),("C",5,0),("E",5,-1),("G",4,0),("C",5,0),("E",5,-1)], [("A",3,-1),("E",3,-1)]),
        50: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),
        51: ([("D",4,-1),("F",4,0),("A",4,-1),("C",5,0),("A",4,-1),("F",4,0)], [("D",3,-1),("A",3,-1)]),
        52: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",2,-1),("E",3,-1)]),
        53: ([("B",4,-1),("D",5,-1),("F",5,0),("A",5,-1),("F",5,0),("D",5,-1)], [("B",2,-1),("F",3,0)]),
        54: ([("E",4,-1),("G",4,0),("B",4,-1),("D",5,-1),("F",5,0),("B",4,-1)], [("E",3,-1),("B",2,-1)]),
        55: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),
        56: ([("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("A",4,-1)], [("F",3,0),("C",3,0)]),
        57: ([("D",4,-1),("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("A",4,-1)], [("D",3,-1),("A",2,-1)]),
        58: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("A",5,-1)], [("A",3,-1),("E",3,-1)]),
        59: ([("B",4,-1),("D",5,-1),("F",5,0),("A",5,-1),("F",5,0),("D",5,-1)], [("B",2,-1),("F",3,0)]),
        60: ([("E",4,-1),("G",4,0),("B",4,-1),("D",5,0),("G",5,0),("B",4,-1)], [("E",3,-1),("B",2,-1)]),
        61: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),
        62: ([("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("A",4,-1)], [("F",3,0),("C",3,0)]),
        63: ([("D",4,-1),("F",4,0),("B",4,-1),("D",5,-1),("F",5,0),("B",4,-1)], [("D",3,-1),("B",2,-1)]),
        64: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),
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

        rh_pat, lh_roots = sec4_piano_data[mn]
        for s, o, a in rh_pat:
            m.append(rh(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(lh(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(lh(s2, o2, 6, "quarter", dot=True, alter=a2))

    # Section V: mm 65-80, return to F major, enriched
    sec5_piano_data = {
        65: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0)], [("F",3,0),("F",2,0)]),
        66: ([("F",4,0),("A",4,0),("E",5,0),("G",4,0),("C",5,0),("E",5,0)], [("F",3,0),("C",3,0)]),
        67: ([("F",4,0),("B",4,-1),("D",5,0),("A",4,0),("D",5,0),("F",5,0)], [("F",3,0),("F",2,0)]),
        68: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),
        69: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),
        70: ([("G",4,0),("B",4,0),("D",5,0),("F",5,0),("D",5,0),("B",4,0)], [("G",3,0),("D",3,0)]),
        71: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),
        # m.72: clarinet melody in piano RH (F-G-A-Bb-C)
        72: ([("F",4,0),("G",4,0),("A",4,0),("B",4,-1),("C",5,0),("E",5,0)], [("A",2,0),("E",3,0)]),
        73: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),
        74: ([("D",4,0),("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0)], [("D",3,0),("A",2,0)]),
        75: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),
        76: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),
        77: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),
        78: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),
        79: ([("G",4,0),("B",4,-1),("D",5,0),("A",4,0),("C",5,0),("E",5,0)], [("G",3,0),("C",3,0)]),
        80: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("F",2,0)]),
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

        rh_pat, lh_roots = sec5_piano_data[mn]
        for s, o, a in rh_pat:
            m.append(rh(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2, o2, a2 = lh_roots[1]
        m.append(lh(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(lh(s2, o2, 6, "quarter", dot=True, alter=a2))

    return score


def write_musicxml(score, filepath):
    rough = ET.tostring(score, encoding="unicode")
    dom = minidom.parseString(rough)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">')
    root_str = dom.documentElement.toprettyxml(indent="  ")
    if root_str.startswith("<?xml"):
        root_str = root_str.split("?>", 1)[1].lstrip("\n")
    lines.append(root_str)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written to {filepath}")


if __name__ == "__main__":
    score = build_score()
    write_musicxml(score, "/home/khaled/rachmaniclaude/experiment/008/track_02/score.musicxml")
    print("Done generating v2 score.")
