#!/usr/bin/env python3
"""Generate 'Farine et Lavande' -- Clarinet in Bb + Piano.

First love at 17, summer in a French village, working at a bakery.

6/8 time, F major. ~72 measures.
The clarinet is a Bb transposing instrument -- we write at concert pitch
and music21 handles the transposition to written pitch in MusicXML.

Structure:
  A  (mm.1-16)   -- "Avant l'aube" (Before dawn) - Piano alone, pre-dawn bakery
  B  (mm.17-32)  -- "Elle entre" (She walks in) - Clarinet enters, tentative
  C  (mm.33-48)  -- "La conversation" - Call and response, growing warmth
  D  (mm.49-60)  -- "L'apres-midi" (The afternoon) - Walking together, D minor -> Bb
  E  (mm.61-72)  -- "Le soir" (Evening) - Return to F, bittersweet close
"""

from music21 import (
    stream, note, chord, key, meter, tempo, instrument,
    expressions, dynamics, duration, articulations, tie, layout, bar,
)
from music21.dynamics import Crescendo, Diminuendo
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "score.musicxml")

# ── Helpers ──────────────────────────────────────────────────────────────

def n(pitch, dur, **kwargs):
    """Note. dur in quarter-lengths (dotted quarter = 1.5, eighth = 0.5)."""
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
    return nt


def r(dur):
    """Rest. dur in quarter-lengths."""
    return note.Rest(quarterLength=dur)


def ch(pitches, dur, **kwargs):
    """Chord."""
    c = chord.Chord(pitches, quarterLength=dur)
    if kwargs.get('staccato'):
        c.articulations.append(articulations.Staccato())
    if kwargs.get('fermata'):
        c.expressions.append(expressions.Fermata())
    if kwargs.get('accent'):
        c.articulations.append(articulations.Accent())
    return c


def add_measure(part, m_num, elements, ts=None, ks=None, tempo_mark=None,
                dyn=None, expression_text=None):
    """Add a measure to a part."""
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


# ── Piano accompaniment patterns ────────────────────────────────────────

def arp_6_8(bass, mid, top):
    """Standard 6/8 broken chord: bass-mid-top bass-mid-top."""
    return [n(bass, 0.5), n(mid, 0.5), n(top, 0.5),
            n(bass, 0.5), n(mid, 0.5), n(top, 0.5)]


def arp_varied(bass, mid, top, high):
    """Wider arpeggio: bass-mid-top-mid-high-top."""
    return [n(bass, 0.5), n(mid, 0.5), n(top, 0.5),
            n(mid, 0.5), n(high, 0.5), n(top, 0.5)]


def dotted_bass(bass, mid, top):
    """Dotted quarter bass + quarter-eighth upper."""
    return [n(bass, 1.5), n(mid, 1.0), n(top, 0.5)]


def waltz_68(bass, mid, top):
    """Waltz-like: dotted quarter bass, quarter+eighth upper."""
    return [n(bass, 1.5), n(mid, 1.0), n(top, 0.5)]


def rocking(bass, p1, p2, bridge=None):
    """Gentle rocking: bass-bridge-p1-p2 or bass-p1-p2 repeated.
    If bridge is given, adds a middle note to reduce leaps."""
    if bridge:
        return [n(bass, 0.5, staccato=True), n(bridge, 0.5), n(p1, 0.5),
                n(p2, 0.5), n(p1, 0.5), n(bass, 0.5, staccato=True)]
    return [n(bass, 0.5, staccato=True), n(p1, 0.5), n(p2, 0.5),
            n(bass, 0.5, staccato=True), n(p1, 0.5), n(p2, 0.5)]


# ══════════════════════════════════════════════════════════════════════════
# Section A: "Avant l'aube" (mm.1-16) -- Piano alone
# Pre-dawn bakery. Flour dust in lamplight. Repetitive work, quiet joy.
# F major, gentle 6/8, mostly soft.
# ══════════════════════════════════════════════════════════════════════════

