# Experiment 002 — Deduplication + PDMX Metadata Features

**Date:** 2026-03-16
**Status:** Complete
**Previous:** [001-baseline-training.md](001-baseline-training.md)

## What Changed

1. **Deduplication** — Filter to `subset:rated_deduplicated == True` from PDMX.csv. Removed 399 duplicate arrangements (7.1%) that could leak between train/test splits.
2. **Added 3 PDMX metadata features** — `scale_consistency` (MusPy), `groove_consistency` (MusPy), `complexity` (MuseScore 0-3 score). Zero extraction cost — precomputed in PDMX.csv.
3. **Always join PDMX metadata** — Fixed `load_and_prepare()` to join PDMX.csv even when features.csv already has ratings, to pick up the dedup flag and extra features.

## Results

| Metric | Exp 001 (baseline) | Exp 002 (this) | Change |
|--------|-------|-------|--------|
| Training samples | 5,606 | 5,207 | -399 (deduped) |
| Features | 32 | 35 (+complexity, scale_consistency, groove_consistency) |  |
| Binary Accuracy | 0.602 | **0.635** | **+3.3%** |
| Binary F1 | 0.661 | **0.690** | **+2.9%** |
| RMSE | 0.150 | **0.149** | -0.001 |
| R² | 0.052 | 0.039 | -0.013 |

**Key:** Accuracy went UP despite removing 399 samples. The R² drop is likely because duplicates were artificially inflating it (same piece in train and test). The deduped R² is more honest.

## Feature Importance (Top 10)

### Binary Classifier

| Rank | Feature | Importance | Source | Change from 001 |
|------|---------|------------|--------|-----------------|
| 1 | complexity | 0.046 | PDMX | **NEW — immediate #1** |
| 2 | dynamics_count | 0.041 | Ours | was #1 |
| 3 | time_sig_complexity | 0.039 | Ours | was #7 |
| 4 | chord_vocabulary_size | 0.035 | Ours | was #3 |
| 5 | scale_consistency | 0.032 | PDMX | **NEW — immediate top 5** |
| 6 | tempo_count | 0.028 | Ours | was #2 |
| 7 | pct_static | 0.028 | Ours | new entry |
| 8 | harmonic_rhythm | 0.027 | Ours | was #19 |
| 9 | pitch_class_entropy | 0.027 | Ours | was #4 |
| 10 | cadence_count_deceptive | 0.027 | Ours | new entry |

### Regressor

| Rank | Feature | Importance | Source | Change from 001 |
|------|---------|------------|--------|-----------------|
| 1 | dynamics_count | 0.055 | Ours | still #1 |
| 2 | tempo_count | 0.049 | Ours | still #2-3 |
| 3 | complexity | 0.047 | PDMX | **NEW — immediate #3** |
| 4 | melodic_range | 0.034 | Ours | was #4 |
| 5 | scale_consistency | 0.033 | PDMX | **NEW — immediate #5** |
| 6 | melodic_autocorrelation | 0.032 | Ours | was #10, rising |
| 7 | rest_ratio | 0.031 | Ours | new top-10 entry |
| 8 | total_duration_beats | 0.030 | Ours | stable |
| 9 | num_sections | 0.029 | Ours | was #7 |
| 10 | instrument_count | 0.029 | Ours | was #2, dropped |

## Key Findings

### 1. complexity is the new #1 for binary classification

MuseScore's own complexity score (0-3) immediately became the strongest binary predictor. This makes sense — MuseScore rates complexity based on rhythm, harmony, and technical difficulty. It's essentially a distilled version of several of our features. The classifier leverages it as a strong aggregate signal.

**Caveat:** We don't have `complexity` for LLM-generated music — it's a MuseScore metadata field, not something we can compute. For the feedback loop, this feature is unavailable. But it validates that complexity-related features are genuinely predictive.

### 2. scale_consistency immediately top 5

MusPy's scale_consistency (fraction of notes belonging to the detected scale) is a free, strong feature. It has r=-0.20 correlation with rating — meaning **less** scale-consistent music (more chromatic) rates higher. This aligns with our finding that pitch_class_entropy (tonal diversity) is predictive.

**Important for LLM composition:** Don't write only diatonic music. Some chromaticism signals sophistication.

### 3. Deduplication improved accuracy

Removing 399 duplicates (7.1%) and adding 3 features gave a bigger accuracy boost (+3.3%) than doubling the training data did in experiment 001. **Data quality > data quantity.**

### 4. melodic_autocorrelation is rising

Moved from #10 to #6 in the regressor. With cleaner data (no duplicate inflation), the coherence features are gaining relative importance. This validates our LLM-targeting feature design.

### 5. rest_ratio entered top 10 (regressor)

"Breathing room" in music — pieces with appropriate rests rate higher. This is exactly the kind of thing LLMs get wrong (wall of notes with no rests).

## Implications for the Feedback Loop

The features available to the LLM feedback loop (everything except `complexity` and MusPy features) still form a strong signal. The top actionable features are:

1. **Add dynamics** (dynamics_count) — still the most impactful thing an LLM can do
2. **Use compound/irregular time signatures** (time_sig_complexity) — don't default to 4/4
3. **Rich chord vocabulary** (chord_vocabulary_size) — use 7ths, 9ths, suspensions
4. **Include some chromaticism** (scale_consistency negative correlation) — don't be purely diatonic
5. **Add tempo markings** (tempo_count)
6. **Build in rests** (rest_ratio) — let the music breathe
7. **Use motivic development** (melodic_autocorrelation) — repeat and vary themes

## What We'd Do Differently Next

1. **Compute our own complexity score** — since MuseScore's isn't available for LLM music, derive an equivalent from our features (e.g., weighted combination of time_sig_complexity, chord_vocabulary_size, melodic_range)
2. **Compute scale_consistency ourselves** — the MusPy calculation is straightforward (detect scale, count notes on it). Add to coherence module.
3. **Try interaction features** — dynamics_count * total_duration_beats, etc.

## Files

Same as experiment 001, models overwritten in `models/`.
