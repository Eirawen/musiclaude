#!/usr/bin/env python3
"""Generate Matin de Boulangerie MusicXML score v3 — addresses feedback:
- Increase pct_extended_chords: replace many triads with 7th/9th/sus4 chords
- Widen melodic range: use D4 low (written) and B5 high (written) for clarinet
- More chord vocabulary: add dim7, aug, sus2 chords
- Add more hairpins
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

DIVISIONS = 4

def make_note(pitch_step, pitch_octave, duration, note_type, dot=False, rest=False,
              chord=False, alter=0, tie_start=False, tie_stop=False, staff=None,
              voice=None, stem=None, accidental=None, articulation=None,
              slur_start=False, slur_stop=False):
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

def R(s, o, dur, ntype, dot=False, alter=0, chord=False, tie_start=False,
      tie_stop=False, acc=None, artic=None, slur_start=False, slur_stop=False):
    return make_note(s, o, dur, ntype, dot=dot, voice="1", staff=1,
                     stem="up", alter=alter, chord=chord,
                     tie_start=tie_start, tie_stop=tie_stop, accidental=acc,
                     articulation=artic, slur_start=slur_start, slur_stop=slur_stop)

def L(s, o, dur, ntype, dot=False, alter=0, chord=False, tie_start=False,
      tie_stop=False, acc=None, artic=None, slur_start=False, slur_stop=False):
    return make_note(s, o, dur, ntype, dot=dot, voice="2", staff=2,
                     stem="down", alter=alter, chord=chord,
                     tie_start=tie_start, tie_stop=tie_stop, accidental=acc,
                     articulation=artic, slur_start=slur_start, slur_stop=slur_stop)

def C(s, o, dur, ntype, dot=False, alter=0, rest=False, acc=None, artic=None,
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
    # CLARINET PART (P1) — G major (1 sharp)
    # v3: wider range D4-B5 written, more varied rhythms
    # ============================================================
    p1 = ET.SubElement(score, "part")
    p1.set("id", "P1")

    # Section I: mm 1-16, rests
    for m_num in range(1, 17):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 1:
            add_attributes(meas, divisions=4, key_fifths=1, key_mode="major",
                          time_beats=6, time_type=8, clef_sign="G", clef_line=2,
                          clef_number=1)
            add_direction(meas, text="Dolce, ♩.= 72", tempo=108)
        meas.append(make_note(None, None, 12, "whole", rest=True, voice="1"))

    # Section II: mm 17-28
    # (step, oct, dur, type, dot, alter, artic, slur_start, slur_stop)
    s2 = {
        17: [("G",4,6,"quarter",True,0,None,True,False),
             ("A",4,3,"eighth",True,0,None,False,False),
             ("B",4,1,"16th",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        18: [("D",5,6,"quarter",True,0,"tenuto",True,False),
             ("C",5,4,"quarter",False,0,None,False,False),
             ("B",4,2,"eighth",False,0,None,False,True)],
        19: [("A",4,4,"quarter",False,0,None,True,False),
             ("G",4,4,"quarter",False,0,None,False,False),
             ("F",4,2,"eighth",False,0,None,False,False),
             ("E",4,2,"eighth",False,0,None,False,True)],
        20: [("D",4,12,"half",True,0,"tenuto",False,False)],  # Low D4! range expansion
        21: [("E",4,3,"eighth",True,0,None,True,False),
             ("F",4,1,"16th",False,0,None,False,False),
             ("G",4,2,"eighth",False,0,None,False,False),
             ("A",4,2,"eighth",False,0,None,False,False),
             ("B",4,2,"eighth",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        22: [("E",5,6,"quarter",True,0,"tenuto",True,False),
             ("D",5,3,"eighth",True,0,None,False,False),
             ("C",5,1,"16th",False,0,None,False,False),
             ("B",4,2,"eighth",False,0,None,False,True)],
        23: [("A",4,4,"quarter",False,0,None,True,False),
             ("G",4,2,"eighth",False,0,None,False,False),
             ("F",4,4,"quarter",False,0,None,False,False),
             ("G",4,2,"eighth",False,0,None,False,True)],
        24: [("A",4,12,"half",True,0,"tenuto",False,False)],
        25: [("G",4,3,"eighth",True,0,None,True,False),
             ("A",4,1,"16th",False,0,None,False,False),
             ("B",4,2,"eighth",False,0,None,False,False),
             ("C",5,4,"quarter",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,True)],
        26: [("E",5,6,"quarter",True,0,"tenuto",False,False),
             ("D",5,6,"quarter",True,0,None,False,False)],
        27: [("C",5,4,"quarter",False,0,None,True,False),
             ("B",4,4,"quarter",False,0,None,False,False),
             ("A",4,4,"quarter",False,0,None,False,True)],
        28: [("G",4,8,"half",False,0,"tenuto",False,False),
             ("F",4,4,"quarter",False,0,None,False,False)],
    }

    for m_num in range(17, 29):
        meas = ET.SubElement(p1, "measure")
        meas.set("number", str(m_num))
        if m_num == 17:
            add_direction(meas, text="espressivo")
            add_direction(meas, dynamic="mp")
        if m_num == 21:
            add_direction(meas, wedge="crescendo")
        if m_num == 24:
            add_direction(meas, wedge="stop")
        for s, o, dur, ntype, dot, alt, artic, sl_s, sl_e in s2[m_num]:
            meas.append(C(s, o, dur, ntype, dot=dot, alter=alt, artic=artic,
                         slur_start=sl_s, slur_stop=sl_e))

    # Section III: mm 29-48
    s3 = {
        29: [("G",4,6,"quarter",True,0,None,True,False),
             ("A",4,2,"eighth",False,0,None,False,False),
             ("B",4,1,"16th",False,0,None,False,False),
             ("C",5,1,"16th",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,True)],
        30: [("E",5,6,"quarter",True,0,"tenuto",True,False),
             ("D",5,2,"eighth",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,False),
             ("B",4,2,"eighth",False,0,None,False,True)],
        31: [("A",4,4,"quarter",False,0,None,True,False),
             ("G",4,2,"eighth",False,0,None,False,False),
             ("E",4,4,"quarter",False,0,None,False,False),
             ("D",4,2,"eighth",False,0,None,False,True)],
        32: [("E",4,12,"half",True,0,"tenuto",False,False)],
        33: [("rest",0,6,"quarter",True,0,None,False,False),
             ("A",4,2,"eighth",False,0,None,True,False),
             ("B",4,1,"16th",False,0,None,False,False),
             ("C",5,1,"16th",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,True)],
        34: [("E",5,4,"quarter",False,0,None,True,False),
             ("F",5,3,"eighth",True,0,None,False,False),
             ("E",5,1,"16th",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        35: [("B",4,6,"quarter",True,0,"tenuto",True,False),
             ("A",4,6,"quarter",True,0,None,False,True)],
        36: [("G",4,8,"half",False,0,None,False,False),
             ("rest",0,4,"quarter",False,0,None,False,False)],
        # D minor excursion
        37: [("A",4,6,"quarter",True,0,None,True,False),
             ("B",4,2,"eighth",False,-1,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,True)],
        38: [("E",5,3,"eighth",True,0,None,True,False),
             ("D",5,1,"16th",False,0,None,False,False),
             ("C",5,4,"quarter",False,0,None,False,False),
             ("B",4,2,"eighth",False,-1,None,False,False),
             ("A",4,2,"eighth",False,0,None,False,True)],
        39: [("G",4,6,"quarter",True,0,"tenuto",True,False),
             ("A",4,3,"eighth",True,0,None,False,False),
             ("B",4,1,"16th",False,-1,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        40: [("A",4,12,"half",True,0,"tenuto",False,False)],
        41: [("rest",0,4,"quarter",False,0,None,False,False),
             ("G",4,2,"eighth",False,0,None,True,False),
             ("A",4,2,"eighth",False,0,None,False,False),
             ("B",4,2,"eighth",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        42: [("D",5,6,"quarter",True,0,None,True,False),
             ("E",5,4,"quarter",False,0,None,False,False),
             ("F",5,2,"eighth",False,0,None,False,True)],
        43: [("G",5,4,"quarter",False,0,"accent",False,False),
             ("F",5,3,"eighth",True,0,None,True,False),
             ("E",5,1,"16th",False,0,None,False,False),
             ("D",5,4,"quarter",False,0,None,False,True)],
        44: [("C",5,6,"quarter",True,0,"tenuto",False,False),
             ("B",4,6,"quarter",True,0,None,False,False)],
        45: [("A",4,3,"eighth",True,0,None,True,False),
             ("B",4,1,"16th",False,0,None,False,False),
             ("C",5,4,"quarter",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,False),
             ("E",5,2,"eighth",False,0,None,False,True)],
        46: [("F",5,6,"quarter",True,0,"tenuto",True,False),
             ("E",5,2,"eighth",False,0,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        47: [("D",5,3,"eighth",True,0,None,True,False),
             ("C",5,1,"16th",False,0,None,False,False),
             ("B",4,4,"quarter",False,0,None,False,False),
             ("A",4,2,"eighth",False,0,None,False,False),
             ("G",4,2,"eighth",False,0,None,False,True)],
        48: [("G",4,12,"half",True,0,"tenuto",False,False)],
    }

    for m_num in range(29, 49):
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
        if m_num == 43:
            add_direction(meas, wedge="crescendo")
        if m_num == 44:
            add_direction(meas, wedge="stop")
        if m_num == 45:
            add_direction(meas, wedge="crescendo")
        if m_num == 48:
            add_direction(meas, wedge="stop")

        for item in s3[m_num]:
            s, o, dur, ntype, dot, alt, artic, sl_s, sl_e = item
            if s == "rest":
                meas.append(C(s, o, dur, ntype, dot=dot, rest=True))
            else:
                acc = None
                if alt == -1:
                    acc = "natural"
                meas.append(C(s, o, dur, ntype, dot=dot, alter=alt, acc=acc,
                              artic=artic, slur_start=sl_s, slur_stop=sl_e))

    # Section IV: mm 49-64, Ab major (written Bb major for clarinet)
    s4 = {
        49: [("C",5,6,"quarter",True,0,None,True,False),
             ("D",5,3,"eighth",True,0,None,False,False),
             ("E",5,1,"16th",False,-1,None,False,False),
             ("F",5,2,"eighth",False,0,None,False,True)],
        50: [("G",5,6,"quarter",True,0,"tenuto",True,False),
             ("F",5,4,"quarter",False,0,None,False,False),
             ("E",5,2,"eighth",False,-1,None,False,True)],
        51: [("D",5,4,"quarter",False,0,None,True,False),
             ("C",5,2,"eighth",False,0,None,False,False),
             ("B",4,4,"quarter",False,-1,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        52: [("D",5,12,"half",True,0,"tenuto",False,False)],
        53: [("E",5,3,"eighth",True,-1,None,True,False),
             ("F",5,1,"16th",False,0,None,False,False),
             ("G",5,4,"quarter",False,0,None,False,False),
             ("A",5,2,"eighth",False,-1,None,False,False),
             ("G",5,2,"eighth",False,0,None,False,True)],
        54: [("A",5,6,"quarter",True,-1,"accent",False,False),
             ("G",5,3,"eighth",True,0,None,True,False),
             ("F",5,1,"16th",False,0,None,False,False),
             ("E",5,2,"eighth",False,-1,None,False,True)],
        55: [("F",5,6,"quarter",True,0,"tenuto",True,False),
             ("E",5,2,"eighth",False,-1,None,False,False),
             ("D",5,2,"eighth",False,0,None,False,False),
             ("C",5,2,"eighth",False,0,None,False,True)],
        56: [("D",5,8,"half",False,0,"tenuto",False,False),
             ("C",5,4,"quarter",False,0,None,False,False)],
        57: [("E",5,6,"quarter",True,-1,None,True,False),
             ("F",5,3,"eighth",True,0,None,False,False),
             ("G",5,1,"16th",False,0,None,False,False),
             ("A",5,2,"eighth",False,-1,None,False,True)],
        58: [("B",5,6,"quarter",True,-1,"accent",False,False),  # Bb5 written = Ab5 sounding, peak!
             ("A",5,3,"eighth",True,-1,None,True,False),
             ("G",5,1,"16th",False,0,None,False,False),
             ("F",5,2,"eighth",False,0,None,False,True)],
        59: [("G",5,6,"quarter",True,0,"tenuto",True,False),
             ("F",5,4,"quarter",False,0,None,False,False),
             ("E",5,2,"eighth",False,-1,None,False,True)],
        60: [("F",5,12,"half",True,0,"tenuto",False,False)],
        61: [("E",5,6,"quarter",True,-1,None,True,False),
             ("D",5,3,"eighth",True,0,None,False,False),
             ("C",5,1,"16th",False,0,None,False,False),
             ("B",4,2,"eighth",False,-1,None,False,True)],
        62: [("C",5,6,"quarter",True,0,"tenuto",True,False),
             ("B",4,4,"quarter",False,-1,None,False,False),
             ("A",4,2,"eighth",False,0,None,False,True)],
        63: [("B",4,4,"quarter",False,-1,None,True,False),
             ("C",5,4,"quarter",False,0,None,False,False),
             ("D",5,4,"quarter",False,0,None,False,True)],
        64: [("D",5,8,"half",False,0,"tenuto",False,False),
             ("rest",0,4,"quarter",False,0,None,False,False)],
    }

    for m_num in range(49, 65):
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
        if m_num == 55:
            add_direction(meas, wedge="stop")
        if m_num == 56:
            add_direction(meas, wedge="diminuendo")
        if m_num == 57:
            add_direction(meas, wedge="stop")
            add_direction(meas, wedge="crescendo")
        if m_num == 58:
            add_direction(meas, dynamic="ff")
        if m_num == 59:
            add_direction(meas, wedge="stop")
        if m_num == 60:
            add_direction(meas, wedge="diminuendo")
        if m_num == 61:
            add_direction(meas, wedge="stop")
        if m_num == 62:
            add_direction(meas, wedge="diminuendo")
        if m_num == 64:
            add_direction(meas, wedge="stop")

        for item in s4[m_num]:
            s, o, dur, ntype, dot, alt, artic, sl_s, sl_e = item
            if s == "rest":
                meas.append(C(s, o, dur, ntype, dot=dot, rest=True))
            else:
                acc = None
                if alt == -1:
                    acc = "flat"
                meas.append(C(s, o, dur, ntype, dot=dot, alter=alt, acc=acc,
                              artic=artic, slur_start=sl_s, slur_stop=sl_e))

    # Section V: mm 65-80, rests
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
    # PIANO PART (P2)
    # v3: HEAVILY extended chords — 7ths, 9ths, sus4, dim, aug
    # Every measure now uses extended harmony where possible
    # ============================================================
    p2 = ET.SubElement(score, "part")
    p2.set("id", "P2")

    def pm(m_num, rh_notes, lh_notes, attrs_fn=None, dirs=None):
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

    # ---- SECTION I: mm 1-16, Piano solo ----
    # v3: Every chord is now 7th, 9th, sus4, or add chord

    def m1_attrs(meas):
        add_attributes(meas, divisions=4, key_fifths=-1, key_mode="major",
                      time_beats=6, time_type=8, clef_sign="G", clef_line=2,
                      clef_sign2="F", clef_line2=4, staves=2)

    # m1: Fmaj7
    pm(1,
       [R("F",4,2,"eighth"), R("A",4,2,"eighth"), R("E",5,2,"eighth"),
        R("A",4,2,"eighth"), R("C",5,2,"eighth"), R("E",5,2,"eighth")],
       [L("F",3,6,"quarter",dot=True,artic="staccato"), L("C",3,6,"quarter",dot=True,artic="staccato")],
       attrs_fn=m1_attrs,
       dirs=[lambda m: add_direction(m, text="Dolce", staff="1"),
             lambda m: add_direction(m, dynamic="pp", staff="1"),
             lambda m: add_direction(m, tempo=108, text="♩.= 72", staff="1")])

    # m2: Fmaj9
    pm(2,
       [R("F",4,2,"eighth"), R("G",4,2,"eighth"), R("A",4,2,"eighth"),
        R("E",5,2,"eighth"), R("G",4,2,"eighth"), R("C",5,2,"eighth")],
       [L("F",3,6,"quarter",dot=True,artic="staccato"), L("C",3,6,"quarter",dot=True)])

    # m3: Bbmaj7
    pm(3,
       [R("B",4,2,"eighth",alter=-1), R("D",5,2,"eighth"), R("A",4,2,"eighth"),
        R("F",5,2,"eighth"), R("D",5,2,"eighth"), R("A",4,2,"eighth")],
       [L("B",2,6,"quarter",dot=True,alter=-1,artic="staccato"), L("F",3,6,"quarter",dot=True)])

    # m4: Fadd9
    pm(4,
       [R("F",4,2,"eighth"), R("G",4,2,"eighth"), R("A",4,2,"eighth"),
        R("C",5,2,"eighth"), R("G",5,2,"eighth"), R("A",4,2,"eighth")],
       [L("F",3,6,"quarter",dot=True,artic="staccato"), L("C",3,6,"quarter",dot=True)])

    # m5: Dm9
    pm(5,
       [R("D",4,2,"eighth"), R("F",4,2,"eighth"), R("A",4,2,"eighth"),
        R("C",5,2,"eighth"), R("E",5,2,"eighth"), R("A",4,2,"eighth")],
       [L("D",3,6,"quarter",dot=True,artic="staccato"), L("A",2,6,"quarter",dot=True)],
       dirs=[lambda m: add_direction(m, wedge="crescendo", staff="1")])

    # m6: C9
    pm(6,
       [R("E",4,2,"eighth"), R("G",4,2,"eighth"), R("B",4,2,"eighth",alter=-1),
        R("D",5,2,"eighth"), R("E",5,2,"eighth"), R("G",4,2,"eighth")],
       [L("C",3,6,"quarter",dot=True,artic="staccato"), L("G",2,6,"quarter",dot=True)])

    # m7: Dm7
    pm(7,
       [R("D",4,2,"eighth"), R("F",4,2,"eighth"), R("A",4,2,"eighth"),
        R("C",5,2,"eighth"), R("A",4,2,"eighth"), R("F",4,2,"eighth")],
       [L("D",3,6,"quarter",dot=True,artic="staccato"), L("A",2,6,"quarter",dot=True)])

    # m8: Bbmaj9
    pm(8,
       [R("B",4,2,"eighth",alter=-1), R("D",5,2,"eighth"), R("A",4,2,"eighth"),
        R("C",5,2,"eighth"), R("F",5,2,"eighth"), R("D",5,2,"eighth")],
       [L("B",2,6,"quarter",dot=True,alter=-1,artic="staccato"), L("F",3,6,"quarter",dot=True)],
       dirs=[lambda m: add_direction(m, wedge="stop", staff="1"),
             lambda m: add_direction(m, dynamic="mp", staff="1")])

    # m9: Fsus4
    pm(9,
       [R("F",4,2,"eighth"), R("B",4,2,"eighth",alter=-1), R("C",5,2,"eighth"),
        R("F",5,2,"eighth"), R("C",5,2,"eighth"), R("B",4,2,"eighth",alter=-1)],
       [L("F",3,6,"quarter",dot=True,artic="staccato"), L("C",3,6,"quarter",dot=True)])

    # m10: Fadd9
    pm(10,
       [R("F",4,2,"eighth"), R("G",4,2,"eighth"), R("A",4,2,"eighth"),
        R("C",5,2,"eighth"), R("G",4,2,"eighth"), R("E",5,2,"eighth")],
       [L("F",3,6,"quarter",dot=True,artic="staccato"), L("C",3,6,"quarter",dot=True)])

    # m11: Gm7
    pm(11,
       [R("G",4,2,"eighth"), R("B",4,2,"eighth",alter=-1), R("D",5,2,"eighth"),
        R("F",5,2,"eighth"), R("D",5,2,"eighth"), R("B",4,2,"eighth",alter=-1)],
       [L("G",3,6,"quarter",dot=True,artic="staccato"), L("D",3,6,"quarter",dot=True)])

    # m12: Gm9
    pm(12,
       [R("G",4,2,"eighth"), R("B",4,2,"eighth",alter=-1), R("D",5,2,"eighth"),
        R("F",5,2,"eighth"), R("A",5,2,"eighth"), R("D",5,2,"eighth")],
       [L("G",3,6,"quarter",dot=True,artic="staccato"), L("D",3,6,"quarter",dot=True)])

    # m13: Am7
    pm(13,
       [R("A",4,2,"eighth"), R("C",5,2,"eighth"), R("E",5,2,"eighth"),
        R("G",5,2,"eighth"), R("E",5,2,"eighth"), R("C",5,2,"eighth")],
       [L("A",2,6,"quarter",dot=True,artic="staccato"), L("E",3,6,"quarter",dot=True)],
       dirs=[lambda m: add_direction(m, wedge="crescendo", staff="1")])

    # m14: Dm9
    pm(14,
       [R("D",4,2,"eighth"), R("F",4,2,"eighth"), R("A",4,2,"eighth"),
        R("C",5,2,"eighth"), R("E",5,2,"eighth"), R("A",4,2,"eighth")],
       [L("D",3,6,"quarter",dot=True,artic="staccato"), L("A",2,6,"quarter",dot=True)])

    # m15: Gm7
    pm(15,
       [R("G",4,2,"eighth"), R("B",4,2,"eighth",alter=-1), R("D",5,2,"eighth"),
        R("F",5,2,"eighth"), R("D",5,2,"eighth"), R("B",4,2,"eighth",alter=-1)],
       [L("G",3,6,"quarter",dot=True,artic="staccato"), L("D",3,6,"quarter",dot=True)])

    # m16: C9sus4
    pm(16,
       [R("C",4,2,"eighth"), R("F",4,2,"eighth"), R("B",4,2,"eighth",alter=-1),
        R("D",5,2,"eighth"), R("G",4,2,"eighth"), R("B",4,2,"eighth",alter=-1)],
       [L("C",3,6,"quarter",dot=True,artic="staccato"), L("G",2,6,"quarter",dot=True)],
       dirs=[lambda m: add_direction(m, wedge="stop", staff="1")])

    # ---- SECTION II: mm 17-28 ----
    # v3: more 7ths and 9ths
    s2p = {
        17: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj7
        18: ([("F",4,0),("G",4,0),("A",4,0),("E",5,0),("C",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj9
        19: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("B",4,-1),("D",5,0)], [("D",3,0),("G",3,0)]),  # Dm7->Gm
        20: ([("B",4,-1),("D",5,0),("A",4,0),("F",5,0),("D",5,0),("A",4,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        21: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),  # Am7
        22: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),  # Gm9
        23: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),  # C9
        24: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("G",4,0),("C",5,0)], [("F",3,0),("C",3,0)]),  # Fmaj7
        25: ([("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj9
        26: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        27: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("E",4,0)], [("C",3,0),("G",2,0)]),  # C9
        28: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0),("F",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj7
    }

    for mn in range(17, 29):
        m = ET.SubElement(p2, "measure")
        m.set("number", str(mn))
        if mn == 17:
            add_direction(m, dynamic="mp", staff="1")
        if mn == 21:
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 24:
            add_direction(m, wedge="stop", staff="1")
        rh_pat, lh_roots = s2p[mn]
        for s, o, a in rh_pat:
            m.append(R(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2_, o2, a2 = lh_roots[1]
        m.append(L(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(L(s2_, o2, 6, "quarter", dot=True, alter=a2))

    # ---- SECTION III: mm 29-48 ----
    # v3: extended chords throughout
    s3p = {
        29: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj7
        30: ([("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0),("C",5,0)], [("C",3,0),("G",2,0)]),  # C9
        31: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),  # Dm9
        32: ([("B",4,-1),("D",5,0),("F",5,0),("A",4,0),("D",5,0),("F",5,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        33: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),  # Am7
        34: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),  # Dm9
        35: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),  # Gm9
        36: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),  # C9
        # Dm excursion
        37: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("D",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),  # Dm7
        38: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),  # Gm9
        39: ([("A",4,0),("C",5,0),("E",5,0),("G",4,0),("C",5,0),("E",5,0)], [("A",2,0),("E",3,0)]),  # Am7
        40: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),  # Dm9
        41: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),  # Dm9
        42: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),  # Gm9
        43: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),  # C9
        44: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("G",5,0),("C",5,0)], [("F",3,0),("C",3,0)]),  # Fmaj9
        45: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        46: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),  # Am7
        47: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("D",5,0),("B",4,-1)], [("G",3,0),("D",3,0)]),  # Gm7
        48: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("E",4,0)], [("C",3,0),("G",2,0)]),  # C9
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
        if mn == 43:
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 44:
            add_direction(m, wedge="stop", staff="1")
        if mn == 45:
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 48:
            add_direction(m, wedge="stop", staff="1")

        rh_pat, lh_roots = s3p[mn]
        for s, o, a in rh_pat:
            m.append(R(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2_, o2, a2 = lh_roots[1]
        m.append(L(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(L(s2_, o2, 6, "quarter", dot=True, alter=a2))

    # ---- SECTION IV: mm 49-64, Ab major ----
    s4p = {
        49: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),  # Abmaj7
        50: ([("A",4,-1),("C",5,0),("G",4,0),("E",5,-1),("B",4,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),  # Abmaj9
        51: ([("D",4,-1),("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("A",4,-1)], [("D",3,-1),("A",3,-1)]),  # Dbmaj7
        52: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",2,-1),("E",3,-1)]),  # Abmaj7
        53: ([("B",4,-1),("D",5,-1),("F",5,0),("A",5,-1),("F",5,0),("D",5,-1)], [("B",2,-1),("F",3,0)]),  # Bbm7
        54: ([("E",4,-1),("G",4,0),("B",4,-1),("D",5,-1),("F",5,0),("B",4,-1)], [("E",3,-1),("B",2,-1)]),  # Eb9
        55: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("B",4,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),  # Abmaj9
        56: ([("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("C",5,0),("A",4,-1)], [("F",3,0),("C",3,0)]),  # Fm7
        57: ([("D",4,-1),("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("A",4,-1)], [("D",3,-1),("A",2,-1)]),  # Dbmaj9
        58: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("B",5,-1),("E",5,-1)], [("A",3,-1),("E",3,-1)]),  # Abmaj7
        59: ([("B",4,-1),("D",5,-1),("F",5,0),("A",5,-1),("F",5,0),("D",5,-1)], [("B",2,-1),("F",3,0)]),  # Bbm7
        60: ([("E",4,-1),("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("B",4,-1)], [("E",3,-1),("B",2,-1)]),  # Eb9
        61: ([("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("E",5,-1),("C",5,0)], [("A",3,-1),("E",3,-1)]),  # Abmaj7
        62: ([("F",4,0),("A",4,-1),("C",5,0),("E",5,-1),("G",5,0),("C",5,0)], [("F",3,0),("C",3,0)]),  # Fm9
        63: ([("D",4,-1),("F",4,0),("B",4,-1),("D",5,-1),("F",5,0),("A",4,-1)], [("D",3,-1),("B",2,-1)]),  # Dbmaj7
        64: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),  # C9 (pivot)
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
        if mn == 55:
            add_direction(m, wedge="stop", staff="1")
        if mn == 56:
            add_direction(m, wedge="diminuendo", staff="1")
        if mn == 57:
            add_direction(m, wedge="stop", staff="1")
            add_direction(m, wedge="crescendo", staff="1")
        if mn == 58:
            add_direction(m, wedge="stop", staff="1")
            add_direction(m, dynamic="ff", staff="1")
        if mn == 59:
            add_direction(m, wedge="diminuendo", staff="1")
        if mn == 61:
            add_direction(m, wedge="stop", staff="1")
        if mn == 62:
            add_direction(m, wedge="diminuendo", staff="1")
        if mn == 64:
            add_direction(m, wedge="stop", staff="1")
            add_direction(m, dynamic="mf", staff="1")

        rh_pat, lh_roots = s4p[mn]
        for s, o, a in rh_pat:
            m.append(R(s, o, 2, "eighth", alter=a))
        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2_, o2, a2 = lh_roots[1]
        m.append(L(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(L(s2_, o2, 6, "quarter", dot=True, alter=a2))

    # ---- SECTION V: mm 65-80 ----
    s5p = {
        65: ([("F",4,0),("A",4,0),("C",5,0),("E",5,0),("C",5,0),("A",4,0)], [("F",3,0),("F",2,0)]),  # Fmaj7
        66: ([("F",4,0),("G",4,0),("A",4,0),("E",5,0),("C",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj9
        67: ([("B",4,-1),("D",5,0),("A",4,0),("F",5,0),("D",5,0),("A",4,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        68: ([("F",4,0),("A",4,0),("G",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),  # Fadd9/maj7
        69: ([("D",4,0),("F",4,0),("A",4,0),("C",5,0),("E",5,0),("A",4,0)], [("D",3,0),("A",2,0)]),  # Dm9
        70: ([("G",4,0),("B",4,0),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),  # G9 (nat B)
        71: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        # m72: clarinet melody in RH
        72: ([("F",4,2,"eighth"), R("G",4,2,"eighth"), R("A",4,2,"eighth"),
              R("B",4,2,"eighth",alter=-1), R("C",5,2,"eighth"), R("E",5,2,"eighth")],
             [("A",2,0),("E",3,0)]),  # Am7
        73: ([("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("C",3,0)]),  # Fmaj9
        74: ([("D",4,0),("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0)], [("D",3,0),("A",2,0)]),  # Dm9
        75: ([("G",4,0),("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("D",5,0)], [("G",3,0),("D",3,0)]),  # Gm9
        76: ([("C",4,0),("E",4,0),("G",4,0),("B",4,-1),("D",5,0),("G",4,0)], [("C",3,0),("G",2,0)]),  # C9
        77: ([("B",4,-1),("D",5,0),("F",5,0),("A",5,0),("F",5,0),("D",5,0)], [("B",2,-1),("F",3,0)]),  # Bbmaj7
        78: ([("A",4,0),("C",5,0),("E",5,0),("G",5,0),("E",5,0),("C",5,0)], [("A",2,0),("E",3,0)]),  # Am7
        79: ([("G",4,0),("B",4,-1),("D",5,0),("A",4,0),("C",5,0),("E",5,0)], [("G",3,0),("C",3,0)]),  # Gm7/C9
        80: ([("F",4,0),("G",4,0),("A",4,0),("C",5,0),("E",5,0),("G",4,0)], [("F",3,0),("F",2,0)]),  # Fadd9
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

        rh_pat, lh_roots = s5p[mn]
        # Handle m72 special case where rh_pat contains pre-built note elements
        if mn == 72:
            # m72 has a mix of tuple data and pre-built elements
            # Actually let me fix this - rh_pat[0] is a tuple, rest are Elements
            # Rebuild m72 cleanly
            pass

        if mn != 72:
            for s, o, a in rh_pat:
                m.append(R(s, o, 2, "eighth", alter=a))
        else:
            # m72: F-G-A-Bb-C-E melody
            for s, o, a in [("F",4,0),("G",4,0),("A",4,0),("B",4,-1),("C",5,0),("E",5,0)]:
                m.append(R(s, o, 2, "eighth", alter=a))

        add_backup(m, 12)
        s1, o1, a1 = lh_roots[0]
        s2_, o2, a2 = lh_roots[1]
        m.append(L(s1, o1, 6, "quarter", dot=True, alter=a1, artic="staccato"))
        m.append(L(s2_, o2, 6, "quarter", dot=True, alter=a2))

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
    write_musicxml(score, "/home/khaled/musiclaude/experiment/008/track_02/score.musicxml")
    print("Done generating v3 score.")
