# Track 03: Matin de Boulangerie

Clarinet in Bb and Piano, 6/8 time, F major.
Vibe: First love at 17, summer in a French village, working at a bakery.

## Structure
- A (mm. 1-8): Morning -- core motif F-G-A over Fmaj7/Dm7/BbMaj7/C7 arpeggios
- A' (mm. 9-16): Flourishing -- motif ornamented with turns, chromatic C# and F#
- B (mm. 17-24): The Bakery -- staccato, playful, C major tonicization, dim7 chord
- A'' (mm. 25-32): Sunset Walk -- motif in chalumeau register, rich 7ths, wide range
- Coda (mm. 33-36): Lingering -- motif fragments fading to pp

## Revision 1 Changes (addressing profile feedback)

Initial score: 28/41 features at or above high-rated median.
Revised score: 33/42 features at or above high-rated median.

### What changed

1. **Chromaticism** (scale_consistency 0.985 -> 0.938, target ~0.914): Added Eb, Ab, C#, F#, G# as passing tones and chromatic neighbors in the clarinet; chromatic bass walks (G-Ab-Bb, D-C#-C, F-Eb-Bb) in piano left hand; diminished 7th chord (D-F-Ab-B) and D7 (with F#) in the B section.

2. **Motivic development** (melodic_autocorrelation improved, no longer flagged): Established a clear 3-note motif (F-G-A, rising seconds) in m.1 and repeated it in every section -- transposed to C-D-E (m.5), G-A-B (B section), returned in low register F4-G4-A4 (A'' section), and as a final whisper in the Coda.

3. **Range utilization** (avg_range_utilization 0.207 -> 0.247): Extended clarinet down to F4 (chalumeau register) in A'' and Coda; piano bass down to F1/G1/A1; piano treble up to D6.

4. **Rhythmic variety** (4 -> 6 duration types): Added dotted eighths (0.75 QL), sixteenths (0.25 QL), and dotted quarters (1.5 QL) alongside the existing eighths (0.5) and quarters (1.0). Also 2.0 QL for fermata notes.

5. **Rest ratio** (0.040 -> improved, no longer flagged): Added breathing rests after phrases in clarinet (every 2-4 bars), half-measure rests at section endings (m.8, 12, 16, 24, 28, 32), rests in piano B-section patterns.

6. **Pitch class entropy** (2.85 -> improved, no longer flagged): More chromatic pitch classes (C#, Eb, F#, G#, Ab) distributed throughout all sections.

7. **Extended chords** (pct_extended_chords 0.431 -> 0.401, still below target): Replaced most piano triads with 7th chords (Fmaj7, Dm7, Am7, BbMaj7, C7, C9), though the staccato B-section chords keep some shorter voicings.

### Remaining gaps after revision
- groove_consistency slightly worse (the varied rhythms in clarinet hurt intra-section consistency)
- avg_range_utilization still below target (0.247 vs 0.328)
- hairpin_count = 0 (crescendo/diminuendo spanners present but not detected as hairpins by the extractor)
- phrase_length_regularity flagged (phrasing is intentionally varied between sections)
