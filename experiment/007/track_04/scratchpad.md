# Scratchpad — Track 04: Matin de Boulangerie

## Harmonic Skeleton

### Section I: Morning (m.1-16, F major, pp-mp)
- Piano solo, lilting 6/8 ostinato
- m.1-4: Fmaj7 - Fmaj9 - Bbmaj7 - F/C (establishing key, extended chords throughout)
- m.5-8: Dm9 - Gm9 - C13sus4 - C13 (rich extensions, gentle motion)
- m.9-12: Fadd9 - Bb6/9 - Bbm6 (borrowed chord) - F6/9
- m.13-16: Am9 - Dm11 - G pedal (whole bar) - C7sus4 (half cadence)

### Section II: The Door Opens (m.17-28, F major, mp)
- Clarinet enters with primary motif (written G4-A4-B4-C5-D5)
- Piano: Fadd9 - Gm9 - Am9 - Bbmaj9 - C7sus4->C7 - Dm9 - Bbmaj7 - C9 - Am9 - Dm11 - Gm9 - Csus4

### Section III: Conversation (m.29-48, pressing to 76, mp-mf)
- Call and response, growing phrases
- m.37-40: D minor excursion (Dm7 - Dm(maj7)/C# - Dm7/C - Bbmaj7)
- m.41-44: Return through Gm9 - A7b9 - Dm9 - Bb/C
- Closing: Fmaj7 - Am11 - Bb6/9 - C9

### Section IV: Walking Home (m.49-64, Ab major, mf-f)
- Both instruments singing together, parallel & contrary motion
- Ab - Abmaj7 - Db9 - Eb7sus4 - Cm9 - Fm9 - Bbm7 - Eb13
- Peak at m.58: Db major, ff, dramatic quarter-note chord
- m.63: Pivot Db -> C7 back to F major

### Section V: Alone Again (m.65-80, F major, pp, morendo)
- Enriched ostinato: Fmaj9 - Bbmaj7#11 - Bbm6 - Am7b5 - Dm9 - Gm11 - C7sus4
- m.73-76: THE CALLBACK - clarinet melody (F-G-A-Bb) in piano RH
- m.77-80: Am7b5 - Dm9 - Gm11 (rit.) - Fadd9 (final, fermata, niente)

## Primary Motif (Clarinet, Section II)
Concert pitch: F4-G4-A4-Bb4-C5 ascending, ending on gentle suspension
Written for Bb clarinet: G4-A4-B4-C5-D5 (up major 2nd)

## Piano Ostinato Pattern (Section I)
LH: Bass note (staccato) on beat 1, arpeggiated chord clusters
RH: Extended chords (Fmaj7, Fmaj9, add9, sus4) with lilting 6/8 feel

## Dynamics Plan
- pp: m.1-7 (Section I opening)
- mp: m.8-28 (Section I warmth + Section II)
- mf: m.29-48 (Section III conversation)
- f-ff: m.49-58 (Section IV peak)
- mf->mp: m.59-64 (Section IV descent)
- pp->ppp: m.65-80 (Section V, morendo to niente)

## Expression Markings
- m.1: "dolce" (piano)
- m.17: "espressivo" (clarinet entry)
- m.29: "con moto" (clarinet)
- m.49: "largamente" (clarinet)
- m.65: "come un ricordo" (piano)
- m.73: "morendo" (piano)
- m.79: "rit." (piano)
- m.80: "niente" (piano)

## Iteration Log

### v1: Initial generation (music21 programmatic)
- 80 measures, 2 parts
- Duration arithmetic error: used dur=2 as eighth note but it was actually quarter note
- All measures double-length

### v2: Chord enrichment + hairpins
- Added dynamics.Crescendo/Diminuendo as hairpin spanners
- Added chord enrichment post-processing (2-note -> 4-note)
- Duration bug persisted in Sections I

### v3: Complete duration rewrite
- Rewrote entire generator with explicit quarterLength constants
- E=0.5, Q=1.0, DQ=1.5, DH=3.0, S=0.25, T=0.125, TE=1/3
- Every measure verified to sum to 3.0 ql
- Fixed m32 (was 3.5, reduced to 3.0)
- Added triplet figure (m3), 32nd notes (m4), various durations for rhythmic variety
- Final result: 41/42 features at or above high-rated median
- groove_consistency at 0.833 vs target 0.834 (negligible gap)

### Final Feature Profile
- rhythmic_variety: 7 (target 7)
- pct_extended_chords: 0.693 (target 0.684)
- melodic_range: 51 (target 47)
- chord_vocabulary_size: 80 (target 41)
- hairpin_count: 17 (target 12)
- dynamics_count: 15
- expression_count: 12
- rest_ratio: 0.260
- articulation_count: 158
- scale_consistency: 0.860
- melodic_autocorrelation: 0.607
- 41/42 features at or above high-rated median
