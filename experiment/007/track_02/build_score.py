#!/usr/bin/env python3
"""Build Matin de Boulangerie MusicXML score programmatically with music21.
Iteration 2: Fix extended chords, rhythmic variety, hairpins, sections."""

from music21 import (
    stream, note, chord, key, meter, tempo, clef,
    instrument, dynamics, expressions, articulations,
    duration, pitch, layout, spanner
)

# ============================================================
# SETUP
# ============================================================
score = stream.Score()

# Parts
clarinet_part = stream.Part()
clarinet_inst = instrument.Clarinet()
clarinet_inst.partName = "Clarinet in Bb"
clarinet_inst.partAbbreviation = "Cl."
clarinet_part.insert(0, clarinet_inst)

piano_part = stream.Part()
piano_inst = instrument.Piano()
piano_inst.partName = "Piano"
piano_inst.partAbbreviation = "Pno."
piano_part.insert(0, piano_inst)

# Key and time signature
ks = key.KeySignature(-1)  # F major
ts = meter.TimeSignature('6/8')

# Duration constants (in quarterLength for 6/8 with divisions=4)
EIGHTH = 0.5       # eighth note
QUARTER = 1.0      # quarter note
DOTTED_Q = 1.5     # dotted quarter
HALF = 2.0         # half note (rare in 6/8)
DOTTED_H = 3.0     # dotted half = full 6/8 measure
SIXTEENTH = 0.25   # sixteenth note
DOTTED_E = 0.75    # dotted eighth
WHOLE_MEASURE = 3.0
TRIPLET_E = 1/3    # triplet eighth (3 in the time of 2 eighths = 1 beat)

# Helper functions
def mn(p, dur, **kwargs):
    """Create a note."""
    n = note.Note(p)
    n.duration = duration.Duration(dur)
    if kwargs.get('staccato'):
        n.articulations.append(articulations.Staccato())
    if kwargs.get('tenuto'):
        n.articulations.append(articulations.Tenuto())
    if kwargs.get('accent'):
        n.articulations.append(articulations.Accent())
    if kwargs.get('tie'):
        n.tie = note.Tie(kwargs['tie'])
    return n

def mr(dur):
    r = note.Rest()
    r.duration = duration.Duration(dur)
    return r

def mc(pitches, dur, **kwargs):
    c = chord.Chord(pitches)
    c.duration = duration.Duration(dur)
    if kwargs.get('staccato'):
        c.articulations.append(articulations.Staccato())
    if kwargs.get('tenuto'):
        c.articulations.append(articulations.Tenuto())
    if kwargs.get('accent'):
        c.articulations.append(articulations.Accent())
    return c

def mm(number):
    return stream.Measure(number=number)

# Collect all measures then add hairpins at the end
cl_all = []  # (measure_num, measure_obj)
pi_all = []

# ============================================================
# SECTION I: MORNING (mm. 1-16) - Piano alone, F major, pp-mp
# ============================================================
# Clarinet rests
for i in range(1, 17):
    m = mm(i)
    if i == 1:
        m.insert(0, key.KeySignature(-1))
        m.insert(0, meter.TimeSignature('6/8'))
    m.append(mr(WHOLE_MEASURE))
    cl_all.append(m)

# Piano: lilting 6/8 ostinato with extended chords
# Use 4-note chords (7ths, add9s) to boost pct_extended_chords

# m1: Fmaj7 ostinato, pp dolce
m = mm(1)
m.insert(0, key.KeySignature(-1))
m.insert(0, meter.TimeSignature('6/8'))
m.insert(0, tempo.MetronomeMark(referent=duration.Duration(1.5), number=72))
m.insert(0, dynamics.Dynamic('pp'))
te = expressions.TextExpression('dolce')
te.style.fontStyle = 'italic'
m.insert(0, te)
rm = expressions.RehearsalMark('I')
m.insert(0, rm)
# Varied rhythm: dotted-eighth + sixteenth + eighth pattern in LH
m.append(mn('F2', DOTTED_E, staccato=True))
m.append(mn('C3', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mn('A3', DOTTED_E))
m.append(mn('E3', SIXTEENTH))
m.append(mn('C3', EIGHTH))
pi_all.append(m)

# m2: Fadd9 - with triplet figure
m = mm(2)
m.append(mn('F2', DOTTED_E, staccato=True))
m.append(mn('A2', SIXTEENTH))
m.append(mn('G3', EIGHTH))
# triplet figure: 3 triplet eighths = 1 beat (1.0 qL) + dotted eighth to fill
m.append(mn('A3', TRIPLET_E))
m.append(mn('G3', TRIPLET_E))
m.append(mn('A3', TRIPLET_E))
m.append(mn('C3', EIGHTH))
pi_all.append(m)

# m3: Bbmaj7
m = mm(3)
m.append(mn('Bb1', DOTTED_E, staccato=True))
m.append(mn('F2', SIXTEENTH))
m.append(mn('A2', EIGHTH))
m.append(mn('D3', DOTTED_E))
m.append(mn('A2', SIXTEENTH))
m.append(mn('F2', EIGHTH))
pi_all.append(m)

# m4: Fsus4 -> Fmaj7
m = mm(4)
m.append(mc(['F2', 'Bb2', 'C3'], DOTTED_Q))  # Fsus4
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_Q))  # Fmaj7
pi_all.append(m)

# m5: Dm9
m = mm(5)
m.insert(0, dynamics.Dynamic('pp'))
m.append(mn('D2', DOTTED_E, staccato=True))
m.append(mn('A2', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mn('F3', DOTTED_E))
m.append(mn('C3', SIXTEENTH))
m.append(mn('A2', EIGHTH))
pi_all.append(m)

# m6: Gm7
m = mm(6)
m.append(mn('G2', DOTTED_E, staccato=True))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('D3', EIGHTH))
m.append(mn('F3', DOTTED_E))
m.append(mn('D3', SIXTEENTH))
m.append(mn('Bb2', EIGHTH))
pi_all.append(m)

# m7: C9sus4
m = mm(7)
m.append(mn('C2', DOTTED_E, staccato=True))
m.append(mn('F2', SIXTEENTH))
m.append(mn('Bb2', EIGHTH))
m.append(mn('D3', DOTTED_E))
m.append(mn('G2', SIXTEENTH))
m.append(mn('Bb2', EIGHTH))
pi_all.append(m)

