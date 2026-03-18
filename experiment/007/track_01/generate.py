#!/usr/bin/env python3
"""Generate Matin de Boulangerie MusicXML score programmatically using music21.
Iteration 3: Use chordal textures (block chords + melody) so music21 recognizes
extended chords. More chord types. Wider range."""

from music21 import (
    stream, note, chord, clef, key, meter, tempo, instrument,
    dynamics, expressions, articulations, layout, duration, pitch, bar, repeat
)
from music21 import converter
from music21.dynamics import Crescendo, Diminuendo

# === HELPERS ===
def n(p, dur, **kw):
    ql_map = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0, 5: 1.25, 6: 1.5, 8: 2.0, 10: 2.5, 12: 3.0}
    ql = ql_map.get(dur, dur / 4.0)
    nn = note.Note(p, quarterLength=ql)
    if kw.get('tie_start'):
        nn.tie = note.Tie('start')
    if kw.get('tie_stop'):
        nn.tie = note.Tie('stop')
    if kw.get('staccato'):
        nn.articulations.append(articulations.Staccato())
    if kw.get('tenuto'):
        nn.articulations.append(articulations.Tenuto())
    if kw.get('accent'):
        nn.articulations.append(articulations.Accent())
    return nn

def r(dur):
    ql_map = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0, 6: 1.5, 8: 2.0, 12: 3.0}
    ql = ql_map.get(dur, dur / 4.0)
    return note.Rest(quarterLength=ql)

def ch(pitches, dur, **kw):
    ql_map = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1.0, 5: 1.25, 6: 1.5, 8: 2.0, 10: 2.5, 12: 3.0}
    ql = ql_map.get(dur, dur / 4.0)
    c = chord.Chord(pitches, quarterLength=ql)
    if kw.get('staccato'):
        c.articulations.append(articulations.Staccato())
    if kw.get('tenuto'):
        c.articulations.append(articulations.Tenuto())
    if kw.get('accent'):
        c.articulations.append(articulations.Accent())
    return c

def make_measure(number, elements, ts=None, ks=None):
    m = stream.Measure(number=number)
    if ts:
        m.timeSignature = meter.TimeSignature(ts)
    if ks:
        m.keySignature = key.KeySignature(ks)
    for el in elements:
        m.append(el)
    return m

# Pattern: bass note (eighth) + block chord (2 beats) | bass note (eighth) + block chord (2 beats)
# This gives 6/8 feel AND creates real 4+ note chords for extended chord detection.
# Total: 2 + 4 + 2 + 4 = 12 ✓
# Or variation: bass(2) + chord(4) + bass(2) + chord(4) = 12

# Another pattern: bass(2) + chord(2) + melody(2) | bass(2) + chord(2) + melody(2) = 12

# ============================================================
# BUILD SCORE
# ============================================================
score = stream.Score()
score.insert(0, layout.ScoreLayout())

clarinet_part = stream.Part()
piano_part = stream.Part()

cl_inst = instrument.Clarinet()
clarinet_part.insert(0, cl_inst)
pn_inst = instrument.Piano()
piano_part.insert(0, pn_inst)

clarinet_part.partName = "Clarinet in Bb"
clarinet_part.partAbbreviation = "Cl."
piano_part.partName = "Piano"
piano_part.partAbbreviation = "Pno."

# ============================================================
# SECTION I: MORNING (mm. 1-16) - Piano alone
# Pattern: bass eighth + 4-note block chord (dotted quarter) + treble melody (dotted quarter)
# Bass(2) + Chord(6) + Melody(4) = 12... no
# Let's do: bass(2) + chord(4) | bass(2) + chord(4) = 12
# Or: bass(2) + chord(2) + top(2) | bass(2) + chord(2) + top(2) = 12 (arp feel with chords)
# Best for detection: bass(2) + block_chord(4) + bass(2) + block_chord(4) = 12
# ============================================================

