#!/usr/bin/env python3
"""Generate 'Prelude to a New World' -- JRPG Main Menu Theme.

A main menu theme for a Final Fantasy game starring Claude.
Instrumentation: Flute, French Horn, Harp, Violin I, Viola, Cello.

Key: Bb major -> Eb major -> G minor -> Bb major
Time: 4/4, Andante maestoso (q=72) -> flowing middle -> triumphant return
~64 measures.

Sections:
  I.   Crystal Prelude (mm.1-16) -- Harp arpeggios establish the world.
       Horn calls out the hero's motif. Strings enter softly. Bb major.
       Brief tonicization to F major (m.3-4), Eb major (m.7-8).
  II.  The Journey Begins (mm.17-32) -- Flute takes the melody, fuller
       orchestration. Bb -> Db major (m.21) -> Eb major (m.25) -> Bb (m.29).
  III. Shadow of Doubt (mm.33-48) -- G minor -> Bb minor (m.37) ->
       C minor (m.41) -> D major (m.45). Darker, chromatic.
       Viola and cello lead. The conflict hinted at. Horn echoes distantly.
  IV.  Promise of Dawn (mm.49-64) -- Eb major -> Ab major (m.53) ->
       Bb major (m.57). Full ensemble, hero's motif triumphant.

Revision 1 changes (from profile feedback):
  - scale_consistency: added chromatic passing tones (C#, F#, G#, Ab) throughout
  - phrase_length_regularity: enforced strict 4-bar phrase groups with cadential rests
  - pitch_class_entropy: spread all 12 pitch classes more evenly across parts
  - rhythmic_variety: added dotted-quarter (1.5), dotted-eighth (0.75), triplet (1/3),
    sixteenth (0.25) values in addition to existing half/quarter/eighth
  - modulation_count: 10 explicit key changes via tonicizations

The hero's motif: Bb4 - D5 - F5 - Eb5 - D5 (rising arpeggio with stepback)
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

    # Flute
    flute_part = stream.Part()
    flute_part.insert(0, instrument.Flute())
    flute_part.partName = "Flute"
    flute_part.partAbbreviation = "Fl."

    # French Horn
    horn_part = stream.Part()
    horn_part.insert(0, instrument.Horn())
    horn_part.partName = "Horn in F"
    horn_part.partAbbreviation = "Hn."

    # Harp
    harp_part = stream.Part()
    harp_part.insert(0, instrument.Harp())
    harp_part.partName = "Harp"
    harp_part.partAbbreviation = "Hp."

    # Violin I
    vln_part = stream.Part()
    vln_part.insert(0, instrument.Violin())
    vln_part.partName = "Violin I"
    vln_part.partAbbreviation = "Vln. I"

    # Viola
    vla_part = stream.Part()
    vla_part.insert(0, instrument.Viola())
    vla_part.partName = "Viola"
    vla_part.partAbbreviation = "Vla."

    # Cello
    vc_part = stream.Part()
    vc_part.insert(0, instrument.Violoncello())
    vc_part.partName = "Violoncello"
    vc_part.partAbbreviation = "Vc."

    build_flute(flute_part)
    build_horn(horn_part)
    build_harp(harp_part)
    build_violin(vln_part)
    build_viola(vla_part)
    build_cello(vc_part)

    s.insert(0, flute_part)
    s.insert(0, horn_part)
    s.insert(0, harp_part)
    s.insert(0, vln_part)
    s.insert(0, vla_part)
    s.insert(0, vc_part)

    return s


# -- Flute Part ------------------------------------------------------------

def build_flute(part):
    """Flute: carries the melody in Section II, ornaments in III, soars in IV.

    Revision 1: more chromaticism (F#, C#, G#, Ab passing tones), triplet rhythms,
    stricter 4-bar phrases, more tonicizations.
    """
    BAR = 4.0
    TRIPLET = 1.0 / 3.0  # triplet eighth = 1/3 quarter

    # == Section I: Crystal Prelude (mm.1-16) -- Flute tacet, then enters ==
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('B-')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.9-12: Flute enters with a gentle countermelody (chromatic neighbor tones)
    add_measure(part, 9, [
        r(2.0), n('F5', 0.75), n('E5', 0.25), n('Eb5', 1.0),
    ], dyn='p', expression_text='dolce')

    add_measure(part, 10, [
        n('D5', 1.5), n('C#5', 0.5), n('Bb4', 1.0), r(1.0),
    ])

    add_measure(part, 11, [
        r(2.0), n('G5', 0.75), n('F#5', 0.25), n('F5', 1.0),
    ])

    # m.12: Phrase end rest (4-bar phrase: 9-12)
    add_measure(part, 12, [
        n('Eb5', 1.5), n('D5', 0.5), n('C5', 1.0), r(1.0),
    ])

    # m.13-16: Flute echoes the hero's motif fragment, with chromatic inflection
    add_measure(part, 13, [
        n('Bb4', 1.0), n('D5', 1.0), n('F5', 1.0, tenuto=True), n('E5', 1.0),
    ], dyn='mp')

    # m.14: Phrase breath
    add_measure(part, 14, [
        n('D5', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 15, [
        n('C#5', 0.75), n('D5', 0.25), n('Eb5', 0.5), n('E5', 0.5),
        n('F5', 1.0, tenuto=True), r(1.0),
    ])

    # m.16: Phrase end (4-bar phrase: 13-16)
    add_measure(part, 16, [
        n('Bb4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II: The Journey Begins (mm.17-32) -- Flute leads melody ==
    # Hero's motif in full: Bb4-D5-F5-Eb5-D5, then developed
    add_measure(part, 17, [
        n('Bb4', 1.0), n('D5', 1.0), n('F5', 1.5, accent=True), n('Eb5', 0.5),
    ], dyn='mf', expression_text='con anima',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=80))

    add_measure(part, 18, [
        n('D5', 2.0, tenuto=True), n('C#5', 0.5), n('C5', 0.5), n('Bb4', 1.0),
    ])

    add_measure(part, 19, [
        n('Eb5', 1.0), n('F5', 1.0), n('G5', 1.5, accent=True), n('F#5', 0.5),
    ])

    # m.20: Phrase end rest (4-bar: 17-20)
    add_measure(part, 20, [
        n('Eb5', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24: Tonicize Db major -- dreamy color shift
    add_measure(part, 21, [
        n('Db5', 1.0), n('F5', 1.0), n('Ab5', 1.5, accent=True), n('Gb5', 0.5),
    ], dyn='f', ks=key.Key('D-'))

    add_measure(part, 22, [
        n('F5', 1.5), n('Eb5', 0.5), n('Db5', 1.0, tenuto=True), n('C5', 1.0),
    ])

    add_measure(part, 23, [
        n('Bb4', 1.0), n('C5', 0.5), n('Db5', 0.5),
        n('Eb5', 1.0, accent=True), n('F5', 1.0),
    ])

    # m.24: Phrase end rest (4-bar: 21-24)
    add_measure(part, 24, [
        n('Gb5', 2.0, tenuto=True), n('F5', 1.0), r(1.0),
    ])

    # m.25-28: Modulate to Eb major, flourish with triplets
    add_measure(part, 25, [
        n('Bb5', TRIPLET, accent=True), n('Ab5', TRIPLET), n('G5', TRIPLET),
        n('F5', TRIPLET), n('Eb5', TRIPLET), n('D5', TRIPLET),
        n('Eb5', 1.0, tenuto=True), n('D5', 1.0),
    ], ks=key.Key('E-'))

    add_measure(part, 26, [
        n('C5', 1.0), n('Bb4', 1.0), n('Ab4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 27, [
        n('F5', 1.0), n('E5', 0.5), n('D5', 0.5),
        n('C5', 1.0, tenuto=True), n('Bb4', 1.0),
    ])

    # m.28: Phrase end (4-bar: 25-28)
    add_measure(part, 28, [
        n('Eb5', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Return to Bb, quiet transition with chromatic passing tones
    add_measure(part, 29, [
        n('G5', 2.0, trill=True), n('F#5', 0.5), n('F5', 0.5), n('E5', 1.0),
    ], dyn='mp', ks=key.Key('B-'))

    add_measure(part, 30, [
        n('D5', 2.0, tenuto=True), n('C#5', 0.5), n('C5', 0.5), r(1.0),
    ])

    add_measure(part, 31, [
        n('Bb4', 1.0), n('C5', 0.5), n('D5', 0.5), n('Eb5', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.32: Phrase end (4-bar: 29-32)
    add_measure(part, 32, [
        n('D5', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III: Shadow of Doubt (mm.33-48) ==
    # m.33-36: G minor, flute sparse and haunting

    add_measure(part, 33, [
        r(BAR),
    ], ks=key.Key('g'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=66,
                                       text="Misterioso"))

    add_measure(part, 34, [r(BAR)])

    add_measure(part, 35, [
        r(2.0), n('D5', 0.75, tenuto=True), n('Eb5', 0.25), n('E5', 1.0),
    ], dyn='p')

    # m.36: Phrase end (4-bar: 33-36)
    add_measure(part, 36, [
        n('F#5', 1.5, accent=True), n('G5', 0.5), n('F5', 1.0), r(1.0),
    ])

    # m.37-40: Bb minor tonicization -- darker coloring
    add_measure(part, 37, [
        r(BAR),
    ], ks=key.Key('b-'))

    add_measure(part, 38, [r(BAR)])

    add_measure(part, 39, [
        r(2.0), n('Bb5', 1.0, trill=True), n('A5', 1.0),
    ], dyn='pp')

    # m.40: Phrase end (4-bar: 37-40)
    add_measure(part, 40, [
        n('Ab5', 1.0), n('Gb5', 1.0, tenuto=True), r(2.0),
    ])

    # m.41-44: C minor tonicization, flute responds to viola
    add_measure(part, 41, [
        n('D5', 1.0), n('Eb5', 0.5), n('D5', 0.5),
        n('C5', 1.0, tenuto=True), n('B4', 1.0),
    ], dyn='p', ks=key.Key('c'))

    add_measure(part, 42, [
        n('Ab4', 1.5), n('Bb4', 0.5), n('C5', 1.0), r(1.0),
    ])

    add_measure(part, 43, [
        n('D5', 0.5), n('Eb5', 0.5), n('F#5', 1.0, accent=True),
        n('G5', 1.0, tenuto=True), r(1.0),
    ])

    # m.44: Phrase end (4-bar: 41-44)
    add_measure(part, 44, [
        n('F5', 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: D major tonicization, building toward return
    add_measure(part, 45, [
        n('A5', 1.0), n('G#5', 0.25), n('F#5', 0.75),
        n('D5', 1.0, accent=True), n('C#5', 1.0),
    ], dyn='mp', ks=key.Key('D'))

    add_measure(part, 46, [
        n('B4', 1.0), n('C#5', 0.5), n('D5', 0.5),
        n('E5', 1.0, tenuto=True), n('F#5', 1.0),
    ], dyn='mf')

    add_measure(part, 47, [
        n('G5', 1.0, accent=True), n('F#5', 0.5), n('E5', 0.5),
        n('D5', 1.0), n('C#5', 1.0),
    ])

    # m.48: Phrase end (4-bar: 45-48)
    add_measure(part, 48, [
        n('D5', 2.0, tenuto=True), r(2.0),
    ])

    # == Section IV: Promise of Dawn (mm.49-64) ==
    # m.49-52: Eb major, triumphant statement

    add_measure(part, 49, [
        n('Eb5', 1.0, accent=True), n('G5', 1.0), n('Bb5', 1.5, accent=True), n('Ab5', 0.5),
    ], dyn='f', expression_text='Triumphantly',
       ks=key.Key('E-'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=76,
                                       text="Maestoso"))

    add_measure(part, 50, [
        n('G5', 2.0, tenuto=True), n('Bb5', 1.0, accent=True), n('C6', 1.0),
    ])

    add_measure(part, 51, [
        n('D6', TRIPLET), n('C6', TRIPLET), n('Bb5', TRIPLET),
        n('Ab5', 1.0, accent=True), n('G5', 1.0), n('F5', 1.0),
    ])

    # m.52: Phrase end (4-bar: 49-52)
    add_measure(part, 52, [
        n('Eb5', 2.0, tenuto=True), r(2.0),
    ])

    # m.53-56: Ab major tonicization -- warm, expansive
    add_measure(part, 53, [
        n('Ab5', 1.0), n('Bb5', 1.0), n('C6', 1.0, accent=True), n('Db6', 1.0),
    ], dyn='ff', ks=key.Key('A-'))

    add_measure(part, 54, [
        n('C6', 2.0, tenuto=True), n('Bb5', 0.5), n('Ab5', 0.5), n('G5', 1.0),
    ])

    add_measure(part, 55, [
        n('F5', 1.0), n('Eb5', 0.5), n('Db5', 0.5),
        n('C5', 1.0, accent=True), n('Db5', 1.0),
    ], dyn='f')

    # m.56: Phrase end (4-bar: 53-56)
    add_measure(part, 56, [
        n('Eb5', 2.0, tenuto=True), r(2.0),
    ])

    # m.57-60: Bb major return, gentle wind-down
    add_measure(part, 57, [
        n('F5', 1.0, tenuto=True), n('Eb5', 1.0), n('D5', 1.0), n('C#5', 1.0),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 58, [
        n('Bb4', 2.0, tenuto=True), n('D5', 1.0), r(1.0),
    ], dyn='mp')

    add_measure(part, 59, [
        n('Eb5', 0.75), n('D5', 0.25), n('C#5', 0.5), n('C5', 0.5),
        n('Bb4', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.60: Phrase end (4-bar: 57-60)
    add_measure(part, 60, [
        n('F5', 2.0, tenuto=True), r(2.0),
    ])

    # m.61-64: Final echo of the motif, fading
    add_measure(part, 61, [
        n('Bb4', 1.0), n('D5', 1.0), n('F5', 1.5, tenuto=True), n('E5', 0.5),
    ], dyn='p', expression_text='morendo')

    add_measure(part, 62, [
        n('D5', 2.0, tenuto=True), r(2.0),
    ], dyn='pp')

    add_measure(part, 63, [
        n('Bb5', 4.0, tenuto=True),
    ], dyn='ppp')

    # m.64: Final (4-bar: 61-64)
    add_measure(part, 64, [
        n('Bb5', 4.0, fermata=True),
    ])


# -- French Horn Part ------------------------------------------------------

def build_horn(part):
    """Horn: announces the hero's motif, provides harmonic backbone.

    Revision 1: more chromaticism, matching key changes with other parts.
    """
    BAR = 4.0

    # == Section I (mm.1-16) ==
    for m_num in range(1, 5):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('B-')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.5-8: Horn announces the hero's motif with chromatic grace
    add_measure(part, 5, [
        n('Bb3', 1.0, accent=True), n('D4', 1.0), n('F4', 1.5, tenuto=True), n('E4', 0.5),
    ], dyn='mf', expression_text='nobile')

    add_measure(part, 6, [
        n('D4', 3.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 7, [
        n('Eb4', 1.0), n('D4', 0.5), n('C#4', 0.5),
        n('Bb3', 1.5, tenuto=True), r(0.5),
    ])

    # m.8: Phrase end (4-bar: 5-8)
    add_measure(part, 8, [
        n('F3', 2.0, tenuto=True), r(2.0),
    ])

    # m.9-12: Horn sustains with chromatic inflections
    add_measure(part, 9, [
        n('Bb3', 4.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 10, [
        n('A3', 1.5, tenuto=True), n('Ab3', 0.5), n('Bb3', 2.0),
    ])

    add_measure(part, 11, [
        n('C4', 3.0, tenuto=True), n('B3', 1.0),
    ])

    # m.12: Phrase end (4-bar: 9-12)
    add_measure(part, 12, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ])

    # m.13-16: Gentle echo of the motif
    add_measure(part, 13, [
        n('F3', 1.0), n('Bb3', 1.0), n('D4', 1.0, tenuto=True), n('C#4', 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 15, [
        n('Eb4', 1.5, tenuto=True), n('D4', 0.5), n('C4', 1.0), r(1.0),
    ])

    # m.16: Phrase end (4-bar: 13-16)
    add_measure(part, 16, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.17-32) ==
    add_measure(part, 17, [
        n('F3', 2.0, tenuto=True), n('Bb3', 2.0, tenuto=True),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=80))

    add_measure(part, 18, [
        n('A3', 2.0, tenuto=True), n('G#3', 1.0), n('G3', 1.0),
    ])

    add_measure(part, 19, [
        n('Eb4', 2.0, tenuto=True), n('D4', 2.0),
    ])

    # m.20: Phrase end (4-bar: 17-20)
    add_measure(part, 20, [
        n('C4', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24: Db major tonicization
    add_measure(part, 21, [
        n('Db3', 2.0, tenuto=True), n('F3', 2.0, tenuto=True),
    ], dyn='f', ks=key.Key('D-'))

    add_measure(part, 22, [
        n('Ab3', 2.0, tenuto=True), n('Gb3', 2.0),
    ])

    add_measure(part, 23, [
        n('Gb3', 2.0, tenuto=True), n('F3', 2.0),
    ])

    # m.24: Phrase end (4-bar: 21-24)
    add_measure(part, 24, [
        n('Eb3', 2.0, tenuto=True), r(2.0),
    ])

    # m.25-28: Eb major
    add_measure(part, 25, [
        n('Eb4', 2.0, accent=True), n('D4', 1.0), n('C4', 1.0),
    ], ks=key.Key('E-'))

    add_measure(part, 26, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    add_measure(part, 27, [
        n('Ab3', 2.0, tenuto=True), n('G3', 2.0),
    ])

    # m.28: Phrase end (4-bar: 25-28)
    add_measure(part, 28, [
        n('Eb3', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    # m.29-32: Transition back to Bb
    add_measure(part, 29, [
        n('Bb3', 4.0, tenuto=True),
    ], dyn='p', ks=key.Key('B-'))

    add_measure(part, 30, [
        n('A3', 2.0, tenuto=True), n('G#3', 1.0), n('G3', 1.0),
    ])

    add_measure(part, 31, [
        n('F#3', 4.0, tenuto=True),
    ])

    # m.32: Phrase end (4-bar: 29-32)
    add_measure(part, 32, [
        n('G3', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.33-48) ==
    add_measure(part, 33, [
        r(BAR),
    ], ks=key.Key('g'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=66,
                                       text="Misterioso"))

    add_measure(part, 34, [r(BAR)])

    add_measure(part, 35, [
        n('G3', 4.0, tenuto=True),
    ], dyn='pp', expression_text='lontano')

    # m.36: Phrase end (4-bar: 33-36)
    add_measure(part, 36, [
        n('F#3', 2.0, tenuto=True), r(2.0),
    ])

    # m.37-40: Bb minor
    add_measure(part, 37, [
        n('Db3', 2.0, tenuto=True), n('Eb3', 2.0),
    ], dyn='p', ks=key.Key('b-'))

    add_measure(part, 38, [
        n('F3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 39, [
        n('Gb3', 4.0, tenuto=True),
    ], dyn='pp')

    # m.40: Phrase end (4-bar: 37-40)
    add_measure(part, 40, [
        n('Db3', 2.0, tenuto=True), r(2.0),
    ])

    # m.41-44: C minor, horn begins to return
    add_measure(part, 41, [
        n('Eb3', 2.0, tenuto=True), n('D3', 2.0),
    ], dyn='p', ks=key.Key('c'))

    add_measure(part, 42, [
        n('C3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 43, [
        n('D4', 1.0, accent=True), n('C4', 1.0),
        n('B3', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    # m.44: Phrase end (4-bar: 41-44)
    add_measure(part, 44, [
        n('G3', 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: D major, building to return
    add_measure(part, 45, [
        n('D4', 1.0), n('C#4', 1.0), n('D4', 1.0, accent=True), n('E4', 1.0),
    ], dyn='mf', ks=key.Key('D'))

    add_measure(part, 46, [
        n('F#4', 2.0, tenuto=True), n('E4', 1.0), n('D4', 1.0),
    ])

    add_measure(part, 47, [
        n('C#4', 1.0), n('D4', 1.0), n('E4', 1.0, accent=True), n('F#4', 1.0),
    ], dyn='f')

    # m.48: Phrase end (4-bar: 45-48)
    add_measure(part, 48, [
        n('F#4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section IV (mm.49-64) ==
    # m.49-52: Eb major, triumphant
    add_measure(part, 49, [
        n('Eb4', 1.0, accent=True), n('G4', 1.0),
        n('Bb4', 1.5, accent=True), n('Ab4', 0.5),
    ], dyn='ff', expression_text='glorioso',
       ks=key.Key('E-'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=76,
                                       text="Maestoso"))

    add_measure(part, 50, [
        n('G4', 3.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 51, [
        n('Ab4', 1.0), n('Bb4', 1.0, accent=True),
        n('G4', 1.0, tenuto=True), n('F4', 1.0),
    ])

    # m.52: Phrase end (4-bar: 49-52)
    add_measure(part, 52, [
        n('Eb4', 2.0, tenuto=True), r(2.0),
    ])

    # m.53-56: Ab major
    add_measure(part, 53, [
        n('Ab3', 1.0), n('C4', 1.0), n('Eb4', 1.0, accent=True), n('Ab4', 1.0),
    ], dyn='ff', ks=key.Key('A-'))

    add_measure(part, 54, [
        n('Gb4', 2.0, tenuto=True), n('F4', 1.0), n('Eb4', 1.0),
    ])

    add_measure(part, 55, [
        n('Db4', 1.0, accent=True), n('Eb4', 1.0),
        n('F4', 1.0, tenuto=True), n('Gb4', 1.0),
    ], dyn='f')

    # m.56: Phrase end (4-bar: 53-56)
    add_measure(part, 56, [
        n('Ab4', 2.0, tenuto=True), r(2.0),
    ])

    # m.57-60: Bb major, winding down
    add_measure(part, 57, [
        n('D4', 2.0, tenuto=True), n('C4', 2.0),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 58, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 59, [
        n('Eb4', 1.0, tenuto=True), n('D4', 1.0), n('C#4', 1.0), r(1.0),
    ], dyn='p')

    # m.60: Phrase end (4-bar: 57-60)
    add_measure(part, 60, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ])

    # m.61-64: Final horn call
    add_measure(part, 61, [
        n('Bb3', 1.0), n('D4', 1.0), n('F4', 1.5, tenuto=True), n('E4', 0.5),
    ], dyn='p', expression_text='lontano')

    add_measure(part, 62, [
        n('D4', 3.0, tenuto=True), r(1.0),
    ], dyn='pp')

    add_measure(part, 63, [
        n('Bb3', 4.0, tenuto=True),
    ], dyn='ppp')

    # m.64: Final (4-bar: 61-64)
    add_measure(part, 64, [
        n('F3', 4.0, fermata=True),
    ])


# -- Harp Part -------------------------------------------------------------

def build_harp(part):
    """Harp: crystalline arpeggios, the sound of the menu screen.

    Revision 1: chromatic passing tones in arpeggios, matching key changes,
    triplet figures for rhythmic variety.
    """
    BAR = 4.0
    TRIPLET = 1.0 / 3.0

    # == Section I (mm.1-16) -- Harp opens the world ==

    add_measure(part, 1, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('F4', 0.5),
    ], ts=meter.TimeSignature('4/4'), ks=key.Key('B-'),
       tempo_mark=tempo.MetronomeMark(
           referent=duration.Duration(1.0), number=72,
           text="Andante maestoso"
       ),
       dyn='p', expression_text='luminoso')

    add_measure(part, 2, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5), n('Bb3', 0.5),
    ])

    # m.3-4: Brief F major tonicization -- chromatic color
    add_measure(part, 3, [
        n('F2', 0.5), n('A2', 0.5), n('C3', 0.5), n('E3', 0.5),
        n('A3', 0.5), n('C4', 0.5), n('F4', 0.5), n('C4', 0.5),
    ], ks=key.Key('F'))

    # m.4: Phrase end (4-bar: 1-4)
    add_measure(part, 4, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('Bb3', 1.0, tenuto=True), r(1.0),
    ], ks=key.Key('B-'))

    # m.5-8: Under horn entry, with chromatic neighbor tones
    add_measure(part, 5, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('D4', 0.5),
    ], dyn='mp')

    add_measure(part, 6, [
        n('G2', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('Bb3', 0.5), n('D4', 0.5), n('G4', 0.5), n('D4', 0.5),
    ])

    # m.7: Eb major coloring
    add_measure(part, 7, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5), n('Bb3', 0.5),
    ], ks=key.Key('E-'))

    # m.8: Phrase end (4-bar: 5-8)
    add_measure(part, 8, [
        n('F2', 0.5), n('A2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
        n('F3', 1.0, tenuto=True), r(1.0),
    ], ks=key.Key('B-'))

    # m.9-12: Richer arpeggios with chromatic 7th tones
    add_measure(part, 9, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('Bb3', 0.5), n('D4', 0.5), n('F4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 10, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('D3', 0.5),
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 11, [
        n('C2', 0.5), n('E2', 0.5), n('G2', 0.5), n('Bb2', 0.5),
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    # m.12: Phrase end (4-bar: 9-12)
    add_measure(part, 12, [
        n('F2', 0.5), n('A2', 0.5), n('C#3', 0.5), n('Eb3', 0.5),
        n('F3', 1.0, tenuto=True), r(1.0),
    ])

    # m.13-16: Chordal, sustained with chromatic bass
    add_measure(part, 13, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 2.0), ch(['Eb3', 'G3', 'Bb3'], 2.0),
    ], dyn='mp')

    add_measure(part, 14, [
        ch(['F2', 'A2', 'C#3', 'F3'], 2.0), r(2.0),
    ])

    add_measure(part, 15, [
        ch(['Eb2', 'G2', 'Bb2', 'D3'], 2.0), ch(['F2', 'A2', 'C3', 'Eb3'], 2.0),
    ])

    # m.16: Phrase end (4-bar: 13-16)
    add_measure(part, 16, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.17-32) ==

    add_measure(part, 17, [
        n('Bb2', 0.5), n('F3', 0.5), n('Bb3', 0.5), n('D4', 0.5),
        n('F3', 0.5), n('Bb3', 0.5), n('D4', 0.5), n('F4', 0.5),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=80))

    add_measure(part, 18, [
        n('F2', 0.5), n('C3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('C3', 0.5), n('F3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 19, [
        n('Eb2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    # m.20: Phrase end (4-bar: 17-20)
    add_measure(part, 20, [
        n('F2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('A3', 0.5),
        n('C3', 1.0, tenuto=True), r(1.0),
    ])

    # m.21-24: Db major arpeggios -- dreamy tonicization
    add_measure(part, 21, [
        n('Db2', 0.5), n('Ab2', 0.5), n('Db3', 0.5), n('F3', 0.5),
        n('Ab3', 0.5), n('Db4', 0.5), n('F4', 0.5), n('Db4', 0.5),
    ], ks=key.Key('D-'))

    add_measure(part, 22, [
        n('Gb2', 0.5), n('Bb2', 0.5), n('Db3', 0.5), n('Gb3', 0.5),
        n('Bb3', 0.5), n('Db4', 0.5), n('Gb4', 0.5), n('Db4', 0.5),
    ])

    add_measure(part, 23, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
    ])

    # m.24: Phrase end (4-bar: 21-24)
    add_measure(part, 24, [
        n('Db2', 0.5), n('F2', 0.5), n('Ab2', 0.5), n('Db3', 0.5),
        n('F3', 1.0, tenuto=True), r(1.0),
    ])

    # m.25-28: Eb major flowing eighths with chromatic neighbors
    add_measure(part, 25, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5), n('G3', 0.5),
    ], ks=key.Key('E-'))

    add_measure(part, 26, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C3', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 27, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('F3', 0.5),
        n('Ab3', 0.5), n('B3', 0.5), n('C4', 0.5), n('F4', 0.5),
    ])

    # m.28: Phrase end (4-bar: 25-28)
    add_measure(part, 28, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 1.0, tenuto=True), r(1.0),
    ])

    # m.29-32: Transition back to Bb, chromatic chords
    add_measure(part, 29, [
        ch(['Eb3', 'G3', 'Bb3', 'D4'], 2.0), ch(['D3', 'F#3', 'A3', 'C4'], 2.0),
    ], dyn='mp', ks=key.Key('B-'))

    add_measure(part, 30, [
        ch(['G2', 'B2', 'D3', 'F3'], 2.0), r(2.0),
    ])

    add_measure(part, 31, [
        n('D2', 0.5), n('A2', 0.5), n('D3', 0.5), n('F#3', 0.5),
        n('A3', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.32: Phrase end (4-bar: 29-32)
    add_measure(part, 32, [
        ch(['G2', 'Bb2', 'D3'], 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.33-48) -- G minor ==
    # m.33-36: Sparse, dark arpeggios

    add_measure(part, 33, [
        n('G2', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('Bb3', 0.5), n('D4', 0.5), n('G4', 0.5), n('D4', 0.5),
    ], dyn='p', ks=key.Key('g'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=66,
                                       text="Misterioso"))

    add_measure(part, 34, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5), n('Bb3', 0.5),
    ])

    add_measure(part, 35, [
        n('C2', 0.5), n('Eb2', 0.5), n('G2', 0.5), n('C3', 0.5),
        n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5), n('G3', 0.5),
    ])

    # m.36: Phrase end (4-bar: 33-36)
    add_measure(part, 36, [
        n('D2', 0.5), n('F#2', 0.5), n('A2', 0.5), n('D3', 0.5),
        n('F#3', 1.0, tenuto=True), r(1.0),
    ])

    # m.37-40: Bb minor -- darker arpeggios with Gb, Db
    add_measure(part, 37, [
        n('Bb2', 0.5), n('Db3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('Db4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('F4', 0.5),
    ], dyn='mp', ks=key.Key('b-'))

    add_measure(part, 38, [
        n('Gb2', 0.5), n('Bb2', 0.5), n('Db3', 0.5), n('Gb3', 0.5),
        n('Bb3', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 39, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('Eb4', 0.5),
    ])

    # m.40: Phrase end (4-bar: 37-40)
    add_measure(part, 40, [
        n('Db2', 0.5), n('F2', 0.5), n('Ab2', 0.5), n('Db3', 0.5),
        n('F3', 1.0, tenuto=True), r(1.0),
    ])

    # m.41-44: C minor chords
    add_measure(part, 41, [
        ch(['C2', 'Eb2', 'G2', 'Bb2'], 2.0), ch(['Ab2', 'C3', 'Eb3', 'G3'], 2.0),
    ], dyn='p', ks=key.Key('c'))

    add_measure(part, 42, [
        ch(['F2', 'Ab2', 'C3', 'Eb3'], 2.0), r(2.0),
    ])

    add_measure(part, 43, [
        ch(['D2', 'F#2', 'A2', 'C3'], 2.0, accent=True),
        ch(['G2', 'B2', 'D3'], 2.0),
    ])

    # m.44: Phrase end (4-bar: 41-44)
    add_measure(part, 44, [
        ch(['G2', 'B2', 'D3', 'F3'], 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: D major, building -- bright arpeggios with F#, C#
    add_measure(part, 45, [
        n('D2', 0.5), n('F#2', 0.5), n('A2', 0.5), n('D3', 0.5),
        n('F#3', 0.5), n('A3', 0.5), n('D4', 0.5), n('A3', 0.5),
    ], dyn='mf', ks=key.Key('D'))

    add_measure(part, 46, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('B3', 0.5), n('D4', 0.5), n('G4', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 47, [
        n('A2', 0.5), n('C#3', 0.5), n('E3', 0.5), n('A3', 0.5),
        n('C#4', 0.5), n('E4', 0.5), n('A4', 0.5), n('E4', 0.5),
    ], dyn='f')

    # m.48: Phrase end (4-bar: 45-48)
    add_measure(part, 48, [
        n('D2', 0.5), n('A2', 0.5), n('D3', 0.5), n('F#3', 0.5),
        n('A3', 1.0, tenuto=True), r(1.0),
    ])

    # == Section IV (mm.49-64) ==
    # m.49-52: Eb major, glorious arpeggios

    add_measure(part, 49, [
        n('Eb2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('Bb3', 0.5), n('Eb4', 0.5), n('G4', 0.5), n('Bb4', 0.5),
    ], dyn='f',
       ks=key.Key('E-'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=76,
                                       text="Maestoso"))

    add_measure(part, 50, [
        n('Ab2', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
        n('Eb4', 0.5), n('Ab4', 0.5), n('C5', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 51, [
        n('Bb2', 0.5), n('F3', 0.5), n('Bb3', 0.5), n('D4', 0.5),
        n('F4', 0.5), n('Bb4', 0.5), n('D5', 0.5), n('Bb4', 0.5),
    ])

    # m.52: Phrase end (4-bar: 49-52)
    add_measure(part, 52, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 1.0, tenuto=True), r(1.0),
    ])

    # m.53-56: Ab major tonicization
    add_measure(part, 53, [
        n('Ab1', 0.5), n('Eb2', 0.5), n('Ab2', 0.5), n('C3', 0.5),
        n('Eb3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
    ], dyn='ff', ks=key.Key('A-'))

    add_measure(part, 54, [
        n('Db2', 0.5), n('Ab2', 0.5), n('Db3', 0.5), n('F3', 0.5),
        n('Ab3', 0.5), n('Db4', 0.5), n('F4', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 55, [
        n('Eb2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5),
        n('Bb3', 0.5), n('Eb4', 0.5), n('G4', 0.5), n('Bb4', 0.5),
    ], dyn='f')

    # m.56: Phrase end (4-bar: 53-56)
    add_measure(part, 56, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 1.0, tenuto=True), r(1.0),
    ])

    # m.57-60: Bb major return, winding down
    add_measure(part, 57, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('F4', 0.5),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 58, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 1.0, tenuto=True), r(1.0),
    ], dyn='mp')

    add_measure(part, 59, [
        n('F2', 0.5), n('A2', 0.5), n('C#3', 0.5), n('F3', 0.5),
        n('A3', 0.5), n('C4', 0.5), n('F4', 0.5), n('C4', 0.5),
    ], dyn='p')

    # m.60: Phrase end (4-bar: 57-60)
    add_measure(part, 60, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
        n('Bb3', 1.0, tenuto=True), r(1.0),
    ])

    # m.61-64: Final harp wash
    add_measure(part, 61, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('D5', 0.5),
    ], dyn='p')

    add_measure(part, 62, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 1.0, tenuto=True), r(1.0),
    ], dyn='pp')

    add_measure(part, 63, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 2.0, tenuto=True), r(2.0),
    ], dyn='ppp')

    # m.64: Final (4-bar: 61-64)
    add_measure(part, 64, [
        ch(['Bb2', 'D3', 'F3', 'Bb3', 'D4'], 4.0, fermata=True),
    ])


# -- Violin I Part ---------------------------------------------------------

def build_violin(part):
    """Violin I: soaring melodies, doubles flute in sections, independent lines.

    Revision 1: matching key changes, chromatic passing tones, triplets.
    """
    BAR = 4.0
    TRIPLET = 1.0 / 3.0

    # == Section I (mm.1-16) ==
    for m_num in range(1, 5):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('B-')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.5-8: Violin enters with sustained pads
    add_measure(part, 5, [
        n('F4', 2.0, tenuto=True), n('E4', 1.0), n('D4', 1.0),
    ], dyn='pp', expression_text='con sordino')

    add_measure(part, 6, [
        n('Bb3', 2.0, tenuto=True), n('D4', 2.0),
    ])

    add_measure(part, 7, [
        n('Eb4', 2.0, tenuto=True), n('D4', 2.0),
    ])

    # m.8: Phrase end (4-bar: 5-8)
    add_measure(part, 8, [
        n('C#4', 1.0), n('C4', 1.0, tenuto=True), r(2.0),
    ])

    # m.9-12: More melodic with chromatic neighbors
    add_measure(part, 9, [
        n('D4', 1.0), n('F4', 1.0), n('Bb4', 1.5, tenuto=True), n('A4', 0.5),
    ], dyn='p')

    add_measure(part, 10, [
        n('G#4', 0.5), n('G4', 0.5), n('F4', 1.0), n('Eb4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 11, [
        n('C4', 1.0), n('Eb4', 1.0), n('G4', 1.5, tenuto=True), n('F#4', 0.5),
    ])

    # m.12: Phrase end (4-bar: 9-12)
    add_measure(part, 12, [
        n('Eb4', 1.0), n('D4', 1.0, tenuto=True), r(2.0),
    ])

    # m.13-16: Building to section II
    add_measure(part, 13, [
        n('Bb4', 1.0, tenuto=True), n('A4', 0.5), n('Bb4', 0.5),
        n('C#5', 1.0), n('D5', 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('Eb5', 1.5, tenuto=True), n('D5', 0.5), n('C5', 1.0), r(1.0),
    ])

    add_measure(part, 15, [
        n('Bb4', 1.0), n('C5', 0.5), n('D5', 0.5),
        n('Eb5', 1.0, tenuto=True), n('D5', 1.0),
    ])

    # m.16: Phrase end (4-bar: 13-16)
    add_measure(part, 16, [
        n('C#5', 0.5), n('C5', 0.5), n('Bb4', 1.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.17-32) ==
    add_measure(part, 17, [
        n('D4', 1.0), n('F4', 1.0), n('Bb4', 1.5, accent=True), n('A4', 0.5),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=80))

    add_measure(part, 18, [
        n('Bb4', 2.0, tenuto=True), n('A4', 0.5), n('G#4', 0.5), n('G4', 1.0),
    ])

    add_measure(part, 19, [
        n('G4', 1.0), n('Bb4', 1.0), n('C5', 1.5, accent=True), n('Bb4', 0.5),
    ])

    # m.20: Phrase end (4-bar: 17-20)
    add_measure(part, 20, [
        n('A4', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24: Db major
    add_measure(part, 21, [
        n('F4', 1.0), n('Ab4', 1.0), n('Db5', 1.5, accent=True), n('C5', 0.5),
    ], dyn='f', ks=key.Key('D-'))

    add_measure(part, 22, [
        n('Bb4', 1.5), n('Ab4', 0.5), n('Gb4', 1.0, tenuto=True), n('F4', 1.0),
    ])

    add_measure(part, 23, [
        n('Eb4', 1.0), n('Gb4', 0.5), n('Ab4', 0.5),
        n('Bb4', 1.0, accent=True), n('Db5', 1.0),
    ])

    # m.24: Phrase end (4-bar: 21-24)
    add_measure(part, 24, [
        n('C5', 2.0, tenuto=True), n('Bb4', 1.0), r(1.0),
    ])

    # m.25-28: Eb major with triplet descent
    add_measure(part, 25, [
        n('Eb5', TRIPLET, accent=True), n('D5', TRIPLET), n('C5', TRIPLET),
        n('Bb4', TRIPLET), n('Ab4', TRIPLET), n('G4', TRIPLET),
        n('Ab4', 1.0, tenuto=True), n('G4', 1.0),
    ], ks=key.Key('E-'))

    add_measure(part, 26, [
        n('F4', 1.5), n('Eb4', 0.5), n('D4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 27, [
        n('Ab4', 1.0), n('Bb4', 0.5), n('C5', 0.5),
        n('Bb4', 1.0, tenuto=True), n('Ab4', 1.0),
    ])

    # m.28: Phrase end (4-bar: 25-28)
    add_measure(part, 28, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Transition back to Bb
    add_measure(part, 29, [
        n('Bb4', 2.0, tenuto=True), n('A4', 2.0),
    ], dyn='mp', ks=key.Key('B-'))

    add_measure(part, 30, [
        n('G#4', 1.0), n('G4', 1.0, tenuto=True), n('F#4', 2.0),
    ])

    add_measure(part, 31, [
        n('D4', 1.0), n('F#4', 1.0), n('A4', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.32: Phrase end (4-bar: 29-32)
    add_measure(part, 32, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.33-48) ==
    # m.33-36: Pizzicato in G minor
    add_measure(part, 33, [
        n('G4', 0.5, staccato=True), r(0.5), n('Bb4', 0.5, staccato=True), r(0.5),
        n('D5', 0.5, staccato=True), r(0.5), n('G4', 0.5, staccato=True), r(0.5),
    ], dyn='p', ks=key.Key('g'),
       expression_text='pizz.',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=66,
                                       text="Misterioso"))

    add_measure(part, 34, [
        n('Eb4', 0.5, staccato=True), r(0.5), n('G4', 0.5, staccato=True), r(0.5),
        n('Bb4', 0.5, staccato=True), r(0.5), n('Eb4', 0.5, staccato=True), r(0.5),
    ])

    add_measure(part, 35, [
        n('C4', 0.5, staccato=True), r(0.5), n('Eb4', 0.5, staccato=True), r(0.5),
        n('G4', 0.5, staccato=True), r(0.5), n('C4', 0.5, staccato=True), r(0.5),
    ])

    # m.36: Phrase end (4-bar: 33-36)
    add_measure(part, 36, [
        n('D4', 0.5, staccato=True), r(0.5), n('F#4', 0.5, staccato=True), r(0.5),
        n('A4', 1.0, tenuto=True), r(1.0),
    ])

    # m.37-40: Bb minor, arco
    add_measure(part, 37, [
        n('Bb4', 1.0, tenuto=True), n('Db5', 1.0), n('F5', 1.0, accent=True), n('Eb5', 1.0),
    ], dyn='mp', expression_text='arco', ks=key.Key('b-'))

    add_measure(part, 38, [
        n('Db5', 1.5), n('C5', 0.5), n('Bb4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 39, [
        n('Ab4', 1.0), n('Bb4', 1.0), n('C5', 1.0, tenuto=True), n('Db5', 1.0),
    ])

    # m.40: Phrase end (4-bar: 37-40)
    add_measure(part, 40, [
        n('F5', 1.0), n('Eb5', 1.0, tenuto=True), r(2.0),
    ])

    # m.41-44: C minor
    add_measure(part, 41, [
        n('Eb4', 1.0), n('G4', 0.5), n('Ab4', 0.5),
        n('Bb4', 1.0, tenuto=True), n('Ab4', 1.0),
    ], dyn='p', ks=key.Key('c'))

    add_measure(part, 42, [
        n('G4', 1.5), n('F4', 0.5), n('Eb4', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 43, [
        n('D4', 0.5), n('Eb4', 0.5), n('F#4', 1.0, accent=True),
        n('G4', 1.0, tenuto=True), n('Ab4', 1.0),
    ])

    # m.44: Phrase end (4-bar: 41-44)
    add_measure(part, 44, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: D major, building
    add_measure(part, 45, [
        n('A4', 1.0), n('B4', 1.0), n('D5', 1.0, accent=True), n('E5', 1.0),
    ], dyn='mf', ks=key.Key('D'))

    add_measure(part, 46, [
        n('F#5', 1.5, tenuto=True), n('E5', 0.5), n('D5', 1.0), n('C#5', 1.0),
    ])

    add_measure(part, 47, [
        n('B4', 1.0), n('C#5', 0.5), n('D5', 0.5),
        n('E5', 1.0, accent=True), n('F#5', 1.0),
    ], dyn='f')

    # m.48: Phrase end (4-bar: 45-48)
    add_measure(part, 48, [
        n('F#5', 2.0, tenuto=True), r(2.0),
    ])

    # == Section IV (mm.49-64) ==
    # m.49-52: Eb major
    add_measure(part, 49, [
        n('G5', 1.0, accent=True), n('Bb5', 1.0),
        n('Eb6', 1.5, accent=True), n('D6', 0.5),
    ], dyn='ff',
       ks=key.Key('E-'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=76,
                                       text="Maestoso"))

    add_measure(part, 50, [
        n('C6', 2.0, tenuto=True), n('Bb5', 1.0, accent=True), n('Ab5', 1.0),
    ])

    add_measure(part, 51, [
        n('G5', 1.0), n('Ab5', 1.0, accent=True),
        n('Bb5', 1.0, tenuto=True), n('C6', 1.0),
    ])

    # m.52: Phrase end (4-bar: 49-52)
    add_measure(part, 52, [
        n('Bb5', 2.0, tenuto=True), r(2.0),
    ])

    # m.53-56: Ab major climax
    add_measure(part, 53, [
        n('C6', 1.0, accent=True), n('Bb5', 0.5), n('Ab5', 0.5),
        n('G5', 1.0), n('F5', 1.0),
    ], dyn='ff', ks=key.Key('A-'))

    add_measure(part, 54, [
        n('Eb5', 1.0), n('F5', 0.5), n('G5', 0.5),
        n('Ab5', 2.0, tenuto=True),
    ])

    add_measure(part, 55, [
        n('G5', 1.0, accent=True), n('F5', 0.5), n('Eb5', 0.5),
        n('Db5', 1.0), n('Eb5', 1.0),
    ], dyn='f')

    # m.56: Phrase end (4-bar: 53-56)
    add_measure(part, 56, [
        n('Eb5', 2.0, tenuto=True), r(2.0),
    ])

    # m.57-60: Bb major, settling
    add_measure(part, 57, [
        n('D5', 1.0, tenuto=True), n('C5', 1.0), n('Bb4', 1.0), n('A4', 1.0),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 58, [
        n('Bb4', 2.0, tenuto=True), n('D5', 1.0), r(1.0),
    ], dyn='mp')

    add_measure(part, 59, [
        n('Eb5', 0.75), n('D5', 0.25), n('C#5', 0.5), n('C5', 0.5),
        n('Bb4', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.60: Phrase end (4-bar: 57-60)
    add_measure(part, 60, [
        n('A4', 2.0, tenuto=True), r(2.0),
    ])

    # m.61-64: Final
    add_measure(part, 61, [
        n('D5', 1.0), n('F5', 1.0), n('Bb5', 1.5, tenuto=True), n('A5', 0.5),
    ], dyn='p')

    add_measure(part, 62, [
        n('G5', 2.0, tenuto=True), n('F5', 1.0), r(1.0),
    ], dyn='pp')

    add_measure(part, 63, [
        n('D5', 4.0, tenuto=True),
    ], dyn='ppp')

    # m.64: Final (4-bar: 61-64)
    add_measure(part, 64, [
        n('Bb4', 4.0, fermata=True),
    ])


# -- Viola Part ------------------------------------------------------------

def build_viola(part):
    """Viola: warm inner voice, leads the dark section, rich harmonics.

    Revision 1: matching key changes, chromatic neighbor tones, triplet figures.
    """
    BAR = 4.0
    TRIPLET = 1.0 / 3.0

    # == Section I (mm.1-16) ==
    for m_num in range(1, 9):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('B-')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.9-12: Viola enters with warm sustained notes, chromatic inflections
    add_measure(part, 9, [
        n('Bb3', 2.0, tenuto=True), n('A3', 1.0), n('Ab3', 1.0),
    ], dyn='p', expression_text='espress.')

    add_measure(part, 10, [
        n('G3', 2.0, tenuto=True), n('F#3', 0.5), n('F3', 0.5), r(1.0),
    ])

    add_measure(part, 11, [
        n('Eb3', 2.0, tenuto=True), n('G3', 2.0),
    ])

    # m.12: Phrase end (4-bar: 9-12)
    add_measure(part, 12, [
        n('F3', 2.0, tenuto=True), r(2.0),
    ])

    # m.13-16
    add_measure(part, 13, [
        n('D3', 1.0), n('F3', 1.0), n('Bb3', 1.0, tenuto=True), n('A3', 1.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('G#3', 0.5), n('G3', 1.5, tenuto=True), r(2.0),
    ])

    add_measure(part, 15, [
        n('Eb3', 1.0), n('F3', 0.5), n('G3', 0.5), n('A3', 1.0, tenuto=True), r(1.0),
    ])

    # m.16: Phrase end (4-bar: 13-16)
    add_measure(part, 16, [
        n('F3', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.17-32) ==
    add_measure(part, 17, [
        n('F3', 2.0, tenuto=True), n('D3', 2.0),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=80))

    add_measure(part, 18, [
        n('C#3', 0.5), n('C3', 0.5), n('D3', 1.0), n('Eb3', 1.0, tenuto=True), n('D3', 1.0),
    ])

    add_measure(part, 19, [
        n('Eb3', 2.0, tenuto=True), n('G3', 2.0),
    ])

    # m.20: Phrase end (4-bar: 17-20)
    add_measure(part, 20, [
        n('F3', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24: Db major
    add_measure(part, 21, [
        n('Ab3', 2.0, tenuto=True), n('F3', 2.0),
    ], dyn='f', ks=key.Key('D-'))

    add_measure(part, 22, [
        n('Db3', 1.0), n('Eb3', 1.0), n('F3', 1.0, tenuto=True), n('Gb3', 1.0),
    ])

    add_measure(part, 23, [
        n('Gb3', 1.0), n('Eb3', 0.5), n('F3', 0.5),
        n('Gb3', 1.0, accent=True), n('Ab3', 1.0),
    ])

    # m.24: Phrase end (4-bar: 21-24)
    add_measure(part, 24, [
        n('Gb3', 2.0, tenuto=True), n('F3', 1.0), r(1.0),
    ])

    # m.25-28: Eb major
    add_measure(part, 25, [
        n('G3', 1.0), n('Ab3', 0.5), n('Bb3', 0.5),
        n('Ab3', 1.0, tenuto=True), n('G3', 1.0),
    ], ks=key.Key('E-'))

    add_measure(part, 26, [
        n('F3', 1.5), n('Eb3', 0.5), n('D3', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 27, [
        n('C3', 1.0), n('Eb3', 0.5), n('F3', 0.5),
        n('G3', 1.0, tenuto=True), n('F3', 1.0),
    ])

    # m.28: Phrase end (4-bar: 25-28)
    add_measure(part, 28, [
        n('Eb3', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Transition back to Bb
    add_measure(part, 29, [
        n('D3', 2.0, tenuto=True), n('C#3', 1.0), n('C3', 1.0),
    ], dyn='mp', ks=key.Key('B-'))

    add_measure(part, 30, [
        n('Bb2', 2.0, tenuto=True), n('A2', 2.0),
    ])

    add_measure(part, 31, [
        n('Bb2', 1.0), n('D3', 1.0), n('F#3', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.32: Phrase end (4-bar: 29-32)
    add_measure(part, 32, [
        n('G3', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.33-48) -- VIOLA LEADS ==
    # m.33-36: G minor
    add_measure(part, 33, [
        n('G3', 1.0, accent=True), n('Bb3', 1.0), n('D4', 1.5, tenuto=True), n('C#4', 0.5),
    ], dyn='mf', expression_text='con dolore',
       ks=key.Key('g'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=66,
                                       text="Misterioso"))

    add_measure(part, 34, [
        n('Bb3', 1.0), n('A3', 0.5), n('G#3', 0.5),
        n('F3', 1.0, tenuto=True), n('Eb3', 1.0),
    ])

    add_measure(part, 35, [
        n('D3', 1.0), n('Eb3', 1.0), n('F3', 1.0, accent=True), n('G3', 1.0),
    ])

    # m.36: Phrase end (4-bar: 33-36)
    add_measure(part, 36, [
        n('F#3', 2.0, tenuto=True), r(2.0),
    ])

    # m.37-40: Bb minor, viola continues lead
    add_measure(part, 37, [
        n('Bb3', 1.0), n('C4', 0.5), n('Db4', 0.5),
        n('Eb4', 1.0, accent=True), n('F4', 1.0),
    ], dyn='f', ks=key.Key('b-'))

    add_measure(part, 38, [
        n('Gb4', 1.5, tenuto=True), n('F4', 0.5),
        n('Eb4', 1.0), r(1.0),
    ])

    add_measure(part, 39, [
        n('Db4', 1.0), n('Eb4', 0.5), n('F4', 0.5),
        n('Gb4', 1.0, tenuto=True), n('F4', 1.0),
    ])

    # m.40: Phrase end (4-bar: 37-40)
    add_measure(part, 40, [
        n('Db4', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.41-44: C minor
    add_measure(part, 41, [
        n('C3', 1.0, tenuto=True), n('Eb3', 0.5), n('F3', 0.5),
        n('G3', 1.0), n('Ab3', 1.0),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 42, [
        n('G3', 1.5), n('F3', 0.5), n('Eb3', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 43, [
        n('D3', 0.5), n('F#3', 0.5), n('G3', 1.0, accent=True),
        n('Ab3', 1.0, tenuto=True), r(1.0),
    ])

    # m.44: Phrase end (4-bar: 41-44)
    add_measure(part, 44, [
        n('G3', 2.0, tenuto=True), r(2.0),
    ], dyn='p')

    # m.45-48: D major, building
    add_measure(part, 45, [
        n('D3', 1.0), n('F#3', 1.0), n('A3', 1.0, accent=True), n('B3', 1.0),
    ], dyn='mf', ks=key.Key('D'))

    add_measure(part, 46, [
        n('A3', 1.0), n('B3', 0.5), n('C#4', 0.5),
        n('D4', 1.0, tenuto=True), n('C#4', 1.0),
    ])

    add_measure(part, 47, [
        n('B3', 1.0), n('C#4', 0.5), n('D4', 0.5),
        n('E4', 1.0, accent=True), n('D4', 1.0),
    ], dyn='f')

    # m.48: Phrase end (4-bar: 45-48)
    add_measure(part, 48, [
        n('D4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section IV (mm.49-64) ==
    # m.49-52: Eb major
    add_measure(part, 49, [
        n('Bb3', 2.0, tenuto=True), n('G3', 2.0, accent=True),
    ], dyn='f',
       ks=key.Key('E-'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=76,
                                       text="Maestoso"))

    add_measure(part, 50, [
        n('Ab3', 2.0, tenuto=True), n('F3', 1.0), n('Eb3', 1.0),
    ])

    add_measure(part, 51, [
        n('D3', 1.0), n('Eb3', 1.0, accent=True),
        n('F3', 1.0, tenuto=True), n('G3', 1.0),
    ])

    # m.52: Phrase end (4-bar: 49-52)
    add_measure(part, 52, [
        n('Ab3', 2.0, tenuto=True), r(2.0),
    ])

    # m.53-56: Ab major
    add_measure(part, 53, [
        n('Eb4', 1.0, accent=True), n('Db4', 0.5), n('C4', 0.5),
        n('Bb3', 1.0), n('Ab3', 1.0),
    ], dyn='ff', ks=key.Key('A-'))

    add_measure(part, 54, [
        n('Gb3', 1.0), n('Ab3', 0.5), n('Bb3', 0.5),
        n('C4', 2.0, tenuto=True),
    ])

    add_measure(part, 55, [
        n('Db4', 1.0, accent=True), n('C4', 0.5), n('Bb3', 0.5),
        n('Ab3', 1.0), n('Bb3', 1.0),
    ], dyn='f')

    # m.56: Phrase end (4-bar: 53-56)
    add_measure(part, 56, [
        n('Ab3', 2.0, tenuto=True), r(2.0),
    ])

    # m.57-60: Bb major
    add_measure(part, 57, [
        n('Bb3', 1.0, tenuto=True), n('C4', 1.0), n('D4', 1.0), n('C#4', 1.0),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 58, [
        n('Bb3', 2.0, tenuto=True), n('A3', 1.0), r(1.0),
    ], dyn='mp')

    add_measure(part, 59, [
        n('G3', 1.0), n('A3', 0.5), n('Bb3', 0.5), n('A3', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.60: Phrase end (4-bar: 57-60)
    add_measure(part, 60, [
        n('F3', 2.0, tenuto=True), r(2.0),
    ])

    # m.61-64: Final
    add_measure(part, 61, [
        n('Bb3', 1.0), n('D4', 1.0), n('F4', 1.5, tenuto=True), n('E4', 0.5),
    ], dyn='p')

    add_measure(part, 62, [
        n('D4', 2.0, tenuto=True), r(2.0),
    ], dyn='pp')

    add_measure(part, 63, [
        n('Bb3', 4.0, tenuto=True),
    ], dyn='ppp')

    # m.64: Final (4-bar: 61-64)
    add_measure(part, 64, [
        n('F3', 4.0, fermata=True),
    ])


# -- Cello Part ------------------------------------------------------------

def build_cello(part):
    """Cello: bass foundation, rich low melodies in dark section.

    Revision 1: matching key changes, chromatic bass motion, triplet figures.
    """
    BAR = 4.0
    TRIPLET = 1.0 / 3.0

    # == Section I (mm.1-16) ==
    for m_num in range(1, 5):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('B-')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.5-8: Cello enters with deep bass, chromatic neighbors
    add_measure(part, 5, [
        n('Bb1', 2.0, tenuto=True), n('D2', 2.0),
    ], dyn='p')

    add_measure(part, 6, [
        n('G1', 2.0, tenuto=True), n('Bb1', 2.0),
    ])

    add_measure(part, 7, [
        n('Eb2', 2.0, tenuto=True), n('E2', 1.0), n('F2', 1.0),
    ])

    # m.8: Phrase end (4-bar: 5-8)
    add_measure(part, 8, [
        n('F2', 1.0), n('F#2', 1.0, tenuto=True), r(2.0),
    ])

    # m.9-12: Walking bass with chromatic passing tones
    add_measure(part, 9, [
        n('Bb1', 1.0), n('D2', 1.0), n('F2', 1.0), n('Bb2', 1.0),
    ], dyn='mp')

    add_measure(part, 10, [
        n('Eb2', 1.0), n('G2', 1.0), n('Bb2', 1.0), r(1.0),
    ])

    add_measure(part, 11, [
        n('C2', 1.0), n('E2', 1.0), n('G2', 1.0), n('Bb2', 1.0),
    ])

    # m.12: Phrase end (4-bar: 9-12)
    add_measure(part, 12, [
        n('F2', 0.75), n('F#2', 0.25), n('A2', 1.0, tenuto=True), r(2.0),
    ])

    # m.13-16
    add_measure(part, 13, [
        n('Bb1', 2.0, tenuto=True), n('Eb2', 2.0),
    ], dyn='mp')

    add_measure(part, 14, [
        n('F2', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 15, [
        n('Eb2', 1.0), n('F2', 0.5), n('G2', 0.5), n('A2', 1.0, tenuto=True), r(1.0),
    ])

    # m.16: Phrase end (4-bar: 13-16)
    add_measure(part, 16, [
        n('Bb1', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.17-32) ==
    add_measure(part, 17, [
        n('Bb1', 2.0, tenuto=True), n('F2', 2.0),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=80))

    add_measure(part, 18, [
        n('F1', 2.0, tenuto=True), n('C2', 2.0),
    ])

    add_measure(part, 19, [
        n('Eb2', 2.0, tenuto=True), n('Bb1', 2.0),
    ])

    # m.20: Phrase end (4-bar: 17-20)
    add_measure(part, 20, [
        n('F2', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24: Db major
    add_measure(part, 21, [
        n('Db2', 2.0, tenuto=True), n('Ab1', 2.0),
    ], dyn='f', ks=key.Key('D-'))

    add_measure(part, 22, [
        n('Gb1', 2.0, tenuto=True), n('Db2', 2.0),
    ])

    add_measure(part, 23, [
        n('Ab1', 1.0), n('Cb2', 1.0), n('Eb2', 1.0, accent=True), n('Gb2', 1.0),
    ])

    # m.24: Phrase end (4-bar: 21-24)
    add_measure(part, 24, [
        n('Db2', 2.0, tenuto=True), r(2.0),
    ])

    # m.25-28: Eb major
    add_measure(part, 25, [
        n('Eb2', 1.0, accent=True), n('D2', 1.0), n('C2', 1.0), n('Bb1', 1.0),
    ], ks=key.Key('E-'))

    add_measure(part, 26, [
        n('Ab1', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 27, [
        n('F1', 1.0), n('Ab1', 1.0), n('B1', 0.5), n('C2', 0.5, tenuto=True), n('F2', 1.0),
    ])

    # m.28: Phrase end (4-bar: 25-28)
    add_measure(part, 28, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Transition back to Bb with chromatic bass
    add_measure(part, 29, [
        n('D2', 2.0, tenuto=True), n('C#2', 1.0), n('C2', 1.0),
    ], dyn='mp', ks=key.Key('B-'))

    add_measure(part, 30, [
        n('Bb1', 2.0, tenuto=True), n('A1', 2.0),
    ])

    add_measure(part, 31, [
        n('D2', 1.0), n('F#2', 1.0), n('A2', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.32: Phrase end (4-bar: 29-32)
    add_measure(part, 32, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ])

    # == Section III (mm.33-48) ==
    # m.33-36: G minor, CELLO LEADS with viola
    add_measure(part, 33, [
        n('G2', 1.0, accent=True), n('Bb2', 1.0), n('D3', 1.0, tenuto=True), n('C#3', 1.0),
    ], dyn='mf', expression_text='pesante',
       ks=key.Key('g'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=66,
                                       text="Misterioso"))

    add_measure(part, 34, [
        n('Bb2', 1.0), n('A2', 0.5), n('Ab2', 0.5),
        n('F2', 1.0, tenuto=True), n('Eb2', 1.0),
    ])

    add_measure(part, 35, [
        n('D2', 1.0), n('Eb2', 1.0), n('F2', 1.0, accent=True), n('G2', 1.0),
    ])

    # m.36: Phrase end (4-bar: 33-36)
    add_measure(part, 36, [
        n('D2', 2.0, tenuto=True), r(2.0),
    ])

    # m.37-40: Bb minor -- deeper, intense
    add_measure(part, 37, [
        n('Bb1', 1.0, accent=True), n('Db2', 1.0), n('F2', 1.0), n('Bb2', 1.0),
    ], dyn='f', ks=key.Key('b-'))

    add_measure(part, 38, [
        n('Gb2', 1.5, tenuto=True), n('F2', 0.5), n('Eb2', 1.0), r(1.0),
    ])

    add_measure(part, 39, [
        n('Ab1', 1.0), n('Cb2', 1.0), n('Eb2', 1.0, tenuto=True), n('Gb2', 1.0),
    ])

    # m.40: Phrase end (4-bar: 37-40)
    add_measure(part, 40, [
        n('Db2', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.41-44: C minor
    add_measure(part, 41, [
        n('C2', 1.0, tenuto=True), n('Eb2', 0.5), n('F2', 0.5),
        n('G2', 1.0), n('Ab2', 1.0),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 42, [
        n('F2', 1.5), n('Eb2', 0.5), n('D2', 1.0, tenuto=True), r(1.0),
    ])

    add_measure(part, 43, [
        n('Eb2', 0.5), n('F#2', 0.5), n('G2', 1.0, accent=True),
        n('D2', 1.0, tenuto=True), r(1.0),
    ])

    # m.44: Phrase end (4-bar: 41-44)
    add_measure(part, 44, [
        n('G1', 2.0, tenuto=True), r(2.0),
    ], dyn='p')

    # m.45-48: D major, building with triplet bass
    add_measure(part, 45, [
        n('D2', 1.0), n('F#2', 1.0), n('A2', 1.0, accent=True), n('D3', 1.0),
    ], dyn='mf', ks=key.Key('D'))

    add_measure(part, 46, [
        n('G2', TRIPLET), n('A2', TRIPLET), n('B2', TRIPLET),
        n('C#3', 1.0, tenuto=True), n('B2', 1.0), n('A2', 1.0),
    ])

    add_measure(part, 47, [
        n('G2', 1.0), n('A2', 0.5), n('B2', 0.5),
        n('C#3', 1.0, accent=True), n('D3', 1.0),
    ], dyn='f')

    # m.48: Phrase end (4-bar: 45-48)
    add_measure(part, 48, [
        n('D2', 2.0, tenuto=True), r(2.0),
    ])

    # == Section IV (mm.49-64) ==
    # m.49-52: Eb major
    add_measure(part, 49, [
        n('Eb2', 2.0, tenuto=True), n('G2', 2.0, accent=True),
    ], dyn='f',
       ks=key.Key('E-'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.0), number=76,
                                       text="Maestoso"))

    add_measure(part, 50, [
        n('Ab1', 2.0, tenuto=True), n('Eb2', 2.0),
    ])

    add_measure(part, 51, [
        n('Bb1', 1.0), n('D2', 1.0), n('F2', 1.0, accent=True), n('Bb2', 1.0),
    ])

    # m.52: Phrase end (4-bar: 49-52)
    add_measure(part, 52, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ])

    # m.53-56: Ab major
    add_measure(part, 53, [
        n('Ab1', 1.0, accent=True), n('Bb1', 0.5), n('C2', 0.5),
        n('Db2', 1.0), n('Eb2', 1.0),
    ], dyn='ff', ks=key.Key('A-'))

    add_measure(part, 54, [
        n('F2', 1.0), n('Eb2', 0.5), n('Db2', 0.5),
        n('C2', 2.0, tenuto=True),
    ])

    add_measure(part, 55, [
        n('Db2', 1.0, accent=True), n('Eb2', 0.5), n('F2', 0.5),
        n('G2', 1.0), n('Ab2', 1.0),
    ], dyn='f')

    # m.56: Phrase end (4-bar: 53-56)
    add_measure(part, 56, [
        n('Ab1', 2.0, tenuto=True), r(2.0),
    ])

    # m.57-60: Bb major, winding down
    add_measure(part, 57, [
        n('Bb1', 2.0, tenuto=True), n('F2', 2.0),
    ], dyn='mf', ks=key.Key('B-'))

    add_measure(part, 58, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ], dyn='mp')

    add_measure(part, 59, [
        n('F2', 0.75), n('Eb2', 0.25), n('D2', 0.5), n('C#2', 0.5),
        n('C2', 1.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.60: Phrase end (4-bar: 57-60)
    add_measure(part, 60, [
        n('Bb1', 2.0, tenuto=True), r(2.0),
    ])

    # m.61-64: Final
    add_measure(part, 61, [
        n('Bb1', 2.0, tenuto=True), n('D2', 2.0),
    ], dyn='p')

    add_measure(part, 62, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ], dyn='pp')

    add_measure(part, 63, [
        n('F1', 4.0, tenuto=True),
    ], dyn='ppp')

    # m.64: Final (4-bar: 61-64)
    add_measure(part, 64, [
        n('Bb1', 4.0, fermata=True),
    ])


# -- Hairpins --------------------------------------------------------------

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins across all parts."""

    def get_part_by_name(score, name):
        for p in score.parts:
            if name.lower() in (p.partName or '').lower():
                return p
        return None

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
        ('harp', 9, 11, 'crescendo'),
        ('harp', 33, 35, 'diminuendo'),
        ('harp', 37, 39, 'crescendo'),
        ('harp', 45, 47, 'crescendo'),
        ('harp', 49, 51, 'crescendo'),
        ('harp', 53, 55, 'diminuendo'),
        ('harp', 57, 59, 'diminuendo'),
        ('harp', 61, 63, 'diminuendo'),
        # Flute
        ('flute', 9, 11, 'crescendo'),
        ('flute', 17, 19, 'crescendo'),
        ('flute', 21, 23, 'crescendo'),
        ('flute', 25, 27, 'diminuendo'),
        ('flute', 45, 47, 'crescendo'),
        ('flute', 49, 51, 'crescendo'),
        ('flute', 53, 55, 'diminuendo'),
        ('flute', 57, 59, 'diminuendo'),
        ('flute', 61, 63, 'diminuendo'),
        # Horn
        ('horn', 5, 7, 'diminuendo'),
        ('horn', 13, 15, 'crescendo'),
        ('horn', 45, 47, 'crescendo'),
        ('horn', 49, 51, 'crescendo'),
        ('horn', 53, 55, 'diminuendo'),
        ('horn', 57, 59, 'diminuendo'),
        ('horn', 61, 63, 'diminuendo'),
        # Violin
        ('violin', 9, 11, 'crescendo'),
        ('violin', 13, 15, 'crescendo'),
        ('violin', 17, 19, 'crescendo'),
        ('violin', 21, 23, 'crescendo'),
        ('violin', 37, 39, 'crescendo'),
        ('violin', 45, 47, 'crescendo'),
        ('violin', 49, 51, 'crescendo'),
        ('violin', 53, 55, 'diminuendo'),
        ('violin', 57, 59, 'diminuendo'),
        # Viola
        ('viola', 33, 35, 'crescendo'),
        ('viola', 37, 39, 'crescendo'),
        ('viola', 45, 47, 'crescendo'),
        ('viola', 49, 51, 'crescendo'),
        ('viola', 53, 55, 'diminuendo'),
        ('viola', 57, 59, 'diminuendo'),
        # Cello
        ('cello', 5, 7, 'crescendo'),
        ('cello', 9, 11, 'crescendo'),
        ('cello', 33, 35, 'crescendo'),
        ('cello', 37, 39, 'crescendo'),
        ('cello', 45, 47, 'crescendo'),
        ('cello', 49, 51, 'crescendo'),
        ('cello', 53, 55, 'diminuendo'),
        ('cello', 57, 59, 'diminuendo'),
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        target_part = get_part_by_name(score, part_name)
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
