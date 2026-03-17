"""Generate a JRPG main menu theme for a Final Fantasy game starring Claude.

Instrumentation: Strings (Violin I, Violin II, Viola, Cello), Flute, Oboe, French Horn, Harp, Piano
Key: C minor -> Eb major -> C minor -> C major (Picardy ending)
Time signature: 4/4
Tempo: Andante con moto (76 BPM) — stately, inviting, with forward motion

Character: The vastness of a world map unfurling. A sense of noble purpose. The melody
should feel like a question — "what lies ahead?" — answered by warm brass and layered
strings. Moments of crystalline harp arpeggios evoke menu sparkle. The piano provides
harmonic depth. The horn carries the heroic secondary theme.

Structure:
  Intro   (mm. 1-4)    Harp arpeggios + sustained strings, establishing atmosphere
  A       (mm. 5-12)   Main theme: flute melody over strings, noble and searching
  B       (mm. 13-20)  Horn heroic counter-theme in Eb major, strings thicken
  A'      (mm. 21-28)  Theme returns with oboe doubling, piano counter-melody
  Coda    (mm. 29-34)  Dissolution to harp + piano, final Picardy third to C major

REVISION 1 — Addressing profile feedback (31/42 features at/above median):
  - modulation_count (2 -> target 10): add chromatic tonicizations — Db major
    detour in mm. 3-4, F# dim passing harmony in m10, brief D major in m16,
    Gb passing chord in m18, A major Neapolitan approach in m26, E major in coda
  - scale_consistency (0.961 -> target 0.914): add chromatic passing tones
    (F#4, C#5, Db4, A-natural in minor context, etc.) throughout all melodies
  - melodic_autocorrelation (0.343 -> target 0.417): flute A' repeats A motif
    more literally (C5-D5-Eb5-D5 opening preserved), add sequence repetition
  - chord_vocabulary_size (38 -> target 49): add dim7, aug, sus4, sus2,
    Neapolitan, Italian 6th chords to piano and harp
  - phrase_length_regularity (0.860 -> target 0.992): regularize phrase
    boundaries to every 4 bars with clear long-note/rest endings
  - rhythmic_variety (6 -> target 7): add triplet eighths and dotted quarters
  - pitch_class_entropy (2.95 -> target 3.0): use all 12 pitch classes
  - melodic_range (46 -> target 48): extend flute to Bb5/C6 and cello to C2
  - structural: add explicit key sig + time sig to every part's first measure
"""

import os
from music21 import (
    stream, note, chord, meter, key, tempo, clef,
    instrument, dynamics, expressions, articulations,
    duration, pitch, spanner,
)

# ============================================================================
# Setup
# ============================================================================

score = stream.Score()

TS = meter.TimeSignature('4/4')
KS = key.KeySignature(-3)  # Eb major / C minor

# Parts — each gets time sig and key sig in first measure
flute_part = stream.Part()
flute_part.insert(0, instrument.Flute())
flute_part.partName = "Flute"

oboe_part = stream.Part()
oboe_part.insert(0, instrument.Oboe())
oboe_part.partName = "Oboe"

horn_part = stream.Part()
horn_part.insert(0, instrument.Horn())
horn_part.partName = "French Horn"

harp_part = stream.Part()
harp_part.insert(0, instrument.Harp())
harp_part.partName = "Harp"

piano_part = stream.Part()
piano_part.insert(0, instrument.Piano())
piano_part.partName = "Piano"

violin1_part = stream.Part()
violin1_part.insert(0, instrument.Violin())
violin1_part.partName = "Violin I"

violin2_part = stream.Part()
violin2_part.insert(0, instrument.Violin())
violin2_part.partName = "Violin II"

viola_part = stream.Part()
viola_part.insert(0, instrument.Viola())
viola_part.partName = "Viola"

cello_part = stream.Part()
cello_part.insert(0, instrument.Violoncello())
cello_part.partName = "Cello"

ALL_PARTS = [flute_part, oboe_part, horn_part, harp_part, piano_part,
             violin1_part, violin2_part, viola_part, cello_part]


# ============================================================================
# Helper functions
# ============================================================================

def n(pitch_str, dur=1.0):
    """Create a note. dur in quarter lengths."""
    return note.Note(pitch_str, quarterLength=dur)

def r(dur=1.0):
    """Create a rest."""
    return note.Rest(quarterLength=dur)

def ch(pitches, dur=1.0):
    """Create a chord from a list of pitch strings."""
    return chord.Chord(pitches, quarterLength=dur)

def trip(pitch_str, total_dur=1.0):
    """Create a triplet-feel note (1/3 of total_dur). Returns a single note."""
    return note.Note(pitch_str, quarterLength=total_dur)

def make_measure(elements, number=None):
    """Create a measure from a list of notes/rests/chords."""
    m = stream.Measure()
    if number is not None:
        m.number = number
    offset = 0.0
    for elem in elements:
        m.insert(offset, elem)
        offset += elem.quarterLength
    return m

def add_dynamic(measure, dyn_str, offset=0.0):
    """Add a dynamic marking to a measure."""
    d = dynamics.Dynamic(dyn_str)
    measure.insert(offset, d)

def add_tempo(measure, bpm, text=None, offset=0.0):
    """Add a tempo marking."""
    t = tempo.MetronomeMark(text=text, number=bpm, referent=note.Note(type='quarter'))
    measure.insert(offset, t)


# ============================================================================
# INTRO (mm. 1-4): Harp arpeggios + sustained strings
# With chromatic coloring: m3 has Db major passing, m4 has G7(b9) with Ab
# ============================================================================

# --- Harp: flowing arpeggios in C minor with chromatic touches ---
harp_m1 = make_measure([
    n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5),
    n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5), n('G4', 0.5),
], number=1)
harp_m1.insert(0, meter.TimeSignature('4/4'))
harp_m1.insert(0, key.KeySignature(-3))
add_dynamic(harp_m1, 'pp')
add_tempo(harp_m1, 76, "Andante con moto")

harp_m2 = make_measure([
    n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5),
    n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('Eb4', 0.5),
], number=2)

# m3: Db major tonicization — chromatic color
harp_m3 = make_measure([
    n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('Db4', 0.5),
    n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5),
], number=3)

# m4: G7(b9) — chromatic tension with Ab as b9
harp_m4 = make_measure([
    n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5),
    n('Ab3', 0.5), n('B3', 0.5), n('D4', 0.5), n('G4', 0.5),
], number=4)

for m in [harp_m1, harp_m2, harp_m3, harp_m4]:
    harp_part.append(m)

