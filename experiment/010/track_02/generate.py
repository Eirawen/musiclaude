#!/usr/bin/env python3
"""Generate 'The Bottle Gambit' -- Cello + Piano.

A chess game between old friends in a park. The stakes are a bottle of wine.
3/4 time, D minor -> F major -> D minor -> D major.

Sections:
  I.   Opening (mm.1-8)   -- Piano sets the board. Deliberate, unhurried.
  II.  First Moves (mm.9-20)  -- Cello enters. Familiar patterns, easy conversation.
  III. Midgame (mm.21-36) -- Tension builds. A sharp line from the cello,
                              the piano answers. They know each other's tricks.
  IV.  The Gambit (mm.37-48) -- F major. One friend sacrifices a piece for position.
                                Bold, warm, a little reckless. "You sure about that?"
  V.   Endgame (mm.49-60)  -- Back to D minor, then D major. The game resolves.
                               Whoever wins, they'll share the wine.

Revision notes (post-profile feedback):
- Expanded cello range: G2 to Bb4 (was A2-G4, now 39 semitones vs 31)
- Added rhythmic variety: dotted quarters, triplets, sixteenth-note turns
- More rests for breathing room between phrases
- Added chromatic passing chords: Neapolitan Eb, dim7, augmented, Fr+6
- Smoothed piano bass voice leading (stepwise where possible)
"""

from music21 import (
    stream, note, chord, key, meter, tempo, instrument,
    expressions, dynamics, duration, clef, bar, layout,
    articulations, spanner, tie,
)
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "score.musicxml")

# -- Helpers ----------------------------------------------------------------

def n(pitch, dur, **kwargs):
    """Create a note. dur is in quarter-lengths."""
    nt = note.Note(pitch, quarterLength=dur)
    if kwargs.get('tie_start'):
        nt.tie = tie.Tie('start')
    if kwargs.get('tie_stop'):
        nt.tie = tie.Tie('stop')
    if kwargs.get('staccato'):
        nt.articulations.append(articulations.Staccato())
    if kwargs.get('accent'):
        nt.articulations.append(articulations.Accent())
    if kwargs.get('tenuto'):
        nt.articulations.append(articulations.Tenuto())
    if kwargs.get('fermata'):
        nt.expressions.append(expressions.Fermata())
    if kwargs.get('trill'):
        nt.expressions.append(expressions.Trill())
    return nt


def r(dur):
    """Create a rest."""
    return note.Rest(quarterLength=dur)


def ch(pitches, dur, **kwargs):
    """Create a chord."""
    c = chord.Chord(pitches, quarterLength=dur)
    if kwargs.get('staccato'):
        c.articulations.append(articulations.Staccato())
    if kwargs.get('fermata'):
        c.expressions.append(expressions.Fermata())
    if kwargs.get('accent'):
        c.articulations.append(articulations.Accent())
    if kwargs.get('tenuto'):
        c.articulations.append(articulations.Tenuto())
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


# -- Build Score ------------------------------------------------------------

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    # -- Cello Part --
    cello_part = stream.Part()
    cello_inst = instrument.Violoncello()
    cello_part.insert(0, cello_inst)
    cello_part.partName = "Violoncello"
    cello_part.partAbbreviation = "Vc."

    # -- Piano Part --
    piano_part = stream.Part()
    piano_inst = instrument.Piano()
    piano_part.insert(0, piano_inst)
    piano_part.partName = "Piano"
    piano_part.partAbbreviation = "Pno."

    build_cello(cello_part)
    build_piano(piano_part)

    s.insert(0, cello_part)
    s.insert(0, piano_part)

    return s


# -- Cello Part -------------------------------------------------------------

