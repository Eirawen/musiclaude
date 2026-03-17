#!/usr/bin/env python3
"""Generate 'Matin de Boulangerie' -- Clarinet in Bb + Piano.

Follows the composition plan in scratchpad.md exactly:
  - 80 measures, 6/8, F major (piano) / G major (clarinet in Bb)
  - 5 sections with full harmonic, melodic, and expression plans.
"""

from music21 import (
    stream, note, chord, key, meter, tempo, instrument,
    expressions, dynamics, duration, clef, bar, layout,
    articulations, spanner, tie,
)
from music21.common.types import OffsetQL
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "score.musicxml")

# ── Helpers ──────────────────────────────────────────────────────────────

def n(pitch, dur, **kwargs):
    """Create a note. dur is in quarter-lengths (dotted quarter = 1.5, eighth = 0.5, etc.)."""
    nt = note.Note(pitch, quarterLength=dur)
    if kwargs.get('tie_start'):
        nt.tie = tie.Tie('start')
    if kwargs.get('tie_stop'):
        nt.tie = tie.Tie('stop')
    if kwargs.get('tie_continue'):
        nt.tie = tie.Tie('continue')
    if kwargs.get('staccato'):
        nt.articulations.append(articulations.Staccato())
    if kwargs.get('accent'):
        nt.articulations.append(articulations.Accent())
    if kwargs.get('tenuto'):
        nt.articulations.append(articulations.Tenuto())
    if kwargs.get('fermata'):
        nt.expressions.append(expressions.Fermata())
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
    return c


def measure_offset(m_num):
    """Return the offset in quarter-lengths for the start of measure m_num (1-indexed).
    6/8 = 3 quarter-lengths per measure."""
    return (m_num - 1) * 3.0


# ── Build Score ──────────────────────────────────────────────────────────

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    # -- Clarinet in Bb Part --
    clarinet_part = stream.Part()
    clarinet_inst = instrument.Clarinet()  # Bb clarinet (transposition = M-2)
    clarinet_part.insert(0, clarinet_inst)
    clarinet_part.partName = "Clarinet in Bb"
    clarinet_part.partAbbreviation = "Cl."

    # -- Piano Part --
    piano_part = stream.Part()
    piano_inst = instrument.Piano()
    piano_part.insert(0, piano_inst)
    piano_part.partName = "Piano"
    piano_part.partAbbreviation = "Pno."

    # Build measures for both parts
    build_clarinet(clarinet_part)
    build_piano(piano_part)

    s.insert(0, clarinet_part)
    s.insert(0, piano_part)

    return s


def add_measure(part, m_num, elements, ts=None, ks=None, tempo_mark=None,
                dyn=None, expression_text=None, cresc=False, decresc=False):
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


def add_hairpin(part, m_start, m_end, hairpin_type='crescendo'):
    """Add a hairpin (crescendo/diminuendo) spanning from m_start to m_end."""
    # We'll add these after building measures via spanners
    pass  # Handled inline


# ── Piano Arpeggiation Patterns ─────────────────────────────────────────

def piano_arpeggio_6_8(bass, mid, top, stac=False):
    """Standard 6/8 arpeggiation: bass-mid-top as eighth notes (3 QL total)."""
    return [
        n(bass, 0.5, staccato=stac),
        n(mid, 0.5),
        n(top, 0.5),
        n(bass, 0.5, staccato=stac),
        n(mid, 0.5),
        n(top, 0.5),
    ]


def piano_arpeggio_varied(bass, mid, top, high, stac=False):
    """Varied arpeggiation with an upper note: bass-mid-top-mid-high-top."""
    return [
        n(bass, 0.5, staccato=stac),
        n(mid, 0.5),
        n(top, 0.5),
        n(mid, 0.5),
        n(high, 0.5),
        n(top, 0.5),
    ]


def piano_dotted_pattern(bass, mid, top, stac=False):
    """Dotted-quarter pattern: bass(dotted quarter) mid-top(eighth) for rhythmic variety."""
    return [
        n(bass, 1.5, staccato=stac),  # dotted quarter
        n(mid, 1.0),                   # quarter
        n(top, 0.5),                   # eighth
    ]


def piano_mixed_rhythm(bass, mid, top, high):
    """Mixed rhythm: dotted eighth+sixteenth, then eighths. Adds rhythmic variety."""
    return [
        n(bass, 0.75),   # dotted eighth
        n(mid, 0.25),    # sixteenth
        n(top, 0.5),     # eighth
        n(high, 1.0),    # quarter
        n(top, 0.5),     # eighth
    ]