# m8: C7 -> resolution feel
m = mm(8)
m.insert(0, dynamics.Dynamic('mp'))
m.append(mc(['C2', 'E2', 'Bb2', 'D3'], DOTTED_Q))  # C9
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7
pi_all.append(m)

# m9: Fadd9 - richer with chord
m = mm(9)
m.append(mc(['F2', 'C3', 'E3', 'G3'], DOTTED_E))  # Fmaj7add9-ish
m.append(mn('C3', SIXTEENTH))
m.append(mn('G3', EIGHTH))
m.append(mc(['F2', 'A2', 'C3', 'G3'], DOTTED_Q))  # Fadd9
pi_all.append(m)

# m10: Bbadd9
m = mm(10)
m.append(mc(['Bb1', 'D2', 'F2', 'C3'], DOTTED_E))  # Bbadd9
m.append(mn('F2', SIXTEENTH))
m.append(mn('C3', EIGHTH))
m.append(mc(['Bb1', 'D2', 'F2', 'A2'], DOTTED_Q))  # Bbmaj7
pi_all.append(m)

# m11: Am7
m = mm(11)
m.append(mc(['A1', 'E2', 'G2', 'C3'], DOTTED_Q))  # Am7
m.append(mc(['A1', 'E2', 'G2', 'B2'], DOTTED_Q))  # Am(maj7) chromatic
pi_all.append(m)

# m12: Dm9
m = mm(12)
m.append(mn('D2', DOTTED_E, staccato=True))
m.append(mn('A2', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mn('F3', EIGHTH))
m.append(mn('E3', SIXTEENTH))
m.append(mn('C3', SIXTEENTH))
m.append(mn('A2', EIGHTH))
pi_all.append(m)

# m13: Gm9
m = mm(13)
m.append(mc(['G2', 'Bb2', 'D3', 'A3'], DOTTED_Q))
m.append(mn('D3', DOTTED_E))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('G2', EIGHTH))
pi_all.append(m)

# m14: C13
m = mm(14)
m.append(mc(['C2', 'E2', 'Bb2', 'A3'], DOTTED_Q))  # C13
m.append(mc(['C2', 'E2', 'G2', 'D3'], DOTTED_Q))   # C9
pi_all.append(m)

