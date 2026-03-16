# Feature Catalog

32 features extracted from MusicXML via music21. One row per score.

## Harmonic Features (`harmonic.py`)

| Feature | Type | Range | What it measures |
|---------|------|-------|-----------------|
| `chord_vocabulary_size` | int | 0-30+ | Number of unique chord types (commonName). Low = harmonically boring. |
| `pct_extended_chords` | float | 0-1 | Fraction of chords that are 7ths, 9ths, etc. or have 4+ pitches. |
| `harmonic_rhythm` | float | 0-∞ | Average quarter-note beats between chord changes. High = slow harmonic movement. |
| `cadence_count_authentic` | int | 0+ | V→I progressions. The "strongest" resolution. |
| `cadence_count_half` | int | 0+ | X→V progressions. Creates tension/expectation. |
| `cadence_count_deceptive` | int | 0+ | V→vi progressions. Surprise resolution. |
| `cadence_count_plagal` | int | 0+ | IV→I progressions. "Amen" cadence. |
| `key_stability` | float | 0-1 | Fraction of notes in the detected key's scale. Low = atonal or poorly established key. |
| `modulation_count` | int | 0+ | Key changes detected via windowed Krumhansl-Schmuckler analysis (4-measure windows). |

## Melodic Features (`melodic.py`)

| Feature | Type | Range | What it measures |
|---------|------|-------|-----------------|
| `avg_interval_size` | float | 0-24+ | Mean absolute melodic interval in semitones across all parts. |
| `pct_stepwise` | float | 0-1 | Fraction of intervals ≤ 2 semitones. High = smooth/singable. |
| `melodic_range` | int | 0-88 | Total semitone range (highest - lowest note in entire score). |
| `pct_rising` | float | 0-1 | Fraction of intervals going up. |
| `pct_falling` | float | 0-1 | Fraction of intervals going down. |
| `pct_static` | float | 0-1 | Fraction of unison intervals (0 semitones). |
| `rhythmic_variety` | int | 1+ | Number of unique duration values (quarterLength). Low = rhythmic monotony. |
| `repetition_density` | float | 0-1 | Fraction of measures that repeat earlier measures (same pitch sequence). |

## Structural Features (`structural.py`)

| Feature | Type | Range | What it measures |
|---------|------|-------|-----------------|
| `num_parts` | int | 1+ | Number of parts/instruments. |
| `total_duration_beats` | float | 0+ | Total score duration in quarter-note beats. |
| `dynamics_count` | int | 0+ | Number of dynamic markings (pp, p, mp, mf, f, ff, etc.). |
| `tempo_count` | int | 0+ | Number of MetronomeMark objects. |
| `time_sig_complexity` | float | 0/0.5/1 | 0=simple, 0.5=mixed, 1=compound meter. |
| `num_sections` | int | 0+ | RehearsalMark + RepeatBracket + RepeatMark count. |

## Orchestration Features (`orchestration.py`)

| Feature | Type | Range | What it measures |
|---------|------|-------|-----------------|
| `instrument_names` | str | — | Comma-separated instrument names (excluded from training). |
| `instrument_count` | int | 1+ | Number of distinct instruments. |
| `voice_crossing_count` | int | 0+ | Times a lower part's note is higher than the upper part at the same offset. |
| `avg_range_utilization` | float | 0-1+ | Average (actual range / comfortable instrument range) across parts. |
| `doubling_score` | float | 0-1 | Fraction of beats where 2+ parts share a pitch class. |

## Coherence Features (`coherence.py`) — LLM-targeted

| Feature | Type | Range | What it measures | LLM failure mode it catches |
|---------|------|-------|------------------|-----------------------------|
| `note_density` | float | 0+ | Notes per quarter-note beat. | Overstuffed or empty measures |
| `rest_ratio` | float | 0-1 | Fraction of total time occupied by rests. Normal: 5-25%. | LLMs forget rests (0% is a red flag) |
| `pitch_class_entropy` | float | 0-3.58 | Shannon entropy of pitch class distribution. | Stuck on few notes vs. atonal randomness |
| `interval_entropy` | float | 0-5+ | Shannon entropy of melodic interval distribution. | Repetitive intervals vs. scattered chaos |
| `melodic_autocorrelation` | float | -1 to 1 | Autocorrelation at 1-measure lag. High = structured motifs. | Random-walk melody (no phrase structure) |
| `phrase_length_regularity` | float | 0+ | Coefficient of variation of phrase lengths. Low = regular. | No detectable phrase boundaries |
| `strong_beat_consonance` | float | 0-1 | Fraction of strong beats with consonant intervals. | Accidental dissonance on downbeats |
| `rhythmic_independence` | float | 0-1 | How independently parts move rhythmically. | Parts in lockstep (bad orchestration) |
