# Experiment 001 — Baseline Training on PDMX

**Date:** 2026-03-16
**Status:** Complete

## Setup

| Parameter | Value |
|-----------|-------|
| Dataset | PDMX (Zenodo 2024) |
| Total files extracted | 25,561 (5,617 rated + 19,998 unrated sample) |
| Training samples (rated, n_ratings >= 10) | 5,606 |
| Features | 32 numeric (harmonic, melodic, structural, orchestration, coherence) |
| Binary threshold | 4.76 (median of filtered subset) |
| Class balance | 49.2% below / 50.8% above threshold |
| XGBoost hyperparameters | 200 estimators, max_depth=6, lr=0.1, subsample=0.8, colsample_bytree=0.8 |
| Isolation Forest | 200 estimators, contamination=0.1, robust scaling |
| Test split | 20%, stratified (binary), random_state=42 |
| Hardware | RTX 4080 Laptop (CUDA), 20-core CPU |
| Extraction time | ~several hours, 16 workers, checkpointed every 500 files |

## Results

### Binary Classifier (good vs not good)

| Metric | Value |
|--------|-------|
| Accuracy | 0.602 |
| F1 (good class) | 0.661 |
| Precision (good) | 0.63 |
| Recall (good) | 0.69 |

### Regressor (continuous rating)

| Metric | Value |
|--------|-------|
| RMSE | 0.150 |
| R² | 0.052 |

### Distribution Scorer

| Metric | Value |
|--------|-------|
| Training samples | 25,561 |
| Features | 32 |
| Contamination | 10% |

## Statistical Significance

| Test | Result |
|------|--------|
| Binomial test (accuracy vs 50% baseline) | z = 5.03, p = 2.79e-07 |
| Permutation test (R² vs random features) | 0/10,000 random trials exceed R² = 0.052 |
| Cohen's h (effect size) | 0.205 (small, at boundary of small/negligible) |

**Verdict:** Real signal, not noise. Statistically significant at p < 0.0001. Effect size is small but expected given the compressed rating range (std = 0.171, useful range ~0.5 points).

## Feature Importance (Top 10)

### Binary Classifier

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | dynamics_count | 0.053 | Structural |
| 2 | tempo_count | 0.035 | Structural |
| 3 | chord_vocabulary_size | 0.033 | Harmonic |
| 4 | pitch_class_entropy | 0.032 | Coherence |
| 5 | voice_crossing_count | 0.032 | Orchestration |
| 6 | total_duration_beats | 0.032 | Structural |
| 7 | time_sig_complexity | 0.030 | Structural |
| 8 | melodic_range | 0.030 | Melodic |
| 9 | rhythmic_independence | 0.030 | Coherence |
| 10 | pct_falling | 0.029 | Melodic |

### Regressor

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | dynamics_count | 0.060 | Structural |
| 2 | instrument_count | 0.046 | Orchestration |
| 3 | tempo_count | 0.041 | Structural |
| 4 | melodic_range | 0.039 | Melodic |
| 5 | pitch_class_entropy | 0.034 | Coherence |
| 6 | phrase_length_regularity | 0.033 | Coherence |
| 7 | num_sections | 0.032 | Structural |
| 8 | cadence_count_half | 0.031 | Harmonic |
| 9 | avg_range_utilization | 0.031 | Orchestration |
| 10 | melodic_autocorrelation | 0.031 | Coherence |

## Key Findings

### 1. dynamics_count is #1 by a wide margin

Both models agree. Pieces with dynamic markings (pp, mp, mf, ff, crescendo, decrescendo) are rated substantially higher. This is the single most actionable signal for LLM composition — **always add dynamics**.

Why: Skilled composers include performance instructions. The presence of dynamics is a proxy for compositional care. LLMs generating only notes without expression markings will be penalized.

### 2. Expression markers > musical content for prediction

dynamics_count and tempo_count (expression metadata) outperform harmonic and melodic features. This is a confound — expression markings correlate with composer skill but aren't the music itself. However, it's directly actionable: LLMs can trivially add dynamics and tempo markings.

### 3. Coherence features validate the LLM-targeting thesis

All 8 coherence features appear in the top half of importance rankings. pitch_class_entropy is #4-5 in both models. phrase_length_regularity and melodic_autocorrelation are top-10 in the regressor. These features were specifically designed to catch LLM failure modes and they carry genuine predictive signal even on human-composed music.

### 4. The classifier is weak but directionally correct

60% accuracy on a 0.5-point rating range is not impressive in isolation. But:
- It's statistically significant (p < 0.0001)
- The feature importance is stable across both models
- The primary value is the **interpretable feedback**, not the prediction
- The Isolation Forest handles the catastrophic failure modes

### 5. R² of 0.052 is honest

32 structural features explain ~5% of rating variance. The remaining 95% is genre popularity, arrangement quality, performer reputation, taste, and factors outside our feature set. This is expected and we frame it honestly in the report.

## What We'd Do Differently

1. **Try n_ratings >= 5 for more data** — 9.9K samples vs 5.6K. Noisier labels but more statistical power. Could A/B test this.
2. **Add genre as a feature** — we excluded it to learn genre-agnostic quality, but genre is clearly a confounder. Could try genre-conditioned models.
3. **Tune the threshold** — 4.76 is the median but maybe not optimal. Could sweep thresholds and plot accuracy/F1 curves.
4. **Feature engineering** — interactions between features (e.g., dynamics_count / total_duration_beats = dynamics per beat) might help.
5. **Try gradient boosting alternatives** — LightGBM or CatBoost for comparison.

## Files

| Artifact | Path |
|----------|------|
| Features CSV | `features.csv` (25,561 rows, 39 cols) |
| Binary classifier | `models/quality_classifier.joblib` |
| Regressor | `models/quality_regressor.joblib` |
| Distribution scorer | `models/distribution_scorer.joblib` |
| Classifier importance plot | `models/classifier_importance.png` |
| Regressor importance plot | `models/regressor_importance.png` |
| Target file list | `data/target_basenames.txt` |
| PDMX analysis plots | `analysis/plots/01-08_*.png` |
| Dashboard | `analysis/dashboard.py` (localhost:8501) |
