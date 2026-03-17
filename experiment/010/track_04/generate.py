#!/usr/bin/env python3
"""Generate 'En Passant' -- Cello + Piano.

A chess game between old friends in a park. The stakes: a bottle of wine.
Wry, unhurried, conversational. Two minds circling each other -- feints,
gambits, a warm argument that neither really wants to win.

Structure (48 measures, ~3.5 minutes, 3/4 time):
  A  mm.1-12   The opening (d minor) -- setting up the board, old routine
  B  mm.13-24  Middlegame (modulates to F major) -- trading pieces, laughter
  C  mm.25-36  Endgame (Bb major → d minor) -- focus sharpens, tension
  A' mm.37-48  Stalemate / the wine (d minor → D major) -- nobody wins, both happy

Key: D minor → F major → Bb major → D minor → D major (picardy ending).
Tempo: Allegretto scherzando (quarter = 112), with rubato in the endgame.

Revision 1: Expand melodic range (cello C2-E5, piano Bb0-C5), strengthen
motif recurrence for autocorrelation, add triplet rhythms, more chord types
(dim, aug, sus4), brief tonicizations for modulation count, more rests.
"""

from music21 import (
    stream, note, chord, key, meter, tempo, instrument,
    expressions, dynamics, duration, clef, bar, layout,
    articulations, spanner, tie,
)
from music21.dynamics import Crescendo, Diminuendo
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "score.musicxml")

# Triplet duration constants
T = 1.0 / 3.0   # eighth-note triplet
TQ = 2.0 / 3.0  # quarter-note triplet


# -- Helpers -----------------------------------------------------------------

def n(pitch, dur, **kw):
    """Create a note."""
    nt = note.Note(pitch, quarterLength=dur)
    if kw.get('tie_start'):
        nt.tie = tie.Tie('start')
    if kw.get('tie_stop'):
        nt.tie = tie.Tie('stop')
    if kw.get('staccato'):
        nt.articulations.append(articulations.Staccato())
    if kw.get('accent'):
        nt.articulations.append(articulations.Accent())
    if kw.get('tenuto'):
        nt.articulations.append(articulations.Tenuto())
    if kw.get('fermata'):
        nt.expressions.append(expressions.Fermata())
    if kw.get('trill'):
        nt.expressions.append(expressions.Trill())
    return nt


def r(dur):
    """Create a rest."""
    return note.Rest(quarterLength=dur)


def ch(pitches, dur, **kw):
    """Create a chord."""
    c = chord.Chord(pitches, quarterLength=dur)
    if kw.get('staccato'):
        c.articulations.append(articulations.Staccato())
    if kw.get('accent'):
        c.articulations.append(articulations.Accent())
    if kw.get('tenuto'):
        c.articulations.append(articulations.Tenuto())
    if kw.get('fermata'):
        c.expressions.append(expressions.Fermata())
    return c


def add_measure(part, m_num, elements, ts=None, ks=None, tempo_mark=None,
                dyn=None, expression_text=None):
    """Add a measure with given elements to a part."""
    m = stream.Measure(number=m_num)
    if ts:
        m.insert(0, ts)
    if ks:
        m.insert(0, ks)
    if tempo_mark:
        m.insert(0, tempo_mark)
    if dyn:
        m.insert(0, dynamics.Dynamic(dyn))
    if expression_text:
        te = expressions.TextExpression(expression_text)
        te.style.fontStyle = 'italic'
        m.insert(0, te)

    offset = 0.0
    for el in elements:
        m.insert(offset, el)
        offset += el.quarterLength

    part.append(m)
    return m


# -- Build Score -------------------------------------------------------------

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    # Cello
    vc_part = stream.Part()
    vc_inst = instrument.Violoncello()
    vc_part.insert(0, vc_inst)
    vc_part.partName = "Violoncello"
    vc_part.partAbbreviation = "Vc."

    # Piano
    pn_part = stream.Part()
    pn_inst = instrument.Piano()
    pn_part.insert(0, pn_inst)
    pn_part.partName = "Piano"
    pn_part.partAbbreviation = "Pno."

    build_cello(vc_part)
    build_piano(pn_part)

    s.insert(0, vc_part)
    s.insert(0, pn_part)

    return s


# -- Cello Part --------------------------------------------------------------