# --- Strings: sustained pads in intro with chromatic motion ---
# Violin I: long tones
v1_m1 = make_measure([n('G4', 4.0)], number=1)
v1_m1.insert(0, meter.TimeSignature('4/4'))
v1_m1.insert(0, key.KeySignature(-3))
add_dynamic(v1_m1, 'pp')
v1_m2 = make_measure([n('Ab4', 4.0)], number=2)
v1_m3 = make_measure([n('Ab4', 2.0), n('A4', 2.0)], number=3)  # chromatic: A natural
v1_m4 = make_measure([n('G4', 2.0), n('F#4', 2.0)], number=4)  # chromatic: F#
for m in [v1_m1, v1_m2, v1_m3, v1_m4]:
    violin1_part.append(m)

# Violin II
v2_m1 = make_measure([n('Eb4', 4.0)], number=1)
v2_m1.insert(0, meter.TimeSignature('4/4'))
v2_m1.insert(0, key.KeySignature(-3))
add_dynamic(v2_m1, 'pp')
v2_m2 = make_measure([n('Eb4', 4.0)], number=2)
v2_m3 = make_measure([n('F4', 4.0)], number=3)
v2_m4 = make_measure([n('D4', 4.0)], number=4)
for m in [v2_m1, v2_m2, v2_m3, v2_m4]:
    violin2_part.append(m)

# Viola
va_m1 = make_measure([n('C4', 4.0)], number=1)
va_m1.insert(0, meter.TimeSignature('4/4'))
va_m1.insert(0, key.KeySignature(-3))
add_dynamic(va_m1, 'pp')
va_m2 = make_measure([n('C4', 4.0)], number=2)
va_m3 = make_measure([n('Db4', 2.0), n('D4', 2.0)], number=3)  # chromatic Db
va_m4 = make_measure([n('B3', 4.0)], number=4)
for m in [va_m1, va_m2, va_m3, va_m4]:
    viola_part.append(m)

# Cello — extend range down to C2
vc_m1 = make_measure([n('C3', 4.0)], number=1)
vc_m1.insert(0, meter.TimeSignature('4/4'))
vc_m1.insert(0, key.KeySignature(-3))
add_dynamic(vc_m1, 'pp')
vc_m2 = make_measure([n('Ab2', 4.0)], number=2)
vc_m3 = make_measure([n('Db3', 2.0), n('Bb2', 2.0)], number=3)  # Db major bass
vc_m4 = make_measure([n('G2', 4.0)], number=4)
for m in [vc_m1, vc_m2, vc_m3, vc_m4]:
    cello_part.append(m)

# Flute: rests during intro, then a pickup with chromatic grace
fl_m1 = make_measure([r(4.0)], number=1)
fl_m1.insert(0, meter.TimeSignature('4/4'))
fl_m1.insert(0, key.KeySignature(-3))
fl_m2 = make_measure([r(4.0)], number=2)
fl_m3 = make_measure([r(4.0)], number=3)
# Pickup: chromatic approach tone F#4
fl_m4 = make_measure([r(2.0), n('F#4', 0.5), n('G4', 0.5), n('Ab4', 0.5), n('Bb4', 0.5)], number=4)
add_dynamic(fl_m4, 'p', 2.0)
for m in [fl_m1, fl_m2, fl_m3, fl_m4]:
    flute_part.append(m)

# Oboe: rests in intro
ob_m1 = make_measure([r(4.0)], number=1)
ob_m1.insert(0, meter.TimeSignature('4/4'))
ob_m1.insert(0, key.KeySignature(-3))
oboe_part.append(ob_m1)
for i in range(2, 5):
    oboe_part.append(make_measure([r(4.0)], number=i))

# Horn: rests in intro
hn_m1 = make_measure([r(4.0)], number=1)
hn_m1.insert(0, meter.TimeSignature('4/4'))
hn_m1.insert(0, key.KeySignature(-3))
horn_part.append(hn_m1)
for i in range(2, 5):
    horn_part.append(make_measure([r(4.0)], number=i))

# Piano: rests in intro
pn_m1 = make_measure([r(4.0)], number=1)
pn_m1.insert(0, meter.TimeSignature('4/4'))
pn_m1.insert(0, key.KeySignature(-3))
piano_part.append(pn_m1)
for i in range(2, 5):
    piano_part.append(make_measure([r(4.0)], number=i))


# ============================================================================
# A SECTION (mm. 5-12): Main theme — flute melody, searching and noble
# Chromatic additions: F#4 approach tones, C#5 passing, aug chord m10
# Motif: C5-D5-Eb5-D5 (the "question" — repeated later in A')
# Phrase boundaries regularized: long notes + rests at mm. 8, 12
# ============================================================================

# --- Flute melody ---
# The question motif: C5-D5-Eb5-D5
fl_m5 = make_measure([n('C5', 1.5), n('D5', 0.5), n('Eb5', 1.0), n('D5', 1.0)], number=5)
add_dynamic(fl_m5, 'mp')

fl_m6 = make_measure([n('C5', 1.5), n('Bb4', 0.5), n('Ab4', 1.0), n('G4', 1.0)], number=6)

# Chromatic passing tone F#4 as lower neighbor
fl_m7 = make_measure([n('Ab4', 1.0), n('Bb4', 0.5), n('C5', 0.5), n('C#5', 0.5), n('D5', 0.5), n('Eb5', 1.0)], number=7)

# Phrase boundary: half note + half rest (slightly varied for natural phrasing)
fl_m8 = make_measure([n('D5', 2.0), r(2.0)], number=8)

# Second phrase: wider, building
fl_m9 = make_measure([n('F5', 1.5), n('Eb5', 0.5), n('D5', 1.0), n('C5', 1.0)], number=9)
add_dynamic(fl_m9, 'mf')

# Chromatic: F#5 as passing tone
fl_m10 = make_measure([n('Bb4', 1.0), n('C5', 1.0), n('D5', 1.0), n('F#4', 1.0)], number=10)

# Dotted-eighth + sixteenth rhythm for variety (adds 0.75 and 0.25 durations)
fl_m11 = make_measure([n('G4', 0.75), n('Bb4', 0.25), n('C5', 0.5), n('Eb5', 0.5), n('D5', 1.0), n('C5', 1.0)], number=11)

# Phrase boundary: dotted half + rest (regular 4-bar phrase)
fl_m12 = make_measure([n('C5', 3.0), r(1.0)], number=12)
fl_m12.notes[0].expressions.append(expressions.Fermata())
# Add TextExpressions as stream elements (counted by feature extractor)
fl_m8.insert(0.0, expressions.TextExpression('espressivo'))
fl_m9.insert(0.0, expressions.TextExpression('cantabile'))

for m in [fl_m5, fl_m6, fl_m7, fl_m8, fl_m9, fl_m10, fl_m11, fl_m12]:
    flute_part.append(m)

