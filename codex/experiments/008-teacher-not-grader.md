# 008: Teacher Not Grader — Canonical Wisdom in the Compose Prompt

**Date:** 2026-03-17
**Status:** Complete
**Result:** HYPOTHESIS REJECTED

## Question

Does injecting compositional principles from canonical repertoire analysis into the
compose prompt (pre-composition guidance) produce better music than the baseline prompt?

## Background

Experiment 007 showed that canonical data as post-hoc feature targets fails — the LLM
hits Beethoven's numbers on paper but produces incoherent music ("clownhouse"). This
experiment tests the "teacher not grader" hypothesis: canonical data is valuable as
compositional wisdom BEFORE writing, not as feature counts to hit AFTER writing.

## The Canonical Wisdom

9 principles extracted by `scripts/analyze_canonical_patterns.py` from 198 richly
annotated canonical masterworks (pieces with dynamics>=10 AND hairpins>=5):

1. **Dynamics are structural** — 53% appear at phrase boundaries
2. **Establish character early** — 11% of dynamics in first 10% of piece
3. **Flat trajectories dominate** — 55% of pieces; loudest moment at median 26%
4. **Balance cresc/dim** — 0.92:1 ratio
5. **Staccato clusters** — 87.6% appear near other staccatos
6. **Accents on weak beats** — 67% off strong beats
7. **Dynamics follow pitch** — 46% rising pitch = rising dynamics
8. **Real expression vocabulary** — dolce, rall., a tempo, etc.
9. **Moderate dynamic range** — pp to ff, not extremes

Additionally, the wisdom-enhanced prompt includes an "Expression Plan" section in the
scratchpad template, requiring the composer to plan expression placement before writing.

## Setup

- **Piece:** *Matin de Boulangerie* — same contract as experiment 007
- **2 conditions:**
  - **control:** Original compose prompt (no wisdom) + v1 PDMX profile feedback
  - **wisdom:** Enhanced compose prompt (9 principles + expression plan) + v1 PDMX profile feedback
- **Both use v1 PDMX profile** — isolating the effect of pre-composition guidance
- **3 feedback iterations** each
- **Blinding:** Tracks randomized, answer key sealed before listening

## Results

**Ranking: control > wisdom**

The wisdom composer scored 41/42 features above median (vs 36/41 control) — better
on paper, worse to listen to. The listener described wisdom as "unpleasant to listen
to," "always minor," "listening to nothing at all." The control "felt like a song."

The canonical principles pushed the composer toward more chromatic, minor-key,
expressively complex territory — but without melodic fundamentals to support it.
This is the competence ceiling problem at a different layer: experiment 007 showed
canonical *targets* exceed LLM capability; experiment 008 shows canonical *principles*
exceed LLM capability.

Both tracks were called "aimless." The core problem is not expression or feature
targets — it's **fundamental melodic and harmonic competence**: phrases that go
somewhere, progressions with direction, rhythmic identity.

See `experiment/008/RESULTS.md` for full verbatim feedback and analysis.

## Files

- `experiment/008/hypothesis.md` — Pre-registered hypothesis and predictions
- `experiment/008/answer_key.json` — Condition assignments (sealed)
- `experiment/008/compose_control.md` — Control condition prompt
- `experiment/008/compose_wisdom.md` — Wisdom-enhanced condition prompt
- `experiment/008/track_01/` — Track 01 (score + scratchpad)
- `experiment/008/track_02/` — Track 02 (score + scratchpad)