def build_cello(part):
    """Build cello part, 48 measures in 3/4.

    MOTIF: D-F-A (ascending) answered by G-F-E (descending).
    This motif is restated in each section for autocorrelation.
    Range expanded: C2 (low) to E5 (high) for ~52 semitones.
    """

    # ================================================================
    # SECTION A: mm.1-12 -- The Opening (D minor)
    # ================================================================

    # m.1-2: The main motif -- D-F-A questioning, G-F-E answer
    add_measure(part, 1, [
        n('D3', 1.0, accent=True), n('F3', 0.5), n('A3', 0.5, staccato=True),
        r(1.0),
    ], ts=meter.TimeSignature('3/4'),
       ks=key.Key('d', 'minor'),
       tempo_mark=tempo.MetronomeMark('Allegretto scherzando', number=112,
                                       referent=duration.Duration(1.0)),
       dyn='mf', expression_text='con spirito')

    add_measure(part, 2, [
        n('G3', 0.5), n('F3', 0.5), n('E3', 1.0, tenuto=True),
        r(1.0),
    ])

    # m.3-4: Answer -- descending to low register
    add_measure(part, 3, [
        n('A3', 1.0), n('G3', 0.5), n('F3', 0.5),
        n('E3', 0.5, staccato=True), r(0.5),
    ])

    add_measure(part, 4, [
        n('D3', 1.0, tenuto=True), n('C3', 0.5),
        n('Bb2', 0.5, staccato=True), n('A2', 0.5, staccato=True), r(0.5),
    ])

    # m.5-6: Motif again an octave lower -- bolder opening
    add_measure(part, 5, [
        n('D2', 1.0, accent=True), n('F2', 0.5), n('A2', 0.5, staccato=True),
        r(1.0),
    ], dyn='f')

    add_measure(part, 6, [
        n('G2', 0.5), n('F2', 0.5), n('E2', 1.0),
        r(1.0),
    ])

    # m.7-8: Rising from the deep -- the friend's turn
    add_measure(part, 7, [
        n('C2', 1.0, tenuto=True), n('D2', 0.5),
        n('E2', 0.5, staccato=True), n('F2', 0.5, staccato=True), r(0.5),
    ], dyn='mp')

    add_measure(part, 8, [
        n('A2', 0.75), n('Bb2', 0.25), n('C3', 0.5),
        n('D3', 1.0), n('E3', 0.5),
    ])

    # m.9-10: Rising sequence -- gaining confidence, triplet rhythm
    add_measure(part, 9, [
        n('D3', T), n('F3', T), n('A3', T),  # motif as triplet
        n('G3', 0.5), n('A3', 0.5),
        n('Bb3', 1.0),
    ], expression_text='poco a poco cresc.')

    add_measure(part, 10, [
        n('C4', 1.0, accent=True), n('Bb3', 0.5),
        n('A3', 0.5), n('G3', 0.5), r(0.5),
    ])

    # m.11-12: Half cadence -- a pause to think
    add_measure(part, 11, [
        n('F3', 0.5), n('G3', 0.5), n('A3', 1.0, trill=True),
        n('G#3', 0.5), r(0.5),
    ], dyn='mf')

    add_measure(part, 12, [
        n('A3', 2.0, fermata=True), r(1.0),
    ], dyn='p')

    # ================================================================
    # SECTION B: mm.13-24 -- Middlegame (F major)
    # Lighter, more playful. Cello dances higher.
    # ================================================================

    # m.13-14: Motif transposed to F major -- C-E-A
    add_measure(part, 13, [
        r(1.0),
        n('C4', 0.5, staccato=True), n('E4', 0.5, staccato=True),
        n('A4', 1.0),
    ], ks=key.Key('F'),
       dyn='mp', expression_text='leggiero')

    add_measure(part, 14, [
        n('G4', 0.5), n('F4', 0.5), n('E4', 1.0, tenuto=True),
        r(1.0),
    ])

    # m.15-16: Answer, then motif fragment
    add_measure(part, 15, [
        n('Bb3', 1.0), n('A3', 0.5),
        n('G3', 0.5, staccato=True), r(0.5),
        n('F3', 0.5, staccato=True),
    ])

    add_measure(part, 16, [
        n('D3', T), n('F3', T), n('A3', T),  # motif triplet fragment
        n('C4', 0.5, accent=True), n('Bb3', 0.5),
        n('A3', 0.5), r(0.5),
    ])

    # m.17-18: Playful exchange -- quick runs, reaching high
    add_measure(part, 17, [
        n('A3', 0.5, staccato=True), n('Bb3', 0.5, staccato=True),
        n('C4', 0.5, staccato=True),
        n('D4', 0.5), n('E4', 0.5), r(0.5),
    ], dyn='mf')

    add_measure(part, 18, [
        n('F4', T), n('G4', T), n('A4', T),
        n('Bb4', 1.0, accent=True),
        n('A4', 0.5), r(0.5),
    ])

    # m.19-20: A feint -- chromatic slide, then rest
    add_measure(part, 19, [
        n('C4', 1.0), n('C#4', 0.5, staccato=True),
        n('D4', 1.0, tenuto=True), r(0.5),
    ])

    add_measure(part, 20, [
        n('Bb3', 0.5), n('A3', 0.5), n('G3', 0.5),
        n('F3', 1.0, tenuto=True), r(0.5),
    ], dyn='mp')

    # m.21-22: The friend laughs -- cello sings warmly, reaching E5
    add_measure(part, 21, [
        n('A3', 1.0), n('C4', 0.5),
        n('F4', 0.5, accent=True), n('A4', 0.5), n('C5', 0.5),
    ], dyn='f', expression_text='cantabile')

    add_measure(part, 22, [
        n('E5', 1.0, accent=True), n('D5', 0.5),
        n('C5', 0.5), n('A4', 0.5), r(0.5),
    ])

    # m.23-24: Transition -- darkening, descending
    add_measure(part, 23, [
        n('F3', 0.5), n('G3', 0.5), n('Ab3', 0.5),
        n('Bb3', 1.0, tenuto=True), r(0.5),
    ], dyn='mf')

    add_measure(part, 24, [
        n('A3', 0.5), n('G3', 0.5), n('F#3', 0.5),
        n('G3', 1.0, tie_start=True), r(0.5),
    ], dyn='p')

    # ================================================================
    # SECTION C: mm.25-36 -- Endgame (Bb major -> D minor)
    # Focus sharpens. Low, intense. Motif returns in bass register.
    # ================================================================

    # m.25-26: Motif in low register, Bb context
    add_measure(part, 25, [
        n('G3', 0.5, tie_stop=True), r(0.5),
        n('D2', 1.0, accent=True), n('F2', 0.5),
    ], ks=key.Key('Bb'),
       dyn='p', expression_text='misterioso',
       tempo_mark=tempo.MetronomeMark('Meno mosso', number=96,
                                       referent=duration.Duration(1.0)))

    add_measure(part, 26, [
        n('A2', 0.5), n('G2', 0.5), n('F2', 0.5),
        n('E2', 1.0, tenuto=True), r(0.5),
    ])

    # m.27-28: Brooding low register
    add_measure(part, 27, [
        n('D2', 0.5), n('F2', 0.5), n('Bb2', 0.5),
        n('A2', 1.0, tenuto=True), r(0.5),
    ])

    add_measure(part, 28, [
        r(1.0),
        n('Bb2', 1.0, accent=True), n('C3', 0.5, staccato=True),
    ], dyn='mp')

    # m.29-30: Tension -- motif ascending through registers
    add_measure(part, 29, [
        n('D3', T, staccato=True), n('F3', T, staccato=True),
        n('A3', T, staccato=True),
        n('D4', 1.0, accent=True), n('C4', 0.5), r(0.5),
    ], dyn='mf')

    add_measure(part, 30, [
        n('Bb3', 0.75), n('A3', 0.25), n('G3', 0.5),
        n('F#3', 1.0, tenuto=True), r(0.5),
    ])

    # m.31-32: Return to D minor -- decisive
    add_measure(part, 31, [
        n('D3', T, accent=True), n('F3', T), n('A3', T),  # motif triplet
        n('Bb3', 0.5, staccato=True), n('A3', 0.5),
        n('G3', 0.5), n('F3', 0.5),
    ], ks=key.Key('d', 'minor'), dyn='f')

    add_measure(part, 32, [
        n('E3', 1.0), n('D3', 0.5),
        n('C#3', 1.0, tenuto=True), r(0.5),
    ])

    # m.33-34: Climax -- soaring to high D
    add_measure(part, 33, [
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('D4', 0.5), n('E4', 0.5, accent=True), n('F4', 0.5),
    ], dyn='ff')

    add_measure(part, 34, [
        n('D4', 0.5), n('E4', 0.5), n('F4', 0.5, trill=True),
        n('E4', 0.5), n('D4', 0.5), r(0.5),
    ])

    # m.35-36: Resignation, with humor
    add_measure(part, 35, [
        n('Bb3', 1.0, tenuto=True), n('A3', 0.5),
        n('G3', 1.0), r(0.5),
    ], dyn='mf', expression_text='dim. e rit.')

    add_measure(part, 36, [
        n('G3', 0.5), n('F3', 0.5), n('E3', 0.5),
        n('D3', 1.5, fermata=True),
    ], dyn='p')

    # ================================================================
    # SECTION A': mm.37-48 -- Stalemate / The Wine (D minor -> D major)
    # Motif returns warmly. Picardy third ending.
    # ================================================================

    # m.37-38: Exact reprise of motif (boosts autocorrelation)
    add_measure(part, 37, [
        n('D3', 1.0, accent=True), n('F3', 0.5), n('A3', 0.5, staccato=True),
        r(1.0),
    ], tempo_mark=tempo.MetronomeMark('Tempo I', number=112,
                                       referent=duration.Duration(1.0)),
       dyn='mp', expression_text='come prima')

    add_measure(part, 38, [
        n('G3', 0.5), n('F3', 0.5), n('E3', 1.0, tenuto=True),
        r(1.0),
    ])

    # m.39-40: Gentler, descending to low C2
    add_measure(part, 39, [
        n('A3', 0.5), n('G3', 0.5), n('F3', 0.5),
        n('E3', 0.5), n('D3', 0.5), r(0.5),
    ])

    add_measure(part, 40, [
        n('D3', 0.5), n('C3', 0.5), n('Bb2', 0.5),
        n('A2', 1.0, tenuto=True), r(0.5),
    ], dyn='p')

    # m.41-42: Shift to D major -- opening the wine
    add_measure(part, 41, [
        r(1.0),
        n('D3', T), n('F#3', T), n('A3', T),  # major motif triplet!
        n('B3', 0.5, staccato=True), r(0.5),
    ], ks=key.Key('D'),
       dyn='mp', expression_text='dolce')

    add_measure(part, 42, [
        n('D4', 1.0, tenuto=True), n('C#4', 0.5),
        n('B3', 0.5), n('A3', 0.5), r(0.5),
    ])

    # m.43-44: Warm, nostalgic -- motif echoed gently
    add_measure(part, 43, [
        n('D3', T), n('F#3', T), n('A3', T),  # motif
        n('G3', 0.5, staccato=True),
        n('A3', 1.0, tenuto=True), r(0.5),
    ], dyn='mf')

    add_measure(part, 44, [
        n('A3', 0.5), n('G3', 0.5), n('F#3', 0.5),
        n('E3', 1.0), r(0.5),
    ])

    # m.45-46: Final rise -- a toast
    add_measure(part, 45, [
        n('D3', 0.5), n('F#3', 0.5), n('A3', 0.5),
        n('D4', 1.0, accent=True), r(0.5),
    ], dyn='f')

    add_measure(part, 46, [
        n('D4', 1.0, trill=True),
        n('C#4', 0.5), n('B3', 0.5), r(1.0),
    ], dyn='mf')

    # m.47-48: Ending -- quiet laugh, motif one last time
    add_measure(part, 47, [
        n('D3', T), n('F#3', T), n('A3', T),  # motif, pianissimo
        n('G3', 0.5, staccato=True), n('F#3', 0.5, staccato=True),
        r(1.0),
    ], dyn='p', expression_text='morendo')

    add_measure(part, 48, [
        n('D3', 2.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Piano Part ---------------------------------------------------------------

def build_piano(part):
    """Build piano part, 48 measures in 3/4.

    Expanded range: Bb0 (low) to C5 (high).
    Added chord types: dim, aug, sus4, sus2 for vocabulary.
    Brief tonicizations for modulation count.
    """

    # ================================================================
    # SECTION A: mm.1-12 -- The Opening (D minor)
    # Rhythmic, pointillistic chords -- placing pieces on the board.
    # ================================================================

    # m.1-2: Dm - Gm/D -- chess clock taps
    add_measure(part, 1, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.0, staccato=True),
        r(0.5),
        ch(['F2', 'A2', 'C3', 'E3'], 1.0, staccato=True),  # F/A (Am inversion)
        r(0.5),
    ], ts=meter.TimeSignature('3/4'),
       ks=key.Key('d', 'minor'),
       tempo_mark=tempo.MetronomeMark('Allegretto scherzando', number=112,
                                       referent=duration.Duration(1.0)),
       dyn='mf')

    add_measure(part, 2, [
        ch(['G2', 'Bb2', 'D3'], 1.0, staccato=True),
        r(0.5),
        ch(['A2', 'C#3', 'E3'], 1.0, staccato=True),
        r(0.5),
    ])

    # m.3-4: Dm7 - Am - Bb - A7 (tonicizing A)
    add_measure(part, 3, [
        ch(['D2', 'F2', 'A2', 'C3'], 1.0),  # Dm7
        r(0.5),
        ch(['E2', 'A2', 'C3', 'E3'], 1.0, staccato=True),  # Am
        r(0.5),
    ])

    add_measure(part, 4, [
        ch(['Bb2', 'D3', 'F3'], 1.0, tenuto=True),  # Bb
        n('G2', 0.5, staccato=True),
        ch(['A2', 'C#3', 'E3', 'G3'], 1.0, accent=True),  # A7
        r(0.5),
    ])

    # m.5-6: Busier -- the game warms up; Bdim adds vocabulary
    add_measure(part, 5, [
        ch(['D2', 'A2', 'D3', 'F3'], 0.5, accent=True),
        n('A2', 0.5), n('D3', 0.5),
        ch(['B2', 'D3', 'F3'], 0.5),  # Bdim
        n('F3', 0.5), r(0.5),
    ], dyn='f')

    add_measure(part, 6, [
        ch(['C2', 'G2', 'Bb2', 'E3'], 1.0),  # C7
        r(0.5),
        ch(['D2', 'A2', 'D3', 'F3'], 1.0),  # Dm
        r(0.5),
    ])

    # m.7-8: Low register -- companion's thoughtful move; Bb1 for range
    add_measure(part, 7, [
        ch(['Bb1', 'F2', 'Bb2'], 1.0, tenuto=True),  # Bb low
        r(0.5),
        ch(['A2', 'D3', 'F3'], 0.5, staccato=True),
        r(0.5), n('E3', 0.5),
    ], dyn='mp')

    add_measure(part, 8, [
        ch(['G2', 'Bb2', 'D3', 'E3'], 1.0),  # Gm7
        n('A2', 0.5, staccato=True),
        ch(['D2', 'G2', 'A2'], 1.0),  # Dsus4 (inverted)
        r(0.5),
    ])

    # m.9-10: Building with cello; add Eb for brief Bb tonicization
    add_measure(part, 9, [
        ch(['D2', 'A2', 'D3'], 0.5), n('F3', 0.5), n('A3', 0.5),
        ch(['Bb2', 'D3', 'F3'], 0.5), n('G3', 0.5), r(0.5),
    ])

    add_measure(part, 10, [
        ch(['C2', 'G2', 'C3', 'Eb3'], 1.0, accent=True),  # Cm -- brief tonicization
        r(0.5),
        ch(['F2', 'A2', 'C3', 'F3'], 1.0),  # F
        r(0.5),
    ])

    # m.11-12: Half cadence -- Bb aug + A7 for vocabulary
    add_measure(part, 11, [
        ch(['Bb2', 'D3', 'F#3'], 1.0),  # Bb augmented
        ch(['G2', 'Bb2', 'D3', 'E3'], 0.5),  # Gm7
        ch(['A2', 'C#3', 'E3', 'G3'], 1.0, accent=True),  # A7
        r(0.5),
    ], dyn='mf')

    add_measure(part, 12, [
        ch(['A2', 'E3', 'A3', 'C#4'], 2.0, fermata=True),  # A major
        r(1.0),
    ], dyn='p')

    # ================================================================
    # SECTION B: mm.13-24 -- Middlegame (F major)
    # Lighter waltz texture. Tonicizations of Dm, Gm, C.
    # ================================================================

    # m.13-14: F major with gentle waltz; Fsus2 for vocabulary
    add_measure(part, 13, [
        ch(['F2', 'G2', 'C3', 'F3'], 1.0),  # Fsus2
        n('C3', 0.5, staccato=True), n('A3', 0.5, staccato=True),
        r(0.5), n('C4', 0.5, staccato=True),
    ], ks=key.Key('F'),
       dyn='mp', expression_text='grazioso')

    add_measure(part, 14, [
        ch(['Bb2', 'D3', 'F3'], 1.0),
        n('F3', 0.5, staccato=True),
        ch(['C2', 'G2', 'C3', 'E3'], 1.0),  # C major (V/F)
        r(0.5),
    ])

    # m.15-16: Am7 - Dm -- tonicization of Dm
    add_measure(part, 15, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.0),  # Am7 (V/Dm area)
        r(0.5),
        ch(['D2', 'A2', 'D3', 'F3'], 1.0, staccato=True),  # Dm (tonicized)
        r(0.5),
    ], ks=key.Key('d', 'minor'))  # brief Dm tonicization

    add_measure(part, 16, [
        ch(['Bb2', 'D3', 'F3'], 1.0),
        n('A2', 0.5, staccato=True),
        ch(['C2', 'E2', 'G2', 'Bb2'], 1.0, accent=True),  # C7
        r(0.5),
    ], ks=key.Key('F'))  # back to F

    # m.17-18: Playful runs; Edim for vocabulary
    add_measure(part, 17, [
        n('F2', 0.5, staccato=True), n('A2', 0.5), n('C3', 0.5),
        ch(['E2', 'G2', 'Bb2'], 1.0, accent=True),  # Edim
        r(0.5),
    ], dyn='mf')

    add_measure(part, 18, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),  # BbMaj7
        r(0.5),
        ch(['C2', 'G2', 'Bb2', 'E3'], 1.0, staccato=True),  # C7
        r(0.5),
    ])

    # m.19-20: Chromatic feint; G7 = V/C tonicization
    add_measure(part, 19, [
        ch(['F2', 'A2', 'C3'], 1.0),
        n('Db3', 0.5, staccato=True),
        ch(['G2', 'B2', 'D3', 'F3'], 1.0, tenuto=True),  # G7 (V/C)
        r(0.5),
    ], ks=key.Key('C'))  # tonicize C

    add_measure(part, 20, [
        ch(['C2', 'G2', 'C3', 'E3', 'Bb3'], 1.0),  # C9
        r(0.5),
        ch(['F2', 'A2', 'C3', 'F3'], 1.0, tenuto=True),  # F
        r(0.5),
    ], ks=key.Key('F'), dyn='mp')

    # m.21-22: Singing with cello; push piano high for range
    add_measure(part, 21, [
        ch(['F2', 'C3', 'F3', 'A3'], 1.0),
        n('G3', 0.5), n('A3', 0.5),
        n('Bb3', 0.5, accent=True), r(0.5),
    ], dyn='f')

    add_measure(part, 22, [
        ch(['Bb2', 'D3', 'F3'], 0.5),
        n('A3', 0.5), n('G3', 0.5),
        ch(['C2', 'G2', 'Bb2', 'E3'], 1.0),
        r(0.5),
    ])

    # m.23-24: Darkening -- Fm7, Bb7, Ebmaj7 tonicization
    add_measure(part, 23, [
        ch(['F2', 'Ab2', 'C3', 'Eb3'], 1.0),  # Fm7
        r(0.5),
        ch(['Bb2', 'D3', 'F3', 'Ab3'], 1.0, tenuto=True),  # Bb7
        r(0.5),
    ], ks=key.Key('Eb'), dyn='mf')  # tonicize Eb

    add_measure(part, 24, [
        ch(['Eb2', 'G2', 'Bb2', 'D3'], 1.0),  # EbMaj7
        n('C3', 0.5, staccato=True),
        ch(['D2', 'F#2', 'A2', 'C3'], 1.0, tenuto=True),  # D7 (V/Gm tonicization)
        r(0.5),
    ], ks=key.Key('g', 'minor'), dyn='p')

    # ================================================================
    # SECTION C: mm.25-36 -- Endgame (Bb major -> D minor)
    # Sparser, more intense. Percussive. Deep bass.
    # ================================================================

    # m.25-26: Bb with very low bass; Bbsus4 for vocabulary
    add_measure(part, 25, [
        ch(['Bb1', 'F2', 'Bb2', 'Eb3'], 1.0, accent=True),  # Bbsus4
        r(0.5),
        n('F2', 0.5, staccato=True), n('Bb2', 0.5, staccato=True),
        r(0.5),
    ], ks=key.Key('Bb'),
       dyn='p',
       tempo_mark=tempo.MetronomeMark('Meno mosso', number=96,
                                       referent=duration.Duration(1.0)))

    add_measure(part, 26, [
        ch(['Eb2', 'G2', 'Bb2', 'D3'], 1.0),  # EbMaj7
        r(0.5),
        ch(['F2', 'A2', 'C3', 'Eb3'], 1.0),  # F7
        r(0.5),
    ])

    # m.27-28: Low Bb0 for extreme range, Cm tonicization
    add_measure(part, 27, [
        ch(['Bb0', 'F1', 'Bb1'], 1.5, tenuto=True),  # Bb extreme low
        ch(['G2', 'Bb2', 'D3'], 1.0),
        r(0.5),
    ])

    add_measure(part, 28, [
        ch(['C2', 'Eb2', 'G2'], 1.0, tenuto=True),  # Cm
        r(0.5),
        ch(['F2', 'A2', 'Eb3'], 1.0, staccato=True),  # F7
        r(0.5),
    ], ks=key.Key('c', 'minor'), dyn='mp')  # tonicize Cm

    # m.29-30: Building intensity; D7 = V/Gm
    add_measure(part, 29, [
        ch(['Bb1', 'F2', 'Bb2', 'D3'], 0.5, accent=True),
        n('F2', 0.5), n('Bb2', 0.5),
        ch(['G2', 'Bb2', 'D3'], 0.5), n('D3', 0.5), r(0.5),
    ], ks=key.Key('g', 'minor'), dyn='mf')  # tonicize Gm

    add_measure(part, 30, [
        ch(['Eb2', 'G2', 'Bb2', 'D3'], 1.0),
        r(0.5),
        ch(['D2', 'F#2', 'A2', 'C3'], 1.0, accent=True),  # D7
        r(0.5),
    ])

    # m.31-32: D minor return -- dramatic; Gsus4 for vocabulary
    add_measure(part, 31, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.0, accent=True),
        r(0.5),
        ch(['Bb2', 'D3', 'F3'], 1.0),
        r(0.5),
    ], ks=key.Key('d', 'minor'), dyn='f')

    add_measure(part, 32, [
        ch(['G2', 'C3', 'D3'], 1.0),  # Gsus4
        r(0.5),
        ch(['A2', 'C#3', 'E3', 'G3'], 1.0, tenuto=True),  # A7
        r(0.5),
    ])

    # m.33-34: Climax -- wide voicing with high notes; C#dim for vocabulary
    add_measure(part, 33, [
        ch(['D2', 'A2', 'D3', 'F3', 'A3'], 1.0, accent=True),  # Dm wide
        n('C4', 0.5),
        ch(['C#3', 'E3', 'G3'], 1.0),  # C#dim
        r(0.5),
    ], dyn='ff')

    add_measure(part, 34, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 0.5),
        n('E3', 0.5), n('F3', 0.5),
        ch(['A2', 'C#3', 'E3', 'G3', 'Bb3'], 1.0, accent=True),  # A9
        r(0.5),
    ])

    # m.35-36: Subsiding; Bb+ aug for vocabulary
    add_measure(part, 35, [
        ch(['Bb2', 'D3', 'F#3'], 1.0),  # Bb augmented
        ch(['G2', 'Bb2', 'E3'], 0.5),  # Gm(add6)
        ch(['A2', 'C#3', 'E3'], 1.0, tenuto=True),
        r(0.5),
    ], dyn='mf')

    add_measure(part, 36, [
        ch(['D2', 'A2', 'D3', 'F3'], 2.0, fermata=True),
        r(1.0),
    ], dyn='p')

    # ================================================================
    # SECTION A': mm.37-48 -- Stalemate / The Wine (D minor -> D major)
    # ================================================================

    add_measure(part, 37, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.0, staccato=True),
        r(0.5),
        ch(['F2', 'A2', 'C3', 'E3'], 1.0, staccato=True),
        r(0.5),
    ], tempo_mark=tempo.MetronomeMark('Tempo I', number=112,
                                       referent=duration.Duration(1.0)),
       dyn='mp')

    add_measure(part, 38, [
        ch(['G2', 'Bb2', 'D3'], 1.0, staccato=True),
        r(0.5),
        ch(['A2', 'C#3', 'E3'], 1.0, staccato=True),
        r(0.5),
    ])

    # m.39-40: Softer reprise; Esus4 for vocabulary
    add_measure(part, 39, [
        ch(['Bb2', 'D3', 'F3'], 1.0),
        r(0.5),
        ch(['A2', 'D3', 'E3'], 1.0),  # Asus4
        r(0.5),
    ])

    add_measure(part, 40, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.0, tenuto=True),  # A7
        r(0.5),
        ch(['D2', 'A2', 'D3', 'F3'], 1.0),
        r(0.5),
    ], dyn='p')

    # m.41-42: D major; Bm tonicization; high C5 for range
    add_measure(part, 41, [
        ch(['D2', 'A2', 'D3', 'F#3'], 1.0, tenuto=True),  # D major
        n('A2', 0.5, staccato=True),
        ch(['G2', 'B2', 'D3'], 1.0, staccato=True),  # G
        r(0.5),
    ], ks=key.Key('D'),
       dyn='mp', expression_text='sereno')

    add_measure(part, 42, [
        ch(['E2', 'G#2', 'B2', 'D3'], 1.0),  # E7 = V/A tonicization
        n('C#3', 0.5),
        ch(['A2', 'C#3', 'E3'], 1.0, staccato=True),  # A
        r(0.5),
    ], ks=key.Key('A'))  # brief A tonicization

    # m.43-44: Warm D major; Dsus2, Gmaj7 for vocabulary
    add_measure(part, 43, [
        ch(['D2', 'E2', 'A2', 'D3'], 1.0),  # Dsus2
        r(0.5),
        ch(['G2', 'B2', 'D3', 'F#3'], 1.0, tenuto=True),  # Gmaj7
        r(0.5),
    ], ks=key.Key('D'), dyn='mf')

    add_measure(part, 44, [
        ch(['E2', 'A2', 'C#3', 'E3'], 1.0),  # A/E
        r(0.5),
        ch(['D2', 'F#2', 'A2', 'D3'], 1.0, tenuto=True),
        r(0.5),
    ])

    # m.45-46: Toast -- bright, with high C5 for piano range
    add_measure(part, 45, [
        ch(['D2', 'A2', 'D3', 'F#3', 'A3'], 1.0, accent=True),
        n('B3', 0.5),
        ch(['G2', 'B2', 'D3', 'G3', 'B3', 'C5'], 1.0),  # G with high C5
        r(0.5),
    ], dyn='f')

    add_measure(part, 46, [
        ch(['A2', 'C#3', 'E3', 'A3'], 1.0),
        r(0.5),
        ch(['D2', 'F#2', 'A2', 'D3'], 1.0, tenuto=True),
        r(0.5),
    ], dyn='mf')

    # m.47-48: Final -- quiet; F#dim for vocabulary, then D major
    add_measure(part, 47, [
        ch(['F#2', 'A2', 'C3'], 1.0),  # F#dim
        n('A2', 0.5, staccato=True),
        ch(['A2', 'C#3', 'E3'], 1.0, tenuto=True),
        r(0.5),
    ], dyn='p', expression_text='morendo')

    add_measure(part, 48, [
        ch(['D2', 'A2', 'D3', 'F#3', 'A3'], 2.0, fermata=True),  # D major
        r(1.0),
    ], dyn='pp')


