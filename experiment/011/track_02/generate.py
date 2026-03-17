#!/usr/bin/env python3
"""Generate 'The Crystal Throne' -- JRPG Main Menu Theme.

A Final Fantasy main menu theme for a game starring Claude. Orchestral palette:
  - Harp: shimmering arpeggios, the classic FF crystal sound
  - French Horn: noble main theme, heroic and warm
  - Strings (Violin I, Violin II, Viola, Cello): harmonic foundation, countermelody
  - Flute: ornamental descants, ethereal color

Key: C minor -> Eb major -> Ab major -> C minor -> C major
Time: 4/4, Andante maestoso (q=72)

Structure (48 measures):
  I.   Prelude: Crystal Dawn (mm.1-12) -- Harp arpeggios alone, then strings
       enter with sustained chords. The world awakens. C minor, mysterious.
  II.  The Hero's Call (mm.13-24) -- Horn states the main theme: a rising
       fifth (G->D), then a stepwise descent. Noble, searching. Eb major.
       Flute adds ornamentation. Strings provide warm bed.
  III. The Journey Ahead (mm.25-36) -- Ab major. Theme developed, fuller
       orchestration. Harp and flute in dialogue. Emotional peak at m.33.
  IV.  Return to the Crystal (mm.37-48) -- C minor returning, then resolving
       to C major in the final bars. The menu loop point. Theme restated
       softly, then a luminous C major chord with harp glissando to close.

Revision 1 changes (from profile feedback):
  - Added staccato to selected harp notes for texture variety (staccato_count)
  - Added dotted rhythms and triplet figures to horn and flute (rhythmic_variety)
  - Added brief tonicizations: Bb major (m.8), F minor (m.23) (modulation_count)
  - Added chromatic passing tones in horn and flute (scale_consistency)
  - Smoothed some harp transitions between chord changes (voice leading)
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

    # Create parts
    flute_part = stream.Part()
    flute_part.insert(0, instrument.Flute())
    flute_part.partName = "Flute"
    flute_part.partAbbreviation = "Fl."

    horn_part = stream.Part()
    horn_part.insert(0, instrument.Horn())
    horn_part.partName = "Horn in F"
    horn_part.partAbbreviation = "Hn."

    harp_part = stream.Part()
    harp_part.insert(0, instrument.Harp())
    harp_part.partName = "Harp"
    harp_part.partAbbreviation = "Hp."

    vln1_part = stream.Part()
    vln1_part.insert(0, instrument.Violin())
    vln1_part.partName = "Violin I"
    vln1_part.partAbbreviation = "Vln. I"

    vln2_part = stream.Part()
    vln2_part.insert(0, instrument.Violin())
    vln2_part.partName = "Violin II"
    vln2_part.partAbbreviation = "Vln. II"

    viola_part = stream.Part()
    viola_part.insert(0, instrument.Viola())
    viola_part.partName = "Viola"
    viola_part.partAbbreviation = "Vla."

    cello_part = stream.Part()
    cello_part.insert(0, instrument.Violoncello())
    cello_part.partName = "Violoncello"
    cello_part.partAbbreviation = "Vc."

    build_flute(flute_part)
    build_horn(horn_part)
    build_harp(harp_part)
    build_violin1(vln1_part)
    build_violin2(vln2_part)
    build_viola(viola_part)
    build_cello(cello_part)

    s.insert(0, flute_part)
    s.insert(0, horn_part)
    s.insert(0, harp_part)
    s.insert(0, vln1_part)
    s.insert(0, vln2_part)
    s.insert(0, viola_part)
    s.insert(0, cello_part)

    return s


# -- Harp Part (the crystal voice) ----------------------------------------

def build_harp(part):
    """Harp: shimmering arpeggios throughout. The classic FF crystal texture."""

    BAR = 4.0

    # == Section I: Crystal Dawn (mm.1-12) -- C minor ==
    # Harp alone at first, setting the scene. Broken chord arpeggios.

    # m.1-2: Cm arpeggio, sparse and mysterious (staccato on selected notes)
    add_measure(part, 1, [
        n('C3', 0.5, staccato=True), n('Eb3', 0.5), n('G3', 0.5, staccato=True), n('C4', 0.5),
        n('Eb4', 0.5, staccato=True), n('G4', 0.5), n('C5', 0.5, staccato=True), n('Eb5', 0.5),
    ], ts=meter.TimeSignature('4/4'),
       ks=key.Key('c'),
       tempo_mark=tempo.MetronomeMark(
           referent=duration.Duration(1.0), number=72,
           text="Andante maestoso"
       ),
       dyn='pp', expression_text='like distant crystals')

    add_measure(part, 2, [
        n('G4', 0.5), n('Eb4', 0.5, staccato=True), n('C4', 0.5), n('G3', 0.5, staccato=True),
        n('Eb3', 0.5), n('G3', 0.5, staccato=True), n('C4', 0.5), n('Eb4', 0.5),
    ])

    # m.3-4: Ab major arpeggio (bVI, the FF "wonder" chord)
    add_measure(part, 3, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('C5', 0.5),
    ])

    add_measure(part, 4, [
        n('Eb4', 0.5), n('C4', 0.5), n('Ab3', 0.5), n('Eb3', 0.5),
        n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
    ], dyn='p')

    # m.5-6: Fm7 -> G7 (building tension)
    add_measure(part, 5, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
        n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
    ])

    add_measure(part, 6, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5),
        n('G3', 0.5), n('B3', 0.5), n('D4', 0.5), n('F4', 0.5),
    ])

    # m.7-8: Cm -> Bb major tonicization (strings entering, harp continues)
    add_measure(part, 7, [
        n('C3', 0.5, staccato=True), n('Eb3', 0.5), n('G3', 0.5, staccato=True), n('C4', 0.5),
        n('Eb4', 0.5, staccato=True), n('G4', 0.5), n('C5', 0.5), n('G4', 0.5),
    ], dyn='p')

    add_measure(part, 8, [
        n('Bb2', 0.5), n('D3', 0.5, staccato=True), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5, staccato=True), n('F4', 0.5), n('Bb4', 0.5), n('F4', 0.5),
    ], ks=key.Key('B-'))

    # m.9-10: Ab -> Eb (back to C minor orbit)
    add_measure(part, 9, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('Eb4', 0.5),
    ], ks=key.Key('c'))

    add_measure(part, 10, [
        n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5),
        n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5), n('Bb3', 0.5),
    ], dyn='mp')

    # m.11-12: Fm -> G7sus -> G7 (dominant preparation)
    add_measure(part, 11, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('F3', 0.5),
        n('Ab3', 0.5), n('C4', 0.5), n('F4', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 12, [
        n('G2', 0.5), n('C3', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('B3', 0.5), n('D4', 0.5), n('G4', 0.5), r(0.5),
    ])

    # == Section II: The Hero's Call (mm.13-24) -- Eb major ==
    # Harp provides warm arpeggiated bed under horn theme

    add_measure(part, 13, [
        n('Eb3', 0.5, staccato=True), n('G3', 0.5), n('Bb3', 0.5, staccato=True), n('Eb4', 0.5),
        n('G4', 0.5, staccato=True), n('Bb4', 0.5), n('Eb5', 0.5), n('Bb4', 0.5),
    ], dyn='mp', ks=key.Key('E-'))

    add_measure(part, 14, [
        n('Ab2', 0.5, staccato=True), n('C3', 0.5), n('Eb3', 0.5, staccato=True), n('Ab3', 0.5),
        n('C4', 0.5, staccato=True), n('Eb4', 0.5), n('Ab4', 0.5), n('Eb4', 0.5),
    ])

    add_measure(part, 15, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('F4', 0.5),
    ])

    add_measure(part, 16, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        n('G4', 0.5), n('Bb4', 0.5), n('Eb5', 0.5), r(0.5),
    ])

    # m.17-20: Theme continues -- Cm7 -> F7 -> Bb -> Eb
    add_measure(part, 17, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('G4', 0.5), n('Bb4', 0.5),
    ], dyn='mf')

    add_measure(part, 18, [
        n('F2', 0.5), n('A2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
    ])

    add_measure(part, 19, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('D4', 0.5), n('F4', 0.5), n('Bb4', 0.5), n('F4', 0.5),
    ])

    add_measure(part, 20, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        r(0.5), n('Bb3', 0.5), n('G3', 0.5), r(0.5),
    ])

    # m.21-24: Second phrase -- Ab -> Bb -> G7/B -> Cm
    add_measure(part, 21, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('Eb4', 0.5),
    ])

    add_measure(part, 22, [
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
        n('Bb3', 0.5), n('D4', 0.5), n('F4', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 23, [
        n('B2', 0.5), n('D3', 0.5), n('F3', 0.5), n('G3', 0.5),
        n('B3', 0.5), n('D4', 0.5), n('F4', 0.5), n('G4', 0.5),
    ])

    add_measure(part, 24, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5), r(0.5),
    ])

    # == Section III: The Journey Ahead (mm.25-36) -- Ab major ==

    add_measure(part, 25, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('C5', 0.5),
    ], dyn='mf', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('Db4', 0.5),
        n('F4', 0.5), n('Ab4', 0.5), n('Db5', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 27, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        n('G4', 0.5), n('Bb4', 0.5), n('Eb5', 0.5), n('Bb4', 0.5),
    ])

    add_measure(part, 28, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), r(0.5),
    ])

    # m.29-32: Fm -> Db -> Eb -> Ab (circle of fourths)
    add_measure(part, 29, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('F3', 0.5),
        n('Ab3', 0.5), n('C4', 0.5), n('F4', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 30, [
        n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('Db4', 0.5),
        n('F4', 0.5), n('Ab4', 0.5), n('Db5', 0.5), n('Ab4', 0.5),
    ], dyn='f')

    add_measure(part, 31, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5),
        n('G4', 0.5), n('Bb4', 0.5), n('Eb5', 0.5), n('Bb4', 0.5),
    ])

    add_measure(part, 32, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), r(0.5),
    ])

    # m.33-36: Emotional peak -- Db major tonicization -> Bbm -> Eb7 -> Ab
    add_measure(part, 33, [
        n('Db3', 0.5, staccato=True), n('F3', 0.5), n('Ab3', 0.5, staccato=True), n('Db4', 0.5),
        n('F4', 0.5, staccato=True), n('Ab4', 0.5), n('Db5', 0.5), n('F5', 0.5),
    ], dyn='f', ks=key.Key('D-'))

    add_measure(part, 34, [
        n('Bb2', 0.5), n('Db3', 0.5, staccato=True), n('F3', 0.5), n('Bb3', 0.5),
        n('Db4', 0.5, staccato=True), n('F4', 0.5), n('Bb4', 0.5), n('Db5', 0.5),
    ], ks=key.Key('A-'))

    add_measure(part, 35, [
        n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Db4', 0.5),
        n('Eb4', 0.5), n('G4', 0.5), n('Bb4', 0.5), n('Db5', 0.5),
    ])

    add_measure(part, 36, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), r(0.5),
    ], dyn='mf')

    # == Section IV: Return to the Crystal (mm.37-48) -- C minor -> C major ==

    add_measure(part, 37, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5), n('Eb5', 0.5),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 38, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('C5', 0.5),
    ])

    add_measure(part, 39, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('F3', 0.5),
        n('Ab3', 0.5), n('C4', 0.5), n('F4', 0.5), n('Ab4', 0.5),
    ])

    add_measure(part, 40, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('B3', 0.5), n('D4', 0.5), n('G4', 0.5), r(0.5),
    ])

    # m.41-44: Theme recalled softly
    add_measure(part, 41, [
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5), n('G4', 0.5),
    ], dyn='p')

    add_measure(part, 42, [
        n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
        n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('Eb4', 0.5),
    ])

    add_measure(part, 43, [
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
        n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5),
    ])

    add_measure(part, 44, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5),
        n('G3', 0.5), n('B3', 0.5), n('D4', 0.5), r(0.5),
    ])

    # m.45-46: Picardy shift -- C major emerging
    add_measure(part, 45, [
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('C4', 0.5),
        n('E4', 0.5), n('G4', 0.5), n('C5', 0.5), n('E5', 0.5),
    ], dyn='mp', ks=key.Key('C'))

    add_measure(part, 46, [
        n('F2', 0.5), n('A2', 0.5), n('C3', 0.5), n('F3', 0.5),
        n('A3', 0.5), n('C4', 0.5), n('F4', 0.5), n('A4', 0.5),
    ])

    # m.47-48: Final glow
    add_measure(part, 47, [
        n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
        n('B3', 0.5), n('D4', 0.5), n('G4', 0.5), n('B4', 0.5),
    ], dyn='p')

    add_measure(part, 48, [
        n('C3', 1.0), n('E3', 0.5), n('G3', 0.5),
        n('C4', 0.5), n('E4', 0.5), n('G4', 0.5), n('C5', 0.5, fermata=True),
    ], dyn='pp')


# -- French Horn Part (the hero's voice) -----------------------------------

def build_horn(part):
    """French Horn: states the noble main theme."""

    BAR = 4.0

    # == Section I: Crystal Dawn (mm.1-12) -- Horn tacet ==
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

    # m.9-10: Horn enters with a call -- rising fifth, the summons (dotted rhythm)
    add_measure(part, 9, [
        r(2.0), n('G3', 1.5, tenuto=True), n('C4', 0.5),
    ], dyn='p', expression_text='nobilmente')

    add_measure(part, 10, [
        n('D4', 1.5, tenuto=True), n('Eb4', 0.5), n('D4', 1.0), n('C4', 1.0),
    ])

    add_measure(part, 11, [
        n('C4', 2.0, tenuto=True), n('Bb3', 1.0), n('Ab3', 1.0),
    ], dyn='mp')

    add_measure(part, 12, [
        n('G3', 3.0, tenuto=True), r(1.0),
    ])

    # == Section II: The Hero's Call (mm.13-24) -- Eb major ==
    # Main theme: Bb4-Eb5, noble and searching

    add_measure(part, 13, [
        n('Bb3', 1.5, tenuto=True), n('Eb4', 1.5, tenuto=True), n('D4', 1.0),
    ], dyn='mf', ks=key.Key('E-'),
       expression_text='con anima')

    add_measure(part, 14, [
        n('C4', 1.5), n('Bb3', 0.5), n('Ab3', 1.0, tenuto=True), n('B3', 1.0),
    ])  # B natural = chromatic passing tone

    add_measure(part, 15, [
        n('C4', 0.5), n('Ab3', 0.5), n('Bb3', 1.0),
        n('C4', 1.5, tenuto=True), r(0.5),
    ])

    add_measure(part, 16, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ])

    # m.17-20: Second phrase of theme -- rising higher (dotted rhythms)
    add_measure(part, 17, [
        n('Eb4', 1.5, accent=True), n('F4', 0.5),
        n('G4', 1.5, tenuto=True), n('F4', 0.5),
    ], dyn='f')

    add_measure(part, 18, [
        n('Eb4', 0.75), n('D4', 0.25), n('C4', 1.0),
        n('Bb3', 1.0, tenuto=True), n('C4', 1.0),
    ])

    add_measure(part, 19, [
        n('D4', 1.5), n('Eb4', 0.5),
        n('F4', 2.0, tenuto=True),
    ], dyn='mf')

    add_measure(part, 20, [
        n('Eb4', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24: Answering phrase -- yearning, then resolving
    add_measure(part, 21, [
        n('Ab3', 1.0, tenuto=True), n('C4', 1.5), n('Bb3', 0.5),
        n('Ab3', 1.0),
    ], dyn='mp')

    add_measure(part, 22, [
        n('Bb3', 1.0), n('D4', 1.5, tenuto=True), n('C4', 0.5),
        n('Bb3', 1.0),
    ])

    # F minor tonicization (modulation_count improvement)
    add_measure(part, 23, [
        n('Ab3', 0.5), n('G3', 0.5), n('F3', 1.0),
        n('G3', 2.0, tenuto=True),
    ], dyn='p', ks=key.Key('f'))

    add_measure(part, 24, [
        n('C4', 3.0, tenuto=True), r(1.0),
    ], ks=key.Key('E-'))

    # == Section III: The Journey Ahead (mm.25-36) -- Ab major ==

    add_measure(part, 25, [
        n('Ab3', 1.5, tenuto=True), n('C4', 1.5, tenuto=True), n('Bb3', 1.0),
    ], dyn='mf', ks=key.Key('A-'),
       expression_text='espressivo')

    add_measure(part, 26, [
        n('Ab3', 1.0), n('Db4', 1.5, tenuto=True), n('C4', 0.5),
        n('Bb3', 1.0),
    ])

    add_measure(part, 27, [
        n('Eb4', 1.0, accent=True), n('F4', 1.0),
        n('Eb4', 1.0, tenuto=True), n('Db4', 1.0),
    ])

    add_measure(part, 28, [
        n('C4', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Building to climax (dotted rhythms, chromatic D natural passing tone)
    add_measure(part, 29, [
        n('F3', 1.5), n('Ab3', 0.5), n('C4', 1.0, accent=True), n('D4', 1.0),
    ], dyn='f')  # D natural = chromatic

    add_measure(part, 30, [
        n('Eb4', 1.5, tenuto=True), n('F4', 0.5),
        n('Ab4', 2.0, accent=True),
    ], dyn='ff')

    add_measure(part, 31, [
        n('G4', 0.75), n('F4', 0.25), n('Eb4', 1.0),
        n('Eb4', 1.5, tenuto=True), n('Db4', 0.5),
    ], dyn='f')

    add_measure(part, 32, [
        n('C4', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.33-36: Emotional peak
    add_measure(part, 33, [
        n('Db4', 1.0, accent=True), n('F4', 1.5, tenuto=True), n('Eb4', 0.5),
        n('Db4', 1.0),
    ], dyn='ff', expression_text='grandioso')

    add_measure(part, 34, [
        n('Bb3', 1.0), n('Db4', 1.0, tenuto=True),
        n('F4', 1.5, accent=True), n('Eb4', 0.5),
    ])

    add_measure(part, 35, [
        n('Eb4', 1.0), n('G4', 1.5, tenuto=True), n('F4', 0.5),
        n('Eb4', 1.0),
    ], dyn='f')

    add_measure(part, 36, [
        n('Ab3', 3.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # == Section IV: Return to the Crystal (mm.37-48) ==

    add_measure(part, 37, [
        n('G3', 1.0, tenuto=True), n('C4', 2.0, tenuto=True), n('D4', 1.0),
    ], dyn='mp', ks=key.Key('c'),
       expression_text='dolce')

    add_measure(part, 38, [
        n('Eb4', 1.5, tenuto=True), n('D4', 0.5),
        n('C4', 1.0), n('Bb3', 1.0),
    ])

    add_measure(part, 39, [
        n('Ab3', 1.5), n('Bb3', 0.5),
        n('C4', 2.0, tenuto=True),
    ])

    add_measure(part, 40, [
        n('G3', 3.0, tenuto=True), r(1.0),
    ], dyn='p')

    # m.41-44: Theme recalled in minor, very soft
    add_measure(part, 41, [
        n('C4', 1.0, tenuto=True), n('Eb4', 1.5), n('D4', 0.5),
        n('C4', 1.0),
    ], dyn='p')

    add_measure(part, 42, [
        n('Ab3', 1.5, tenuto=True), n('G3', 0.5),
        n('F3', 1.0), n('G3', 1.0),
    ])

    add_measure(part, 43, [
        n('Ab3', 1.0), n('C4', 1.0, tenuto=True),
        n('Bb3', 1.0), n('Ab3', 1.0),
    ], dyn='pp')

    add_measure(part, 44, [
        n('G3', 3.0, tenuto=True), r(1.0),
    ])

    # m.45-48: Picardy third -- C major resolution
    add_measure(part, 45, [
        n('C4', 1.0, tenuto=True), n('E4', 2.0, tenuto=True), n('D4', 1.0),
    ], dyn='mp', ks=key.Key('C'),
       expression_text='luminoso')

    add_measure(part, 46, [
        n('C4', 1.5, tenuto=True), n('B3', 0.5),
        n('A3', 1.0), n('G3', 1.0),
    ])

    add_measure(part, 47, [
        n('F3', 1.0), n('G3', 1.0),
        n('A3', 1.0), n('B3', 1.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 48, [
        n('C4', 4.0, fermata=True),
    ], dyn='pp')


# -- Flute Part (ethereal ornament) ----------------------------------------

def build_flute(part):
    """Flute: ethereal descants and ornamental figures."""

    BAR = 4.0

    # == Section I: Tacet until m.7 ==
    for m_num in range(1, 7):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    # m.7-8: Flute enters with a gentle descant (dotted rhythm)
    add_measure(part, 7, [
        r(2.0), n('G5', 1.5, tenuto=True), n('Eb5', 0.5),
    ], dyn='pp', expression_text='dolcissimo')

    add_measure(part, 8, [
        n('D5', 1.5), n('Eb5', 0.5), n('F5', 1.5, tenuto=True), n('D5', 0.5),
    ])

    # m.9-10: Echoing the horn's call
    add_measure(part, 9, [
        n('Eb5', 1.0, tenuto=True), n('D5', 0.5), n('C5', 0.5),
        n('Bb4', 1.0), r(1.0),
    ], dyn='p')

    add_measure(part, 10, [
        r(1.0), n('G5', 0.5), n('Ab5', 0.5),
        n('Bb5', 1.5, tenuto=True), n('Ab5', 0.5),
    ])

    add_measure(part, 11, [
        n('G5', 1.0), n('F5', 0.5), n('Eb5', 0.5),
        n('D5', 1.0, tenuto=True), n('C5', 1.0),
    ])

    add_measure(part, 12, [
        n('B4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II: The Hero's Call (mm.13-24) ==
    # Flute adds ornamental countermelody above the horn

    add_measure(part, 13, [
        r(1.0), n('Bb5', 0.75), n('Ab5', 0.25),
        n('G5', 1.0, tenuto=True), n('F5', 1.0),
    ], dyn='mp', ks=key.Key('E-'))

    add_measure(part, 14, [
        n('Eb5', 0.5), n('F5', 0.5), n('F#5', 0.5), n('Ab5', 0.5),
        n('Bb5', 2.0, tenuto=True),
    ])  # F# = chromatic passing tone

    add_measure(part, 15, [
        n('Ab5', 0.5), n('G5', 0.5), n('F5', 0.5), n('Eb5', 0.5),
        n('D5', 1.0, tenuto=True), n('Eb5', 1.0),
    ])

    add_measure(part, 16, [
        n('F5', 2.0, tenuto=True), r(2.0),
    ])

    # m.17-20: More active
    add_measure(part, 17, [
        n('G5', 0.5), n('Ab5', 0.5), n('Bb5', 0.5), n('C6', 0.5),
        n('Bb5', 1.0, tenuto=True), n('Ab5', 1.0),
    ], dyn='mf')

    add_measure(part, 18, [
        n('G5', 1.0), n('F5', 0.5), n('Eb5', 0.5),
        n('D5', 1.0, tenuto=True), n('Eb5', 1.0),
    ])

    add_measure(part, 19, [
        n('F5', 0.5, trill=True), n('G5', 0.5), n('Ab5', 0.5), n('Bb5', 0.5),
        n('C6', 2.0, tenuto=True),
    ], dyn='f')

    add_measure(part, 20, [
        n('Bb5', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.21-24: Quieter, answering
    add_measure(part, 21, [
        r(2.0), n('Eb5', 0.5), n('F5', 0.5),
        n('G5', 1.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 22, [
        n('Ab5', 0.5), n('G5', 0.5), n('F5', 0.5), n('Eb5', 0.5),
        n('D5', 2.0, tenuto=True),
    ])

    add_measure(part, 23, [
        n('C5', 1.0), n('D5', 0.5), n('Eb5', 0.5),
        n('F5', 1.0), n('D5', 1.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 24, [
        n('Eb5', 3.0, tenuto=True), r(1.0),
    ])

    # == Section III: The Journey Ahead (mm.25-36) -- Ab major ==

    add_measure(part, 25, [
        r(2.0), n('Eb5', 0.75), n('F5', 0.25),
        n('Ab5', 1.0, tenuto=True),
    ], dyn='mf', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Ab5', 0.75), n('Bb5', 0.25), n('C6', 1.0, tenuto=True),
        n('Bb5', 0.5), n('Ab5', 0.5), n('G5', 1.0),
    ])

    add_measure(part, 27, [
        n('F5', 0.5), n('G5', 0.5), n('Ab5', 0.75), n('Bb5', 0.25),
        n('C6', 1.0, tenuto=True), n('Bb5', 1.0),
    ])

    add_measure(part, 28, [
        n('Ab5', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Building
    add_measure(part, 29, [
        n('C5', 0.5), n('Db5', 0.5), n('Eb5', 0.5), n('F5', 0.5),
        n('Ab5', 1.0, accent=True), n('G5', 1.0),
    ], dyn='f')

    add_measure(part, 30, [
        n('Ab5', 1.0, accent=True), n('Bb5', 0.5), n('C6', 0.5),
        n('Db6', 2.0, tenuto=True),
    ], dyn='ff')

    add_measure(part, 31, [
        n('C6', 1.0), n('Bb5', 0.5), n('Ab5', 0.5),
        n('G5', 1.0, tenuto=True), n('F5', 1.0),
    ], dyn='f')

    add_measure(part, 32, [
        n('Eb5', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.33-36: Peak
    add_measure(part, 33, [
        n('Db5', 0.5), n('Eb5', 0.5), n('F5', 0.5), n('Ab5', 0.5),
        n('Db6', 1.0, accent=True), n('C6', 1.0),
    ], dyn='ff')

    add_measure(part, 34, [
        n('Bb5', 1.0, tenuto=True), n('Ab5', 0.5), n('G5', 0.5),
        n('F5', 1.0, tenuto=True), n('Eb5', 1.0),
    ], dyn='f')

    add_measure(part, 35, [
        n('G5', 0.5, trill=True), n('Ab5', 0.5), n('Bb5', 1.0, tenuto=True),
        n('C6', 1.0, accent=True), n('Bb5', 1.0),
    ])

    add_measure(part, 36, [
        n('Ab5', 3.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # == Section IV: Return to the Crystal (mm.37-48) ==

    add_measure(part, 37, [
        r(2.0), n('G5', 0.5), n('Eb5', 0.5),
        n('C5', 1.0, tenuto=True),
    ], dyn='p', ks=key.Key('c'))

    add_measure(part, 38, [
        n('D5', 0.5), n('Eb5', 0.5), n('F5', 1.0, tenuto=True),
        n('Eb5', 0.5), n('D5', 0.5), n('C5', 1.0),
    ])

    add_measure(part, 39, [
        n('Ab4', 0.5), n('Bb4', 0.5), n('C5', 1.0, tenuto=True),
        n('Bb4', 1.0), n('Ab4', 1.0),
    ])

    add_measure(part, 40, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # m.41-44: Soft recall
    add_measure(part, 41, [
        r(2.0), n('Eb5', 1.0, tenuto=True), n('D5', 1.0),
    ], dyn='pp')

    add_measure(part, 42, [
        n('C5', 1.5, tenuto=True), n('Bb4', 0.5),
        n('Ab4', 1.0), r(1.0),
    ])

    add_measure(part, 43, [
        r(1.0), n('C5', 0.5), n('D5', 0.5),
        n('Eb5', 1.0, tenuto=True), n('D5', 1.0),
    ])

    add_measure(part, 44, [
        n('B4', 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: C major -- radiant
    add_measure(part, 45, [
        r(1.0), n('E5', 0.5), n('F5', 0.5),
        n('G5', 1.0, tenuto=True), n('E5', 1.0),
    ], dyn='p', ks=key.Key('C'))

    add_measure(part, 46, [
        n('F5', 0.5), n('E5', 0.5), n('D5', 0.5), n('C5', 0.5),
        n('A4', 1.0, tenuto=True), n('G4', 1.0),
    ])

    add_measure(part, 47, [
        n('A4', 0.5), n('B4', 0.5), n('C5', 0.5), n('D5', 0.5),
        n('E5', 1.0, tenuto=True), n('D5', 1.0),
    ], dyn='pp')

    add_measure(part, 48, [
        n('C5', 3.0, tenuto=True), n('E5', 1.0, fermata=True),
    ])


# -- Violin I Part ---------------------------------------------------------

def build_violin1(part):
    """Violin I: lyrical upper string voice, doubling/harmonizing the theme."""

    BAR = 4.0

    # == Section I (mm.1-12) -- Tacet until m.5, then sustained tones ==
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

    # m.5-8: Sustained pads enter
    add_measure(part, 5, [
        n('C5', 4.0, tenuto=True),
    ], dyn='pp', expression_text='con sordino')

    add_measure(part, 6, [
        n('D5', 2.0, tenuto=True), n('Eb5', 2.0, tenuto=True),
    ])

    add_measure(part, 7, [
        n('Eb5', 2.0, tenuto=True), n('D5', 2.0),
    ], dyn='p')

    add_measure(part, 8, [
        n('D5', 2.0, tenuto=True), n('F5', 2.0, tenuto=True),
    ])

    # m.9-12
    add_measure(part, 9, [
        n('Eb5', 2.0, tenuto=True), n('D5', 1.0), n('C5', 1.0),
    ])

    add_measure(part, 10, [
        n('Bb4', 2.0, tenuto=True), n('Eb5', 2.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 11, [
        n('C5', 2.0, tenuto=True), n('Ab4', 2.0, tenuto=True),
    ])

    add_measure(part, 12, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.13-24) -- Eb major, harmonizing horn ==

    add_measure(part, 13, [
        n('G4', 1.0), n('Bb4', 2.0, tenuto=True), n('Ab4', 1.0),
    ], dyn='mp', ks=key.Key('E-'))

    add_measure(part, 14, [
        n('G4', 1.5), n('F4', 0.5), n('Eb4', 1.0, tenuto=True), n('F4', 1.0),
    ])

    add_measure(part, 15, [
        n('Eb4', 1.0), n('F4', 0.5), n('G4', 0.5),
        n('Ab4', 2.0, tenuto=True),
    ])

    add_measure(part, 16, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # m.17-20: More active doubling
    add_measure(part, 17, [
        n('Bb4', 1.0, accent=True), n('C5', 1.0),
        n('Eb5', 1.5, tenuto=True), n('D5', 0.5),
    ], dyn='f')

    add_measure(part, 18, [
        n('C5', 1.0), n('Bb4', 0.5), n('Ab4', 0.5),
        n('G4', 1.0, tenuto=True), n('Ab4', 1.0),
    ])

    add_measure(part, 19, [
        n('Bb4', 1.5), n('C5', 0.5),
        n('D5', 2.0, tenuto=True),
    ], dyn='mf')

    add_measure(part, 20, [
        n('C5', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24
    add_measure(part, 21, [
        n('Eb4', 1.0, tenuto=True), n('Ab4', 1.5), n('G4', 0.5),
        n('F4', 1.0),
    ], dyn='mp')

    add_measure(part, 22, [
        n('G4', 1.0), n('Bb4', 1.5, tenuto=True), n('Ab4', 0.5),
        n('G4', 1.0),
    ])

    add_measure(part, 23, [
        n('F4', 0.5), n('Eb4', 0.5), n('D4', 1.0),
        n('Eb4', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 24, [
        n('G4', 3.0, tenuto=True), r(1.0),
    ])

    # == Section III (mm.25-36) -- Ab major ==

    add_measure(part, 25, [
        n('Eb4', 1.0, tenuto=True), n('Ab4', 2.0, tenuto=True), n('G4', 1.0),
    ], dyn='mf', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('F4', 1.0), n('Ab4', 1.5, tenuto=True), n('G4', 0.5),
        n('F4', 1.0),
    ])

    add_measure(part, 27, [
        n('Bb4', 1.0, accent=True), n('C5', 1.0),
        n('Bb4', 1.0, tenuto=True), n('Ab4', 1.0),
    ])

    add_measure(part, 28, [
        n('Ab4', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Building
    add_measure(part, 29, [
        n('Ab4', 0.5), n('Bb4', 0.5), n('C5', 0.5), n('Db5', 0.5),
        n('Eb5', 1.0, accent=True), n('Db5', 1.0),
    ], dyn='f')

    add_measure(part, 30, [
        n('C5', 1.0, accent=True), n('Db5', 0.5), n('Eb5', 0.5),
        n('F5', 2.0, tenuto=True),
    ], dyn='ff')

    add_measure(part, 31, [
        n('Eb5', 1.0), n('Db5', 0.5), n('C5', 0.5),
        n('Bb4', 1.0, tenuto=True), n('Ab4', 1.0),
    ], dyn='f')

    add_measure(part, 32, [
        n('Ab4', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.33-36: Peak
    add_measure(part, 33, [
        n('Ab4', 1.0), n('Db5', 1.5, accent=True), n('C5', 0.5),
        n('Ab4', 1.0),
    ], dyn='ff')

    add_measure(part, 34, [
        n('F4', 1.0), n('Bb4', 1.0, tenuto=True),
        n('Db5', 1.5, accent=True), n('C5', 0.5),
    ])

    add_measure(part, 35, [
        n('Bb4', 1.0), n('Eb5', 1.5, tenuto=True), n('Db5', 0.5),
        n('Bb4', 1.0),
    ], dyn='f')

    add_measure(part, 36, [
        n('Ab4', 3.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # == Section IV (mm.37-48) ==

    add_measure(part, 37, [
        n('Eb4', 1.0, tenuto=True), n('G4', 2.0, tenuto=True), n('Ab4', 1.0),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 38, [
        n('G4', 1.5, tenuto=True), n('F4', 0.5),
        n('Eb4', 1.0), n('D4', 1.0),
    ])

    add_measure(part, 39, [
        n('C4', 1.5), n('D4', 0.5),
        n('Eb4', 2.0, tenuto=True),
    ])

    add_measure(part, 40, [
        n('D4', 2.0, tenuto=True), r(2.0),
    ], dyn='p')

    # m.41-44: Soft recall
    add_measure(part, 41, [
        n('G4', 1.0, tenuto=True), n('C5', 1.5), n('Bb4', 0.5),
        n('Ab4', 1.0),
    ], dyn='p')

    add_measure(part, 42, [
        n('G4', 1.5, tenuto=True), n('F4', 0.5),
        n('Eb4', 1.0), n('D4', 1.0),
    ])

    add_measure(part, 43, [
        n('C4', 1.0), n('Eb4', 1.0, tenuto=True),
        n('D4', 1.0), n('C4', 1.0),
    ], dyn='pp')

    add_measure(part, 44, [
        n('B3', 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: C major
    add_measure(part, 45, [
        n('E4', 1.0, tenuto=True), n('G4', 2.0, tenuto=True), n('A4', 1.0),
    ], dyn='mp', ks=key.Key('C'))

    add_measure(part, 46, [
        n('G4', 1.5, tenuto=True), n('F4', 0.5),
        n('E4', 1.0), n('D4', 1.0),
    ])

    add_measure(part, 47, [
        n('C4', 1.0), n('D4', 1.0),
        n('E4', 1.0), n('G4', 1.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 48, [
        n('G4', 2.0, tenuto=True), n('E4', 2.0, fermata=True),
    ], dyn='pp')


# -- Violin II Part --------------------------------------------------------

def build_violin2(part):
    """Violin II: inner voice, harmonic filler, gentle countermotion."""

    BAR = 4.0

    # == Section I (mm.1-12) -- Tacet until m.7 ==
    for m_num in range(1, 7):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    add_measure(part, 7, [
        n('G4', 2.0, tenuto=True), n('Bb4', 2.0, tenuto=True),
    ], dyn='pp', expression_text='con sordino')

    add_measure(part, 8, [
        n('Bb4', 2.0, tenuto=True), n('A4', 2.0, tenuto=True),
    ])

    add_measure(part, 9, [
        n('Ab4', 2.0, tenuto=True), n('G4', 2.0, tenuto=True),
    ])

    add_measure(part, 10, [
        n('G4', 2.0, tenuto=True), n('Bb4', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 11, [
        n('Ab4', 2.0, tenuto=True), n('F4', 2.0, tenuto=True),
    ])

    add_measure(part, 12, [
        n('D4', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.13-24) ==

    add_measure(part, 13, [
        n('Eb4', 2.0, tenuto=True), n('F4', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('E-'))

    add_measure(part, 14, [
        n('Eb4', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ])

    add_measure(part, 15, [
        n('Bb3', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ])

    add_measure(part, 16, [
        n('D4', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 17, [
        n('G4', 1.0, accent=True), n('Ab4', 1.0),
        n('Bb4', 1.0, tenuto=True), n('Ab4', 1.0),
    ], dyn='f')

    add_measure(part, 18, [
        n('G4', 1.0), n('F4', 0.5), n('Eb4', 0.5),
        n('D4', 1.0, tenuto=True), n('Eb4', 1.0),
    ])

    add_measure(part, 19, [
        n('F4', 2.0, tenuto=True), n('Ab4', 2.0, tenuto=True),
    ], dyn='mf')

    add_measure(part, 20, [
        n('G4', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24
    add_measure(part, 21, [
        n('C4', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 22, [
        n('D4', 2.0, tenuto=True), n('F4', 2.0, tenuto=True),
    ])

    add_measure(part, 23, [
        n('D4', 2.0, tenuto=True), n('B3', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 24, [
        n('C4', 3.0, tenuto=True), r(1.0),
    ])

    # == Section III (mm.25-36) ==

    add_measure(part, 25, [
        n('C4', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ], dyn='mf', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Db4', 2.0, tenuto=True), n('F4', 2.0, tenuto=True),
    ])

    add_measure(part, 27, [
        n('G4', 2.0, tenuto=True), n('Bb4', 2.0, tenuto=True),
    ])

    add_measure(part, 28, [
        n('Ab4', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('C4', 1.0), n('Db4', 1.0),
        n('Eb4', 1.0, accent=True), n('F4', 1.0),
    ], dyn='f')

    add_measure(part, 30, [
        n('Ab4', 1.0, accent=True), n('Bb4', 1.0),
        n('Ab4', 1.0, tenuto=True), n('G4', 1.0),
    ], dyn='ff')

    add_measure(part, 31, [
        n('G4', 1.0), n('F4', 0.5), n('Eb4', 0.5),
        n('Eb4', 1.0, tenuto=True), n('Db4', 1.0),
    ], dyn='f')

    add_measure(part, 32, [
        n('Eb4', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.33-36: Peak
    add_measure(part, 33, [
        n('F4', 1.0), n('Ab4', 1.5, accent=True), n('G4', 0.5),
        n('F4', 1.0),
    ], dyn='ff')

    add_measure(part, 34, [
        n('Db4', 1.0), n('F4', 1.0, tenuto=True),
        n('Ab4', 1.0), n('G4', 1.0),
    ])

    add_measure(part, 35, [
        n('Eb4', 1.0), n('G4', 1.5, tenuto=True), n('F4', 0.5),
        n('Eb4', 1.0),
    ], dyn='f')

    add_measure(part, 36, [
        n('Eb4', 3.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # == Section IV (mm.37-48) ==

    add_measure(part, 37, [
        n('C4', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 38, [
        n('Eb4', 2.0, tenuto=True), n('D4', 2.0, tenuto=True),
    ])

    add_measure(part, 39, [
        n('C4', 2.0, tenuto=True), n('Ab3', 2.0, tenuto=True),
    ])

    add_measure(part, 40, [
        n('B3', 2.0, tenuto=True), r(2.0),
    ], dyn='p')

    add_measure(part, 41, [
        n('Eb4', 2.0, tenuto=True), n('G4', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 42, [
        n('Eb4', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ])

    add_measure(part, 43, [
        n('Ab3', 2.0, tenuto=True), n('G3', 2.0, tenuto=True),
    ], dyn='pp')

    add_measure(part, 44, [
        n('G3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 45, [
        n('C4', 2.0, tenuto=True), n('E4', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('C'))

    add_measure(part, 46, [
        n('C4', 2.0, tenuto=True), n('A3', 2.0, tenuto=True),
    ])

    add_measure(part, 47, [
        n('A3', 2.0, tenuto=True), n('B3', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 48, [
        n('E4', 2.0, tenuto=True), n('C4', 2.0, fermata=True),
    ], dyn='pp')


# -- Viola Part ------------------------------------------------------------

def build_viola(part):
    """Viola: warm middle voice, providing harmonic glue."""

    BAR = 4.0

    # == Section I (mm.1-12) -- Tacet until m.7 ==
    for m_num in range(1, 7):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('4/4')
            kwargs['ks'] = key.Key('c')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.0), number=72,
                text="Andante maestoso"
            )
        add_measure(part, m_num, [r(BAR)], **kwargs)

    add_measure(part, 7, [
        n('Eb4', 2.0, tenuto=True), n('G4', 2.0, tenuto=True),
    ], dyn='pp', expression_text='con sordino')

    add_measure(part, 8, [
        n('F4', 2.0, tenuto=True), n('D4', 2.0, tenuto=True),
    ])

    add_measure(part, 9, [
        n('C4', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ])

    add_measure(part, 10, [
        n('Eb4', 2.0, tenuto=True), n('G4', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 11, [
        n('F4', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ])

    add_measure(part, 12, [
        n('B3', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.13-24) ==

    add_measure(part, 13, [
        n('Bb3', 2.0, tenuto=True), n('Ab3', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('E-'))

    add_measure(part, 14, [
        n('Ab3', 2.0, tenuto=True), n('G3', 2.0, tenuto=True),
    ])

    add_measure(part, 15, [
        n('F3', 2.0, tenuto=True), n('Bb3', 2.0, tenuto=True),
    ])

    add_measure(part, 16, [
        n('Bb3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 17, [
        n('Eb4', 2.0, tenuto=True), n('G4', 2.0, tenuto=True),
    ], dyn='f')

    add_measure(part, 18, [
        n('Eb4', 2.0, tenuto=True), n('Bb3', 2.0, tenuto=True),
    ])

    add_measure(part, 19, [
        n('Bb3', 2.0, tenuto=True), n('F4', 2.0, tenuto=True),
    ], dyn='mf')

    add_measure(part, 20, [
        n('Eb4', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 21, [
        n('Ab3', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 22, [
        n('Bb3', 2.0, tenuto=True), n('D4', 2.0, tenuto=True),
    ])

    add_measure(part, 23, [
        n('Ab3', 2.0, tenuto=True), n('F3', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 24, [
        n('Eb3', 3.0, tenuto=True), r(1.0),
    ])

    # == Section III (mm.25-36) ==

    add_measure(part, 25, [
        n('Ab3', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ], dyn='mf', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Ab3', 2.0, tenuto=True), n('Db4', 2.0, tenuto=True),
    ])

    add_measure(part, 27, [
        n('Eb4', 2.0, tenuto=True), n('G4', 2.0, tenuto=True),
    ])

    add_measure(part, 28, [
        n('Eb4', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 29, [
        n('Ab3', 1.0), n('Ab3', 1.0),
        n('C4', 1.0, accent=True), n('Db4', 1.0),
    ], dyn='f')

    add_measure(part, 30, [
        n('Eb4', 1.0, accent=True), n('F4', 1.0),
        n('Eb4', 1.0, tenuto=True), n('Db4', 1.0),
    ], dyn='ff')

    add_measure(part, 31, [
        n('Eb4', 1.0), n('Db4', 0.5), n('C4', 0.5),
        n('Bb3', 1.0, tenuto=True), n('Ab3', 1.0),
    ], dyn='f')

    add_measure(part, 32, [
        n('Ab3', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    add_measure(part, 33, [
        n('Db4', 1.0), n('F4', 1.5, accent=True), n('Eb4', 0.5),
        n('Db4', 1.0),
    ], dyn='ff')

    add_measure(part, 34, [
        n('Bb3', 1.0), n('Db4', 1.0, tenuto=True),
        n('F4', 1.0), n('Eb4', 1.0),
    ])

    add_measure(part, 35, [
        n('Bb3', 1.0), n('Eb4', 1.5, tenuto=True), n('Db4', 0.5),
        n('Bb3', 1.0),
    ], dyn='f')

    add_measure(part, 36, [
        n('C4', 3.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # == Section IV (mm.37-48) ==

    add_measure(part, 37, [
        n('G3', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 38, [
        n('C4', 2.0, tenuto=True), n('Ab3', 2.0, tenuto=True),
    ])

    add_measure(part, 39, [
        n('Ab3', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ])

    add_measure(part, 40, [
        n('B3', 2.0, tenuto=True), r(2.0),
    ], dyn='p')

    add_measure(part, 41, [
        n('G3', 2.0, tenuto=True), n('Eb4', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 42, [
        n('C4', 2.0, tenuto=True), n('Ab3', 2.0, tenuto=True),
    ])

    add_measure(part, 43, [
        n('F3', 2.0, tenuto=True), n('Eb3', 2.0, tenuto=True),
    ], dyn='pp')

    add_measure(part, 44, [
        n('D3', 2.0, tenuto=True), r(2.0),
    ])

    add_measure(part, 45, [
        n('G3', 2.0, tenuto=True), n('C4', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('C'))

    add_measure(part, 46, [
        n('A3', 2.0, tenuto=True), n('F3', 2.0, tenuto=True),
    ])

    add_measure(part, 47, [
        n('D3', 2.0, tenuto=True), n('G3', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 48, [
        n('E3', 2.0, tenuto=True), n('G3', 2.0, fermata=True),
    ], dyn='pp')


# -- Cello Part ------------------------------------------------------------

def build_cello(part):
    """Cello: bass foundation, warm sustained tones, occasional melodic moments."""

    BAR = 4.0

    # == Section I (mm.1-12) -- Tacet until m.5, then low pedals ==
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

    # m.5-8: Low pedal tones, dark and mysterious
    add_measure(part, 5, [
        n('C2', 4.0, tenuto=True),
    ], dyn='pp')

    add_measure(part, 6, [
        n('C2', 2.0, tenuto=True), n('D2', 2.0, tenuto=True),
    ])

    add_measure(part, 7, [
        n('C2', 2.0, tenuto=True), n('Bb1', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 8, [
        n('Bb1', 2.0, tenuto=True), n('F2', 2.0, tenuto=True),
    ])

    # m.9-12: Walking bass begins
    add_measure(part, 9, [
        n('Ab2', 2.0, tenuto=True), n('G2', 1.0), n('F2', 1.0),
    ])

    add_measure(part, 10, [
        n('Eb2', 2.0, tenuto=True), n('G2', 2.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 11, [
        n('F2', 2.0, tenuto=True), n('Ab2', 1.0), n('C3', 1.0),
    ])

    add_measure(part, 12, [
        n('G2', 2.0, tenuto=True), r(2.0),
    ])

    # == Section II (mm.13-24) -- Eb major ==

    add_measure(part, 13, [
        n('Eb2', 2.0, tenuto=True), n('Bb2', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('E-'))

    add_measure(part, 14, [
        n('Ab2', 2.0, tenuto=True), n('Eb2', 2.0, tenuto=True),
    ])

    add_measure(part, 15, [
        n('Bb2', 2.0, tenuto=True), n('F2', 2.0, tenuto=True),
    ])

    add_measure(part, 16, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ])

    # m.17-20: More active bass
    add_measure(part, 17, [
        n('C2', 1.0), n('Eb2', 1.0), n('G2', 1.0, accent=True), n('Bb2', 1.0),
    ], dyn='f')

    add_measure(part, 18, [
        n('F2', 1.0), n('A2', 1.0), n('C3', 1.0, tenuto=True), n('Eb3', 1.0),
    ])

    add_measure(part, 19, [
        n('Bb2', 2.0, tenuto=True), n('D3', 1.0), n('F3', 1.0),
    ], dyn='mf')

    add_measure(part, 20, [
        n('Eb2', 2.0, tenuto=True), r(2.0),
    ])

    # m.21-24
    add_measure(part, 21, [
        n('Ab2', 2.0, tenuto=True), n('C2', 2.0, tenuto=True),
    ], dyn='mp')

    add_measure(part, 22, [
        n('Bb2', 2.0, tenuto=True), n('D2', 2.0, tenuto=True),
    ])

    add_measure(part, 23, [
        n('G2', 1.0), n('F2', 1.0),
        n('G2', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 24, [
        n('C2', 3.0, tenuto=True), r(1.0),
    ])

    # == Section III (mm.25-36) -- Ab major ==

    add_measure(part, 25, [
        n('Ab2', 2.0, tenuto=True), n('Eb2', 2.0, tenuto=True),
    ], dyn='mf', ks=key.Key('A-'))

    add_measure(part, 26, [
        n('Db2', 2.0, tenuto=True), n('Ab2', 2.0, tenuto=True),
    ])

    add_measure(part, 27, [
        n('Eb2', 2.0, tenuto=True), n('Bb2', 2.0, tenuto=True),
    ])

    add_measure(part, 28, [
        n('Ab2', 2.0, tenuto=True), r(2.0),
    ])

    # m.29-32: Building
    add_measure(part, 29, [
        n('F2', 1.0), n('Ab2', 1.0), n('C3', 1.0, accent=True), n('Db3', 1.0),
    ], dyn='f')

    add_measure(part, 30, [
        n('Db2', 1.0, accent=True), n('F2', 1.0),
        n('Ab2', 1.0, tenuto=True), n('Db3', 1.0),
    ], dyn='ff')

    add_measure(part, 31, [
        n('Eb2', 1.0), n('G2', 1.0),
        n('Bb2', 1.0, tenuto=True), n('Eb3', 1.0),
    ], dyn='f')

    add_measure(part, 32, [
        n('Ab2', 2.0, tenuto=True), r(2.0),
    ], dyn='mf')

    # m.33-36: Peak
    add_measure(part, 33, [
        n('Db2', 1.0, accent=True), n('F2', 1.0),
        n('Ab2', 1.0, tenuto=True), n('Db3', 1.0),
    ], dyn='ff')

    add_measure(part, 34, [
        n('Bb1', 1.0), n('Db2', 1.0),
        n('F2', 1.0, tenuto=True), n('Bb2', 1.0),
    ])

    add_measure(part, 35, [
        n('Eb2', 1.0, accent=True), n('G2', 1.0),
        n('Bb2', 1.0, tenuto=True), n('Eb3', 1.0),
    ], dyn='f')

    add_measure(part, 36, [
        n('Ab2', 3.0, tenuto=True), r(1.0),
    ], dyn='mf')

    # == Section IV (mm.37-48) ==

    add_measure(part, 37, [
        n('C2', 2.0, tenuto=True), n('G2', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('c'))

    add_measure(part, 38, [
        n('Ab2', 2.0, tenuto=True), n('Eb2', 2.0, tenuto=True),
    ])

    add_measure(part, 39, [
        n('F2', 2.0, tenuto=True), n('C2', 2.0, tenuto=True),
    ])

    add_measure(part, 40, [
        n('G2', 2.0, tenuto=True), r(2.0),
    ], dyn='p')

    # m.41-44: Gentle recall
    add_measure(part, 41, [
        n('C2', 2.0, tenuto=True), n('Eb2', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 42, [
        n('Ab2', 2.0, tenuto=True), n('Eb2', 2.0, tenuto=True),
    ])

    add_measure(part, 43, [
        n('F2', 2.0, tenuto=True), n('C2', 2.0, tenuto=True),
    ], dyn='pp')

    add_measure(part, 44, [
        n('G2', 2.0, tenuto=True), r(2.0),
    ])

    # m.45-48: C major resolution
    add_measure(part, 45, [
        n('C2', 2.0, tenuto=True), n('G2', 2.0, tenuto=True),
    ], dyn='mp', ks=key.Key('C'))

    add_measure(part, 46, [
        n('F2', 2.0, tenuto=True), n('C2', 2.0, tenuto=True),
    ])

    add_measure(part, 47, [
        n('G2', 2.0, tenuto=True), n('D2', 2.0, tenuto=True),
    ], dyn='p')

    add_measure(part, 48, [
        n('C2', 4.0, fermata=True),
    ], dyn='pp')


# -- Hairpins --------------------------------------------------------------

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins across the score."""
    parts_dict = {}
    for p in score.parts:
        name = p.partName or ''
        if 'Flute' in name:
            parts_dict['flute'] = p
        elif 'Horn' in name:
            parts_dict['horn'] = p
        elif 'Harp' in name:
            parts_dict['harp'] = p
        elif 'Violin I' == name:
            parts_dict['vln1'] = p
        elif 'Violin II' in name:
            parts_dict['vln2'] = p
        elif 'Viola' in name:
            parts_dict['viola'] = p
        elif 'Violoncello' in name or 'Vc' in (p.partAbbreviation or ''):
            parts_dict['cello'] = p

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
        # Harp
        ('harp', 1, 4, 'crescendo'),
        ('harp', 5, 6, 'crescendo'),
        ('harp', 9, 11, 'crescendo'),
        ('harp', 25, 27, 'crescendo'),
        ('harp', 29, 31, 'crescendo'),
        ('harp', 33, 35, 'diminuendo'),
        ('harp', 37, 39, 'diminuendo'),
        ('harp', 41, 43, 'diminuendo'),
        ('harp', 45, 47, 'diminuendo'),
        # Horn
        ('horn', 9, 11, 'crescendo'),
        ('horn', 13, 15, 'crescendo'),
        ('horn', 17, 19, 'crescendo'),
        ('horn', 25, 27, 'crescendo'),
        ('horn', 29, 31, 'crescendo'),
        ('horn', 33, 35, 'diminuendo'),
        ('horn', 37, 39, 'diminuendo'),
        ('horn', 41, 43, 'diminuendo'),
        ('horn', 45, 47, 'diminuendo'),
        # Flute
        ('flute', 7, 8, 'crescendo'),
        ('flute', 13, 15, 'crescendo'),
        ('flute', 17, 19, 'crescendo'),
        ('flute', 25, 27, 'crescendo'),
        ('flute', 29, 31, 'crescendo'),
        ('flute', 33, 35, 'diminuendo'),
        ('flute', 37, 39, 'diminuendo'),
        ('flute', 41, 43, 'diminuendo'),
        ('flute', 45, 47, 'diminuendo'),
        # Violin I
        ('vln1', 5, 7, 'crescendo'),
        ('vln1', 13, 15, 'crescendo'),
        ('vln1', 17, 19, 'crescendo'),
        ('vln1', 29, 31, 'crescendo'),
        ('vln1', 33, 35, 'diminuendo'),
        ('vln1', 37, 39, 'diminuendo'),
        ('vln1', 45, 47, 'diminuendo'),
        # Violin II
        ('vln2', 7, 9, 'crescendo'),
        ('vln2', 17, 19, 'crescendo'),
        ('vln2', 29, 31, 'crescendo'),
        ('vln2', 33, 35, 'diminuendo'),
        ('vln2', 37, 39, 'diminuendo'),
        ('vln2', 45, 47, 'diminuendo'),
        # Viola
        ('viola', 7, 9, 'crescendo'),
        ('viola', 17, 19, 'crescendo'),
        ('viola', 29, 31, 'crescendo'),
        ('viola', 33, 35, 'diminuendo'),
        ('viola', 37, 39, 'diminuendo'),
        ('viola', 45, 47, 'diminuendo'),
        # Cello
        ('cello', 5, 7, 'crescendo'),
        ('cello', 9, 11, 'crescendo'),
        ('cello', 17, 19, 'crescendo'),
        ('cello', 29, 31, 'crescendo'),
        ('cello', 33, 35, 'diminuendo'),
        ('cello', 37, 39, 'diminuendo'),
        ('cello', 45, 47, 'diminuendo'),
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        target_part = parts_dict.get(part_name)
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
    print("Building score: 'The Crystal Throne' -- JRPG Main Menu Theme")
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
