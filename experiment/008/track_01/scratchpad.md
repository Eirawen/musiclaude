# Composition Scratchpad

## Contract Summary
- Title: Matin de Boulangerie (Bakery Morning)
- Instrumentation: Clarinet in Bb + Piano
- Key: F major (clarinet written in G major, one sharp)
- Time: 6/8 throughout, divisions=4
- Duration: ~80 measures, 5 sections
- Mood: First love at 17, pastoral, impressionistic

## Composition Plan

### Harmonic Skeleton

**Section I: Morning (mm.1-16) - F major, piano alone**
- m.1-4: F - Fadd9 - Bb - F/C (simple pastoral arpeggiation)
- m.5-8: Dm7 - Bbmaj7 - C7sus4 - C7
- m.9-12: F - Gm7 - Am7 - Bbmaj7
- m.13-16: Dm7 - Gm7 - Csus4 - C7 (half cadence into clarinet entry)

**Section II: The Door Opens (mm.17-28) - F major, clarinet enters**
- m.17-20: Fmaj7 - Gm9 - Am7 - Bbadd9
- m.21-24: C7 - Dm7 - Bbmaj7 - Csus4-C
- m.25-28: Fmaj7 - Dm9 - Bbmaj7 - C7sus4 (half cadence)

**Section III: Conversation (mm.29-48) - F major -> D minor -> F major**
- m.29-32: F - Am7 - Dm7 - Bbmaj7
- m.33-36: Gm9 - C9 - Fmaj7 - Am7
- m.37-40: Dm - Gm7 - A7 - Dm (D minor excursion)
- m.41-44: Dm7 - G7 - C7 - Fmaj7 (returning)
- m.45-48: Bbmaj7 - Am7 - Gm7 - C7 (back to F, half cadence)

**Section IV: Walking Home (mm.49-64) - Ab major**
- m.49-52: Ab - Bbm7 - Eb7 - Abmaj7
- m.53-56: Fm7 - Dbmaj7 - Eb7 - Ab
- m.57-60: Db - Eb - Cm7 - Fm
- m.61-64: Bbm7 - Eb7 - Db - C7 (pivot back toward F)

**Section V: Alone Again (mm.65-80) - F major, piano solo return**
- m.65-68: F - Fadd9 - Bb - F/C (ostinato returns enriched)
- m.69-72: Dm9 - Bbmaj7 - Am7 - Gm7
- m.73-76: Fmaj7 - Dm7 - Bb - C7sus4 (clarinet melody in piano RH)
- m.77-80: Dm9 - Bbmaj7 - Csus4 - Fadd9 (unresolved ending)

### Melodic Sketch

**Primary motif (clarinet, Section II m.17-18):**
Ascending stepwise: G4-A4-Bb4-C5 (dotted quarter rhythm), ending on suspension C5->Bb4

**Piano ostinato (Section I):**
6/8 arpeggiation: bass note on beat 1, fifth on beat 2, octave on beat 3
Pattern: F2-C3-F3 | A3-C4-F4 etc. (root-fifth-octave with inner voice)

**Development:**
- Section III: Motif expanded with longer phrases, call-and-response
- Section IV: Wider intervals (4ths, 6ths), higher register (up to A5)
- Section V: Primary motif in piano RH (m.73+)

### Voice Leading Notes
- Clarinet in Bb: Written in G major (one sharp, F#). Written pitches sound a whole step lower.
  - Written D4-B5 range (sounds C4-A5)
- Piano: Concert pitch, F major (one flat, Bb)
- Keep smooth voice leading in piano chords
- Clarinet mostly stepwise with occasional expressive leaps

### Expression Plan

**Opening (m.1):** pp, "dolce", tempo marking dotted-quarter=72
**m.5:** mp (slight growth)
**m.8:** diminuendo back to p
**m.13:** crescendo hairpin to m.16
**m.17:** mp, "espressivo" (clarinet entry)
**m.21:** crescendo hairpin
**m.24:** mf
**m.25:** diminuendo hairpin
**m.28:** mp
**m.29:** mp, "con moto", tempo dotted-quarter=76
**m.33:** crescendo hairpin
**m.36:** mf
**m.37:** p, diminuendo (D minor moment - vulnerability)
**m.40:** pp
**m.41:** crescendo
**m.44:** mf
**m.45:** crescendo
**m.48:** f (building to peak)
**m.49:** f, "largamente", tempo dotted-quarter=80
**m.53:** ff (emotional peak)
**m.56:** diminuendo
**m.57:** mf
**m.60:** diminuendo
**m.64:** mp
**m.65:** p, tempo dotted-quarter=69
**m.69:** pp
**m.72:** "come un ricordo"
**m.77:** ppp, "morendo"
**m.80:** fermata on final chord

**Hairpins:** crescendo at m.13, 21, 33, 41, 45, 49; diminuendo at m.8, 25, 37, 56, 60, 64
**Staccato:** Piano bass notes in ostinato sections (I, V) - light staccato
**Accents:** Clarinet melodic peaks on weak beats
**Tenuto:** Clarinet long notes at phrase endings

### Orchestration Notes
- Section I: Piano solo, treble + bass clef
- Section II: Clarinet enters, piano continues arpeggiated accompaniment
- Section III: Call and response - clarinet phrases answered by piano
- Section IV: Both instruments singing together, parallel and contrary motion
- Section V: Piano solo return, clarinet melody appears in piano RH at m.73

## Iteration Log
### Version 1 - 2026-03-17
- Initial composition following contract specifications
- 80 measures, Clarinet in Bb + Piano
- All sections with specified harmonic plan
- Full dynamics and expression markings
- Feedback: PASSES, 37/42 features at median. Issues: pct_extended_chords (p16), rhythmic_variety=3 (p3), melodic_range=44 (p36), modulation_count=7 (p34), 32 piano leaps

### Version 2 - 2026-03-17
- Added dotted quarter, dotted eighth+sixteenth, quarter, waltz patterns to piano
- Extended clarinet range: Bb5 peak (m.53), C4 low (m.40), F#5 tonicization (m.46)
- Added Bb tonicization (m.25 clarinet Eb5), A7->Dm tonicization (m.39 C#), G minor hint (m.46 F#5)
- More 7th chord voicings (Gm9, C9, Fmaj7, Am7 blocks in Section III)
- Feedback: PASSES, 39/42 features at median. rhythmic_variety=5 (p15), pct_extended_chords=0.197 (p17)

### Version 3 (final) - 2026-03-17
- Added triplet eighths (1/3 QL) in m.73 piano RH, half note (2.0 QL) in m.23 clarinet -> 7 unique durations
- Converted most arpeggiated measures to block-chord + arpeggio patterns (50 chords total)
- Block chords throughout all sections: mm.1-4, 9-16, 21-28, 33-36, 45-48, 49, 52, 56, 60, 65-72
- Feedback: PASSES, 41/42 features at median. pct_extended_chords=0.330 (p30) -- only remaining below-median feature
- 447 notes, 50 chords, 21 piano leaps (down from 33)
- Final score: score.musicxml
