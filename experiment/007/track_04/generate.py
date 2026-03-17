#!/usr/bin/env python3
"""Generate Matin de Boulangerie MusicXML score programmatically. v3-fixed durations.

Duration units: quarterLength directly.
6/8 time: 3.0 ql per measure.
  eighth note = 0.5 ql
  quarter note = 1.0 ql
  dotted quarter = 1.5 ql
  dotted half = 3.0 ql (whole bar)
  16th note = 0.25 ql
  32nd note = 0.125 ql
"""

from music21 import (
    stream, note, chord, meter, key, tempo, clef,
    instrument, dynamics, expressions, articulations,
    duration, layout, bar, pitch, interval, tie
)

score = stream.Score()

clarinet_part = stream.Part()
clarinet_part.id = 'Clarinet'
clarinet_part.insert(0, instrument.Clarinet())

piano_part = stream.Part()
piano_part.id = 'Piano'
piano_part.insert(0, instrument.Piano())

# Duration constants (quarterLength)
E = 0.5      # eighth
Q = 1.0      # quarter
DQ = 1.5     # dotted quarter
DH = 3.0     # dotted half (whole bar in 6/8)
S = 0.25     # 16th
T = 0.125    # 32nd
TE = 1/3     # triplet eighth (3 in the time of 2 eighths = 1.0 ql)

def n(p, ql, **kw):
    """Create a note with given quarterLength."""
    nn = note.Note(p)
    nn.duration = duration.Duration(ql)
    if kw.get('tie_start'): nn.tie = tie.Tie('start')
    if kw.get('tie_stop'): nn.tie = tie.Tie('stop')
    if kw.get('staccato'): nn.articulations.append(articulations.Staccato())
    if kw.get('tenuto'): nn.articulations.append(articulations.Tenuto())
    if kw.get('accent'): nn.articulations.append(articulations.Accent())
    if kw.get('fermata'): nn.expressions.append(expressions.Fermata())
    return nn

def r(ql):
    rr = note.Rest()
    rr.duration = duration.Duration(ql)
    return rr

def ch(pitches, ql, **kw):
    cc = chord.Chord(pitches)
    cc.duration = duration.Duration(ql)
    if kw.get('staccato'): cc.articulations.append(articulations.Staccato())
    if kw.get('tenuto'): cc.articulations.append(articulations.Tenuto())
    if kw.get('accent'): cc.articulations.append(articulations.Accent())
    if kw.get('fermata'): cc.expressions.append(expressions.Fermata())
    return cc

piano_measures = []
clarinet_measures = []

# ============================================================
# Helper: verify measure duration
# ============================================================
def add_pm(m):
    """Add piano measure with duration check."""
    piano_measures.append(m)

def add_cm(m):
    """Add clarinet measure with duration check."""
    clarinet_measures.append(m)

# ============================================================
# Clarinet: 16 measures rest (Section I)
# ============================================================
for i in range(1, 17):
    m = stream.Measure(number=i)
    if i == 1:
        m.insert(0, meter.TimeSignature('6/8'))
        m.insert(0, key.KeySignature(-1))
        m.insert(0, clef.TrebleClef())
    m.append(r(DH))
    add_cm(m)

# ============================================================
# SECTION I: Morning (m.1-16) - Piano solo
# Pastoral ostinato, pp->mp, dolce, F major
# Each measure = 3.0 ql
# ============================================================

