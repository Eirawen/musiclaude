# Track 04: "En Passant" -- Cello & Piano

## Concept
A chess game between old friends in a park. The stakes: a bottle of wine.
3/4 time, D minor, 48 measures. Four sections: Opening, Middlegame, Endgame, Stalemate/Wine.

## Revision Summary (1 round)

### Feedback from initial version
The quality profile flagged 8 features below high-rated median (34/42 passing):
1. melodic_range = 29 (target 48)
2. melodic_autocorrelation = 0.244 (target 0.417)
3. avg_range_utilization = 0.253 (target 0.328)
4. groove_consistency = 0.794 (target 0.839)
5. modulation_count = 5 (target 10)
6. rhythmic_variety = 6 (target 7)
7. chord_vocabulary_size = 41 (target 49)
8. rest_ratio = 0.125 (target 0.145)

### Changes made
- **Melodic range**: Extended cello down to C2 (mm.5-7, 25-27) and up to E5 (mm.21-22). Added Bb0 in piano bass (m.27) and C5 in treble (m.45). Range: 29 -> 40 semitones.
- **Melodic autocorrelation**: Made the D-F-A motif recur explicitly in every section -- mm.1, 5, 9, 16, 29, 31, 37, 41, 43, 47. Used triplet rhythm for motif restatements. Autocorrelation: 0.244 -> 0.534 (exceeds target).
- **Rhythmic variety**: Added eighth-note triplets (T = 1/3 quarter) for motif restatements. Variety: 6 -> 7 (meets target).
- **Chord vocabulary**: Added Bdim, Edim, C#dim, F#dim, Bb+, Fsus2, Bbsus4, Dsus2, Asus4, A9 chord types. Vocabulary: 41 -> 46.
- **Rest ratio**: Replaced many held notes with rest + shorter note patterns across both parts. Ratio: 0.125 -> 0.231 (exceeds target).
- **Tonicizations**: Added key signature changes for brief tonicizations of Dm, C, Eb, Gm, Cm, A within sections.

### Results after revision
- 37/42 features at or above high-rated median (was 34/42)
- Composition passes quality threshold
- Remaining gaps: avg_range_utilization (0.218), melodic_range (40), groove_consistency (0.794), modulation_count (5), chord_vocabulary (46)