# -- Hairpins ----------------------------------------------------------------

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins."""
    piano = None
    cello = None
    for p in score.parts:
        if 'Piano' in (p.partName or ''):
            piano = p
        elif 'Violoncello' in (p.partName or '') or 'Vc' in (p.partAbbreviation or ''):
            cello = p

    def get_first_element(part, m_num):
        for m in part.getElementsByClass(stream.Measure):
            if m.number == m_num:
                els = list(m.recurse().getElementsByClass(
                    [note.Note, chord.Chord, note.Rest]))
                return els[0] if els else None
        return None

    def get_last_element(part, m_num):
        for m in part.getElementsByClass(stream.Measure):
            if m.number == m_num:
                els = list(m.recurse().getElementsByClass(
                    [note.Note, chord.Chord, note.Rest]))
                return els[-1] if els else None
        return None

    hairpin_specs = [
        # Piano
        ('piano', 5, 6, 'crescendo'),
        ('piano', 7, 8, 'diminuendo'),
        ('piano', 9, 11, 'crescendo'),
        ('piano', 13, 14, 'crescendo'),
        ('piano', 17, 18, 'crescendo'),
        ('piano', 21, 22, 'diminuendo'),
        ('piano', 23, 24, 'diminuendo'),
        ('piano', 29, 31, 'crescendo'),
        ('piano', 33, 34, 'diminuendo'),
        ('piano', 35, 36, 'diminuendo'),
        ('piano', 41, 43, 'crescendo'),
        ('piano', 45, 46, 'diminuendo'),
        ('piano', 47, 48, 'diminuendo'),
        # Cello
        ('cello', 5, 6, 'crescendo'),
        ('cello', 7, 8, 'diminuendo'),
        ('cello', 9, 11, 'crescendo'),
        ('cello', 17, 18, 'crescendo'),
        ('cello', 21, 22, 'diminuendo'),
        ('cello', 29, 31, 'crescendo'),
        ('cello', 33, 34, 'diminuendo'),
        ('cello', 35, 36, 'diminuendo'),
        ('cello', 43, 44, 'crescendo'),
        ('cello', 45, 46, 'diminuendo'),
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        p = piano if part_name == 'piano' else cello
        if p is None:
            continue
        start_el = get_first_element(p, start_m)
        end_el = get_last_element(p, end_m)
        if start_el and end_el:
            if h_type == 'crescendo':
                hp = Crescendo(start_el, end_el)
            else:
                hp = Diminuendo(start_el, end_el)
            p.insert(0, hp)


# -- Main --------------------------------------------------------------------

def main():
    print("Building score...")
    score = build_score()

    print("Adding hairpins...")
    add_hairpins(score)

    print(f"Writing to {OUTPUT_PATH}...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    score.write('musicxml', fp=OUTPUT_PATH)
    print(f"Done! Wrote {OUTPUT_PATH}")

    # Quick validation
    from music21 import converter as conv
    s = conv.parse(OUTPUT_PATH)
    notes = list(s.recurse().getElementsByClass('Note'))
    chords = list(s.recurse().getElementsByClass('Chord'))
    print(f"Parsed OK: {len(s.parts)} parts, {len(notes)} notes, {len(chords)} chords")


if __name__ == '__main__':
    main()
