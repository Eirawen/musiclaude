# Validator Checks

All checks run via `validate_score()`. Errors block the pipeline. Warnings are surfaced as critiques.

## Errors (score is INVALID)

| Check | Condition | Message |
|-------|-----------|---------|
| Has parts | `len(score.parts) == 0` | "Score has no parts/instruments." |
| Has notes | No Note or Chord objects found | "Score contains no notes or chords." |
| Valid time signatures | Numerator or denominator ≤ 0 | "Invalid time signature: {ratio}" |

## Warnings (score is valid but flagged)

| Check | Condition | Message |
|-------|-----------|---------|
| Few notes | < 4 notes/chords total | "Score has very few notes. May be incomplete." |
| No time signature | No TimeSignature objects | "No explicit time signature found." |
| Unusual time signature | Numerator > 24 | "Unusual time signature: {ratio}" |
| Measure overflow | Measure duration > time signature duration | "Part X measure Y: duration exceeds time signature." |
| No key signature | No KeySignature objects | "No key signature found." |
| Note below range | Note pitch < instrument.lowestNote | "Note X in Part Y is below instrument range." |
| Note above range | Note pitch > instrument.highestNote | "Note X in Part Y is above instrument range." |
| Parallel fifths | > 3 consecutive perfect 5ths between top 2 parts | "Found N instances of parallel fifths." |
| Parallel octaves | > 3 consecutive unisons/octaves between top 2 parts | "Found N instances of parallel octaves." |
| Large leaps | > 5 leaps larger than an octave in a single part | "Part X has N leaps larger than an octave." |

## Not Yet Implemented (potential additions)

- Unresolved suspensions (4-3, 7-6 that never resolve)
- Doubled leading tone in chords
- Direct/hidden fifths and octaves
- Spacing violations between voices (> octave between adjacent upper voices)
- Cross-relation between parts (chromatic contradiction)
