# Experiment 003 — Disaggregated Performance Directives

**Date:** 2026-03-16
**Status:** Complete
**Previous:** [002-dedup-pdmx-features.md](002-dedup-pdmx-features.md)

## What Changed

Added 5 new features by disaggregating performance directives (inspired by PDMX paper noting 12M directives):
- `hairpin_count` — crescendo/decrescendo wedges (DynamicWedge)
- `articulation_count` — total note-attached articulations
- `staccato_count` — staccato + staccatissimo
- `accent_count` — accent + strong accent
- `expression_count` — expressions excluding RehearsalMark (fermatas, trills, ornaments)

Extracted via `scripts/extract_new_features.py` (re-parsed all 25K files, merged into features_v2.csv).

## Results

| Metric | Exp 002 | Exp 003 (this) | Change |
|--------|---------|-------|--------|
| Features | 35 | 40 (+5 directive types) | |
| Binary Accuracy | **0.635** | 0.621 | -1.4% |
| Binary F1 | **0.690** | 0.683 | -0.7% |
| RMSE | 0.149 | **0.147** | **-0.002** |
| R² | 0.039 | **0.055** | **+41% relative** |

**Split outcome:** Regressor significantly improved. Binary classifier slightly dipped. Classic bias-variance tradeoff — more correlated features dilute binary tree splits but help continuous prediction.

## Feature Importance — Regressor (the winner)

| Rank | Feature | Importance | New? |
|------|---------|------------|------|
| 1 | complexity | 0.050 | |
| 2 | tempo_count | 0.044 | |
| 3 | dynamics_count | 0.035 | |
| 4 | **hairpin_count** | 0.035 | **YES** |
| 5 | **staccato_count** | 0.031 | **YES** |
| 6 | **accent_count** | 0.031 | **YES** |
| 7 | scale_consistency | 0.029 | |
| 8 | **expression_count** | 0.028 | **YES** |
| 9 | total_duration_beats | 0.028 | |
| 10 | melodic_autocorrelation | 0.027 | |

All 5 new features landed in the top half. hairpin_count tied for #3 (with dynamics_count). The regressor now has a much richer picture of "how expressive is this score."

## Key Findings

### 1. Performance directives are NOT just a single signal
Breaking dynamics_count into its components revealed that hairpins, staccatos, accents, and expressions each carry independent predictive power. The regressor R² jumped 41% from this decomposition alone.

### 2. Staccato specifically predicts quality
staccato_count at #5 in the regressor suggests that scores with articulate, detailed notation (where the composer specified exactly how each note should be played) rate higher. This is actionable for LLMs: don't just write notes, specify articulations.

### 3. Binary classifier may need feature selection
The accuracy dip suggests 40 features is getting noisy for binary classification with 5.2K samples. Could try: (a) feature selection via RFECV, (b) regularization, (c) only use top-20 features for binary, full set for regression.

### 4. The regressor is becoming the more useful model
R² went from 0.039 → 0.055 (+41%). With continuous prediction, we get finer-grained feedback for the composition loop than binary good/not-good.

## Implications for LLM Composition Feedback

Updated actionable list:
1. **Add dynamics** (dynamics_count) — spot dynamics like pp, mf, ff
2. **Add hairpins** (hairpin_count) — crescendo and decrescendo wedges
3. **Add staccato markings** (staccato_count) — don't leave all notes legato by default
4. **Add accents** (accent_count) — mark emphasized notes
5. **Use tempo markings** (tempo_count) — include metronome marks and tempo text
6. **Add expressions** (expression_count) — fermatas, trills, ornaments
7. **Use compound/irregular meters** (time_sig_complexity)
8. **Rich chord vocabulary** (chord_vocabulary_size)
9. **Build in rests** (rest_ratio)
10. **Use motivic development** (melodic_autocorrelation)

## Files

| Artifact | Path |
|----------|------|
| Features v2 CSV | `features_v2.csv` (25,561 rows, 44 cols) |
| New feature extraction script | `scripts/extract_new_features.py` |
| Models | `models/` (overwritten) |
