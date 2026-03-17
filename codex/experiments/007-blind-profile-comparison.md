# 007: Blind Profile Comparison — Canonical vs PDMX

**Date:** 2026-03-17
**Status:** Complete
**Result:** HYPOTHESIS REJECTED

## Question

Does a feature profile built from 2,871 canonical masterworks produce better
composition feedback than one built from noisy MuseScore community ratings?

## Answer

**No.** The PDMX profile (v1) won decisively. All three canonical profiles
produced music the listener described as "clownhouse," "AI generated," "drifting,"
and "the piano just doesn't sound right."

## Setup

- **Piece:** *Matin de Boulangerie* — piano + clarinet, 6/8, F major, ~80 measures,
  5-section narrative (morning routine → first meeting → conversation → walking
  home → alone with the memory)
- **4 conditions** composed in parallel by independent agents, each with 3
  feedback iterations:
  - v1-pdmx: 5,894 MuseScore community uploads
  - v3-full: 2,871 canonical pieces (all corpora)
  - v3-dcml: 1,101 piano sonatas/quartets (Mozart, Beethoven, Chopin)
  - v3-lieder: 1,650 art songs + orchestral works
- **Blinding:** Tracks randomized as 01-04, answer key sealed before listening

## Results

**Ranking: v1-pdmx >>>> v3-full >> v3-lieder > v3-dcml**

The listener's words for v1: *"The piano supports the clarinet and the clarinet
supports the piano. They're intertwined."*

The listener's words for v3-lieder: *"It's almost like a clownhouse. Like something
that would play in a horror film as a group of clowns gets ready to slaughter their
unsuspecting audience."*

## The Key Finding

**Profile targets must match the composer's capabilities, not the ideal.**

All four tracks hit 40-41/42 features above their respective profile medians.
The LLM successfully hit Beethoven's numbers on paper. But hitting Beethoven's
dynamics count (15) without Beethoven's voice leading produced incoherent music
with correct-looking metadata.

The PDMX profile targets (dynamics=8, hairpins=1) fall within what the LLM can
competently execute. The canonical targets (dynamics=15, hairpins=10) don't.

This is the **competence ceiling problem**: the profile should be calibrated to
the composer, not to the reference corpus.

## Predictions vs Reality

5/5 pre-registered predictions wrong. The hypothesis was comprehensively rejected.

## What This Changes

1. **v1 (PDMX) remains the default profile** — validated twice now (experiments
   005 and 007)
2. **Canonical data is valuable for analysis, not as targets** — understanding
   what makes Beethoven work ≠ telling an LLM to write like Beethoven
3. **Next improvement vector: composition quality**, not profile targets. Better
   voice leading, melodic coherence, harmonic foundations. Then targets can rise.
4. **PDMX "noise" may be signal** — community composers' expression levels may
   represent what competent-but-non-masterful music looks like, which is exactly
   the LLM's peer group

## Files

- `experiment/007/RESULTS.md` — full results with verbatim listener feedback
- `experiment/007/the_conversation.md` — the song design conversation
- `experiment/007/all_scratchpads.md` — all 4 composers' planning documents
- `experiment/007/answer_key.json` — condition assignments
- `experiment/007/track_01/` through `track_04/` — scores, MP3s, scratchpads
