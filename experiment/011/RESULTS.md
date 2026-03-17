# Experiment 011 Results: JRPG Theme, Free Instrumentation

**Date:** 2026-03-17
**Result:** All scores down. Full orchestral writing is beyond LLM capability. More parts = worse music.

## Answer Key

| Listen | Score | Track | Condition | Parts |
|--------|-------|-------|-----------|-------|
| D | **73** | track_03 | v1-exp5 (PDMX + revise) | 9 |
| A | 70 | track_02 | v3-exp9 (canonical + autonomous) | 7 |
| B | 68 | track_01 | v1-exp9 (PDMX + autonomous) | 9 |
| C | 60 | track_04 | v3-exp5 (canonical + revise) | 6 |

## Verbatim Listener Feedback

### Listen_A (track_02 / v3-exp9) — 70/100

> Starts off harps, low bassoon? is that contrabassoon or bass. probably bass.
> 27 the ensemble comes in. They move together. Its almost angelic. But doesn't
> quite cohere.
>
> 55 is really pretty, the voices moving. But theres no... theres no clear top.
> Theres no sound pyramid in this orchestration. Theres no bass supporting a clear
> melody. Its everything happening all at once in the same pitch. Not even as good
> as the first jrpg try we had u do by default.

### Listen_B (track_01 / v1-exp9) — 68/100

> uh, weird, starts off very fucking similar with the harps. thats bizarre. then
> kicks in violin 1. oh this is quite a bit nicer bringing in the melody at 15-30.
> It feels like theres actually distinct voices in the ensemble, albeit some mixing
> issues
>
> oo, 45-48 sounds gross as fuck. fucking haunting, im not going to lie. while i
> *like this more* it also sounds ass.

### Listen_C (track_04 / v3-exp5) — 60/100

> the harps at the start remind me of ff14. same orchestral grossness. this shit
> is sort of ass. its pretty fucking cursed. im going to skip ahead a bit i cant
> handle 3 more minutes of this atonal stuff. oh its more the same

### Listen_D (track_03 / v1-exp5) — 73/100

> first without harps. simple, happy chords that are canonical. voices are sort
> of distinct, theres actually lines even if those lines sound bad.
>
> why the fuck does claude love minor chords so much. i think, all of these are
> bad, of their badness, D is the least bad, but thats cuz d is simple. the score
> differentials dont reflect it, all of these sort of suck bad.
>
> wait, d has a few bangers. alright fine d gets 73/100

## Analysis

### 1. The Orchestration Ceiling

The LLM can't orchestrate. It knows the JRPG orchestral vocabulary — harp arpeggios,
horn themes, string pads — from textual descriptions of the genre. But it can't manage
the vertical relationships between 6-9 simultaneous voices. The result: "no sound
pyramid," "everything happening all at once in the same pitch," "atonal," "cursed."

| Experiment | Parts | Avg Score |
|-----------|-------|-----------|
| 010 (cello + piano) | 2 | **87.3** |
| 009 (clarinet + piano) | 2 | 71.0 |
| **011 (full orchestra)** | **6-9** | **67.8** |

More parts = worse music. The LLM can write for 2 instruments but can't orchestrate
for 6-9. This is a second dimension of the competence ceiling: not just "what targets
can it hit" but "how many voices can it manage simultaneously."

### 2. Convergent Orchestration from Text

Every agent independently chose nearly identical instrumentation:
- Track 01: Harp, Flute, Oboe, Horn, Vln I, Vln II, Viola, Cello, Contrabass (9)
- Track 02: Flute, Horn, Harp, Vln I, Vln II, Viola, Cello (7)
- Track 03: Flute, Oboe, Horn, Harp, Piano, Vln I, Vln II, Viola, Cello (9)
- Track 04: Flute, Horn, Harp, Vln I, Viola, Cello (6)

All four opened with harp arpeggios (except track 03). They're all reconstructing
the Final Fantasy prelude trope from textual descriptions — "Uematsu uses harp
arpeggios" — without having seen actual MusicXML of it. The conceptual understanding
is correct; the execution fails at the counterpoint level.

### 3. Profile and Workflow Results

| Profile | Avg |
|---------|-----|
| v1 (PDMX) | **70.5** |
| v3 (canonical) | 65.0 |

| Workflow | Avg |
|----------|-----|
| exp9 (autonomous) | 69.0 |
| exp5 (revise) | 66.5 |

v1 wins, exp9 slightly ahead — but the differences are noise when all scores are bad.
The orchestration problem dominates everything else.

### 4. The Simplicity Pattern

The winner (D, 73/100) was described as "simple, happy chords that are canonical" and
"first without harps." The listener's preference pattern across all experiments:

- **Experiment 009:** Best = simple eighth-note melody (83)
- **Experiment 010:** Best = "continuous and flowing" call-and-response (90)
- **Experiment 011:** Best = "simple, happy chords" (73)

Simplicity wins. Every time.

### 5. The Minor Key Problem

> "why the fuck does claude love minor chords so much"

All four tracks gravitated toward C minor / D minor / G minor. This may reflect the
LLM's association of "epic" or "dramatic" JRPG themes with minor keys. The listener
consistently preferred major-key passages.

## What This Changes

1. **Orchestral writing is beyond current LLM capability** — stick to 2-3 parts max
2. **Instrumentation ceiling hierarchy**: cello+piano (87) > clarinet+piano (71) > full orchestra (68)
3. **Free instrumentation choice led all agents to full orchestra** — which is the wrong
   choice. If the system recommends instrumentation, it should cap at 2-3 parts.
4. **The "JRPG theme" vibe didn't help** — it triggered orchestral associations that
   the LLM can't execute. Vibe choice affects instrumentation choice affects quality.
5. **Minor key bias** is a consistent issue across experiments

## Files

- `experiment/011/answer_key.json` — Condition assignments
- `experiment/011/.blind_map.json` — Blind listening map
- `experiment/011/track_01/` through `track_04/` — Scores, scripts, notes
- `experiment/011/listen_A.mp3` through `listen_D.mp3` — Blinded audio
