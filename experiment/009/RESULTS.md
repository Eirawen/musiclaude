# Experiment 009 Results: Minimal Prompting × Profile Choice

**Date:** 2026-03-17
**Result:** Mixed — minimal prompting massively improved coherence; exp5 workflow still wins; v3 profile surprisingly competitive

## Answer Key

| Listen | Score | Track | Condition |
|--------|-------|-------|-----------|
| D | **83** | track_03 | **v1-exp5** (PDMX profile + revise based on feedback) |
| C | 78 | track_01 | v3-exp9 (canonical profile + autonomous) |
| A | 73 | track_04 | v3-exp5 (canonical profile + revise based on feedback) |
| B | 50 | track_02 | v1-exp9 (PDMX profile + autonomous) |

## Verbatim Listener Feedback

### Listen_A (track_04 / v3-exp5) — 73/100

> Starts off with these gorgeous chords, but meanders for a while. Same issue with
> a weird clarinet, oh wow! the clarinet did a fucking trill! thats new! we haven't
> had a clarinet trill before! Another trill! Weird. okay now quite a few trills, a
> piano trill that time.
>
> Overall, a lot more cohesive than previous experiments. This feels like something
> with personality. IS THAT ALLARGANDO? IT FUCKING ALLARGANDOS. NONE OF THE PRIOR
> AGENTS DID ANY ALLARGANDO'ing.
>
> At this point I cant tell how much of this is me just really not liking the sound
> of the musescore clarinet or the key this is composed in. For being the star of
> the show, the clarinet doesn't quite shine as she should, and the pianos a bit
> repetitive, but this was nowhere near as insulting to listen to as before.

### Listen_B (track_02 / v1-exp9) — 50/100

> Simpler, also meanders for a while. Im not fond of the direction it takes the
> clarinet. I have to stop listening. This shit is sort of ass. Fine ill keep going.
> Interesting ideas around 1:15-1:21. Again, the entire piece is fucked because the
> clarinet just sounds like ass and never finds an identity.

### Listen_C (track_01 / v3-exp9) — 78/100

> The opening chord brings you in. This is the first version that feels like it
> understands the role of the piano in this piece. Which isn't to be grim, but is
> to be adolescent. AND THERE COMES THE FUCKING CLARINET ONCE MORE. MAYBE IT JUST
> CANT WRITE CLARINET LINES? LIKE OH MY GOD. but the segment from 0:52-1:02 is
> actually a really expressive portion of clarinet. Even if i think its all in the
> wrong key.
>
> 1:21 gets bold, and its a swing and a miss!
>
> by 1:30 its back to being the good piano from the start.
>
> The throughline is, wow, its good at the piano in this piece, and like all others,
> ass at the clarinet.

### Listen_D (track_03 / v1-exp5) — 83/100

> The first piece to open with the clarinet! And not have this weird 30 second piano
> intro to the piece! It opens with the piano and clarinet in twain. Its also the
> first piece that understands the clarinet at all! The clarinet is actually playing
> a melody! And it trills! OH IT HAS SUCH FUN IDEAS FROM 0:38-0:47! Its like a weird
> carnival type thing! This is the ONLY PIECE that to this point has made me feel
> anything like first love in the slightest, like a carousel.
>
> It starts fucking up the clarinet later on, and its not the greatest, its not a
> great piece, but we're forcing it to write piano/clarinet duos. Maybe its just bad
> at piano clarinet duos.

## Analysis

### 1. Minimal prompting massively improved coherence

| Experiment | Best score | Worst score | Listener tone |
|-----------|-----------|------------|---------------|
| 007 (contract + skill + canonical targets) | "intertwined" (1st place) | "clownhouse" | Horrified |
| 008 (contract + skill + wisdom) | preferred control | "listening to nothing" | Bored/repulsed |
| **009 (one-sentence vibe, no skill)** | **83** | **50** | **Engaged, specific critique** |

The listener went from "aimless" and "clownhouse" to specific musical feedback: "gorgeous
chords," "the clarinet did a trill!," "fun ideas like a carousel." The problem narrowed
from fundamental incoherence to a specific instrumental weakness (clarinet writing).

### 2. Exp5 workflow beats exp9

| Workflow | Avg score |
|----------|-----------|
| exp5 (revise based on feedback) | **78** |
| exp9 (autonomous — agent chooses) | 64 |

The agent exercising autonomous judgment produced worse results than the agent that
simply revised based on feedback. The "musician with taste" hypothesis didn't hold —
at least not yet. When the agent rejected suggestions to preserve "pastoral character,"
it was protecting something that wasn't actually working.

### 3. v3 canonical profile surprisingly competitive

| Profile | Avg score |
|---------|-----------|
| v3 (canonical) | **75.5** |
| v1 (PDMX) | 66.5 |

This contradicts experiment 007 where v3 lost decisively. The difference: in 007,
v3 was used with a rigid contract + skill pipeline. In 009, v3 was used with minimal
prompting. The canonical profile's higher targets may work BETTER when the agent has
freedom to pursue them naturally rather than being forced to retrofit them.

However, the overall winner was still v1-exp5. v3's average was pulled up by v3-exp9
(78) while v1's average was dragged down by v1-exp9 (50).

### 4. The clarinet problem

Across ALL conditions, the piano was decent and the clarinet was the weak link:
- "the clarinet just sounds like ass and never finds an identity"
- "MAYBE IT JUST CANT WRITE CLARINET LINES?"
- "ass at the clarinet"
- "the clarinet doesn't quite shine as she should"

Only v1-exp5 (track D) got even close: "the first piece that understands the clarinet
at all! The clarinet is actually playing a melody!" This suggests clarinet writing
specifically is a capability gap — the LLM may be better at piano idiom than wind
instrument idiom.

## Predictions vs Reality

| Prediction | Result |
|-----------|--------|
| exp9 will beat exp5 | **WRONG** — exp5 won (78 vs 64) |
| v1 will beat v3 | **WRONG** — v3 won on average (75.5 vs 66.5) |
| v1-exp9 will be overall winner | **WRONG** — v1-exp5 won (83) |
| All 4 more coherent than exp 008 | **CORRECT** — massive improvement |

## What This Changes

1. **Minimal prompting is validated** — no contract, no skill template, just a vibe +
   instrumentation. All 4 tracks more coherent than experiments 7-8.
2. **Exp5 workflow (revise based on feedback) is the proven winner** — validated in
   experiments 005, 007, 008, and now 009.
3. **v3 canonical profile deserves re-evaluation** — it failed under rigid pipelines
   (007) but was competitive under minimal prompting (009). The profile itself may
   not be the problem; the pipeline was.
4. **Clarinet writing is a specific capability gap** — next experiment should test
   different instrumentation to isolate whether the problem is clarinet-specific or
   general to non-piano instruments.
5. **Autonomous feedback rejection didn't help** — the agent's musical judgment isn't
   reliable enough to override statistical feedback. Keep feedback as "revise" not
   "consider."

## Files

- `experiment/009/answer_key.json` — Condition assignments
- `experiment/009/.blind_map.json` — Blind listening map
- `experiment/009/hypothesis.md` — Pre-registered hypothesis
- `experiment/009/track_01/` through `track_04/` — Scores, scripts, notes
- `experiment/009/listen_A.mp3` through `listen_D.mp3` — Blinded audio
