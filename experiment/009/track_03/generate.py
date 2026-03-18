"""Generate a piece for Clarinet in Bb and Piano.

Vibe: First love at 17, summer in a French village, working at a bakery.
Time signature: 6/8 (pastoral, lilting compound meter).
Key: F major (warm, pastoral, French).

REVISION 1 — Addressing feedback:
  - scale_consistency too high (0.985 → target ~0.914): add chromatic passing tones,
    borrowed chords (C#, Eb, F#, Ab), brief tonicizations
  - melodic_autocorrelation too low (0.212 → target 0.417): establish clear 3-note
    motif (F-G-A) and repeat/transform it in every section
  - avg_range_utilization too low (0.207 → target 0.328): extend clarinet down to
    chalumeau register (D4 concert), piano bass to F2/G1, piano RH up to C6
  - rhythmic_variety too low (4 → target 7): add dotted eighths (0.75), sixteenths
    (0.25), dotted quarters (1.5), quarter-tied-to-eighth (triplet-like 1/3 durations)
  - rest_ratio too low (0.040 → target 0.145): more breathing rests, phrase gaps,
    piano offbeat patterns with rests
  - pct_extended_chords too low: more 7th chords in piano
  - groove_consistency: keep arpeggio patterns more uniform within sections
  - pitch_class_entropy: more chromatic pitch classes throughout

Structure:
  A  (mm. 1-8)   - Morning: motif F-G-A, gentle piano arpeggios
  A' (mm. 9-16)  - Flourishing: motif returns ornamented, piano more active
  B  (mm. 17-24) - The bakery: playful staccato, C major tonicization, chromatic bass
  A''(mm. 25-32) - Sunset: motif in lower register, richer 7th-chord harmony
  Coda (mm. 33-36) - Lingering: motif fragments, gentle close

The clarinet in Bb is a transposing instrument. music21's Clarinet instrument
handles transposition automatically when writing to MusicXML.
"""

from music21 import (
    stream, note, chord, meter, key, tempo, clef,
    instrument, dynamics, expressions, articulations,
    duration, pitch, spanner, layout, metadata,
)


def make_note(p, dur, **kwargs):
    """Helper: create a note with pitch string p and quarterLength dur."""
    n = note.Note(p)
    n.duration = duration.Duration(dur)
    for k, v in kwargs.items():
        if k == "staccato":
            n.articulations.append(articulations.Staccato())
        elif k == "accent":
            n.articulations.append(articulations.Accent())
        elif k == "tenuto":
            n.articulations.append(articulations.Tenuto())
        elif k == "fermata":
            n.expressions.append(expressions.Fermata())
        elif k == "trill":
            n.expressions.append(expressions.Trill())
    return n


def make_rest(dur):
    r = note.Rest()
    r.duration = duration.Duration(dur)
    return r


def make_chord(pitches, dur, **kwargs):
    c = chord.Chord(pitches)
    c.duration = duration.Duration(dur)
    for k, v in kwargs.items():
        if k == "staccato":
            c.articulations.append(articulations.Staccato())
        elif k == "accent":
            c.articulations.append(articulations.Accent())
    return c