def piano_section_I():
    measures = []

    # m1: Fmaj7 - pp, dolce
    m = make_measure(1, [], ts='6/8', ks=-1)
    m.insert(0, tempo.MetronomeMark('Andante pastorale', 72, note.Note(quarterLength=1.5)))
    m.insert(0, dynamics.Dynamic('pp'))
    te = expressions.TextExpression('dolce')
    te.style.fontStyle = 'italic'
    m.insert(0, te)
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'A4', 'C5'], 4))   # Fmaj7 chord
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'E4', 'F4', 'C5'], 4))    # Fmaj7 voicing 2
    measures.append(m)

    # m2: Fadd9
    m = make_measure(2, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'A3', 'G4', 'A4'], 4))   # Fadd9
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'G4', 'C5'], 4))   # Fadd9 spread
    measures.append(m)

    # m3: Bbmaj7 - dotted eighth bass for variety
    m = make_measure(3, [])
    m.append(n('B-2', 3, staccato=True))   # dotted eighth
    m.append(n('F3', 1))                    # sixteenth
    m.append(ch(['A3', 'D4', 'F4', 'A4'], 2))   # Bbmaj7
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'D4', 'B-4'], 4))  # Bbmaj7 spread
    measures.append(m)

    # m4: Fsus4 -> Fmaj7
    m = make_measure(4, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'B-3', 'F4', 'C5'], 4))  # Fsus4
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'A3', 'E4', 'C5'], 4))   # Fmaj7 resolution
    measures.append(m)

    # m5: Dm9
    m = make_measure(5, [])
    m.append(n('D2', 2, staccato=True))
    m.append(ch(['A2', 'C4', 'E4', 'F4'], 4))   # Dm9
    m.append(n('D2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'C4', 'E4'], 4))   # Dm9 voicing 2
    measures.append(m)

    # m6: Gm9
    m = make_measure(6, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'A3', 'B-3', 'F4'], 4))  # Gm9
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B-3', 'D4', 'F4', 'A4'], 4))  # Gm9 upper
    measures.append(m)

    # m7: C9
    m = make_measure(7, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'D4', 'E4'], 4))  # C9
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'B-4', 'D5'], 4))  # C9 upper
    measures.append(m)

    # m8: Fadd9 -> mp
    m = make_measure(8, [])
    m.insert(0, dynamics.Dynamic('mp'))
    m.append(n('F2', 3, staccato=True))    # dotted eighth
    m.append(n('C3', 1))                    # sixteenth
    m.append(ch(['A3', 'C4', 'G4', 'A4'], 2))   # Fadd9
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'G4', 'A4', 'C5'], 4))   # Fadd9 high
    measures.append(m)

    # m9: Fmaj7#11 - Lydian color
    m = make_measure(9, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'A4', 'B4'], 4))   # Fmaj7#11
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'E4', 'B4', 'C5'], 4))   # Fmaj7#11 voicing
    measures.append(m)

    # m10: Am7
    m = make_measure(10, [])
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['E3', 'G3', 'C4', 'E4'], 4))   # Am7
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C4', 'E4', 'G4', 'A4'], 4))   # Am7 upper
    measures.append(m)

    # m11: Bb6/9
    m = make_measure(11, [])
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'G3', 'C4', 'D4'], 4))   # Bb6/9
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'G4', 'C5'], 4))   # Bb6/9 upper
    measures.append(m)

    # m12: Bdim7 - chromatic passing
    m = make_measure(12, [])
    m.append(n('B2', 3, staccato=True))    # dotted eighth
    m.append(n('F3', 1))                    # sixteenth
    m.append(ch(['A-3', 'B3', 'D4', 'F4'], 2))  # Bdim7
    m.append(n('B2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'A-4', 'B4'], 4))  # Bdim7 upper
    measures.append(m)

    # m13: Gm11
    m = make_measure(13, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'C4', 'F4', 'A4'], 4))   # Gm11
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B-3', 'D4', 'F4', 'C5'], 4))  # Gm11 voicing
    measures.append(m)

    # m14: C7sus4
    m = make_measure(14, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'F4', 'G4'], 4))  # C7sus4
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['B-3', 'F4', 'G4', 'C5'], 4))  # C7sus4 upper
    measures.append(m)

    # m15: C13
    m = make_measure(15, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'E4', 'A4'], 4))  # C13
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'A4', 'B-4'], 4))  # C13 upper
    measures.append(m)

    # m16: Fmaj9 - settling
    m = make_measure(16, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'G4', 'A4'], 4))   # Fmaj9
    m.append(ch(['F2', 'C3', 'E4', 'G4', 'A4'], 6))  # Fmaj9 full, held
    measures.append(m)

    return measures

def clarinet_section_I():
    measures = []
    for i in range(1, 17):
        if i == 1:
            m = make_measure(i, [r(12)], ts='6/8', ks=-1)
        else:
            m = make_measure(i, [r(12)])
        measures.append(m)
    return measures

# ============================================================
# SECTION II: THE DOOR OPENS (mm. 17-28)
# ============================================================

def piano_section_II():
    measures = []

    # m17: Fmaj9 - colorful
    m = make_measure(17, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'G4', 'A4'], 4))   # Fmaj9
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'E4', 'G4', 'C5'], 4))   # Fmaj9 spread
    measures.append(m)

    # m18: Gm11
    m = make_measure(18, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'C4', 'F4', 'B-4'], 4))  # Gm11
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'C4', 'D4'], 4))   # Gm9
    measures.append(m)

    # m19: Am7 - dotted rhythm
    m = make_measure(19, [])
    m.append(n('A2', 3, staccato=True))
    m.append(n('E3', 1))
    m.append(ch(['G3', 'C4', 'E4', 'A4'], 2))   # Am7
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C4', 'E4', 'G4', 'B4'], 4))   # Am7 w/ 9th
    measures.append(m)

    # m20: Bbmaj9
    m = make_measure(20, [])
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'C4', 'D4'], 4))   # Bbmaj9
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['A3', 'D4', 'F4', 'C5'], 4))   # Bbmaj9 spread
    measures.append(m)

    # m21: C9sus4
    m = make_measure(21, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'D4', 'F4'], 4))  # C9sus4
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'G4', 'B-4'], 4))  # C9sus4 upper
    measures.append(m)

    # m22: C7 resolution
    m = make_measure(22, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'E4', 'G4'], 4))  # C7
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'B-4', 'D5'], 4))  # C9 upper
    measures.append(m)

    # m23: Dm9
    m = make_measure(23, [])
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'E4', 'F4'], 4))   # Dm9
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['F4', 'A4', 'C5', 'E5'], 4))   # Dm9 high
    measures.append(m)

    # m24: Bbmaj7#11
    m = make_measure(24, [])
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'E4', 'F4'], 4))   # Bbmaj7#11
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['A3', 'D4', 'E4', 'B-4'], 4))  # Bbmaj7#11 voicing
    measures.append(m)

    # m25: Gm7 with sixteenths
    m = make_measure(25, [])
    m.append(n('G2', 2, staccato=True))
    m.append(n('D3', 1))
    m.append(n('F3', 1))
    m.append(ch(['B-3', 'D4', 'F4', 'A4'], 2))  # Gm7
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'G4', 'B-4'], 4))  # Gm upper
    measures.append(m)

    # m26: Csus4add9
    m = make_measure(26, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'D4', 'F4', 'G4'], 4))   # Csus4/9
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['F4', 'G4', 'B-4', 'C5'], 4))  # Csus4/7 high
    measures.append(m)

    # m27: Fmaj9
    m = make_measure(27, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'G4', 'A4'], 4))   # Fmaj9
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'G4', 'A4', 'C5'], 4))   # Fmaj9 spread
    measures.append(m)

    # m28: F6/9
    m = make_measure(28, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'D4', 'G4', 'A4'], 4))   # F6/9
    m.append(ch(['F2', 'C3', 'A3', 'D4', 'G4'], 6))  # F6/9 full, held
    measures.append(m)

    return measures