def build_piano(part):
    # -- Section A: mm.1-16 --

    # m.1-4: F - Dm7 - Bbmaj7 - C7
    # A simple rocking figure, like kneading dough
    add_measure(part, 1,
        rocking('F2', 'A3', 'C4', bridge='C3'),
        ts=meter.TimeSignature('6/8'),
        ks=key.Key('F'),
        tempo_mark=tempo.MetronomeMark(
            referent=duration.Duration(1.5), number=66,
            text="Tranquillo"
        ),
        dyn='pp', expression_text='dolce, comme le matin')

    add_measure(part, 2,
        rocking('D2', 'A3', 'F3', bridge='A2'))  # Dm7

    add_measure(part, 3, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 block
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 4, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7 block
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    # m.5-8: F/A - Gm7 - Am7 - Bbmaj7
    # The rocking expands, a breath of morning air
    add_measure(part, 5, [
        ch(['A2', 'C3', 'F3', 'E3'], 1.5),  # Fmaj7/A
        n('C3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ], dyn='p')

    add_measure(part, 6, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 block
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 7, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7 block
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 8, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 block
        n('F3', 0.75), n('A3', 0.25), n('F3', 0.5),
    ])

    # m.9-12: Dm9 - Gm7 - C9 - Fmaj7
    # Growing warmth as the oven heats
    add_measure(part, 9, [
        ch(['D2', 'A2', 'C3', 'E3', 'F3'], 1.5),  # Dm9
        n('A2', 0.5), n('C3', 0.5), n('F3', 0.5),
    ], dyn='mp')

    add_measure(part, 10,
        waltz_68('G2', 'Bb2', 'F3'))  # Gm7

    add_measure(part, 11, [
        ch(['C3', 'E3', 'G3', 'Bb3', 'D4'], 1.5),  # C9
        n('E3', 0.5), n('Bb3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 12,
        arp_varied('F2', 'A2', 'C3', 'E3'))  # Fmaj7

    # m.13-16: Bb - Am7 - Gm7 - Csus4->C
    # Descending bass line, settling into the routine
    add_measure(part, 13, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 14,
        arp_6_8('A2', 'C3', 'G3'))  # Am7

    add_measure(part, 15, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7
        n('Bb2', 0.75), n('D3', 0.25), n('F3', 0.5),
    ])

    add_measure(part, 16, [
        ch(['C3', 'F3', 'G3', 'Bb3'], 1.5),  # Csus4
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7 resolving
    ], dyn='p')

    # ── Section B: mm.17-32 -- "Elle entre" ──
    # The bell above the door rings. She walks in.

    add_measure(part, 17, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7 block
        n('C3', 1.0), n('A3', 0.5),
    ], dyn='mp')  # supportive, under clarinet

    add_measure(part, 18, [
        ch(['Bb2', 'D3', 'F3', 'Ab3'], 1.5),  # Bb with Ab (borrowed from minor)
        n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5),
    ])

    add_measure(part, 19, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7 block
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 20, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    # m.21-24: Piano responds to clarinet's phrase
    add_measure(part, 21, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7
        n('A3', 0.75), n('G3', 0.25), n('F3', 0.5),  # descending answer
    ])

    add_measure(part, 22, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.5),  # Dm7
        n('A2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    add_measure(part, 23, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 24, [
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
        n('Bb3', 0.75), n('G3', 0.25), n('E3', 0.5),
    ])  # C7 arpeggiated with dotted figure

    # m.25-28: Second half of B, more confident
    add_measure(part, 25,
        arp_varied('F2', 'C3', 'F3', 'A3'),
        dyn='mf')

    add_measure(part, 26, [
        ch(['G2', 'Bb2', 'D3', 'F3', 'A3'], 1.5),  # Gm9
        n('Bb2', 0.5), n('D3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 27, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7
        n('C3', 0.75), n('E3', 0.25), n('G3', 0.5),
    ])

    add_measure(part, 28,
        dotted_bass('Bb2', 'F3', 'A3'))  # Bbmaj7

    # m.29-32: Winding phrase to close section B
    add_measure(part, 29, [
        ch(['C3', 'E3', 'G3', 'Bb3', 'D4'], 1.5),  # C9
        n('E3', 0.5), n('G3', 0.5), n('D4', 0.5),
    ])

    add_measure(part, 30, [
        n('D2', 0.75), n('A2', 0.25), n('F3', 0.5),
        n('E3', 0.5), n('C3', 0.5), n('A2', 0.5),
    ], dyn='mp')  # Dm7 descending

    add_measure(part, 31, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),
        n('G3', 1.0), n('F3', 0.5),
    ])  # Bbmaj7

    add_measure(part, 32, [
        ch(['C3', 'F3', 'G3', 'Bb3'], 1.5),  # Csus4
        n('E3', 1.0), n('G3', 0.5),           # -> C resolution
    ], dyn='p')

    # ── Section C: mm.33-48 -- "La conversation" ──
    # Getting to know each other. Call and response between clarinet and piano.

    add_measure(part, 33, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7
        n('A3', 0.5), n('C4', 0.5), n('E4', 0.5),  # piano rising answer
    ], dyn='mp',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=72))

    add_measure(part, 34, [
        n('D4', 1.0, accent=True), n('C4', 0.5),  # piano melody response
        n('Bb3', 0.5), n('A3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 35,
        arp_varied('D2', 'A2', 'D3', 'F3'))  # Dm7, under clarinet

    add_measure(part, 36, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7
        n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ])

    # m.37-40: Piano takes the melody, clarinet sustains
    add_measure(part, 37, [
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5),
        n('D4', 0.75), n('C4', 0.25), n('Bb3', 0.5),
    ], dyn='mf')  # Piano melody

    add_measure(part, 38, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 0.5), n('G3', 0.5), n('Bb3', 0.5),
    ])

    add_measure(part, 39, [
        ch(['F2', 'A2', 'C3', 'E3'], 1.5),  # Fmaj7
        n('C3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 40,
        arp_varied('Bb2', 'D3', 'F3', 'A3'))  # Bbmaj7

    # m.41-44: Building intensity -- heart beats faster
    add_measure(part, 41, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7
        n('E3', 0.75), n('G3', 0.25), n('C4', 0.5),
    ], dyn='mf')

    add_measure(part, 42, [
        ch(['D2', 'A2', 'D3', 'F3', 'A3'], 1.5),  # Dm9
        n('A2', 0.5), n('D3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 43, [
        ch(['G2', 'Bb2', 'D3', 'F3', 'A3'], 1.5),  # Gm9
        n('G3', 0.75), n('F3', 0.25), n('D3', 0.5),
    ])

    add_measure(part, 44, [
        ch(['C3', 'E3', 'G3', 'Bb3', 'D4'], 1.5),  # C9
        ch(['C3', 'E3', 'Bb3'], 1.0),
        r(0.5),
    ], dyn='f')

    # m.45-48: Peak of C -- the laugh, the shared flour-dusted hands
    add_measure(part, 45, [
        ch(['F2', 'C3', 'E3', 'A3', 'C4'], 1.5),  # Fmaj7
        n('F3', 0.5), n('A3', 0.5), n('C4', 0.5),
    ], dyn='f')

    add_measure(part, 46, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7 (add 7th)
        n('D3', 0.75), n('F3', 0.25), n('Bb3', 0.5),
    ])

    add_measure(part, 47, [
        n('A2', 0.75), n('C3', 0.25), n('E3', 0.5),
        n('G3', 1.0), n('E3', 0.5),
    ])  # Am7

    add_measure(part, 48, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('G3', 0.75), n('Bb3', 0.25), n('E3', 0.5),
    ], dyn='mf')

    # ── Section D: mm.49-60 -- "L'apres-midi" ──
    # Walking through the village together. D minor shading, then Bb warmth.

    add_measure(part, 49, [
        ch(['D2', 'A2', 'D3', 'F3'], 1.5),  # Dm
        n('A2', 0.5), n('D3', 0.5), n('F3', 0.5),
    ], dyn='mp', expression_text='un poco rubato',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=69))

    add_measure(part, 50,
        waltz_68('G2', 'Bb2', 'D3'))  # Gm

    add_measure(part, 51, [
        n('A2', 0.75), n('C#3', 0.25), n('E3', 0.5),  # A7
        n('G3', 1.0), n('E3', 0.5),
    ])

    add_measure(part, 52, [
        ch(['D2', 'A2', 'D3', 'F3', 'B3'], 1.5),  # Dm6 (B natural = dorian color)
        n('F3', 0.5), n('A3', 1.0, tenuto=True),
    ])

    # m.53-56: Shift to Bb major -- sunlight through plane trees
    add_measure(part, 53, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ], dyn='mf')

    add_measure(part, 54, [
        ch(['Eb2', 'G2', 'Bb2', 'D3'], 1.5),  # Ebmaj7
        n('G#2', 0.5), n('B2', 0.5), n('D3', 0.5),  # chromatic passing (Ab-B) to next bar
    ])

    add_measure(part, 55, [
        ch(['F2', 'A2', 'C3', 'Eb3'], 1.5),  # F7 (V7/Bb)
        n('A2', 0.5), n('C3', 0.5), n('Eb3', 0.5),
    ])

    add_measure(part, 56, [
        ch(['Bb2', 'D3', 'F3', 'Bb3'], 1.5),  # Bb
        n('D3', 1.0), n('F3', 0.5),
    ])

    # m.57-60: Transitioning back to F
    add_measure(part, 57, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7
        n('Bb2', 0.75), n('D3', 0.25), n('F3', 0.5),
    ], dyn='mp')

    add_measure(part, 58, [
        ch(['A2', 'C3', 'E3', 'G3'], 1.5),  # Am7
        n('C3', 0.5), n('E3', 0.5), n('G3', 0.5),
    ])

    add_measure(part, 59, [
        ch(['Bb2', 'D3', 'F3', 'A3'], 1.5),  # Bbmaj7
        n('D3', 0.5), n('F3', 0.5), n('A3', 0.5),
    ])

    add_measure(part, 60, [
        n('C3', 0.75), n('E3', 0.25), n('G3', 0.5),
        n('Bb3', 1.0), n('G3', 0.5),
    ], dyn='p')  # C7

    # ── Section E: mm.61-72 -- "Le soir" ──
    # Evening. She leaves. The bakery is quiet again.

    add_measure(part, 61,
        rocking('F2', 'A3', 'C4', bridge='C3'),
        dyn='p',
        tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=63,
                                        text="Lento"))

    add_measure(part, 62,
        rocking('Bb1', 'D3', 'F3', bridge='F2'))  # Bb -- lower bass for range

    add_measure(part, 63, [
        ch(['G2', 'Bb2', 'D3', 'F3'], 1.5),  # Gm7
        n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
    ])

    add_measure(part, 64, [
        ch(['C3', 'E3', 'G3', 'Bb3'], 1.5),  # C7
        n('E3', 1.0), n('G3', 0.5),
    ])

    # m.65-68: Piano echoes the clarinet's opening phrase
    add_measure(part, 65, [
        n('F2', 0.5, staccato=True), n('A2', 0.5), n('C3', 0.5),
        n('F4', 1.0), n('G4', 0.5),  # echo of clarinet motif
    ], dyn='pp', expression_text='come un ricordo')

    add_measure(part, 66, [
        n('D2', 0.5, staccato=True), n('A2', 0.5), n('F3', 0.5),
        n('A4', 1.0, tenuto=True), n('G4', 0.5),
    ])

    add_measure(part, 67, [
        n('Bb2', 0.5, staccato=True), n('D3', 0.5), n('F3', 0.5),
        n('F4', 1.0), n('E4', 0.5),
    ])

    add_measure(part, 68, [
        ch(['C3', 'F3', 'G3', 'Bb3'], 1.5),  # Csus4
        n('E3', 1.0), n('F3', 0.5),  # resolution
    ])

    # m.69-72: Final measures -- morning will come again
    add_measure(part, 69, [
        ch(['Db2', 'F2', 'Ab2', 'C3'], 1.5),  # Dbmaj7 -- Neapolitan color
        n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5),
    ], dyn='ppp', expression_text='morendo')

    add_measure(part, 70, [
        ch(['Bb1', 'D2', 'F2', 'A2'], 1.5),  # Bbmaj7 -- low voicing for depth
        n('D3', 1.0), n('A3', 0.5),
    ])

    add_measure(part, 71, [
        n('C2', 1.0), n('E2', 0.5),  # C7 bass, low
        n('G2', 0.5), n('Bb2', 1.0),
    ])  # C7 (was Csus4)

    add_measure(part, 72, [
        ch(['F2', 'C3', 'F3', 'G3', 'A3'], 3.0, fermata=True),
    ])  # Fadd9 -- unresolved, the summer isn't over yet