def piano_chord_pattern(pitches, dur=3.0):
    """Block chord for a full measure."""
    return [ch(pitches, dur)]


def piano_rocking(bass, p1, p2, stac=False):
    """Rocking accompaniment: bass, p1-p2 alternating."""
    return [
        n(bass, 0.5, staccato=stac),
        n(p1, 0.5),
        n(p2, 0.5),
        n(bass, 0.5, staccato=stac),
        n(p1, 0.5),
        n(p2, 0.5),
    ]


def piano_waltz_6_8(bass, mid, top):
    """Waltz-like 6/8: dotted quarter bass, quarter+eighth upper. Rhythmic variety."""
    return [
        n(bass, 1.5),   # dotted quarter
        n(mid, 1.0),    # quarter
        n(top, 0.5),    # eighth
    ]


# ── Clarinet Part ────────────────────────────────────────────────────────
# NOTE: Clarinet in Bb is a transposing instrument. music21 handles this:
# we write at CONCERT pitch and music21 transposes when writing MusicXML.
# Actually, for ClarinetBb, music21 writes in transposed (written) pitch
# in MusicXML. We need to think in SOUNDING pitch and let music21 handle it.
#
# Per scratchpad: written in G major (F#), sounding in F major.
# We'll write at SOUNDING pitch (concert pitch) and let music21 transpose.

