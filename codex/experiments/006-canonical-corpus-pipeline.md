# 006: Canonical MusicXML Corpus Pipeline

**Date:** 2026-03-16
**Status:** Complete

## The Insight

> "The original premise of pdmx was that human rating mattered — it sure as fuck
> does not, and is noisy as shit." — Khaled

PDMX ratings gave us R²=0.039. But we don't need ratings at all. The feature
profile system works by comparing a composition against *distributions of good
music*. And canonical repertoire IS definitionally good music — Bach, Beethoven,
Mozart, Schubert, Chopin. No stars needed.

## The Journey

### Step 1: MIDI velocity inference (the hard way)

First attempt was MAESTRO — 1,276 competition piano performances as MIDI files.
Built `midi_inference.py` to infer dynamics and hairpins from velocity:

**Bug 1 — note-level vs window-level inference:**
Note-by-note velocity analysis produced absurd values (hairpin_count=72 vs
expected ~1-20). Switched to window-based analysis (16-beat windows for dynamics,
8-beat for hairpins) which matches human notation scale.

**Bug 2 — `part.recurse()` gives measure-relative offsets:**
A 2,347-note piece showed all offsets in range 0-4 (one measure!). The fix:
use `score.flatten()` which gives absolute offsets (0-1570 range).

**Bug 3 — staccato/accent can't be inferred from MIDI:**
Piano key release naturally creates gaps = looks like staccato everywhere
(116-316 detected vs MusicXML median 2). Velocity variation = looks like accents
(12-69 vs PDMX median 0). Dropped these entirely — only dynamics_count and
hairpin_count are reliably inferable from MIDI velocity.

**Conclusion:** MIDI inference is a lossy approximation. Why approximate when
real notation exists?

### Step 2: MusicXML corpora (the right way)

Canonical MusicXML scores have ALL features with real notational markings:

| Corpus | Extracted | Format | Content |
|--------|-----------|--------|---------|
| OpenScore Lieder | 1,462 | mxl | Art songs (Schubert, Schumann, Wolf, etc.) |
| OpenScore Orchestra | 188 | mxl | Symphonies (Beethoven, Bruckner, Dvořák, etc.) |
| OpenScore Quartets | 120 | mscx→mxl | String quartets (Beethoven, Boccherini, etc.) |
| DCML | 1,101 | mscx→mxl | Piano sonatas, quartets (Mozart, Beethoven, Chopin, Grieg) |
| **Total** | **2,871** | | 2 failures (Janáček — unusual notation) |

### Step 3: The MuseScore version hack

music21 can't parse `.mscx` files. musescore3 can convert them to `.mxl`, BUT:

```
Cannot read file K310-1_reviewed.mscx:
This score was saved using a newer version of MuseScore.
```

Installed musescore3 is v3.2.3; files were saved with v3.6.2. The version check
is in the XML header. **The hack:**

```python
content = content.replace(
    '<museScore version="3.02">', '<museScore version="3.01">'
).replace(
    "<programVersion>3.6.2</programVersion>",
    "<programVersion>3.2.3</programVersion>",
)
```

Patching the XML header bypasses the version check. The actual format differences
between 3.2 and 3.6 are minor enough that conversion works perfectly.

**Result:** 1,223/1,223 files converted, 0 failures. The Leland font falls back
to Bravura (cosmetic only), and some measures have minor rounding warnings.

### Step 4: Feature extraction at scale

Extraction pipeline: `scripts/extract_canonical_features.py`
- ProcessPoolExecutor with checkpointing every 100 results
- Resume support (skips already-processed files)
- Corpus tagging (each row has a `corpus` column — sliceable for subset profiles)

First batch (Lieder + Orchestra, 4 workers): 1,650 pieces, 0 failures, ~10 min
Second batch (DCML + Quartets, 16 workers): 1,221 pieces, 2 failures, ~12 min

**Lesson:** 4 workers → 16 workers cut time from ~2 hours to ~12 minutes. music21
is CPU-bound, not I/O-bound, and DCML piano sonata movements are small files.

### Step 5: The final profile (v3)

Built `models/feature_profile_v3.joblib` from all 2,871 canonical pieces.

**v3 (Canonical, 2,871 pieces) vs v1 (PDMX rated, 5,894 pieces):**

| Feature | v1 (PDMX) | v3 (Canonical) | Shift |
|---------|-----------|----------------|-------|
| dynamics_count | 8 | **15** | +87% |
| hairpin_count | 1 | **10** | +900% |
| staccato_count | 0 | **9** | new baseline |
| expression_count | 4 | **10** | +150% |
| articulation_count | 23 | **30** | +30% |
| accent_count | 0 | **1** | new baseline |
| voice_crossing_count | 1 | **6** | +500% |
| pitch_class_entropy | 3.00 | **3.12** | richer chromaticism |
| num_parts | 2 | **3** | broader ensembles |
| total_duration_beats | 253 | **192** | shorter but denser |

Canonical pieces are dramatically more expressive *per beat*. Beethoven's
Op.2 No.1 alone has 73 dynamics — the average PDMX high-rated piece has 8.

### Corpus sliceability

The `corpus` column enables building targeted profiles from any subset:

| Profile variant | Pieces | Character |
|----------------|--------|-----------|
| All canonical (v3) | 2,871 | Broad classical reference |
| Lieder only | 1,462 | Voice+piano, song form, lyrical |
| DCML only | 1,101 | Piano sonatas/quartets, classical form |
| Lieder + Orchestra | 1,650 | Pre-DCML baseline |
| Orchestra only | 188 | Full orchestral, rich orchestration |
| Quartets only | 120 | Chamber music, voice leading |

Any combination can be built by filtering `canonical_features.csv` on `corpus`
before passing to `build_canonical_profile.py`.

## Gotchas discovered

- **G13:** `.mscx` not parseable by music21 — convert via musescore3 CLI
- **G14:** musescore3 version check is a bypassable XML header patch
- **G15:** 16+ workers for mixed-size corpora (large orchestral files dominate at 4 workers)
- **G16:** MIDI staccato/accent inference is unreliable — only dynamics/hairpins work

## Scripts

- `scripts/convert_mscx_to_mxl.py` — Batch mscx→mxl with version hack (1,223 files, 0 failures)
- `scripts/extract_canonical_features.py` — Parallel extraction with checkpointing and corpus tagging
- `scripts/build_canonical_profile.py` — Build v3 profile from canonical data, compare with v1
- `scripts/extract_maestro_features.py` — MAESTRO MIDI extraction (secondary)
- `scripts/fix_maestro_inference.py` — Recalibrate MIDI velocity inference values

## Artifacts

| File | What |
|------|------|
| `data/canonical/canonical_features.csv` | 2,871 × 45 feature matrix with corpus tags |
| `models/feature_profile_v3.joblib` | Canonical profile (all 2,871 pieces) |
| `models/feature_profile.joblib` | PDMX profile v1 (untouched, for blind test) |
| `data/maestro/maestro_features.csv` | 1,276 MAESTRO MIDI features (secondary) |
| `experiment/hypothesis_canonical_profile.md` | Pre-registered hypothesis |

## What's next

See experiment 007 for the blind listening test results.

**Spoiler:** The canonical profiles lost. Badly. The old PDMX profile produced the
only composition the listener actually liked. Higher feature targets ≠ better music
when the composer (LLM) can't execute at that level. See 007 for the full analysis.
