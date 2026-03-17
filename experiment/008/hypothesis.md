# Experiment 008: Teacher Not Grader — Canonical Wisdom in the Compose Prompt

**Date:** 2026-03-17
**Status:** Pre-registered

## Hypothesis

Injecting compositional principles derived from canonical repertoire analysis into the
compose prompt (pre-composition guidance) will produce better music than the baseline
compose prompt, even when both use the same v1 PDMX feature profile for feedback.

## Rationale

Experiment 007 showed that canonical data as post-hoc feature targets fails — the LLM
hits Beethoven's numbers on paper but produces incoherent music. The hypothesis here is
that the canonical data is valuable as *teaching* (compositional wisdom before writing)
rather than *grading* (feature counts to hit after writing).

The 9 principles injected into the compose prompt are:
1. Dynamics are structural, not decorative (53% at phrase boundaries)
2. Establish character early (11% of dynamics in first 10%)
3. Don't default to quiet→loud arcs (55% flat trajectory, loudest at 26%)
4. Balance crescendo and diminuendo (0.92:1 ratio)
5. Staccato travels in packs (87.6% clustering)
6. Accents highlight the unexpected (67% on weak beats)
7. Dynamics follow pitch contour (46% rising pitch = rising dynamics)
8. Use real expression vocabulary (dolce, rall., a tempo, etc.)
9. Dynamic range is moderate (pp to ff, not extremes)

## Design

- **Piece:** Same contract as experiment 007 — *Matin de Boulangerie*
- **2 conditions:**
  - **control:** Original compose skill prompt (no wisdom section) + v1 profile feedback
  - **wisdom:** Enhanced compose skill prompt (with canonical wisdom) + v1 profile feedback
- **Both use v1 PDMX profile** — isolating the effect of pre-composition guidance
- **3 feedback iterations** each
- **Blinding:** Tracks randomized as track_01/track_02, answer key sealed before listening

## Predictions

1. The wisdom-enhanced composition will have more contextually appropriate expression
   (dynamics at phrase boundaries, staccato in passages, accents on weak beats)
2. The wisdom-enhanced composition will sound more "intentional" and less "sprinkled"
3. Both compositions will score similarly on feature counts (same profile feedback)
4. The difference will be in musical coherence, not feature hit rates

## What would change our mind

- If control sounds equally good → the principles are too abstract to be actionable
- If wisdom sounds worse → the principles are constraining rather than guiding
- If both sound the same → the LLM already knows this implicitly
