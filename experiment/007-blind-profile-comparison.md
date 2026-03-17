# Experiment 007: Blind Profile Comparison

**Date:** 2026-03-16
**Status:** Protocol designed, awaiting execution

## Question

Does a feature profile built from canonical repertoire (v3) produce better
composition feedback than one built from PDMX community ratings (v1)?

## Profiles under test

| Code | Profile | Source | Pieces |
|------|---------|--------|--------|
| **A** | v1 | PDMX high-rated (rating≥median, n_ratings≥10) | 5,894 |
| **B** | v3-full | All canonical corpora | 2,871 |
| **C** | v3-lieder | Lieder + Orchestra only (pre-DCML) | 1,650 |
| **D** | v3-dcml | DCML only (piano sonatas, quartets) | 1,101 |

Conditions A–D will be shuffled and relabeled as Track 01–04 per song.
The listener (Khaled) will not know which profile produced which track.

## Why 4 conditions, not 2?

The corpus is sliceable — each subset has a different character:
- Lieder = lyrical, voice+piano, song form
- DCML = classical form, piano sonatas, developmental
- Full = all of the above + orchestra + quartets

If DCML hurts (too piano-focused) or helps (adds formal rigor), we'll see it.
If Lieder alone is enough, we save complexity.

## Protocol

### Step 1: Song contract
Khaled defines ONE song via `/song-contract`. Same contract for all conditions.
Pick something that exercises expression (not just a 12-bar blues).

### Step 2: Composition (blinded)
Claude composes the same contract 4 times in separate contexts, each with a
different profile loaded. Each composition goes through the full `/compose`
pipeline (3 feedback iterations).

Output files are named neutrally:
```
experiment/007/track_01.musicxml
experiment/007/track_02.musicxml
experiment/007/track_03.musicxml
experiment/007/track_04.musicxml
```

The answer key is sealed in `experiment/007/answer_key.json` (created before
listening, not opened until ratings are complete).

### Step 3: Render audio
All 4 tracks rendered to MP3 via musescore3:
```
experiment/007/track_01.mp3
experiment/007/track_02.mp3
experiment/007/track_03.mp3
experiment/007/track_04.mp3
```

### Step 4: Blind listening
Khaled listens to all 4 tracks (randomized order) and rates each on:

1. **Overall quality** (0-100)
2. **Expressiveness** — dynamics, articulation, phrasing (0-10)
3. **Harmonic interest** — chord variety, voice leading (0-10)
4. **Structural coherence** — form, phrasing, development (0-10)
5. **Would you listen again?** (yes/no)
6. **Free-form notes** — what stood out, what annoyed you

### Step 5: Reveal + analysis
Open answer key, map tracks to profiles, analyze results.

## Predictions (pre-registered)

1. **v3-full (B) will win overall** — broadest reference, most balanced
2. **v3-lieder (C) will score highest on expressiveness** — Lieder are the
   most expressively marked genre in our corpus
3. **v3-dcml (D) will score highest on structural coherence** — sonata form
   is the most formally rigorous structure
4. **v1 (A) will score lowest on expressiveness** — PDMX medians are much
   lower for dynamics/hairpins/expression
5. **All v3 variants will beat v1** — canonical data is simply richer

## What you (Khaled) need to do

1. **Define a song contract** — something moderately ambitious (not too simple,
   not a full symphony). A piano piece with a slow section and a fast section
   would exercise dynamics and tempo well. Or a chamber piece (piano + violin).

2. **Don't look at the composition process** — I'll compose all 4 versions and
   give you only the MP3s with neutral filenames.

3. **Listen and rate** — fill in the scorecard for each track.

4. **Tell me your ratings** — I'll reveal the answer key and we'll analyze.

## Timing

- Song contract: ~5 minutes
- 4 compositions × 3 iterations: ~20-30 minutes (can be parallelized)
- Audio rendering: ~2 minutes
- Listening + rating: ~15-20 minutes
- Analysis: ~5 minutes

Total: ~1 hour if compositions are parallelized.
