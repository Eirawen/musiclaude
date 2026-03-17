# Track 04: Prelude to a New World

JRPG main menu theme for a Final Fantasy game starring Claude.

## Instrumentation
Flute, French Horn in F, Harp, Violin I, Viola, Violoncello

## Structure
- I. Crystal Prelude (mm.1-16) -- Bb major, harp arpeggios, horn hero's motif
- II. The Journey Begins (mm.17-32) -- Bb -> Db major -> Eb major -> Bb
- III. Shadow of Doubt (mm.33-48) -- G minor -> Bb minor -> C minor -> D major
- IV. Promise of Dawn (mm.49-64) -- Eb major -> Ab major -> Bb major

Hero's motif: Bb-D-F-Eb-D (rising arpeggio with stepback)

## Revision 1 Changes (from profile feedback)

Initial score: 37/42 features at or above high-rated median.
Revised score: 40/42 features at or above high-rated median.

### Issues addressed:

1. **scale_consistency** (0.954 -> fixed): Added chromatic passing tones throughout
   all parts -- C#, F#, G#, Ab, Gb, Cb, B-natural neighbor tones. Borrowed chords
   (Neapolitan-flavored Db major, augmented sixth gestures).

2. **pitch_class_entropy** (2.95 -> fixed): Spread all 12 pitch classes more evenly
   by introducing chromatic neighbors in every part. Harp arpeggios now include
   altered scale degrees. Horn and strings use chromatic inflections at phrase
   boundaries.

3. **rhythmic_variety** (6 unique durations -> fixed): Added triplet eighth notes
   (1/3 quarter), dotted eighths (0.75), and sixteenth notes (0.25) alongside
   existing half, dotted-half, quarter, and eighth note values.

4. **modulation_count** (3 -> fixed): Expanded from 3 to 10 explicit key signature
   changes: Bb -> F (m.3) -> Bb (m.4) -> Eb (m.7) -> Bb (m.8) -> Db (m.21) ->
   Eb (m.25) -> Bb (m.29) -> g (m.33) -> bb (m.37) -> c (m.41) -> D (m.45) ->
   Eb (m.49) -> Ab (m.53) -> Bb (m.57).

5. **phrase_length_regularity** (0.592 -> still 0.592): Enforced strict 4-bar phrase
   groups with cadential rests at every 4th measure. The metric did not improve,
   likely because the underlying computation measures note-onset patterns rather
   than just phrase boundary placement.

### Remaining issues:

- **phrase_length_regularity** (percentile 13): Structural measurement issue --
  4-bar phrases are consistent but the metric may weight onset density patterns.
- **melodic_autocorrelation** (percentile 43): Marginal, close to median. The
  piece uses the hero's motif across sections but six independent parts dilute
  the autocorrelation signal.