def clarinet_section_II():
    """Clarinet primary motif. Written Bb clarinet pitch (up M2)."""
    measures = []

    # m17: breath + entry
    m = make_measure(17, [])
    m.insert(0, dynamics.Dynamic('mp'))
    te = expressions.TextExpression('espressivo')
    te.style.fontStyle = 'italic'
    m.insert(0, te)
    m.append(r(2))
    m.append(n('G4', 4, tenuto=True))   # sounds F4
    m.append(n('A4', 4))                 # sounds G4
    m.append(n('B4', 2))                 # sounds A4
    measures.append(m)

    # m18: top of motif
    m = make_measure(18, [])
    m.append(n('C5', 6, tenuto=True))   # sounds Bb4
    m.append(n('B4', 4))                 # sounds A4
    m.append(n('A4', 2))
    measures.append(m)

    # m19: dotted eighth + sixteenth variation
    m = make_measure(19, [])
    m.append(n('G4', 3))
    m.append(n('A4', 1))
    m.append(n('B4', 2))
    m.append(n('D5', 2))    # leap
    m.append(n('C5', 2))
    m.append(n('B4', 2))
    measures.append(m)

    # m20: settling
    m = make_measure(20, [])
    m.append(n('C5', 6, tenuto=True))
    m.append(n('A4', 4))
    m.append(r(2))
    measures.append(m)

    # m21: rising
    m = make_measure(21, [])
    m.append(n('G4', 2))
    m.append(n('A4', 2))
    m.append(n('B4', 2))
    m.append(n('D5', 4, tenuto=True))
    m.append(n('C5', 2))
    measures.append(m)

    # m22: higher with dotted rhythm
    m = make_measure(22, [])
    m.append(n('E5', 6, tenuto=True))   # sounds D5
    m.append(n('D5', 3))
    m.append(n('B4', 1))
    m.append(n('C5', 2))
    measures.append(m)

    # m23: gentle descent
    m = make_measure(23, [])
    m.append(n('A4', 4))
    m.append(n('G4', 2))
    m.append(n('F4', 6))    # sounds Eb4
    measures.append(m)

    # m24: breath
    m = make_measure(24, [])
    m.append(n('E4', 6))    # sounds D4
    m.append(r(6))
    measures.append(m)

    # m25: echo with dotted rhythm
    m = make_measure(25, [])
    m.append(r(2))
    m.append(n('G4', 3))
    m.append(n('A4', 1))
    m.append(n('B4', 2))
    m.append(n('C5', 4))
    measures.append(m)

    # m26: suspension
    m = make_measure(26, [])
    m.append(n('D5', 8, tenuto=True))
    m.append(n('C5', 4))
    measures.append(m)

    # m27: final descent
    m = make_measure(27, [])
    m.append(n('A4', 6))
    m.append(n('G4', 6))
    measures.append(m)

    # m28: settling
    m = make_measure(28, [])
    m.append(n('G4', 8, tenuto=True))
    m.append(r(4))
    measures.append(m)

    return measures

# ============================================================
# SECTION III: CONVERSATION (mm. 29-48)
# ============================================================

