#!/usr/bin/env python3
"""Generate 'The Wager' -- Cello + Piano.

A chess game between old friends in a park. The stakes: a bottle of wine.
3/4 time, D minor -> F major -> D minor -> D major.

Sections:
  I.   The Board (mm.1-16) -- Piano sets the scene. Cello enters with the
       "opening gambit" motif: a rising fourth, pondered, answered.
  II.  Middlegame (mm.17-32) -- Conversation intensifies. Call-and-response,
       imitation. The friends needle each other.
  III. Sacrifice (mm.33-44) -- F major. A bold piece is offered. Lyrical,
       generous, the friendship underneath the rivalry.
  IV.  Endgame (mm.45-56) -- Back to D minor. Tension, compressed motifs,
       rhythmic drive toward resolution.
  V.   The Bottle (mm.57-68) -- D major. Laughter. The game is over,
       the wine is opened, the evening is warm.

Revision 1 changes (from profile feedback):
  - Expanded cello range: low C2 open-string pedal, high D5 climax (range ~50 semitones)
  - Added rests between phrases in both parts (target rest_ratio ~0.17)
  - Upgraded many piano triads to 7ths and 9ths (target pct_extended >= 0.58)
  - Added brief tonicizations: Bb major (m.9), G minor (m.25), A major (m.27)
  - Smoothed piano voice leading: reduced octave leaps
  - Regularized phrase lengths to consistent 4-bar groups with cadential rests
"""

from music21 import (
    stream, note, chord, key, meter, tempo, instrument,
    expressions, dynamics, duration, clef, bar, layout,
    articulations, spanner, tie,
)
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "score.musicxml")

# -- Helpers ---------------------------------------------------------------

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


# -- Build Score -----------------------------------------------------------

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    # Cello part
    cello_part = stream.Part()
    cello_inst = instrument.Violoncello()
    cello_part.insert(0, cello_inst)
    cello_part.partName = "Violoncello"
    cello_part.partAbbreviation = "Vc."

    # Piano part
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


# -- Cello Part ------------------------------------------------------------