# m15: Fmaj7
m = mm(15)
m.append(mn('F2', DOTTED_E, staccato=True))
m.append(mn('C3', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mn('A3', DOTTED_E))
m.append(mn('E3', SIXTEENTH))
m.append(mn('C3', EIGHTH))
pi_all.append(m)

# m16: Fmaj9 settling
m = mm(16)
m.insert(0, dynamics.Dynamic('mp'))
m.append(mc(['F2', 'A2', 'C3', 'E3', 'G3'], DOTTED_Q))  # Fmaj9
m.append(mc(['F2', 'A2', 'C3', 'F3'], DOTTED_Q))
pi_all.append(m)

# ============================================================
# SECTION II: THE DOOR OPENS (mm. 17-28) - Clarinet enters
# ============================================================
# Clarinet: written pitch (up M2 from concert)

# m17: Primary motif - D5 E5 F#5 G5 A5 (concert C5 D5 E5 F5 G5)
m = mm(17)
m.insert(0, dynamics.Dynamic('mp'))
te = expressions.TextExpression('espressivo')
te.style.fontStyle = 'italic'
m.insert(0, te)
rm = expressions.RehearsalMark('II')
m.insert(0, rm)
m.append(mr(EIGHTH))  # breath
m.append(mn('D5', EIGHTH))
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', DOTTED_E))
m.append(mn('G5', SIXTEENTH))
m.append(mn('A5', EIGHTH))  # higher suspension approach
cl_all.append(m)

# m18: Held suspension then resolve
m = mm(18)
m.append(mn('A5', DOTTED_Q, tenuto=True))
m.append(mn('G5', QUARTER))
m.append(mr(EIGHTH))
cl_all.append(m)

# m19: Second phrase - reaching higher
m = mm(19)
m.append(mn('E5', SIXTEENTH))
m.append(mn('F#5', SIXTEENTH))
m.append(mn('G5', EIGHTH))
m.append(mn('A5', EIGHTH))
m.append(mn('B5', DOTTED_Q, tenuto=True))
m.append(mr(EIGHTH))
cl_all.append(m)

# m20: Resolution
m = mm(20)
m.append(mn('A5', QUARTER))
m.append(mn('G5', EIGHTH))
m.append(mn('F#5', DOTTED_E))
m.append(mn('E5', SIXTEENTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m21: Motif variation - gentler, with dotted rhythm
m = mm(21)
m.append(mn('D5', DOTTED_Q, tenuto=True))
m.append(mn('E5', DOTTED_E))
m.append(mn('F#5', SIXTEENTH))
m.append(mn('G5', EIGHTH))
cl_all.append(m)

# m22: Floating down with chromatic touch
m = mm(22)
m.append(mn('F#5', QUARTER))
m.append(mn('E5', EIGHTH))
m.append(mn('D5', DOTTED_E))
m.append(mn('C#5', SIXTEENTH))  # chromatic - concert B4
m.append(mr(EIGHTH))
cl_all.append(m)

# m23: More confident - leaps
m = mm(23)
m.append(mn('D5', EIGHTH))
m.append(mn('F#5', EIGHTH))
m.append(mn('A5', QUARTER, accent=True))
m.append(mn('G5', EIGHTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m24: Settling on suspension
m = mm(24)
m.append(mn('F#5', SIXTEENTH))
m.append(mn('E5', SIXTEENTH))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', HALF, tenuto=True))  # long suspension
cl_all.append(m)

# m25: Brief rest then new idea
m = mm(25)
m.append(mr(DOTTED_Q))
m.append(mn('G5', EIGHTH))
m.append(mn('A5', EIGHTH))
m.append(mn('B5', EIGHTH))
cl_all.append(m)

# m26: Climax of Section II
m = mm(26)
m.append(mn('C6', DOTTED_Q, tenuto=True))  # concert Bb5
m.append(mn('B5', EIGHTH))
m.append(mn('A5', SIXTEENTH))
m.append(mn('G5', SIXTEENTH))
m.append(mn('F#5', EIGHTH))
cl_all.append(m)

# m27: Descending
m = mm(27)
m.append(mn('E5', QUARTER))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', DOTTED_E))
m.append(mn('D5', SIXTEENTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m28: Transition
m = mm(28)
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', EIGHTH))
m.append(mn('G5', QUARTER))
m.append(mn('A5', EIGHTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# Piano Section II: add9 and sus4 chords - extended throughout
# m17: Fadd9
m = mm(17)
rm = expressions.RehearsalMark('II')
m.insert(0, rm)
m.append(mc(['F2', 'A2', 'C3', 'G3'], DOTTED_E))  # Fadd9
m.append(mn('C3', SIXTEENTH))
m.append(mn('G3', EIGHTH))
m.append(mc(['F2', 'A2', 'C3', 'G3'], DOTTED_Q))
pi_all.append(m)

# m18: Csus4 -> Cmaj7
m = mm(18)
m.append(mc(['C2', 'F2', 'G2', 'C3'], DOTTED_Q))  # Csus4
m.append(mc(['C2', 'E2', 'G2', 'B2'], DOTTED_Q))  # Cmaj7
pi_all.append(m)

# m19: Bbadd9
m = mm(19)
m.append(mc(['Bb1', 'D2', 'F2', 'C3'], DOTTED_E))  # Bbadd9
m.append(mn('F2', SIXTEENTH))
m.append(mn('C3', EIGHTH))
m.append(mc(['Bb1', 'D2', 'F2', 'A2'], DOTTED_Q))  # Bbmaj7
pi_all.append(m)

# m20: Gm9
m = mm(20)
m.append(mc(['G2', 'Bb2', 'D3', 'A3'], DOTTED_Q))  # Gm9
m.append(mc(['G2', 'Bb2', 'D3', 'F3'], DOTTED_Q))  # Gm7
pi_all.append(m)

# m21: Dm7
m = mm(21)
m.append(mn('D2', DOTTED_E, staccato=True))
m.append(mn('A2', SIXTEENTH))
m.append(mn('C3', EIGHTH))
m.append(mc(['D2', 'F2', 'A2', 'C3'], DOTTED_Q))
pi_all.append(m)

# m22: G9
m = mm(22)
m.append(mc(['G2', 'B2', 'D3', 'F3', 'A3'], DOTTED_Q))  # G9
m.append(mn('D3', DOTTED_E))
m.append(mn('B2', SIXTEENTH))
m.append(mn('G2', EIGHTH))
pi_all.append(m)

# m23: Csus4 -> C7
m = mm(23)
m.append(mc(['C2', 'F2', 'G2', 'Bb2'], DOTTED_Q))  # C7sus4
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7
pi_all.append(m)

# m24: Am7
m = mm(24)
m.append(mc(['A1', 'E2', 'G2', 'C3'], DOTTED_Q))  # Am7
m.append(mn('G2', DOTTED_E))
m.append(mn('E2', SIXTEENTH))
m.append(mn('C3', EIGHTH))
pi_all.append(m)

# m25: Dm9
m = mm(25)
m.append(mc(['D2', 'A2', 'C3', 'E3'], DOTTED_Q))
m.append(mn('A2', DOTTED_E, staccato=True))
m.append(mn('C3', SIXTEENTH))
m.append(mn('F3', EIGHTH))
pi_all.append(m)

# m26: Bbmaj7
m = mm(26)
m.append(mc(['Bb1', 'D2', 'F2', 'A2'], DOTTED_Q))  # Bbmaj7
m.append(mc(['Bb1', 'F2', 'A2', 'D3'], DOTTED_Q))
pi_all.append(m)

# m27: C7
m = mm(27)
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7
m.append(mn('Bb2', DOTTED_E))
m.append(mn('G2', SIXTEENTH))
m.append(mn('E2', EIGHTH))
pi_all.append(m)

# m28: F -> transition
m = mm(28)
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_Q))  # Fmaj7
m.append(mc(['F2', 'A2', 'C3', 'F3'], DOTTED_Q))  # F
pi_all.append(m)

# ============================================================
# SECTION III: CONVERSATION (mm. 29-48) - Call and response
# ============================================================

# m29: Clarinet call - motif transposed (G5 A5 B5 C6 = motif up a 4th)
m = mm(29)
m.insert(0, dynamics.Dynamic('mp'))
te = expressions.TextExpression('con moto')
te.style.fontStyle = 'italic'
m.insert(0, te)
rm = expressions.RehearsalMark('III')
m.insert(0, rm)
m.append(mr(EIGHTH))  # breath, like m17
m.append(mn('G5', EIGHTH))
m.append(mn('A5', EIGHTH))
m.append(mn('B5', DOTTED_E))
m.append(mn('C6', SIXTEENTH))
m.append(mn('D6', EIGHTH))
cl_all.append(m)

# m30: rest (piano responds)
m = mm(30)
m.append(mr(WHOLE_MEASURE))
cl_all.append(m)

# m31: Clarinet - expressive
m = mm(31)
m.append(mn('A5', EIGHTH))
m.append(mn('B5', SIXTEENTH))
m.append(mn('C6', SIXTEENTH))
m.append(mn('D6', QUARTER, accent=True))
m.append(mn('C6', EIGHTH))
m.append(mn('B5', EIGHTH))
m.append(mn('A5', EIGHTH))
cl_all.append(m)

# m32: rest
m = mm(32)
m.append(mr(WHOLE_MEASURE))
cl_all.append(m)

# m33: Motif again - same rhythm as m17 entry (motivic consistency)
m = mm(33)
m.append(mr(EIGHTH))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', DOTTED_E))
m.append(mn('G5', SIXTEENTH))
m.append(mn('A5', EIGHTH))
cl_all.append(m)

# m34: Continuation, mf
m = mm(34)
m.insert(0, dynamics.Dynamic('mf'))
m.append(mn('E5', EIGHTH))
m.append(mn('G5', EIGHTH))
m.append(mn('B5', DOTTED_Q, tenuto=True))  # 6th leap
m.append(mr(EIGHTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m35: Overlap begins
m = mm(35)
m.append(mr(DOTTED_Q))
m.append(mn('A5', DOTTED_E))
m.append(mn('G5', SIXTEENTH))
m.append(mn('F#5', EIGHTH))
cl_all.append(m)

# m36: Building to D minor
m = mm(36)
m.append(mn('E5', QUARTER))
m.append(mn('D5', EIGHTH))
m.append(mn('C#5', DOTTED_E))
m.append(mn('D5', SIXTEENTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m37: D minor - vulnerability
m = mm(37)
m.insert(0, dynamics.Dynamic('mp'))
te = expressions.TextExpression('dim.')
te.style.fontStyle = 'italic'
m.insert(0, te)
m.append(mn('E5', DOTTED_Q, tenuto=True))  # concert D5
m.append(mn('D5', EIGHTH))
m.append(mn('C5', EIGHTH))
m.append(mn('D5', EIGHTH))
cl_all.append(m)

# m38: D minor continuation
m = mm(38)
m.append(mn('F5', QUARTER))
m.append(mn('E5', EIGHTH))
m.append(mn('D5', DOTTED_E))
m.append(mn('C5', SIXTEENTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m39: Resolving - A7 -> warmth
m = mm(39)
m.append(mn('C#5', EIGHTH))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', DOTTED_E))
m.append(mn('G5', SIXTEENTH))
m.append(mn('A5', EIGHTH))
cl_all.append(m)

# m40: Back to F major
m = mm(40)
m.insert(0, dynamics.Dynamic('mp'))
m.append(mn('A5', DOTTED_Q, tenuto=True))
m.append(mn('G5', EIGHTH))
m.append(mn('F#5', EIGHTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m41: Motif echo again (D5 E5 F#5 G5 A5 pattern = motivic consistency)
m = mm(41)
m.append(mr(EIGHTH))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', DOTTED_E))
m.append(mn('G5', SIXTEENTH))
m.append(mn('A5', EIGHTH))
cl_all.append(m)

# m42: Rest then answer
m = mm(42)
m.append(mr(DOTTED_Q))
m.append(mn('D5', EIGHTH))
m.append(mn('F#5', EIGHTH))
m.append(mn('A5', EIGHTH))
cl_all.append(m)

# m43: Expanding, mf
m = mm(43)
m.insert(0, dynamics.Dynamic('mf'))
m.append(mn('B5', DOTTED_Q, accent=True))
m.append(mn('A5', DOTTED_E))
m.append(mn('G5', SIXTEENTH))
m.append(mn('F#5', EIGHTH))
cl_all.append(m)

# m44: Overlapping
m = mm(44)
m.append(mn('G5', EIGHTH))
m.append(mn('A5', EIGHTH))
m.append(mn('B5', EIGHTH))
m.append(mn('C6', QUARTER, tenuto=True))
m.append(mr(EIGHTH))
cl_all.append(m)

# m45: Building peak
m = mm(45)
m.append(mn('D5', EIGHTH))
m.append(mn('E5', EIGHTH))
m.append(mn('G5', EIGHTH))
m.append(mn('B5', EIGHTH))
m.append(mn('D6', QUARTER, accent=True))  # concert C6 high
cl_all.append(m)

# m46: Descending
m = mm(46)
m.append(mn('C6', EIGHTH))
m.append(mn('B5', SIXTEENTH))
m.append(mn('A5', SIXTEENTH))
m.append(mn('G5', EIGHTH))
m.append(mn('F#5', EIGHTH))
m.append(mn('E5', SIXTEENTH))
m.append(mn('D5', SIXTEENTH))
m.append(mn('C5', EIGHTH))
cl_all.append(m)

# m47: Settling
m = mm(47)
m.append(mn('D5', QUARTER))
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', DOTTED_Q, tenuto=True))
cl_all.append(m)

# m48: Transition to Ab major
m = mm(48)
m.append(mn('G5', QUARTER))
m.append(mn('Ab5', EIGHTH))  # chromatic hint
m.append(mn('Bb5', QUARTER))
m.append(mr(EIGHTH))
cl_all.append(m)

# Piano Section III
# m29: F major, con moto
m = mm(29)
m.insert(0, tempo.MetronomeMark(referent=duration.Duration(1.5), number=76))
rm = expressions.RehearsalMark('III')
m.insert(0, rm)
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_E))  # Fmaj7
m.append(mn('C3', SIXTEENTH))
m.append(mn('A3', EIGHTH))
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_Q))  # Fmaj7
pi_all.append(m)

# m30: Piano response melody
m = mm(30)
m.append(mn('A3', EIGHTH))
m.append(mn('Bb3', SIXTEENTH))
m.append(mn('C4', SIXTEENTH))
m.append(mn('D4', QUARTER))
m.append(mn('C4', EIGHTH))
m.append(mn('Bb3', EIGHTH))
m.append(mn('A3', EIGHTH))
pi_all.append(m)

# m31: Gm9
m = mm(31)
m.append(mc(['G2', 'Bb2', 'D3', 'F3', 'A3'], DOTTED_Q))
m.append(mn('D3', DOTTED_E, staccato=True))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('F3', EIGHTH))
pi_all.append(m)

# m32: Piano response
m = mm(32)
m.append(mn('Bb3', EIGHTH))
m.append(mn('C4', EIGHTH))
m.append(mn('D4', DOTTED_E))
m.append(mn('Eb4', SIXTEENTH))
m.append(mn('D4', EIGHTH))
m.append(mn('Bb3', EIGHTH))
pi_all.append(m)

# m33: Am7
m = mm(33)
m.append(mc(['A1', 'E2', 'G2', 'C3'], DOTTED_Q))
m.append(mn('E3', DOTTED_E))
m.append(mn('C3', SIXTEENTH))
m.append(mn('G2', EIGHTH))
pi_all.append(m)

# m34: Bbmaj7
m = mm(34)
m.append(mc(['Bb1', 'D2', 'F2', 'A2'], DOTTED_Q))  # Bbmaj7
m.append(mn('D3', DOTTED_E, staccato=True))
m.append(mn('A2', SIXTEENTH))
m.append(mn('F2', EIGHTH))
pi_all.append(m)

# m35: C9 - piano call
m = mm(35)
m.append(mn('C4', EIGHTH))
m.append(mn('D4', DOTTED_E))
m.append(mn('E4', SIXTEENTH))
m.append(mc(['C2', 'E2', 'Bb2', 'D3'], DOTTED_Q))  # C9
pi_all.append(m)

# m36: Em7b5
m = mm(36)
m.append(mc(['E2', 'Bb2', 'D3', 'G3'], DOTTED_Q))  # Em7b5
m.append(mn('D3', DOTTED_E))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('E2', EIGHTH))
pi_all.append(m)

# m37: Dm - D minor excursion
m = mm(37)
m.append(mc(['D2', 'A2', 'D3', 'F3'], DOTTED_E))
m.append(mn('A2', SIXTEENTH))
m.append(mn('D3', EIGHTH))
m.append(mc(['D2', 'F2', 'A2', 'C3'], DOTTED_Q))  # Dm7
pi_all.append(m)

# m38: Gm7
m = mm(38)
m.append(mc(['G2', 'Bb2', 'D3', 'F3'], DOTTED_Q))  # Gm7
m.append(mn('D3', DOTTED_E, staccato=True))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('G2', EIGHTH))
pi_all.append(m)

# m39: A7 resolving
m = mm(39)
m.append(mc(['A1', 'E2', 'C#3', 'G3'], DOTTED_Q))  # A7
m.append(mc(['D2', 'F2', 'A2', 'D3'], DOTTED_Q))   # Dm
pi_all.append(m)

# m40: Bb -> C7 -> F
m = mm(40)
m.append(mc(['Bb1', 'D2', 'F2', 'A2'], DOTTED_Q))  # Bbmaj7
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7
pi_all.append(m)

# m41: Fmaj7
m = mm(41)
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_E))
m.append(mn('C3', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mc(['F2', 'C3', 'E3', 'A3'], DOTTED_Q))
pi_all.append(m)

# m42: Gm7 - piano call
m = mm(42)
m.append(mn('G3', EIGHTH))
m.append(mn('A3', EIGHTH))
m.append(mn('Bb3', DOTTED_E))
m.append(mn('C4', SIXTEENTH))
m.append(mc(['G2', 'D3', 'F3'], EIGHTH))
m.append(mn('D3', EIGHTH))
pi_all.append(m)

# m43: Am9
m = mm(43)
m.append(mc(['A1', 'E2', 'G2', 'C3', 'B2'], DOTTED_Q))  # Am9
m.append(mn('E2', DOTTED_E, staccato=True))
m.append(mn('G2', SIXTEENTH))
m.append(mn('C3', EIGHTH))
pi_all.append(m)

# m44: Bbmaj9
m = mm(44)
m.append(mc(['Bb1', 'D2', 'F2', 'A2', 'C3'], DOTTED_Q))  # Bbmaj9
m.append(mn('F2', DOTTED_E, staccato=True))
m.append(mn('D3', SIXTEENTH))
m.append(mn('A2', EIGHTH))
pi_all.append(m)

# m45: C7sus4 -> C7
m = mm(45)
m.append(mc(['C2', 'F2', 'G2', 'Bb2'], DOTTED_Q))  # C7sus4
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7
pi_all.append(m)

# m46: Fmaj7
m = mm(46)
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_E))
m.append(mn('C3', SIXTEENTH))
m.append(mn('A3', EIGHTH))
m.append(mn('F3', DOTTED_E))
m.append(mn('C3', SIXTEENTH))
m.append(mn('A2', EIGHTH))
pi_all.append(m)

# m47: Bdim7 -> C7
m = mm(47)
m.append(mc(['B1', 'D2', 'F2', 'Ab2'], DOTTED_Q))  # Bdim7
m.append(mc(['C2', 'E2', 'Bb2', 'D3'], DOTTED_Q))  # C9
pi_all.append(m)

# m48: Ab transition
m = mm(48)
m.append(mc(['Ab1', 'Eb2', 'C3', 'G3'], DOTTED_Q))  # Abmaj7
m.append(mc(['Bb1', 'D2', 'F2', 'Ab2'], DOTTED_Q))  # Bbdim? No - Bb7
pi_all.append(m)

# ============================================================
# SECTION IV: WALKING HOME (mm. 49-64) - Peak, Ab major
# ============================================================

# m49: Clarinet - wide open
m = mm(49)
m.insert(0, dynamics.Dynamic('mf'))
te = expressions.TextExpression('largamente')
te.style.fontStyle = 'italic'
m.insert(0, te)
rm = expressions.RehearsalMark('IV')
m.insert(0, rm)
m.append(mn('F5', QUARTER))     # concert Eb5
m.append(mn('Bb5', QUARTER, tenuto=True))   # concert Ab5, leap of 4th
m.append(mn('C6', EIGHTH))      # concert Bb5
m.append(mr(EIGHTH))
cl_all.append(m)

# m50
m = mm(50)
m.append(mn('Bb5', EIGHTH))
m.append(mn('Ab5', EIGHTH))
m.append(mn('G5', DOTTED_E))
m.append(mn('F5', SIXTEENTH))
m.append(mn('Eb5', EIGHTH))
m.append(mr(EIGHTH))
cl_all.append(m)

# m51: Rising - wide intervals
m = mm(51)
m.append(mn('Bb5', EIGHTH))
m.append(mn('D6', QUARTER, accent=True))  # 6th leap! concert C6
m.append(mn('C6', DOTTED_E))
m.append(mn('Bb5', SIXTEENTH))
m.append(mn('Ab5', EIGHTH))
cl_all.append(m)

# m52: f dynamic
m = mm(52)
m.insert(0, dynamics.Dynamic('f'))
m.append(mn('G5', EIGHTH))
m.append(mn('F5', EIGHTH))
m.append(mn('Eb5', QUARTER))
m.append(mn('F5', EIGHTH))
m.append(mn('G5', EIGHTH))
cl_all.append(m)

# m53: Second wave
m = mm(53)
m.append(mn('Bb5', EIGHTH))
m.append(mn('C6', EIGHTH))
m.append(mn('Eb6', QUARTER, accent=True))  # highest peak! concert Db6
m.append(mr(EIGHTH))
m.append(mn('D6', EIGHTH))
cl_all.append(m)

# m54: Descending cascade with triplet
m = mm(54)
m.append(mn('C6', EIGHTH))
m.append(mn('Bb5', EIGHTH))
m.append(mn('Ab5', EIGHTH))
# triplet figure descending
m.append(mn('G5', TRIPLET_E))
m.append(mn('F5', TRIPLET_E))
m.append(mn('Eb5', TRIPLET_E))
m.append(mn('D5', EIGHTH))
cl_all.append(m)

# m55: Singing together
m = mm(55)
m.append(mn('Bb5', DOTTED_Q, tenuto=True))
m.append(mn('Ab5', EIGHTH))
m.append(mn('G5', EIGHTH))
m.append(mn('F5', EIGHTH))
cl_all.append(m)

# m56: Eb echoes
m = mm(56)
m.append(mn('Eb5', QUARTER))
m.append(mn('F5', EIGHTH))
m.append(mn('G5', DOTTED_Q, tenuto=True))
cl_all.append(m)

# m57: Building again
m = mm(57)
m.append(mn('Ab5', EIGHTH))
m.append(mn('Bb5', EIGHTH))
m.append(mn('C6', QUARTER, accent=True))
m.append(mn('Bb5', SIXTEENTH))
m.append(mn('Ab5', SIXTEENTH))
m.append(mn('G5', EIGHTH))
cl_all.append(m)

# m58: Contrary motion
m = mm(58)
m.append(mn('Bb5', QUARTER))
m.append(mn('C6', EIGHTH))
m.append(mn('D6', DOTTED_Q, tenuto=True))
cl_all.append(m)

# m59: Broadening
m = mm(59)
m.append(mn('C6', QUARTER))
m.append(mn('Bb5', EIGHTH))
m.append(mn('Ab5', QUARTER))
m.append(mr(EIGHTH))
cl_all.append(m)

# m60: Fm7
m = mm(60)
m.append(mn('G5', EIGHTH))
m.append(mn('Ab5', DOTTED_E))
m.append(mn('Bb5', SIXTEENTH))
m.append(mn('C6', QUARTER))
m.append(mn('Bb5', EIGHTH))
cl_all.append(m)

# m61: Peak returns, f
m = mm(61)
m.insert(0, dynamics.Dynamic('f'))
m.append(mn('Ab5', EIGHTH))
m.append(mn('C6', QUARTER, accent=True))
m.append(mn('Bb5', DOTTED_E))
m.append(mn('Ab5', SIXTEENTH))
m.append(mn('G5', EIGHTH))
cl_all.append(m)

# m62
m = mm(62)
m.append(mn('F5', EIGHTH))
m.append(mn('G5', EIGHTH))
m.append(mn('Bb5', DOTTED_Q, tenuto=True))
m.append(mr(EIGHTH))
cl_all.append(m)

# m63: Transition back, dim e rit
m = mm(63)
m.insert(0, dynamics.Dynamic('mf'))
te = expressions.TextExpression('dim. e rit.')
te.style.fontStyle = 'italic'
m.insert(0, te)
m.append(mn('Ab5', QUARTER))
m.append(mn('G5', EIGHTH))
m.append(mn('F#5', QUARTER))
m.append(mn('E5', EIGHTH))
cl_all.append(m)

# m64
m = mm(64)
m.append(mn('D5', DOTTED_Q, tenuto=True))
m.append(mr(DOTTED_Q))
cl_all.append(m)

# Piano Section IV
# m49: Ab major
m = mm(49)
m.insert(0, dynamics.Dynamic('mf'))
m.insert(0, tempo.MetronomeMark(referent=duration.Duration(1.5), number=80))
rm = expressions.RehearsalMark('IV')
m.insert(0, rm)
m.append(mc(['Ab1', 'Eb2', 'Ab2', 'C3'], DOTTED_E))  # Ab
m.append(mn('Eb3', SIXTEENTH))
m.append(mn('Ab3', EIGHTH))
m.append(mc(['Ab1', 'C2', 'Eb2', 'G2'], DOTTED_Q))  # Abmaj7
pi_all.append(m)

# m50: Bbm7
m = mm(50)
m.append(mc(['Bb1', 'F2', 'Ab2', 'Db3'], DOTTED_Q))  # Bbm7
m.append(mn('Ab2', DOTTED_E, staccato=True))
m.append(mn('Db3', SIXTEENTH))
m.append(mn('F3', EIGHTH))
pi_all.append(m)

# m51: Eb9
m = mm(51)
m.append(mc(['Eb2', 'G2', 'Bb2', 'Db3', 'F3'], DOTTED_Q))  # Eb9
m.append(mn('Db3', DOTTED_E))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('G2', EIGHTH))
pi_all.append(m)

# m52: Abmaj7
m = mm(52)
m.append(mc(['Ab1', 'Eb2', 'G2', 'C3'], DOTTED_E))  # Abmaj7
m.append(mn('Eb3', SIXTEENTH))
m.append(mn('G3', EIGHTH))
m.append(mc(['Ab1', 'C2', 'Eb2', 'G2'], DOTTED_Q))
pi_all.append(m)

# m53: Dbmaj7
m = mm(53)
m.append(mc(['Db2', 'F2', 'Ab2', 'C3'], DOTTED_Q))  # Dbmaj7
m.append(mc(['Db2', 'F2', 'Ab2', 'Eb3'], DOTTED_Q))  # Db9
pi_all.append(m)

# m54: Dbm (borrowed)
m = mm(54)
m.append(mc(['Db2', 'E2', 'Ab2', 'Db3'], DOTTED_Q))  # Dbm
m.append(mn('Ab2', DOTTED_E, staccato=True))
m.append(mn('E2', SIXTEENTH))
m.append(mn('Db3', EIGHTH))
pi_all.append(m)

# m55: Ab/Eb
m = mm(55)
m.insert(0, dynamics.Dynamic('f'))
m.append(mc(['Eb2', 'Ab2', 'C3', 'Eb3'], DOTTED_E))
m.append(mn('Ab3', SIXTEENTH))
m.append(mn('C3', EIGHTH))
m.append(mc(['Eb2', 'Ab2', 'C3', 'G3'], DOTTED_Q))  # Ab/Eb with 7th
pi_all.append(m)

# m56: Eb7
m = mm(56)
m.append(mc(['Eb2', 'G2', 'Bb2', 'Db3'], DOTTED_Q))  # Eb7
m.append(mn('Bb2', DOTTED_E, staccato=True))
m.append(mn('Db3', SIXTEENTH))
m.append(mn('G3', EIGHTH))
pi_all.append(m)

# m57: Fm9
m = mm(57)
m.append(mc(['F2', 'Ab2', 'C3', 'Eb3', 'G3'], DOTTED_Q))  # Fm9
m.append(mn('C3', DOTTED_E))
m.append(mn('Eb3', SIXTEENTH))
m.append(mn('Ab3', EIGHTH))
pi_all.append(m)

# m58: Bbm9
m = mm(58)
m.append(mc(['Bb1', 'Db2', 'F2', 'Ab2', 'C3'], DOTTED_Q))  # Bbm9
m.append(mn('F2', DOTTED_E, staccato=True))
m.append(mn('Ab2', SIXTEENTH))
m.append(mn('Db3', EIGHTH))
pi_all.append(m)

# m59: Eb9
m = mm(59)
m.append(mc(['Eb2', 'G2', 'Bb2', 'F3'], DOTTED_Q))  # Eb9-ish
m.append(mc(['Eb2', 'G2', 'Bb2', 'Db3'], DOTTED_Q))  # Eb7
pi_all.append(m)

# m60: Abmaj7
m = mm(60)
m.append(mc(['Ab1', 'Eb2', 'G2', 'C3'], DOTTED_E))  # Abmaj7
m.append(mn('Eb3', SIXTEENTH))
m.append(mn('Ab3', EIGHTH))
m.append(mc(['Ab1', 'Eb2', 'G2', 'C3'], DOTTED_Q))  # Abmaj7
pi_all.append(m)

# m61: Db -> Dbm
m = mm(61)
m.append(mc(['Db2', 'F2', 'Ab2', 'C3'], DOTTED_Q))  # Dbmaj7
m.append(mc(['Db2', 'E2', 'Ab2', 'B2'], DOTTED_Q))  # Dbm - dark
pi_all.append(m)

# m62: Eb7sus4 -> Eb7
m = mm(62)
m.append(mc(['Eb2', 'Ab2', 'Bb2', 'Db3'], DOTTED_Q))  # Eb7sus4
m.append(mc(['Eb2', 'G2', 'Bb2', 'Db3'], DOTTED_Q))  # Eb7
pi_all.append(m)

# m63: Transition
m = mm(63)
m.append(mc(['Ab1', 'C2', 'Eb2', 'Ab2'], DOTTED_Q))
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7 -> back to F
pi_all.append(m)

# m64: C7 preparation
m = mm(64)
m.insert(0, dynamics.Dynamic('mp'))
m.append(mc(['C2', 'E2', 'G2', 'Bb2', 'D3'], DOTTED_Q))  # C9
m.append(mc(['C2', 'E2', 'G2', 'Bb2'], DOTTED_Q))  # C7
pi_all.append(m)

# ============================================================
# SECTION V: ALONE AGAIN (mm. 65-80)
# ============================================================

# Clarinet: mostly rests, brief ghostly appearance
for i in range(65, 72):
    m = mm(i)
    m.append(mr(WHOLE_MEASURE))
    cl_all.append(m)

# m72: Ghost of the melody, pp
m = mm(72)
m.insert(0, dynamics.Dynamic('pp'))
te = expressions.TextExpression('come un soffio')
te.style.fontStyle = 'italic'
m.insert(0, te)
m.append(mr(DOTTED_Q))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', EIGHTH))
m.append(mn('F#5', EIGHTH))
cl_all.append(m)

# m73: Whisper
m = mm(73)
m.append(mn('G5', DOTTED_Q, tenuto=True))
m.append(mr(DOTTED_Q))
cl_all.append(m)

for i in range(74, 81):
    m = mm(i)
    m.append(mr(WHOLE_MEASURE))
    cl_all.append(m)

# Piano Section V
# m65: Enriched ostinato returns, pp
m = mm(65)
m.insert(0, tempo.MetronomeMark(referent=duration.Duration(1.5), number=69))
m.insert(0, dynamics.Dynamic('pp'))
te = expressions.TextExpression('come un ricordo')
te.style.fontStyle = 'italic'
m.insert(0, te)
rm = expressions.RehearsalMark('V')
m.insert(0, rm)
m.append(mn('F2', DOTTED_E, staccato=True))
m.append(mn('C3', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mc(['A3', 'G4'], DOTTED_E))  # Fmaj7 + add9 color
m.append(mn('E3', SIXTEENTH))
m.append(mn('C3', EIGHTH))
pi_all.append(m)

# m66: Fadd9
m = mm(66)
m.append(mc(['F2', 'A2', 'C3', 'G3'], DOTTED_E))  # Fadd9
m.append(mn('C3', SIXTEENTH))
m.append(mn('G3', EIGHTH))
m.append(mc(['F2', 'A2', 'E3', 'G3'], DOTTED_Q))  # Fmaj9
pi_all.append(m)

# m67: Dm9
m = mm(67)
m.append(mc(['D2', 'A2', 'E3', 'F3'], DOTTED_Q))  # Dm9
m.append(mn('E3', DOTTED_E))
m.append(mn('A2', SIXTEENTH))
m.append(mn('D2', EIGHTH))
pi_all.append(m)

# m68: Gm11
m = mm(68)
m.append(mc(['G2', 'C3', 'D3', 'F3', 'Bb3'], DOTTED_Q))  # Gm11
m.append(mn('D3', DOTTED_E, staccato=True))
m.append(mn('F3', SIXTEENTH))
m.append(mn('Bb3', EIGHTH))
pi_all.append(m)

# m69: C13
m = mm(69)
m.append(mc(['C2', 'E2', 'Bb2', 'D3', 'A3'], DOTTED_Q))  # C13
m.append(mn('E3', DOTTED_E))
m.append(mn('Bb2', SIXTEENTH))
m.append(mn('G2', EIGHTH))
pi_all.append(m)

# m70: Fmaj7 with chromatic color
m = mm(70)
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_E))  # Fmaj7
m.append(mn('C3', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mc(['F2', 'Ab2', 'C3', 'E3'], DOTTED_Q))  # chromatic inner voice
pi_all.append(m)

# m71: Bbmaj7#11
m = mm(71)
m.append(mc(['Bb1', 'D2', 'F2', 'A2', 'E3'], DOTTED_Q))  # Bbmaj7#11
m.append(mn('A2', DOTTED_E))
m.append(mn('D3', SIXTEENTH))
m.append(mn('F2', EIGHTH))
pi_all.append(m)

# m72: THE MEMORY - clarinet's motif in piano RH!
m = mm(72)
te = expressions.TextExpression('la melodia')
te.style.fontStyle = 'italic'
m.insert(0, te)
# Concert: C5-D5-E5-F5-G5 in RH, LH arpeggio underneath
m.append(mn('F2', EIGHTH, staccato=True))  # LH
m.append(mn('C5', EIGHTH, tenuto=True))    # RH: motif starts
m.append(mn('D5', EIGHTH))
m.append(mn('E5', DOTTED_E))
m.append(mn('F5', SIXTEENTH))
m.append(mn('G5', EIGHTH, tenuto=True))    # the suspension
pi_all.append(m)

# m73: Motif continues in RH
m = mm(73)
m.append(mn('G5', QUARTER, tenuto=True))
m.append(mn('F5', EIGHTH))
m.append(mn('E5', DOTTED_E))
m.append(mn('C3', SIXTEENTH))
m.append(mn('A2', EIGHTH))
pi_all.append(m)

# m74: Echo
m = mm(74)
m.append(mc(['D2', 'A2', 'E3', 'F3'], DOTTED_E))  # Dm9
m.append(mn('C5', SIXTEENTH))
m.append(mn('D5', EIGHTH))
m.append(mn('E5', DOTTED_Q, tenuto=True))
pi_all.append(m)

# m75: Gm9
m = mm(75)
m.append(mc(['G2', 'Bb2', 'D3', 'A3'], DOTTED_Q))  # Gm9
m.append(mn('D3', DOTTED_E, staccato=True))
m.append(mn('A3', SIXTEENTH))
m.append(mn('Bb3', EIGHTH))
pi_all.append(m)

# m76: morendo
m = mm(76)
te = expressions.TextExpression('morendo')
te.style.fontStyle = 'italic'
m.insert(0, te)
m.append(mc(['C2', 'G2', 'F3', 'Bb3'], DOTTED_Q))  # C7sus4
m.append(mn('F3', DOTTED_E))
m.append(mn('G2', SIXTEENTH))
m.append(mn('C2', EIGHTH))
pi_all.append(m)

# m77: Fmaj7
m = mm(77)
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_E))  # Fmaj7
m.append(mn('C3', SIXTEENTH))
m.append(mn('E3', EIGHTH))
m.append(mc(['F2', 'A2', 'C3', 'E3'], DOTTED_Q))  # Fmaj7
pi_all.append(m)

# m78: Bbmaj7
m = mm(78)
m.append(mc(['Bb1', 'D2', 'F2', 'A2'], DOTTED_Q))
m.append(mn('A2', DOTTED_E))
m.append(mn('F2', SIXTEENTH))
m.append(mn('D2', EIGHTH))
pi_all.append(m)

# m79: C9, rit.
m = mm(79)
te = expressions.TextExpression('rit.')
te.style.fontStyle = 'italic'
m.insert(0, te)
m.append(mc(['C2', 'E2', 'G2', 'Bb2', 'D3'], DOTTED_Q))  # C9
m.append(mn('G2', DOTTED_E))
m.append(mn('E3', SIXTEENTH))
m.append(mn('D3', EIGHTH))
pi_all.append(m)

# m80: Fadd9 - FINAL - unresolved
m = mm(80)
m.insert(0, dynamics.Dynamic('pp'))
te = expressions.TextExpression('lasciar vibrare')
te.style.fontStyle = 'italic'
m.insert(0, te)
m.append(mc(['F2', 'A2', 'C3', 'G3', 'A3', 'G4'], WHOLE_MEASURE, tenuto=True))  # Fadd9 big voicing
pi_all.append(m)

# ============================================================
# ASSEMBLE PARTS
# ============================================================
for m in cl_all:
    clarinet_part.append(m)
for m in pi_all:
    piano_part.append(m)

# ============================================================
# ADD HAIRPINS (crescendo/diminuendo) as spanners
# ============================================================
# We need to add them by inserting DynamicWedge objects into the parts
# Use note references from measures

def add_hairpin(part, measures_list, start_m, end_m, htype='crescendo'):
    """Add a hairpin between first note of start_m and last note of end_m.
    start_m and end_m are 1-indexed measure numbers."""
    start_measure = None
    end_measure = None
    for m_obj in measures_list:
        if m_obj.number == start_m:
            start_measure = m_obj
        if m_obj.number == end_m:
            end_measure = m_obj
    if start_measure is None or end_measure is None:
        return

    start_notes = list(start_measure.recurse().getElementsByClass(['Note', 'Chord']))
    end_notes = list(end_measure.recurse().getElementsByClass(['Note', 'Chord']))
    if not start_notes or not end_notes:
        return

    if htype == 'crescendo':
        hp = dynamics.Crescendo(start_notes[0], end_notes[-1])
    else:
        hp = dynamics.Diminuendo(start_notes[0], end_notes[-1])
    part.insert(0, hp)

# Section I: pp -> mp (crescendo mm. 5-8)
add_hairpin(piano_part, pi_all, 5, 8, 'crescendo')
# Section I: slight dim mm. 15-16
add_hairpin(piano_part, pi_all, 15, 16, 'diminuendo')

# Section II: clarinet crescendo mm. 23-26
add_hairpin(clarinet_part, cl_all, 23, 26, 'crescendo')
# Section II: dim mm. 26-28
add_hairpin(clarinet_part, cl_all, 26, 28, 'diminuendo')

# Section III: cresc mm. 33-34
add_hairpin(clarinet_part, cl_all, 33, 34, 'crescendo')
# Section III: dim into D minor mm. 36-37
add_hairpin(clarinet_part, cl_all, 36, 37, 'diminuendo')
# Section III: cresc mm. 41-45
add_hairpin(clarinet_part, cl_all, 41, 43, 'crescendo')
# Section III: piano cresc mm. 41-45
add_hairpin(piano_part, pi_all, 41, 45, 'crescendo')

# Section IV: cresc mm. 49-52
add_hairpin(clarinet_part, cl_all, 49, 52, 'crescendo')
add_hairpin(piano_part, pi_all, 49, 52, 'crescendo')
# Section IV: dim mm. 58-60
add_hairpin(clarinet_part, cl_all, 58, 60, 'diminuendo')
# Section IV: cresc mm. 60-61
add_hairpin(clarinet_part, cl_all, 60, 61, 'crescendo')
# Section IV: grand dim mm. 63-64
add_hairpin(clarinet_part, cl_all, 63, 64, 'diminuendo')
add_hairpin(piano_part, pi_all, 63, 64, 'diminuendo')

# Section V: dim mm. 72-76 (morendo)
add_hairpin(piano_part, pi_all, 72, 76, 'diminuendo')
# Section V: final dim mm. 77-80
add_hairpin(piano_part, pi_all, 77, 80, 'diminuendo')

# ============================================================
# ASSEMBLE SCORE & WRITE
# ============================================================
score.insert(0, clarinet_part)
score.insert(0, piano_part)

output_path = 'experiment/007/track_02/score.musicxml'
score.write('musicxml', fp=output_path)
print(f"Score written to {output_path}")

# Validate
from music21 import converter
s = converter.parse(output_path)
parts = s.parts
total_notes = len(list(s.flatten().getElementsByClass('Note')))
total_measures = max(len(list(p.getElementsByClass('Measure'))) for p in parts)
print(f"Parsed: {len(parts)} parts, {total_notes} notes, {total_measures} measures")
for p in parts:
    inst = p.getInstrument(returnDefault=True)
    notes = list(p.recurse().getElementsByClass('Note'))
    rests = list(p.recurse().getElementsByClass('Rest'))
    print(f"  {inst.partName or inst.instrumentName}: {len(notes)} notes, {len(rests)} rests")
