# Experiment 009: Minimal Prompting × Profile Choice

**Date:** 2026-03-17
**Status:** Pre-registered

## Hypothesis

Giving the agent maximum creative freedom with minimal prompting, and treating
profile feedback as suggestions (not mandates), will produce better music than
the constrained skill pipeline — regardless of which profile is used.

## Design

**2×2 factorial:**

| | v1 (PDMX) | v3 (Canonical) |
|---|-----------|----------------|
| **exp5 workflow** (compose freely, revise based on feedback) | v1-exp5 | v3-exp5 |
| **exp9 workflow** (compose freely, feedback as suggestions — agent chooses) | v1-exp9 | v3-exp9 |

**Prompt:** One-sentence vibe only. No contract, no skill template, no scratchpad format.

**Key difference between workflows:**
- exp5: Agent composes, sees feedback, revises to address it (one round)
- exp9: Agent composes, sees feedback, decides FOR ITSELF what to incorporate or reject.
  The agent is the musician. The feedback is advisory, not mandatory.

## Predictions

1. exp9 workflow will beat exp5 workflow (autonomy > compliance)
2. v1 profile will beat v3 profile (competence ceiling still applies)
3. v1-exp9 will be the overall winner (right profile + right workflow)
4. All 4 tracks will be more coherent than experiment 008's tracks (less constraint = more coherence)

## What would change our mind

- If exp5 beats exp9 → the agent needs structure, not freedom
- If v3 beats v1 → the competence ceiling only applies under constrained workflows
- If all 4 sound equally aimless → the problem is deeper than workflow/profile
