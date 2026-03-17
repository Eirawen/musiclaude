# Scratchpad: Matin de Boulangerie — Track 02

## Harmonic Skeleton

### Section I: Morning (mm. 1-16), F major, dotted-quarter=72
- Ostinato pattern: Piano LH arpeggiation F-C-F (root-5th-octave) in 6/8
- Piano RH: gentle inner voice movement over ostinato
- Chords: F → Fsus4→F → Bb/F → F → Dm7 → Gm7 → C7sus4 → C7
- Repeat with variation: Fadd9 → Bb → Am7 → Dm → Gm9 → C7 → F
- pp → mp arc over 16 bars
- Marking: "dolce" at m.1

### Section II: The Door Opens (mm. 17-28), F major
- Clarinet enters mp espressivo
- Primary motif: C5-D5-E5-F5-G5(held, suspension) — ascending stepwise, "first glance"
- Piano shifts to add9 and sus4 chords: Fadd9, Csus4→C, Bbadd9, Gm9
- Second phrase: motif varied, ending on A5 (reaching higher)
- Piano: Dm9 → G9 → Csus4 → C → Am7 → Dm7 → Bbmaj7 → C7

### Section III: Conversation (mm. 29-48), dotted-quarter=76, "con moto"
- Call and response: clarinet phrases answered by piano RH
- Longer phrases, braver intervals (4ths, 6ths)
- m.37-40: D minor excursion (Dm → Gm → A7 → Dm → Bb → C7 → F)
- Dynamics: mp → mf with diminuendo into D minor moment
- Chords: F → Gm7 → Am7 → Bbmaj7 → C9 → Dm7 → Em7b5 → A7
  Then: Dm → Gm7 → C7 → Fmaj7 → Bb → Bdim → C7sus4 → C7

### Section IV: Walking Home (mm. 49-64), dotted-quarter=80, "largamente"
- Modulate to Ab major at m.49
- Emotional peak: parallel and contrary motion
- Wide intervals, higher register for clarinet (up to A5)
- mf → f with rich hairpins
- Chords: Ab → Bbm7 → Eb7 → Abmaj7 → Db → Dbm → Ab/Eb → Eb7
  Then: Fm7 → Bbm9 → Eb9 → Ab → Db → Eb7sus4 → Eb7 → Ab
- Transition back: Ab → C7 → F (m.63-64)

### Section V: Alone Again (mm. 65-80), dotted-quarter=69, rit. final bars
- Piano solo returns with enriched ostinato
- Added 7ths, chromatic touches: Fmaj7, Dm9, Gm11, C13
- m.72: Clarinet's primary motif (from Section II) appears in piano RH
- "come un ricordo" marking
- pp, morendo
- Final chord: Fadd9, unresolved, pp

## Voice Leading Plan
- Piano LH: steady 6/8 arpeggiation providing harmonic foundation
- Piano RH: chordal support, inner voice movement, takes over melody in Section V
- Clarinet: lyrical melody floating above piano, mostly stepwise with expressive leaps
- At emotional peak (Section IV): both instruments in wider intervals, fuller texture

## Primary Motif (Clarinet, Concert Pitch)
C5 - D5 - E5 - F5 - G5(held)
Written for Bb Clarinet: D5 - E5 - F#5 - G5 - A5

## Transposition Note
Clarinet in Bb: written pitch is M2 higher than concert pitch.
MusicXML: <transpose><diatonic>-1</diatonic><chromatic>-2</chromatic></transpose>
This means the MusicXML contains the WRITTEN pitch (transposed up M2 from concert).

## Duration Math (divisions=4)
- 6/8 time: one measure = 6 eighth notes = 12 duration units
- Eighth note = 2 units
- Quarter note = 4 units
- Dotted quarter = 6 units
- Half note (dotted) = 12 units (full measure)
- Sixteenth note = 1 unit
- Dotted eighth = 3 units

## Iteration Log

### Iteration 1 (Initial)
- 650 notes, 80 measures, 2 parts
- 38/42 features at or above high-rated median
- Issues: pct_extended_chords=0.021 (need 0.58), rhythmic_variety=3 (need 7), hairpin_count=2 (need 10)

### Iteration 2
- Rewrote to use 4-note chords extensively, added 16th/dotted-8th rhythms, added 16 hairpins
- 39/42 features at or above high-rated median
- pct_extended_chords=0.452, rhythmic_variety=6, hairpin_count=16
- Remaining: pct_extended_chords still below target, rhythmic_variety needs +1, groove_consistency=0.810

### Iteration 3 (Final)
- Added triplet figures for rhythmic_variety=7, more 4-note chords, repeated primary motif in clarinet (mm. 29, 33, 41) for melodic_autocorrelation
- 40/42 features at or above high-rated median
- pct_extended_chords=0.485, melodic_autocorrelation=0.422 (was 0.166), groove_consistency=0.806
- Remaining below target: pct_extended_chords (0.485 vs 0.58), groove_consistency (0.806 vs 0.827) — marginal gaps