def piano_section_III():
    measures = []

    # m29: Fmaj7 - con moto
    m = make_measure(29, [], ks=-1)
    m.insert(0, tempo.MetronomeMark('Con moto', 76, note.Note(quarterLength=1.5)))
    te = expressions.TextExpression('con moto')
    te.style.fontStyle = 'italic'
    m.insert(0, te)
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'A4', 'C5'], 4))   # Fmaj7
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'E4', 'F4'], 4))   # Fmaj7
    measures.append(m)

    # m30: Gm7 dotted
    m = make_measure(30, [])
    m.append(n('G2', 3, staccato=True))
    m.append(n('D3', 1))
    m.append(ch(['F3', 'B-3', 'D4', 'G4'], 2))  # Gm7
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B-3', 'D4', 'F4', 'A4'], 4))  # Gm9
    measures.append(m)

    # m31: Am9
    m = make_measure(31, [])
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['E3', 'G3', 'B3', 'C4'], 4))   # Am9
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C4', 'E4', 'G4', 'B4'], 4))   # Am9 upper
    measures.append(m)

    # m32: Bbadd9
    m = make_measure(32, [])
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'B-3', 'C4', 'D4'], 4))  # Bbadd9
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'C5', 'D5'], 4))   # Bbadd9 high
    measures.append(m)

    # m33: C9 - mf
    m = make_measure(33, [])
    m.insert(0, dynamics.Dynamic('mf'))
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'D4', 'E4'], 4))  # C9
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'B-4', 'D5'], 4))  # C9 upper
    measures.append(m)

    # m34: Dm9
    m = make_measure(34, [])
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'E4', 'F4'], 4))   # Dm9
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['F4', 'A4', 'C5', 'E5'], 4))   # Dm9 high
    measures.append(m)

    # m35: Gm9
    m = make_measure(35, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'A3', 'B-3', 'F4'], 4))  # Gm9
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B-3', 'D4', 'F4', 'A4'], 4))  # Gm9 upper
    measures.append(m)

    # m36: A7b9 - secondary dom
    m = make_measure(36, [])
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['E3', 'C#4', 'G4', 'B-4'], 4)) # A7b9
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C#4', 'E4', 'G4', 'B-4'], 4)) # A7b9 upper
    measures.append(m)

    # m37: Dm7 - D minor excursion - mp
    m = make_measure(37, [], ks=-1)
    m.insert(0, dynamics.Dynamic('mp'))
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'F4', 'A4'], 4))   # Dm7
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['F3', 'C4', 'D4', 'A4'], 4))   # Dm7 voicing
    measures.append(m)

    # m38: Gm(add9)
    m = make_measure(38, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'A3', 'B-3', 'D4'], 4))  # Gm(add9)
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B-3', 'D4', 'G4', 'A4'], 4))  # Gm(add9) upper
    measures.append(m)

    # m39: A7#5 augmented dom
    m = make_measure(39, [])
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['E3', 'C#4', 'F4', 'G4'], 4))  # A7#5 (F=aug5th enharmonic)
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C#4', 'F4', 'G4', 'B4'], 4))  # A7#5 upper
    measures.append(m)

    # m40: Dm6
    m = make_measure(40, [])
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['A3', 'B3', 'D4', 'F4'], 4))   # Dm6
    m.append(ch(['D3', 'A3', 'B3', 'F4'], 6))   # Dm6 held
    measures.append(m)

    # m41: Bbmaj7 - mf
    m = make_measure(41, [])
    m.insert(0, dynamics.Dynamic('mf'))
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'D4', 'F4'], 4))   # Bbmaj7
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['A3', 'D4', 'F4', 'A4'], 4))   # Bbmaj7 upper
    measures.append(m)

    # m42: C7#9
    m = make_measure(42, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'D#4', 'E4'], 4)) # C7#9
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'B-4', 'D#5'], 4)) # C7#9 upper
    measures.append(m)

    # m43: F/A
    m = make_measure(43, [])
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'C4', 'F4'], 4))
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C4', 'F4', 'A4', 'C5'], 4))
    measures.append(m)

    # m44: Dm11
    m = make_measure(44, [])
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'G4', 'A4'], 4))   # Dm11
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['G4', 'A4', 'C5', 'D5'], 4))   # Dm11 upper
    measures.append(m)

    # m45: Gm7 sixteenths
    m = make_measure(45, [])
    m.append(n('G2', 2, staccato=True))
    m.append(n('D3', 1))
    m.append(n('F3', 1))
    m.append(ch(['B-3', 'D4', 'F4', 'A4'], 2))  # Gm7
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'G4', 'B-4'], 4))  # Gm upper
    measures.append(m)

    # m46: C7sus4
    m = make_measure(46, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'F4', 'G4'], 4))  # C7sus4
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['F4', 'G4', 'B-4', 'C5'], 4))  # C7sus4 upper
    measures.append(m)

    # m47: C13
    m = make_measure(47, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'E4', 'A4'], 4))  # C13
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'A4', 'B-4', 'D5'], 4))  # C13 upper
    measures.append(m)

    # m48: Ebaug - pivot to Ab
    m = make_measure(48, [])
    m.append(n('E-3', 2, staccato=True))
    m.append(ch(['G3', 'B3', 'E-4', 'G4'], 4))  # Ebaug
    m.append(n('E-3', 2, staccato=True))
    m.append(ch(['B3', 'E-4', 'G4', 'B4'], 4))  # Ebaug upper
    measures.append(m)

    return measures

