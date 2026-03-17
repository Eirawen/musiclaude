#!/usr/bin/env python3
"""Generate 'Matin d'ete' -- Clarinet in Bb + Piano.

First love at 17, summer in a French village, working at a bakery.
6/8 time, G major (concert pitch). Clarinet in Bb transposes automatically.

Sections:
  I.   Dawn (mm.1-12) -- Piano alone, gentle arpeggios. The bakery waking.
  II.  She Arrives (mm.13-28) -- Clarinet enters, hopeful melody.
  III. Flour Dust (mm.29-44) -- Playful call-and-response, working together.
  IV.  Walking Home (mm.45-52) -- Eb major, the world changed.
  V.   Goodnight (mm.53-64) -- Return to G, clarinet fades, memory lingers.
"""

from music21 import (
    stream, note, chord, key, meter, tempo, instrument,
    expressions, dynamics, duration, clef, bar, layout,
    articulations, spanner, tie,
)
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


# ── Build Score ──────────────────────────────────────────────────────────

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    # -- Clarinet in Bb Part --
    clarinet_part = stream.Part()
    clarinet_inst = instrument.Clarinet()  # Bb clarinet, music21 handles transposition
    clarinet_part.insert(0, clarinet_inst)
    clarinet_part.partName = "Clarinet in Bb"
    clarinet_part.partAbbreviation = "Cl."

    # -- Piano Part --
    piano_part = stream.Part()
    piano_inst = instrument.Piano()
    piano_part.insert(0, piano_inst)
    piano_part.partName = "Piano"
    piano_part.partAbbreviation = "Pno."

    build_clarinet(clarinet_part)
    build_piano(piano_part)

    s.insert(0, clarinet_part)
    s.insert(0, piano_part)

    return s


# ── Clarinet Part ────────────────────────────────────────────────────────
# Written at CONCERT pitch. music21's Clarinet instrument handles
# transposition to written pitch (up M2) in the MusicXML output.