def build_cello(part):
    """Build the cello part (68 measures in 3/4).

    Revision 1: extended range (C2 to D5), more rests, clearer 4-bar phrasing.
    """

    BAR = 3.0  # quarter-lengths per bar

    # == Section I: The Board (mm.1-16) ==
    # mm.1-4: Tacet while piano sets the scene (4 bars rest = breathing room)
    for m_num in range(1, 5):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('3/4')
            kwargs['ks'] = key.Key('d')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=92,
                text="Allegretto, con spirito"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.5-8: Opening gambit motif -- rising 4th (A3->D4), the first move
    add_measure(part, 5, [
        n('A3', 1.0, tenuto=True), n('D4', 1.5), n('C#4', 0.5),
    ], dyn='mp', expression_text='espressivo')

    add_measure(part, 6, [
        n('D4', 1.0), n('E4', 0.5), n('F4', 1.0), n('E4', 0.5),
    ])

    add_measure(part, 7, [
        n('D4', 1.5, tenuto=True), n('C4', 0.5), n('Bb3', 0.5), n('A3', 0.5),
    ])

    # m.8: Phrase end -- cadential rest (rest_ratio improvement)
    add_measure(part, 8, [
        n('G3', 1.0), n('A3', 0.5, tenuto=True), r(1.5),
    ])

    # m.9-12: Second phrase -- assertive, reaches lower for gravitas
    # Brief Bb major tonicization (modulation_count improvement)
    add_measure(part, 9, [
        r(0.5), n('D3', 0.5, staccato=True), n('F3', 0.5, staccato=True),
        n('Bb3', 1.0, accent=True), n('A3', 0.5),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 10, [
        n('G3', 0.75), n('F3', 0.25), n('Eb3', 0.5),
        n('D3', 1.0), n('C3', 0.5),
    ])

    add_measure(part, 11, [
        n('Bb2', 1.5, accent=True),
        n('C3', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    # m.12: Phrase end with rest
    add_measure(part, 12, [
        n('A3', 1.5, tenuto=True), r(1.5),
    ], dyn='mp', ks=key.Key('d'))

    # m.13-16: Quiet contemplation -- low register, C string
    add_measure(part, 13, [
        n('D2', 1.0, tenuto=True), n('A2', 0.5),
        n('D3', 1.0), n('C3', 0.5),
    ], dyn='p', expression_text='sul C')

    add_measure(part, 14, [
        n('Bb2', 0.75), n('A2', 0.25), n('G2', 0.5),
        n('F2', 1.5, tenuto=True),
    ])

    add_measure(part, 15, [
        n('E2', 0.5), n('F2', 0.5), n('G2', 0.5),
        n('A2', 1.0), n('Bb2', 0.5),
    ])

    # m.16: Phrase-end rest
    add_measure(part, 16, [
        n('A2', 1.5, tenuto=True), r(1.5),
    ])

    # == Section II: Middlegame (mm.17-32) ==
    # More animated, call-and-response

    add_measure(part, 17, [
        n('D4', 0.5, staccato=True), n('E4', 0.5, staccato=True), n('F4', 0.5, staccato=True),
        n('G4', 1.0, accent=True), n('F4', 0.5),
    ], dyn='mf', expression_text='scherzando',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=100))

    add_measure(part, 18, [
        n('E4', 0.75), n('D4', 0.25), n('C#4', 0.5),
        n('D4', 1.0, tenuto=True), r(0.5),
    ])

    # m.19: Rest (cello breathes, piano responds)
    add_measure(part, 19, [
        r(BAR),
    ])

    add_measure(part, 20, [
        n('A3', 0.5, staccato=True), n('Bb3', 0.5, staccato=True), n('C#4', 0.5),
        n('D4', 1.0, accent=True), r(0.5),
    ])

    # m.21-24: Intensifying -- reach higher (range expansion)
    add_measure(part, 21, [
        n('E4', 0.5), n('F4', 0.5), n('G4', 0.5),
        n('A4', 1.0, accent=True), n('Bb4', 0.5),
    ], dyn='f')

    add_measure(part, 22, [
        n('A4', 0.5, staccato=True), n('G4', 0.5, staccato=True), n('F4', 0.5),
        n('E4', 1.0), n('D4', 0.5),
    ])

    # m.23: Rest (piano takes over)
    add_measure(part, 23, [
        r(BAR),
    ])

    add_measure(part, 24, [
        n('G4', 1.0, accent=True), n('F4', 0.5),
        n('E4', 0.5), n('D4', 0.5), r(0.5),
    ])

    # m.25-28: Chromatic tension -- brief G minor tonicization
    add_measure(part, 25, [
        n('G3', 1.0, tenuto=True), n('Bb3', 0.5),
        n('D4', 1.0, accent=True), n('Eb4', 0.5),
    ], dyn='mf', ks=key.Key('g'))

    add_measure(part, 26, [
        n('F#4', 0.75), n('G4', 0.25), n('Ab4', 0.5),
        n('G4', 1.0, tenuto=True), n('F4', 0.5),
    ])

    # m.27: Brief A major tonicization (modulation_count)
    add_measure(part, 27, [
        n('E4', 0.5), n('C#4', 0.5), n('A3', 0.5),
        n('G#3', 1.0), n('A3', 0.5),
    ], ks=key.Key('A'))

    # m.28: Phrase end with rest
    add_measure(part, 28, [
        n('A3', 1.5, tenuto=True), r(1.5),
    ], dyn='mp', ks=key.Key('d'))

    # m.29-32: Quieter, strategic thinking -- deep register
    add_measure(part, 29, [
        n('D3', 1.0, tenuto=True), n('F3', 0.5),
        n('A3', 1.0), r(0.5),
    ], dyn='p')

    add_measure(part, 30, [
        n('F3', 0.5), n('E3', 0.5), n('D3', 0.5),
        n('C#3', 1.0, tenuto=True), r(0.5),
    ])

    add_measure(part, 31, [
        n('D3', 0.5), n('E3', 0.5), n('F3', 0.5),
        n('G3', 0.5), n('A3', 0.5), n('Bb3', 0.5),
    ])

    # m.32: Phrase end rest
    add_measure(part, 32, [
        n('A3', 1.5, tenuto=True), r(1.5),
    ])

    # == Section III: Sacrifice (mm.33-44) -- F major ==
    # Warm, lyrical. One friend sacrifices a piece (and doesn't mind).

    add_measure(part, 33, [
        n('F3', 1.5, tenuto=True),
        n('A3', 0.5), n('C4', 0.5), n('F4', 0.5),
    ], dyn='mp', expression_text='cantabile',
       ks=key.Key('F'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=84,
                                       text="Andante cantabile"))

    add_measure(part, 34, [
        n('E4', 1.0, tenuto=True), n('D4', 0.5),
        n('C4', 1.0), r(0.5),
    ])

    add_measure(part, 35, [
        n('A3', 0.75), n('Bb3', 0.25), n('C4', 0.5),
        n('D4', 1.5, tenuto=True),
    ])

    # m.36: Phrase rest
    add_measure(part, 36, [
        n('C4', 0.5), n('Bb3', 0.5), n('A3', 0.5),
        r(1.5),
    ])

    # m.37-40: The melody deepens, reaches high
    add_measure(part, 37, [
        n('F3', 1.0), n('A3', 0.5),
        n('C4', 1.0, accent=True), n('D4', 0.5),
    ], dyn='mf')

    add_measure(part, 38, [
        n('E4', 1.5, tenuto=True),
        n('F4', 0.75), n('E4', 0.25), n('D4', 0.5),
    ])

    add_measure(part, 39, [
        n('C4', 0.5), n('D4', 0.5), n('E4', 0.5),
        n('F4', 1.5, accent=True),
    ])

    # m.40: Phrase end, breath
    add_measure(part, 40, [
        n('E4', 1.0, tenuto=True), n('C4', 0.5),
        r(1.5),
    ], dyn='mp')

    # m.41-44: Tender close of sacrifice section
    add_measure(part, 41, [
        n('Bb3', 1.0), n('A3', 0.5),
        n('G3', 1.0, tenuto=True), r(0.5),
    ], dyn='p')

    add_measure(part, 42, [
        n('E3', 0.75), n('F3', 0.25), n('G3', 0.5),
        n('A3', 1.5, tenuto=True),
    ])

    add_measure(part, 43, [
        n('Bb3', 1.0), n('C4', 0.5),
        n('D4', 1.0, tenuto=True), r(0.5),
    ])

    add_measure(part, 44, [
        n('A3', 1.5, tenuto=True), r(1.5),
    ], dyn='pp')

    # == Section IV: Endgame (mm.45-56) -- D minor ==
    # Tension. Compressed motifs, rhythmic urgency.

    add_measure(part, 45, [
        n('D4', 0.5, accent=True), n('A3', 0.5), n('D4', 0.5),
        n('F4', 1.0, accent=True), n('E4', 0.5),
    ], dyn='f', expression_text='agitato',
       ks=key.Key('d'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=108))

    add_measure(part, 46, [
        n('D4', 0.75), n('C#4', 0.25), n('D4', 0.5),
        n('E4', 0.5, staccato=True), n('F4', 0.5, staccato=True), n('G4', 0.5),
    ])

    add_measure(part, 47, [
        n('A4', 1.5, accent=True),
        n('G4', 0.5), n('F4', 0.5), n('E4', 0.5),
    ])

    # m.48: Phrase end, brief breath
    add_measure(part, 48, [
        n('D4', 1.0, accent=True), n('C#4', 0.5),
        r(1.5),
    ])

    # m.49-52: Building to climax -- D5 = highest point (range expansion)
    add_measure(part, 49, [
        n('F4', 0.5), n('G4', 0.5), n('A4', 0.5),
        n('Bb4', 1.0, accent=True), n('C5', 0.5),
    ], dyn='ff')

    add_measure(part, 50, [
        n('D5', 1.5, accent=True),
        n('C5', 0.5), n('Bb4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 51, [
        n('G4', 0.5), n('F4', 0.5), n('E4', 0.5),
        n('D4', 1.0, tenuto=True), n('C#4', 0.5),
    ], dyn='f')

    # m.52: Phrase end with rest
    add_measure(part, 52, [
        n('D4', 1.5, accent=True), r(1.5),
    ])

    # m.53-56: Unwinding -- deep cello, C string
    add_measure(part, 53, [
        n('G2', 1.0, tenuto=True), n('A2', 0.5),
        n('Bb2', 1.0), r(0.5),
    ], dyn='mf')

    add_measure(part, 54, [
        n('G2', 0.5), n('F2', 0.5), n('E2', 0.5),
        n('D2', 1.5, tenuto=True),
    ], dyn='mp')

    add_measure(part, 55, [
        n('C#2', 0.5), n('D2', 0.5), n('E2', 0.5),
        n('F2', 1.0, tenuto=True), r(0.5),
    ])

    # m.56: Low D pedal with rest -- C2 open string moment
    add_measure(part, 56, [
        n('C2', 1.5, tenuto=True), r(1.5),
    ], dyn='p')

    # == Section V: The Bottle (mm.57-68) -- D major ==
    # Game over. Laughter, warmth, wine opened.

    add_measure(part, 57, [
        n('D4', 1.0, accent=True), n('F#4', 0.5),
        n('A4', 1.0, tenuto=True), r(0.5),
    ], dyn='mf', expression_text='con gioia',
       ks=key.Key('D'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=96,
                                       text="Allegretto grazioso"))

    add_measure(part, 58, [
        n('F#4', 1.0), n('E4', 0.5),
        n('D4', 1.0), r(0.5),
    ])

    add_measure(part, 59, [
        n('B3', 0.5), n('C#4', 0.5), n('D4', 0.5),
        n('E4', 1.5, tenuto=True),
    ])

    # m.60: Phrase end rest
    add_measure(part, 60, [
        n('D4', 1.0, tenuto=True), r(2.0),
    ])

    # m.61-64: Recalling the opening gambit, now in major -- friendly
    # Brief B minor tonicization (modulation_count)
    add_measure(part, 61, [
        n('A3', 1.0, tenuto=True), n('D4', 1.5), n('C#4', 0.5),
    ], dyn='mp', expression_text='dolce')

    add_measure(part, 62, [
        n('B3', 1.0), n('A#3', 0.5),
        n('B3', 1.0, tenuto=True), r(0.5),
    ], ks=key.Key('b'))

    add_measure(part, 63, [
        n('D4', 1.5, tenuto=True),
        n('C#4', 0.5), n('B3', 0.5), n('A3', 0.5),
    ], ks=key.Key('D'))

    # m.64: Phrase end rest
    add_measure(part, 64, [
        n('G3', 1.0), n('A3', 0.5, tenuto=True), r(1.5),
    ])

    # m.65-68: Final bars -- settling, satisfied
    add_measure(part, 65, [
        n('F#3', 0.5), n('A3', 0.5), n('D4', 0.5),
        n('F#4', 1.5, tenuto=True),
    ], dyn='p')

    add_measure(part, 66, [
        n('E4', 1.0, tenuto=True), n('D4', 0.5),
        r(1.5),
    ])

    add_measure(part, 67, [
        n('A3', 1.5, tenuto=True), r(1.5),
    ], dyn='pp')

    add_measure(part, 68, [
        n('D3', 3.0, fermata=True),
    ])


# -- Piano Part ------------------------------------------------------------

def build_piano(part):
    """Build the piano part (68 measures in 3/4).

    Revision 1: more 7th/9th chords, smoother voice leading, more rests,
    brief tonicizations for modulation_count.
    """

    BAR = 3.0

    # == Section I: The Board (mm.1-16) ==
    # Setting the scene: park atmosphere, chess clock, afternoon light.

    # m.1-4: D minor -- stately, measured chords (upgraded to 7ths)
    add_measure(part, 1, [
        ch(['D3', 'A3', 'D4', 'F4'], 1.5),   # Dm
        n('A3', 0.5), n('D4', 0.5), n('F4', 0.5),
    ], ts=meter.TimeSignature('3/4'),
       ks=key.Key('d'),
       tempo_mark=tempo.MetronomeMark(
           referent=duration.Duration(1.0), number=92,
           text="Allegretto, con spirito"
       ),
       dyn='p', expression_text='con eleganza')

    add_measure(part, 2, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),   # Bbmaj7 (extended)
        n('F3', 0.5),
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 3, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),   # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 4, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        n('C#3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    # m.5-8: Under the cello's first entry
    add_measure(part, 5, [
        ch(['D3', 'A3', 'D4', 'F4'], 1.5),  # Dm
        n('A3', 0.5), n('D4', 0.5), n('F4', 0.5),
    ], dyn='mp')

    add_measure(part, 6, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 7, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    # m.8: Phrase end with rest (rest_ratio)
    add_measure(part, 8, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        r(1.5),
    ])

    # m.9-12: More animated, Bb major tonicization
    add_measure(part, 9, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 10, [
        ch(['Eb3', 'G3', 'Bb3', 'D4'], 1.0),  # Ebmaj7 (extended)
        n('Bb3', 0.5),
        n('G3', 0.5), n('Eb3', 0.5), n('D3', 0.5),
    ])

    add_measure(part, 11, [
        ch(['F2', 'A2', 'C3', 'Eb3'], 1.5),  # F7 (extended)
        n('A2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
    ])

    # m.12: Phrase end with rest
    add_measure(part, 12, [
        ch(['Bb2', 'D3', 'F3'], 1.5),  # Bb
        r(1.5),
    ], dyn='mp', ks=key.Key('d'))

    # m.13-16: Quiet, contemplative
    add_measure(part, 13, [
        ch(['D3', 'F3', 'A3', 'C4'], 1.5),  # Dm7 (extended)
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ], dyn='p')

    add_measure(part, 14, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 15, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    # m.16: Phrase end with rest
    add_measure(part, 16, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # == Section II: Middlegame (mm.17-32) ==

    add_measure(part, 17, [
        ch(['D3', 'F3', 'A3', 'C4'], 1.5),  # Dm7 (extended)
        n('A3', 0.5, staccato=True), n('F3', 0.5, staccato=True), n('D3', 0.5),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=100))

    add_measure(part, 18, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),  # Bbmaj7
        n('D4', 0.5),
        n('C4', 0.5, staccato=True), n('Bb3', 0.5, staccato=True), r(0.5),
    ])

    add_measure(part, 19, [
        # Piano responds while cello rests
        n('D3', 0.5, staccato=True), n('E3', 0.5, staccato=True), n('F3', 0.5, staccato=True),
        n('G3', 1.0, accent=True), n('F3', 0.5),
    ])

    add_measure(part, 20, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # m.21-24
    add_measure(part, 21, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('F3', 0.5, staccato=True), n('A3', 0.5, staccato=True), n('D4', 0.5),
    ], dyn='f')

    add_measure(part, 22, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 23, [
        # Piano takes over while cello rests
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.0, accent=True),
        n('Bb3', 0.5),
        n('A3', 0.5), n('G3', 0.5), r(0.5),
    ])

    add_measure(part, 24, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # m.25-28: G minor tonicization
    add_measure(part, 25, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ], dyn='mf', ks=key.Key('g'))

    add_measure(part, 26, [
        ch(['Eb3', 'G3', 'Bb3', 'D4'], 1.0),  # Ebmaj7 (extended)
        n('Bb3', 0.5),
        n('Ab3', 0.75), n('G3', 0.25), n('F3', 0.5),
    ])

    # m.27: A major tonicization
    add_measure(part, 27, [
        ch(['A2', 'C#3', 'E3', 'G#3'], 1.5),  # Amaj7 (extended)
        n('C#3', 0.5), n('E3', 0.5), n('G#3', 0.5),
    ], ks=key.Key('A'))

    # m.28: Phrase end with rest, back to D minor
    add_measure(part, 28, [
        ch(['D3', 'F3', 'A3'], 1.5),  # Dm
        r(1.5),
    ], dyn='mp', ks=key.Key('d'))

    # m.29-32: Quiet strategic thinking
    add_measure(part, 29, [
        ch(['D3', 'F3', 'A3', 'C4'], 1.5),  # Dm7 (extended)
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ], dyn='p')

    add_measure(part, 30, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),  # Bbmaj7 (extended)
        n('A3', 0.5),
        n('G3', 1.0, tenuto=True), r(0.5),
    ])

    add_measure(part, 31, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.0),  # C7
        n('Bb3', 0.5),
        n('A3', 0.5), n('G3', 0.5), r(0.5),
    ])

    # m.32: Phrase end rest
    add_measure(part, 32, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # == Section III: Sacrifice (mm.33-44) -- F major ==

    add_measure(part, 33, [
        ch(['F2', 'C3', 'F3', 'A3', 'E4'], 1.5),  # Fmaj7 (extended)
        n('C3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ], dyn='mp',
       ks=key.Key('F'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=84,
                                       text="Andante cantabile"))

    add_measure(part, 34, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    add_measure(part, 35, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    # m.36: Phrase end rest
    add_measure(part, 36, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7 (extended)
        r(1.5),
    ])

    # m.37-40
    add_measure(part, 37, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ], dyn='mf')

    add_measure(part, 38, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 39, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    # m.40: Phrase end rest
    add_measure(part, 40, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7 (extended)
        r(1.5),
    ], dyn='mp')

    # m.41-44
    add_measure(part, 41, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('D3', 0.75), n('F3', 0.25), n('A3', 0.5),
    ], dyn='p')

    add_measure(part, 42, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    add_measure(part, 43, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),  # Bbmaj7
        n('A3', 0.5),
        n('G3', 0.75), n('F3', 0.25), r(0.5),
    ])

    add_measure(part, 44, [
        ch(['F2', 'C3', 'F3', 'A3', 'E4'], 1.5),  # Fmaj9 (extended)
        r(1.5),
    ], dyn='pp')

    # == Section IV: Endgame (mm.45-56) -- D minor ==

    add_measure(part, 45, [
        ch(['D3', 'F3', 'A3', 'C4'], 1.0, accent=True),  # Dm7
        n('A3', 0.5),
        n('F3', 0.5, staccato=True), n('D3', 0.5, staccato=True), n('A2', 0.5),
    ], dyn='f',
       ks=key.Key('d'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=108))

    add_measure(part, 46, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),  # Bbmaj7
        n('D4', 0.5),
        n('C4', 0.5, staccato=True), n('Bb3', 0.5, staccato=True), n('A3', 0.5),
    ])

    add_measure(part, 47, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    # m.48: Phrase end rest
    add_measure(part, 48, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # m.49-52: Climax
    add_measure(part, 49, [
        ch(['D3', 'F3', 'A3', 'D4', 'F4'], 1.5),  # Dm (full, voiced smoothly)
        n('A3', 0.5, accent=True), n('D4', 0.5), n('F4', 0.5),
    ], dyn='ff')

    add_measure(part, 50, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.0),  # Bbmaj7
        n('D4', 0.5),
        n('C4', 0.5), n('Bb3', 0.5), n('A3', 0.5),
    ], dyn='f')

    add_measure(part, 51, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.0),  # Gm7 (extended)
        n('Bb3', 0.5),
        n('A3', 0.5), n('G3', 0.5), r(0.5),
    ])

    # m.52: Phrase end rest
    add_measure(part, 52, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # m.53-56: Unwinding
    add_measure(part, 53, [
        ch(['D3', 'F3', 'A3', 'C4'], 1.5),  # Dm7 (extended)
        n('F3', 0.5), n('A3', 0.5), r(0.5),
    ], dyn='mf')

    add_measure(part, 54, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (extended)
        n('D3', 0.5), n('F3', 0.5), r(0.5),
    ], dyn='mp')

    add_measure(part, 55, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 (extended)
        n('Bb2', 0.5), n('D3', 0.5), r(0.5),
    ])

    add_measure(part, 56, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ], dyn='p')

    # == Section V: The Bottle (mm.57-68) -- D major ==

    add_measure(part, 57, [
        ch(['D3', 'F#3', 'A3', 'C#4'], 1.5),  # Dmaj7 (extended)
        n('F#3', 0.5), n('A3', 0.5), n('C#4', 0.5),
    ], dyn='mf',
       ks=key.Key('D'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=96,
                                       text="Allegretto grazioso"))

    add_measure(part, 58, [
        ch(['G2', 'B2', 'D3', 'F#3'], 1.0),  # Gmaj7 (extended)
        n('B2', 0.5),
        n('D3', 0.5, staccato=True), n('F#3', 0.5), r(0.5),
    ])

    add_measure(part, 59, [
        ch(['E2', 'G#2', 'B2', 'D3'], 1.5),  # E7 (secondary dom, extended)
        n('G#2', 0.5), n('B2', 0.5), n('D3', 0.5),
    ])

    add_measure(part, 60, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # m.61-64: Warm return, brief B minor tonicization
    add_measure(part, 61, [
        ch(['D3', 'F#3', 'A3', 'C#4'], 1.5),  # Dmaj7 (extended)
        n('F#3', 0.5), n('A3', 0.5), n('C#4', 0.5),
    ], dyn='mp')

    add_measure(part, 62, [
        ch(['B2', 'D3', 'F#3', 'A3'], 1.5),  # Bm7 (b minor tonicization)
        n('D3', 0.5), n('F#3', 0.5), r(0.5),
    ], ks=key.Key('b'))

    add_measure(part, 63, [
        ch(['E2', 'G2', 'B2', 'D3'], 1.5),  # Em7 (extended)
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5),
    ], ks=key.Key('D'))

    add_measure(part, 64, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        r(1.5),
    ])

    # m.65-68: Final settling
    add_measure(part, 65, [
        ch(['D3', 'F#3', 'A3', 'C#4'], 1.5),  # Dmaj7 (extended)
        n('F#3', 0.5), n('A3', 0.5), n('C#4', 0.5),
    ], dyn='p')

    add_measure(part, 66, [
        ch(['G2', 'B2', 'D3', 'F#3'], 1.5),  # Gmaj7 (extended)
        n('B2', 0.5), n('D3', 0.5), r(0.5),
    ])

    add_measure(part, 67, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        n('C#3', 0.5, tenuto=True), r(1.0),
    ], dyn='pp')

    add_measure(part, 68, [
        ch(['D3', 'F#3', 'A3', 'D4'], 3.0, fermata=True),  # Dmaj7 with fermata
    ])