def clarinet_section_III():
    measures = []

    # m29: call - dotted rhythm
    m = make_measure(29, [])
    m.append(n('G4', 3))
    m.append(n('A4', 1))
    m.append(n('B4', 2))
    m.append(n('D5', 6, tenuto=True))
    measures.append(m)

    # m30: rest then response
    m = make_measure(30, [])
    m.append(r(6))
    m.append(n('E5', 2))
    m.append(n('D5', 2))
    m.append(n('B4', 2))
    measures.append(m)

    # m31: longer phrase
    m = make_measure(31, [])
    m.append(n('C5', 3))
    m.append(n('B4', 1))
    m.append(n('A4', 2))
    m.append(n('G4', 2))
    m.append(n('A4', 2))
    m.append(n('B4', 2))
    measures.append(m)

    # m32: held
    m = make_measure(32, [])
    m.append(n('C5', 6, tenuto=True))
    m.append(r(2))
    m.append(n('D5', 4))
    measures.append(m)

    # m33: bolder
    m = make_measure(33, [])
    m.append(n('E5', 4, accent=True))
    m.append(n('D5', 2))
    m.append(n('E5', 3))
    m.append(n('F5', 1))
    m.append(n('D5', 2))
    measures.append(m)

    # m34: energy
    m = make_measure(34, [])
    m.append(n('E5', 6, tenuto=True))
    m.append(n('C5', 2))
    m.append(n('B4', 2))
    m.append(n('A4', 2))
    measures.append(m)

    # m35: leap
    m = make_measure(35, [])
    m.append(n('G4', 2))
    m.append(n('B4', 2))
    m.append(n('D5', 2))
    m.append(n('F5', 4, tenuto=True))
    m.append(n('E5', 2))
    measures.append(m)

    # m36: chromatic
    m = make_measure(36, [])
    m.append(n('D5', 6))
    m.append(n('C#5', 3))
    m.append(n('B4', 1))
    m.append(n('A4', 2))
    measures.append(m)

    # m37: D minor - lower
    m = make_measure(37, [])
    m.insert(0, dynamics.Dynamic('mp'))
    m.append(n('A4', 6, tenuto=True))
    m.append(n('G4', 3))
    m.append(n('F4', 1))
    m.append(n('E4', 2))
    measures.append(m)

    # m38: sighing
    m = make_measure(38, [])
    m.append(n('F4', 4))
    m.append(n('E4', 2))
    m.append(n('D4', 6))    # sounds C4 - lowest in this section
    measures.append(m)

    # m39: pleading
    m = make_measure(39, [])
    m.append(n('E4', 3))
    m.append(n('F4', 1))
    m.append(n('G4', 2))
    m.append(n('B4', 4, tenuto=True))
    m.append(n('A4', 2))
    measures.append(m)

    # m40: resolution
    m = make_measure(40, [])
    m.append(n('G4', 8))
    m.append(r(4))
    measures.append(m)

    # m41: warming back - mf
    m = make_measure(41, [])
    m.insert(0, dynamics.Dynamic('mf'))
    m.append(r(6))
    m.append(n('B4', 2))
    m.append(n('C5', 2))
    m.append(n('D5', 2))
    measures.append(m)

    # m42: growing, sixteenths
    m = make_measure(42, [])
    m.append(n('E5', 6, accent=True))
    m.append(n('D5', 1))
    m.append(n('C5', 1))
    m.append(n('B4', 2))
    m.append(n('C5', 2))
    measures.append(m)

    # m43: flowing
    m = make_measure(43, [])
    m.append(n('D5', 3))
    m.append(n('C5', 1))
    m.append(n('A4', 2))
    m.append(n('G4', 2))
    m.append(n('A4', 2))
    m.append(n('B4', 2))
    measures.append(m)

    # m44: lyrical
    m = make_measure(44, [])
    m.append(n('D5', 6, tenuto=True))
    m.append(n('C5', 4))
    m.append(n('A4', 2))
    measures.append(m)

    # m45: building
    m = make_measure(45, [])
    m.append(n('B4', 2))
    m.append(n('C5', 2))
    m.append(n('D5', 2))
    m.append(n('E5', 4, tenuto=True))
    m.append(n('D5', 2))
    measures.append(m)

    # m46: reaching
    m = make_measure(46, [])
    m.append(n('F5', 6, accent=True))
    m.append(n('E5', 3))
    m.append(n('D5', 1))
    m.append(n('C5', 2))
    measures.append(m)

    # m47: settling
    m = make_measure(47, [])
    m.append(n('D5', 3))
    m.append(n('C5', 1))
    m.append(n('B4', 2))
    m.append(n('A4', 6))
    measures.append(m)

    # m48: transition
    m = make_measure(48, [])
    m.append(n('G4', 6))
    m.append(r(6))
    measures.append(m)

    return measures

# ============================================================
# SECTION IV: WALKING HOME (mm. 49-64) - Ab major
# ============================================================

def piano_section_IV():
    measures = []

    # m49: Abmaj9 - f, largamente
    m = make_measure(49, [], ks=-4)
    m.insert(0, tempo.MetronomeMark('Largamente', 80, note.Note(quarterLength=1.5)))
    te = expressions.TextExpression('largamente')
    te.style.fontStyle = 'italic'
    m.insert(0, te)
    m.insert(0, dynamics.Dynamic('f'))
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['E-2', 'G3', 'B-3', 'C4'], 4))    # Abmaj9
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['C4', 'E-4', 'G4', 'B-4'], 4))    # Abmaj9 upper
    measures.append(m)

    # m50: Bbm9
    m = make_measure(50, [])
    m.append(n('B-1', 2, staccato=True))
    m.append(ch(['F2', 'A-3', 'C4', 'D-4'], 4))    # Bbm9
    m.append(n('B-1', 2, staccato=True))
    m.append(ch(['D-4', 'F4', 'A-4', 'C5'], 4))    # Bbm9 upper
    measures.append(m)

    # m51: Eb9 dotted - climactic, high register
    m = make_measure(51, [])
    m.append(n('E-2', 3, staccato=True))
    m.append(n('B-2', 1))
    m.append(ch(['D-4', 'F4', 'G4', 'B-4'], 2))    # Eb9
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['G4', 'B-4', 'D-5'], 2))           # Eb9 upper
    m.append(n('A-5', 2))                             # high Ab5 - extends melodic range!
    measures.append(m)

    # m52: Abmaj7
    m = make_measure(52, [])
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['E-2', 'G3', 'C4', 'E-4'], 4))    # Abmaj7
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['C4', 'E-4', 'G4', 'A-4'], 4))    # Abmaj7 upper
    measures.append(m)

    # m53: Fm9
    m = make_measure(53, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E-3', 'G3', 'A-3'], 4))    # Fm9
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A-3', 'C4', 'E-4', 'G4'], 4))    # Fm9 upper
    measures.append(m)

    # m54: Bbm11
    m = make_measure(54, [])
    m.append(n('B-1', 2, staccato=True))
    m.append(ch(['F2', 'A-3', 'E-4', 'F4'], 4))    # Bbm11
    m.append(n('B-1', 2, staccato=True))
    m.append(ch(['E-4', 'F4', 'A-4', 'B-4'], 4))   # Bbm11 upper
    measures.append(m)

    # m55: Eb7sus4
    m = make_measure(55, [])
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['B-2', 'D-4', 'A-4', 'B-4'], 4))  # Eb7sus4
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['A-4', 'B-4', 'D-5', 'E-5'], 4))  # Eb7sus4 high
    measures.append(m)

    # m56: Eb13
    m = make_measure(56, [])
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['B-2', 'D-4', 'G4', 'C5'], 4))    # Eb13
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['G4', 'B-4', 'C5', 'E-5'], 4))    # Eb13 upper
    measures.append(m)

    # m57: Ab6/9
    m = make_measure(57, [])
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['E-2', 'F3', 'B-3', 'C4'], 4))    # Ab6/9
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['C4', 'E-4', 'F4', 'B-4'], 4))    # Ab6/9 upper
    measures.append(m)

    # m58: Dbmaj9
    m = make_measure(58, [])
    m.append(n('D-2', 2, staccato=True))
    m.append(ch(['A-2', 'C3', 'E-3', 'F3'], 4))    # Dbmaj9
    m.append(n('D-2', 2, staccato=True))
    m.append(ch(['F3', 'A-3', 'C4', 'E-4'], 4))    # Dbmaj9 upper
    measures.append(m)

    # m59: Bbm7 with sixteenths
    m = make_measure(59, [])
    m.append(n('B-1', 2, staccato=True))
    m.append(n('F2', 1))
    m.append(n('A-2', 1))
    m.append(ch(['D-3', 'F3', 'A-3', 'B-3'], 2))   # Bbm7
    m.append(n('B-1', 2, staccato=True))
    m.append(ch(['F4', 'A-4', 'B-4', 'D-5'], 4))   # Bbm7 upper
    measures.append(m)

    # m60: Eb7b9
    m = make_measure(60, [])
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['B-2', 'D-4', 'E4', 'G4'], 4))    # Eb7b9 (E nat = Fb enhar)
    m.append(n('E-2', 2, staccato=True))
    m.append(ch(['G4', 'B-4', 'D-5', 'E5'], 4))    # Eb7b9 high
    measures.append(m)

    # m61: Abmaj7
    m = make_measure(61, [])
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['E-2', 'G3', 'C4', 'E-4'], 4))
    m.append(n('A-1', 2, staccato=True))
    m.append(ch(['C4', 'E-4', 'G4', 'A-4'], 4))
    measures.append(m)

    # m62: Fm(maj7)
    m = make_measure(62, [])
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E3', 'A-3', 'C4'], 4))     # Fm(maj7)
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A-3', 'C4', 'E4', 'F4'], 4))     # Fm(maj7) upper
    measures.append(m)

    # m63: Db6/9
    m = make_measure(63, [])
    m.append(n('D-2', 2, staccato=True))
    m.append(ch(['A-2', 'B-2', 'E-3', 'F3'], 4))   # Db6/9
    m.append(n('D-2', 2, staccato=True))
    m.append(ch(['F3', 'A-3', 'B-3', 'E-4'], 4))   # Db6/9 upper
    measures.append(m)

    # m64: C7 pivot back to F
    m = make_measure(64, [], ks=-1)
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'E4', 'G4'], 4))     # C7
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'B-4', 'C5'], 4))     # C7 upper
    measures.append(m)

    return measures

