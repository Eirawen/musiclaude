# Experiment 005: Blind A/B/C Listening Test

**Date:** 2026-03-16
**Status:** Complete
**Commit:** fbea00b

## Question

Does feature profile feedback produce better compositions than XGBoost score feedback or no feedback at all?

## Setup

- **Songs:** 3 (piano waltz, violin-piano duet, piano prelude)
- **Conditions:** 3 per song
  - **Baseline** — Raw first draft from Claude, no feedback loop
  - **XGBoost** — One revision round using XGBoost predicted rating + feature deficiency list
  - **Profile** — One revision round using percentile-based feature profile ranked by importance
- **Evaluation:** Blind (listener received 9 randomized MP3s numbered 01-09, no condition labels)
- **Listener:** Project PI (N=1)
- **Randomization:** Fixed seed (42) for reproducibility, answer key saved to `.answer_key.json`

All conditions used the same Claude model (Opus) and same song prompts. Baseline compositions were generated first, then features extracted and fed through both feedback systems to produce revision instructions. Revision agents composed independently guided by their respective feedback.

## Results

| Song | Baseline | XGBoost | Profile | Winner |
|------|----------|---------|---------|--------|
| Waltz | 88 | 82 | **93** | Profile (+5) |
| Duet | 83 | **86** | 84 | XGBoost (+3) |
| Prelude | 55 | 62 | **70** | Profile (+15) |
| **Average** | **75.3** | **76.7** | **82.3** | **Profile (+7.0)** |

Profile wins 2/3 songs. Both feedback methods beat baseline in every song (except XGBoost hurt the waltz: 82 vs 88 baseline).

## Key Findings

1. **Profile feedback is 5x more effective than XGBoost feedback** (+7.0 vs +1.3 avg improvement over baseline)
2. **XGBoost can hurt compositions** — the waltz regressed from 88→82. Listener mistook the XGBoost version for the unrevised baseline ("simplest, least expressive")
3. **Profile pieces praised for musicality** — "subtle touches", "actual style", "felt like a human playing it"
4. **Profile creates better iteration foundations** — listener said of duet/profile (84): "I'd rather iterate on this one than the other two" despite xgboost scoring 86
5. **Listener correctly identified all 3 song families blind** — grouped variants correctly without knowing which was which

## Why Profile Wins

XGBoost feedback says: "Predicted rating: 4.6/5.0, P(good): 97%. Feature deficiencies: dynamics_count below threshold."

Profile feedback says: "**dynamics_count** = 0 (percentile 3 in high-rated music, target median: 8). Add dynamic markings throughout the score. **hairpin_count** = 0 (percentile 12, target: 1). Add crescendo and decrescendo hairpins to shape phrases."

The difference is specificity and ranking. Profile tells Claude *exactly what to fix* in *priority order* with *concrete targets*. XGBoost gives a score and a flat list. Claude responds to specific instructions with specific improvements ("subtle touches"); it responds to vague signals with vague changes (or over-correction).

## Limitations

- N=1 listener — directionally useful, not statistically significant
- 3 songs — small sample, though effect sizes are large
- Single revision round — profile might compound advantages over multiple iterations
- Listener is the project PI — potential for unconscious bias (mitigated by blind design)

## What Changed

- Profile feedback set as default pathway in `/compose` and `/assess-quality`
- XGBoost retained as secondary reference signal
- `/compose` now includes automatic profile feedback loop (up to 3 iterations)

## What We'd Do Differently

- More songs (10+) for statistical power
- Multiple listeners for inter-rater reliability
- Multiple revision rounds to test compounding effects
- Include a "random feedback" control to establish the value of *any* structured feedback vs profile-specific feedback