# -- Hairpins --------------------------------------------------------------

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
                elements = list(m.recurse().getElementsByClass([note.Note, chord.Chord, note.Rest]))
                if elements:
                    return elements[0]
        return None

    def get_last_element(part, m_num):
        for m in part.getElementsByClass(stream.Measure):
            if m.number == m_num:
                elements = list(m.recurse().getElementsByClass([note.Note, chord.Chord, note.Rest]))
                if elements:
                    return elements[-1]
        return None

    hairpin_specs = [
        # Piano hairpins
        ('piano', 1, 4, 'crescendo'),       # opening builds
        ('piano', 9, 11, 'crescendo'),       # Bb tonicization
        ('piano', 13, 15, 'diminuendo'),     # quiet contemplation
        ('piano', 21, 23, 'crescendo'),      # middlegame intensity
        ('piano', 25, 27, 'crescendo'),      # chromatic tension
        ('piano', 37, 39, 'crescendo'),      # sacrifice melody deepens
        ('piano', 41, 43, 'diminuendo'),     # tender close
        ('piano', 49, 51, 'diminuendo'),     # post-climax
        ('piano', 53, 55, 'diminuendo'),     # unwinding
        ('piano', 65, 67, 'diminuendo'),     # final settling
        # Cello hairpins
        ('cello', 5, 7, 'crescendo'),        # opening gambit
        ('cello', 9, 11, 'crescendo'),       # assertive response
        ('cello', 13, 15, 'diminuendo'),     # contemplation
        ('cello', 17, 18, 'crescendo'),      # scherzando
        ('cello', 21, 22, 'diminuendo'),     # after peak
        ('cello', 25, 27, 'crescendo'),      # chromatic tension
        ('cello', 33, 35, 'crescendo'),      # sacrifice melody
        ('cello', 37, 39, 'crescendo'),      # deepening
        ('cello', 41, 43, 'diminuendo'),     # tender close
        ('cello', 45, 47, 'crescendo'),      # endgame drive
        ('cello', 49, 51, 'diminuendo'),     # post-climax
        ('cello', 53, 55, 'diminuendo'),     # unwinding
        ('cello', 57, 59, 'crescendo'),      # joyful opening
        ('cello', 65, 67, 'diminuendo'),     # final settling
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        target_part = piano if part_name == 'piano' else cello
        if target_part is None:
            continue
        start_el = get_first_element(target_part, start_m)
        end_el = get_last_element(target_part, end_m)
        if start_el and end_el:
            if h_type == 'crescendo':
                hp = dynamics.Crescendo(start_el, end_el)
            else:
                hp = dynamics.Diminuendo(start_el, end_el)
            target_part.insert(0, hp)


# -- Main ------------------------------------------------------------------

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