def clarinet_section_IV():
    """Peak. Wide intervals, high register, rhythmic variety."""
    measures = []

    # m49: soaring
    m = make_measure(49, [])
    m.insert(0, dynamics.Dynamic('f'))
    m.append(n('B-4', 3, accent=True))
    m.append(n('C5', 1))
    m.append(n('D5', 2))
    m.append(n('F5', 6, tenuto=True))   # sounds Eb5
    measures.append(m)

    # m50: high singing
    m = make_measure(50, [])
    m.append(n('E-5', 2))
    m.append(n('F5', 2))
    m.append(n('G5', 2))    # sounds F5
    m.append(n('F5', 4, tenuto=True))
    m.append(n('D5', 2))
    measures.append(m)

    # m51: dotted descent
    m = make_measure(51, [])
    m.append(n('E-5', 3))
    m.append(n('C5', 1))
    m.append(n('B-4', 2))
    m.append(n('C5', 2))
    m.append(n('D5', 2))
    m.append(n('E-5', 2))
    measures.append(m)

    # m52: breath and rise
    m = make_measure(52, [])
    m.append(n('F5', 6, tenuto=True))
    m.append(r(2))
    m.append(n('D5', 2))
    m.append(n('E-5', 2))
    measures.append(m)

    # m53: peak with wide interval
    m = make_measure(53, [])
    m.append(n('G5', 4, accent=True))   # sounds F5 - highest!
    m.append(n('E-5', 2))
    m.append(n('D5', 2))
    m.append(n('C5', 2))
    m.append(n('B-4', 2))
    measures.append(m)

    # m54: sixteenths
    m = make_measure(54, [])
    m.append(n('C5', 1))
    m.append(n('D5', 1))
    m.append(n('F5', 2))
    m.append(n('G5', 2))
    m.append(n('F5', 4, tenuto=True))
    m.append(n('E-5', 2))
    measures.append(m)

    # m55: big sustained
    m = make_measure(55, [])
    m.append(n('G5', 8, accent=True))
    m.append(n('F5', 4))
    measures.append(m)

    # m56: descending
    m = make_measure(56, [])
    m.append(n('E-5', 3))
    m.append(n('D5', 1))
    m.append(n('C5', 2))
    m.append(n('B-4', 4))
    m.append(n('C5', 2))
    measures.append(m)

    # m57: lyrical
    m = make_measure(57, [])
    m.append(n('D5', 2))
    m.append(n('E-5', 2))
    m.append(n('F5', 2))
    m.append(n('E-5', 6, tenuto=True))
    measures.append(m)

    # m58: warmth, dotted
    m = make_measure(58, [])
    m.append(n('D5', 3))
    m.append(n('B-4', 1))
    m.append(n('C5', 2))
    m.append(n('D5', 2))
    m.append(n('E-5', 2))
    m.append(n('C5', 2))
    measures.append(m)

    # m59: descent
    m = make_measure(59, [])
    m.append(n('D5', 6, tenuto=True))
    m.append(n('C5', 4))
    m.append(n('B-4', 2))
    measures.append(m)

    # m60: winding, wide
    m = make_measure(60, [])
    m.append(n('C5', 2))
    m.append(n('B-4', 2))
    m.append(n('G4', 2))
    m.append(n('B-4', 4))
    m.append(n('A4', 2))
    measures.append(m)

    # m61: gentling - mf
    m = make_measure(61, [])
    m.insert(0, dynamics.Dynamic('mf'))
    m.append(n('B-4', 6, tenuto=True))
    m.append(n('G4', 4))
    m.append(r(2))
    measures.append(m)

    # m62: fading
    m = make_measure(62, [])
    m.append(n('A4', 2))
    m.append(n('B-4', 2))
    m.append(n('C5', 2))
    m.append(n('B-4', 4))
    m.append(n('G4', 2))
    measures.append(m)

    # m63: last gesture dotted
    m = make_measure(63, [])
    m.append(n('A4', 3))
    m.append(n('B-4', 1))
    m.append(n('C5', 2))
    m.append(n('B-4', 6, tenuto=True))
    measures.append(m)

    # m64: pivot
    m = make_measure(64, [])
    m.append(n('B4', 6))
    m.append(n('A4', 4))
    m.append(r(2))
    measures.append(m)

    return measures

