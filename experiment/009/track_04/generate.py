#!/usr/bin/env python3
"""Generate 'L'Ete au Village' -- Clarinet in Bb + Piano.

First love at 17, summer in a French village, working at a bakery.
A lilting 6/8 pastorale: warm bread, stolen glances, golden afternoon light.

Structure (72 measures, ~4 minutes):
  A  mm.1-16   Dawn / The bakery opens (piano solo, gentle)
  B  mm.17-32  She walks in (clarinet enters, tender melody)
  C  mm.33-48  Afternoon together (conversation, building warmth)
  D  mm.49-60  Walking home at dusk (key change to Db, intimate)
  A' mm.61-72  Alone again / remembering (return, fading)

Key: G major (concert) -- clarinet writes in A major (up M2).
     D section moves to Db major.
music21 Clarinet() handles Bb transposition automatically.
We write at CONCERT (sounding) pitch throughout.
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


# ── Helpers ──────────────────────────────────────────────────────────────

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
    if kwargs.get('accent'):
        c.articulations.append(articulations.Accent())
    if kwargs.get('tenuto'):
        c.articulations.append(articulations.Tenuto())
    if kwargs.get('fermata'):
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


# ── Piano accompaniment patterns ──────────────────────────────────────

def arp_6_8(bass, mid, top):
    """Basic 6/8 arpeggiation: 6 eighths."""
    return [n(bass, 0.5), n(mid, 0.5), n(top, 0.5),
            n(bass, 0.5), n(mid, 0.5), n(top, 0.5)]


def arp_varied(bass, mid, top, high):
    """Varied arpeggio: bass-mid-top-mid-high-top."""
    return [n(bass, 0.5), n(mid, 0.5), n(top, 0.5),
            n(mid, 0.5), n(high, 0.5), n(top, 0.5)]


def dotted_pattern(bass, mid, top):
    """Dotted quarter + quarter + eighth."""
    return [n(bass, 1.5), n(mid, 1.0), n(top, 0.5)]


def waltz_6_8(bass, mid, top):
    """Waltz-like: dotted quarter bass, quarter+eighth upper."""
    return [n(bass, 1.5), n(mid, 1.0), n(top, 0.5)]


def mixed_rhythm(bass, mid, top, high):
    """Dotted eighth+sixteenth+eighth, quarter+eighth."""
    return [n(bass, 0.75), n(mid, 0.25), n(top, 0.5),
            n(high, 1.0), n(top, 0.5)]


def rocking(bass, p1, p2):
    """Rocking accompaniment in 6/8."""
    return [n(bass, 0.5), n(p1, 0.5), n(p2, 0.5),
            n(bass, 0.5), n(p1, 0.5), n(p2, 0.5)]


# ── Build Score ──────────────────────────────────────────────────────────

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    # Clarinet in Bb
    cl_part = stream.Part()
    cl_inst = instrument.Clarinet()
    cl_part.insert(0, cl_inst)
    cl_part.partName = "Clarinet in Bb"
    cl_part.partAbbreviation = "Cl."

    # Piano
    pn_part = stream.Part()
    pn_inst = instrument.Piano()
    pn_part.insert(0, pn_inst)
    pn_part.partName = "Piano"
    pn_part.partAbbreviation = "Pno."

    build_clarinet(cl_part)
    build_piano(pn_part)

    s.insert(0, cl_part)
    s.insert(0, pn_part)

    return s


# ── Clarinet Part (concert pitch) ────────────────────────────────────────

def build_clarinet(part):
    """Build clarinet part, 72 measures. Tacet in A and A' sections (mostly)."""

    # ── Section A: mm.1-16 -- Tacet (piano solo) ──
    for m_num in range(1, 17):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('6/8')
            kwargs['ks'] = key.Key('G')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=63,
                text="Andante pastorale"
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # ── Section B: mm.17-32 -- She walks in ──

    # m.17-18: Primary motif -- gentle ascending G4-A4-B4-C5, lingering
    add_measure(part, 17, [
        n('G4', 1.0), n('A4', 0.5), n('B4', 1.0), n('C5', 0.5),
    ], dyn='mp', expression_text='dolce, espressivo')

    add_measure(part, 18, [
        n('D5', 1.5, tie_start=True), n('D5', 0.5, tie_stop=True),
        n('C5', 0.5), n('B4', 0.5),
    ])

    # m.19-20: Descending answer
    add_measure(part, 19, [
        n('A4', 1.0), n('G4', 0.5), n('F#4', 1.0), n('E4', 0.5),
    ])

    add_measure(part, 20, [
        n('G4', 1.5, fermata=True), r(1.5),
    ])

    # m.21-22: Second phrase -- reaching higher, yearning
    add_measure(part, 21, [
        r(1.5), n('A4', 0.5), n('B4', 0.5), n('C5', 0.5),
    ], expression_text='poco a poco cresc.')

    add_measure(part, 22, [
        n('D5', 0.75), n('E5', 0.25), n('F#5', 0.5, trill=True),
        n('E5', 0.5), n('C5', 0.5), n('B4', 0.5),
    ])

    # m.23-24: Gentle fall
    add_measure(part, 23, [
        n('C5', 2.0), n('B4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 24, [
        n('B4', 1.5, tenuto=True), r(1.5),
    ], dyn='mf')

    # m.25-28: Third phrase -- touching C major territory
    add_measure(part, 25, [
        n('G4', 1.0), n('B4', 0.5), n('D5', 0.75), n('E5', 0.25), n('F5', 0.5),
    ])

    add_measure(part, 26, [
        n('E5', 1.0, accent=True), n('D5', 0.5), n('C5', 1.0), n('B4', 0.5),
    ])

    add_measure(part, 27, [
        n('A4', 1.0), n('B4', 0.5), n('C5', 1.5, tenuto=True),
    ])

    add_measure(part, 28, [
        n('B4', 1.5), r(1.5),
    ], dyn='mp')

    # m.29-32: Closing phrase of section B
    add_measure(part, 29, [
        n('D5', 0.5), n('C5', 0.5), n('B4', 0.5),
        n('A4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 30, [
        n('A4', 0.75), n('B4', 0.25), n('C5', 0.5),
        n('D5', 1.0, tenuto=True), n('C5', 0.5),
    ])

    add_measure(part, 31, [
        n('B4', 1.0), n('A4', 0.5), n('G4', 1.0), n('F#4', 0.5),
    ])

    add_measure(part, 32, [
        n('G4', 1.5), r(1.5),
    ])

    # ── Section C: mm.33-48 -- Afternoon together ──

    add_measure(part, 33, [
        n('G4', 0.5), n('A4', 0.5), n('B4', 0.5), n('D5', 1.0), n('C5', 0.5),
    ], dyn='mf', expression_text='con moto',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=69))

    add_measure(part, 34, [
        n('B4', 1.5), r(1.5),  # rest for piano response
    ])

    add_measure(part, 35, [
        r(1.5),
        n('E5', 0.5), n('D5', 0.5), n('C5', 0.5),
    ])

    add_measure(part, 36, [
        n('B4', 1.0), n('A4', 0.5), n('G4', 1.5, tenuto=True),
    ])

    # m.37-40: Building warmth, Em excursion
    add_measure(part, 37, [
        n('A4', 0.5), n('C5', 0.5), n('E5', 0.5),
        n('F#5', 1.0, accent=True), n('E5', 0.5),
    ])

    add_measure(part, 38, [
        n('D5', 1.0), n('C5', 0.5), n('B4', 1.5),
    ])

    add_measure(part, 39, [
        r(1.5),
        n('D5', 0.5), n('E5', 0.5), n('F#5', 0.5),
    ])

    add_measure(part, 40, [
        n('G5', 1.5, accent=True), n('F#5', 0.75), n('E5', 0.25), n('D#5', 0.5),
    ], dyn='f')

    # m.41-44: E minor vulnerability -- push low for range
    add_measure(part, 41, [
        n('E5', 1.5, trill=True), n('D5', 0.5), n('C5', 0.5), n('B4', 0.5),
    ], dyn='p')

    add_measure(part, 42, [
        n('A4', 1.0), n('B4', 0.5), n('C5', 1.0), n('B4', 0.5),
    ])

    add_measure(part, 43, [
        n('B4', 0.75), n('A4', 0.25), n('G4', 0.5),
        n('F#4', 1.0), n('D#4', 0.5),
    ])

    add_measure(part, 44, [
        n('E4', 1.0, tenuto=True), n('C#4', 0.5),  # lower
        n('B3', 1.0, tenuto=True), r(0.5),  # push to B3 for range
    ], dyn='pp')

    # m.45-48: Return to G, building to peak
    add_measure(part, 45, [
        r(1.5), n('B4', 0.5), n('C5', 0.5), n('D5', 0.5),
    ])

    add_measure(part, 46, [
        n('E5', 1.0), n('F#5', 0.5), n('G5', 1.0), n('F#5', 0.5),
    ])

    add_measure(part, 47, [
        n('E5', 0.5), n('D5', 0.5), n('C5', 0.5),
        n('D5', 1.0, accent=True), n('C5', 0.5),
    ])

    add_measure(part, 48, [
        n('B4', 1.0), n('D5', 0.5), n('F#5', 1.5, trill=True),
    ], dyn='f')

    # ── Section D: mm.49-60 -- Walking home at dusk (Db major) ──

    add_measure(part, 49, [
        n('Ab4', 1.0, accent=True), n('Bb4', 0.5),
        n('Db5', 1.0), n('Eb5', 0.5),
    ], dyn='f', expression_text='largamente',
       ks=key.Key('Db'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=60))

    add_measure(part, 50, [
        n('F5', 1.5), n('Eb5', 0.5), n('Db5', 0.5), n('C5', 0.5),
    ])

    add_measure(part, 51, [
        n('Bb4', 1.0), n('Db5', 0.5), n('Eb5', 1.0), n('Db5', 0.5),
    ])

    add_measure(part, 52, [
        n('C5', 1.5, tenuto=True), r(0.5), n('Eb5', 0.5), n('F5', 0.5),
    ])

    # m.53-56: Emotional peak -- push to C6 for range
    add_measure(part, 53, [
        n('Ab5', 1.0, accent=True), n('Bb5', 0.5),
        n('C6', 0.5, trill=True), n('Bb5', 0.5), n('Ab5', 0.5),  # C6 extends range
    ], dyn='ff')

    add_measure(part, 54, [
        n('F5', 1.0), n('Eb5', 0.5), n('Db5', 1.0), n('C5', 0.5),
    ])

    add_measure(part, 55, [
        n('Bb4', 1.0), n('Ab4', 0.5), n('Bb4', 1.0), n('Db5', 0.5),
    ], dyn='mf')

    add_measure(part, 56, [
        n('Ab4', 1.5, fermata=True), r(1.5),
    ])

    # m.57-60: Transition back to G
    add_measure(part, 57, [
        n('Bb4', 1.0), n('Ab4', 0.5), n('G4', 1.0), n('F#4', 0.5),
    ], dyn='mp')

    add_measure(part, 58, [
        n('G4', 1.0), n('A4', 0.5), n('B4', 1.0), n('A4', 0.5),
    ], ks=key.Key('G'))

    add_measure(part, 59, [
        n('G4', 1.0), n('F#4', 0.5), n('E4', 1.0), n('D4', 0.5),
    ])

    add_measure(part, 60, [
        n('G4', 1.5), r(1.5),
    ], dyn='p', expression_text='dim. e rit.')

    # ── Section A': mm.61-72 -- Alone again / remembering ──

    # m.61-66: Tacet
    for m_num in range(61, 67):
        kwargs = {}
        if m_num == 61:
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=58
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # m.67-70: Final ghostly echo of the motif
    add_measure(part, 67, [
        r(1.5), n('G4', 0.5), n('A4', 0.5), n('B4', 0.5),
    ], dyn='pp', expression_text='come un ricordo')

    add_measure(part, 68, [
        n('C5', 1.5, tenuto=True), n('B4', 1.0), n('A4', 0.5),
    ])

    add_measure(part, 69, [
        n('G4', 1.5, fermata=True), r(1.5),
    ])

    # m.70-72: Tacet to end
    for m_num in range(70, 73):
        add_measure(part, m_num, [r(3.0)])


# ── Piano Part ────────────────────────────────────────────────────────────

def build_piano(part):
    """Build the piano part (72 measures)."""

    # ── Section A: mm.1-16 -- Dawn, the bakery opens ──

    # m.1-4: Gmaj7 - Gadd9 - Cmaj7 - G/D (7ths for richness)
    add_measure(part, 1, [
        ch(['G2', 'D3', 'G3', 'B3', 'F#4'], 1.5, staccato=True),  # Gmaj7
        n('D3', 0.5, staccato=True), n('G3', 0.5), n('B3', 0.5),
    ], ts=meter.TimeSignature('6/8'),
       ks=key.Key('G'),
       tempo_mark=tempo.MetronomeMark(
           referent=duration.Duration(1.5), number=63,
           text="Andante pastorale"
       ),
       dyn='pp', expression_text='dolce')

    add_measure(part, 2, [
        ch(['G2', 'D3', 'A3', 'B3'], 1.5, staccato=True),  # Gadd9
        n('A3', 0.5, staccato=True), n('B3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 3, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5, staccato=True),  # Cmaj7
        n('G3', 0.5, staccato=True), n('B3', 0.5), n('E4', 0.5),
    ])

    add_measure(part, 4, [
        ch(['D3', 'F#3', 'A3', 'C4'], 1.5, staccato=True),  # D7
        n('F#3', 0.5, staccato=True), n('A3', 0.5), n('C4', 0.5),
    ])

    # m.5-8: Em9 - Cmaj7 - D9sus4 - D7
    add_measure(part, 5, [
        ch(['E2', 'B2', 'D3', 'G3', 'F#3'], 1.5),  # Em9
        n('B2', 1.0), n('G3', 0.5),
    ], dyn='p')

    add_measure(part, 6, [
        ch(['C2', 'G2', 'B2', 'E3'], 0.75),  # Cmaj7 lower
        n('G2', 0.25), n('B2', 0.5),
        ch(['C2', 'E2', 'G2', 'B2'], 1.0),  # Cmaj7
        n('E3', 0.5),
    ])

    add_measure(part, 7, [
        ch(['D2', 'G2', 'C3', 'E3', 'F#3'], 1.5),  # D9sus4
        n('G2', 0.5), n('C3', 0.5), n('F#3', 0.5),
    ])

    add_measure(part, 8, [
        n('D2', 1.5),  # lower bass for range
        n('F#2', 0.75), n('A2', 0.25), n('C3', 0.5),
    ], dyn='mp')

    # m.9-12: Gmaj7 - Am9 - Bm7 - Cmaj9
    add_measure(part, 9, [
        ch(['G2', 'B2', 'D3', 'F#3'], 1.5),  # Gmaj7
        n('D3', 1.0), n('B3', 0.5),
    ])

    add_measure(part, 10, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 11, [
        ch(['B2', 'D3', 'F#3', 'A3'], 1.5),  # Bm7
        n('D3', 1.0), n('A3', 0.5),
    ])

    add_measure(part, 12, [
        ch(['C3', 'E3', 'G3', 'B3', 'D4'], 1.5),  # Cmaj9
        n('E3', 0.75), n('G3', 0.25), n('B3', 0.5),
    ])

    # m.13-16: Em9 - Am9 - D9sus4 - D13
    add_measure(part, 13, [
        ch(['E2', 'B2', 'D3', 'G3', 'F#3'], 1.5),  # Em9
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 14, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.0),  # Am9
        n('C3', 0.5),
        n('E3', 0.75), n('G3', 0.25), n('E3', 0.5),
    ])

    add_measure(part, 15, [
        ch(['D2', 'G2', 'A2', 'C3', 'E3'], 1.5),  # D9sus4 (lower voicing)
        n('G2', 1.0), n('A2', 0.5),
    ])

    add_measure(part, 16, [
        ch(['D2', 'F#2', 'A2', 'C3', 'E3'], 1.5),  # D13 (lower)
        n('F#2', 0.5), n('A2', 1.0),
    ])

    # ── Section B: mm.17-32 -- She walks in ──

    add_measure(part, 17, [
        ch(['G2', 'D3', 'F#3', 'B3'], 1.5),  # Gmaj7 chord
        n('D3', 0.5), n('F#3', 0.5), n('B3', 0.5),
    ], dyn='mp')

    add_measure(part, 18, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9 chord
        n('C3', 0.5), n('E3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 19, [
        ch(['B2', 'D3', 'F#3', 'A3'], 1.5),  # Bm7 chord
        n('D3', 1.0), n('A3', 0.5),
    ])

    add_measure(part, 20, [
        ch(['C3', 'E3', 'G3', 'B3', 'D4'], 1.5),  # Cmaj9 chord
        n('G3', 0.5), n('C4', 0.5), n('D4', 0.5),
    ])

    # m.21-24: D9 - Em9 - Cmaj9 - Dsus4-D7
    add_measure(part, 21, [
        ch(['D3', 'F#3', 'A3', 'C4', 'E4'], 1.5),  # D9
        n('F#3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 22, [
        ch(['E2', 'B2', 'D3', 'G3', 'F#3'], 1.5),  # Em9
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 23, [
        ch(['C3', 'E3', 'G3', 'B3', 'D4'], 1.5),  # Cmaj9
        n('E3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 24, [
        ch(['D3', 'G3', 'A3', 'C4'], 1.5),  # Dsus4
        ch(['D3', 'F#3', 'A3', 'C4'], 1.5),  # D7
    ], dyn='mf')

    # m.25-28: Gmaj9 - Em9 - Cmaj7 - D7sus4
    add_measure(part, 25, [
        ch(['G2', 'B2', 'D3', 'F#3', 'A3'], 1.5),  # Gmaj9
        n('D3', 0.5), n('F#3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 26, [
        ch(['E2', 'B2', 'D3', 'F#3', 'G3'], 1.5),  # Em9
        n('B2', 0.5), n('D3', 0.5), n('F#3', 0.5),
    ])

    add_measure(part, 27, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('E3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 28, [
        ch(['D3', 'G3', 'A3', 'C4', 'E4'], 1.5),  # D9sus4
        n('G3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ], dyn='mp')

    # m.29-32: Closing B section
    add_measure(part, 29, [
        ch(['G2', 'B2', 'D3', 'F#3'], 0.75),
        n('G3', 0.25), n('B3', 0.5),
        n('D4', 1.0), n('B3', 0.5),
    ])

    add_measure(part, 30, [
        n('E3', 0.75), n('A3', 0.25), n('C4', 0.5),
        n('E4', 1.0, accent=True, trill=True), n('D4', 0.5),
    ])

    add_measure(part, 31, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),
        r(1.5),
    ])

    add_measure(part, 32, [
        ch(['C3', 'E3', 'G3', 'B3'], 0.75),  # Cmaj7
        n('E3', 0.25), n('G3', 0.5),
        ch(['D3', 'F#3', 'A3', 'C4'], 1.0),  # D7
        n('G3', 0.5),
    ])

    # ── Section C: mm.33-48 -- Afternoon together ──

    add_measure(part, 33, [
        ch(['G2', 'B2', 'D3', 'F#3'], 0.75),
        n('G3', 0.25), n('B3', 0.5),
        n('D4', 1.0), n('B3', 0.5),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=69))

    add_measure(part, 34, [
        n('F#3', 0.75), n('B3', 0.25), n('D4', 0.5),
        n('F#4', 1.0, accent=True, trill=True), n('D4', 0.5),
    ])

    add_measure(part, 35, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),
        r(1.5),
    ])

    add_measure(part, 36, [
        ch(['C3', 'E3', 'G3', 'B3'], 0.75),  # Cmaj7
        n('E3', 0.25), n('G3', 0.5),
        ch(['D3', 'F#3', 'A3', 'C4'], 1.0),  # D7
        n('A3', 0.5),
    ])

    # m.37-40: Am9 - D9 - Gmaj9 - Bm9
    add_measure(part, 37, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9
        n('C3', 0.5), n('E3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 38, [
        ch(['D3', 'F#3', 'A3', 'C4', 'E4'], 1.5),  # D9
        n('F#3', 0.5), n('C4', 0.5), n('E4', 0.5),
    ])

    add_measure(part, 39, [
        ch(['G2', 'B2', 'D3', 'F#3', 'A3'], 1.5),  # Gmaj9
        n('B3', 0.5), n('D4', 0.5), n('F#4', 0.5),
    ])

    add_measure(part, 40, [
        ch(['B2', 'D3', 'F#3', 'A3', 'C#4'], 1.5),  # Bm9
        n('F#3', 0.5), n('A3', 0.5), n('D4', 0.5),
    ], dyn='f')

    # m.41-44: Em7 - Am9 - B7 - Em9 (E minor excursion)
    add_measure(part, 41, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),  # Em7
        n('F#3', 0.75), n('G3', 0.25), n('B3', 0.5),
    ], dyn='p')

    add_measure(part, 42, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9
        n('C3', 1.0), n('G3', 0.5),
    ])

    add_measure(part, 43, [
        n('B1', 0.75), n('D#2', 0.25), n('F#2', 0.5),  # lower B7 voicing for range
        n('A2', 1.0), n('F#2', 0.5),
    ])

    add_measure(part, 44, [
        ch(['E2', 'B2', 'D3', 'F#3', 'G3'], 1.5),  # Em9
        n('B2', 1.0), n('E3', 0.5),
    ], dyn='pp', expression_text='sospirando')

    # m.45-48: Em9 - A7 - D9 - Gmaj9
    add_measure(part, 45, [
        ch(['E2', 'B2', 'D3', 'G3', 'F#3'], 1.5),  # Em9
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 46, [
        ch(['A2', 'C#3', 'E3', 'G3'], 1.5),  # A7
        n('C#3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 47, [
        ch(['D3', 'F#3', 'A3', 'C4', 'E4'], 1.5),  # D9
        n('F#3', 0.5), n('A3', 1.0),
    ])

    add_measure(part, 48, [
        ch(['G2', 'B2', 'D3', 'F#3', 'A3'], 1.5),  # Gmaj9
        ch(['G2', 'B2', 'D3', 'F#3'], 1.0),  # Gmaj7
        r(0.5),
    ], dyn='f')

    # ── Section D: mm.49-60 -- Walking home at dusk (Db major) ──

    add_measure(part, 49, [
        ch(['Ab2', 'Eb3', 'Ab3', 'C4', 'G4'], 1.5),
        n('Eb3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
    ], dyn='f', expression_text='largamente',
       ks=key.Key('Db'),
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=60))

    add_measure(part, 50, [
        n('Bb2', 1.0), n('Db3', 0.5),
        n('F3', 0.75), n('Ab3', 0.25), n('F3', 0.5),
    ])

    add_measure(part, 51, [
        n('Eb2', 0.75), n('G2', 0.25), n('Bb2', 0.5),
        n('Db3', 1.0), n('Bb2', 0.5),
    ])

    add_measure(part, 52, [
        ch(['Ab2', 'C3', 'Eb3', 'G3'], 1.5),
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ])

    # m.53-56: Peak
    add_measure(part, 53, [
        ch(['F2', 'Ab2', 'C3', 'Eb3'], 1.5),  # Fm7
        n('Ab2', 0.75), n('C3', 0.25), n('Eb3', 0.5),  # smoother voice leading
    ], dyn='ff')

    add_measure(part, 54, [
        ch(['Db2', 'F2', 'Ab2', 'C3', 'Eb3'], 1.5),  # Dbmaj9
        n('Db3', 0.5), n('F3', 1.0),
    ])

    add_measure(part, 55, [
        n('Eb2', 1.0), n('Bb2', 0.5),
        n('Db3', 0.75), n('G3', 0.25), n('Db3', 0.5),
    ], dyn='mf')

    add_measure(part, 56, [
        ch(['Ab2', 'Eb3', 'Ab3', 'C4', 'G4'], 1.5, fermata=True),  # Abmaj7 with fermata
        n('Eb3', 1.0), n('Ab3', 0.5),
    ])

    # m.57-60: Transition back to G
    add_measure(part, 57, [
        ch(['Bb1', 'Db2', 'F2', 'Ab2', 'C3'], 1.5),  # Bbm9 -- very low for range
        n('Db2', 0.75), n('F2', 0.25), n('Ab2', 0.5),
    ], dyn='mp')

    add_measure(part, 58, [
        n('D2', 1.0), n('F#2', 0.5),  # lower D voicing for range
        n('A2', 0.75), n('C3', 0.25), n('A2', 0.5),
    ], ks=key.Key('G'))

    add_measure(part, 59, [
        n('E2', 0.75), n('G2', 0.25), n('B2', 0.5),
        n('D3', 1.0), n('B2', 0.5),
    ])

    add_measure(part, 60, [
        ch(['G2', 'D3', 'G3', 'B3'], 1.5),
        n('D3', 1.0), n('G3', 0.5),
    ], dyn='p')

    # ── Section A': mm.61-72 -- Alone again ──

    # m.61-64: Gmaj7 - Gadd9 - Cmaj7 - D7 (reprise with 7ths)
    add_measure(part, 61, [
        ch(['G2', 'D3', 'G3', 'B3', 'F#4'], 1.5, staccato=True),  # Gmaj7
        n('D3', 0.5, staccato=True), n('G3', 0.5), n('B3', 0.5),
    ], dyn='p',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=58))

    add_measure(part, 62, [
        ch(['G2', 'D3', 'A3', 'B3'], 1.5, staccato=True),  # Gadd9
        n('A3', 0.5, staccato=True), n('B3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 63, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5, staccato=True),  # Cmaj7
        n('G3', 0.5, staccato=True), n('B3', 0.5), n('E4', 0.5),
    ])

    add_measure(part, 64, [
        ch(['D3', 'F#3', 'A3', 'C4'], 1.5, staccato=True),  # D7
        n('F#3', 0.5, staccato=True), n('A3', 0.5), n('C4', 0.5),
    ])

    # m.65-66: Em9 - Cmaj9
    add_measure(part, 65, [
        ch(['E2', 'B2', 'D3', 'G3', 'F#3'], 1.5),  # Em9
        n('B2', 1.0), n('G3', 0.5),
    ], dyn='pp')

    add_measure(part, 66, [
        ch(['C3', 'E3', 'G3', 'B3', 'D4'], 1.5),  # Cmaj9
        n('E3', 1.0), n('B3', 0.5),
    ])

    # m.67-68: Piano echoes clarinet motif
    add_measure(part, 67, [
        n('G2', 0.5, staccato=True), n('B2', 0.5), n('F#3', 0.5),
        n('G4', 1.0 / 3), n('A4', 1.0 / 3), n('B4', 1.0 / 3),
        n('D5', 0.5),
    ])

    add_measure(part, 68, [
        n('E2', 0.5, staccato=True), n('B2', 0.5), n('G3', 0.5),
        n('C5', 1.0, tenuto=True), n('B4', 0.5),
    ])

    # m.69-70: Winding down
    add_measure(part, 69, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('E3', 1.0), n('B3', 0.5),
    ])

    add_measure(part, 70, [
        ch(['D2', 'F#2', 'A2', 'C3'], 1.5),  # D7 low
        n('F#2', 1.0), n('A2', 0.5),
    ], dyn='ppp', expression_text='morendo')

    # m.71-72: Final chords
    add_measure(part, 71, [
        n('D2', 1.0), n('G2', 0.5),
        n('A2', 0.5), n('C3', 1.0),
    ])

    add_measure(part, 72, [
        ch(['G1', 'D2', 'G2', 'A2', 'B2', 'F#3'], 3.0, fermata=True),  # Gmaj7 low voicing
    ])


# ── Add Hairpins ──────────────────────────────────────────────────────────

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins."""
    piano = None
    clarinet = None
    for p in score.parts:
        if 'Piano' in (p.partName or ''):
            piano = p
        elif 'Clarinet' in (p.partName or ''):
            clarinet = p

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
        # Piano hairpins
        ('piano', 5, 7, 'crescendo'),
        ('piano', 8, 8, 'diminuendo'),
        ('piano', 13, 16, 'crescendo'),
        ('piano', 21, 23, 'crescendo'),
        ('piano', 25, 27, 'diminuendo'),
        ('piano', 33, 35, 'crescendo'),
        ('piano', 41, 43, 'diminuendo'),
        ('piano', 45, 47, 'crescendo'),
        ('piano', 53, 55, 'diminuendo'),
        ('piano', 56, 56, 'diminuendo'),
        ('piano', 60, 60, 'diminuendo'),
        ('piano', 69, 71, 'diminuendo'),
        # Clarinet hairpins
        ('clarinet', 21, 23, 'crescendo'),
        ('clarinet', 25, 27, 'crescendo'),
        ('clarinet', 37, 39, 'crescendo'),
        ('clarinet', 41, 43, 'diminuendo'),
        ('clarinet', 45, 47, 'crescendo'),
        ('clarinet', 53, 55, 'diminuendo'),
        ('clarinet', 57, 59, 'diminuendo'),
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        p = piano if part_name == 'piano' else clarinet
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


# ── Main ─────────────────────────────────────────────────────────────────

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