# ══════════════════════════════════════════════════════════════════════════
# Clarinet Part (concert pitch -- music21 transposes for Bb clarinet)
# ══════════════════════════════════════════════════════════════════════════

def build_clarinet(part):

    # ── Section A: mm.1-16 -- Tacet (piano solo) ──
    for m_num in range(1, 17):
        kwargs = {}
        if m_num == 1:
            kwargs['ts'] = meter.TimeSignature('6/8')
            kwargs['ks'] = key.Key('F')
            kwargs['tempo_mark'] = tempo.MetronomeMark(
                referent=duration.Duration(1.5), number=66,
                text="Tranquillo"
            )
        add_measure(part, m_num, [r(3.0)], **kwargs)

    # ── Section B: mm.17-32 -- "Elle entre" ──
    # Clarinet enters with a simple, shy melody. Like looking up from work.

    # m.17-18: First motif -- stepwise F4-G4-A4, pause, Bb4 sigh
    add_measure(part, 17, [
        r(1.5),
        n('F4', 0.5), n('G4', 0.5), n('A4', 0.5),
    ], dyn='p', expression_text='timidamente')

    add_measure(part, 18, [
        n('Bb4', 1.5, tenuto=True),
        n('A4', 1.0), n('G4', 0.5),
    ])

    # m.19-20: Descending answer -- shy retreat
    add_measure(part, 19, [
        n('F4', 1.0), n('E4', 0.5), n('Eb4', 0.5), n('D4', 0.5), n('C4', 0.5),
        # Eb4 = chromatic passing tone, a touch of blue
    ])

    add_measure(part, 20, [
        n('F4', 1.5, tenuto=True), r(1.5),
    ])

    # m.21-24: Second attempt, reaching a bit higher
    add_measure(part, 21, [
        r(1.5),
        n('A4', 0.5), n('Bb4', 0.5), n('C5', 0.5),
    ], dyn='mp')

    add_measure(part, 22, [
        n('D5', 1.0, tenuto=True), n('C#5', 0.5),  # C# = chromatic upper neighbor
        n('C5', 0.5), n('Bb4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 23, [
        n('A4', 1.5), n('G4', 1.0), n('F4', 0.5),
    ])

    add_measure(part, 24, [
        n('G4', 1.5, tenuto=True), r(1.5),
    ])

    # m.25-28: Growing confidence, longer phrases
    add_measure(part, 25, [
        n('F4', 0.5), n('A4', 0.5), n('C5', 0.5),
        n('D5', 0.75), n('C5', 0.25), n('Bb4', 0.5),
    ], dyn='mf')

    add_measure(part, 26, [
        n('C5', 1.0, accent=True), n('Bb4', 0.5),
        n('A4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 27, [
        n('A4', 0.5), n('Bb4', 0.5), n('C5', 0.5),
        n('D5', 1.5, tie_start=True),
    ])

    add_measure(part, 28, [
        n('D5', 0.5, tie_stop=True), n('C5', 0.5), n('Bb4', 0.5),
        n('A4', 1.0), r(0.5),
    ], dyn='mp')

    # m.29-32: Closing the section, settling
    add_measure(part, 29, [
        n('G4', 1.0), n('A4', 0.5),
        n('Bb4', 1.0), n('C5', 0.5),
    ])

    add_measure(part, 30, [
        n('D5', 0.75), n('C5', 0.25), n('A4', 0.5),
        n('G4', 1.0, tenuto=True), r(0.5),
    ])

    add_measure(part, 31, [
        n('F4', 1.0), n('A4', 0.5),
        n('Bb4', 1.5, tenuto=True),
    ])

    add_measure(part, 32, [
        n('A4', 1.5), r(1.5),
    ], dyn='p')

    # ── Section C: mm.33-48 -- "La conversation" ──
    # Call and response. She says something, he answers. The melody weaves.

    add_measure(part, 33, [
        n('C5', 0.5), n('D5', 0.5), n('E5', 0.5),
        n('F5', 1.0, accent=True), n('E5', 0.5),
    ], dyn='mf',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=72))

    add_measure(part, 34, [
        n('D5', 1.5), r(1.5),  # rest for piano answer
    ])

    add_measure(part, 35, [
        r(1.5),
        n('A4', 0.5), n('Bb4', 0.5), n('C5', 0.5),  # clarinet picks back up
    ])

    add_measure(part, 36, [
        n('D5', 0.75), n('C5', 0.25), n('Bb4', 0.5),
        n('A4', 1.0, tenuto=True), n('G4', 0.5),
    ])

    # m.37-40: Piano leads, clarinet sustains / comments
    add_measure(part, 37, [
        n('F4', 1.5, tie_start=True),
        n('F4', 1.5, tie_stop=True),
    ])  # Long tone while piano has melody

    add_measure(part, 38, [
        n('E4', 1.0), n('F4', 0.5),
        n('G4', 1.5),
    ])

    add_measure(part, 39, [
        n('A4', 1.0), n('G4', 0.5),
        n('F4', 1.0), n('E4', 0.5),
    ])

    add_measure(part, 40, [
        n('F4', 1.5, tenuto=True), r(1.5),
    ])

    # m.41-44: Building together, hearts racing
    add_measure(part, 41, [
        n('C5', 0.5), n('D5', 0.5), n('E5', 0.5),
        n('F5', 0.75), n('E5', 0.25), n('D5', 0.5),
    ], dyn='f')

    add_measure(part, 42, [
        n('E5', 1.0, accent=True), n('D5', 0.5),
        n('C5', 0.5), n('Bb4', 0.5), n('A4', 0.5),
    ])

    add_measure(part, 43, [
        n('Bb4', 1.0), n('C5', 0.5),
        n('D5', 1.0), n('E5', 0.5),
    ])

    add_measure(part, 44, [
        n('F5', 1.5, tie_start=True),
        n('F5', 1.0, tie_stop=True), n('E5', 0.5),
    ])

    # m.45-48: Peak -- the moment you realize
    add_measure(part, 45, [
        n('F5', 0.5), n('G5', 0.5), n('Bb5', 0.5),  # push to Bb5 -- the peak
        n('A5', 0.75, accent=True), n('G5', 0.25), n('F5', 0.5),
    ], dyn='f')

    add_measure(part, 46, [
        n('E5', 1.0), n('D5', 0.5),
        n('C5', 1.0), n('Bb4', 0.5),
    ])

    add_measure(part, 47, [
        n('A4', 0.75), n('C5', 0.25), n('E5', 0.5),
        n('D5', 1.0, tenuto=True), n('C5', 0.5),
    ])

    add_measure(part, 48, [
        n('C5', 1.5), r(1.5),
    ], dyn='mf')

    # ── Section D: mm.49-60 -- "L'apres-midi" ──
    # Walking through the village. D minor shading, then warmth of Bb.

    add_measure(part, 49, [
        n('D4', 1.0), n('E4', 0.5),
        n('F4', 1.0), n('A4', 0.5),
    ], dyn='mp',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=69))

    add_measure(part, 50, [
        n('Bb4', 1.5, tenuto=True),
        n('A4', 0.5), n('G4', 0.5), n('F4', 0.5),
    ])

    add_measure(part, 51, [
        n('E4', 1.0), n('C#4', 0.5),  # A7 color, longing
        n('D4', 1.5, tenuto=True),
    ])

    add_measure(part, 52, [
        n('F4', 0.5), n('G#4', 0.5), n('A4', 0.5),  # G# = chromatic approach to A
        n('D5', 1.5),
    ])

    # m.53-56: Bb major warmth
    add_measure(part, 53, [
        n('D5', 0.5), n('Eb5', 0.5), n('F5', 0.5),
        n('D5', 1.0, accent=True), n('C5', 0.5),
    ], dyn='mf')

    add_measure(part, 54, [
        n('Bb4', 1.5),
        n('G4', 0.5), n('A4', 0.5), n('Bb4', 0.5),
    ])

    add_measure(part, 55, [
        n('C5', 1.0), n('A4', 0.5),
        n('F4', 1.5),
    ])

    add_measure(part, 56, [
        n('D5', 1.0, tenuto=True), n('C5', 0.5),
        n('Bb4', 1.5),
    ])

    # m.57-60: Transition back to F
    add_measure(part, 57, [
        n('A4', 1.0), n('Ab4', 0.5),  # Ab = chromatic passing, melancholy tinge
        n('G4', 1.0), n('F#4', 0.5),  # F# = leading to G, borrowed from G major
    ], dyn='p')

    add_measure(part, 58, [
        n('G4', 1.5),
        n('A4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 59, [
        n('F4', 1.0), n('A4', 0.5),
        n('Bb4', 1.0), n('C5', 0.5),
    ])

    add_measure(part, 60, [
        n('A4', 1.5, tenuto=True), r(1.5),
    ], dyn='pp')

    # ── Section E: mm.61-72 -- "Le soir" ──
    # Evening. She's gone. The memory lingers.

    # m.61-64: Ghostly return of opening motif
    add_measure(part, 61, [
        r(1.5),
        n('F4', 0.5), n('G4', 0.5), n('A4', 0.5),
    ], dyn='pp',
       tempo_mark=tempo.MetronomeMark(referent=duration.Duration(1.5), number=63,
                                       text="Lento"))

    add_measure(part, 62, [
        n('Bb4', 1.5, tenuto=True),
        n('A4', 1.0), n('G4', 0.5),
    ])

    add_measure(part, 63, [
        n('F4', 1.5), r(1.5),
    ])

    add_measure(part, 64, [
        r(3.0),
    ])

    # m.65-68: Brief reappearance, fragmentary
    add_measure(part, 65, [
        r(1.5),
        n('A4', 0.5), n('Bb4', 0.5), n('B4', 0.5),  # B natural = chromatic passing
    ], dyn='ppp')

    add_measure(part, 66, [
        n('C5', 0.5), n('Db5', 1.0, tenuto=True), r(1.5),  # Db = Neapolitan sigh
    ])

    add_measure(part, 67, [
        n('C5', 1.0), n('A4', 0.5),
        n('F4', 1.5),
    ])

    add_measure(part, 68, [
        n('G4', 1.0), n('F#4', 0.5),  # F# = chromatic neighbor, wistful
        n('G4', 1.5, tenuto=True),
    ])

    # m.69-72: Final notes, dissolving
    add_measure(part, 69, [
        r(1.5),
        n('F4', 0.5), n('A4', 0.5), n('C5', 0.5),
    ], dyn='ppp')

    add_measure(part, 70, [
        n('D5', 2.0, tenuto=True), n('C5', 0.5), r(0.5),
    ])

    add_measure(part, 71, [
        n('A4', 1.5, tie_start=True),
        n('A4', 1.5, tie_stop=True),
    ])

    add_measure(part, 72, [
        n('F4', 3.0, fermata=True),
    ])


# ══════════════════════════════════════════════════════════════════════════
# Hairpins (crescendo / diminuendo)
# ══════════════════════════════════════════════════════════════════════════

def add_hairpins(score):
    piano = clarinet = None
    for p in score.parts:
        if 'Piano' in (p.partName or ''):
            piano = p
        elif 'Clarinet' in (p.partName or ''):
            clarinet = p

    def get_first(part, m_num):
        for m in part.getElementsByClass(stream.Measure):
            if m.number == m_num:
                els = list(m.recurse().getElementsByClass([note.Note, chord.Chord, note.Rest]))
                return els[0] if els else None
        return None

    def get_last(part, m_num):
        for m in part.getElementsByClass(stream.Measure):
            if m.number == m_num:
                els = list(m.recurse().getElementsByClass([note.Note, chord.Chord, note.Rest]))
                return els[-1] if els else None
        return None

    specs = [
        # Piano
        ('piano', 9, 11, 'crescendo'),
        ('piano', 15, 16, 'diminuendo'),
        ('piano', 25, 28, 'crescendo'),
        ('piano', 30, 32, 'diminuendo'),
        ('piano', 41, 44, 'crescendo'),
        ('piano', 56, 57, 'diminuendo'),
        ('piano', 61, 62, 'diminuendo'),
        ('piano', 69, 72, 'diminuendo'),
        # Clarinet
        ('clarinet', 21, 24, 'crescendo'),
        ('clarinet', 25, 28, 'crescendo'),
        ('clarinet', 41, 44, 'crescendo'),
        ('clarinet', 45, 48, 'diminuendo'),
        ('clarinet', 57, 60, 'diminuendo'),
        ('clarinet', 69, 72, 'diminuendo'),
    ]

    for part_name, start_m, end_m, h_type in specs:
        p = piano if part_name == 'piano' else clarinet
        if not p:
            continue
        s = get_first(p, start_m)
        e = get_last(p, end_m)
        if s and e:
            hp = Crescendo(s, e) if h_type == 'crescendo' else Diminuendo(s, e)
            p.insert(0, hp)


# ══════════════════════════════════════════════════════════════════════════
# Build Score
# ══════════════════════════════════════════════════════════════════════════

def build_score():
    s = stream.Score()
    s.insert(0, layout.StaffGroup([]))

    cl_part = stream.Part()
    cl_inst = instrument.Clarinet()  # Bb clarinet
    cl_part.insert(0, cl_inst)
    cl_part.partName = "Clarinet in Bb"
    cl_part.partAbbreviation = "Cl."

    pno_part = stream.Part()
    pno_inst = instrument.Piano()
    pno_part.insert(0, pno_inst)
    pno_part.partName = "Piano"
    pno_part.partAbbreviation = "Pno."

    build_clarinet(cl_part)
    build_piano(pno_part)

    s.insert(0, cl_part)
    s.insert(0, pno_part)

    return s


def main():
    print("Building 'Farine et Lavande'...")
    score = build_score()

    print("Adding hairpins...")
    add_hairpins(score)

    print(f"Writing to {OUTPUT_PATH}...")
    score.write('musicxml', fp=OUTPUT_PATH)
    print(f"Done! Wrote {OUTPUT_PATH}")

    # Quick validation
    from music21 import converter
    s = converter.parse(OUTPUT_PATH)
    notes = list(s.recurse().getElementsByClass('Note'))
    chords = list(s.recurse().getElementsByClass('Chord'))
    print(f"Parsed OK: {len(s.parts)} parts, {len(notes)} notes, {len(chords)} chords")


if __name__ == '__main__':
    main()