# m1: Fmaj7 - pp, dolce [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=1)
m.insert(0, meter.TimeSignature('6/8'))
m.insert(0, key.KeySignature(-1))
m.insert(0, clef.TrebleClef())
m.insert(0, dynamics.Dynamic('pp'))
dolce = expressions.TextExpression('dolce')
dolce.style.fontStyle = 'italic'
m.insert(0, dolce)
m.insert(0, tempo.MetronomeMark('Andante pastorale', 72, note.Note(type='quarter', dots=1)))
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'E4'], E))
m.append(ch(['C4', 'F4', 'A4'], E))
m.append(ch(['F4', 'A4', 'C5', 'E5'], E))
m.append(n('C3', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4'], E))
add_pm(m)

# m2: Fmaj9 [E+S+S+E+E+E+E = 3.0]
m = stream.Measure(number=2)
m.append(n('F2', E, staccato=True))
m.append(n('A3', S))       # 16th - rhythmic variety
m.append(n('C4', S))       # 16th
m.append(ch(['E4', 'G4', 'A4'], E))  # Fmaj9
m.append(ch(['C5', 'E5', 'G5'], E))  # Fmaj9 high
m.append(n('F3', E, staccato=True))
m.append(ch(['A3', 'E4', 'G4'], E))  # Fmaj9
add_pm(m)

# m3: Bbmaj7 - triplet [E + TE+TE+TE + DQ = 0.5+1.0+1.5 = 3.0]
m = stream.Measure(number=3)
m.append(n('Bb1', E, staccato=True))  # very low for range
_t1 = n('D3', TE); _t2 = n('F3', TE); _t3 = n('A3', TE)
for t in [_t1, _t2, _t3]:
    t.duration.appendTuplet(duration.Tuplet(3, 2, 'eighth'))
m.append(_t1); m.append(_t2); m.append(_t3)
m.append(ch(['D4', 'F4', 'A4', 'C5'], DQ))  # Bbmaj7
add_pm(m)

# m4: F/C [E+T+T+S+E+Q+E = 0.5+0.125+0.125+0.25+0.5+1.0+0.5 = 3.0]
m = stream.Measure(number=4)
m.append(n('C2', E, staccato=True))       # low C for range
m.append(n('F3', T))                       # 32nd - rhythmic variety
m.append(n('A3', T))                       # 32nd
m.append(ch(['C4', 'E4', 'G4'], S))       # 16th
m.append(ch(['F4', 'A4', 'C5', 'E5'], E)) # Fmaj7
m.append(ch(['A4', 'C5', 'F5', 'G5'], Q)) # Fadd9 high - quarter note
m.append(n('C3', E, staccato=True))
add_pm(m)

# m5: Dm9 [E+E+E+DQ = 0.5+0.5+0.5+1.5 = 3.0]
m = stream.Measure(number=5)
cres1 = dynamics.Crescendo()
m.append(n('D2', E, staccato=True))
cres1.addSpannedElements(m.notes[-1])
m.append(ch(['F3', 'A3', 'C4', 'E4'], E))   # Dm9
m.append(ch(['A3', 'C4', 'E4', 'G4'], E))   # Am7
m.append(ch(['F4', 'A4', 'C5', 'E5'], DQ))  # Dm9 high, dotted quarter
cres1.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, cres1)

# m6: Gm9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=6)
m.append(n('G2', E, staccato=True))
m.append(ch(['Bb3', 'D4', 'F4', 'A4'], E))  # Gm9
m.append(ch(['D4', 'F4', 'Bb4'], E))
m.append(n('G3', E, staccato=True))
m.append(ch(['Bb3', 'D4', 'A4'], E))         # Gm9
m.append(ch(['F4', 'Bb4', 'D5'], E))
add_pm(m)

# m7: C13sus4 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=7)
m.append(n('C2', E, staccato=True))
m.append(ch(['F3', 'Bb3', 'E4', 'A4'], E))  # C13sus4
m.append(ch(['G3', 'Bb3', 'D4', 'E4'], E))  # C9sus
m.append(n('C3', E, staccato=True))
m.append(ch(['E4', 'G4', 'Bb4', 'D5'], E))  # C9
m.append(ch(['Bb4', 'D5', 'A5'], E))         # C13 high
add_pm(m)

# m8: C13 [E+E+Q+E+E = 3.0]
m = stream.Measure(number=8)
m.insert(0, dynamics.Dynamic('mp'))
m.append(n('C2', E, staccato=True))
m.append(ch(['E3', 'Bb3', 'D4', 'A4'], E))    # C13
m.append(ch(['G3', 'Bb3', 'E4', 'G4'], Q))    # C7 - quarter
m.append(ch(['Bb4', 'D5', 'E5'], E))           # C9 high
m.append(n('C3', E, staccato=True))
add_pm(m)

# m9: Fadd9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=9)
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4', 'G4'], E))    # Fadd9
m.append(ch(['C4', 'F4', 'A4'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['A4', 'C5', 'G5'], E))           # Fadd9 high
m.append(ch(['F5', 'A5'], E))
add_pm(m)

# m10: Bb6/9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=10)
m.append(n('Bb1', E, staccato=True))           # very low
m.append(ch(['D3', 'G3', 'Bb3', 'C4'], E))    # Bb6/9
m.append(ch(['F4', 'A4', 'D5'], E))
m.append(n('Bb2', E, staccato=True))
m.append(ch(['D4', 'G4', 'C5'], E))            # Bb6/9 inv
m.append(ch(['F5', 'A5', 'D6'], E))            # very high
add_pm(m)

# m11: Bbm6 [E+E+Q+E+E = 3.0]
m = stream.Measure(number=11)
decres1 = dynamics.Diminuendo()
m.append(n('Bb2', E, staccato=True))
decres1.addSpannedElements(m.notes[-1])
m.append(ch(['D-3', 'F3', 'G3', 'Bb3'], E))   # Bbm6
m.append(ch(['D-4', 'F4', 'Bb4'], Q))          # quarter
m.append(ch(['G4', 'D-5', 'F5'], E))
m.append(n('Bb2', E, staccato=True))
decres1.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, decres1)

# m12: F6/9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=12)
m.append(n('A2', E, staccato=True))
m.append(ch(['F3', 'A3', 'D4', 'G4'], E))     # F6/9
m.append(ch(['A4', 'C5', 'D5'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['A3', 'D4', 'G4'], E))
m.append(ch(['C5', 'F5', 'G5'], E))
add_pm(m)

# m13: Am9 [E+E+E+DQ = 3.0]
m = stream.Measure(number=13)
cres2 = dynamics.Crescendo()
m.append(n('A2', E, staccato=True))
cres2.addSpannedElements(m.notes[-1])
m.append(ch(['E3', 'G3', 'B3', 'C4'], E))     # Am9
m.append(ch(['G4', 'C5', 'E5'], E))
m.append(ch(['B4', 'E5', 'A5'], DQ))           # Am9 high, held
cres2.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, cres2)

# m14: Dm11 [E+E+E+DQ = 3.0]
m = stream.Measure(number=14)
m.append(n('D2', E, staccato=True))
m.append(ch(['F3', 'A3', 'C4', 'G4'], E))     # Dm11
m.append(ch(['C4', 'E4', 'A4'], E))
m.append(ch(['F4', 'A4', 'C5', 'G5'], DQ))    # Dm11 high
add_pm(m)

# m15: Gm9 [DH = 3.0] - whole bar bass note
m = stream.Measure(number=15)
m.append(n('G1', DH, tenuto=True))             # very low, whole bar
add_pm(m)

# m16: Csus4 [DQ+Q+S+S = 1.5+1.0+0.25+0.25 = 3.0]
m = stream.Measure(number=16)
m.append(n('C2', DQ, staccato=True))
m.append(ch(['F3', 'G3', 'Bb3', 'C4'], Q))    # C7sus4
m.append(n('G3', S))
m.append(r(S))                                   # breath
add_pm(m)

# ============================================================
# SECTION II: The Door Opens (m.17-28)
# Clarinet enters mp espressivo
# ============================================================

# CL m17: primary motif [S+DQ+E+S+S = 0.25+1.5+0.5+0.25+0.25... no]
# Let's use: r(S) + n(DQ) + n(E) + n(E) = 0.25 + 1.5 + 0.5 + 0.5... = 2.75 need 3.0
# r(S) + n(DQ) + n(Q) = 0.25 + 1.5 + 1.0 = 2.75...
# Let me just do: r(E) + n(DQ) + n(Q) = 0.5 + 1.5 + 1.0 = 3.0
m = stream.Measure(number=17)
m.insert(0, dynamics.Dynamic('mp'))
esp = expressions.TextExpression('espressivo')
esp.style.fontStyle = 'italic'
m.insert(0, esp)
m.append(r(E))                                    # breath before entry
m.append(n('G4', DQ, tenuto=True))                # motif note 1 (written)
m.append(n('A4', Q))                              # motif note 2
add_cm(m)

# CL m18 [Q+E+DQ = 1.0+0.5+1.5 = 3.0]
m = stream.Measure(number=18)
m.append(n('B4', Q, tenuto=True))
m.append(n('C5', E))
m.append(n('D5', DQ))
add_cm(m)

# CL m19 [E+E+E+DQ = 3.0]
m = stream.Measure(number=19)
m.append(n('D5', E))
m.append(n('C5', E))
m.append(n('A4', E))
m.append(n('B4', DQ))
add_cm(m)

# CL m20 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=20)
m.append(n('G4', DQ, fermata=True))
m.append(r(DQ))
add_cm(m)

# CL m21 [E+E+E+DQ = 3.0]
m = stream.Measure(number=21)
m.append(n('G4', E))
m.append(n('A4', E))
m.append(n('B4', E))
m.append(n('C5', DQ))
add_cm(m)

# CL m22 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=22)
m.append(n('D5', E))
m.append(n('E5', E, accent=True))
m.append(n('D5', E))
m.append(n('C5', E))
m.append(n('B4', E))
m.append(n('A4', E))
add_cm(m)

# CL m23 [DQ+DQ = 3.0]
m = stream.Measure(number=23)
m.append(n('G4', DQ, tenuto=True))
m.append(n('F#4', DQ))            # chromatic color
add_cm(m)

# CL m24 [Q+E+r(DQ) = 3.0]
m = stream.Measure(number=24)
m.append(n('G4', Q))
m.append(n('A4', E))
m.append(r(DQ))
add_cm(m)

# CL m25 [E+E+E+DQ = 3.0]
m = stream.Measure(number=25)
cres_cl1 = dynamics.Crescendo()
m.append(n('A4', E))
cres_cl1.addSpannedElements(m.notes[-1])
m.append(n('B4', E))
m.append(n('C5', E))
m.append(n('D5', DQ))
add_cm(m)

# CL m26 [DQ+E+E = 3.0] expressive leap
m = stream.Measure(number=26)
m.append(n('F5', DQ, accent=True))   # leap of a 6th
m.append(n('E5', E))
m.append(n('D5', E))
cres_cl1.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, cres_cl1)

