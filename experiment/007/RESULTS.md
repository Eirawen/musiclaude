# Experiment 007: Results

**Date:** 2026-03-17
**Hypothesis:** Canonical repertoire profiles (v3) will produce better compositions than PDMX community profiles (v1)
**Result:** HYPOTHESIS REJECTED. v1 won decisively.

## Answer Key

| Track | Profile | Source | Ranking |
|-------|---------|--------|---------|
| **01** | **v1-pdmx** | 5,894 MuseScore community uploads | **1st (clear winner)** |
| 02 | v3-full | 2,871 canonical pieces (all corpora) | 2nd (distant) |
| 04 | v3-lieder | 1,650 art songs + orchestral | 3rd |
| 03 | v3-dcml | 1,101 piano sonatas/quartets | 4th |

**Listener ranking: 01 >>>> 02 >> 04 > 03**

The four `>` symbols are the listener's — not a typo.

## Listener Feedback (Verbatim)

### Track 01 (v1-pdmx) — Winner
> "What a delightful surprise compared to track 2. I start off feeling like
> I'm just a little guy working at a store, by second 15 or so, it's like
> there's the girl. There she is.
>
> And when the clarinet hits, it feels like a personalized entrance. Like I'm
> asking her out on a date. The piano supports the clarinet and the clarinet
> supports the piano. They're intertwined, rather than fighting each other
> like I saw in track 02.
>
> At about 1:08 the relationship develops, and the changes in volume support
> this. What I really appreciate is that at about 1:38 or so, the model
> decrescendos the piano, but leaves the clarinet at the forefront, before
> even she fades away."

### Track 02 (v3-full) — 2nd place
> "I certainly did not feel like first love with this piece. I felt a lot more
> like I was almost in an argument. This is the first piece that sort of feels
> 'AI generated' in a sense. It has almost the skeleton of music to it, but
> there's no clear melody. It just doesn't sound good to listen to. I don't
> like it, to be honest, and it's hard to explain why. It feels drifting."

### Track 04 (v3-lieder) — 3rd place
> "Starts off on poor footing. Has the worst piano fundamentals of every
> single piece so far. There is not a chord that is in melody. It's like
> the first love between a very slow farmhand and the widowed butterchurner.
> Christ this piece sucks. Not a single piece of it is pleasant to listen to.
> From seconds 25-30 it ALMOST LOCKS IN but then it's just, fucking ass?
> It's almost like a clownhouse. Like something that would play in a horror
> film as a group of clowns gets ready to slaughter their unsuspecting audience."

### Track 03 (v3-dcml) — 4th place
> "If I had to guess which one was the OG profile before the additions, it'd
> be this one. Within the first 15 seconds you get a feel for the sort of
> naive simplicity of our old approaches. But there's nothing wrong with naive
> simplicity, in a way. It's not quite all that impressive though, it suffers
> from the same problem as track 2, it's not all that gripping, basically.
>
> Oh god, now we're at about 1:25 and it's starting to sound like track 04's
> clownhouse. I can tell it's doing interesting things now, it's playing a lot
> with volume, but the thing is that the piano just doesn't sound right."

## Feature Comparison

| Feature | Track 01 (v1) | Track 02 (v3-full) | Track 03 (v3-dcml) | Track 04 (v3-lieder) |
|---------|-------------|-------------------|-------------------|---------------------|
| Notes | 354 | 401 | 657 | 315 |
| Features ≥ median | 41/42 | 40/42 | 41/42 | 41/42 |
| Dynamics | 14 | 20 | 37 | 15 |
| Hairpins | 18 | 16 | 18 | 17 |
| Articulations | 183 | 53 | — | 158 |
| Chord types | 74 | 71 | 69 | — |

Track 03 has nearly DOUBLE the notes of any other track (657 vs 315-401).
Track 03 has more than double the dynamics (37 vs 14-20).

## The Key Finding

**Higher feature targets ≠ better music.**

