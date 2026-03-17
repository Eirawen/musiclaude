# Track 03: JRPG Main Menu Theme ("Claude's Overture")

## Concept
A Final Fantasy-style main menu theme for a game starring Claude. Scored for
flute, oboe, French horn, harp, piano, and string quartet (Vln I, Vln II, Vla, Vc).

Key: C minor -> Eb major -> C minor -> C major (Picardy ending)
Tempo: Andante con moto (76 BPM)
Structure: Intro (mm. 1-4) | A (5-12) | B (13-20) | A' (21-28) | Coda (29-34)

The melody ("the question motif": C5-D5-Eb5-D5) appears in the flute,
representing a sense of noble searching. The horn carries a heroic counter-theme
in Eb major. Harp arpeggios provide crystalline menu atmosphere. The Picardy
third ending (C major) provides warmth and resolution.

## Revision Summary

Initial score: 31/42 features at or above high-rated median.
Revised score: 39/42 features at or above high-rated median.

### Changes Made (addressing profile feedback)

1. **scale_consistency** (0.961 -> improved): Added chromatic passing tones
   throughout -- F#4, C#5, Db, A-natural, E-natural in minor context. Added
   F#dim7, Neapolitan Db, augmented, and Gb chords to harp and piano.

2. **chord_vocabulary_size** (38 -> improved): Introduced Cm7, AbM7, Fm9,
   Gsus4, F#dim7, Bbsus4, D major, Ab augmented, Gb major, G7(b9), Db major
   (Neapolitan), C7, and Ab add9 chords across piano and harp parts.

3. **melodic_autocorrelation** (0.343 -> 0.413): Flute A' section now repeats
   the exact opening motif (C5-D5-Eb5-D5) from section A, then diverges.

4. **pitch_class_entropy** (2.95 -> improved): All 12 pitch classes now appear
   through chromatic additions (F#, C#, Db, A-natural, E-natural, Gb).

5. **rhythmic_variety** (6 -> 9 types): Added triplet eighths (1/3),
   dotted-eighth+sixteenth (0.75+0.25), and 2.5 duration values.

6. **melodic_range** (46 -> 48 semitones): Extended flute to C6 (MIDI 84)
   in the A' climax and cello to C2 (MIDI 36).

7. **expression_count** (2 -> 6): Added TextExpressions (espressivo, cantabile,
   con brio, maestoso) plus fermatas, trills on sustained notes.

8. **articulation_count** (7 -> 25+): Added tenuto on long notes, staccato on
   short detached notes, accents at climactic points across all string parts.

9. **Structural fixes**: Added explicit time signature (4/4) and key signature
   (3 flats) to every part's first measure.

### Accepted Gaps

- **modulation_count** (2 vs target 10): The Krumhansl key-finding algorithm
  analyzes all 9 parts together in 4-bar windows. With the full ensemble playing
  in C minor / Eb major, individual chromatic chords don't shift the detected key
  of the window. Achieving 10 modulations would require wholesale key changes that
  would undermine the cohesive menu-theme character.

- **phrase_length_regularity** (0.877 vs 0.992): Very close. The slight gap comes
  from intentional phrase length variety for musical naturalness.

- **melodic_autocorrelation** (0.413 vs 0.417): Only 0.004 below target --
  effectively at the boundary.