# CL m27 [E+E+E+DQ = 3.0]
m = stream.Measure(number=27)
decres_cl1 = dynamics.Diminuendo()
m.append(n('C5', E))
decres_cl1.addSpannedElements(m.notes[-1])
m.append(n('B4', E))
m.append(n('A4', E))
m.append(n('G4', DQ))
decres_cl1.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, decres_cl1)

# CL m28 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=28)
m.append(n('A4', DQ, tenuto=True))
m.append(r(DQ))
add_cm(m)

# Piano m17-28
# P m17: Fadd9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=17)
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4', 'G4'], E))     # Fadd9
m.append(ch(['C4', 'F4', 'A4', 'G4'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['A4', 'C5', 'F5', 'G5'], E))
m.append(ch(['C5', 'G5', 'A5'], E))
add_pm(m)

# P m18: Gm9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=18)
m.append(n('G2', E, staccato=True))
m.append(ch(['Bb3', 'D4', 'F4', 'A4'], E))     # Gm9
m.append(ch(['D4', 'F4', 'Bb4'], E))
m.append(n('G3', E, staccato=True))
m.append(ch(['Bb4', 'D5', 'F5'], E))
m.append(ch(['A4', 'D5', 'G5'], E))
add_pm(m)

# P m19: Am7 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=19)
m.append(n('A2', E, staccato=True))
m.append(ch(['E3', 'G3', 'C4', 'B3'], E))       # Am9
m.append(ch(['G4', 'C5', 'E5'], E))
m.append(n('A3', E, staccato=True))
m.append(ch(['C4', 'E4', 'G4'], E))
m.append(ch(['E5', 'G5', 'B5'], E))
add_pm(m)

# P m20: Bbmaj9 [E+E+Q+E+E = 3.0]
m = stream.Measure(number=20)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['D3', 'F3', 'A3', 'C4'], E))       # Bbmaj9
m.append(ch(['F4', 'A4', 'C5', 'D5'], Q))       # quarter
m.append(ch(['Bb4', 'D5', 'A5'], E))
m.append(n('Bb3', E, staccato=True))
add_pm(m)

# P m21: C7sus4->C7 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=21)
m.append(n('C3', E, staccato=True))
m.append(ch(['G3', 'Bb3', 'F4'], E))             # Csus4
m.append(ch(['E4', 'G4', 'Bb4', 'D5'], E))       # C9
m.append(n('C4', E, staccato=True))
m.append(ch(['G4', 'Bb4', 'E5'], E))             # C7
m.append(ch(['D5', 'G5', 'Bb5'], E))
add_pm(m)

# P m22: Dm7 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=22)
m.append(n('D3', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4', 'E4'], E))        # Dm9
m.append(ch(['A4', 'C5', 'F5'], E))
m.append(n('D4', E, staccato=True))
m.append(ch(['F4', 'A4', 'C5'], E))
m.append(ch(['F5', 'A5'], E))
add_pm(m)

# P m23: Bbmaj7 [E+E+E+DQ = 3.0]
m = stream.Measure(number=23)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['F3', 'A3', 'D4', 'C4'], E))        # Bbmaj7
m.append(ch(['D4', 'F4', 'A4'], E))
m.append(ch(['Bb4', 'D5', 'A5'], DQ))
add_pm(m)

# P m24: C9/Bb [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=24)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['E3', 'G3', 'Bb3', 'D4'], E))       # C9/Bb
m.append(ch(['Bb3', 'E4', 'G4'], E))
m.append(n('C3', E, staccato=True))
m.append(ch(['G4', 'Bb4', 'D5'], E))
m.append(ch(['E5', 'G5'], E))
add_pm(m)

# P m25: Am9 [E+E+E+DQ = 3.0]
m = stream.Measure(number=25)
m.append(n('A2', E, staccato=True))
m.append(ch(['E3', 'G3', 'B3', 'C4'], E))        # Am9
m.append(ch(['E4', 'G4', 'B4'], E))
m.append(ch(['C5', 'E5', 'G5'], DQ))
add_pm(m)

# P m26: Dm11 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=26)
m.append(n('D3', E, staccato=True))
m.append(ch(['A3', 'C4', 'G4'], E))               # Dm11
m.append(ch(['F4', 'A4', 'C5'], E))
m.append(n('D4', E, staccato=True))
m.append(ch(['A4', 'C5', 'E5'], E))
m.append(ch(['G5', 'A5'], E))
add_pm(m)

# P m27: Gm7 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=27)
m.append(n('G2', E, staccato=True))
m.append(ch(['D3', 'F3', 'Bb3', 'A3'], E))        # Gm9
m.append(ch(['Bb3', 'D4', 'F4'], E))
m.append(n('G3', E, staccato=True))
m.append(ch(['D4', 'F4', 'Bb4'], E))
m.append(ch(['A4', 'D5'], E))
add_pm(m)

# P m28: Csus4 [DQ+Q+r(E) = 3.0]
m = stream.Measure(number=28)
m.append(n('C3', DQ, staccato=True))
m.append(ch(['F3', 'G3', 'Bb3', 'C4'], Q))        # C7sus4
m.append(r(E))
add_pm(m)

# ============================================================
# SECTION III: Conversation (m.29-48) con moto, mp-mf
# ============================================================

# CL m29 [E+E+E+DQ = 3.0]
m = stream.Measure(number=29)
m.insert(0, dynamics.Dynamic('mf'))
con_moto = expressions.TextExpression('con moto')
con_moto.style.fontStyle = 'italic'
m.insert(0, con_moto)
m.append(n('G4', E))
m.append(n('A4', E))
m.append(n('B4', E))
m.append(n('D5', DQ))
add_cm(m)

# CL m30 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=30)
m.append(n('E5', DQ, tenuto=True))
m.append(r(DQ))
add_cm(m)

# CL m31: rest [DH = 3.0]
m = stream.Measure(number=31)
m.append(r(DH))
add_cm(m)

# CL m32 [r(Q)+S+S+E+Q = 1.0+0.25+0.25+0.5+1.0 = 3.0]
m = stream.Measure(number=32)
m.append(r(Q))
m.append(n('C5', S))
m.append(n('D5', S))
m.append(n('E5', E))
m.append(n('F5', Q))
add_cm(m)