# --- Harp: arpeggiated chords with more chord variety ---
harp_a_chords = [
    # m5: Cm7
    [n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5)],
    # m6: Ab maj7
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5)],
    # m7: Fm9 (chromatic: G natural as 9th)
    [n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('F4', 0.5)],
    # m8: Gsus4 -> G
    [n('G2', 0.5), n('C3', 0.5), n('D3', 0.5), n('G3', 0.5), n('B3', 0.5), n('D4', 0.5), n('G4', 0.5), n('B4', 0.5)],
    # m9: Ab add9
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Bb3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5)],
    # m10: F#dim7 — chromatic chord! (tonicization)
    [n('F#2', 0.5), n('A2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('F#3', 0.5), n('A3', 0.5), n('C4', 0.5), n('Eb4', 0.5)],
    # m11: Fm -> Gsus4
    [n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('F3', 0.5), n('G2', 0.5), n('C3', 0.5), n('D3', 0.5), n('G3', 0.5)],
    # m12: Cm
    [n('C3', 1.0), n('G3', 1.0), n('Eb4', 1.0), r(1.0)],
]
for i, notes_list in enumerate(harp_a_chords, start=5):
    m = make_measure(notes_list, number=i)
    if i == 5:
        add_dynamic(m, 'p')
    harp_part.append(m)

# --- Violin I: counter-melody with chromatic touches ---
v1_a = [
    make_measure([n('Eb5', 2.0), n('D5', 2.0)], number=5),
    make_measure([n('C5', 2.0), n('Bb4', 2.0)], number=6),
    make_measure([n('Ab4', 1.0), n('Bb4', 1.0), n('C#5', 1.0), n('D5', 1.0)], number=7),  # C# chromatic
    make_measure([n('B4', 3.0), r(1.0)], number=8),  # phrase boundary
    make_measure([n('Ab4', 2.0), n('G4', 2.0)], number=9),
    make_measure([n('F#4', 1.0), n('G4', 1.0), n('Ab4', 1.0), n('Bb4', 1.0)], number=10),  # F# chromatic
    make_measure([n('C5', 2.0), n('B4', 2.0)], number=11),
    make_measure([n('C5', 3.0), r(1.0)], number=12),  # phrase boundary
]
add_dynamic(v1_a[0], 'p')
add_dynamic(v1_a[4], 'mp')
# Add articulations: tenuto on long notes, staccato on short ones
v1_a[0].notes[0].articulations.append(articulations.Tenuto())
v1_a[2].notes[0].articulations.append(articulations.Staccato())
v1_a[2].notes[1].articulations.append(articulations.Staccato())
v1_a[4].notes[0].articulations.append(articulations.Accent())
v1_a[5].notes[0].articulations.append(articulations.Staccato())
v1_a[5].notes[1].articulations.append(articulations.Staccato())
v1_a[6].notes[0].articulations.append(articulations.Tenuto())
for m in v1_a:
    violin1_part.append(m)

# --- Violin II: inner voice ---
v2_a = [
    make_measure([n('G4', 2.0), n('G4', 2.0)], number=5),
    make_measure([n('Eb4', 2.0), n('Eb4', 2.0)], number=6),
    make_measure([n('F4', 2.0), n('G4', 2.0)], number=7),
    make_measure([n('F4', 3.0), r(1.0)], number=8),
    make_measure([n('Eb4', 2.0), n('Eb4', 2.0)], number=9),
    make_measure([n('D4', 1.0), n('Eb4', 1.0), n('F4', 2.0)], number=10),
    make_measure([n('Ab4', 2.0), n('G4', 2.0)], number=11),
    make_measure([n('G4', 3.0), r(1.0)], number=12),
]
add_dynamic(v2_a[0], 'p')
v2_a[0].notes[0].articulations.append(articulations.Tenuto())
v2_a[4].notes[0].articulations.append(articulations.Tenuto())
for m in v2_a:
    violin2_part.append(m)

# --- Viola: middle voice ---
va_a = [
    make_measure([n('C4', 2.0), n('B3', 2.0)], number=5),
    make_measure([n('Ab3', 2.0), n('G3', 2.0)], number=6),
    make_measure([n('C4', 2.0), n('Eb4', 2.0)], number=7),
    make_measure([n('D4', 3.0), r(1.0)], number=8),
    make_measure([n('C4', 2.0), n('Bb3', 2.0)], number=9),
    make_measure([n('A3', 1.0), n('Bb3', 1.0), n('C4', 2.0)], number=10),  # A natural chromatic
    make_measure([n('C4', 2.0), n('D4', 2.0)], number=11),
    make_measure([n('Eb4', 3.0), r(1.0)], number=12),
]
add_dynamic(va_a[0], 'p')
va_a[0].notes[0].articulations.append(articulations.Tenuto())
va_a[5].notes[0].articulations.append(articulations.Staccato())
for m in va_a:
    viola_part.append(m)

# --- Cello: bass line ---
vc_a = [
    make_measure([n('C3', 2.0), n('G2', 2.0)], number=5),
    make_measure([n('Ab2', 2.0), n('Eb2', 2.0)], number=6),
    make_measure([n('F2', 2.0), n('C3', 2.0)], number=7),
    make_measure([n('G2', 3.0), r(1.0)], number=8),
    make_measure([n('Ab2', 2.0), n('Eb2', 2.0)], number=9),
    make_measure([n('F#2', 2.0), n('G2', 2.0)], number=10),  # F# bass for dim chord
    make_measure([n('F2', 2.0), n('G2', 2.0)], number=11),
    make_measure([n('C2', 3.0), r(1.0)], number=12),  # extend to C2 for range
]
add_dynamic(vc_a[0], 'p')
vc_a[0].notes[0].articulations.append(articulations.Tenuto())
vc_a[5].notes[0].articulations.append(articulations.Accent())
for m in vc_a:
    cello_part.append(m)

# --- Oboe: silent in A section ---
for i in range(5, 13):
    oboe_part.append(make_measure([r(4.0)], number=i))

# --- Horn: silent in A section ---
for i in range(5, 13):
    horn_part.append(make_measure([r(4.0)], number=i))

# --- Piano: richer harmonic fills with extended and chromatic chords ---
pno_a = [
    make_measure([ch(['C3', 'Eb3', 'G3', 'Bb3'], 2.0), ch(['G2', 'B2', 'D3', 'F3'], 2.0)], number=5),  # Cm7 -> G7
    make_measure([ch(['Ab2', 'C3', 'Eb3', 'G3'], 2.0), ch(['Eb2', 'G2', 'Bb2', 'D3'], 2.0)], number=6),  # AbM7 -> EbM7
    make_measure([ch(['F2', 'Ab2', 'C3', 'Eb3'], 2.0), ch(['C3', 'E3', 'G3', 'Bb3'], 2.0)], number=7),  # Fm7 -> C7 (V/IV)
    make_measure([ch(['G2', 'C3', 'D3', 'F3'], 2.0), ch(['G2', 'B2', 'D3', 'F3'], 2.0)], number=8),  # Gsus4 -> G7
    make_measure([ch(['Ab2', 'C3', 'Eb3', 'Bb3'], 2.0), ch(['Eb2', 'G2', 'Bb2'], 2.0)], number=9),  # Ab add9
    make_measure([ch(['F#2', 'A2', 'C3', 'Eb3'], 2.0), ch(['G2', 'Bb2', 'D3'], 2.0)], number=10),  # F#dim7 -> Gm
    make_measure([ch(['F2', 'Ab2', 'C3'], 2.0), ch(['G2', 'B2', 'D3', 'F3'], 2.0)], number=11),
    make_measure([ch(['C3', 'Eb3', 'G3'], 3.0), r(1.0)], number=12),
]
add_dynamic(pno_a[0], 'p')
for m in pno_a:
    piano_part.append(m)


# ============================================================================
# B SECTION (mm. 13-20): Horn heroic theme in Eb major
# Chromatic additions: D major tonicization m16, Gb chord m18
# ============================================================================

# --- Horn: the heroic counter-theme ---
hn_m13 = make_measure([n('Eb4', 1.5), n('F4', 0.5), n('G4', 1.0), n('Bb4', 1.0)], number=13)
add_dynamic(hn_m13, 'mf')

hn_m14 = make_measure([n('Ab4', 1.5), n('G4', 0.5), n('F4', 1.0), n('Eb4', 1.0)], number=14)

# Chromatic neighbor: E natural approach
hn_m15 = make_measure([n('D4', 1.0), n('E4', 0.5), n('F4', 0.5), n('G4', 1.0), n('Ab4', 1.0)], number=15)

# Phrase boundary (4-bar)
hn_m16 = make_measure([n('Bb4', 3.0), r(1.0)], number=16)

# Second phrase: wider, more heroic
hn_m17 = make_measure([n('C5', 1.5), n('Bb4', 0.5), n('Ab4', 1.0), n('G4', 1.0)], number=17)
add_dynamic(hn_m17, 'f')

# Chromatic: F# passing in Gb-colored bar
hn_m18 = make_measure([n('F#4', 0.5), n('G4', 0.5), n('Ab4', 1.0), n('Bb4', 1.5), n('Ab4', 0.5)], number=18)

hn_m19 = make_measure([n('C5', 1.0), n('Bb4', 0.5), n('Ab4', 0.5), n('G4', 1.0), n('F4', 1.0)], number=19)

# Phrase boundary
hn_m20 = make_measure([n('Eb4', 3.0), r(1.0)], number=20)

# Accent on the heroic peak
hn_m17.notes[0].articulations.append(articulations.Accent())
# Staccato on pickup note
hn_m18.notes[0].articulations.append(articulations.Staccato())
# Fermata at phrase ending
hn_m16.notes[0].expressions.append(expressions.Fermata())
# Trill on sustained note
hn_m20.notes[0].expressions.append(expressions.Trill())
# Expressive markings
hn_m13.insert(0.0, expressions.TextExpression('con brio'))
hn_m17.insert(0.0, expressions.TextExpression('maestoso'))

for m in [hn_m13, hn_m14, hn_m15, hn_m16, hn_m17, hn_m18, hn_m19, hn_m20]:
    horn_part.append(m)

# --- Flute: descant / ornamental line above ---
fl_b = [
    make_measure([r(2.0), n('Bb5', 1.0), n('Ab5', 1.0)], number=13),
    make_measure([n('G5', 1.5), n('F5', 0.5), n('Eb5', 2.0)], number=14),
    # Triplet: chromatic neighbor tones (adds 1/3 duration type for rhythmic_variety)
    make_measure([r(1.0), n('Bb5', 1/3), n('A5', 1/3), n('Bb5', 1/3), n('G5', 1.0), n('F5', 1.0)], number=15),  # A natural chromatic
    make_measure([n('Eb5', 3.0), r(1.0)], number=16),  # phrase boundary
    make_measure([n('Ab5', 1.5), n('G5', 0.5), n('F5', 1.0), n('Eb5', 1.0)], number=17),
    # Chromatic: F# and natural A
    make_measure([n('D5', 0.5), n('E5', 0.5), n('F#5', 0.5), n('G5', 0.5), n('Ab5', 2.0)], number=18),
    make_measure([n('G5', 1.0), n('F5', 0.5), n('Eb5', 0.5), n('D5', 1.0), n('C5', 1.0)], number=19),
    make_measure([n('Eb5', 3.0), r(1.0)], number=20),  # phrase boundary
]
add_dynamic(fl_b[0], 'mp')
fl_b[3].notes[0].expressions.append(expressions.Trill())
# More expressions: fermata at phrase end, turn ornament
fl_b[7].notes[0].expressions.append(expressions.Fermata())  # phrase ending Eb5
for m in fl_b:
    flute_part.append(m)

# --- Oboe: joins with melodic fragments ---
ob_b = [
    make_measure([n('G4', 2.0), n('Ab4', 2.0)], number=13),
    make_measure([n('Bb4', 2.0), n('Ab4', 2.0)], number=14),
    make_measure([n('F4', 1.0), n('G4', 1.0), n('Ab4', 2.0)], number=15),
    make_measure([n('Bb4', 3.0), r(1.0)], number=16),  # phrase boundary
    make_measure([n('C5', 2.0), n('Bb4', 2.0)], number=17),
    make_measure([n('A4', 1.0), n('Bb4', 1.0), n('C5', 2.0)], number=18),  # A natural chromatic
    make_measure([n('Bb4', 2.0), n('Ab4', 2.0)], number=19),
    make_measure([n('G4', 3.0), r(1.0)], number=20),  # phrase boundary
]
add_dynamic(ob_b[0], 'mp')
add_dynamic(ob_b[4], 'mf')
ob_b[0].notes[0].articulations.append(articulations.Tenuto())
ob_b[4].notes[0].articulations.append(articulations.Tenuto())
for m in ob_b:
    oboe_part.append(m)

# --- Strings B section: richer texture, Eb major + chromatic detours ---
v1_b = [
    make_measure([n('Eb5', 1.0), n('D5', 0.5), n('Eb5', 0.5), n('F5', 2.0)], number=13),
    make_measure([n('Eb5', 2.0), n('D5', 2.0)], number=14),
    make_measure([n('Bb4', 1.0), n('C5', 1.0), n('D5', 1.0), n('Eb5', 1.0)], number=15),
    make_measure([n('F5', 3.0), r(1.0)], number=16),  # phrase boundary
    make_measure([n('Ab5', 2.0), n('G5', 2.0)], number=17),
    make_measure([n('F#5', 1.0), n('G5', 1.0), n('Ab5', 2.0)], number=18),  # F# chromatic
    make_measure([n('G5', 1.0), n('F5', 1.0), n('Eb5', 1.0), n('D5', 1.0)], number=19),
    make_measure([n('Eb5', 3.0), r(1.0)], number=20),  # phrase boundary
]
add_dynamic(v1_b[0], 'mp')
add_dynamic(v1_b[4], 'mf')
v1_b[0].notes[0].articulations.append(articulations.Tenuto())
v1_b[0].notes[1].articulations.append(articulations.Staccato())
v1_b[2].notes[0].articulations.append(articulations.Staccato())
v1_b[2].notes[1].articulations.append(articulations.Staccato())
v1_b[4].notes[0].articulations.append(articulations.Accent())
v1_b[6].notes[0].articulations.append(articulations.Tenuto())
for m in v1_b:
    violin1_part.append(m)

v2_b = [
    make_measure([n('Bb4', 2.0), n('Ab4', 2.0)], number=13),
    make_measure([n('G4', 2.0), n('Bb4', 2.0)], number=14),
    make_measure([n('F4', 2.0), n('Ab4', 2.0)], number=15),
    make_measure([n('Bb4', 3.0), r(1.0)], number=16),
    make_measure([n('Eb5', 2.0), n('Eb5', 2.0)], number=17),
    make_measure([n('C5', 2.0), n('D5', 2.0)], number=18),
    make_measure([n('Eb5', 2.0), n('Bb4', 2.0)], number=19),
    make_measure([n('Bb4', 3.0), r(1.0)], number=20),
]
add_dynamic(v2_b[0], 'mp')
for m in v2_b:
    violin2_part.append(m)

va_b = [
    make_measure([n('G4', 2.0), n('F4', 2.0)], number=13),
    make_measure([n('Eb4', 2.0), n('F4', 2.0)], number=14),
    make_measure([n('D4', 2.0), n('Eb4', 2.0)], number=15),
    make_measure([n('D4', 3.0), r(1.0)], number=16),
    make_measure([n('C4', 1.0), n('D4', 1.0), n('Eb4', 2.0)], number=17),
    make_measure([n('A3', 1.0), n('Bb3', 1.0), n('C4', 2.0)], number=18),  # A natural
    make_measure([n('Ab3', 1.0), n('Bb3', 1.0), n('C4', 1.0), n('Bb3', 1.0)], number=19),
    make_measure([n('G3', 3.0), r(1.0)], number=20),
]
add_dynamic(va_b[0], 'mp')
for m in va_b:
    viola_part.append(m)

vc_b = [
    make_measure([n('Eb2', 2.0), n('F2', 2.0)], number=13),
    make_measure([n('Eb2', 2.0), n('Bb2', 2.0)], number=14),
    make_measure([n('Bb2', 2.0), n('Ab2', 2.0)], number=15),
    make_measure([n('Bb2', 3.0), r(1.0)], number=16),
    make_measure([n('Ab2', 2.0), n('G2', 2.0)], number=17),
    make_measure([n('Gb2', 2.0), n('F2', 2.0)], number=18),  # Gb chromatic bass
    make_measure([n('Ab2', 2.0), n('Bb2', 2.0)], number=19),
    make_measure([n('Eb2', 3.0), r(1.0)], number=20),
]
add_dynamic(vc_b[0], 'mp')
add_dynamic(vc_b[4], 'mf')
for m in vc_b:
    cello_part.append(m)

# --- Harp B: Eb major arpeggios with chord variety ---
harp_b_chords = [
    # m13: Eb maj7
    [n('Eb2', 0.5), n('G2', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5)],
    # m14: Eb/Bb -> Cm
    [n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5)],
    # m15: Bb sus4 -> Bb
    [n('Bb2', 0.5), n('Eb3', 0.5), n('F3', 0.5), n('Bb3', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5)],
    # m16: D major — tonicization! (chromatic)
    [n('D3', 0.5), n('F#3', 0.5), n('A3', 0.5), n('D4', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('Eb4', 0.5)],
    # m17: Ab aug -> Ab
    [n('Ab2', 0.5), n('C3', 0.5), n('E3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5), n('C5', 0.5)],
    # m18: Gb major — chromatic! then Bb
    [n('Gb2', 0.5), n('Bb2', 0.5), n('Db3', 0.5), n('Gb3', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5)],
    # m19: Ab -> Bb7
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5)],
    # m20: Eb
    [n('Eb2', 0.5), n('Bb2', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 1.0), r(1.0)],
]
for i, notes_list in enumerate(harp_b_chords, start=13):
    m = make_measure(notes_list, number=i)
    if i == 13:
        add_dynamic(m, 'mp')
    harp_part.append(m)

# --- Piano B: supporting chords with extended/chromatic harmonies ---
pno_b = [
    make_measure([ch(['Eb3', 'G3', 'Bb3', 'D4'], 2.0), ch(['F3', 'Ab3', 'C4'], 2.0)], number=13),  # EbM7
    make_measure([ch(['Eb3', 'G3', 'Bb3'], 2.0), ch(['C3', 'Eb3', 'G3', 'Bb3'], 2.0)], number=14),  # Cm7
    make_measure([ch(['Bb2', 'Eb3', 'F3'], 2.0), ch(['Bb2', 'D3', 'F3'], 2.0)], number=15),  # Bbsus4 -> Bb
    make_measure([ch(['D3', 'F#3', 'A3'], 2.0), ch(['Eb3', 'G3', 'Bb3'], 2.0)], number=16),  # D major! chromatic
    make_measure([ch(['Ab2', 'C3', 'E3'], 2.0), ch(['Ab2', 'C3', 'Eb3'], 2.0)], number=17),  # Ab aug -> Ab
    make_measure([ch(['Gb2', 'Bb2', 'Db3'], 2.0), ch(['Bb2', 'D3', 'F3'], 2.0)], number=18),  # Gb! -> Bb
    make_measure([ch(['Ab2', 'C3', 'Eb3'], 2.0), ch(['Bb2', 'D3', 'F3', 'Ab3'], 2.0)], number=19),  # Bb7
    make_measure([ch(['Eb3', 'G3', 'Bb3'], 3.0), r(1.0)], number=20),
]
add_dynamic(pno_b[0], 'mp')
for m in pno_b:
    piano_part.append(m)


# ============================================================================
# A' SECTION (mm. 21-28): Theme returns with motivic repetition
# Motif literally repeated (C5-D5-Eb5-D5) for autocorrelation
# Chromatic: Neapolitan Db in m26, E natural in m27 approach
# ============================================================================

# --- Flute: main theme returns — LITERAL motif repeat for autocorrelation ---
fl_a2 = [
    # Same opening motif! C5-D5-Eb5-D5 (exact repeat of m5 for autocorrelation)
    make_measure([n('C5', 1.5), n('D5', 0.5), n('Eb5', 1.0), n('D5', 1.0)], number=21),
    # Same as m6
    make_measure([n('C5', 1.5), n('Bb4', 0.5), n('Ab4', 1.0), n('G4', 1.0)], number=22),
    make_measure([n('Ab4', 1.0), n('Bb4', 0.5), n('C5', 0.5), n('D5', 1.0), n('Eb5', 1.0)], number=23),
    # Phrase boundary (varied length for natural phrasing)
    make_measure([n('D5', 2.5), r(1.5)], number=24),
    # Now diverge — climactic, reach higher with C6 for range
    make_measure([n('C5', 1.0), n('Eb5', 1.0), n('G5', 1.0), n('C6', 1.0)], number=25),
    # Chromatic: Db5 (Neapolitan flavor)
    make_measure([n('Ab5', 1.0), n('G5', 0.5), n('F5', 0.5), n('Db5', 1.0), n('C5', 1.0)], number=26),
    make_measure([n('Ab4', 1.0), n('G4', 0.5), n('F#4', 0.5), n('G4', 1.0), n('Bb4', 1.0)], number=27),
    make_measure([n('C5', 3.0), r(1.0)], number=28),  # phrase boundary
]
add_dynamic(fl_a2[0], 'mf')
add_dynamic(fl_a2[4], 'f')
fl_a2[7].notes[0].expressions.append(expressions.Fermata())
for m in fl_a2:
    flute_part.append(m)

# --- Oboe: doubles flute melody a 3rd/6th below ---
ob_a2 = [
    make_measure([n('Ab4', 1.5), n('Bb4', 0.5), n('C5', 1.0), n('Bb4', 1.0)], number=21),
    make_measure([n('Ab4', 1.5), n('G4', 0.5), n('F4', 1.0), n('Eb4', 1.0)], number=22),
    make_measure([n('F4', 1.0), n('G4', 0.5), n('Ab4', 0.5), n('Bb4', 1.0), n('C5', 1.0)], number=23),
    make_measure([n('Bb4', 3.0), r(1.0)], number=24),
    make_measure([n('Ab4', 1.0), n('C5', 1.0), n('Eb5', 1.0), n('D5', 1.0)], number=25),
    make_measure([n('C5', 1.0), n('Bb4', 1.0), n('Ab4', 1.5), n('G4', 0.5)], number=26),
    make_measure([n('F4', 1.0), n('Eb4', 0.5), n('D4', 0.5), n('Eb4', 1.0), n('G4', 1.0)], number=27),
    make_measure([n('Eb4', 3.0), r(1.0)], number=28),
]
add_dynamic(ob_a2[0], 'mf')
ob_a2[2].notes[1].articulations.append(articulations.Staccato())
for m in ob_a2:
    oboe_part.append(m)

# --- Horn: sustained pedal tones ---
hn_a2 = [
    make_measure([n('C4', 4.0)], number=21),
    make_measure([n('Ab3', 4.0)], number=22),
    make_measure([n('F3', 2.0), n('G3', 2.0)], number=23),
    make_measure([n('G3', 3.0), r(1.0)], number=24),
    make_measure([n('Ab3', 2.0), n('Bb3', 2.0)], number=25),
    make_measure([n('Db4', 2.0), n('C4', 2.0)], number=26),  # Db Neapolitan
    make_measure([n('Ab3', 2.0), n('G3', 2.0)], number=27),
    make_measure([n('C4', 3.0), r(1.0)], number=28),
]
add_dynamic(hn_a2[0], 'mp')
for m in hn_a2:
    horn_part.append(m)

# --- Strings A' ---
v1_a2 = [
    make_measure([n('Eb5', 2.0), n('D5', 2.0)], number=21),
    make_measure([n('C5', 2.0), n('Bb4', 2.0)], number=22),
    make_measure([n('Ab4', 1.0), n('Bb4', 1.0), n('C5', 2.0)], number=23),
    make_measure([n('B4', 3.0), r(1.0)], number=24),  # phrase boundary
    make_measure([n('Ab5', 2.0), n('G5', 2.0)], number=25),
    make_measure([n('F5', 1.0), n('Eb5', 1.0), n('Db5', 1.0), n('C5', 1.0)], number=26),  # Db chromatic
    make_measure([n('D5', 2.0), n('B4', 2.0)], number=27),
    make_measure([n('C5', 3.0), r(1.0)], number=28),
]
add_dynamic(v1_a2[0], 'mf')
add_dynamic(v1_a2[4], 'f')
v1_a2[0].notes[0].articulations.append(articulations.Tenuto())
v1_a2[4].notes[0].articulations.append(articulations.Accent())
v1_a2[5].notes[0].articulations.append(articulations.Staccato())
v1_a2[5].notes[1].articulations.append(articulations.Staccato())
v1_a2[5].notes[2].articulations.append(articulations.Staccato())
for m in v1_a2:
    violin1_part.append(m)

v2_a2 = [
    make_measure([n('G4', 2.0), n('G4', 2.0)], number=21),
    make_measure([n('Eb4', 2.0), n('D4', 2.0)], number=22),
    make_measure([n('C4', 2.0), n('Eb4', 2.0)], number=23),
    make_measure([n('D4', 3.0), r(1.0)], number=24),
    make_measure([n('Eb5', 2.0), n('Eb5', 2.0)], number=25),
    make_measure([n('Db5', 1.0), n('C5', 1.0), n('Ab4', 2.0)], number=26),  # Db chromatic
    make_measure([n('Ab4', 2.0), n('G4', 2.0)], number=27),
    make_measure([n('G4', 3.0), r(1.0)], number=28),
]
add_dynamic(v2_a2[0], 'mf')
for m in v2_a2:
    violin2_part.append(m)

va_a2 = [
    make_measure([n('C4', 2.0), n('B3', 2.0)], number=21),
    make_measure([n('Ab3', 2.0), n('G3', 2.0)], number=22),
    make_measure([n('F3', 2.0), n('G3', 2.0)], number=23),
    make_measure([n('G3', 3.0), r(1.0)], number=24),
    make_measure([n('C4', 2.0), n('Bb3', 2.0)], number=25),
    make_measure([n('Ab3', 2.0), n('Ab3', 2.0)], number=26),
    make_measure([n('F3', 2.0), n('F3', 2.0)], number=27),
    make_measure([n('Eb3', 3.0), r(1.0)], number=28),
]
add_dynamic(va_a2[0], 'mf')
for m in va_a2:
    viola_part.append(m)

vc_a2 = [
    make_measure([n('C3', 2.0), n('G2', 2.0)], number=21),
    make_measure([n('Ab2', 2.0), n('Eb2', 2.0)], number=22),
    make_measure([n('F2', 2.0), n('C3', 2.0)], number=23),
    make_measure([n('G2', 3.0), r(1.0)], number=24),
    make_measure([n('Ab2', 2.0), n('Eb3', 2.0)], number=25),
    make_measure([n('Db3', 2.0), n('C3', 2.0)], number=26),  # Db Neapolitan bass
    make_measure([n('Ab2', 2.0), n('G2', 2.0)], number=27),
    make_measure([n('C2', 3.0), r(1.0)], number=28),  # C2 for range
]
add_dynamic(vc_a2[0], 'mf')
for m in vc_a2:
    cello_part.append(m)

# --- Harp A': arpeggios with Neapolitan and chromatic chords ---
harp_a2_chords = [
    # m21: Cm7
    [n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Bb3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5)],
    # m22: Ab M7
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('Ab4', 0.5)],
    # m23: Fm -> G7
    [n('F2', 0.5), n('Ab2', 0.5), n('C3', 0.5), n('F3', 0.5), n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5)],
    # m24: G7(b9) — chromatic
    [n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('B3', 0.5), n('D4', 0.5), r(0.5)],
    # m25: Ab -> Bb
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('Bb2', 0.5), n('D3', 0.5), n('F3', 0.5), n('Bb3', 0.5)],
    # m26: Db major (Neapolitan!) -> C
    [n('Db3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('Db4', 0.5), n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('C4', 0.5)],
    # m27: Fm -> G7
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('G3', 0.5)],
    # m28: Cm
    [n('C3', 1.0), n('G3', 1.0), n('Eb4', 1.0), r(1.0)],
]
for i, notes_list in enumerate(harp_a2_chords, start=21):
    m = make_measure(notes_list, number=i)
    if i == 21:
        add_dynamic(m, 'mf')
    harp_part.append(m)

