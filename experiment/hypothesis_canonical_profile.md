# Hypothesis: Canonical Repertoire Profile (v3)

**Date**: 2026-03-16
**Status**: Pre-test

## Hypothesis

A feature profile built from canonical MusicXML repertoire (OpenScore Lieder,
String Quartets, Orchestral works, DCML analysis corpus) will produce better
composition feedback than our current PDMX-only profile (v1), because:

1. **No rating noise**: PDMX ratings are noisy (R²=0.039). Canonical repertoire
   IS definitionally good music — no human ratings needed.
2. **Real notation markings**: MusicXML scores have explicit dynamics, hairpins,
   articulations, tempo markings. No inference from MIDI velocity needed.
3. **Genre diversity**: Lieder (art songs), string quartets, orchestral works,
   piano sonatas — broader than PDMX's MuseScore community uploads.
4. **Higher quality floor**: Every piece is published, performed, canonical.
   PDMX includes student exercises and arrangements.

## Datasets

| Corpus | Files | Format | Genres |
|--------|-------|--------|--------|
| OpenScore Lieder | 1,462 | mxl | Art songs (voice+piano) |
| OpenScore Quartets | 122 | mscx→mxl | String quartets |
| OpenScore Orchestra | 188 | mxl | Orchestral movements |
| DCML Corpus | 1,101 | mscx→mxl | Piano sonatas, quartets, etc. |
| **Total** | **~2,873** | | |

Plus optionally: MAESTRO (1,276 MIDI with velocity inference — piano only).

## Predictions

1. **Expressive features will shift up**: dynamics_count, hairpin_count,
   articulation_count medians will increase vs PDMX profile — canonical pieces
   have richer expressive markings than average MuseScore uploads.
2. **Structural features will be more consistent**: section_count,
   phrase_length_regularity will have tighter distributions — canonical pieces
   follow classical form more reliably.
3. **Compositions guided by this profile will sound more "professional"**:
   The feedback will push toward more dynamic contrast, better phrasing,
   and richer harmonic vocabulary.
4. **Risk — piano/vocal bias**: Heavy piano representation (DCML, Lieder,
   MAESTRO) could skew features like note_density and avg_range_utilization
   toward keyboard norms. Orchestral corpus helps but is smallest subset.

## Test Plan

1. Build canonical profile (v3) alongside existing v1 (PDMX-only)
2. Compose same piece twice — once with v1 feedback, once with v3 feedback
3. Blind listening test (same protocol as experiment 005)
4. Compare feature distributions v1 vs v3
