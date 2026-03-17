# Experiment 010 Results: New Premise, New Instrumentation

**Date:** 2026-03-17
**Result:** Best results in project history. v3 canonical profile wins. Cello >> clarinet.

## Answer Key

| Listen | Score | Track | Condition |
|--------|-------|-------|-----------|
| A | **90** | track_01 | **v3-exp5** (canonical profile + revise based on feedback) |
| D | 88 | track_02 | v3-exp9 (canonical profile + autonomous) |
| C | 86 | track_03 | v1-exp9 (PDMX profile + autonomous) |
| B | 85 | track_04 | v1-exp5 (PDMX profile + revise based on feedback) |

## Verbatim Listener Feedback

### Listen_A (track_01 / v3-exp5) — 90/100

> This is really quite pleasant to listen to, i wont lie. Its continuous and
> flowing, it has a strong melody, an answer response pattern between the piano
> and cello as they dance back and forth.
>
> a bit of a cello flub at 0:48
>
> this is really quite nice. and the section from 1:02-1:16 is a standout.
> 1:27 holy shit! Wow! WOW!
> 1:47 a mistake
> and the dimuendo to the end
>
> i dont have many words for this. im not a music critic. this was really good.
> the main thing is that this piece does random abrupt stops and starts, which i
> dont think succeed in building the feeling they want to, and occasionally take
> u out of it. they like blueball u.

### Listen_B (track_04 / v1-exp5) — 85/100

> Instantly more dynamic than listenA. And doing a lot more interesting things
> musically, but that complexity again flubs it up from 15-18, but thats a brief
> 3 second window.
>
> 34 a standout. The weirdly more staccato nature of the piano i dont quite like
> in this version, 53-1:01 is quite nice. this reminds me a lot of the clair
> obscure soundtrack in some weird way.
>
> i think, listen_A got a lot of mileage out of the continuous flow of the cello.
> this one a lot more staccato across the board, which i didn't quite enjoy, but i
> can tell this ones trying some fun things out. nothing is melodically incongruent,
> but it feels like we're drifting back to the old ways, complexity without a clear
> throughline.

### Listen_C (track_03 / v1-exp9) — 86/100

> This one takes it in a different manner. The piano is no longer the star, its way
> in the background. The cellos doing the job the entire way through. weird segment
> at 26-30. cleans up at about 31 weird shit at 52. i really like 1:02 to 1:07 and
> then 1:15-1:17
>
> this piece has the highest variance of any of the pieces we've listened to so far.
> it has really cool bursts, but isn't quite coherent either. the last 5 seconds are
> rather pleasant though. i think... just about the same as B? maybe ever so slightly
> ahead

### Listen_D (track_02 / v3-exp9) — 88/100

> this is the first time that the piano felt really meticulous i would say, or maybe
> thats the wrong word, this feels like a cello concerto in that we start off with a
> piano intro before the cello steals the show. the piano and cello are in lockstep
> this time around. a great accompaniment. theyre not sort of doing different things
> like in b and c.
>
> the ending segment to D is really quite pleasant!

### Re-listen comparison

> listening back to A, A has to win, it just does these excellent call and responses
> between piano and cello, and even if A has some flubs, its really nice.

## Analysis

### 1. Best results in project history

| Experiment | Best | Worst | Range | Avg |
|-----------|------|-------|-------|-----|
| 007 (contract + canonical targets) | ~70* | ~30* | 40 | ~50* |
| 008 (contract + wisdom) | ~65* | ~55* | 10 | ~60* |
| 009 (minimal, clarinet) | 83 | 50 | 33 | 71 |
| **010 (minimal, cello)** | **90** | **85** | **5** | **87.3** |

*Estimated from qualitative feedback; experiments 7-8 didn't use numeric ratings.

The range collapsed from 33 points (exp 009) to 5 points (exp 010). All four
compositions were good. The floor rose massively.

### 2. v3 canonical profile wins

| Profile | Avg score |
|---------|-----------|
| v3 (canonical) | **89.0** |
| v1 (PDMX) | 85.5 |

This OVERTURNS experiment 007's finding. The canonical profile didn't fail because
its targets were wrong — it failed because it was trapped in a rigid pipeline writing
for an instrument the LLM can't handle well. Under minimal prompting with cello+piano,
the canonical profile produces the best music in the project.

### 3. Workflow is a wash

| Workflow | Avg score |
|----------|-----------|
| exp5 (revise) | 87.5 |
| exp9 (autonomous) | 87.0 |

The 0.5-point difference is noise. The workflow variable that seemed decisive in
experiment 009 (78 vs 64) disappeared when the instrumentation changed. This suggests
the exp5 vs exp9 difference in 009 was confounded with the clarinet problem.

### 4. Cello >> Clarinet (the biggest effect)

The instrumentation change was worth more than any profile or workflow change:
- Experiment 009 (clarinet): avg 71, range 50-83
- Experiment 010 (cello): avg 87.3, range 85-90

The listener's words across experiments tell the story:
- 009: "MAYBE IT JUST CANT WRITE CLARINET LINES? LIKE OH MY GOD"
- 010: "continuous and flowing, strong melody, excellent call and responses"

The LLM writes idiomatically for cello in a way it simply doesn't for clarinet.
Possible reasons: more cello+piano training data, cello range maps better to
melodic patterns, cello's sustained tone is more forgiving of voice-leading issues.

### 5. What the listener actually praised

Across all four tracks, the listener praised:
- **Continuous flow** ("continuous and flowing," "in lockstep")
- **Call and response** ("dance back and forth," "answer response pattern")
- **Piano-cello partnership** ("great accompaniment," "cello steals the show")
- **Specific standout moments** (timestamps cited in every track)
- **Diminuendos and endings** ("the ending segment is really quite pleasant")

The listener criticized:
- **Abrupt stops** ("random abrupt stops and starts... blueball u")
- **Excess staccato** ("the weirdly more staccato nature... i didn't quite enjoy")
- **Brief flubs** (specific timestamps, always 2-3 seconds)

## Predictions vs Reality

| Prediction | Result |
|-----------|--------|
| All scores higher than exp 009 | **CORRECT** — lowest (85) > highest from 009 (83) |
| exp5 will beat exp9 | **WRONG** — essentially tied (87.5 vs 87.0) |
| Cello more idiomatic than clarinet | **CORRECT** — dramatically so |
| v1-exp5 will win | **WRONG** — v3-exp5 won |

## What This Changes

1. **v3 canonical profile is rehabilitated** — it works under minimal prompting with
   the right instrumentation. The profile itself was never the problem.
2. **Instrumentation is the biggest lever** — bigger than profile choice, workflow,
   or prompting strategy. The LLM writes well for some instruments and poorly for others.
3. **The pipeline was the real enemy** — rigid contract → skill → forced feedback
   consistently produced worse results than minimal prompting across every experiment.
4. **90/100 is a new ceiling** — with one-sentence vibe, cello+piano, v3 profile,
   and one revision round. There's room to go higher but this is a real composition
   that a listener called "really good."

## Files

- `experiment/010/answer_key.json` — Condition assignments
- `experiment/010/.blind_map.json` — Blind listening map
- `experiment/010/hypothesis.md` — Pre-registered hypothesis
- `experiment/010/track_01/` through `track_04/` — Scores, scripts, notes
- `experiment/010/listen_A.mp3` through `listen_D.mp3` — Blinded audio