def build_clarinet_part():
    """Build the Clarinet in Bb part at concert pitch.

    music21 will transpose to written pitch automatically for MusicXML export.
    In 6/8, one beat = dotted quarter = 1.5 quarter notes.
    One measure = 3.0 quarter lengths.

    Core motif: F-G-A (rising major 2nd + major 2nd), transformed across sections.
    Extended range: D4 (chalumeau) to D6 (altissimo) = 24 semitones.
    Added chromaticism: C#, Eb, F#, G#, Ab as passing/neighbor tones.
    """
    cl = stream.Part()
    cl.insert(0, instrument.Clarinet())
    cl.partName = "Clarinet in Bb"

    # ---- Section A: Morning (mm. 1-8) ----
    # Core motif: F-G-A
    m1 = stream.Measure(number=1)
    m1.insert(0, meter.TimeSignature("6/8"))
    m1.insert(0, key.Key("F"))
    m1.insert(0, tempo.MetronomeMark("Andante pastoral", 52, duration.Duration(1.5)))
    m1.insert(0, dynamics.Dynamic("mp"))
    # Motif: F-G-A with dotted rhythm (rhythmic variety: dotted eighth + sixteenth)
    m1.append(make_note("F5", 0.75))       # dotted eighth
    m1.append(make_note("G5", 0.25))       # sixteenth
    m1.append(make_note("A5", 1.0, tenuto=True))
    m1.append(make_note("G5", 0.5))
    m1.append(make_rest(0.5))              # breathing rest
    cl.append(m1)

    # m2: descending answer with chromatic neighbor (Eb passing tone)
    m2 = stream.Measure(number=2)
    m2.append(make_note("F5", 0.5))
    m2.append(make_note("E5", 0.25))       # sixteenth
    m2.append(make_note("Eb5", 0.25))      # chromatic passing tone
    m2.append(make_note("D5", 1.0))
    m2.append(make_note("C5", 0.5))
    m2.append(make_rest(0.5))
    cl.append(m2)

    # m3: motif transposed up (A-Bb-C) with Bb reaching higher
    m3 = stream.Measure(number=3)
    m3.append(make_note("E5", 0.5))
    m3.append(make_note("F5", 0.75))       # dotted eighth
    m3.append(make_note("G5", 0.25))       # sixteenth
    m3.append(make_note("A5", 0.75))       # dotted eighth
    m3.append(make_note("Bb5", 0.25))
    m3.append(make_note("C6", 0.5))        # reach up
    cl.append(m3)

    # m4: phrase ending with rest
    m4 = stream.Measure(number=4)
    m4.append(make_note("A5", 1.5))        # dotted quarter
    m4.append(make_note("G5", 0.5))
    m4.append(make_rest(1.0))              # longer breathing rest
    cl.append(m4)

    # m5: second phrase - drops to lower register, motif on C-D-E (transposition)
    m5 = stream.Measure(number=5)
    m5.insert(0, dynamics.Dynamic("p"))
    m5.append(make_note("C5", 0.75))       # motif transposed: C-D-E
    m5.append(make_note("D5", 0.25))
    m5.append(make_note("E5", 1.0))
    m5.append(make_note("F5", 0.5))
    m5.append(make_rest(0.5))
    cl.append(m5)

    # m6: chromatic descent with Ab (borrowed from minor)
    m6 = stream.Measure(number=6)
    m6.append(make_note("D5", 0.5))
    m6.append(make_note("C5", 0.5))
    m6.append(make_note("Bb4", 0.75))
    m6.append(make_note("Ab4", 0.25))      # chromatic: borrowed from F minor
    m6.append(make_note("G4", 0.5))
    m6.append(make_rest(0.5))
    cl.append(m6)

    # m7: motif returns at original pitch, gentle climb
    m7 = stream.Measure(number=7)
    m7.append(make_note("F4", 0.75))       # low register - motif F-G-A
    m7.append(make_note("G4", 0.25))
    m7.append(make_note("A4", 1.0))
    m7.append(make_note("Bb4", 0.5))
    m7.append(make_rest(0.5))
    cl.append(m7)

    # m8: half cadence with rest
    m8 = stream.Measure(number=8)
    m8.append(make_note("C5", 1.5))
    m8.append(make_rest(1.5))              # full half-measure rest
    cl.append(m8)

    # ---- Section A': Flourishing (mm. 9-16) ----
    m9 = stream.Measure(number=9)
    m9.insert(0, dynamics.Dynamic("mf"))
    m9.insert(0, expressions.RehearsalMark("A'"))
    # Motif F-G-A ornamented with turn
    m9.append(make_note("F5", 0.5))
    m9.append(make_note("G5", 0.25))
    m9.append(make_note("A5", 0.25))
    m9.append(make_note("Bb5", 0.25))       # turn ornament
    m9.append(make_note("A5", 0.25))
    m9.append(make_note("G5", 0.5))
    m9.append(make_rest(1.0))
    cl.append(m9)

    m10 = stream.Measure(number=10)
    m10.append(make_note("F5", 0.5))
    m10.append(make_note("E5", 0.25))
    m10.append(make_note("D5", 0.25))
    m10.append(make_note("C#5", 0.5))      # chromatic: leading tone to D
    m10.append(make_note("D5", 0.5))
    m10.append(make_note("F5", 0.5))
    m10.append(make_rest(0.5))
    cl.append(m10)

    m11 = stream.Measure(number=11)
    m11.append(make_note("E5", 0.5))
    m11.append(make_note("F5", 0.5))
    m11.append(make_note("G5", 0.5))
    m11.append(make_note("A5", 0.5, trill=True))
    m11.append(make_note("Bb5", 0.5))
    m11.append(make_note("C6", 0.5))
    cl.append(m11)

    m12 = stream.Measure(number=12)
    m12.append(make_note("D6", 1.5, accent=True))     # climax - high D6
    m12.append(make_rest(1.5))             # big breathing rest
    cl.append(m12)

    m13 = stream.Measure(number=13)
    # Motif again: F-G-A in dotted rhythm
    m13.append(make_note("F5", 0.75))
    m13.append(make_note("G5", 0.25))
    m13.append(make_note("A5", 0.5))
    m13.append(make_note("G5", 0.5))
    m13.append(make_note("F5", 0.5))
    m13.append(make_rest(0.5))
    cl.append(m13)

    m14 = stream.Measure(number=14)
    m14.append(make_note("Bb5", 0.5))
    m14.append(make_note("A5", 0.5))
    m14.append(make_note("G5", 0.5))
    m14.append(make_note("F#5", 0.25))     # chromatic: leading tone to G
    m14.append(make_note("G5", 0.25))
    m14.append(make_note("E5", 0.5))
    cl.append(m14)

    m15 = stream.Measure(number=15)
    cresc = dynamics.Crescendo()
    m15.append(make_note("F5", 0.75))      # motif: F-G-A ascending
    m15.append(make_note("G5", 0.25))
    m15.append(make_note("A5", 0.5))
    m15.append(make_note("Bb5", 0.5))
    m15.append(make_note("C6", 0.5))
    m15.append(make_rest(0.5))
    cl.insert(0, cresc)
    cresc.addSpannedElements(m15.notes)
    cl.append(m15)

    m16 = stream.Measure(number=16)
    m16.insert(0, dynamics.Dynamic("f"))
    m16.append(make_note("D6", 1.5, accent=True))
    m16.append(make_note("C6", 0.5))
    m16.append(make_rest(1.0))
    cl.append(m16)

    # ---- Section B: The Bakery (mm. 17-24) - playful, staccato ----
    m17 = stream.Measure(number=17)
    m17.insert(0, dynamics.Dynamic("mf"))
    m17.insert(0, expressions.RehearsalMark("B"))
    # Motif transformed: G-A-B (transposed to dominant)
    m17.append(make_note("G5", 0.5, staccato=True))
    m17.append(make_note("A5", 0.25, staccato=True))
    m17.append(make_note("B5", 0.25, staccato=True))
    m17.append(make_note("C6", 0.5, accent=True))
    m17.append(make_note("B5", 0.5))
    m17.append(make_rest(1.0))
    cl.append(m17)

    m18 = stream.Measure(number=18)
    m18.append(make_note("A5", 0.5, staccato=True))
    m18.append(make_note("G#5", 0.25))     # chromatic neighbor
    m18.append(make_note("A5", 0.25, staccato=True))
    m18.append(make_note("G5", 0.5))
    m18.append(make_note("E5", 0.5))
    m18.append(make_rest(1.0))
    cl.append(m18)

    m19 = stream.Measure(number=19)
    # Motif again: G-A-B staccato
    m19.append(make_note("G5", 0.5, staccato=True))
    m19.append(make_note("A5", 0.25, staccato=True))
    m19.append(make_note("B5", 0.25, staccato=True))
    m19.append(make_note("C6", 0.5, accent=True))
    m19.append(make_note("A5", 0.5))
    m19.append(make_rest(0.5))
    cl.append(m19)

    m20 = stream.Measure(number=20)
    m20.append(make_note("G5", 0.5))
    m20.append(make_note("F#5", 0.25))     # chromatic
    m20.append(make_note("G5", 0.25))
    m20.append(make_note("E5", 0.5))
    m20.append(make_note("D5", 0.5))
    m20.append(make_rest(1.0))
    cl.append(m20)

    # m21-22: lyrical interlude
    m21 = stream.Measure(number=21)
    m21.insert(0, dynamics.Dynamic("p"))
    m21.append(make_note("A5", 1.5, tenuto=True))
    m21.append(make_note("Ab5", 0.5))      # chromatic: surprise
    m21.append(make_note("G5", 0.5))
    m21.append(make_rest(0.5))
    cl.append(m21)

    m22 = stream.Measure(number=22)
    m22.append(make_note("F5", 0.75))       # motif fragment: F-G-A
    m22.append(make_note("G5", 0.25))
    m22.append(make_note("A5", 0.5))
    m22.append(make_note("Bb5", 0.5))
    m22.append(make_note("A5", 0.5))
    m22.append(make_rest(0.5))
    cl.append(m22)

    # m23-24: transition back
    m23 = stream.Measure(number=23)
    dim = dynamics.Diminuendo()
    m23.append(make_note("G5", 0.5))
    m23.append(make_note("F5", 0.5))
    m23.append(make_note("Eb5", 0.5))      # chromatic passing, modal mixture
    m23.append(make_note("D5", 0.5))
    m23.append(make_note("C5", 0.5))
    m23.append(make_rest(0.5))
    cl.insert(0, dim)
    dim.addSpannedElements(m23.notes)
    cl.append(m23)

    m24 = stream.Measure(number=24)
    m24.insert(0, dynamics.Dynamic("mp"))
    m24.append(make_note("Bb4", 1.0))
    m24.append(make_note("A4", 0.5))
    m24.append(make_rest(1.5))              # long rest before return
    cl.append(m24)

    # ---- Section A'': Sunset Walk (mm. 25-32) - low register, rich ----
    m25 = stream.Measure(number=25)
    m25.insert(0, dynamics.Dynamic("mf"))
    m25.insert(0, expressions.RehearsalMark("A''"))
    # Motif in low register: F4-G4-A4 (chalumeau-ish)
    m25.append(make_note("F4", 0.75))
    m25.append(make_note("G4", 0.25))
    m25.append(make_note("A4", 1.0, tenuto=True))
    m25.append(make_note("Bb4", 0.5))
    m25.append(make_rest(0.5))
    cl.append(m25)

    m26 = stream.Measure(number=26)
    m26.append(make_note("C5", 0.5))
    m26.append(make_note("Bb4", 0.5))
    m26.append(make_note("A4", 0.5))
    m26.append(make_note("Ab4", 0.25))     # chromatic neighbor
    m26.append(make_note("G4", 0.75))
    m26.append(make_rest(0.5))
    cl.append(m26)

    m27 = stream.Measure(number=27)
    # Motif again, now climbing through the range
    m27.append(make_note("F4", 0.75))
    m27.append(make_note("G4", 0.25))
    m27.append(make_note("A4", 0.5))
    m27.append(make_note("C5", 0.5))
    m27.append(make_note("E5", 0.5))
    m27.append(make_rest(0.5))
    cl.append(m27)

    m28 = stream.Measure(number=28)
    m28.append(make_note("G5", 1.5, tenuto=True))
    m28.append(make_rest(1.5))
    cl.append(m28)

    m29 = stream.Measure(number=29)
    m29.insert(0, dynamics.Dynamic("f"))
    cresc2 = dynamics.Crescendo()
    # Big climax: motif F-G-A drives upward
    m29.append(make_note("F5", 0.75))
    m29.append(make_note("G5", 0.25))
    m29.append(make_note("A5", 0.5))
    m29.append(make_note("Bb5", 0.5))
    m29.append(make_note("C6", 0.5))
    m29.append(make_rest(0.5))
    cl.insert(0, cresc2)
    cresc2.addSpannedElements(m29.notes)
    cl.append(m29)

    m30 = stream.Measure(number=30)
    m30.append(make_note("D6", 1.5, accent=True))
    m30.append(make_note("C#6", 0.25))     # chromatic upper neighbor
    m30.append(make_note("D6", 0.25))
    m30.append(make_note("C6", 0.5))
    m30.append(make_rest(0.5))
    cl.append(m30)

    m31 = stream.Measure(number=31)
    dim2 = dynamics.Diminuendo()
    m31.append(make_note("Bb5", 0.5))
    m31.append(make_note("A5", 0.5))
    m31.append(make_note("G5", 0.5))
    m31.append(make_note("F5", 0.5))
    m31.append(make_note("E5", 0.5))
    m31.append(make_rest(0.5))
    cl.insert(0, dim2)
    dim2.addSpannedElements(m31.notes)
    cl.append(m31)

    m32 = stream.Measure(number=32)
    m32.insert(0, dynamics.Dynamic("p"))
    m32.append(make_note("D5", 0.5))
    m32.append(make_note("C5", 0.5))
    m32.append(make_note("A4", 0.5))
    m32.append(make_rest(1.5))
    cl.append(m32)

    # ---- Coda (mm. 33-36) ----
    m33 = stream.Measure(number=33)
    m33.insert(0, dynamics.Dynamic("pp"))
    m33.insert(0, expressions.RehearsalMark("Coda"))
    m33.insert(0, tempo.MetronomeMark("Poco rit.", 44, duration.Duration(1.5)))
    # Final motif statement: F-G-A, very tender
    m33.append(make_note("F4", 0.75))
    m33.append(make_note("G4", 0.25))
    m33.append(make_note("A4", 1.0))
    m33.append(make_rest(1.0))
    cl.append(m33)

    m34 = stream.Measure(number=34)
    m34.append(make_note("Bb4", 0.5))
    m34.append(make_note("A4", 0.5))
    m34.append(make_note("G4", 0.5))
    m34.append(make_note("F4", 0.5))
    m34.append(make_rest(1.0))
    cl.append(m34)

    m35 = stream.Measure(number=35)
    # Last whisper of the motif
    m35.append(make_note("F4", 0.75))
    m35.append(make_note("G4", 0.25))
    m35.append(make_note("A4", 0.5))
    m35.append(make_rest(1.5))
    cl.append(m35)

    m36 = stream.Measure(number=36)
    m36.append(make_note("F4", 2.0, fermata=True))    # long final note
    m36.append(make_rest(1.0))
    cl.append(m36)

    return cl