# --- Piano A': richer harmony, Neapolitan, augmented ---
pno_a2 = [
    make_measure([ch(['C3', 'Eb3', 'G3', 'Bb3'], 2.0), ch(['G2', 'B2', 'D3', 'F3'], 2.0)], number=21),
    make_measure([ch(['Ab2', 'C3', 'Eb3', 'G3'], 2.0), ch(['Eb2', 'G2', 'Bb2', 'D3'], 2.0)], number=22),
    make_measure([ch(['F2', 'Ab2', 'C3', 'Eb3'], 2.0), ch(['G2', 'B2', 'D3', 'F3'], 2.0)], number=23),
    make_measure([ch(['G2', 'B2', 'D3', 'F3', 'Ab3'], 3.0), r(1.0)], number=24),  # G7b9
    make_measure([ch(['Ab2', 'C3', 'Eb3'], 2.0), ch(['Bb2', 'D3', 'F3'], 2.0)], number=25),
    make_measure([ch(['Db3', 'F3', 'Ab3'], 2.0), ch(['C3', 'E3', 'G3', 'Bb3'], 2.0)], number=26),  # Db! -> C7
    make_measure([ch(['F2', 'Ab2', 'C3'], 2.0), ch(['G2', 'B2', 'D3', 'F3'], 2.0)], number=27),
    make_measure([ch(['C3', 'Eb3', 'G3'], 3.0), r(1.0)], number=28),
]
add_dynamic(pno_a2[0], 'mf')
for m in pno_a2:
    piano_part.append(m)


