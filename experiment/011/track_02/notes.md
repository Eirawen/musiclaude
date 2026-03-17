# Track 02: The Crystal Throne -- Revision Notes

JRPG main menu theme for a Final Fantasy game starring Claude.

## Instrumentation
Flute, Horn in F, Harp, Violin I, Violin II, Viola, Violoncello

## Key plan
C minor -> Bb major (m.8) -> C minor -> Eb major (m.13) -> F minor (m.23) ->
Ab major (m.25) -> Db major (m.33) -> C minor (m.37) -> C major (m.45, Picardy)

## Profile feedback (iteration 0): 36/42 features at median
## After revision (iteration 1): 38/42 features at median

### Incorporated

1. **staccato_count** (was 0, target 9): Added staccato articulations to
   selected harp arpeggio notes -- alternating staccato creates a "chiming"
   quality that suits the crystal texture. Also added staccato at the climactic
   harp passage (m.33-34). This felt like a genuine improvement: the staccato
   adds sparkle without disrupting flow.

2. **rhythmic_variety** (was 6, target 7): Added dotted rhythms to the horn
   theme (m.9, m.13, m.17) and flute descants (m.7, m.13, m.25-27). Also
   added a couple of short-long patterns (0.75+0.25) for variety. These dotted
   figures give the horn melody more nobility -- a genuine improvement that
   makes the theme more memorable.

3. **modulation_count** (was 7, target 9): Added a Bb major tonicization
   (m.8), F minor tonicization (m.23), and Db major tonicization (m.33).
   The Bb and Db tonicizations were natural additions along the flat-key
   orbit the piece already inhabits. Still at 7 per the model -- the brief
   tonicizations may not register as full modulations to the detector.

4. **scale_consistency**: Added chromatic passing tones -- B natural in the
   horn (m.14, a chromatic approach to C), D natural in the horn (m.29,
   reaching up from Db), and F# in the flute (m.14, chromatic passing tone
   between F and Ab). These add color without disrupting tonal grounding.

### Rejected

1. **phrase_length_regularity** (0.737, target 1.05): The model wants more
   metrically regular phrases. But this is a main menu theme -- it should
   flow continuously, with long-breathed melodies and overlapping entries.
   Forcing rigid 4-bar cadential stops would kill the sense of grandeur and
   mystery. The phrases ARE 4 bars long; the model's phrase detector likely
   struggles with the sustained, overlapping texture. Musical coherence wins.

2. **groove_consistency** (0.816, target 0.827): Nearly at target. The
   variation between sections is intentional -- the prelude has flowing
   arpeggios, the hero's call has a lyrical melody, the journey has driving
   eighth notes. Homogenizing the rhythm would flatten the arc.

3. **Harp octave leaps** (44 leaps >octave): This is idiomatic harp writing.
   The crystal arpeggio texture requires sweeping across multiple octaves.
   Think Ravel's "Introduction and Allegro" or any Zelda/FF harp passage.
   Smoothing these would destroy the signature sound of the piece.

4. **Additional modulations beyond what was added**: The piece already moves
   through Cm, Bb, Eb, f, Ab, Db, Cm, and C major in 48 bars. Adding more
   key centers would make the harmony feel restless rather than majestic.
