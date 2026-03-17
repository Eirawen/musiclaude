# Experiment 008 Results: Teacher Not Grader

**Date:** 2026-03-17
**Result:** HYPOTHESIS REJECTED (again)

## Answer Key

| Track | Condition | Features above median |
|-------|-----------|----------------------|
| track_01 | wisdom (canonical principles) | 41/42 |
| track_02 | control (no wisdom) | 36/41 |

**Ranking: control > wisdom**

## Verbatim Listener Feedback

### Track 01 (wisdom)

> Nice chords. Some occasionally weird off stepped notes, but i rather like the
> chords of the piano. Its rather melancholy though, doesn't feel like first love.
> More like longing for love, if that makes any sense.
>
> The clarinets rather out of place, always minor, always always minor, never in
> a major key. The brains clinging for something and it just doesn't work.
>
> And to that extent, theres this expressive phrase from like 1:25 to 1:40 that
> feels like—
>
> 1:45 gets this piano solo segment that for a brief second feels like a melody,
> a flash of melody. And then its gone.

### Track 02 (control)

> Independently and identically distributed melody line, what i mean is that,
> its a straight through line of eighth notes. a constant 123 456 123 456 on
> the pianos right hand.
>
> But its, on a whole, a lot less gloomy! And it feels like a song. Not a
> particularly, good song, mind you, but a song nonetheless.

### Comparative

> Just, these pieces are both so aimless. I prefer 2 to 1 but thats not like,
> a necessity. I can tell 1 has better underlying ideas its just like, so
> unpleasant to listen to. not in the old experiment way where its a clownhouse
> mess of chromatics but in a more, its like listening to nothing at all. just
> minor keys that are slightly off putting with their usage of accidentals.

## Analysis

### The Pattern Repeats

Experiment 007 tested canonical feature *targets* — LLM hit Beethoven's numbers,
produced incoherent music. Experiment 008 tested canonical compositional *principles*
— LLM followed Beethoven's rules, produced ambitiously broken music.

The wisdom composer scored 41/42 features above median (vs 36/41 control). It had
"better underlying ideas." But the listener described it as "unpleasant to listen to"
and "listening to nothing at all." The control's simple eighth-note patterns "felt
like a song."

### Why the Wisdom Hurt

The 9 canonical principles pushed the composer toward:
- **More complex expression** — accents on weak beats, dynamics following pitch
  contour, staccato passages, balanced crescendo/diminuendo
- **More chromatic territory** — the clarinet was "always minor, always always
  minor" with "off-putting accidentals"
- **More ambitious structure** — but without the melodic fundamentals to support it

The wisdom was *accurate* (canonical composers DO put accents on weak beats, DO
cluster staccatos, DO place dynamics at phrase boundaries). But applying these
principles requires a foundation of:
1. Coherent melody (phrases that go somewhere and resolve)
2. Harmonic direction (not just correct chords but functional progression)
3. Rhythmic identity (not "aimless" note sequences)

Without that foundation, the wisdom produces music that is *correctly decorated
but fundamentally empty*.

### The Competence Ceiling (Layer 2)

| Experiment | What we gave the LLM | Result |
|------------|---------------------|--------|
| 005 | v1 PDMX profile feedback | Best so far (validated) |
| 007 | Canonical feature targets | "Clownhouse" — hit numbers, lost coherence |
| 008 | Canonical compositional principles | "Listening to nothing" — followed rules, lost melody |

The improvement vector is not targets OR principles. It's **fundamental compositional
competence**: write a melody that goes somewhere. The LLM needs to learn to walk
(coherent phrases, functional harmony, rhythmic identity) before it can run
(expressive nuance, structural dynamics, accent placement).

### What Both Tracks Share

The listener called both pieces "aimless." Neither condition solved the core problem:
the LLM doesn't know how to write a melody with direction, tension, and resolution.
The wisdom track dressed this up with better expression; the control track kept it
simple. Neither track made the listener feel "first love in a French village."

## Predictions vs Reality

| Prediction | Result |
|-----------|--------|
| Wisdom will have more contextually appropriate expression | YES — but it didn't help |
| Wisdom will sound more "intentional" | NO — it sounded more melancholy/minor |
| Both will score similarly on feature counts | NO — wisdom scored much higher (41 vs 36) |
| Difference will be in coherence, not hit rates | PARTLY — coherence was worse in wisdom |

## What This Changes

1. **v1 profile + original compose prompt remains the best** — validated in experiments
   005, 007, and now 008
2. **Canonical wisdom as pre-composition guidance doesn't work either** — the principles
   are correct but require a compositional foundation the LLM doesn't have
3. **Next improvement vector: melodic and harmonic fundamentals** — teach the LLM to
   write a melody that resolves, chord progressions with direction, phrases with
   beginning/middle/end. This is more basic than expression or feature targets.
4. **The canonical data is still valuable for analysis** — understanding what makes
   music work, even if we can't yet transfer that understanding to the LLM

## Files

- `experiment/008/answer_key.json` — Condition assignments
- `experiment/008/hypothesis.md` — Pre-registered hypothesis
- `experiment/008/compose_control.md` — Control condition prompt
- `experiment/008/compose_wisdom.md` — Wisdom-enhanced condition prompt
- `experiment/008/track_01/` — Wisdom track (score, scratchpad, generate.py)
- `experiment/008/track_02/` — Control track (score, scratchpad, generate scripts)