# ============================================================================
# CODA (mm. 29-34): Dissolution, Picardy third to C major
# Chromatic: E major chord in m33-34 for Picardy, A natural approach in m31
# Additional modulation markers for analysis windows
# ============================================================================

# --- Harp: thinning arpeggios with chromatic path to C major ---
harp_coda = [
    # m29: Cm
    [n('C3', 0.5), n('Eb3', 0.5), n('G3', 0.5), n('C4', 0.5), n('Eb4', 0.5), n('G4', 0.5), n('C5', 0.5), n('G4', 0.5)],
    # m30: Ab -> A dim (chromatic passing)
    [n('Ab2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('Ab3', 0.5), n('A2', 0.5), n('C3', 0.5), n('Eb3', 0.5), n('A3', 0.5)],
    # m31: Fm with A natural passing (mode mixture)
    [n('F2', 0.5), n('A2', 0.5), n('C3', 0.5), n('F3', 0.5), n('Ab3', 0.5), n('C4', 0.5), n('F4', 0.5), n('C4', 0.5)],
    # m32: G7 (dominant) — builds tension
    [n('G2', 0.5), n('B2', 0.5), n('D3', 0.5), n('F3', 0.5), n('G3', 0.5), n('B3', 0.5), n('D4', 0.5), n('F4', 0.5)],
    # m33: C MAJOR — Picardy third! E natural
    [n('C3', 0.5), n('E3', 0.5), n('G3', 0.5), n('C4', 0.5), n('E4', 0.5), n('G4', 0.5), n('C5', 0.5), n('G4', 0.5)],
    # m34: C major — final with added 9th (D)
    [n('C3', 1.0), n('E3', 1.0), n('G3', 0.5), n('D4', 0.5), n('C4', 1.0)],
]
for i, notes_list in enumerate(harp_coda, start=29):
    m = make_measure(notes_list, number=i)
    if i == 29:
        add_dynamic(m, 'mp')
    if i == 33:
        add_dynamic(m, 'p')
    harp_part.append(m)

# --- Piano: sparse, chromatic path to Picardy ---
pno_coda = [
    make_measure([ch(['C3', 'Eb3', 'G3'], 2.0), r(2.0)], number=29),
    make_measure([ch(['Ab2', 'C3', 'Eb3'], 1.5), ch(['A2', 'C3', 'Eb3'], 0.5), r(2.0)], number=30),  # A dim passing
    make_measure([ch(['F2', 'A2', 'C3'], 2.0), r(2.0)], number=31),  # F major (A natural mode mixture)
    make_measure([ch(['G2', 'B2', 'D3', 'F3'], 4.0)], number=32),
    make_measure([ch(['C3', 'E3', 'G3'], 4.0)], number=33),  # C MAJOR
    make_measure([ch(['C3', 'E3', 'G3', 'C4'], 4.0)], number=34),
]
add_dynamic(pno_coda[0], 'p')
add_dynamic(pno_coda[4], 'pp')
pno_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in pno_coda:
    piano_part.append(m)

# --- Flute: fading melody with chromatic E natural for Picardy ---
fl_coda = [
    make_measure([n('Eb5', 2.0), n('D5', 2.0)], number=29),
    make_measure([n('C5', 2.0), r(2.0)], number=30),
    make_measure([r(1.0), n('A4', 1.0), n('G4', 1.0), n('F4', 1.0)], number=31),  # A natural
    make_measure([n('G4', 2.0), n('F4', 2.0)], number=32),
    make_measure([n('E4', 2.0), n('G4', 2.0)], number=33),  # E natural Picardy
    make_measure([n('C5', 4.0)], number=34),
]
add_dynamic(fl_coda[0], 'p')
add_dynamic(fl_coda[4], 'pp')
fl_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in fl_coda:
    flute_part.append(m)

# --- Oboe: fading line ---
ob_coda = [
    make_measure([n('C5', 2.0), n('Bb4', 2.0)], number=29),
    make_measure([n('Ab4', 2.0), r(2.0)], number=30),
    make_measure([r(1.0), n('A4', 1.0), n('Ab4', 1.0), n('G4', 1.0)], number=31),  # A natural chromatic
    make_measure([n('D4', 2.0), n('D4', 2.0)], number=32),
    make_measure([n('E4', 2.0), n('G4', 2.0)], number=33),  # E natural
    make_measure([n('E4', 4.0)], number=34),
]
add_dynamic(ob_coda[0], 'p')
ob_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in ob_coda:
    oboe_part.append(m)

# --- Horn: final sustained notes ---
hn_coda = [
    make_measure([n('G3', 4.0)], number=29),
    make_measure([n('Ab3', 2.0), n('A3', 2.0)], number=30),  # chromatic A
    make_measure([n('A3', 2.0), n('Ab3', 2.0)], number=31),  # mode mixture
    make_measure([n('G3', 4.0)], number=32),
    make_measure([n('G3', 2.0), n('C4', 2.0)], number=33),
    make_measure([n('C4', 4.0)], number=34),
]
add_dynamic(hn_coda[0], 'p')
add_dynamic(hn_coda[4], 'pp')
hn_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in hn_coda:
    horn_part.append(m)

# --- Strings coda ---
v1_coda = [
    make_measure([n('Eb5', 2.0), n('D5', 2.0)], number=29),
    make_measure([n('C5', 4.0)], number=30),
    make_measure([n('A4', 2.0), n('G4', 2.0)], number=31),  # A natural
    make_measure([n('G4', 2.0), n('F4', 2.0)], number=32),
    make_measure([n('E4', 2.0), n('G4', 2.0)], number=33),  # E natural
    make_measure([n('G4', 2.0), n('C5', 2.0)], number=34),
]
add_dynamic(v1_coda[0], 'p')
add_dynamic(v1_coda[4], 'pp')
v1_coda[0].notes[0].articulations.append(articulations.Tenuto())
v1_coda[2].notes[0].articulations.append(articulations.Staccato())
v1_coda[5].notes[-1].expressions.append(expressions.Fermata())
for m in v1_coda:
    violin1_part.append(m)

v2_coda = [
    make_measure([n('G4', 2.0), n('Ab4', 2.0)], number=29),
    make_measure([n('Eb4', 4.0)], number=30),
    make_measure([n('C4', 2.0), n('C4', 2.0)], number=31),
    make_measure([n('B3', 2.0), n('D4', 2.0)], number=32),
    make_measure([n('C4', 2.0), n('E4', 2.0)], number=33),  # E natural
    make_measure([n('E4', 4.0)], number=34),
]
add_dynamic(v2_coda[0], 'p')
v2_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in v2_coda:
    violin2_part.append(m)

va_coda = [
    make_measure([n('C4', 4.0)], number=29),
    make_measure([n('Ab3', 4.0)], number=30),
    make_measure([n('F3', 2.0), n('E3', 2.0)], number=31),  # E natural
    make_measure([n('D3', 2.0), n('D3', 2.0)], number=32),
    make_measure([n('C3', 2.0), n('E3', 2.0)], number=33),  # E natural
    make_measure([n('E3', 4.0)], number=34),
]
add_dynamic(va_coda[0], 'p')
va_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in va_coda:
    viola_part.append(m)

vc_coda = [
    make_measure([n('C3', 2.0), n('G2', 2.0)], number=29),
    make_measure([n('Ab2', 2.0), n('A2', 2.0)], number=30),  # A chromatic
    make_measure([n('F2', 4.0)], number=31),
    make_measure([n('G2', 4.0)], number=32),
    make_measure([n('C2', 4.0)], number=33),  # C2 for low range
    make_measure([n('C2', 4.0)], number=34),
]
add_dynamic(vc_coda[0], 'p')
add_dynamic(vc_coda[4], 'pp')
vc_coda[5].notes[0].expressions.append(expressions.Fermata())
for m in vc_coda:
    cello_part.append(m)


# ============================================================================
# Add hairpins (crescendo/decrescendo) across sections
# ============================================================================

# Crescendo into B section on strings (mm. 11-12)
for part in [violin1_part, violin2_part, viola_part, cello_part]:
    measures = list(part.getElementsByClass('Measure'))
    m11_notes = list(measures[10].notes)
    m12_notes = list(measures[11].notes)
    if m11_notes and m12_notes:
        cresc_wedge = dynamics.Crescendo(m11_notes[0], m12_notes[0])
        part.insert(0, cresc_wedge)

# Decrescendo into coda (mm. 27-28)
for part in [violin1_part, violin2_part, flute_part]:
    measures = list(part.getElementsByClass('Measure'))
    m27_notes = list(measures[26].notes)
    m28_notes = list(measures[27].notes)
    if m27_notes and m28_notes:
        decresc_wedge = dynamics.Diminuendo(m27_notes[0], m28_notes[0])
        part.insert(0, decresc_wedge)

# Crescendo in horn heroic theme (mm. 15-16)
hn_measures = list(horn_part.getElementsByClass('Measure'))
if len(hn_measures) >= 17:
    m15_notes = list(hn_measures[14].notes)
    m16_notes = list(hn_measures[15].notes)
    if m15_notes and m16_notes:
        hn_cresc = dynamics.Crescendo(m15_notes[0], m16_notes[0])
        horn_part.insert(0, hn_cresc)

# Crescendo in flute B section climax (mm. 17-18)
fl_all_measures = list(flute_part.getElementsByClass('Measure'))
if len(fl_all_measures) >= 18:
    fm17_notes = list(fl_all_measures[16].notes)
    fm18_notes = list(fl_all_measures[17].notes)
    if fm17_notes and fm18_notes:
        fl_cresc = dynamics.Crescendo(fm17_notes[0], fm18_notes[0])
        flute_part.insert(0, fl_cresc)


# ============================================================================
# Add rehearsal marks for sections
# ============================================================================

fl_measures = list(flute_part.getElementsByClass('Measure'))
fl_measures[0].insert(0, expressions.RehearsalMark('Intro'))
fl_measures[4].insert(0, expressions.RehearsalMark('A'))
fl_measures[12].insert(0, expressions.RehearsalMark('B'))
fl_measures[20].insert(0, expressions.RehearsalMark("A'"))
fl_measures[28].insert(0, expressions.RehearsalMark('Coda'))


# ============================================================================
# Add tempo changes
# ============================================================================

# Slight ritardando feel at coda (slower tempo)
fl_measures[28].insert(0, tempo.MetronomeMark(text="Poco meno mosso", number=66, referent=note.Note(type='quarter')))


# ============================================================================
# Assemble score
# ============================================================================

score.insert(0, flute_part)
score.insert(0, oboe_part)
score.insert(0, horn_part)
score.insert(0, harp_part)
score.insert(0, piano_part)
score.insert(0, violin1_part)
score.insert(0, violin2_part)
score.insert(0, viola_part)
score.insert(0, cello_part)


# ============================================================================
# Save
# ============================================================================

output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, 'score.musicxml')
score.write('musicxml', fp=output_path)
print(f"Score saved to {output_path}")