# ============================================================
# SECTION V: ALONE AGAIN (mm. 65-80) - enriched return
# ============================================================

def piano_section_V():
    measures = []

    # m65: Fmaj9 - pp, come un ricordo
    m = make_measure(65, [])
    m.insert(0, tempo.MetronomeMark('Andante, come un ricordo', 69, note.Note(quarterLength=1.5)))
    te = expressions.TextExpression('come un ricordo')
    te.style.fontStyle = 'italic'
    m.insert(0, te)
    m.insert(0, dynamics.Dynamic('pp'))
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'G4', 'A4'], 4))    # Fmaj9
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['A3', 'E4', 'G4', 'C5'], 4))    # Fmaj9 spread
    measures.append(m)

    # m66: Gm11
    m = make_measure(66, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'C4', 'F4', 'A4'], 4))    # Gm11
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'B-3', 'D4'], 4))   # Gm9
    measures.append(m)

    # m67: Am7b5 (half-dim)
    m = make_measure(67, [])
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['E-3', 'G3', 'C4', 'E-4'], 4))  # Am7b5
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['C4', 'E-4', 'G4', 'A4'], 4))   # Am7b5 upper
    measures.append(m)

    # m68: Bbmaj7#11
    m = make_measure(68, [])
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'E4', 'F4'], 4))    # Bbmaj7#11
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['A3', 'D4', 'E4', 'B-4'], 4))   # Bbmaj7#11
    measures.append(m)

    # m69: Dm9 dotted
    m = make_measure(69, [])
    m.append(n('D3', 3, staccato=True))
    m.append(n('A3', 1))
    m.append(ch(['C4', 'E4', 'F4', 'A4'], 2))    # Dm9
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['F4', 'A4', 'C5', 'E5'], 4))    # Dm9 high
    measures.append(m)

    # m70: G7b9
    m = make_measure(70, [])
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'F3', 'A-3', 'B3'], 4))   # G7b9
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B3', 'D4', 'F4', 'A-4'], 4))   # G7b9 upper
    measures.append(m)

    # m71: Cmaj9
    m = make_measure(71, [])
    m.append(n('C3', 2, staccato=True))
    m.append(ch(['G3', 'B3', 'D4', 'E4'], 4))    # Cmaj9
    m.append(n('C3', 2, staccato=True))
    m.append(ch(['E4', 'G4', 'B4', 'D5'], 4))    # Cmaj9 upper
    measures.append(m)

    # m72: Am7 - THE MEMORY: clarinet melody in piano RH
    m = make_measure(72, [])
    te2 = expressions.TextExpression('la melodia, teneramente')
    te2.style.fontStyle = 'italic'
    m.insert(0, te2)
    m.append(n('A2', 2, staccato=True))
    m.append(ch(['E3', 'C4', 'G4'], 4))           # Am7 LH
    # melody enters: F4-G4-A4-Bb4 (but as single notes above chord)
    m.append(n('F4', 1))    # melody start
    m.append(n('G4', 1))
    m.append(n('A4', 2))
    m.append(n('B-4', 2))   # melody Bb
    measures.append(m)

    # m73: Bbmaj7 - melody continues
    m = make_measure(73, [])
    m.append(n('B-2', 2, staccato=True))
    m.append(ch(['F3', 'A3', 'D4'], 4))           # Bbmaj7 LH
    m.append(n('A4', 6, tenuto=True))              # melody held - A (from Bb-A resolution)
    measures.append(m)

    # m74: Bdim7
    m = make_measure(74, [])
    m.append(n('B2', 3, staccato=True))
    m.append(n('F3', 1))
    m.append(ch(['A-3', 'B3', 'D4', 'F4'], 2))   # Bdim7
    m.append(n('B2', 2, staccato=True))
    m.append(ch(['D4', 'F4', 'A-4', 'B4'], 4))   # Bdim7 upper
    measures.append(m)

    # m75: Fmaj7/C
    m = make_measure(75, [])
    m.append(n('C3', 2, staccato=True))
    m.append(ch(['F3', 'E4', 'A4', 'C5'], 4))    # Fmaj7
    m.append(n('C3', 2, staccato=True))
    m.append(ch(['A4', 'C5', 'E5', 'F5'], 4))    # Fmaj7 very high
    measures.append(m)

    # m76: Dm7add11
    m = make_measure(76, [])
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['A3', 'C4', 'G4', 'A4'], 4))    # Dm11
    m.append(n('D3', 2, staccato=True))
    m.append(ch(['F4', 'G4', 'A4', 'C5'], 4))    # Dm11 upper
    measures.append(m)

    # m77: Gm9 - morendo
    m = make_measure(77, [])
    te3 = expressions.TextExpression('morendo')
    te3.style.fontStyle = 'italic'
    m.insert(0, te3)
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['D3', 'A3', 'B-3', 'F4'], 4))   # Gm9
    m.append(n('G2', 2, staccato=True))
    m.append(ch(['B-3', 'D4', 'F4', 'A4'], 4))   # Gm9 upper
    measures.append(m)

    # m78: C7sus4
    m = make_measure(78, [])
    m.append(n('C2', 2, staccato=True))
    m.append(ch(['G2', 'B-3', 'F4', 'G4'], 4))   # C7sus4
    m.append(ch(['C2', 'G2', 'B-3', 'F4', 'G4'], 6))  # C7sus4 held
    measures.append(m)

    # m79: Fmaj9 - ppp
    m = make_measure(79, [])
    m.insert(0, dynamics.Dynamic('ppp'))
    m.append(n('F2', 2, staccato=True))
    m.append(ch(['C3', 'E4', 'G4', 'A4'], 4))    # Fmaj9
    m.append(ch(['F2', 'C3', 'E4', 'G4', 'A4'], 6))  # Fmaj9 held
    measures.append(m)

    # m80: Fadd9 - FINAL - fermata - unresolved
    m = make_measure(80, [])
    final = ch(['F2', 'C3', 'A3', 'G4', 'A4', 'F5'], 12)
    final.expressions.append(expressions.Fermata())
    m.append(final)
    measures.append(m)

    return measures