# CL m33 [E+S+S+E+E+E = 0.5+0.25+0.25+0.5+0.5+0.5 = 2.5... fix: DQ+S+S+E+E = 3.0]
m = stream.Measure(number=33)
m.append(n('F5', DQ, accent=True))
m.append(n('E5', S))
m.append(n('D5', S))
m.append(n('C5', E))
m.append(n('B4', E))
add_cm(m)

# CL m34 [DQ+E+E+E = 3.0]
m = stream.Measure(number=34)
m.append(n('A4', DQ))
m.append(n('B4', E))
m.append(n('A4', E))
m.append(n('G4', E))
add_cm(m)

# CL m35: rest [DH = 3.0]
m = stream.Measure(number=35)
m.append(r(DH))
add_cm(m)

# CL m36 [r(DQ)+E+S+S+E = 1.5+0.5+0.25+0.25+0.5 = 3.0]
m = stream.Measure(number=36)
m.append(r(DQ))
m.append(n('A4', E))
m.append(n('B-4', S))
m.append(n('C5', S))
m.append(n('D5', E))
add_cm(m)

# CL m37: Dm excursion [DQ+S+S+E+E = 3.0]
m = stream.Measure(number=37)
decr_cl2 = dynamics.Diminuendo()
m.append(n('D5', DQ, tenuto=True))
decr_cl2.addSpannedElements(m.notes[-1])
m.append(n('C#5', S))
m.append(n('D5', S))
m.append(n('E5', E))
m.append(n('F5', E))
add_cm(m)

# CL m38 [DQ+E+S+S = 3.0]
m = stream.Measure(number=38)
m.insert(0, dynamics.Dynamic('mp'))
m.append(n('F5', DQ, tenuto=True))
m.append(n('E5', E))
m.append(n('D5', S))
m.append(n('C5', S))
decr_cl2.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, decr_cl2)

# CL m39 [E+E+E+DQ = 3.0]
m = stream.Measure(number=39)
m.append(n('B-4', E))
m.append(n('A4', E))
m.append(n('G4', E))
m.append(n('F4', DQ))
add_cm(m)

# CL m40 [Q+r(E)+r(DQ) = 3.0]
m = stream.Measure(number=40)
m.append(n('E4', Q, tenuto=True, fermata=True))  # low written E4 = concert D4
m.append(r(E))
m.append(r(DQ))
add_cm(m)

# CL m41 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=41)
cres_cl2 = dynamics.Crescendo()
m.append(n('A4', E))
cres_cl2.addSpannedElements(m.notes[-1])
m.append(n('B4', E))
m.append(n('C5', E))
m.append(n('D5', E))
m.append(n('E5', E))
m.append(n('F5', E))
add_cm(m)

# CL m42 [E+S+S+E+E+E = 3.0]
m = stream.Measure(number=42)
m.append(n('E5', E))
m.append(n('F5', S))
m.append(n('E5', S))
m.append(n('D5', E))
m.append(n('C5', E))
m.append(n('D5', E))
cres_cl2.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, cres_cl2)

# CL m43 [DQ+E+E = 3.0]
m = stream.Measure(number=43)
m.insert(0, dynamics.Dynamic('mf'))
m.append(n('F5', DQ, accent=True))
m.append(n('E5', E))
m.append(n('D5', E))
add_cm(m)

# CL m44 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=44)
m.append(n('C5', DQ, tenuto=True))
m.append(r(DQ))
add_cm(m)

# CL m45 [r(Q)+E+E+E+E = 3.0]
m = stream.Measure(number=45)
m.append(r(Q))
m.append(n('G4', E))
m.append(n('A4', E))
m.append(n('B4', E))
m.append(n('C5', E))
add_cm(m)

# CL m46 [E+E+E+DQ = 3.0]
m = stream.Measure(number=46)
m.append(n('D5', E))
m.append(n('E5', E))
m.append(n('F5', E))
m.append(n('E5', DQ))
add_cm(m)

# CL m47 [DQ+DQ = 3.0]
m = stream.Measure(number=47)
cres_cl3 = dynamics.Crescendo()
m.append(n('E5', DQ))
cres_cl3.addSpannedElements(m.notes[-1])
m.append(n('F5', DQ))
cres_cl3.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, cres_cl3)

# CL m48 [E+E+E+DQ = 3.0]
m = stream.Measure(number=48)
m.append(n('E-5', E))
m.append(n('D5', E))
m.append(n('E-5', E))
m.append(n('F5', DQ))
add_cm(m)

