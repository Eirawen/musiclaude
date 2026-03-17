# Track 02 -- "The Bottle Gambit" (Cello + Piano)

**Vibe:** A chess game between old friends in a park. The stakes are a bottle of wine.
**Instrumentation:** Cello + Piano, 3/4 time
**Key areas:** D minor -> F major -> D minor -> D major

## Profile Feedback (v3) -- Decisions

### Incorporated

1. **melodic_range** (3rd -> ~10th percentile): Expanded the cello range from A2-G4 to C2-Bb4 by using the open C string in the reflection section (m.19) and the dolce response (m.43), and pushing to Bb4 in the midgame climax (m.27). Also pushed the piano right hand up to C5 in the midgame. Went from 31 to 36 semitones. Still below target of 48, but accepted -- see rejection notes below.

2. **rhythmic_variety** (7th -> above median): Added dotted quarter-eighth patterns, sixteenth-note neighbor tones (m.14 G#3-A3 turn, m.22 C#4-D4 ornament), dotted-eighth-sixteenth figures (m.12, m.34), and varied phrase entry points. The original was too square.

3. **rest_ratio** (22nd -> 41st percentile): Added rests at phrase endings throughout -- m.12, m.18, m.20, m.28, m.29, m.32, m.40, m.42, m.44, m.46, m.48, m.52. Phrases now breathe. The chess metaphor benefits from silences -- the pause before a move.

4. **pitch_class_entropy** (19th -> 32nd percentile): Added chromatic passing tones: G#3 neighbor tone (m.14), Eb4 Neapolitan color (m.24), F#3 secondary dominant hint (m.30), Eb3 passing tone (m.31, m.50), G#3 chromatic neighbor (m.51). Piano adds dim7 passing chords (m.19, m.31), Neapolitan Eb chord (m.24), augmented chord (m.34), French augmented 6th (m.36), Neapolitan Db in F major (m.38), and secondary dominants (m.26 V/Gm, m.35 V/Dm, m.43 E7).

5. **chord_vocabulary_size** (39th -> above median): Added diminished 7th, augmented triad, Neapolitan, French augmented 6th, and multiple secondary dominants. These serve the narrative -- chromatic tension in the midgame, exotic color in the gambit.

6. **modulation_count** (23rd -> 35th percentile): Added secondary dominant tonicizations (V/Gm in m.26, V/Dm in m.35, E7/Am in m.43) on top of the three main key areas. The brief tonicizations feel like tactical feints in the chess game.

7. **Voice leading** (piano bass leaps): Smoothed the piano bass line to move more stepwise, especially in the waltz accompaniment sections. Added passing tones in the bass (m.4, m.8).

### Rejected

1. **melodic_range target of 48 semitones**: The PDMX median of 48 semitones (4 octaves) reflects a dataset that includes orchestral and multi-instrument pieces. For a cello-piano duo, 36 semitones (3 octaves, C2 to C5) is a natural range. Pushing further would require either unidiomatic cello writing above the fingerboard or a piano part that abandons its accompaniment role to play extreme registers. The piece's intimacy depends on both instruments staying in their conversational range.

2. **phrase_length_regularity** (27th percentile, target 1.05): The model wants more regular phrase lengths. I kept the slight irregularity -- the chess game metaphor calls for phrases that feel like moves of varying deliberation. Some moves are quick (short phrases in the staccato exchange, mm.29-32), some are long considerations (the cantabile build, mm.33-36). Imposing strict 4-bar regularity would make it feel like a student exercise.

3. **groove_consistency** (28th percentile, target 0.827): The model wants consistent rhythmic patterns within sections. I intentionally vary rhythms within sections to reflect the shifting energy of the game. The midgame section mixes staccato exchanges with legato lines because the chess game itself alternates between quick tactical moves and deep strategic thought.

4. **scale_consistency** (already at 78th percentile, above target): The first pass flagged this at 88th percentile saying I was "too diatonic." The revision brought it to 78th by adding chromatic chords. This is fine -- I don't want to add chromaticism beyond what serves the music.