def build_clarinet(part):
    """Build the clarinet part (80 measures). Rests in Section I and V (mostly)."""

    # ── Section I: mm.1-16 - Tacet (piano solo) ──
    for m_num in range(1, 17):
        elements = [r(3.0)]  # Full measure rest
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('6/8')
            kwargs['ks'] = key.Key('F')  # Concert pitch
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=72,
                text="Andante pastorale"
            )
        add_measure(part, m_num, elements, **kwargs)

    # ── Section II: mm.17-28 - Clarinet enters ──
    # m.17-18: Primary motif - ascending stepwise F4-G4-A4-Bb4, end on suspension Bb4->A4
    # (Concert pitch: sounds F4-G4-A4-Bb4-C5->Bb4)
    add_measure(part, 17, [
        n('F4', 1.0), n('G4', 0.5), n('A4', 1.0), n('Bb4', 0.5),
    ], dyn='mp', expression_text='espressivo')

    add_measure(part, 18, [
        n('C5', 1.5, tie_start=True), n('C5', 0.5, tie_stop=True),
        n('Bb4', 1.0, tenuto=True),
    ])

    # m.19-20: Response phrase - descending
    add_measure(part, 19, [
        n('A4', 1.0), n('G4', 0.5), n('F4', 1.0), n('E4', 0.5),
    ])

    add_measure(part, 20, [
        n('F4', 1.5, tenuto=True), r(1.5),
    ])

    # m.21-24: Second phrase - reaching higher
    add_measure(part, 21, [
        r(1.5), n('G4', 0.5), n('A4', 0.5), n('Bb4', 0.5),
    ])  # crescendo starts

    add_measure(part, 22, [
        n('C5', 0.75), n('D5', 0.25), n('E5', 0.5),  # dotted eighth+sixteenth+eighth
        n('D5', 0.5), n('Bb4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 23, [
        n('Bb4', 2.0), n('A4', 0.5), n('G4', 0.5),
        # 2.0 = half note, adds new duration type
    ])

    add_measure(part, 24, [
        n('A4', 1.5, tenuto=True), r(1.5),
    ], dyn='mf')

    # m.25-28: Closing phrase of section II -- brief Bb tonicization
    add_measure(part, 25, [
        n('F4', 1.0), n('A4', 0.5), n('C5', 0.75), n('D5', 0.25), n('Eb5', 0.5),
        # Eb5 suggests Bb tonicization via its 4th degree
    ])

    add_measure(part, 26, [
        n('D5', 1.0, accent=True), n('C5', 0.5), n('Bb4', 1.0), n('A4', 0.5),
    ])

    add_measure(part, 27, [
        n('G4', 1.0), n('A4', 0.5), n('Bb4', 1.5, tenuto=True),
    ])

    add_measure(part, 28, [
        n('A4', 1.5), r(1.5),
    ], dyn='mp')

    # ── Section III: mm.29-48 - Conversation ──
    # m.29-32: Clarinet melody with call-and-response
    add_measure(part, 29, [
        n('F4', 0.5), n('G4', 0.5), n('A4', 0.5), n('C5', 1.0), n('Bb4', 0.5),
    ], dyn='mp', expression_text='con moto',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=76))

    add_measure(part, 30, [
        n('A4', 1.5), r(1.5),  # rest for piano response
    ])

    add_measure(part, 31, [
        r(1.5),  # piano plays
        n('D5', 0.5), n('C5', 0.5), n('Bb4', 0.5),
    ])

    add_measure(part, 32, [
        n('A4', 1.0), n('G4', 0.5), n('F4', 1.5, tenuto=True),
    ])

    # m.33-36: Second call-response, building
    add_measure(part, 33, [
        n('G4', 0.5), n('Bb4', 0.5), n('D5', 0.5),
        n('E5', 1.0, accent=True), n('D5', 0.5),
    ])

    add_measure(part, 34, [
        n('C5', 1.0), n('Bb4', 0.5), n('A4', 1.5),
    ])

    add_measure(part, 35, [
        r(1.5),  # piano response
        n('C5', 0.5), n('D5', 0.5), n('E5', 0.5),
    ])

    add_measure(part, 36, [
        n('F5', 1.5, accent=True), n('E5', 0.75), n('D5', 0.25), n('C#5', 0.5),
        # C#5 suggests A7 tonicization toward Dm
    ], dyn='mf')

    # m.37-40: D minor excursion - vulnerability
    add_measure(part, 37, [
        n('D5', 1.5), n('C5', 0.5), n('Bb4', 0.5), n('A4', 0.5),
    ], dyn='p')

    add_measure(part, 38, [
        n('G4', 1.0), n('A4', 0.5), n('Bb4', 1.0), n('A4', 0.5),
    ])

    add_measure(part, 39, [
        n('A4', 0.75), n('G4', 0.25), n('F4', 0.5),  # dotted eighth+sixteenth+eighth
        n('E4', 1.0), n('C#4', 0.5),  # C#4 for A7->Dm tonicization
    ])

    add_measure(part, 40, [
        n('D4', 1.0, tenuto=True), n('C4', 0.5),  # dip to C4 for range
        r(1.5),
    ], dyn='pp')

    # m.41-44: Return to F major
    add_measure(part, 41, [
        r(1.5), n('A4', 0.5), n('Bb4', 0.5), n('C5', 0.5),
    ])

    add_measure(part, 42, [
        n('D5', 1.0), n('E5', 0.5), n('F5', 1.0), n('E5', 0.5),
    ])

    add_measure(part, 43, [
        n('D5', 0.5), n('C5', 0.5), n('Bb4', 0.5),
        n('C5', 1.0, accent=True), n('Bb4', 0.5),
    ])

    add_measure(part, 44, [
        n('A4', 1.0), n('C5', 0.5), n('F5', 1.5, tenuto=True),
    ], dyn='mf')

    # m.45-48: Building to peak
    add_measure(part, 45, [
        n('F5', 0.5), n('E5', 0.5), n('D5', 0.5),
        n('E5', 1.0), n('F5', 0.5),
    ])

    add_measure(part, 46, [
        n('G5', 1.5, accent=True), n('F#5', 0.5), n('E5', 0.5), n('D5', 0.5),
        # F#5 creates brief G minor tonicization (leading tone)
    ])

    add_measure(part, 47, [
        n('E5', 1.0), n('D5', 0.5), n('C5', 0.75), n('Bb4', 0.25), n('A4', 0.5),
        # dotted eighth+sixteenth adds rhythmic variety in clarinet too
    ])

    add_measure(part, 48, [
        n('C5', 1.0), n('D5', 0.5), n('E5', 1.5, tenuto=True),
    ], dyn='f')

    # ── Section IV: mm.49-64 - Walking Home (Ab major) ──
    add_measure(part, 49, [
        n('Ab4', 1.0, accent=True), n('Bb4', 0.5),
        n('C5', 1.0), n('Eb5', 0.5),
    ], dyn='f', expression_text='largamente',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=80))

    add_measure(part, 50, [
        n('F5', 1.5), n('Eb5', 0.5), n('Db5', 0.5), n('C5', 0.5),
    ])

    add_measure(part, 51, [
        n('Bb4', 1.0), n('C5', 0.5), n('Eb5', 1.0), n('Db5', 0.5),
    ])

    add_measure(part, 52, [
        n('C5', 1.5, tenuto=True), r(0.5), n('Eb5', 0.5), n('F5', 0.5),
    ])

    # m.53-56: Emotional peak - push higher for range
    add_measure(part, 53, [
        n('Ab5', 1.0, accent=True), n('Bb5', 0.5),  # push to Bb5 for extended range
        n('Ab5', 0.5), n('F5', 0.5), n('Eb5', 0.5),
    ], dyn='ff')

    add_measure(part, 54, [
        n('F5', 1.0), n('Eb5', 0.5), n('Db5', 1.0), n('C5', 0.5),
    ])

    add_measure(part, 55, [
        n('Bb4', 1.0), n('Ab4', 0.5), n('Bb4', 1.0), n('C5', 0.5),
    ])

    add_measure(part, 56, [
        n('Ab4', 1.5, tenuto=True), r(1.5),
    ])

    # m.57-60: Winding down
    add_measure(part, 57, [
        n('Db5', 1.0), n('C5', 0.5), n('Bb4', 1.0), n('Ab4', 0.5),
    ], dyn='mf')

    add_measure(part, 58, [
        n('Bb4', 1.0), n('C5', 0.5), n('Eb5', 1.0), n('Db5', 0.5),
    ])

    add_measure(part, 59, [
        n('C5', 1.0), n('Bb4', 0.5), n('Ab4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 60, [
        n('Ab4', 1.5), r(1.5),
    ])

    # m.61-64: Transition back to F
    add_measure(part, 61, [
        n('Bb4', 1.0), n('Ab4', 0.5), n('G4', 1.0), n('F4', 0.5),
    ])

    add_measure(part, 62, [
        n('Eb4', 0.5), n('F4', 0.5), n('G4', 0.5),
        n('Ab4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 63, [
        n('F4', 1.0), n('E4', 0.5), n('F4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 64, [
        n('A4', 1.5, tenuto=True), r(1.5),
    ], dyn='mp')

    # ── Section V: mm.65-80 - Alone Again (mostly tacet, piano solo) ──
    # Tacet mm.65-72
    for m_num in range(65, 73):
        kwargs = {}
        if m_num == 65:
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=69
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # m.73-76: Final ghostly appearance
    add_measure(part, 73, [
        r(1.5), n('F4', 0.5), n('G4', 0.5), n('A4', 0.5),
    ], dyn='pp')

    add_measure(part, 74, [
        n('Bb4', 1.5, tenuto=True), n('A4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 75, [
        n('F4', 1.5), r(1.5),
    ])

    add_measure(part, 76, [
        r(3.0),
    ])

    # m.77-80: Tacet to end
    for m_num in range(77, 81):
        kwargs = {}
        if m_num == 80:
            elements = [r(3.0)]
        else:
            elements = [r(3.0)]
        add_measure(part, m_num, elements, **kwargs)


# ── Piano Part ───────────────────────────────────────────────────────────

def build_piano(part):
    """Build the piano part (80 measures)."""

    # ── Section I: mm.1-16 - Morning, piano alone ──

    # m.1-4: F - Fadd9 - Bb - F/C
    add_measure(part, 1, [
        ch(['F2', 'C3', 'F3', 'A3'], 1.5, staccato=True),  # F chord block
        n('C3', 0.5, staccato=True), n('F3', 0.5), n('A3', 0.5),
    ], ts=meter.TimeSignature('6/8'),
        ks=key.Key('F'),
        tempo_mark=tempo.MetronomeMark(
            referent=duration.Duration(1.5), number=72,
            text="Andante pastorale"
        ),
        dyn='pp', expression_text='dolce')

    add_measure(part, 2, [
        ch(['F2', 'C3', 'G3', 'A3'], 1.5, staccato=True),  # Fadd9 block
        n('G3', 0.5, staccato=True), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 3, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 1.5, staccato=True),  # Bb block
        n('F3', 0.5, staccato=True), n('Bb3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 4, [
        ch(['C3', 'F3', 'A3'], 1.5, staccato=True),  # F/C block
        n('F3', 0.5, staccato=True), n('A3', 0.5), n('C4', 0.5),
    ])

    # m.5-8: Dm7 - Bbmaj7 - C7sus4 - C7
    add_measure(part, 5,
        piano_dotted_pattern('D2', 'A2', 'F3'),
        dyn='mp')  # Dm7 with dotted rhythm

    add_measure(part, 6,
        piano_mixed_rhythm('Bb2', 'F3', 'A3', 'D4'))  # Bbmaj7

    add_measure(part, 7,
        piano_arpeggio_varied('C3', 'F3', 'Bb3', 'E4'))  # C7sus4

    add_measure(part, 8, [
        n('C3', 1.5),  # dotted quarter
        n('E3', 0.75), n('G3', 0.25), n('Bb3', 0.5),  # dotted eighth + sixteenth + eighth
    ], dyn='p')  # C7, dim back to p

    # m.9-12: F - Gm7 - Am7 - Bbmaj7
    add_measure(part, 9, [
        ch(['F2', 'C3', 'F3', 'A3'], 1.5),  # F block
        n('C3', 1.0), n('A3', 0.5),
    ])

    add_measure(part, 10, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 block
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 11, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7 block
        n('C3', 1.0), n('G3', 0.5),
    ])

    add_measure(part, 12, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 block
        n('D3', 0.75), n('F3', 0.25), n('A3', 0.5),
    ])

    # m.13-16: Dm7 - Gm7 - Csus4 - C7
    add_measure(part, 13, [
        ch(['D2', 'A2', 'C3', 'F3'], 1.5),  # Dm7 block
        n('A2', 0.5), n('C3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 14, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.0),  # Gm7 block, quarter
        n('Bb2', 0.5),
        n('D3', 0.75), n('F3', 0.25), n('D3', 0.5),
    ])

    add_measure(part, 15, [
        ch(['C3', 'F3', 'G3', 'Bb3'], 1.5),  # Csus4 block
        n('F3', 1.0), n('G3', 0.5),
    ])

    add_measure(part, 16, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7 block
        n('E3', 0.5), n('G3', 1.0),
    ])

    # ── Section II: mm.17-28 - The Door Opens ──
    # Piano continues arpeggiated accompaniment under clarinet

    # m.17-20: Fmaj7 - Gm9 - Am7 - Bbadd9
    add_measure(part, 17,
        piano_dotted_pattern('F2', 'C3', 'E3'),
        dyn='mp')  # Fmaj7 dotted

    add_measure(part, 18,
        piano_mixed_rhythm('G2', 'Bb2', 'D3', 'A3'))  # Gm9

    add_measure(part, 19,
        piano_waltz_6_8('A2', 'E3', 'G3'))  # Am7

    add_measure(part, 20,
        piano_arpeggio_varied('Bb2', 'F3', 'Bb3', 'C4'))  # Bbadd9

    # m.21-24: C7 - Dm7 - Bbmaj7 - Csus4-C
    add_measure(part, 21, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7 block chord
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])  # cresc

    add_measure(part, 22, [
        ch(['D2', 'A2', 'C3', 'F3'], 1.5),  # Dm7 block chord
        n('A2', 0.5), n('C3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 23, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 block chord
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 24, [
        ch(['C3', 'F3', 'G3', 'Bb3'], 1.5),  # Csus4 block chord
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7 block chord
    ], dyn='mf')

    # m.25-28: Fmaj7 - Dm9 - Bbmaj7 - C7sus4
    add_measure(part, 25, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7 block
        n('C3', 0.5), n('E3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 26, [
        ch(['D2', 'A2', 'C3', 'E3'], 1.5),  # Dm9 block
        n('A2', 0.5), n('C3', 0.5), n('E3', 0.5),
    ])

    add_measure(part, 27, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 block
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 28, [
        ch(['C3', 'F3', 'G3', 'Bb3'], 1.5),  # C7sus4 block
        n('F3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ], dyn='mp')

    # ── Section III: mm.29-48 - Conversation ──

    # m.29-32: F - Am7 - Dm7 - Bbmaj7
    add_measure(part, 29, [
        ch(['F2', 'A2', 'C3', 'E3'], 0.75),  # Fmaj7 chord, dotted eighth
        n('F3', 0.25), n('A3', 0.5),          # sixteenth + eighth
        n('C4', 1.0), n('A3', 0.5),           # quarter + eighth
    ], dyn='mp',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=76))

    add_measure(part, 30, [
        # Piano response when clarinet rests
        n('E3', 0.75), n('A3', 0.25), n('C4', 0.5),  # dotted eighth + sixteenth + eighth
        n('E4', 1.0, accent=True), n('C4', 0.5),
    ])

    add_measure(part, 31, [
        ch(['D2', 'A2', 'C3', 'F3'], 1.5),  # Dm7 sustained (with 7th)
        r(1.5),  # clarinet plays
    ])

    add_measure(part, 32,
        piano_mixed_rhythm('Bb2', 'D3', 'F3', 'A3'))  # Bbmaj7

    # m.33-36: Gm9 - C9 - Fmaj7 - Am7
    add_measure(part, 33, [
        ch(['G2', 'Bb2', 'D3', 'F3', 'A3'], 1.5),  # Gm9 block (5 notes!)
        n('Bb2', 0.5), n('D3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 34, [
        ch(['C3', 'E3', 'G3', 'Bb3', 'D4'], 1.5),  # C9 block (5 notes!)
        n('E3', 0.5), n('Bb3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 35, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7 block
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 36, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7 block
        n('E3', 0.5), n('G3', 0.5), n('A3', 0.5),
    ], dyn='mf')

    # m.37-40: Dm - Gm7 - A7 - Dm (D minor excursion)
    add_measure(part, 37, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.5),
        n('E3', 0.75), n('F3', 0.25), n('A3', 0.5),  # dotted eighth+sixteenth+eighth
    ], dyn='p')

    add_measure(part, 38,
        piano_waltz_6_8('G2', 'Bb2', 'F3'))  # Gm7 waltz

    add_measure(part, 39, [
        n('A2', 0.75), n('C#3', 0.25), n('E3', 0.5),  # dotted eighth+sixteenth+eighth
        n('G3', 1.0), n('E3', 0.5),  # quarter + eighth
    ])  # A7

    add_measure(part, 40,
        piano_dotted_pattern('D2', 'A2', 'D3'),
        dyn='pp')  # Dm

    # m.41-44: Dm7 - G7 - C7 - Fmaj7
    add_measure(part, 41,
        piano_mixed_rhythm('D2', 'A2', 'C3', 'F3'))  # Dm7

    add_measure(part, 42, [
        n('G2', 1.0), n('B2', 0.5),  # quarter + eighth
        n('D3', 0.75), n('F3', 0.25), n('D3', 0.5),  # dotted eighth + sixteenth + eighth
    ])  # G7

    add_measure(part, 43, [
        n('C3', 0.75), n('E3', 0.25), n('Bb3', 0.5),  # dotted eighth + sixteenth + eighth
        n('E3', 0.5), n('G3', 1.0),  # eighth + quarter
    ])  # C7

    add_measure(part, 44,
        piano_arpeggio_varied('F2', 'A2', 'C3', 'E3'),
        dyn='mf')

    # m.45-48: Bbmaj7 - Am7 - Gm9 - C9 (building, all 7th/9th chords)
    add_measure(part, 45, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7
        n('Bb3', 0.75), n('A3', 0.25), n('F3', 0.5),
    ])

    add_measure(part, 46, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7
        n('A3', 0.5), n('G3', 1.0),
    ])

    add_measure(part, 47, [
        ch(['G2', 'Bb2', 'D3', 'F3', 'A3'], 1.5),  # Gm9
        n('G3', 0.75), n('F3', 0.25), n('D3', 0.5),
    ])

    add_measure(part, 48, [
        ch(['C3', 'E3', 'G3', 'Bb3', 'D4'], 1.5),  # C9
        ch(['C3', 'E3', 'Bb3'], 1.0),
        r(0.5),
    ], dyn='f')

    # ── Section IV: mm.49-64 - Walking Home (Ab major) ──

    add_measure(part, 49, [
        ch(['Ab2', 'Eb3', 'Ab3', 'C4', 'G4'], 1.5),  # Abmaj7 w/5th on top
        n('Eb3', 0.5), n('Ab3', 0.5), n('C4', 0.5),
    ], dyn='f', expression_text='largamente',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=80))

    add_measure(part, 50, [
        n('Bb2', 1.0), n('Db3', 0.5),  # quarter + eighth
        n('F3', 0.75), n('Ab3', 0.25), n('F3', 0.5),  # dotted eighth+sixteenth+eighth
    ])  # Bbm7

    add_measure(part, 51, [
        n('Eb2', 0.75), n('G2', 0.25), n('Bb2', 0.5),  # dotted eighth+sixteenth+eighth
        n('Db3', 1.0), n('Bb2', 0.5),  # quarter + eighth
    ])  # Eb7

    add_measure(part, 52, [
        ch(['Ab2', 'C3', 'Eb3', 'G3'], 1.5),  # Abmaj7 block
        n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5),
    ])

    # m.53-56: Emotional peak
    add_measure(part, 53, [
        ch(['F2', 'Ab2', 'C3', 'Eb3'], 1.5),  # Fm7
        n('F3', 0.75), n('Ab3', 0.25), n('C4', 0.5),  # dotted eighth+sixteenth+eighth
    ], dyn='ff')

    add_measure(part, 54, [
        ch(['Db2', 'F2', 'Ab2', 'C3'], 1.5),  # Dbmaj7
        n('Db3', 0.5), n('F3', 1.0),  # eighth + quarter
    ])

    add_measure(part, 55, [
        n('Eb2', 1.0), n('Bb2', 0.5),  # quarter + eighth
        n('Db3', 0.75), n('G3', 0.25), n('Db3', 0.5),  # dotted eighth+sixteenth+eighth
    ])  # Eb7

    add_measure(part, 56, [
        ch(['Ab2', 'Eb3', 'Ab3', 'C4'], 1.5),  # Ab block
        n('Eb3', 1.0), n('Ab3', 0.5),
    ])

    # m.57-60: Db - Eb - Cm7 - Fm
    add_measure(part, 57, [
        ch(['Db2', 'Ab2', 'Db3', 'F3'], 1.5),
        n('Ab2', 0.75), n('Db3', 0.25), n('F3', 0.5),  # dotted eighth+sixteenth+eighth
    ], dyn='mf')

    add_measure(part, 58, [
        n('Eb2', 1.0), n('G2', 0.5),  # quarter + eighth
        n('Bb2', 0.75), n('Eb3', 0.25), n('Bb2', 0.5),  # dotted eighth+sixteenth+eighth
    ])  # Eb7

    add_measure(part, 59, [
        n('C2', 0.75), n('Eb2', 0.25), n('G2', 0.5),  # dotted eighth+sixteenth+eighth
        n('Bb2', 1.0), n('G2', 0.5),  # quarter + eighth
    ])  # Cm7

    add_measure(part, 60, [
        ch(['F2', 'Ab2', 'C3', 'Eb3'], 1.5),  # Fm7 block
        n('Ab2', 1.0), n('C3', 0.5),
    ])

    # m.61-64: Bbm7 - Eb7 - Db - C7 (pivot back)
    add_measure(part, 61, [
        n('Bb1', 1.0), n('Db2', 0.5),  # lower Bb1 for extended bass range
        n('F2', 0.75), n('Ab2', 0.25), n('F2', 0.5),
    ])  # Bbm7

    add_measure(part, 62, [
        n('Eb2', 0.75), n('G2', 0.25), n('Bb2', 0.5),
        n('Db3', 1.0), n('Bb2', 0.5),
    ])  # Eb7

    add_measure(part, 63, [
        ch(['Db2', 'F2', 'Ab2', 'C3'], 1.5),  # Dbmaj7 (add 7th)
        n('F2', 0.75), n('Ab2', 0.25), n('Db3', 0.5),
    ])  # Dbmaj7

    add_measure(part, 64, [
        n('C2', 0.75), n('E2', 0.25), n('G2', 0.5),  # dotted eighth+sixteenth+eighth
        n('Bb2', 1.0), n('E2', 0.5),  # quarter + eighth
    ], dyn='mp')  # C7 pivot

    # ── Section V: mm.65-80 - Alone Again (piano solo return) ──

    # m.65-68: F - Fadd9 - Bb - F/C (ostinato returns, enriched)
    add_measure(part, 65, [
        ch(['F2', 'C3', 'F3', 'A3'], 1.5, staccato=True),  # F block
        n('C3', 0.5, staccato=True), n('F3', 0.5), n('A3', 0.5),
    ], dyn='p',
        tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=69))

    add_measure(part, 66, [
        ch(['F2', 'C3', 'G3', 'A3'], 1.5, staccato=True),  # Fadd9 block
        n('G3', 0.5, staccato=True), n('A3', 0.5), n('C4', 0.5),
    ])

    add_measure(part, 67, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 1.5, staccato=True),  # Bb block
        n('F3', 0.5, staccato=True), n('Bb3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 68, [
        ch(['C3', 'F3', 'A3'], 1.5, staccato=True),  # F/C block
        n('F3', 0.5, staccato=True), n('A3', 0.5), n('C4', 0.5),
    ])

    # m.69-72: Dm9 - Bbmaj7 - Am7 - Gm7
    add_measure(part, 69, [
        ch(['D2', 'A2', 'C3', 'E3'], 1.5),  # Dm9 block
        n('A2', 1.0), n('E3', 0.5),
    ], dyn='pp')

    add_measure(part, 70, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 block
        n('D3', 1.0), n('A3', 0.5),
    ])

    add_measure(part, 71, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7 block
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 72, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 block
        n('Bb2', 1.0), n('F3', 0.5),
    ], expression_text='come un ricordo')

    # m.73-76: Fmaj7 - Dm7 - Bb - C7sus4 (clarinet melody in piano RH)
    # Piano takes over the clarinet motif in the right hand
    add_measure(part, 73, [
        n('F2', 0.5, staccato=True), n('A2', 0.5), n('E3', 0.5),
        # RH melody: F4-G4-A4 as triplet eighths (1/3 QL each)
        n('F4', 1.0/3), n('G4', 1.0/3), n('A4', 1.0/3),  # triplet = 1.0 QL
        n('C5', 0.5),  # eighth
    ])

    add_measure(part, 74, [
        n('D2', 0.5, staccato=True), n('A2', 0.5), n('F3', 0.5),
        n('Bb4', 1.0, tenuto=True), n('A4', 0.5),
    ])

    add_measure(part, 75, [
        n('Bb2', 0.5, staccato=True), n('D3', 0.5), n('F3', 0.5),
        n('G4', 1.0), n('F4', 0.5),
    ])

    add_measure(part, 76, [
        n('C3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
        n('E4', 1.0), n('F4', 0.5, tenuto=True),
    ])

    # m.77-80: Dm9 - Bbmaj7 - Csus4 - Fadd9 (unresolved ending)
    add_measure(part, 77,
        piano_dotted_pattern('D2', 'A2', 'E3'),
        dyn='ppp', expression_text='morendo')

    add_measure(part, 78,
        piano_waltz_6_8('Bb2', 'D3', 'A3'))  # Bbmaj7

    add_measure(part, 79, [
        n('C3', 1.0), n('F3', 0.5),  # quarter + eighth
        n('G3', 0.5), n('Bb3', 1.0),  # eighth + quarter
    ])  # Csus4

    add_measure(part, 80, [
        ch(['F2', 'C3', 'F3', 'G3', 'A3'], 3.0, fermata=True),
    ])  # Fadd9 with fermata


# ── Add Spanners (Hairpins) ──────────────────────────────────────────────

def add_hairpins(score):
    """Add crescendo and diminuendo hairpins to the score."""
    piano = None
    clarinet = None
    for p in score.parts:
        if 'Piano' in (p.partName or ''):
            piano = p
        elif 'Clarinet' in (p.partName or ''):
            clarinet = p

    # Helper: get a note/rest in a measure for attaching spanners
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
        # (part, start_m, end_m, type)
        # Piano hairpins
        ('piano', 8, 8, 'diminuendo'),       # m.8 diminuendo
        ('piano', 13, 16, 'crescendo'),       # m.13 crescendo to m.16
        ('piano', 21, 23, 'crescendo'),       # m.21 crescendo
        ('piano', 25, 27, 'diminuendo'),      # m.25 diminuendo
        ('piano', 33, 35, 'crescendo'),       # m.33 crescendo
        ('piano', 41, 43, 'crescendo'),       # m.41 crescendo
        ('piano', 45, 47, 'crescendo'),       # m.45 crescendo
        ('piano', 56, 56, 'diminuendo'),      # m.56 diminuendo
        ('piano', 60, 60, 'diminuendo'),      # m.60 diminuendo
        ('piano', 64, 64, 'diminuendo'),      # m.64 dim
        # Clarinet hairpins
        ('clarinet', 37, 39, 'diminuendo'),   # m.37 diminuendo
        ('clarinet', 41, 43, 'crescendo'),    # m.41 crescendo
        ('clarinet', 45, 47, 'crescendo'),    # m.45 crescendo
        ('clarinet', 56, 56, 'diminuendo'),   # m.56 diminuendo
        ('clarinet', 60, 60, 'diminuendo'),   # m.60 dim
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