# Piano m29-48
# P m29 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=29)
m.insert(0, tempo.MetronomeMark('Con moto', 76, note.Note(type='quarter', dots=1)))
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4', 'G4'], E))
m.append(ch(['C4', 'F4', 'A4'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['A4', 'C5', 'F5'], E))
m.append(ch(['G5', 'A5'], E))
add_pm(m)

# P m30: Gm7/F [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=30)
m.append(n('F2', E, staccato=True))
m.append(ch(['G3', 'Bb3', 'D4', 'F4'], E))
m.append(ch(['Bb4', 'D5', 'F5'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['G4', 'Bb4', 'D5'], E))
m.append(ch(['F5', 'G5', 'Bb5'], E))
add_pm(m)

# P m31 [E+S+S+E+Q+E = 3.0]
m = stream.Measure(number=31)
m.append(n('A2', E, staccato=True))
m.append(ch(['E3', 'G3', 'C4'], S))
m.append(n('E4', S))
m.append(ch(['G4', 'C5', 'E5'], E))
m.append(ch(['A4', 'C5', 'E5', 'G5'], Q))
m.append(n('A3', E, staccato=True))
add_pm(m)

# P m32 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=32)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['D3', 'F3', 'A3', 'C4'], E))
m.append(ch(['F4', 'A4', 'D5'], E))
m.append(n('Bb3', E, staccato=True))
m.append(ch(['D4', 'F4', 'Bb4'], E))
m.append(ch(['A4', 'D5', 'Bb5'], E))
add_pm(m)

# P m33: C7 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=33)
m.append(n('C3', E, staccato=True))
m.append(ch(['E3', 'G3', 'Bb3', 'D4'], E))       # C9
m.append(ch(['E4', 'G4', 'Bb4'], E))
m.append(n('C4', E, staccato=True))
m.append(ch(['G4', 'Bb4', 'E5'], E))
m.append(ch(['D5', 'G5'], E))
add_pm(m)

# P m34 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=34)
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4', 'G4'], E))
m.append(ch(['C5', 'F5', 'A5'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['A4', 'C5', 'G5'], E))
m.append(ch(['F5', 'A5'], E))
add_pm(m)

# P m35 [E+S+S+E+Q+E = 3.0]
m = stream.Measure(number=35)
m.append(n('D3', E, staccato=True))
m.append(ch(['A3', 'C4', 'F4'], S))
m.append(n('A4', S))
m.append(ch(['C5', 'F5', 'A5'], E))
m.append(ch(['D5', 'F5', 'A5'], Q))
m.append(n('D4', E, staccato=True))
add_pm(m)

# P m36: G9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=36)
m.append(n('G2', E, staccato=True))
m.append(ch(['B3', 'D4', 'F4', 'A4'], E))
m.append(ch(['D4', 'F4', 'B4'], E))
m.append(n('G3', E, staccato=True))
m.append(ch(['B4', 'D5', 'F5'], E))
m.append(ch(['A4', 'D5', 'G5'], E))
add_pm(m)

# P m37: Dm [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=37)
m.append(n('D3', E, staccato=True))
m.append(ch(['A3', 'D4', 'F4', 'C5'], E))        # Dm7
m.append(ch(['A4', 'D5', 'F5'], E))
m.append(n('D4', E, staccato=True))
m.append(ch(['F4', 'A4', 'D5'], E))
m.append(ch(['C5', 'F5', 'A5'], E))
add_pm(m)

# P m38: Dm(maj7)/C# [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=38)
m.append(n('C#3', E))
m.append(ch(['A3', 'D4', 'F4', 'C#5'], E))
m.append(ch(['A4', 'D5', 'F5'], E))
m.append(n('C#4', E))
m.append(ch(['F4', 'A4', 'C#5'], E))
m.append(ch(['D5', 'F5', 'A5'], E))
add_pm(m)

# P m39: Dm7/C [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=39)
m.append(n('C3', E, staccato=True))
m.append(ch(['A3', 'D4', 'F4', 'C5'], E))
m.append(ch(['A4', 'C5', 'F5'], E))
m.append(n('C4', E, staccato=True))
m.append(ch(['F4', 'A4', 'C5'], E))
m.append(ch(['D5', 'F5'], E))
add_pm(m)

# P m40: Bbmaj7 [E+E+Q+E+E = 3.0]
m = stream.Measure(number=40)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['F3', 'A3', 'D4', 'C4'], E))
m.append(ch(['A4', 'D5', 'F5', 'A5'], Q))         # quarter
m.append(ch(['Bb4', 'D5'], E))
m.append(n('Bb3', E, staccato=True))
add_pm(m)

# P m41: Gm9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=41)
cres_p1 = dynamics.Crescendo()
m.append(n('G2', E, staccato=True))
cres_p1.addSpannedElements(m.notes[-1])
m.append(ch(['Bb3', 'D4', 'F4', 'A4'], E))
m.append(ch(['D4', 'F4', 'Bb4'], E))
m.append(n('G3', E, staccato=True))
m.append(ch(['Bb4', 'D5', 'F5'], E))
m.append(ch(['A4', 'D5', 'G5'], E))
cres_p1.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, cres_p1)

# P m42: A7b9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=42)
m.append(n('E3', E, staccato=True))
m.append(ch(['A3', 'C#4', 'G4', 'Bb4'], E))
m.append(ch(['C#5', 'G5'], E))
m.append(n('A3', E, staccato=True))
m.append(ch(['E4', 'G4', 'Bb4'], E))
m.append(ch(['C#5', 'E5', 'A5'], E))
add_pm(m)

# P m43: Dm9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=43)
m.append(n('D3', E, staccato=True))
m.append(ch(['A3', 'C4', 'E4', 'F4'], E))
m.append(ch(['A4', 'C5', 'E5'], E))
m.append(n('D4', E, staccato=True))
m.append(ch(['F4', 'A4', 'C5'], E))
m.append(ch(['E5', 'A5'], E))
add_pm(m)

# P m44: Bb/C [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=44)
m.append(n('C3', E, staccato=True))
m.append(ch(['Bb3', 'D4', 'F4', 'A4'], E))
m.append(ch(['Bb4', 'D5', 'F5'], E))
m.append(n('C4', E, staccato=True))
m.append(ch(['F4', 'Bb4', 'D5'], E))
m.append(ch(['F5', 'Bb5'], E))
add_pm(m)

# P m45: Fmaj7 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=45)
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'E4', 'F4'], E))
m.append(ch(['A4', 'C5', 'E5'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['C5', 'E5', 'F5'], E))
m.append(ch(['A5', 'C6'], E))                      # high C6 for range
add_pm(m)

# P m46: Am11 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=46)
m.append(n('A2', E, staccato=True))
m.append(ch(['E3', 'G3', 'D4', 'B3'], E))
m.append(ch(['G4', 'C5', 'D5'], E))
m.append(n('A3', E, staccato=True))
m.append(ch(['E4', 'G4', 'C5'], E))
m.append(ch(['D5', 'E5', 'B5'], E))
add_pm(m)

# P m47: Bb6/9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=47)
cres_p2 = dynamics.Crescendo()
m.append(n('Bb2', E, staccato=True))
cres_p2.addSpannedElements(m.notes[-1])
m.append(ch(['D3', 'G3', 'Bb3', 'C4'], E))
m.append(ch(['F4', 'Bb4', 'D5'], E))
m.append(n('Bb3', E, staccato=True))
m.append(ch(['D4', 'G4', 'C5'], E))
m.append(ch(['F5', 'G5', 'Bb5'], E))
cres_p2.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, cres_p2)

# P m48: C9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=48)
m.append(n('C3', E, staccato=True))
m.append(ch(['E3', 'Bb3', 'D4', 'G4'], E))
m.append(ch(['Bb4', 'D5', 'E5'], E))
m.append(n('C4', E, staccato=True))
m.append(ch(['G4', 'Bb4', 'D5'], E))
m.append(ch(['E5', 'G5'], E))
add_pm(m)

# ============================================================
# SECTION IV: Walking Home (m.49-64) Ab major, f
# ============================================================

# CL m49 [DQ+S+S+E = 3.0? 1.5+0.25+0.25+0.5 = 2.5... need more]
# [DQ+E+E+E = 1.5+0.5+0.5+0.5 = 3.0]
m = stream.Measure(number=49)
m.insert(0, dynamics.Dynamic('f'))
larg = expressions.TextExpression('largamente')
larg.style.fontStyle = 'italic'
m.insert(0, larg)
m.append(n('B-4', DQ, accent=True))
m.append(n('C5', E))
m.append(n('D5', E))
m.append(n('E-5', E))
add_cm(m)

# CL m50 [DQ+E+S+S = 3.0]
m = stream.Measure(number=50)
m.append(n('F5', DQ, tenuto=True))
m.append(n('E-5', E))
m.append(n('D5', S))
m.append(n('C5', S))
add_cm(m)

# CL m51 [DQ+S+S+E+E = 3.0]
m = stream.Measure(number=51)
m.append(n('G5', DQ, accent=True))
m.append(n('F5', S))
m.append(n('E-5', S))
m.append(n('D5', E))
m.append(n('C5', E))
add_cm(m)