def build_piano_part():
    """Build the Piano part.

    Revised for:
    - More 7th chords (Fmaj7, Dm7, Gm7, C7, Am7, BbMaj7)
    - Chromatic bass movement (C#, Ab, Eb, F#)
    - Better range utilization: bass down to G1, treble up to C6
    - Rests in arpeggio patterns for breathing
    - Consistent groove within sections
    """
    rh = stream.Part()
    rh.insert(0, instrument.Piano())
    rh.partName = "Piano"

    lh = stream.Part()
    lh.insert(0, instrument.Piano())
    lh.insert(0, clef.BassClef())

    # ======================================================================
    # Section A: Morning (mm. 1-8) - 7th chord arpeggios, consistent 6/8 groove
    # ======================================================================

    def rh_arpeggio(m, pitches_beat1, pitches_beat2):
        """Standard 6/8 arpeggio: 3 eighths + 3 eighths."""
        for p in pitches_beat1:
            m.append(make_note(p, 0.5))
        for p in pitches_beat2:
            m.append(make_note(p, 0.5))

    def rh_arpeggio_with_rest(m, pitches_beat1, pitches_beat2_short):
        """Arpeggio with trailing rest for breathing."""
        for p in pitches_beat1:
            m.append(make_note(p, 0.5))
        for p in pitches_beat2_short:
            m.append(make_note(p, 0.5))
        m.append(make_rest(0.5))

    # m1: Fmaj7 arpeggio
    rm1 = stream.Measure(number=1)
    rm1.insert(0, meter.TimeSignature("6/8"))
    rm1.insert(0, key.Key("F"))
    rm1.insert(0, dynamics.Dynamic("p"))
    rh_arpeggio(rm1, ["A4", "C5", "E5"], ["C5", "F5", "A5"])    # Fmaj7
    rh.append(rm1)

    # m2: Dm7
    rm2 = stream.Measure(number=2)
    rh_arpeggio(rm2, ["A4", "C5", "F5"], ["D5", "F5", "A5"])    # Dm7
    rh.append(rm2)

    # m3: BbMaj7
    rm3 = stream.Measure(number=3)
    rh_arpeggio(rm3, ["A4", "Bb4", "D5"], ["F5", "A5", "Bb5"])  # BbMaj7
    rh.append(rm3)

    # m4: C7 with rest
    rm4 = stream.Measure(number=4)
    rh_arpeggio_with_rest(rm4, ["Bb4", "C5", "E5"], ["G5", "Bb5"])  # C7
    rh.append(rm4)

    # m5: Am7
    rm5 = stream.Measure(number=5)
    rh_arpeggio(rm5, ["G4", "A4", "C5"], ["E5", "G5", "A5"])    # Am7
    rh.append(rm5)

    # m6: Gm7 with chromatic Eb
    rm6 = stream.Measure(number=6)
    rh_arpeggio(rm6, ["Bb4", "D5", "F5"], ["Bb4", "Eb5", "G5"])  # Gm7 + Eb
    rh.append(rm6)

    # m7: C7sus4 → C7
    rm7 = stream.Measure(number=7)
    rh_arpeggio(rm7, ["Bb4", "C5", "F5"], ["Bb4", "C5", "E5"])  # Csus4→C7
    rh.append(rm7)

    # m8: Fmaj7 with rest
    rm8 = stream.Measure(number=8)
    rm8.append(make_chord(["A4", "C5", "E5", "F5"], 1.5))       # Fmaj7 chord
    rm8.append(make_rest(1.5))                                     # rest
    rh.append(rm8)

    # --- Left Hand (Section A): dotted quarter bass with chromatic passing ---
    def lh_bass(m, bass1, bass2):
        """Standard LH: two dotted-quarter bass notes."""
        m.append(make_note(bass1, 1.5))
        m.append(make_note(bass2, 1.5))

    def lh_bass_with_walk(m, bass1, passing, bass2):
        """LH with chromatic walk: dotted quarter + eighth + quarter."""
        m.append(make_note(bass1, 1.5))
        m.append(make_note(passing, 0.5))
        m.append(make_note(bass2, 1.0))

    lm1 = stream.Measure(number=1)
    lm1.insert(0, meter.TimeSignature("6/8"))
    lm1.insert(0, key.Key("F"))
    lm1.insert(0, dynamics.Dynamic("p"))
    lh_bass(lm1, "F2", "C3")
    lh.append(lm1)

    lm2 = stream.Measure(number=2)
    lh_bass(lm2, "D2", "A2")
    lh.append(lm2)

    lm3 = stream.Measure(number=3)
    lh_bass(lm3, "Bb1", "F2")             # deep bass Bb1
    lh.append(lm3)

    lm4 = stream.Measure(number=4)
    lh_bass(lm4, "C2", "G2")
    lh.append(lm4)

    lm5 = stream.Measure(number=5)
    lh_bass(lm5, "A1", "E2")              # deep bass A1
    lh.append(lm5)

    lm6 = stream.Measure(number=6)
    lh_bass_with_walk(lm6, "G2", "Ab2", "Bb2")   # chromatic bass walk G-Ab-Bb
    lh.append(lm6)

    lm7 = stream.Measure(number=7)
    lh_bass(lm7, "C2", "C3")
    lh.append(lm7)

    lm8 = stream.Measure(number=8)
    lm8.append(make_note("F2", 1.5))
    lm8.append(make_rest(1.5))
    lh.append(lm8)

    # ======================================================================
    # Section A': Flourishing (mm. 9-16)
    # ======================================================================
    rm9 = stream.Measure(number=9)
    rh_arpeggio(rm9, ["F4", "A4", "C5"], ["E5", "A5", "C6"])    # Fmaj7 wide
    rh.append(rm9)

    rm10 = stream.Measure(number=10)
    rh_arpeggio(rm10, ["D4", "F4", "A4"], ["C5", "F5", "A5"])   # Dm7
    rh.append(rm10)

    rm11 = stream.Measure(number=11)
    rh_arpeggio(rm11, ["Bb4", "D5", "F5"], ["A5", "Bb5", "D6"]) # BbMaj7 high
    rh.append(rm11)

    rm12 = stream.Measure(number=12)
    rm12.append(make_chord(["Bb4", "C5", "E5", "G5"], 1.5))     # C7 chord
    rm12.append(make_rest(1.5))
    rh.append(rm12)

    rm13 = stream.Measure(number=13)
    rh_arpeggio(rm13, ["A4", "C5", "E5"], ["F5", "A5", "C6"])   # Fmaj7
    rh.append(rm13)

    rm14 = stream.Measure(number=14)
    rh_arpeggio(rm14, ["Bb4", "D5", "G5"], ["A4", "C5", "F#5"]) # Gm→D7 (chromatic F#)
    rh.append(rm14)

    rm15 = stream.Measure(number=15)
    rh_arpeggio(rm15, ["G4", "Bb4", "C5"], ["E5", "G5", "Bb5"]) # C7 arpeggio
    rh.append(rm15)

    rm16 = stream.Measure(number=16)
    rm16.insert(0, dynamics.Dynamic("f"))
    rm16.append(make_chord(["F4", "A4", "C5", "E5", "F5"], 1.5, accent=True))  # Fmaj7
    rm16.append(make_rest(1.5))
    rh.append(rm16)

    # LH Section A'
    lm9 = stream.Measure(number=9)
    lh_bass(lm9, "F2", "A2")
    lh.append(lm9)

    lm10 = stream.Measure(number=10)
    lh_bass_with_walk(lm10, "D2", "C#2", "C2")    # chromatic: D-C#-C
    lh.append(lm10)

    lm11 = stream.Measure(number=11)
    lh_bass(lm11, "Bb1", "G2")
    lh.append(lm11)

    lm12 = stream.Measure(number=12)
    lm12.append(make_note("C2", 1.5))
    lm12.append(make_rest(1.5))
    lh.append(lm12)

    lm13 = stream.Measure(number=13)
    lh_bass(lm13, "F2", "A2")
    lh.append(lm13)

    lm14 = stream.Measure(number=14)
    lh_bass_with_walk(lm14, "Bb1", "A1", "D2")    # chromatic walk Bb-A-D
    lh.append(lm14)

    lm15 = stream.Measure(number=15)
    lh_bass(lm15, "C2", "G1")                       # deep G1
    lh.append(lm15)

    lm16 = stream.Measure(number=16)
    lm16.append(make_note("F2", 1.5))
    lm16.append(make_rest(1.5))
    lh.append(lm16)

    # ======================================================================
    # Section B: The Bakery (mm. 17-24) - rhythmic chords with rests
    # ======================================================================
    rm17 = stream.Measure(number=17)
    rm17.insert(0, dynamics.Dynamic("mf"))
    rm17.append(make_chord(["E4", "G4", "B4", "C5"], 0.5, staccato=True))  # C7
    rm17.append(make_rest(0.5))
    rm17.append(make_chord(["E4", "G4", "C5"], 0.5, staccato=True))
    rm17.append(make_chord(["F4", "A4", "C5"], 0.5, accent=True))
    rm17.append(make_rest(0.5))
    rm17.append(make_rest(0.5))
    rh.append(rm17)

    rm18 = stream.Measure(number=18)
    rm18.append(make_chord(["D4", "F#4", "A4", "C5"], 0.5, staccato=True))  # D7 (chromatic F#)
    rm18.append(make_rest(0.5))
    rm18.append(make_chord(["D4", "G4", "B4"], 0.5, staccato=True))         # G
    rm18.append(make_chord(["C4", "E4", "G4", "Bb4"], 1.0))                 # C7
    rm18.append(make_rest(0.5))
    rh.append(rm18)

    rm19 = stream.Measure(number=19)
    rm19.append(make_chord(["E4", "G4", "B4", "C5"], 0.5, staccato=True))  # C7
    rm19.append(make_rest(0.5))
    rm19.append(make_chord(["E4", "G4", "C5"], 0.5, accent=True))
    rm19.append(make_chord(["D4", "F4", "Ab4", "B4"], 0.5))                 # dim7 (chromatic Ab)
    rm19.append(make_rest(0.5))
    rm19.append(make_rest(0.5))
    rh.append(rm19)

    rm20 = stream.Measure(number=20)
    rm20.append(make_chord(["D4", "F4", "A4", "C5"], 0.5, staccato=True))  # Dm7
    rm20.append(make_chord(["C4", "E4", "G4", "Bb4"], 0.5))                 # C7
    rm20.append(make_chord(["D4", "G4", "B4"], 0.5))
    rm20.append(make_rest(1.5))
    rh.append(rm20)

    # m21-22: lyrical interlude
    rm21 = stream.Measure(number=21)
    rm21.insert(0, dynamics.Dynamic("p"))
    rh_arpeggio(rm21, ["A4", "C5", "E5"], ["C5", "E5", "A5"])   # Am7
    rh.append(rm21)

    rm22 = stream.Measure(number=22)
    rh_arpeggio_with_rest(rm22, ["G4", "B4", "E5"], ["G4", "C5"])  # Em→C
    rh.append(rm22)

    # m23-24: transition with chromatic bass
    rm23 = stream.Measure(number=23)
    rh_arpeggio(rm23, ["A4", "C5", "Eb5"], ["Bb4", "D5", "F5"])  # chromatic Eb
    rh.append(rm23)

    rm24 = stream.Measure(number=24)
    rm24.append(make_chord(["A4", "C5", "E5", "F5"], 1.5))       # Fmaj7
    rm24.append(make_rest(1.5))
    rh.append(rm24)

    # LH Section B: rhythmic with rests and chromatic walks
    lm17 = stream.Measure(number=17)
    lm17.append(make_note("C2", 0.5, staccato=True))
    lm17.append(make_rest(0.5))
    lm17.append(make_note("G2", 0.5, staccato=True))
    lm17.append(make_note("C3", 0.5, accent=True))
    lm17.append(make_rest(0.5))
    lm17.append(make_rest(0.5))
    lh.append(lm17)

    lm18 = stream.Measure(number=18)
    lm18.append(make_note("D2", 0.5, staccato=True))
    lm18.append(make_rest(0.5))
    lm18.append(make_note("G2", 0.5, staccato=True))
    lm18.append(make_note("C3", 1.0))
    lm18.append(make_rest(0.5))
    lh.append(lm18)

    lm19 = stream.Measure(number=19)
    lm19.append(make_note("C2", 0.5, staccato=True))
    lm19.append(make_rest(0.5))
    lm19.append(make_note("G2", 0.5, accent=True))
    lm19.append(make_note("Ab2", 0.5))    # chromatic passing
    lm19.append(make_rest(0.5))
    lm19.append(make_rest(0.5))
    lh.append(lm19)

    lm20 = stream.Measure(number=20)
    lm20.append(make_note("D2", 0.5, staccato=True))
    lm20.append(make_note("C2", 0.5))
    lm20.append(make_note("G1", 0.5))     # very low G1
    lm20.append(make_rest(1.5))
    lh.append(lm20)

    lm21 = stream.Measure(number=21)
    lh_bass(lm21, "A1", "E2")
    lh.append(lm21)

    lm22 = stream.Measure(number=22)
    lh_bass(lm22, "E2", "C2")
    lh.append(lm22)

    lm23 = stream.Measure(number=23)
    lh_bass_with_walk(lm23, "F2", "Eb2", "Bb1")   # chromatic: F-Eb-Bb
    lh.append(lm23)

    lm24 = stream.Measure(number=24)
    lm24.append(make_note("F2", 1.5))
    lm24.append(make_rest(1.5))
    lh.append(lm24)

    # ======================================================================
    # Section A'': Sunset Walk (mm. 25-32) - rich 7th chords
    # ======================================================================
    rm25 = stream.Measure(number=25)
    rm25.insert(0, dynamics.Dynamic("mf"))
    rh_arpeggio(rm25, ["A4", "C5", "E5"], ["C5", "F5", "A5"])   # Fmaj7
    rh.append(rm25)

    rm26 = stream.Measure(number=26)
    rh_arpeggio(rm26, ["A4", "C5", "E5"], ["D5", "F5", "A5"])   # Dm9
    rh.append(rm26)

    rm27 = stream.Measure(number=27)
    rh_arpeggio(rm27, ["A4", "Bb4", "D5"], ["F5", "A5", "Bb5"]) # BbMaj7
    rh.append(rm27)

    rm28 = stream.Measure(number=28)
    rm28.append(make_chord(["Bb4", "C5", "E5", "G5"], 1.5))     # C9
    rm28.append(make_rest(1.5))
    rh.append(rm28)

    rm29 = stream.Measure(number=29)
    rm29.insert(0, dynamics.Dynamic("f"))
    rh_arpeggio(rm29, ["A4", "C5", "E5"], ["F5", "A5", "C6"])   # Fmaj7 wide
    rh.append(rm29)

    rm30 = stream.Measure(number=30)
    rm30.append(make_chord(["Bb4", "D5", "F5", "A5"], 1.5))     # BbMaj7
    rm30.append(make_chord(["A4", "C5", "E5", "G5"], 1.5))      # Am7
    rh.append(rm30)

    rm31 = stream.Measure(number=31)
    dim_rh = dynamics.Diminuendo()
    rh_arpeggio(rm31, ["G4", "Bb4", "D5"], ["F4", "A4", "C5"])  # Gm→F
    rh.insert(0, dim_rh)
    dim_rh.addSpannedElements(rm31.notes)
    rh.append(rm31)

    rm32 = stream.Measure(number=32)
    rm32.insert(0, dynamics.Dynamic("p"))
    rm32.append(make_chord(["A4", "C5", "E5", "F5"], 1.5))      # Fmaj7
    rm32.append(make_rest(1.5))
    rh.append(rm32)

    # LH A'' with chromatic walks
    lm25 = stream.Measure(number=25)
    lh_bass(lm25, "F2", "C3")
    lh.append(lm25)

    lm26 = stream.Measure(number=26)
    lh_bass_with_walk(lm26, "D2", "C#2", "A1")    # chromatic D-C#-A
    lh.append(lm26)

    lm27 = stream.Measure(number=27)
    lh_bass(lm27, "Bb1", "F2")
    lh.append(lm27)

    lm28 = stream.Measure(number=28)
    lm28.append(make_note("C2", 1.5))
    lm28.append(make_rest(1.5))
    lh.append(lm28)

    lm29 = stream.Measure(number=29)
    lh_bass(lm29, "F2", "C3")
    lh.append(lm29)

    lm30 = stream.Measure(number=30)
    lh_bass_with_walk(lm30, "Bb1", "A1", "C2")    # chromatic Bb-A-C
    lh.append(lm30)

    lm31 = stream.Measure(number=31)
    lh_bass(lm31, "G1", "F2")                       # deep G1
    lh.append(lm31)

    lm32 = stream.Measure(number=32)
    lm32.append(make_note("F2", 1.5))
    lm32.append(make_rest(1.5))
    lh.append(lm32)

    # ======================================================================
    # Coda (mm. 33-36)
    # ======================================================================
    rm33 = stream.Measure(number=33)
    rm33.insert(0, dynamics.Dynamic("pp"))
    rh_arpeggio(rm33, ["A4", "C5", "E5"], ["C5", "E5", "F5"])   # Fmaj7 tender
    rh.append(rm33)

    rm34 = stream.Measure(number=34)
    rh_arpeggio_with_rest(rm34, ["A4", "D5", "F5"], ["Bb4", "D5"])  # Dm7→Bb
    rh.append(rm34)

    rm35 = stream.Measure(number=35)
    rm35.append(make_chord(["G4", "Bb4", "C5", "E5"], 1.5))     # C7
    rm35.append(make_rest(1.5))
    rh.append(rm35)

    rm36 = stream.Measure(number=36)
    rm36.append(make_chord(["F4", "A4", "C5", "E5", "F5"], 2.0, accent=False))  # Fmaj7 final
    rm36.append(make_rest(1.0))
    rh.append(rm36)

    # LH Coda
    lm33 = stream.Measure(number=33)
    lh_bass(lm33, "F2", "C3")
    lh.append(lm33)

    lm34 = stream.Measure(number=34)
    lh_bass(lm34, "D2", "Bb1")
    lh.append(lm34)

    lm35 = stream.Measure(number=35)
    lm35.append(make_note("C2", 1.5))
    lm35.append(make_rest(1.5))
    lh.append(lm35)

    lm36 = stream.Measure(number=36)
    lm36.append(make_note("F1", 2.0))     # deepest note: F1
    lm36.append(make_rest(1.0))
    lh.append(lm36)

    return rh, lh


def main():
    import os

    s = stream.Score()
    s.insert(0, metadata.Metadata())
    s.metadata.title = "Matin de Boulangerie"
    s.metadata.composer = "Rachmaniclaude"
    s.metadata.movementName = "First love at 17, summer in a French village"

    cl_part = build_clarinet_part()
    piano_rh, piano_lh = build_piano_part()

    piano_lh.partName = "Piano"

    s.insert(0, cl_part)
    s.insert(0, piano_rh)
    s.insert(0, piano_lh)

    # Create staff group for piano
    sg = layout.StaffGroup([piano_rh, piano_lh], symbol="brace")
    s.insert(0, sg)

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "score.musicxml")
    s.write("musicxml", fp=out_path)
    print(f"Score written to {out_path}")


if __name__ == "__main__":
    main()