The canonical profiles set targets that match what Beethoven, Schubert, and
Mozart achieved in their scores:
- dynamics_count median: 15 (v3) vs 8 (v1)
- hairpin_count median: 10 (v3) vs 1 (v1)
- staccato_count median: 9 (v3) vs 0 (v1)
- expression_count median: 10 (v3) vs 4 (v1)

The LLM successfully *hit* those targets — all tracks achieved 40-41/42 features
above their respective profile medians. But hitting Beethoven's numbers without
Beethoven's craft produced music that sounds like a "clownhouse."

## Why This Happened

### 1. The Competence Ceiling
An LLM generating MusicXML can competently handle a certain level of musical
complexity. The v1 profile (PDMX community uploads) set targets that fall within
this competence range. The v3 profiles (canonical masterworks) set targets beyond
it.

It's like giving a student driver Formula 1 performance targets. They'll hit the
numbers on paper but crash into every wall.

### 2. Expression Without Foundation
When the feedback loop says "add 15 dynamics and 10 hairpins," the LLM adds them.
But dynamics and hairpins only sound good when they're supported by coherent melody
and voice leading underneath. The listener said it clearly:

> "The piano supports the clarinet and the clarinet supports the piano. They're
> intertwined." (Track 01, v1)

vs.

> "The piano just doesn't sound right." (Tracks 03 and 04, v3)

The canonical profiles pushed for more markings, but the LLM couldn't write the
musical foundation to support them. The markings became noise layered on incoherence.

### 3. Density ≠ Quality
Track 03 (v3-dcml) had 657 notes — nearly double Track 01's 354. The DCML profile,
built from Beethoven sonatas full of running passages, pushed for higher note density.
But more notes from an LLM means more opportunities for wrong notes.

### 4. Community Music May Be the Right Reference
The PDMX community uploads are written by humans at a range of skill levels — many
are students, hobbyists, arrangers. Their expression levels (dynamics=8, hairpins=1)
may actually represent what *competent but non-masterful* music looks like. That's
a much better target for an LLM than canonical masterworks.

## Pre-registered Predictions vs Reality

| Prediction | Result |
|-----------|--------|
| v3-full will win overall | WRONG — v1 won |
| v3-lieder will score highest on expressiveness | WRONG — "clownhouse" |
| v3-dcml will score highest on structural coherence | WRONG — "piano doesn't sound right" |
| v1 will score lowest on expressiveness | WRONG — most expressive to the listener |
| All v3 variants will beat v1 | WRONG — v1 beat all of them |

**5/5 predictions wrong.** The hypothesis was comprehensively rejected.

## What This Changes

1. **Keep v1 (PDMX) as the default profile.** It works. Canonical data doesn't.
2. **The profile's job is to set achievable targets**, not ideal ones. The gap
   between "what great music has" and "what an LLM can competently produce" is
   the whole ballgame.
3. **Canonical corpus data is still valuable** — but as analysis material, not as
   profile targets. Understanding what makes Beethoven's dynamics work (voice
   leading, harmonic rhythm, motivic development) is different from telling an
   LLM "write 15 dynamics."
4. **The next improvement vector is probably not the profile** — it's the
   composition skill itself. Better MusicXML generation, better voice leading,
   better melodic coherence. Then the targets can be raised.
5. **The PDMX ratings, noisy as they are, accidentally captured something real:**
   the level of musical complexity that non-expert composers can execute well.
   That's exactly the LLM's peer group.

## The Irony

We spent hours downloading 2,871 canonical masterworks, hacking MuseScore version
headers, running 16-worker parallel extraction, building subset profiles from
Lieder, DCML, and orchestral corpora — and the best music came from the profile
we already had.

But this is how science works. The negative result is the finding. Now we know:
**match the profile to the composer's capabilities, not to the ideal.**

## Files

- `experiment/007/track_01/` through `track_04/` — scores, MP3s, scratchpads
- `experiment/007/answer_key.json` — condition assignments
- `experiment/007/the_conversation.md` — the song design conversation
- `experiment/007/all_scratchpads.md` — all 4 composers' planning documents
- `experiment/007/hypothesis_canonical_profile.md` — pre-registered predictions