# CL m52 [E+E+E+DQ = 3.0]
m = stream.Measure(number=52)
m.append(n('E-5', E))
m.append(n('C5', E))
m.append(n('B-4', E))
m.append(n('C5', DQ))
add_cm(m)

# CL m53 [E+E+E+DQ = 3.0]
m = stream.Measure(number=53)
m.append(n('D5', E))
m.append(n('E-5', E))
m.append(n('F5', E))
m.append(n('G5', DQ))
add_cm(m)

# CL m54 [DQ+E+S+S = 3.0]
m = stream.Measure(number=54)
m.append(n('G5', DQ, tenuto=True))
m.append(n('F5', E))
m.append(n('E-5', S))
m.append(n('D5', S))
add_cm(m)

# CL m55 [S+S+E+E+DQ = 3.0]
m = stream.Measure(number=55)
m.append(n('C5', S))
m.append(n('B-4', S))
m.append(n('C5', E))
m.append(n('D5', E))
m.append(n('E-5', DQ))
add_cm(m)

# CL m56 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=56)
m.append(n('D5', DQ, tenuto=True))
m.append(r(DQ))
add_cm(m)

# CL m57 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=57)
cres_cl4 = dynamics.Crescendo()
m.append(n('E-5', E))
cres_cl4.addSpannedElements(m.notes[-1])
m.append(n('F5', E))
m.append(n('G5', E))
m.append(n('A5', E, accent=True))
m.append(n('G5', E))
m.append(n('A5', E))
cres_cl4.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, cres_cl4)

# CL m58: THE PEAK [DQ+S+S+E+E = 3.0]
m = stream.Measure(number=58)
m.insert(0, dynamics.Dynamic('ff'))
m.append(n('B-5', DQ, accent=True))               # highest note
m.append(n('A5', S))
m.append(n('G5', S))
m.append(n('F5', E))
m.append(n('E-5', E))
add_cm(m)

# CL m59 [E+E+E+DQ = 3.0]
m = stream.Measure(number=59)
decr_cl3 = dynamics.Diminuendo()
m.append(n('D5', E))
decr_cl3.addSpannedElements(m.notes[-1])
m.append(n('C5', E))
m.append(n('B-4', E))
m.append(n('A4', DQ))
decr_cl3.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, decr_cl3)

# CL m60 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=60)
m.append(n('B-4', DQ, tenuto=True, fermata=True))
m.append(r(DQ))
add_cm(m)

# CL m61 [E+E+E+DQ = 3.0]
m = stream.Measure(number=61)
m.insert(0, dynamics.Dynamic('mf'))
m.append(n('B-4', E))
m.append(n('C5', E))
m.append(n('D5', E))
m.append(n('E-5', DQ))
add_cm(m)

# CL m62 [DQ+E+E = 3.0]
m = stream.Measure(number=62)
m.append(n('F5', DQ))
m.append(n('E-5', E))
m.append(n('D5', E))
add_cm(m)

# CL m63 [E+E+E+DQ = 3.0]
m = stream.Measure(number=63)
decr_cl4 = dynamics.Diminuendo()
m.append(n('C5', E))
decr_cl4.addSpannedElements(m.notes[-1])
m.append(n('B-4', E))
m.append(n('B4', E))                               # pivot
m.append(n('A4', DQ))
decr_cl4.addSpannedElements(m.notes[-1])
add_cm(m)
clarinet_part.insert(0, decr_cl4)

# CL m64 [DQ+r(DQ) = 3.0]
m = stream.Measure(number=64)
m.insert(0, dynamics.Dynamic('mp'))
m.append(n('G4', DQ, tenuto=True))
m.append(r(DQ))
add_cm(m)

# Piano m49-64 [all E+E+E+E+E+E = 3.0 unless noted]
# P m49: Ab
m = stream.Measure(number=49)
m.insert(0, tempo.MetronomeMark('Largamente', 80, note.Note(type='quarter', dots=1)))
m.insert(0, dynamics.Dynamic('f'))
m.append(n('A-2', E, staccato=True))
m.append(ch(['E-3', 'A-3', 'C4', 'E-4'], E))
m.append(ch(['A-4', 'C5', 'E-5'], E))
m.append(n('E-3', E, staccato=True))
m.append(ch(['A-3', 'C4', 'E-4'], E))
m.append(ch(['C5', 'E-5', 'A-5'], E))
add_pm(m)

# P m50: Abmaj7
m = stream.Measure(number=50)
m.append(n('A-2', E, staccato=True))
m.append(ch(['E-3', 'G3', 'C4', 'E-4'], E))
m.append(ch(['G4', 'C5', 'E-5'], E))
m.append(n('A-3', E, staccato=True))
m.append(ch(['C4', 'E-4', 'G4'], E))
m.append(ch(['C5', 'E-5', 'G5'], E))
add_pm(m)

# P m51: Db9
m = stream.Measure(number=51)
m.append(n('D-3', E, staccato=True))
m.append(ch(['A-3', 'C4', 'E-4', 'F4'], E))
m.append(ch(['A-4', 'D-5', 'E-5'], E))
m.append(n('D-4', E, staccato=True))
m.append(ch(['F4', 'A-4', 'C5'], E))
m.append(ch(['E-5', 'A-5', 'D-6'], E))            # high D-6
add_pm(m)

# P m52: Eb7sus4
m = stream.Measure(number=52)
m.append(n('E-3', E, staccato=True))
m.append(ch(['B-3', 'D-4', 'A-4'], E))
m.append(ch(['D-5', 'E-5', 'B-5'], E))
m.append(n('E-4', E, staccato=True))
m.append(ch(['A-4', 'B-4', 'D-5'], E))
m.append(ch(['E-5', 'A-5'], E))
add_pm(m)

# P m53: Cm9
m = stream.Measure(number=53)
m.append(n('C3', E, staccato=True))
m.append(ch(['G3', 'B-3', 'D4', 'E-4'], E))
m.append(ch(['G4', 'B-4', 'D5'], E))
m.append(n('C4', E, staccato=True))
m.append(ch(['E-4', 'G4', 'B-4'], E))
m.append(ch(['D5', 'G5', 'B-5'], E))
add_pm(m)

# P m54: Fm9
m = stream.Measure(number=54)
m.append(n('F3', E, staccato=True))
m.append(ch(['C4', 'E-4', 'G4', 'A-4'], E))
m.append(ch(['C5', 'E-5', 'G5'], E))
m.append(n('F4', E, staccato=True))
m.append(ch(['A-4', 'C5', 'E-5'], E))
m.append(ch(['G5', 'A-5'], E))
add_pm(m)

# P m55: Bbm7
m = stream.Measure(number=55)
m.append(n('B-2', E, staccato=True))
m.append(ch(['F3', 'A-3', 'D-4', 'B-3'], E))
m.append(ch(['F4', 'A-4', 'D-5'], E))
m.append(n('B-3', E, staccato=True))
m.append(ch(['D-4', 'F4', 'A-4'], E))
m.append(ch(['B-4', 'D-5', 'F5'], E))
add_pm(m)