def build_clarinet(part):
    """Build the clarinet part (64 measures)."""

    # ── Section I: mm.1-12 - Tacet (piano solo) ──
    for m_num in range(1, 13):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('6/8')
            kwargs['ks'] = key.Key('G')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=66,
                text="Andante, avec tendresse"
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # ── Section II: mm.13-28 - She Arrives ──
    # The clarinet's first entrance: a simple rising figure, like looking up
    # and seeing someone for the first time.

    # m.13-14: Primary motif -- G4-A4-B4, pause, gentle fall
    add_measure(part, 13, [
        r(1.5),
        n('G4', 0.5), n('A4', 0.5), n('B4', 0.5),
    ], dyn='p', expression_text='semplice')

    add_measure(part, 14, [
        n('D5', 1.5, tenuto=True),
        n('C#5', 0.5), n('B4', 0.5), n('A4', 0.5),  # C#5 chromatic passing tone
    ])

    # m.15-16: Response -- settling on G, a sigh (triplet figure adds rhythmic variety)
    add_measure(part, 15, [
        n('B4', 1.0), n('A4', 0.5),
        n('G4', 1.5, tenuto=True),
    ])

    add_measure(part, 16, [
        n('G4', 1.0), n('F#4', 0.5),
        n('G4', 1.5),  # decorated resolution
    ])

    # m.17-20: Second phrase -- reaching higher, more courage
    add_measure(part, 17, [
        n('A4', 0.5), n('B4', 0.5), n('D5', 0.5),
        n('E5', 1.0, tenuto=True), n('D5', 0.5),
    ], dyn='mp')

    add_measure(part, 18, [
        n('C5', 0.75), n('B4', 0.25), n('A4', 0.5),  # dotted eighth + sixteenth + eighth
        n('G4', 1.0), n('F#4', 0.5),
    ])

    add_measure(part, 19, [
        n('A4', 0.5), n('C5', 0.5), n('E5', 0.5),
        n('F#5', 1.0, accent=True), n('E5', 0.5),
    ])

    add_measure(part, 20, [
        n('D5', 2.0, tenuto=True), n('C5', 0.5), n('B4', 0.5),  # half note (2.0 QL) = new duration
    ])

    # m.21-24: Third phrase -- Em7 coloring, a touch of shyness
    add_measure(part, 21, [
        r(1.5),
        n('B4', 0.5), n('C5', 0.5), n('D5', 0.5),
    ])

    add_measure(part, 22, [
        n('E5', 0.75), n('D5', 0.25), n('C5', 0.5),  # dotted eighth + sixteenth + eighth
        n('B4', 1.0), n('A4', 0.5),
    ])

    add_measure(part, 23, [
        n('G4', 1.0), n('F#4', 0.5),
        n('E4', 1.0), n('D4', 0.5),
    ])

    add_measure(part, 24, [
        n('E4', 1.5, tenuto=True), r(1.5),
    ], dyn='p')

    # m.25-28: Closing phrase -- return to G, warmth
    add_measure(part, 25, [
        n('G4', 1.0), n('B4', 0.5),
        n('D5', 0.75), n('E5', 0.25), n('D5', 0.5),
    ], dyn='mp')

    add_measure(part, 26, [
        n('C5', 1.0, accent=True), n('B4', 0.5),
        n('A4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 27, [
        n('A4', 0.5), n('B4', 0.5), n('C5', 0.5),
        n('D5', 1.5, tenuto=True),
    ])

    add_measure(part, 28, [
        n('B4', 2.5), n('A4', 0.5),  # dotted half (2.5 QL) = another new duration
    ])

    # ── Section III: mm.29-44 - Flour Dust (playful, working together) ──
    add_measure(part, 29, [
        n('D5', 0.5, staccato=True), n('B4', 0.5, staccato=True), n('G4', 0.5, staccato=True),
        n('A4', 1.0), n('B4', 0.5),
    ], dyn='mf', expression_text='leggiero',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=72))

    add_measure(part, 30, [
        n('C5', 0.5, staccato=True), n('D5', 0.5, staccato=True), n('E5', 0.5, staccato=True),
        # triplet figure -- three notes in the space of a quarter (1.0 QL)
        n('D5', 1.0/3), n('C5', 1.0/3), n('D5', 1.0/3),
        n('E5', 0.5),
    ])

    add_measure(part, 31, [
        r(1.5),  # piano responds
        n('E5', 0.5, staccato=True), n('D5', 0.5, staccato=True), n('C5', 0.5),
    ])

    add_measure(part, 32, [
        n('B4', 0.75), n('A4', 0.25), n('G4', 0.5),  # dotted eighth + sixteenth + eighth
        n('G4', 1.5, tenuto=True),
    ])

    # m.33-36: Second exchange, more animated
    add_measure(part, 33, [
        n('B4', 0.5, staccato=True), n('D5', 0.5, staccato=True), n('F#5', 0.5),
        n('G5', 1.0, accent=True), n('F#5', 0.5),
    ], dyn='f')

    add_measure(part, 34, [
        n('E5', 0.75), n('D5', 0.25), n('C#5', 0.5),  # chromatic C#, dotted rhythm
        n('B4', 1.0, tenuto=True), n('A4', 0.5),
    ])

    add_measure(part, 35, [
        r(1.5),  # piano responds
        n('D5', 0.75), n('E5', 0.25), n('F#5', 0.5),
    ])

    add_measure(part, 36, [
        n('G5', 1.5, accent=True),
        n('F#5', 0.5, staccato=True), n('E5', 0.5, staccato=True), n('D5', 0.5),
    ], dyn='mf')

    # m.37-40: E minor moment -- a flour-dusted hand accidentally touched
    add_measure(part, 37, [
        n('E5', 1.5, tenuto=True),
        n('D5', 0.5), n('C5', 0.5), n('B4', 0.5),
    ], dyn='p', expression_text='dolce')

    add_measure(part, 38, [
        n('A4', 1.0), n('G#4', 0.5),  # chromatic G# -- borrowed from E major, bittersweet
        n('A4', 0.75), n('B4', 0.25), n('C5', 0.5),
    ])

    add_measure(part, 39, [
        n('B4', 0.75), n('A4', 0.25), n('G4', 0.5),
        n('F#4', 0.5), n('E4', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 40, [
        n('C4', 1.5, tenuto=True), r(1.5),  # C4 -- lowest point, vulnerability
    ], dyn='pp')

    # m.41-44: Recovery, building back
    add_measure(part, 41, [
        r(1.5),
        n('G4', 0.5), n('A4', 0.5), n('B4', 0.5),
    ], dyn='mp')

    add_measure(part, 42, [
        n('C5', 1.0), n('D5', 0.5),
        n('E5', 1.0), n('D5', 0.5),
    ])

    add_measure(part, 43, [
        n('C5', 0.5), n('B4', 0.5), n('A4', 0.5),
        n('B4', 1.0, accent=True), n('C5', 0.5),
    ])

    add_measure(part, 44, [
        n('D5', 1.0), n('E5', 0.5),
        n('F#5', 1.5, tenuto=True),
    ], dyn='mf')

    # ── Section IV: mm.45-52 - Walking Home at Dusk (Eb major) ──
    add_measure(part, 45, [
        n('Eb5', 1.0, accent=True), n('F5', 0.5),
        n('G5', 1.0), n('Bb4', 0.5),
    ], dyn='f', expression_text='con calore',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=76))

    add_measure(part, 46, [
        n('C5', 1.0), n('Eb5', 0.5),
        n('F5', 1.5),
    ])

    add_measure(part, 47, [
        n('G5', 0.5), n('F5', 0.5), n('Eb5', 0.5),
        n('D5', 1.0), n('C5', 0.5),
    ])

    add_measure(part, 48, [
        n('Bb4', 1.5, tenuto=True), r(0.5),
        n('C5', 0.5), n('D5', 0.5),
    ])

    # m.49-52: Climax and release
    add_measure(part, 49, [
        n('Eb5', 0.5), n('G5', 0.5), n('Ab5', 0.5),
        n('Bb5', 1.5, accent=True),  # highest point -- Bb5, the shared silence before parting
    ], dyn='ff')

    add_measure(part, 50, [
        n('Ab5', 0.75), n('G5', 0.25), n('F5', 0.5),  # dotted rhythm in descent
        n('Eb5', 1.0, tenuto=True), n('C5', 0.5),
    ], dyn='mf')

    add_measure(part, 51, [
        n('Bb4', 1.0), n('C5', 0.5),
        n('D5', 0.75), n('Eb5', 0.25), n('D5', 0.5),  # dotted ornament
    ])

    add_measure(part, 52, [
        n('D5', 1.5, tenuto=True),
        n('C5', 0.5), n('B4', 0.5), n('A4', 0.5),  # B natural pivot back
    ], dyn='mp')

    # ── Section V: mm.53-64 - Goodnight (G major return) ──
    # Mostly tacet -- the clarinet reappears only briefly, a memory

    for m_num in range(53, 57):
        kwargs = {}
        if m_num == 53:
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=63,
                text="Lento"
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # m.57-60: Ghost of the opening motif
    add_measure(part, 57, [
        r(1.5),
        n('G4', 0.5), n('A4', 0.5), n('B4', 0.5),
    ], dyn='pp')

    add_measure(part, 58, [
        n('D5', 1.5, tenuto=True),
        n('C5', 0.5), n('B4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 59, [
        n('G4', 1.5), r(1.5),
    ])

    # m.60-64: Tacet to end
    for m_num in range(60, 65):
        add_measure(part, m_num, [r(3.0)])


# ── Piano Part ───────────────────────────────────────────────────────────

def build_piano(part):
    """Build the piano part (64 measures)."""

    # ── Section I: mm.1-12 - Dawn ──
    # Gentle arpeggiated figures in G major -- morning light through the bakery window

    # m.1-4: Gmaj7 - Gadd9 - Cmaj7 - D9sus4
    add_measure(part, 1, [
        ch(['G2', 'D3', 'G3', 'B3', 'F#4'], 1.5),  # Gmaj7
        n('D3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ], ts=meter.TimeSignature('6/8'),
        ks=key.Key('G'),
        tempo_mark=tempo.MetronomeMark(
            referent=duration.Duration(1.5), number=66,
            text="Andante, avec tendresse"
        ),
        dyn='pp', expression_text='dolce')

    add_measure(part, 2, [
        ch(['G2', 'D3', 'A3', 'B3'], 1.5),  # Gadd9
        n('A3', 0.5), n('B3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 3, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('G3', 0.5), n('B3', 0.5), n('E4', 0.5),
    ])

    add_measure(part, 4, [
        ch(['D3', 'G3', 'A3', 'B3'], 1.5),  # D9sus4 (no third -- floating)
        n('G3', 0.5), n('A3', 0.5), n('D4', 0.5),
    ])

    # m.5-8: Em7 - Cmaj7 - D7sus4 - D7
    add_measure(part, 5, [
        n('E2', 1.5),  # dotted quarter bass
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ], dyn='p')

    add_measure(part, 6, [
        n('C2', 0.75), n('E2', 0.25), n('G2', 0.5),  # dotted eighth + sixteenth + eighth
        n('B2', 1.0), n('E3', 0.5),
    ])  # Cmaj7

    add_measure(part, 7, [
        ch(['D3', 'G3', 'A3', 'C4'], 1.5),  # D7sus4
        n('G3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 8, [
        ch(['D3', 'F#3', 'A3', 'C4'], 1.5),  # D7
        n('F#3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ], dyn='pp')

    # m.9-12: G - Am7 - Bm7 - Cmaj7 (ascending bass, dawn brightening)
    add_measure(part, 9, [
        ch(['G2', 'D3', 'G3', 'B3'], 1.5),
        n('D3', 1.0), n('B3', 0.5),
    ], dyn='p')

    add_measure(part, 10, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 11, [
        ch(['B2', 'D3', 'F#3', 'A3'], 1.5),  # Bm7
        n('D3', 0.5), n('F#3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 12, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('E3', 0.75), n('G3', 0.25), n('B3', 0.5),
    ])

    # ── Section II: mm.13-28 - She Arrives ──
    # Piano accompaniment becomes warmer under the clarinet melody

    # m.13-16: G - D/F# - Em7 - Cmaj7
    add_measure(part, 13, [
        n('G2', 2.0),  # half note bass pedal
        n('D3', 0.5), n('B3', 0.5),
    ], dyn='p')

    add_measure(part, 14, [
        n('F#2', 0.75), n('A2', 0.25), n('D3', 0.5),
        n('F#3', 1.0), n('A3', 0.5),
    ])  # D/F#

    add_measure(part, 15, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),  # Em7
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 16, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('E3', 1.0), n('G3', 0.5),
    ])

    # m.17-20: G - Am7 - D7 - Gmaj7
    add_measure(part, 17, [
        ch(['G2', 'B2', 'D3', 'G3'], 1.5),
        n('D3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ], dyn='mp')

    add_measure(part, 18, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7
        n('E3', 0.5), n('G3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 19, [
        n('D2', 0.75), n('F#2', 0.25), n('A2', 0.5),
        n('C3', 1.0), n('A2', 0.5),
    ])  # D7

    add_measure(part, 20, [
        ch(['G2', 'B2', 'D3', 'F#3'], 1.5),  # Gmaj7
        n('B2', 0.5), n('D3', 0.5), n('F#3', 0.5),
    ])

    # m.21-24: Em - C - Am7 - Bm7
    add_measure(part, 21, [
        ch(['E2', 'G2', 'B2', 'E3'], 1.5),  # Em
        n('G2', 0.5), n('B2', 0.5), n('E3', 0.5),
    ])

    add_measure(part, 22, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('G3', 0.75), n('E3', 0.25), n('C3', 0.5),
    ])

    add_measure(part, 23, [
        n('A2', 0.75), n('C3', 0.25), n('E3', 0.5),
        n('G3', 1.0), n('E3', 0.5),
    ])  # Am7

    add_measure(part, 24, [
        ch(['B2', 'D3', 'F#3', 'A3'], 1.5),  # Bm7
        n('D3', 1.0), n('A3', 0.5),
    ])

    # m.25-28: Cmaj9 - D7 - Em7 - D7/F# (closing phrase)
    add_measure(part, 25, [
        ch(['C3', 'E3', 'G3', 'B3', 'D4'], 1.5),  # Cmaj9
        n('E3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ], dyn='mp')

    add_measure(part, 26, [
        ch(['D3', 'F#3', 'A3', 'C4'], 1.5),  # D7
        n('F#3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 27, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),  # Em7
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 28, [
        n('D2', 0.75), n('F#2', 0.25), n('A2', 0.5),
        n('C3', 1.0), n('F#3', 0.5),
    ])  # D7/F#

    # ── Section III: mm.29-44 - Flour Dust ──
    # Playful, more rhythmic. Call and response.

    # m.29-32: Gmaj7 - D9 - Em7 - Cmaj7
    add_measure(part, 29, [
        ch(['G2', 'B2', 'D3', 'F#3'], 0.75),  # Gmaj7
        n('G3', 0.25), n('B3', 0.5),
        n('D4', 1.0), n('B3', 0.5),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=72))

    add_measure(part, 30, [
        # Piano response when clarinet sustains -- staccato with dotted rhythm
        n('D3', 0.5, staccato=True), n('F#3', 0.5, staccato=True), n('A3', 0.5, staccato=True),
        n('C4', 0.75), n('E4', 0.25), n('A3', 0.5),  # D9 flavor (E = 9th)
    ])

    add_measure(part, 31, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),  # Em7 -- piano plays while clarinet rests
        n('B3', 0.75), n('G3', 0.25), n('E3', 0.5),
    ])

    add_measure(part, 32, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('E3', 0.5, staccato=True), n('G3', 0.5, staccato=True), n('B3', 0.5),
    ])

    # m.33-36: G/B - D9 - Em9 - Am9
    add_measure(part, 33, [
        ch(['B2', 'D3', 'G3', 'B3', 'F#4'], 1.5),  # Gmaj7/B
        n('D3', 0.5, staccato=True), n('G3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 34, [
        ch(['D3', 'F#3', 'A3', 'C4', 'E4'], 1.5),  # D9
        n('F#3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 35, [
        ch(['E2', 'B2', 'D3', 'G3', 'F#3'], 1.5),  # Em9
        n('G3', 0.75), n('A3', 0.25), n('B3', 0.5),
    ])

    add_measure(part, 36, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    # m.37-40: Em - Am7 - B7 - Em (minor moment)
    add_measure(part, 37, [
        ch(['E2', 'G2', 'B2', 'E3'], 1.5),  # Em
        n('G2', 0.75), n('B2', 0.25), n('E3', 0.5),
    ], dyn='p')

    add_measure(part, 38, [
        n('A2', 1.0), n('C3', 0.5),
        n('E3', 0.75), n('G3', 0.25), n('E3', 0.5),
    ])  # Am7

    add_measure(part, 39, [
        n('B2', 0.75), n('D#3', 0.25), n('F#3', 0.5),
        n('A3', 1.0), n('F#3', 0.5),
    ])  # B7

    add_measure(part, 40, [
        ch(['E2', 'G2', 'B2', 'E3'], 1.5),  # Em
        n('B2', 1.0), n('E3', 0.5),
    ], dyn='pp')

    # m.41-44: Am9 - D7 - Gmaj7 - D7/F# (hemiola rhythm in m.43)
    add_measure(part, 41, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ], dyn='mp')

    add_measure(part, 42, [
        n('D2', 0.75), n('F#2', 0.25), n('A2', 0.5),
        n('C3', 1.0), n('F#3', 0.5),
    ])  # D7

    add_measure(part, 43, [
        # Hemiola: 3 quarter notes against 6/8 = 2+2+2 vs 3+3
        ch(['G2', 'B2', 'D3'], 1.0),
        ch(['B2', 'D3', 'G3'], 1.0),
        ch(['D3', 'G3', 'B3'], 1.0),
    ])

    add_measure(part, 44, [
        n('F#2', 1.0), n('A2', 0.5),
        n('D3', 0.75), n('F#3', 0.25), n('A3', 0.5),
    ], dyn='mf')  # D7/F#

    # ── Section IV: mm.45-52 - Walking Home (Eb major) ──

    add_measure(part, 45, [
        ch(['Eb2', 'Bb2', 'Eb3', 'G3', 'D4'], 1.5),  # Ebmaj9
        n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ], dyn='f', expression_text='con calore',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=76))

    add_measure(part, 46, [
        ch(['Ab2', 'C3', 'Eb3', 'G3'], 1.5),  # Abmaj7
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 47, [
        ch(['Bb2', 'D3', 'F3', 'Ab3'], 1.5),  # Bb7
        n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
    ])

    add_measure(part, 48, [
        ch(['Eb2', 'G2', 'Bb2', 'D3'], 1.5),  # Ebmaj7
        n('G2', 0.75), n('Bb2', 0.25), n('Eb3', 0.5),  # dotted rhythm
    ])

    # m.49-52: Fm9 - Abmaj7 - Bb9 - D7 (pivot)
    add_measure(part, 49, [
        ch(['F2', 'Ab2', 'C3', 'Eb3', 'G3'], 1.5),  # Fm9
        n('Ab2', 0.75), n('C3', 0.25), n('Eb3', 0.5),
    ], dyn='ff')

    add_measure(part, 50, [
        ch(['Ab2', 'C3', 'Eb3', 'G3'], 1.5),  # Abmaj7
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ], dyn='mf')

    add_measure(part, 51, [
        ch(['Bb2', 'D3', 'F3', 'Ab3', 'C4'], 1.5),  # Bb9
        n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
    ])

    add_measure(part, 52, [
        n('D2', 0.75), n('F#2', 0.25), n('A2', 0.5),  # D7 -- pivot back to G
        n('C3', 1.0), n('A2', 0.5),
    ], dyn='mp')

    # ── Section V: mm.53-64 - Goodnight ──
    # Opening material returns, more intimate

    # m.53-56: Gmaj7 - Gadd9 - Cmaj9 - D9sus4 (echo of opening, richer)
    add_measure(part, 53, [
        ch(['G2', 'D3', 'G3', 'B3', 'F#4'], 1.5),  # Gmaj7
        n('D3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ], dyn='p',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=63,
                                       text="Lento"))

    add_measure(part, 54, [
        ch(['G2', 'D3', 'A3', 'B3'], 1.5),  # Gadd9
        n('A3', 0.5), n('B3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 55, [
        ch(['C3', 'E3', 'G3', 'B3', 'D4'], 1.5),  # Cmaj9
        n('E3', 0.5), n('G3', 0.5), n('B3', 0.5),
    ])

    add_measure(part, 56, [
        ch(['D3', 'G3', 'A3', 'B3'], 1.5),  # D9sus4
        n('G3', 0.5), n('A3', 0.5), n('D4', 0.5),
    ])

    # m.57-60: Em9 - Cmaj7 - Am9 - D7 (piano echoes melody)
    add_measure(part, 57, [
        ch(['E2', 'B2', 'D3', 'F#3'], 1.5),  # Em9
        # right hand takes the clarinet motif
        n('G4', 0.5, tenuto=True), n('A4', 0.5), n('B4', 0.5),
    ], dyn='pp')

    add_measure(part, 58, [
        n('C2', 0.75), n('E2', 0.25), n('G2', 0.5),
        n('B3', 1.0, tenuto=True), n('G3', 0.5),
    ])

    add_measure(part, 59, [
        ch(['A2', 'C3', 'E3', 'G3', 'B3'], 1.5),  # Am9
        n('C3', 1.0), n('E3', 0.5),
    ])

    add_measure(part, 60, [
        ch(['D3', 'F#3', 'A3', 'C4'], 1.5),  # D7
        n('F#3', 1.0, tenuto=True), n('A3', 0.5),
    ])

    # m.61-64: Em7 - Cmaj7 - Dsus4 - Gadd9 (unresolved, memory lingers)
    add_measure(part, 61, [
        ch(['E2', 'B2', 'D3', 'G3'], 1.5),  # Em7
        n('B2', 0.5), n('D3', 0.5), n('G3', 0.5),
    ], dyn='ppp', expression_text='morendo')

    add_measure(part, 62, [
        ch(['C3', 'E3', 'G3', 'B3'], 1.5),  # Cmaj7
        n('E3', 1.0), n('B3', 0.5),
    ])

    add_measure(part, 63, [
        n('D2', 1.0), n('G2', 0.5),
        n('A2', 0.5), n('D3', 1.0),
    ])  # Dsus4

    add_measure(part, 64, [
        ch(['G2', 'D3', 'G3', 'A3', 'B3'], 3.0, fermata=True),
    ])  # Gadd9 with fermata -- memory lingers


# ── Add Hairpins ─────────────────────────────────────────────────────────

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins to the score."""
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
        ('piano', 5, 7, 'crescendo'),       # dawn brightening
        ('piano', 8, 8, 'diminuendo'),       # settling
        ('piano', 9, 11, 'crescendo'),       # ascending bass
        ('piano', 25, 27, 'crescendo'),      # closing phrase
        ('piano', 37, 39, 'diminuendo'),     # minor moment
        ('piano', 41, 43, 'crescendo'),      # recovery
        ('piano', 49, 49, 'diminuendo'),     # post-climax
        ('piano', 56, 56, 'diminuendo'),     # section end
        ('piano', 61, 63, 'diminuendo'),     # morendo
        # Clarinet hairpins
        ('clarinet', 17, 19, 'crescendo'),   # reaching higher
        ('clarinet', 22, 24, 'diminuendo'),  # shy retreat
        ('clarinet', 29, 30, 'crescendo'),   # playful entry
        ('clarinet', 33, 34, 'crescendo'),   # animated
        ('clarinet', 37, 39, 'diminuendo'),  # tender moment
        ('clarinet', 41, 44, 'crescendo'),   # recovery
        ('clarinet', 49, 49, 'diminuendo'),  # post-climax release
        ('clarinet', 50, 51, 'diminuendo'),  # winding down
    ]

    for part_name, start_m, end_m, h_type in hairpin_specs:
        part = piano if part_name == 'piano' else clarinet
        if part is None:
            continue
        start_el = get_first_element(part, start_m)
        end_el = get_last_element(part, end_m)
        if start_el and end_el:
            if h_type == 'crescendo':
                hp = dynamics.Crescendo(start_el, end_el)
            else:
                hp = dynamics.Diminuendo(start_el, end_el)
            part.insert(0, hp)


# ── Main ─────────────────────────────────────────────────────────────────

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