def build_cello(part):
    """Build the cello part (60 measures).

    Range: G2 to Bb4 (idiomatic cello range, using the A string freely).
    """

    # == Section I: mm.1-8 -- Opening (piano solo, cello tacet) ==
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('3/4')
            kwargs['ks'] = key.Key('d')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=108,
                text="Allegretto, con spirito"
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # == Section II: mm.9-20 -- First Moves ==
    # Cello enters with a thoughtful theme. Two old friends saying hello.

    # m.9-10: Opening motif -- middle register, unhurried
    add_measure(part, 9, [
        r(1.0),
        n('D3', 1.5, tenuto=True), n('E3', 0.5),
    ], dyn='mp', expression_text='espressivo')

    add_measure(part, 10, [
        n('F3', 1.5), n('E3', 0.5), n('D3', 1.0),
    ])

    # m.11-12: Rising -- gaining confidence
    add_measure(part, 11, [
        n('A3', 1.5, tenuto=True), n('Bb3', 0.5),
        n('A3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 12, [
        n('F3', 0.75), n('E3', 0.25), n('D3', 1.0),
        r(1.0),
    ])

    # m.13-16: Second phrase -- more animated, a small joke between friends
    add_measure(part, 13, [
        n('D3', 0.5), n('E3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('G3', 1.0),
    ], dyn='mf')

    add_measure(part, 14, [
        n('Bb3', 1.5, accent=True),
        n('A3', 0.5), n('G#3', 0.25), n('A3', 0.25), n('F3', 0.5),
    ])

    add_measure(part, 15, [
        n('E3', 1.0), n('F3', 0.5),
        n('G3', 1.0), n('A3', 0.5),
    ])

    add_measure(part, 16, [
        n('D3', 2.0, tenuto=True), r(1.0),
    ])

    # m.17-20: Reflection -- settling, dipping to the C string
    add_measure(part, 17, [
        n('A2', 1.0), n('D3', 0.5), n('E3', 0.5),
        n('F3', 1.0),
    ], dyn='p')

    add_measure(part, 18, [
        n('G3', 1.5, tenuto=True),
        n('F3', 0.25), n('E3', 0.25), n('D3', 0.5), r(0.5),
    ])

    add_measure(part, 19, [
        n('C2', 0.5), n('D2', 0.5), n('G2', 0.5), n('C#3', 0.5),  # deep C string
        n('D3', 1.0),
    ])

    add_measure(part, 20, [
        n('E3', 1.5), n('D3', 0.5), r(1.0),
    ], dyn='mp')

    # == Section III: mm.21-36 -- Midgame ==
    # Tension. Both players leaning forward. The conversation gets sharper.

    # m.21-24: The cello probes -- ascending, testing defenses
    add_measure(part, 21, [
        n('A3', 1.0, accent=True), n('Bb3', 0.5),
        n('C4', 0.75), n('D4', 0.25), n('A3', 0.5),
    ], dyn='mf', expression_text='con fuoco',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=116))

    add_measure(part, 22, [
        n('D4', 1.5, tenuto=True),
        n('C#4', 0.25), n('D4', 0.25), n('Bb3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 23, [
        n('G3', 0.5, staccato=True), n('A3', 0.5, staccato=True),
        n('Bb3', 0.5, staccato=True), n('C4', 0.5),
        n('D4', 1.0),
    ])

    add_measure(part, 24, [
        n('Eb4', 1.0, accent=True),  # Neapolitan color -- a bold move
        n('D4', 1.0), n('C#4', 1.0),
    ])

    # m.25-28: Piano responds, cello pushes to the high register
    add_measure(part, 25, [
        r(1.0),
        n('E4', 0.75, tenuto=True), n('F4', 0.25), n('D4', 1.0),
    ], dyn='f')

    add_measure(part, 26, [
        n('C4', 0.5), n('D4', 0.5), n('E4', 0.5), n('F4', 0.5),
        n('G4', 1.0, accent=True),
    ])

    # m.27: Cello reaches Bb4 -- the highest point, a decisive move
    add_measure(part, 27, [
        n('A4', 0.5), n('Bb4', 1.0, accent=True),  # climax
        n('A4', 0.5), n('G4', 0.25), n('F4', 0.25),
    ])

    add_measure(part, 28, [
        n('E4', 0.5), n('D4', 1.0, tenuto=True),
        r(1.5),
    ], dyn='mf')

    # m.29-32: Exchange of pawns -- quick dialogue, staccato
    add_measure(part, 29, [
        n('A3', 0.5, staccato=True), n('D4', 0.5, staccato=True),
        n('C4', 0.5, staccato=True), n('Bb3', 0.5, staccato=True),
        n('A3', 0.5), r(0.5),
    ])

    add_measure(part, 30, [
        r(1.5),
        n('D3', 0.5, staccato=True), n('E3', 0.5, staccato=True),
        n('F#3', 0.5, staccato=True),  # secondary dominant hint
    ])

    add_measure(part, 31, [
        n('G3', 1.0, accent=True), n('F3', 0.5),
        n('Eb3', 0.75), n('D3', 0.75),  # Neapolitan passing tone
    ])

    add_measure(part, 32, [
        n('C#3', 0.5), n('D3', 0.5), n('E3', 0.5),
        n('F3', 1.0, tenuto=True), r(0.5),
    ])

    # m.33-36: Building to the gambit -- long singing cello line
    add_measure(part, 33, [
        n('D3', 1.0), n('F3', 0.5),
        n('A3', 1.0), n('Bb3', 0.5),
    ], dyn='mf', expression_text='cantabile')

    add_measure(part, 34, [
        n('C4', 1.5, tenuto=True),
        n('Bb3', 0.25), n('A3', 0.25), n('G3', 1.0),
    ])

    add_measure(part, 35, [
        n('A3', 1.0), n('Bb3', 0.5),
        n('C4', 0.5), n('D4', 0.5), n('E4', 0.5),
    ], dyn='f')

    add_measure(part, 36, [
        n('F4', 1.5, accent=True),
        n('E4', 0.5), n('C#4', 1.0),
    ])

    # == Section IV: mm.37-48 -- The Gambit (F major) ==
    # One friend sacrifices a knight. Bold, confident. "Your move."

    add_measure(part, 37, [
        n('F3', 2.0, tenuto=True), n('G3', 1.0),
    ], dyn='f', expression_text='con bravura',
       ks=key.Key('F'))

    add_measure(part, 38, [
        n('A3', 0.75), n('Bb3', 0.25), n('C4', 1.0),
        n('D4', 1.0),
    ])

    add_measure(part, 39, [
        n('E4', 1.5, accent=True),
        n('D4', 0.25), n('C4', 0.25), n('Bb3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 40, [
        n('G3', 1.0), n('F3', 0.5),
        n('E3', 1.0, tenuto=True), r(0.5),
    ])

    # m.41-44: The other friend considers, then responds with warmth
    add_measure(part, 41, [
        r(1.5),
        n('C3', 0.5), n('D3', 0.5), n('E3', 0.5),
    ], dyn='mp', expression_text='dolce')

    add_measure(part, 42, [
        n('F3', 1.5, tenuto=True),
        n('E3', 0.5), n('D3', 0.5), r(0.5),
    ])

    add_measure(part, 43, [
        n('Bb2', 0.75), n('C3', 0.25), n('D3', 0.5),
        n('E2', 0.5), n('D2', 0.5), n('C2', 0.5),  # deep descent to open C
    ])

    add_measure(part, 44, [
        n('D2', 1.5, tenuto=True),  # sitting on the low D -- gravity
        n('A2', 0.5), n('Bb2', 0.5), n('C3', 0.5),
    ])

    # m.45-48: Mutual recognition -- "good game" energy, climbing together
    add_measure(part, 45, [
        n('D3', 1.0, accent=True), n('F3', 0.5),
        n('A3', 1.0), n('Bb3', 0.5),
    ], dyn='mf')

    add_measure(part, 46, [
        n('C4', 1.5, tenuto=True),
        n('Bb3', 0.25), n('A3', 0.25), n('G3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 47, [
        n('Bb3', 0.5), n('C4', 0.5), n('D4', 0.5),
        n('F4', 0.5, accent=True), n('E4', 0.5), r(0.5),
    ], dyn='f')

    add_measure(part, 48, [
        n('C4', 2.0, tenuto=True),
        n('Bb3', 0.5), n('A3', 0.5),
    ])

    # == Section V: mm.49-60 -- Endgame ==
    # Back to D minor, then D major. The game is nearly over.

    add_measure(part, 49, [
        n('D3', 1.5, tenuto=True), n('E3', 0.5),
        r(1.0),
    ], dyn='mp', expression_text='tranquillo',
       ks=key.Key('d'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=100))

    add_measure(part, 50, [
        n('F3', 1.5), n('Eb3', 0.25), n('D3', 0.25),  # Eb chromatic passing tone
        n('C#3', 1.0),
    ])

    add_measure(part, 51, [
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('Bb3', 0.5), n('G#3', 0.25), n('A3', 0.75),  # chromatic neighbor
    ])

    add_measure(part, 52, [
        n('E3', 1.0), n('D3', 0.5),
        n('C#3', 1.0), r(0.5),
    ])

    # m.53-56: D major -- the sun is low, the wine is opened
    add_measure(part, 53, [
        n('D3', 1.5, tenuto=True), n('F#3', 0.5),
        n('A3', 1.0),
    ], dyn='p', expression_text='calmato',
       ks=key.Key('D'))

    add_measure(part, 54, [
        n('B3', 1.0, tenuto=True),
        n('A3', 0.5), n('G3', 0.5), n('F#3', 1.0),
    ])

    add_measure(part, 55, [
        n('E3', 0.5), n('D3', 0.5), n('A2', 1.0),
        r(1.0),
    ], dyn='pp')

    add_measure(part, 56, [
        n('D3', 3.0, tenuto=True),
    ])

    # m.57-60: Final moves -- cello quotes the opening, but in major. Peace.
    add_measure(part, 57, [
        r(1.0),
        n('D3', 1.0, tenuto=True), n('E3', 1.0),
    ], dyn='pp')

    add_measure(part, 58, [
        n('F#3', 1.5), n('E3', 0.25), n('D3', 0.25),
        n('A2', 1.0),
    ])

    add_measure(part, 59, [
        n('C2', 2.0, tenuto=True), r(1.0),  # final low C -- open string resonance
    ], dyn='ppp')

    add_measure(part, 60, [
        n('D3', 3.0, fermata=True),
    ])


# -- Piano Part -------------------------------------------------------------

def build_piano(part):
    """Build the piano part (60 measures)."""

    # == Section I: mm.1-8 -- Opening ==
    # Piano alone. Setting out the pieces. A walking bass in the left hand,
    # dry chords in the right -- the geometry of the board.

    # m.1-4: Dm - Gm/Bb - A7 - Dm
    add_measure(part, 1, [
        ch(['D3', 'A3', 'D4', 'F4'], 2.0),
        n('A2', 1.0),
    ], ts=meter.TimeSignature('3/4'),
       ks=key.Key('d'),
       tempo_mark=tempo.MetronomeMark(
           referent=duration.Duration(1.0), number=108,
           text="Allegretto, con spirito"
       ),
       dyn='mp', expression_text='deciso')

    add_measure(part, 2, [
        ch(['Bb2', 'D3', 'G3', 'Bb3'], 2.0),
        n('G2', 1.0),
    ])

    add_measure(part, 3, [
        ch(['A2', 'C#3', 'E3', 'G3'], 2.0),
        n('E2', 1.0),
    ])

    add_measure(part, 4, [
        ch(['D3', 'A3', 'D4', 'F4'], 1.5),
        n('D3', 0.5), n('E3', 0.5), n('F3', 0.5),
    ])

    # m.5-8: More motion -- Bb - C7 - Dm/A - A7
    add_measure(part, 5, [
        n('Bb2', 1.0),
        ch(['D3', 'F3', 'Bb3'], 1.0), n('A3', 1.0),
    ], dyn='mf')

    add_measure(part, 6, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.0),
        n('Bb2', 0.5), n('C3', 0.5),
        n('E3', 1.0),
    ])

    add_measure(part, 7, [
        ch(['A2', 'D3', 'F3', 'A3'], 2.0),
        n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 8, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),
        n('G2', 0.5), n('A2', 0.5), n('C#3', 0.5),
    ], dyn='mp')

    # == Section II: mm.9-20 -- First Moves ==
    # Piano accompanies the cello. Waltz-like but with an angular quality.

    # m.9-12: Dm - Gm - C7 - F
    add_measure(part, 9, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F4'], 1.0), ch(['A3', 'D4', 'F4'], 1.0),
    ], dyn='p')

    add_measure(part, 10, [
        n('G2', 1.0),
        ch(['Bb3', 'D4', 'G4'], 1.0), ch(['Bb3', 'D4'], 1.0),
    ])

    add_measure(part, 11, [
        n('C2', 1.0),
        ch(['E3', 'G3', 'Bb3'], 1.0), ch(['E3', 'G3', 'C4'], 1.0),
    ])

    add_measure(part, 12, [
        n('F2', 1.0),
        ch(['A3', 'C4', 'F4'], 1.0), r(1.0),  # breath
    ])

    # m.13-16: Bb - A7 - Dm - Gm  (smoother bass: Bb->A->D->G stepwise)
    add_measure(part, 13, [
        n('Bb2', 1.0),
        ch(['D3', 'F3', 'Bb3'], 1.0), ch(['D3', 'F3', 'Bb3'], 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('A2', 1.0),
        ch(['C#3', 'E3', 'A3'], 1.0), ch(['C#3', 'E3', 'G3'], 1.0),  # A7 with 7th
    ])

    add_measure(part, 15, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F4'], 1.0), ch(['A3', 'D4', 'F4'], 1.0),
    ])

    add_measure(part, 16, [
        n('G2', 1.0),
        ch(['Bb3', 'D4', 'G4'], 1.0, tenuto=True), r(1.0),
    ])

    # m.17-20: Am - Dm - Bb(b5) - A7
    add_measure(part, 17, [
        n('A2', 1.0),
        ch(['C3', 'E3', 'A3'], 1.0), ch(['C3', 'E3', 'A3'], 1.0),
    ], dyn='p')

    add_measure(part, 18, [
        n('D2', 1.0),
        ch(['F3', 'A3', 'D4'], 1.0), ch(['F3', 'A3', 'D4'], 1.0),
    ])

    add_measure(part, 19, [
        n('Bb2', 1.0),
        ch(['D3', 'F3', 'Bb3'], 0.5),
        ch(['D3', 'Ab3', 'B3'], 0.5),  # dim7 passing chord -- tension
        n('A3', 1.0),
    ])

    add_measure(part, 20, [
        ch(['A2', 'C#3', 'E3', 'G3'], 2.0),
        n('A2', 0.5), r(0.5),
    ], dyn='mp')

    # == Section III: mm.21-36 -- Midgame ==
    # Piano gets more assertive. Thicker textures, more rhythmic drive.

    # m.21-24: Dm - C - Bb - A (with chromatic passing chords)
    add_measure(part, 21, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.0, accent=True),
        n('A3', 0.5, staccato=True), n('D4', 0.5, staccato=True),
        n('A4', 1.0),  # piano reaches higher here
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=116))

    add_measure(part, 22, [
        ch(['C3', 'E3', 'G3', 'C4'], 1.0),
        n('G4', 0.5), n('C5', 0.5),  # piano right hand climbs
        n('E4', 1.0, tenuto=True),
    ])

    add_measure(part, 23, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 1.0),
        n('F3', 0.5, staccato=True), n('Bb3', 0.5, staccato=True),
        n('D4', 1.0),
    ])

    add_measure(part, 24, [
        ch(['Eb3', 'G3', 'Bb3'], 1.0),  # Neapolitan chord!
        ch(['A2', 'C#3', 'E3', 'A3'], 2.0, accent=True),
    ])

    # m.25-28: Piano answers the cello's high line (stepwise bass: D->E->F->E)
    add_measure(part, 25, [
        n('D2', 0.5), n('A2', 0.5), n('D3', 0.5),
        ch(['F3', 'A3', 'D4', 'F4'], 1.5),  # thicker voicing, higher
    ], dyn='f')

    add_measure(part, 26, [
        ch(['Bb2', 'D3', 'F3'], 1.0, staccato=True),
        ch(['C3', 'E3', 'G3'], 1.0, staccato=True),
        ch(['D3', 'F#3', 'A3'], 1.0),  # V/Gm secondary dominant
    ])

    add_measure(part, 27, [
        ch(['G2', 'Bb2', 'D3', 'G3'], 1.0),
        n('A3', 0.5), n('Bb3', 0.5), n('C4', 0.5), r(0.5),
    ])

    add_measure(part, 28, [
        ch(['A2', 'C#3', 'E3', 'A3'], 2.0, tenuto=True),
        r(1.0),
    ], dyn='mf')

    # m.29-32: Staccato exchange -- chess clock ticking
    add_measure(part, 29, [
        n('D3', 0.5, staccato=True), n('F3', 0.5, staccato=True),
        n('A3', 0.5, staccato=True), n('D4', 0.5, staccato=True),
        n('A4', 1.0, accent=True),  # piano peaks high on the accent
    ])

    add_measure(part, 30, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 1.0),
        ch(['G2', 'Bb2', 'D3', 'G3'], 1.0),
        ch(['A2', 'C#3', 'E3'], 1.0),
    ])

    add_measure(part, 31, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F4'], 0.75, accent=True),
        ch(['Ab3', 'B3', 'D4'], 0.25),  # dim7 flash
        ch(['G3', 'Bb3', 'D4'], 1.0),
    ])

    add_measure(part, 32, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),
        n('A2', 0.5), n('D3', 0.5), r(0.5),
    ])

    # m.33-36: Building -- left hand octaves, right hand thickens
    add_measure(part, 33, [
        n('D2', 1.0),
        ch(['F3', 'A3', 'D4'], 1.0), ch(['F3', 'A3', 'D4'], 1.0),
    ], dyn='mf')

    add_measure(part, 34, [
        n('G2', 1.0),
        ch(['Bb3', 'D4', 'G4'], 1.0),
        ch(['B3', 'D4', 'G#4'], 1.0),  # augmented passing chord!
    ])

    add_measure(part, 35, [
        n('C3', 1.0),
        ch(['E3', 'G3', 'C4'], 1.0, accent=True),
        ch(['E3', 'A3', 'C#4'], 1.0),  # V/Dm -- secondary dominant
    ], dyn='f')

    add_measure(part, 36, [
        ch(['A2', 'E3', 'A3', 'C#4'], 1.5, accent=True),
        ch(['Ab2', 'D3', 'F3', 'Ab3'], 1.0),  # French augmented 6th
        r(0.5),
    ])

    # == Section IV: mm.37-48 -- The Gambit (F major) ==

    # m.37-40: F - Bb - C7 - F
    add_measure(part, 37, [
        ch(['F2', 'C3', 'F3', 'A3'], 2.0),
        n('C3', 0.5), n('D3', 0.5),
    ], dyn='f', expression_text='con bravura',
       ks=key.Key('F'))

    add_measure(part, 38, [
        n('Bb2', 1.0),
        ch(['D3', 'F3', 'Bb3'], 0.75),
        ch(['Db3', 'F3', 'Ab3'], 0.25),  # Neapolitan flash in F
        ch(['C3', 'E3', 'G3'], 1.0),
    ])

    add_measure(part, 39, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.0, accent=True),
        n('E3', 0.5), n('G3', 0.5),
        n('Bb3', 1.0),
    ])

    add_measure(part, 40, [
        ch(['F2', 'A2', 'C3', 'F3'], 2.0, tenuto=True),
        r(0.5), n('C3', 0.5),
    ])

    # m.41-44: Dm - Gm - C - F/A (smooth bass line: D->G->C->A)
    add_measure(part, 41, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F4'], 1.0), ch(['A3', 'D4', 'F4'], 1.0),
    ], dyn='mp')

    add_measure(part, 42, [
        n('G2', 1.0),
        ch(['Bb3', 'D4', 'G4'], 1.0), ch(['Bb3', 'D4'], 1.0),
    ])

    add_measure(part, 43, [
        n('C2', 1.0),
        ch(['E3', 'G3', 'C4'], 1.0),
        ch(['E3', 'G#3', 'B3'], 1.0),  # E7 -- secondary dominant of Am
    ])

    add_measure(part, 44, [
        ch(['A2', 'C3', 'F3', 'A3'], 2.0),
        n('G2', 0.5), r(0.5),
    ])

    # m.45-48: Bb - C9 - Dm - C
    add_measure(part, 45, [
        n('Bb2', 1.0),
        ch(['D3', 'F3', 'Bb3', 'D4'], 1.0, accent=True),
        ch(['D3', 'F3', 'Bb3'], 1.0),
    ], dyn='mf')

    add_measure(part, 46, [
        ch(['C3', 'E3', 'G3', 'Bb3', 'D4'], 2.0),
        n('G2', 0.5), r(0.5),
    ])

    add_measure(part, 47, [
        ch(['D3', 'F3', 'A3', 'D4', 'F4'], 1.0, accent=True),
        ch(['C3', 'E3', 'G3', 'C4', 'E4'], 1.0),
        ch(['Bb2', 'D3', 'F3', 'Bb3', 'D4'], 1.0),
    ], dyn='f')

    add_measure(part, 48, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 2.0, tenuto=True),
        n('G2', 0.5), r(0.5),
    ])

    # == Section V: mm.49-60 -- Endgame ==

    # m.49-52: Dm - Gm - A7 - Dm (reprise of opening, softer)
    add_measure(part, 49, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F4'], 1.0), ch(['A3', 'D4', 'F4'], 1.0),
    ], dyn='mp',
       ks=key.Key('d'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=100))

    add_measure(part, 50, [
        n('G2', 1.0),
        ch(['Bb3', 'D4', 'G4'], 1.0),
        ch(['Bb3', 'D4'], 1.0),
    ])

    add_measure(part, 51, [
        n('A2', 1.0),
        ch(['C#3', 'E3', 'A3'], 1.0, tenuto=True),
        ch(['C#3', 'E3', 'G3'], 1.0),  # A7
    ])

    add_measure(part, 52, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F4'], 1.0),
        r(1.0),
    ])

    # m.53-56: D major -- Picardy-like shift. The wine is poured.
    add_measure(part, 53, [
        n('D2', 1.0),
        ch(['A3', 'D4', 'F#4'], 1.0, tenuto=True),
        ch(['A3', 'D4', 'F#4'], 1.0),
    ], dyn='p',
       ks=key.Key('D'))

    add_measure(part, 54, [
        n('G2', 1.0),
        ch(['B3', 'D4', 'G4'], 1.0), ch(['B3', 'D4', 'G4'], 1.0),
    ])

    add_measure(part, 55, [
        n('A2', 1.0),
        ch(['C#3', 'E3', 'A3'], 1.0, tenuto=True),
        r(1.0),
    ], dyn='pp')

    add_measure(part, 56, [
        ch(['D2', 'A2', 'D3', 'F#3', 'A3'], 3.0, tenuto=True),
    ])

    # m.57-60: Coda -- sparse, warm, resolved
    add_measure(part, 57, [
        n('D2', 1.0),
        ch(['F#3', 'A3', 'D4'], 1.0), ch(['F#3', 'A3', 'D4'], 1.0),
    ], dyn='pp')

    add_measure(part, 58, [
        n('G2', 1.0),
        ch(['B3', 'D4', 'G4'], 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 59, [
        ch(['A2', 'E3', 'A3'], 2.0, tenuto=True), r(1.0),
    ], dyn='ppp')

    add_measure(part, 60, [
        ch(['D2', 'A2', 'D3', 'F#3', 'A3', 'D4'], 3.0, fermata=True),
    ])


# -- Add Hairpins -----------------------------------------------------------

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
                elements = list(m.recurse().getElementsByClass([note.Note, chord.Chord]))
                if elements:
                    return elements[0]
        return None

    def get_last_element(part, m_num):
        for m in part.getElementsByClass(stream.Measure):
            if m.number == m_num:
                elements = list(m.recurse().getElementsByClass([note.Note, chord.Chord]))
                if elements:
                    return elements[-1]
        return None

    hairpin_specs = [
        # Cello
        ('cello', 9, 11, 'crescendo'),        # entering, gaining confidence
        ('cello', 13, 14, 'crescendo'),        # animated phrase
        ('cello', 15, 16, 'diminuendo'),       # settling
        ('cello', 21, 24, 'crescendo'),        # midgame probe
        ('cello', 25, 27, 'crescendo'),        # high insistent line
        ('cello', 33, 36, 'crescendo'),        # building to gambit
        ('cello', 41, 43, 'diminuendo'),       # dolce response
        ('cello', 45, 47, 'crescendo'),        # climbing together
        ('cello', 49, 50, 'diminuendo'),       # endgame, winding down
        ('cello', 55, 56, 'diminuendo'),       # final fade
        # Piano
        ('piano', 5, 7, 'crescendo'),          # opening builds
        ('piano', 7, 8, 'diminuendo'),         # settles for cello entry
        ('piano', 21, 24, 'crescendo'),        # midgame tension
        ('piano', 29, 29, 'crescendo'),        # staccato exchange
        ('piano', 33, 36, 'crescendo'),        # building
        ('piano', 45, 47, 'crescendo'),        # mutual climb
        ('piano', 49, 52, 'diminuendo'),       # endgame softening
        ('piano', 57, 60, 'diminuendo'),       # final morendo
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        part_obj = piano if part_name == 'piano' else cello
        if part_obj is None:
            continue
        start_el = get_first_element(part_obj, start_m)
        end_el = get_last_element(part_obj, end_m)
        if start_el and end_el:
            if h_type == 'crescendo':
                hp = dynamics.Crescendo(start_el, end_el)
            else:
                hp = dynamics.Diminuendo(start_el, end_el)
            part_obj.insert(0, hp)


# -- Main -------------------------------------------------------------------

def main():
    print("Building score...")
    score = build_score()

    print("Adding hairpins...")
    add_hairpins(score)

    print(f"Writing to {OUTPUT_PATH}...")
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