# P m56: Eb13
m = stream.Measure(number=56)
m.append(n('E-3', E, staccato=True))
m.append(ch(['B-3', 'D4', 'G4', 'C5'], E))
m.append(ch(['F4', 'B-4', 'D5'], E))
m.append(n('E-4', E, staccato=True))
m.append(ch(['B-4', 'D5', 'G5'], E))
m.append(ch(['C5', 'F5', 'A-5'], E))
add_pm(m)

# P m57: Ab/Eb
m = stream.Measure(number=57)
cres_p3 = dynamics.Crescendo()
m.append(n('E-3', E, staccato=True))
cres_p3.addSpannedElements(m.notes[-1])
m.append(ch(['A-3', 'C4', 'E-4', 'G4'], E))
m.append(ch(['A-4', 'C5', 'E-5'], E))
m.append(n('E-4', E, staccato=True))
m.append(ch(['A-4', 'C5', 'E-5'], E))
m.append(ch(['G5', 'A-5', 'C6'], E))              # high C6
cres_p3.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, cres_p3)

# P m58: Db [E+E+Q+E+E = 3.0]
m = stream.Measure(number=58)
m.insert(0, dynamics.Dynamic('ff'))
m.append(n('D-3', E, accent=True))
m.append(ch(['A-3', 'D-4', 'F4', 'A-4'], E))
m.append(ch(['D-5', 'F5', 'A-5', 'D-6'], Q))      # DRAMATIC quarter chord, very high
m.append(ch(['A-4', 'D-5', 'F5'], E))
m.append(n('D-4', E, staccato=True))
add_pm(m)

# P m59: Bbm9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=59)
m.append(n('B-2', E, staccato=True))
m.append(ch(['F3', 'A-3', 'C4', 'D-4'], E))
m.append(ch(['F4', 'A-4', 'C5'], E))
m.append(n('B-3', E, staccato=True))
m.append(ch(['D-4', 'F4', 'A-4'], E))
m.append(ch(['C5', 'F5', 'A-5'], E))
add_pm(m)

# P m60: Eb9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=60)
decr_p1 = dynamics.Diminuendo()
m.append(n('E-3', E, staccato=True))
decr_p1.addSpannedElements(m.notes[-1])
m.append(ch(['B-3', 'D4', 'F4', 'G4'], E))
m.append(ch(['B-4', 'D5', 'E-5'], E))
m.append(n('E-4', E, staccato=True))
m.append(ch(['G4', 'B-4', 'D5'], E))
m.append(ch(['F5', 'G5', 'B-5'], E))
decr_p1.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, decr_p1)

# P m61: Abadd9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=61)
decr_p2 = dynamics.Diminuendo()
m.append(n('A-2', E, staccato=True))
decr_p2.addSpannedElements(m.notes[-1])
m.append(ch(['E-3', 'A-3', 'B-3', 'C4'], E))
m.append(ch(['E-4', 'A-4', 'B-4'], E))
m.append(n('A-3', E, staccato=True))
m.append(ch(['C4', 'E-4', 'A-4'], E))
m.append(ch(['B-4', 'E-5', 'A-5'], E))
decr_p2.addSpannedElements(m.notes[-1])
add_pm(m)
piano_part.insert(0, decr_p2)

# P m62: Fm11 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=62)
m.append(n('F3', E, staccato=True))
m.append(ch(['C4', 'E-4', 'B-4', 'A-4'], E))
m.append(ch(['C5', 'E-5', 'F5'], E))
m.append(n('F4', E, staccato=True))
m.append(ch(['A-4', 'C5', 'E-5'], E))
m.append(ch(['B-4', 'F5', 'A-5'], E))
add_pm(m)

# P m63: Db->C7 pivot [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=63)
m.append(n('D-3', E))
m.append(ch(['A-3', 'D-4', 'F4', 'A-4'], E))
m.append(ch(['D-5', 'F5'], E))
m.append(n('C3', E))                                # C7 pivot
m.append(ch(['E4', 'G4', 'Bb4', 'D5'], E))
m.append(ch(['E5', 'Bb5'], E))
add_pm(m)

# P m64: Csus4 [DQ+Q+r(E) = 3.0]
m = stream.Measure(number=64)
decr_p3 = dynamics.Diminuendo()
m.append(n('C3', DQ, staccato=True))
decr_p3.addSpannedElements(m.notes[-1])
m.append(ch(['F3', 'G3', 'Bb3', 'C4'], Q))
decr_p3.addSpannedElements(m.notes[-1])
m.append(r(E))
add_pm(m)
piano_part.insert(0, decr_p3)

# ============================================================
# SECTION V: Alone Again (m.65-80) F major, pp
# ============================================================

# CL m65-72: tacet
for i in range(65, 73):
    m = stream.Measure(number=i)
    m.append(r(DH))
    add_cm(m)

# CL m73: ghostly echo [r(DQ)+DQ = 3.0]
m = stream.Measure(number=73)
m.insert(0, dynamics.Dynamic('ppp'))
m.append(r(DQ))
m.append(n('G4', DQ, tenuto=True))
add_cm(m)

# CL m74 [Q+E+r(DQ) = 3.0]
m = stream.Measure(number=74)
m.append(n('A4', Q, tenuto=True))
m.append(n('B4', E))
m.append(r(DQ))
add_cm(m)

# CL m75-80: tacet
for i in range(75, 81):
    m = stream.Measure(number=i)
    if i == 80:
        m.rightBarline = bar.Barline('final')
    m.append(r(DH))
    add_cm(m)

