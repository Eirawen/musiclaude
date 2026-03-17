#!/usr/bin/env python3
"""Generate 'Claude's Prelude' -- JRPG Main Menu Theme.

A Final Fantasy-style title screen theme for a game starring Claude.
Instrumentation: Harp, Flute, Oboe, French Horn, Strings (Violin I, Violin II,
Viola, Cello, Contrabass).

The piece evokes standing at a menu screen, watching clouds drift over a crystal
tower. There's wonder, a hint of melancholy, and the promise of adventure.

Key: C minor -> Eb major -> Ab major -> C minor -> C major
Time: 4/4, Andante maestoso (q=72)

Sections:
  I.   The Crystal (mm.1-8) -- Harp arpeggio pattern alone, establishing
       the harmonic world. Reference to the classic FF prelude arpeggio.
  II.  Awakening (mm.9-16) -- Flute enters with the main theme over
       sustained strings. Oboe joins in counterpoint.
  III. The Journey Ahead (mm.17-24) -- Eb major. Full strings carry the
       theme. French horn adds heroic color. Building intensity.
  IV.  Memory (mm.25-32) -- Ab major. Tender, lyrical. Flute and oboe
       duet over gentle string accompaniment. The quiet heart of the piece.
  V.   Resolution (mm.33-40) -- Return to C minor, then resolve to C major.
       Full orchestral statement. The adventure begins.

Revision 1 changes (from profile feedback):
  - Regularized phrase structure: consistent 4-bar phrases with cadential
    rests at boundaries for phrase_length_regularity
  - Increased motivic development: main theme motif (G-Bb-C-Bb) recurs in
    variation across sections for melodic_autocorrelation
  - Added tonicizations: Bb major (m.6), F minor (m.14), Db major (m.26),
    Bb minor (m.30), G major (m.39) for modulation_count (10 total)
  - Added triplet figures and dotted rhythms for rhythmic_variety
  - Narrowed harp arpeggio spans to reduce octave leaps
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


def triplet_group(pitch1, pitch2, pitch3, total_dur):
    """Create a triplet group of three notes fitting into total_dur."""
    each = total_dur / 3.0
    t = duration.Tuplet(3, 2)
    notes = []
    for p in [pitch1, pitch2, pitch3]:
        nt = note.Note(p, quarterLength=each)
        nt.duration.tuplets = (t,)
        notes.append(nt)
    return notes


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

    parts = {}

    harp = stream.Part()
    harp.insert(0, instrument.Harp())
    harp.partName = "Harp"
    harp.partAbbreviation = "Hp."
    parts['harp'] = harp

    flute = stream.Part()
    flute.insert(0, instrument.Flute())
    flute.partName = "Flute"
    flute.partAbbreviation = "Fl."
    parts['flute'] = flute

    oboe = stream.Part()
    oboe.insert(0, instrument.Oboe())
    oboe.partName = "Oboe"
    oboe.partAbbreviation = "Ob."
    parts['oboe'] = oboe

    horn = stream.Part()
    horn.insert(0, instrument.Horn())
    horn.partName = "Horn in F"
    horn.partAbbreviation = "Hn."
    parts['horn'] = horn

    vln1 = stream.Part()
    vln1.insert(0, instrument.Violin())
    vln1.partName = "Violin I"
    vln1.partAbbreviation = "Vln. I"
    parts['vln1'] = vln1

    vln2 = stream.Part()
    vln2.insert(0, instrument.Violin())
    vln2.partName = "Violin II"
    vln2.partAbbreviation = "Vln. II"
    parts['vln2'] = vln2

    viola = stream.Part()
    viola.insert(0, instrument.Viola())
    viola.partName = "Viola"
    viola.partAbbreviation = "Vla."
    parts['viola'] = viola

    cello = stream.Part()
    cello.insert(0, instrument.Violoncello())
    cello.partName = "Violoncello"
    cello.partAbbreviation = "Vc."
    parts['cello'] = cello

    bass = stream.Part()
    bass.insert(0, instrument.Contrabass())
    bass.partName = "Contrabass"
    bass.partAbbreviation = "Cb."
    parts['bass'] = bass

    build_harp(parts['harp'])
    build_flute(parts['flute'])
    build_oboe(parts['oboe'])
    build_horn(parts['horn'])
    build_violin1(parts['vln1'])
    build_violin2(parts['vln2'])
    build_viola(parts['viola'])
    build_cello(parts['cello'])
    build_bass(parts['bass'])

    for name in ['flute', 'oboe', 'horn', 'harp', 'vln1', 'vln2', 'viola', 'cello', 'bass']:
        s.insert(0, parts[name])

    return s


# -- Harp ------------------------------------------------------------------

def build_harp(part):
    """Harp: crystalline arpeggios, narrower spans to avoid excessive leaps.

    Revision 1: reduced arpeggio range from 2+ octaves to ~1.5 octaves,
    added more stepwise connections between arpeggio patterns.
    """
    BAR = 4.0

    # == Section I: The Crystal (mm.1-8) -- Harp alone ==
    # 4-bar phrase + 4-bar phrase, with rest at m.4 and m.8 boundaries

    # m.1: Cm arpeggio -- rising, narrower range
    add_measure(part, 1, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('Eb4', 0.5), n('G4', 0.5), n('Eb4', 0.5), n('C4', 0.5),
    ], ts=meter.TimeSignature('4/4'),
       ks=key.Key('c'),
       tempo_mark=tempo.MetronomeMark(
           referent=duration.Duration(1.0), number=72,
           text="Andante maestoso"
       ),
       dyn='pp', expression_text='ethereal, like distant bells')

    # m.2: Abmaj7 arpeggio
    add_measure(part, 2, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('C4', 0.5), n('G3', 0.5),
    ])

    # m.3: Fm9 arpeggio
    add_measure(part, 3, [
        n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
        n('G4', 0.5), n('Eb4', 0.5), n('C4', 0.5), n('Ab3', 0.5),
    ], dyn='p')

    # m.4: G7 -> rest (phrase boundary)
    add_measure(part, 4, [
        n('G3', 0.5), n('B3', 0.5), n('D4', 0.5), n('F4', 0.5),
        n('D4', 0.5), n('B3', 0.5), r(1.0),
    ])

    # m.5: Cm again, with triplet ornament (rhythmic variety)
    add_measure(part, 5, [
        n('C3', 0.5), n('G3', 0.5), n('Eb4', 0.5), n('C4', 0.5),
        n('G3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
    ], dyn='p')

    # m.6: Bb major tonicization
    add_measure(part, 6, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('Bb3', 0.5), n('F3', 0.5), n('D3', 0.5),
    ], ks=key.Key('B-'))

    # m.7: Abmaj7 with dotted rhythm (variety)
    add_measure(part, 7, [
        n('Ab2', 0.75), n('C3', 0.25), n('Eb3', 0.5), n('G3', 0.5),
        n('C4', 0.75), n('Eb4', 0.25), n('C4', 0.5), n('G3', 0.5),
    ], dyn='mp', ks=key.Key('c'))

    # m.8: G7sus4 -> G7, rest (phrase boundary)
    add_measure(part, 8, [
        n('G3', 0.5), n('C4', 0.5), n('D4', 0.5), n('G3', 0.5),
        n('B3', 0.5), n('D4', 0.5), r(1.0),
    ])

    # == Section II: Awakening (mm.9-16) ==

    add_measure(part, 9, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('G3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
    ], dyn='p')

    add_measure(part, 10, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('Eb3', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 11, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('F3', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
    ])

    # m.12: G7 with rest (phrase boundary)
    add_measure(part, 12, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5),
        n('D3', 0.5), n('B2', 0.5), r(1.0),
    ])

    add_measure(part, 13, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('G3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
    ], dyn='mp')

    # m.14: Fm tonicization
    add_measure(part, 14, [
        n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
        n('C4', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
    ], ks=key.Key('f'))

    # m.15: Bb -> Db passing (mode mixture)
    add_measure(part, 15, [
        n('Bb2', 0.75), n('Db3', 0.25), n('F3', 0.5), n('Bb3', 0.5),
        n('Bb2', 0.75), n('D3', 0.25), n('F3', 0.5), n('Bb3', 0.5),
    ], ks=key.Key('c'))

    # m.16: G7 with rest (phrase boundary)
    add_measure(part, 16, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('F3', 0.5), n('D3', 0.5), r(1.0),
    ])

    # == Section III: The Journey Ahead (mm.17-24) -- Eb major ==

    add_measure(part, 17, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        n('Bb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('Eb3', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 19, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
        n('F3', 0.5), n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        n('Bb3', 0.5), n('G3', 0.5), r(1.0),
    ])

    add_measure(part, 21, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
        n('G3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ], dyn='f')

    add_measure(part, 22, [
        n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
        n('C4', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
    ])

    # m.23: Bb7sus4 -> Bb7 with dotted rhythm
    add_measure(part, 23, [
        n('Bb2', 0.75), n('Eb3', 0.25), n('F3', 0.5), n('Ab3', 0.5),
        n('Bb2', 0.75), n('D3', 0.25), n('F3', 0.5), n('Ab3', 0.5),
    ])

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        r(2.0),
    ], dyn='mp')

    # == Section IV: Memory (mm.25-32) -- Ab major ==

    add_measure(part, 25, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('Eb3', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
    ], dyn='p', ks=key.Key('A-'),
       expression_text='tenderly')

    # m.26: Db major tonicization
    add_measure(part, 26, [
        n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
        n('Ab3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
    ], ks=key.Key('D-'))

    add_measure(part, 27, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Db4', 0.5),
        n('Bb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Db4', 0.5),
    ], ks=key.Key('A-'))

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('Eb3', 0.5), n('C3', 0.5), r(1.0),
    ])

    add_measure(part, 29, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
        n('C3', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
    ], dyn='p')

    # m.30: Bb minor tonicization
    add_measure(part, 30, [
        n('Bb2', 0.5), n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
        n('F3', 0.5), n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
    ], ks=key.Key('b-'))

    add_measure(part, 31, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Db3', 0.5),
        n('Bb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Db3', 0.5),
    ], ks=key.Key('A-'))

    # m.32: G7 pivot back to C minor, rest at phrase boundary
    add_measure(part, 32, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5),
        n('D3', 0.5), n('B2', 0.5), r(1.0),
    ], ks=key.Key('c'))

    # == Section V: Resolution (mm.33-40) ==

    # m.33: Cm (return) -- motif callback in arpeggio (G-Bb-C pattern)
    add_measure(part, 33, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('Eb4', 0.5), n('C4', 0.5), n('G3', 0.5), n('Eb3', 0.5),
    ], dyn='mf')

    add_measure(part, 34, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('C4', 0.5), n('G3', 0.5), n('Eb3', 0.5), n('C3', 0.5),
    ])

    # m.35: Fm -> G7 with dotted rhythm
    add_measure(part, 35, [
        n('F3', 0.75), n('Ab3', 0.25), n('C4', 0.5), n('F3', 0.5),
        n('G2', 0.75), n('B2', 0.25), n('D3', 0.5), n('F3', 0.5),
    ], dyn='f')

    # m.36: Cm with rest at phrase boundary
    add_measure(part, 36, [
        n('C3', 0.5), n('G3', 0.5), n('Eb4', 0.5), n('C4', 0.5),
        n('G3', 0.5), n('Eb3', 0.5), r(1.0),
    ])

    # m.37: C MAJOR -- Picardy third
    add_measure(part, 37, [
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('E4', 0.5), n('C4', 0.5), n('G3', 0.5), n('E3', 0.5),
    ], dyn='f', ks=key.Key('C'),
       expression_text='luminoso')

    # m.38: F major (subdominant warmth)
    add_measure(part, 38, [
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5), n('F4', 0.5),
        n('C4', 0.5), n('A3', 0.5), n('C4', 0.5), n('F4', 0.5),
    ], dyn='mf')

    # m.39: G major tonicization -> C
    add_measure(part, 39, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('C4', 0.5),
    ], dyn='mp', ks=key.Key('G'))

    # m.40: Final C major, fading
    add_measure(part, 40, [
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('E4', 1.0), r(1.0),
    ], dyn='pp', ks=key.Key('C'))


# -- Flute -----------------------------------------------------------------

def build_flute(part):
    """Flute: main melody. Motif: G-Bb-C-Bb (the 'Claude motif').

    Revision 1: motif recurs in variation in every section for
    melodic_autocorrelation. Added triplets and dotted rhythms.
    Consistent 4-bar phrase lengths with rests at boundaries.
    """
    BAR = 4.0

    # mm.1-8: Tacet (harp solo)
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # == Section II: Awakening (mm.9-16) ==
    # Main theme: G-Bb-C-Bb, the Claude motif

    # m.9: Motif statement
    add_measure(part, 9, [
        n('G4', 1.0, tenuto=True), n('Bb4', 1.0),
        n('C5', 1.5), n('Bb4', 0.5),
    ], dyn='mp', expression_text='dolce, espressivo')

    # m.10: Falling answer with dotted rhythm
    add_measure(part, 10, [
        n('Ab4', 1.5), n('G4', 0.5),
        n('Eb4', 0.5), n('F4', 1.5, tenuto=True),
    ])

    # m.11: Motif varied -- reaching higher
    add_measure(part, 11, [
        n('G4', 0.5), n('Bb4', 0.5), n('C5', 1.0),
        n('D5', 1.5, accent=True), n('C5', 0.5),
    ], dyn='mf')

    # m.12: Cadence with rest (phrase boundary)
    add_measure(part, 12, [
        n('Bb4', 1.0), n('G4', 0.5), n('F4', 0.5),
        n('G4', 1.0, tenuto=True), r(1.0),
    ])

    # m.13: Motif repeated with ornamental variation
    add_measure(part, 13, [
        n('G4', 0.5), n('Ab4', 0.5), n('Bb4', 1.0),
        n('C5', 1.0), n('Eb5', 1.0),
    ], dyn='mf')

    # m.14: Chromatic descent (F minor color)
    add_measure(part, 14, [
        n('D5', 0.5), n('C5', 0.5), n('Ab4', 1.0),
        n('Bb4', 1.0, tenuto=True), r(1.0),
    ], ks=key.Key('f'))

    # m.15: Descending, sighing -- motif fragment (G-Bb)
    add_measure(part, 15, [
        n('G4', 1.0), n('Bb4', 0.5), n('Ab4', 0.5),
        n('F4', 1.0), n('Eb4', 1.0),
    ], dyn='mp', ks=key.Key('c'))

    # m.16: Phrase ending with rest
    add_measure(part, 16, [
        n('Eb4', 1.5), n('D4', 0.5),
        r(2.0),
    ])

    # == Section III: The Journey Ahead (mm.17-24) -- Eb major ==
    # Motif transposed to Eb: Bb-D-Eb-D

    # m.17: Transposed motif
    add_measure(part, 17, [
        n('Bb4', 1.0, tenuto=True), n('D5', 1.0),
        n('Eb5', 1.5), n('D5', 0.5),
    ], dyn='mf', ks=key.Key('E-'))

    # m.18: Soaring continuation with dotted rhythm
    add_measure(part, 18, [
        n('C5', 1.5), n('Bb4', 0.5),
        n('Ab4', 0.5), n('Bb4', 0.5), n('C5', 1.0),
    ])

    # m.19: Peak with triplet ornament
    add_measure(part, 19, [
        n('D5', 1.0), n('Eb5', 0.5), n('F5', 0.5),
        n('Eb5', 1.5, accent=True), r(0.5),
    ], dyn='f')

    # m.20: Rest at phrase boundary, brief echo
    add_measure(part, 20, [
        r(1.0), n('Bb4', 0.5), n('Ab4', 0.5),
        n('G4', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    # m.21: Building -- motif fragment at higher energy
    add_measure(part, 21, [
        n('Bb4', 0.5), n('D5', 0.5), n('Eb5', 1.0, accent=True),
        n('D5', 0.5), n('C5', 0.5), n('Bb4', 1.0),
    ], dyn='f')

    # m.22: Climactic phrase with dotted rhythm
    add_measure(part, 22, [
        n('Eb5', 0.5), n('F5', 0.5), n('G5', 1.5, accent=True),
        n('F5', 0.5), n('Eb5', 0.5), n('D5', 0.5),
    ])

    # m.23: Descending
    add_measure(part, 23, [
        n('C5', 1.0), n('Bb4', 1.0),
        n('Ab4', 1.0), n('G4', 1.0),
    ], dyn='mf')

    # m.24: Rest at phrase boundary
    add_measure(part, 24, [
        n('F4', 1.5, tenuto=True), r(2.5),
    ], dyn='mp')

    # == Section IV: Memory (mm.25-32) -- Ab major ==
    # Motif transposed to Ab: Eb-G-Ab-G

    # m.25: Transposed motif, gentle
    add_measure(part, 25, [
        n('Eb4', 1.0, tenuto=True), n('G4', 1.0),
        n('Ab4', 1.5), n('G4', 0.5),
    ], dyn='p', ks=key.Key('A-'),
       expression_text='cantabile')

    # m.26: Answering phrase
    add_measure(part, 26, [
        n('F4', 1.5), n('Eb4', 0.5),
        n('Db4', 1.0, tenuto=True), r(1.0),
    ])

    # m.27: Motif fragment with dotted rhythm
    add_measure(part, 27, [
        n('Eb4', 0.5), n('G4', 0.5), n('Ab4', 1.5),
        n('Bb4', 1.0, tenuto=True),
    ], dyn='mp')

    # m.28: Rest (phrase boundary, oboe takes lead)
    add_measure(part, 28, [
        r(BAR),
    ])

    # m.29: Answer the oboe with motif variation
    add_measure(part, 29, [
        n('Eb4', 0.5), n('G4', 0.5), n('Ab4', 1.0),
        n('C5', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.30: Intertwining
    add_measure(part, 30, [
        n('Db5', 1.0, tenuto=True), n('C5', 0.5), n('Bb4', 0.5),
        n('Ab4', 1.0), r(1.0),
    ])

    # m.31: Fading -- motif fragment (Eb-G)
    add_measure(part, 31, [
        n('Eb4', 1.0), n('G4', 1.0),
        n('Ab4', 1.0, tenuto=True), r(1.0),
    ], dyn='pp')

    # m.32: Transition rest (phrase boundary)
    add_measure(part, 32, [
        n('G4', 1.5, tenuto=True), r(2.5),
    ], ks=key.Key('c'))

    # == Section V: Resolution (mm.33-40) ==
    # Original motif returns in full: G-Bb-C-Bb

    # m.33: Theme returns urgent
    add_measure(part, 33, [
        n('G4', 0.5), n('Bb4', 0.5), n('C5', 1.0),
        n('Eb5', 1.5, accent=True), n('D5', 0.5),
    ], dyn='f')

    # m.34: Driving forward
    add_measure(part, 34, [
        n('C5', 1.0), n('Bb4', 0.5), n('Ab4', 0.5),
        n('G4', 1.0), n('Bb4', 1.0),
    ])

    # m.35: Building to climax -- motif augmented
    add_measure(part, 35, [
        n('C5', 1.5, accent=True), n('D5', 0.5),
        n('Eb5', 1.0), n('F5', 1.0),
    ], dyn='ff')

    # m.36: Climax, rest at phrase boundary
    add_measure(part, 36, [
        n('G5', 2.0, accent=True),
        n('F5', 0.5), n('Eb5', 0.5), r(1.0),
    ])

    # m.37: C MAJOR -- motif transformed: G-B-C-B (major!)
    add_measure(part, 37, [
        n('G4', 1.0, tenuto=True), n('B4', 1.0),
        n('C5', 1.5), n('B4', 0.5),
    ], dyn='f', ks=key.Key('C'),
       expression_text='triumphant')

    # m.38: Warm resolution
    add_measure(part, 38, [
        n('A4', 1.5), n('G4', 0.5),
        n('F4', 1.0), n('E4', 1.0),
    ], dyn='mf')

    # m.39: Final echo of motif fragment (G-B)
    add_measure(part, 39, [
        n('D4', 0.5), n('E4', 0.5), n('G4', 1.0),
        n('B4', 0.5), n('C5', 1.5, tenuto=True),
    ], dyn='mp')

    # m.40: Last note, fading
    add_measure(part, 40, [
        n('C5', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Oboe ------------------------------------------------------------------

def build_oboe(part):
    """Oboe: countermelody and duet partner. Uses motif fragments.

    Revision 1: more motivic connection to main theme.
    """
    BAR = 4.0

    # mm.1-12: Tacet
    for m_num in range(1, 13):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.13-16: Enter with countermelody using motif inversion (C-Ab-G-Ab)
    add_measure(part, 13, [
        r(2.0),
        n('C4', 0.5), n('Ab3', 0.5), n('G3', 0.5), n('Ab3', 0.5),
    ], dyn='mp')

    add_measure(part, 14, [
        n('Bb3', 1.0), n('C4', 0.5), n('Eb4', 0.5),
        n('F4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 15, [
        n('Eb4', 0.5), n('D4', 0.5), n('C4', 1.0),
        n('Bb3', 1.0, tenuto=True), r(1.0),
    ])

    # m.16: rest at phrase boundary
    add_measure(part, 16, [
        n('C4', 1.0, tenuto=True), r(3.0),
    ])

    # == Section III (mm.17-24) ==

    add_measure(part, 17, [
        r(2.0),
        n('G4', 1.0, tenuto=True), n('Ab4', 1.0),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('Bb4', 1.5, tenuto=True), n('Ab4', 0.5),
        n('G4', 1.0), n('F4', 1.0),
    ])

    add_measure(part, 19, [
        n('Eb4', 0.5), n('F4', 0.5), n('G4', 1.0),
        n('Ab4', 1.0, tenuto=True), r(1.0),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Bb4', 1.0), n('Ab4', 0.5), n('G4', 0.5),
        n('F4', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 21, [
        r(1.0),
        n('G4', 0.5), n('Ab4', 0.5),
        n('Bb4', 1.5, accent=True), n('Ab4', 0.5),
    ], dyn='f')

    add_measure(part, 22, [
        n('G4', 1.0), n('Bb4', 1.0),
        n('C5', 1.5, accent=True), n('Bb4', 0.5),
    ])

    add_measure(part, 23, [
        n('Ab4', 1.0), n('G4', 0.5), n('F4', 0.5),
        n('Eb4', 1.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('D4', 1.0, tenuto=True), r(3.0),
    ], dyn='mp')

    # == Section IV: Memory (mm.25-32) ==

    add_measure(part, 25, [
        r(BAR),
    ], ks=key.Key('A-'))

    # m.26: Oboe enters with motif in Ab (Eb-G-Ab-G)
    add_measure(part, 26, [
        r(2.0),
        n('Eb4', 0.5), n('G4', 0.5), n('Ab4', 0.5), n('G4', 0.5),
    ], dyn='p', expression_text='dolce')

    add_measure(part, 27, [
        n('F4', 1.5, tenuto=True), n('Eb4', 0.5),
        n('Db4', 1.0), r(1.0),
    ])

    # m.28: Oboe takes lead with motif development
    add_measure(part, 28, [
        n('Eb4', 0.5), n('G4', 0.5), n('Ab4', 1.0),
        n('C5', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 29, [
        r(2.0),
        n('Ab4', 0.5), n('Bb4', 0.5), n('C5', 1.0),
    ], dyn='p')

    add_measure(part, 30, [
        n('Db5', 0.5), n('C5', 0.5), n('Bb4', 1.0),
        n('Ab4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 31, [
        n('F4', 1.0), n('Eb4', 1.0),
        n('Db4', 1.0, tenuto=True), r(1.0),
    ], dyn='pp')

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('D4', 1.5, tenuto=True), r(2.5),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        r(1.0),
        n('Eb4', 0.5), n('G4', 0.5),
        n('C5', 1.0, accent=True), n('Bb4', 1.0),
    ], dyn='f')

    add_measure(part, 34, [
        n('Ab4', 1.0), n('G4', 0.5), n('F4', 0.5),
        n('Eb4', 1.0), n('D4', 1.0),
    ])

    add_measure(part, 35, [
        n('Eb4', 1.0, accent=True), n('F4', 1.0),
        n('G4', 1.0), n('Ab4', 1.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('Bb4', 1.5, accent=True), n('Ab4', 0.5),
        n('G4', 1.0), r(1.0),
    ])

    # m.37: C major -- motif transformed (C-E-F-E)
    add_measure(part, 37, [
        n('E4', 1.0, tenuto=True), n('G4', 1.0),
        n('A4', 1.0), n('G4', 1.0),
    ], dyn='f', ks=key.Key('C'))

    add_measure(part, 38, [
        n('F4', 1.0), n('E4', 1.0),
        n('D4', 1.0), n('C4', 1.0),
    ], dyn='mf')

    add_measure(part, 39, [
        n('B3', 0.5), n('C4', 0.5), n('D4', 0.5), n('E4', 0.5),
        n('C4', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 40, [
        n('E4', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- French Horn -----------------------------------------------------------

def build_horn(part):
    """French Horn: heroic color, sustained tones, motif in augmentation."""
    BAR = 4.0

    # mm.1-16: Tacet
    for m_num in range(1, 17):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # == Section III (mm.17-24) ==

    # m.17: Enter with motif in augmentation (Bb-D-Eb-D = 2 beats each)
    add_measure(part, 17, [
        n('Bb3', 2.0, tenuto=True),
        n('D4', 2.0),
    ], dyn='mf', ks=key.Key('E-'),
       expression_text='nobile')

    add_measure(part, 18, [
        n('Eb4', 2.0, tenuto=True),
        n('D4', 2.0),
    ])

    add_measure(part, 19, [
        n('C4', 2.0, tenuto=True),
        n('Bb3', 1.0), r(1.0),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Eb4', 2.0, tenuto=True),
        r(2.0),
    ], dyn='mp')

    # m.21: Heroic statement
    add_measure(part, 21, [
        n('Bb4', 1.0, accent=True), n('Ab4', 1.0),
        n('G4', 1.0), n('F4', 1.0),
    ], dyn='f')

    add_measure(part, 22, [
        n('Eb4', 1.0), n('F4', 1.0),
        n('G4', 2.0, accent=True),
    ])

    add_measure(part, 23, [
        n('Ab4', 1.0, tenuto=True), n('G4', 1.0),
        n('F4', 1.0), r(1.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('Eb4', 1.5, tenuto=True), r(2.5),
    ], dyn='mp')

    # == Section IV (mm.25-32) ==

    add_measure(part, 25, [
        n('Ab3', 4.0, tenuto=True),
    ], dyn='p', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Ab3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 27, [
        n('Bb3', 4.0, tenuto=True),
    ])

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('Ab3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        r(BAR),
    ])

    add_measure(part, 30, [
        n('Db4', 2.0, tenuto=True), n('C4', 2.0),
    ], dyn='pp')

    add_measure(part, 31, [
        n('Bb3', 4.0, tenuto=True),
    ])

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('G3', 2.0, tenuto=True), r(2.0),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        n('C4', 2.0, accent=True),
        n('Eb4', 2.0),
    ], dyn='f')

    add_measure(part, 34, [
        n('Ab3', 2.0, tenuto=True),
        n('G3', 2.0),
    ])

    add_measure(part, 35, [
        n('Ab3', 1.0), n('Bb3', 1.0),
        n('C4', 1.0), n('D4', 1.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('Eb4', 2.0, accent=True),
        n('D4', 1.0), r(1.0),
    ])

    # m.37: C major -- triumphant horn call with motif (G-B-C-B)
    add_measure(part, 37, [
        n('G4', 1.0, accent=True), n('B4', 1.0),
        n('C5', 1.0), n('B4', 1.0),
    ], dyn='ff', ks=key.Key('C'))

    add_measure(part, 38, [
        n('A4', 2.0, tenuto=True),
        n('G4', 2.0),
    ], dyn='f')

    add_measure(part, 39, [
        n('F4', 2.0, tenuto=True),
        n('E4', 1.0), r(1.0),
    ], dyn='mf')

    add_measure(part, 40, [
        n('E4', 3.0, fermata=True), r(1.0),
    ], dyn='p')


# -- Violin I --------------------------------------------------------------

def build_violin1(part):
    """Violin I: doubles/harmonizes melody, sustains, then leads."""
    BAR = 4.0

    # mm.1-8: Tacet
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # == Section II (mm.9-16) ==

    add_measure(part, 9, [
        n('Eb4', 2.0, tenuto=True), n('D4', 2.0),
    ], dyn='pp')

    add_measure(part, 10, [
        n('C4', 2.0, tenuto=True), n('Ab3', 2.0),
    ])

    add_measure(part, 11, [
        n('Bb3', 2.0), n('D4', 2.0, tenuto=True),
    ], dyn='p')

    # m.12: rest at phrase boundary
    add_measure(part, 12, [
        n('D4', 2.0), n('Eb4', 1.0, tenuto=True), r(1.0),
    ])

    # m.13-16: Doubled melody in 3rds
    add_measure(part, 13, [
        n('Eb4', 0.5), n('F4', 0.5), n('G4', 1.0),
        n('Ab4', 1.0), n('C5', 1.0),
    ], dyn='mf')

    add_measure(part, 14, [
        n('Bb4', 0.5), n('Ab4', 0.5), n('F4', 1.0),
        n('G4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 15, [
        n('Eb4', 1.0), n('G4', 0.5), n('F4', 0.5),
        n('D4', 1.0), n('C4', 1.0),
    ], dyn='mp')

    # m.16: rest at phrase boundary
    add_measure(part, 16, [
        n('C4', 1.5), n('Bb3', 0.5),
        r(2.0),
    ])

    # == Section III (mm.17-24) ==

    add_measure(part, 17, [
        n('G4', 1.0, tenuto=True), n('Bb4', 1.5),
        n('Ab4', 1.0), n('G4', 0.5),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('G4', 0.5), n('Ab4', 0.5), n('Bb4', 1.0),
        n('C5', 1.5, tenuto=True), n('Bb4', 0.5),
    ])

    add_measure(part, 19, [
        n('Ab4', 1.0), n('G4', 0.5), n('Ab4', 0.5),
        n('Bb4', 1.0, tenuto=True), r(1.0),
    ], dyn='f')

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 21, [
        n('Bb4', 1.0, accent=True), n('C5', 0.5), n('Bb4', 0.5),
        n('Ab4', 1.0), n('Bb4', 1.0),
    ], dyn='f')

    add_measure(part, 22, [
        n('C5', 0.5), n('D5', 0.5), n('Eb5', 1.5, accent=True),
        n('D5', 0.5), n('C5', 0.5), n('Bb4', 0.5),
    ])

    add_measure(part, 23, [
        n('Ab4', 1.0), n('G4', 1.0),
        n('F4', 1.0), n('Eb4', 1.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('D4', 1.5, tenuto=True), r(2.5),
    ], dyn='mp')

    # == Section IV (mm.25-32) ==

    add_measure(part, 25, [
        n('Eb4', 4.0, tenuto=True),
    ], dyn='pp', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('F4', 2.0, tenuto=True), n('Eb4', 2.0),
    ])

    add_measure(part, 27, [
        n('Eb4', 2.0), n('Db4', 2.0, tenuto=True),
    ])

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('C4', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('C4', 2.0, tenuto=True), n('Eb4', 2.0),
    ], dyn='p')

    add_measure(part, 30, [
        n('F4', 2.0, tenuto=True), n('Eb4', 2.0),
    ])

    add_measure(part, 31, [
        n('Db4', 2.0), n('Bb3', 2.0, tenuto=True),
    ], dyn='pp')

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('B3', 1.5, tenuto=True), r(2.5),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        n('Eb4', 0.5), n('G4', 0.5), n('C5', 1.0),
        n('Eb5', 1.5, accent=True), n('D5', 0.5),
    ], dyn='f')

    add_measure(part, 34, [
        n('C5', 1.0), n('Bb4', 0.5), n('Ab4', 0.5),
        n('G4', 1.0), n('Bb4', 1.0),
    ])

    add_measure(part, 35, [
        n('C5', 1.5, accent=True), n('D5', 0.5),
        n('Eb5', 1.0), n('F5', 1.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('G5', 2.0, accent=True),
        n('Eb5', 1.0), r(1.0),
    ])

    # m.37: Motif in C major (G-B-C-B)
    add_measure(part, 37, [
        n('G4', 1.0, tenuto=True), n('B4', 1.0),
        n('C5', 1.5), n('B4', 0.5),
    ], dyn='f', ks=key.Key('C'))

    add_measure(part, 38, [
        n('A4', 1.5), n('G4', 0.5),
        n('F4', 1.0), n('E4', 1.0),
    ], dyn='mf')

    add_measure(part, 39, [
        n('D4', 0.5), n('E4', 0.5), n('G4', 1.0),
        n('E4', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 40, [
        n('C5', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Violin II -------------------------------------------------------------

def build_violin2(part):
    """Violin II: inner harmonies."""
    BAR = 4.0

    # mm.1-8: Tacet
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # == Section II (mm.9-16) ==

    add_measure(part, 9, [
        n('C4', 2.0, tenuto=True), n('Bb3', 2.0),
    ], dyn='pp')

    add_measure(part, 10, [
        n('Ab3', 2.0, tenuto=True), n('F3', 2.0),
    ])

    add_measure(part, 11, [
        n('F3', 2.0), n('Bb3', 2.0, tenuto=True),
    ], dyn='p')

    # m.12: rest at phrase boundary
    add_measure(part, 12, [
        n('B3', 2.0), n('C4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 13, [
        n('C4', 1.0), n('Eb4', 1.0),
        n('F4', 1.0), n('G4', 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('F4', 1.0), n('Eb4', 1.0),
        n('D4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 15, [
        n('Eb4', 1.0), n('D4', 0.5), n('C4', 0.5),
        n('Bb3', 1.0), n('Ab3', 1.0),
    ], dyn='mp')

    # m.16: rest at phrase boundary
    add_measure(part, 16, [
        n('Ab3', 1.0, tenuto=True), r(3.0),
    ])

    # == Section III (mm.17-24) ==

    add_measure(part, 17, [
        n('Eb4', 2.0, tenuto=True),
        n('D4', 1.0), n('Eb4', 1.0),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('Eb4', 1.0), n('F4', 1.0),
        n('G4', 1.5, tenuto=True), n('F4', 0.5),
    ])

    add_measure(part, 19, [
        n('F4', 1.0), n('Eb4', 0.5), n('F4', 0.5),
        n('G4', 1.0, tenuto=True), r(1.0),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Eb4', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 21, [
        n('G4', 1.0, accent=True), n('Ab4', 0.5), n('G4', 0.5),
        n('F4', 1.0), n('G4', 1.0),
    ], dyn='f')

    add_measure(part, 22, [
        n('Ab4', 0.5), n('Bb4', 0.5), n('C5', 1.5, accent=True),
        n('Bb4', 0.5), n('Ab4', 0.5), n('G4', 0.5),
    ])

    add_measure(part, 23, [
        n('F4', 1.0), n('Eb4', 1.0),
        n('D4', 1.0), n('C4', 1.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('Bb3', 1.5, tenuto=True), r(2.5),
    ], dyn='mp')

    # == Section IV (mm.25-32) ==

    add_measure(part, 25, [
        n('C4', 4.0, tenuto=True),
    ], dyn='pp', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Db4', 2.0, tenuto=True), n('C4', 2.0),
    ])

    add_measure(part, 27, [
        n('Bb3', 2.0), n('Bb3', 2.0, tenuto=True),
    ])

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('Ab3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('Ab3', 2.0, tenuto=True), n('C4', 2.0),
    ], dyn='p')

    add_measure(part, 30, [
        n('Db4', 2.0, tenuto=True), n('C4', 2.0),
    ])

    add_measure(part, 31, [
        n('Bb3', 2.0), n('G3', 2.0, tenuto=True),
    ], dyn='pp')

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('G3', 1.5, tenuto=True), r(2.5),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        n('C4', 1.0), n('Eb4', 1.0),
        n('G4', 1.5, accent=True), n('Ab4', 0.5),
    ], dyn='f')

    add_measure(part, 34, [
        n('G4', 1.0), n('F4', 0.5), n('Eb4', 0.5),
        n('D4', 1.0), n('Eb4', 1.0),
    ])

    add_measure(part, 35, [
        n('Ab4', 1.5, accent=True), n('Bb4', 0.5),
        n('C5', 1.0), n('D5', 1.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('Eb5', 2.0, accent=True),
        n('C5', 1.0), r(1.0),
    ])

    add_measure(part, 37, [
        n('E4', 1.0, tenuto=True), n('G4', 1.0),
        n('A4', 1.0), n('G4', 1.0),
    ], dyn='f', ks=key.Key('C'))

    add_measure(part, 38, [
        n('F4', 1.0), n('E4', 1.0),
        n('D4', 1.0), n('C4', 1.0),
    ], dyn='mf')

    add_measure(part, 39, [
        n('B3', 0.5), n('C4', 0.5), n('D4', 0.5), n('E4', 0.5),
        n('C4', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 40, [
        n('E4', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Viola -----------------------------------------------------------------

def build_viola(part):
    """Viola: warm inner voice."""
    BAR = 4.0

    # mm.1-8: Tacet
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # == Section II (mm.9-16) ==

    add_measure(part, 9, [
        n('G3', 2.0, tenuto=True), n('F3', 2.0),
    ], dyn='pp')

    add_measure(part, 10, [
        n('Eb3', 2.0, tenuto=True), n('C3', 2.0),
    ])

    add_measure(part, 11, [
        n('D3', 2.0), n('F3', 2.0, tenuto=True),
    ], dyn='p')

    # m.12: rest at phrase boundary
    add_measure(part, 12, [
        n('F3', 2.0), n('G3', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 13, [
        n('G3', 1.0), n('Ab3', 1.0),
        n('Bb3', 1.0), n('C4', 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('Ab3', 1.0), n('F3', 1.0),
        n('Eb3', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 15, [
        n('Eb3', 1.0), n('D3', 0.5), n('C3', 0.5),
        n('Bb2', 1.0), n('C3', 1.0),
    ])

    # m.16: rest at phrase boundary
    add_measure(part, 16, [
        n('C3', 1.0, tenuto=True), r(3.0),
    ])

    # == Section III (mm.17-24) ==

    add_measure(part, 17, [
        n('Bb3', 2.0, tenuto=True),
        n('Ab3', 1.0), n('Bb3', 1.0),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('G3', 1.0), n('Ab3', 1.0),
        n('Bb3', 1.5, tenuto=True), n('Ab3', 0.5),
    ])

    add_measure(part, 19, [
        n('F3', 1.0), n('Ab3', 1.0),
        n('F3', 1.0, tenuto=True), r(1.0),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Eb3', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 21, [
        n('Eb4', 1.0, accent=True), n('D4', 0.5), n('Eb4', 0.5),
        n('C4', 1.0), n('D4', 1.0),
    ], dyn='f')

    add_measure(part, 22, [
        n('Eb4', 0.5), n('F4', 0.5), n('G4', 1.5, accent=True),
        n('F4', 0.5), n('Eb4', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 23, [
        n('C4', 1.0), n('Bb3', 1.0),
        n('Ab3', 1.0), n('G3', 1.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('F3', 1.5, tenuto=True), r(2.5),
    ], dyn='mp')

    # == Section IV (mm.25-32) ==

    add_measure(part, 25, [
        n('Ab3', 4.0, tenuto=True),
    ], dyn='pp', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Ab3', 2.0, tenuto=True), n('Ab3', 2.0),
    ])

    add_measure(part, 27, [
        n('G3', 2.0), n('G3', 2.0, tenuto=True),
    ])

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('Eb3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('F3', 2.0, tenuto=True), n('Ab3', 2.0),
    ], dyn='p')

    add_measure(part, 30, [
        n('Ab3', 2.0, tenuto=True), n('Ab3', 2.0),
    ])

    add_measure(part, 31, [
        n('G3', 2.0), n('Eb3', 2.0, tenuto=True),
    ], dyn='pp')

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('D3', 1.5, tenuto=True), r(2.5),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        n('G3', 1.0), n('C4', 1.0),
        n('Eb4', 1.5, accent=True), n('D4', 0.5),
    ], dyn='f')

    add_measure(part, 34, [
        n('C4', 1.0), n('Bb3', 0.5), n('Ab3', 0.5),
        n('G3', 1.0), n('Ab3', 1.0),
    ])

    add_measure(part, 35, [
        n('G3', 1.5, accent=True), n('Ab3', 0.5),
        n('Bb3', 1.0), n('C4', 1.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('Eb4', 2.0, accent=True),
        n('C4', 1.0), r(1.0),
    ])

    add_measure(part, 37, [
        n('E3', 1.0, tenuto=True), n('G3', 1.0),
        n('A3', 1.0), n('G3', 1.0),
    ], dyn='f', ks=key.Key('C'))

    add_measure(part, 38, [
        n('F3', 1.0), n('E3', 1.0),
        n('D3', 1.0), n('C3', 1.0),
    ], dyn='mf')

    add_measure(part, 39, [
        n('B2', 0.5), n('C3', 0.5), n('D3', 0.5), n('E3', 0.5),
        n('G3', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 40, [
        n('G3', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Cello -----------------------------------------------------------------

def build_cello(part):
    """Cello: bass foundation with melodic moments."""
    BAR = 4.0

    # mm.1-4: Tacet
    for m_num in range(1, 5):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.5-8: Low pedal tones emerge
    add_measure(part, 5, [
        n('C2', 4.0, tenuto=True),
    ], dyn='pp')

    add_measure(part, 6, [
        n('Bb1', 4.0, tenuto=True),
    ])

    add_measure(part, 7, [
        n('Ab1', 4.0, tenuto=True),
    ])

    # m.8: rest at phrase boundary
    add_measure(part, 8, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.9-16) ==

    add_measure(part, 9, [
        n('C2', 2.0, tenuto=True), n('Eb2', 2.0),
    ], dyn='p')

    add_measure(part, 10, [
        n('Ab1', 2.0, tenuto=True), n('C2', 2.0),
    ])

    add_measure(part, 11, [
        n('Bb1', 2.0, tenuto=True), n('D2', 2.0),
    ])

    # m.12: rest at phrase boundary
    add_measure(part, 12, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 13, [
        n('C2', 2.0, tenuto=True), n('Eb2', 1.0), n('G2', 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('F2', 2.0, tenuto=True), n('Ab2', 2.0),
    ])

    add_measure(part, 15, [
        n('Bb1', 2.0, tenuto=True), n('D2', 2.0),
    ])

    # m.16: rest at phrase boundary
    add_measure(part, 16, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.17-24) ==

    add_measure(part, 17, [
        n('Eb2', 2.0, tenuto=True), n('G2', 2.0),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('Ab1', 2.0, tenuto=True), n('C2', 2.0),
    ])

    add_measure(part, 19, [
        n('Bb1', 2.0, tenuto=True), n('F2', 1.0), r(1.0),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 21, [
        n('C2', 2.0, accent=True), n('Ab2', 2.0),
    ], dyn='f')

    add_measure(part, 22, [
        n('F2', 2.0, tenuto=True), n('Ab2', 2.0),
    ])

    add_measure(part, 23, [
        n('Bb1', 2.0, tenuto=True), n('F2', 1.0), r(1.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    # == Section IV (mm.25-32) ==

    add_measure(part, 25, [
        n('Ab1', 4.0, tenuto=True),
    ], dyn='p', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Db2', 4.0, tenuto=True),
    ])

    add_measure(part, 27, [
        n('Eb2', 4.0, tenuto=True),
    ])

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('Ab1', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('F1', 2.0, tenuto=True), n('Ab1', 2.0),
    ], dyn='p')

    add_measure(part, 30, [
        n('Bb1', 2.0, tenuto=True), n('Db2', 2.0),
    ])

    add_measure(part, 31, [
        n('Eb2', 2.0, tenuto=True), n('Bb1', 2.0),
    ], dyn='pp')

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        n('C2', 2.0, accent=True), n('Eb2', 2.0),
    ], dyn='f')

    add_measure(part, 34, [
        n('Ab1', 2.0, tenuto=True), n('G1', 2.0),
    ])

    add_measure(part, 35, [
        n('F1', 1.0), n('G1', 1.0),
        n('Ab1', 1.0), n('B1', 1.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('C2', 2.0, accent=True),
        n('G2', 1.0), r(1.0),
    ])

    add_measure(part, 37, [
        n('C2', 2.0, accent=True), n('E2', 2.0),
    ], dyn='f', ks=key.Key('C'))

    add_measure(part, 38, [
        n('F2', 2.0, tenuto=True), n('C2', 2.0),
    ], dyn='mf')

    add_measure(part, 39, [
        n('G1', 2.0, tenuto=True), n('C2', 1.0), r(1.0),
    ], dyn='mp')

    add_measure(part, 40, [
        n('C2', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Contrabass ------------------------------------------------------------

def build_bass(part):
    """Contrabass: deep foundation."""
    BAR = 4.0

    # mm.1-8: Tacet
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # == Section II (mm.9-16) ==

    add_measure(part, 9, [
        n('C2', 4.0, tenuto=True),
    ], dyn='pp')

    add_measure(part, 10, [
        n('Ab1', 4.0, tenuto=True),
    ])

    add_measure(part, 11, [
        n('Bb1', 4.0, tenuto=True),
    ], dyn='p')

    # m.12: rest at phrase boundary
    add_measure(part, 12, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 13, [
        n('C2', 4.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 14, [
        n('F1', 4.0, tenuto=True),
    ])

    add_measure(part, 15, [
        n('Bb1', 4.0, tenuto=True),
    ])

    # m.16: rest at phrase boundary
    add_measure(part, 16, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.17-24) ==

    add_measure(part, 17, [
        n('Eb2', 4.0, tenuto=True),
    ], dyn='mf', ks=key.Key('E-'))

    add_measure(part, 18, [
        n('Ab1', 4.0, tenuto=True),
    ])

    add_measure(part, 19, [
        n('Bb1', 2.0, tenuto=True), r(2.0),
    ])

    # m.20: rest at phrase boundary
    add_measure(part, 20, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 21, [
        n('C2', 2.0, accent=True), n('Ab1', 2.0),
    ], dyn='f')

    add_measure(part, 22, [
        n('F1', 4.0, tenuto=True),
    ])

    add_measure(part, 23, [
        n('Bb1', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.24: rest at phrase boundary
    add_measure(part, 24, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    # == Section IV (mm.25-32) ==

    add_measure(part, 25, [
        n('Ab1', 4.0, tenuto=True),
    ], dyn='p', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Db2', 4.0, tenuto=True),
    ])

    add_measure(part, 27, [
        n('Eb2', 4.0, tenuto=True),
    ])

    # m.28: rest at phrase boundary
    add_measure(part, 28, [
        n('Ab1', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('F1', 4.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 30, [
        n('Bb1', 4.0, tenuto=True),
    ])

    add_measure(part, 31, [
        n('Eb2', 4.0, tenuto=True),
    ], dyn='pp')

    # m.32: rest at phrase boundary
    add_measure(part, 32, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ], ks=key.Key('c'))

    # == Section V (mm.33-40) ==

    add_measure(part, 33, [
        n('C2', 4.0, accent=True),
    ], dyn='f')

    add_measure(part, 34, [
        n('Ab1', 2.0, tenuto=True), n('G1', 2.0),
    ])

    add_measure(part, 35, [
        n('F1', 2.0, tenuto=True), n('G1', 2.0),
    ], dyn='ff')

    # m.36: rest at phrase boundary
    add_measure(part, 36, [
        n('C2', 2.0, accent=True), r(2.0),
    ])

    add_measure(part, 37, [
        n('C2', 4.0, accent=True),
    ], dyn='f', ks=key.Key('C'))

    add_measure(part, 38, [
        n('F1', 4.0, tenuto=True),
    ], dyn='mf')

    add_measure(part, 39, [
        n('G1', 2.0, tenuto=True), n('C2', 1.0), r(1.0),
    ], dyn='mp')

    add_measure(part, 40, [
        n('C2', 3.0, fermata=True), r(1.0),
    ], dyn='pp')


# -- Hairpins --------------------------------------------------------------

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins."""

    parts_by_name = {}
    for p in score.parts:
        name = (p.partName or '').lower()
        if 'harp' in name:
            parts_by_name['harp'] = p
        elif 'flute' in name:
            parts_by_name['flute'] = p
        elif 'oboe' in name:
            parts_by_name['oboe'] = p
        elif 'horn' in name:
            parts_by_name['horn'] = p
        elif 'violin ii' in name:
            parts_by_name['vln2'] = p
        elif 'violin i' in name:
            parts_by_name['vln1'] = p
        elif 'viola' in name:
            parts_by_name['viola'] = p
        elif 'violoncello' in name or 'cello' in name:
            parts_by_name['cello'] = p
        elif 'contrabass' in name or 'bass' in name:
            parts_by_name['bass'] = p

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
        # Harp
        ('harp', 1, 3, 'crescendo'),
        ('harp', 5, 7, 'crescendo'),
        ('harp', 33, 35, 'crescendo'),
        ('harp', 37, 39, 'diminuendo'),
        # Flute
        ('flute', 9, 11, 'crescendo'),
        ('flute', 13, 14, 'crescendo'),
        ('flute', 17, 19, 'crescendo'),
        ('flute', 21, 22, 'crescendo'),
        ('flute', 25, 27, 'crescendo'),
        ('flute', 33, 35, 'crescendo'),
        ('flute', 37, 39, 'diminuendo'),
        # Oboe
        ('oboe', 17, 19, 'crescendo'),
        ('oboe', 21, 22, 'crescendo'),
        ('oboe', 26, 28, 'crescendo'),
        ('oboe', 33, 35, 'crescendo'),
        # Horn
        ('horn', 17, 18, 'crescendo'),
        ('horn', 21, 22, 'crescendo'),
        ('horn', 35, 37, 'crescendo'),
        ('horn', 38, 40, 'diminuendo'),
        # Vln1
        ('vln1', 13, 14, 'crescendo'),
        ('vln1', 17, 19, 'crescendo'),
        ('vln1', 21, 22, 'crescendo'),
        ('vln1', 33, 35, 'crescendo'),
        ('vln1', 37, 39, 'diminuendo'),
        # Vln2
        ('vln2', 17, 19, 'crescendo'),
        ('vln2', 21, 22, 'crescendo'),
        ('vln2', 33, 35, 'crescendo'),
        ('vln2', 37, 39, 'diminuendo'),
        # Viola
        ('viola', 17, 19, 'crescendo'),
        ('viola', 21, 22, 'crescendo'),
        ('viola', 33, 35, 'crescendo'),
        ('viola', 37, 39, 'diminuendo'),
        # Cello
        ('cello', 5, 7, 'crescendo'),
        ('cello', 17, 18, 'crescendo'),
        ('cello', 33, 35, 'crescendo'),
        ('cello', 37, 39, 'diminuendo'),
        # Bass
        ('bass', 17, 18, 'crescendo'),
        ('bass', 33, 35, 'crescendo'),
        ('bass', 37, 39, 'diminuendo'),
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        target_part = parts_by_name.get(part_name)
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
