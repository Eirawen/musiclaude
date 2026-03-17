# 009: Minimal Prompting × Profile Choice

**Date:** 2026-03-17
**Status:** Complete
**Result:** Mixed — minimal prompting validated, exp5 workflow wins, v3 surprisingly competitive

## Question

Does giving the agent maximum creative freedom (one-sentence vibe, no contract/skill)
improve composition quality? Does treating feedback as suggestions (agent can reject)
beat mandatory revision?

## Answer

**Minimal prompting: YES.** All 4 tracks massively more coherent than experiments 7-8.
Listener went from "clownhouse"/"aimless" to specific musical critique ("gorgeous chords,"
"fun ideas like a carousel").

**Autonomous feedback: NO.** Exp5 workflow (revise based on feedback) beat exp9
(agent chooses) 78 vs 64 avg. The agent's musical judgment isn't reliable enough
to override statistical feedback.

**v3 canonical profile: SURPRISINGLY GOOD** under minimal prompting (avg 75.5 vs v1's
66.5). Failed under rigid pipelines (exp 007) but competitive when agent has freedom.

**Overall winner: v1-exp5 (83/100)** — the original experiment 5 approach, again.

## The Clarinet Finding

Across all 4 conditions, the piano was decent and the clarinet was the weak link.
Only one track (v1-exp5) managed a passable clarinet: "the first piece that understands
the clarinet at all!" This suggests clarinet writing is a specific capability gap.

## Key Takeaway

The pipeline was the problem, not the profile or the principles. Removing the rigid
contract → skill → forced iteration pipeline and just letting the agent compose with
a vibe produced the best results across the board.

See `experiment/009/RESULTS.md` for full verbatim feedback and analysis.