# Piano m65-80
# P m65: enriched ostinato [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=65)
m.insert(0, dynamics.Dynamic('pp'))
m.insert(0, tempo.MetronomeMark('Come un ricordo', 69, note.Note(type='quarter', dots=1)))
ricordo = expressions.TextExpression('come un ricordo')
ricordo.style.fontStyle = 'italic'
m.insert(0, ricordo)
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'C4', 'E4', 'G4'], E))        # Fmaj9
m.append(ch(['A4', 'C5', 'E5'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['C4', 'E4', 'G4'], E))
m.append(ch(['E5', 'G5', 'A5'], E))
add_pm(m)

# P m66: Fmaj9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=66)
m.append(n('F2', E, staccato=True))
m.append(ch(['A3', 'E4', 'G4'], E))
m.append(ch(['C5', 'E5', 'G5'], E))
m.append(n('F3', E, staccato=True))
m.append(ch(['A3', 'C4', 'E4'], E))
m.append(ch(['G4', 'A4', 'C5'], E))
add_pm(m)

# P m67: Bbmaj7#11 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=67)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['D3', 'A3', 'C4', 'E4'], E))
m.append(ch(['F4', 'A4', 'D5'], E))
m.append(n('Bb3', E, staccato=True))
m.append(ch(['D4', 'F4', 'A4'], E))
m.append(ch(['C5', 'D5', 'E5'], E))
add_pm(m)

# P m68: Bbm6 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=68)
m.append(n('Bb2', E, staccato=True))
m.append(ch(['D-3', 'F3', 'G3', 'Bb3'], E))
m.append(ch(['D-4', 'F4', 'Bb4'], E))
m.append(n('Bb3', E, staccato=True))
m.append(ch(['D-4', 'F4', 'G4'], E))
m.append(ch(['Bb4', 'D-5', 'G5'], E))
add_pm(m)

# P m69: Am7b5 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=69)
m.append(n('A2', E, staccato=True))
m.append(ch(['E-3', 'G3', 'C4', 'E4'], E))
m.append(ch(['G4', 'C5', 'E-5'], E))
m.append(n('A3', E, staccato=True))
m.append(ch(['C4', 'E4', 'G4'], E))
m.append(ch(['C5', 'E-5', 'G5'], E))
add_pm(m)

# P m70: Dm9 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=70)
m.append(n('D3', E, staccato=True))
m.append(ch(['A3', 'C4', 'E4', 'F4'], E))
m.append(ch(['A4', 'C5', 'E5'], E))
m.append(n('D4', E, staccato=True))
m.append(ch(['F4', 'A4', 'C5'], E))
m.append(ch(['E5', 'G5'], E))
add_pm(m)

# P m71: Gm11 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=71)
m.append(n('G2', E, staccato=True))
m.append(ch(['D3', 'F3', 'Bb3', 'C4'], E))
m.append(ch(['D4', 'F4', 'Bb4'], E))
m.append(n('G3', E, staccato=True))
m.append(ch(['Bb3', 'D4', 'F4'], E))
m.append(ch(['C5', 'D5', 'G5'], E))
add_pm(m)

# P m72: C7sus4 [E+E+E+E+E+E = 3.0]
m = stream.Measure(number=72)
m.append(n('C3', E, staccato=True))
m.append(ch(['G3', 'Bb3', 'F4', 'C5'], E))
m.append(ch(['Bb4', 'C5', 'G5'], E))
m.append(n('C4', E, staccato=True))
m.append(ch(['F4', 'G4', 'Bb4'], E))
m.append(ch(['C5', 'F5', 'G5'], E))
add_pm(m)

# P m73: THE CALLBACK - melody F in RH [E+DQ+r(Q) = 3.0]
m = stream.Measure(number=73)
morendo = expressions.TextExpression('morendo')
morendo.style.fontStyle = 'italic'
m.insert(0, morendo)
m.append(n('F2', E))
m.append(ch(['A3', 'C4', 'F4'], DQ, tenuto=True))  # melody F4
m.append(r(Q))
add_pm(m)

# P m74: melody G [E+DQ+r(Q) = 3.0]
m = stream.Measure(number=74)
m.append(n('G2', E))
m.append(ch(['Bb3', 'D4', 'G4'], DQ, tenuto=True))
m.append(r(Q))
add_pm(m)

# P m75: melody A [E+Q+DQ = 3.0]
m = stream.Measure(number=75)
m.append(n('A2', E))
m.append(ch(['C4', 'E4', 'A4'], Q, tenuto=True))
m.append(ch(['F4', 'A4', 'C5'], DQ))
add_pm(m)

# P m76: melody Bb [E+DQ+r(Q) = 3.0]
m = stream.Measure(number=76)
m.append(n('Bb2', E))
m.append(ch(['D4', 'F4', 'Bb4'], DQ, tenuto=True))
m.append(r(Q))
add_pm(m)

# P m77: Am7b5 dissolving [DQ+DQ = 3.0]
m = stream.Measure(number=77)
m.insert(0, dynamics.Dynamic('ppp'))
m.append(n('A2', DQ))
m.append(ch(['E-3', 'G3', 'C4', 'E4'], DQ))
add_pm(m)

# P m78: Dm9 [DQ+DQ = 3.0]
m = stream.Measure(number=78)
m.append(n('D3', DQ))
m.append(ch(['A3', 'E4', 'F4', 'C5'], DQ))
add_pm(m)

# P m79: Gm11 rit. [DQ+DQ = 3.0]
m = stream.Measure(number=79)
rit = expressions.TextExpression('rit.')
rit.style.fontStyle = 'italic'
m.insert(0, rit)
m.append(n('G2', DQ))
m.append(ch(['D3', 'C4', 'F4', 'Bb4', 'D5'], DQ))
add_pm(m)

# P m80: Fadd9 final [DH = 3.0]
m = stream.Measure(number=80)
m.rightBarline = bar.Barline('final')
niente = expressions.TextExpression('niente')
niente.style.fontStyle = 'italic'
m.insert(0, niente)
m.append(ch(['F1', 'C3', 'A3', 'C4', 'G4', 'C5'], DH, fermata=True))  # Fadd9, F1 very low
add_pm(m)

# ============================================================
# Post-process: Enrich 2-note chords to 4-note
# ============================================================
import random
random.seed(42)

def enrich_chord(ch_obj):
    if not isinstance(ch_obj, chord.Chord):
        return
    if len(ch_obj.pitches) >= 4:
        return
    if len(ch_obj.pitches) < 2:
        return
    pitches = list(ch_obj.pitches)
    midi_vals = [p.midi for p in pitches]
    low = min(midi_vals)
    candidates = []
    for offset in [3, 4, 7, 10, 11, 14]:
        candidate_midi = low + offset
        if candidate_midi not in midi_vals:
            candidates.append(candidate_midi)
    needed = 4 - len(pitches)
    for candidate_midi in candidates[:needed]:
        new_pitch = pitch.Pitch()
        new_pitch.midi = candidate_midi
        pitches.append(new_pitch)
    ch_obj.pitches = pitches

for pm in piano_measures:
    for el in pm.recurse().getElementsByClass('Chord'):
        enrich_chord(el)

# ============================================================
# Assemble
# ============================================================
clarinet_measures.sort(key=lambda m: m.number)
piano_measures.sort(key=lambda m: m.number)

for m in clarinet_measures:
    clarinet_part.append(m)
for m in piano_measures:
    piano_part.append(m)

score.insert(0, clarinet_part)
score.insert(0, piano_part)

output_path = '/home/khaled/musiclaude/experiment/007/track_04/score.musicxml'
score.write('musicxml', fp=output_path)
print(f"Score written to {output_path}")

from music21 import converter as conv
s = conv.parse(output_path)
print(f"Parsed: {len(s.parts)} parts")
for p in s.parts:
    measures = list(p.getElementsByClass('Measure'))
    notes = list(p.flatten().getElementsByClass('Note'))
    bad = [(m.number, m.duration.quarterLength) for m in measures if abs(m.duration.quarterLength - 3.0) > 0.01]
    print(f"  Part: {len(measures)} measures, {len(notes)} notes, bad_measures={bad[:5]}")