def clarinet_section_V():
    measures = []

    for i in range(65, 72):
        m = make_measure(i, [r(12)])
        measures.append(m)

    # m72: whisper held note
    m = make_measure(72, [])
    m.insert(0, dynamics.Dynamic('pp'))
    m.append(n('G4', 12, tenuto=True))
    measures.append(m)

    # m73: gentle fade
    m = make_measure(73, [])
    m.append(n('G4', 6))
    m.append(r(6))
    measures.append(m)

    for i in range(74, 80):
        m = make_measure(i, [r(12)])
        measures.append(m)

    # m80: final with fermata
    m = make_measure(80, [])
    final_n = n('G4', 12, tenuto=True)
    final_n.expressions.append(expressions.Fermata())
    m.append(final_n)
    measures.append(m)

    return measures


# ============================================================
# ASSEMBLE
# ============================================================

cl_measures = (
    clarinet_section_I() +
    clarinet_section_II() +
    clarinet_section_III() +
    clarinet_section_IV() +
    clarinet_section_V()
)
for m in cl_measures:
    clarinet_part.append(m)

pn_measures = (
    piano_section_I() +
    piano_section_II() +
    piano_section_III() +
    piano_section_IV() +
    piano_section_V()
)
for m in pn_measures:
    piano_part.append(m)

# Hairpins - Piano (11)
def add_hairpin(part, start_measure, end_measure, htype='crescendo'):
    start_m = end_m = None
    for m in part.getElementsByClass(stream.Measure):
        if m.number == start_measure:
            start_m = m
        if m.number == end_measure:
            end_m = m
    if not start_m or not end_m:
        return
    sn = list(start_m.flatten().notesAndRests)
    en = list(end_m.flatten().notesAndRests)
    if not sn or not en:
        return
    sp = Crescendo(sn[0], en[-1]) if htype == 'crescendo' else Diminuendo(sn[0], en[-1])
    part.insert(0, sp)

add_hairpin(piano_part, 5, 7, 'crescendo')
add_hairpin(piano_part, 9, 11, 'crescendo')
add_hairpin(piano_part, 13, 15, 'crescendo')
add_hairpin(piano_part, 33, 36, 'crescendo')
add_hairpin(piano_part, 37, 40, 'diminuendo')
add_hairpin(piano_part, 41, 48, 'crescendo')
add_hairpin(piano_part, 49, 55, 'crescendo')
add_hairpin(piano_part, 57, 60, 'diminuendo')
add_hairpin(piano_part, 61, 64, 'diminuendo')
add_hairpin(piano_part, 65, 68, 'diminuendo')
add_hairpin(piano_part, 77, 80, 'diminuendo')

# Hairpins - Clarinet (7)
add_hairpin(clarinet_part, 21, 23, 'crescendo')
add_hairpin(clarinet_part, 25, 27, 'diminuendo')
add_hairpin(clarinet_part, 33, 36, 'crescendo')
add_hairpin(clarinet_part, 37, 40, 'diminuendo')
add_hairpin(clarinet_part, 41, 46, 'crescendo')
add_hairpin(clarinet_part, 49, 55, 'crescendo')
add_hairpin(clarinet_part, 56, 64, 'diminuendo')

# Assemble score
score.insert(0, clarinet_part)
score.insert(0, piano_part)

# Write
output_path = '/home/khaled/rachmaniclaude/experiment/007/track_01/score.musicxml'
score.write('musicxml', fp=output_path)
print(f"Score written to {output_path}")

# Validate
s = converter.parse(output_path)
print(f"Parsed: {len(s.parts)} parts, {len(list(s.flatten().getElementsByClass('Note')))} notes")
for i, part in enumerate(s.parts):
    measures = list(part.getElementsByClass(stream.Measure))
    notes = list(part.flatten().getElementsByClass('Note'))
    print(f"  Part {i} ({part.partName}): {len(measures)} measures, {len(notes)} notes")
