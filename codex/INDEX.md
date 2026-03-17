# MusicLaude Codex

LLM-composed music as structured text (MusicXML), quality-assessed by feature profile comparison against canonical repertoire distributions, iteratively improved via ranked feedback. Core thesis: feature importance from XGBoost training is stable and actionable — telling an LLM "your dynamics_count is at the 3rd percentile, target is 14" produces better music than predicting a rating. Canonical repertoire (Bach, Beethoven, Mozart, Schubert, Chopin) IS definitionally good music — no human ratings needed.

## Top-Level

| File | Purpose |
|------|---------|
| [decisions.md](decisions.md) | Architectural decisions and their rationale |
| [gotchas.md](gotchas.md) | Known pitfalls, footguns, and things that surprised us |

## Features (Feature Extraction Pipeline)

42+ features across 5 modules, extracted via music21 from MusicXML files.

| File | Purpose |
|------|---------|
| [features/feature-catalog.md](features/feature-catalog.md) | Complete catalog of all features: name, module, range, what it measures, why it matters |
| [features/decisions.md](features/decisions.md) | Feature engineering decisions and rationale |
| [features/gotchas.md](features/gotchas.md) | music21 parsing pitfalls, edge cases in MusicXML |

## Classifier (Quality Assessment Models)

Feature profile (primary) + XGBoost (secondary) + Isolation Forest anomaly detection.

| File | Purpose |
|------|---------|
| [classifier/architecture.md](classifier/architecture.md) | Three-signal design: feature profile (primary feedback), XGBoost (secondary reference), distribution scorer (anomaly detection) |
| [classifier/decisions.md](classifier/decisions.md) | Model choices, hyperparameters, threshold decisions |
| [classifier/gotchas.md](classifier/gotchas.md) | Training pitfalls, PDMX data quality issues |

## Compose (LLM Composition Pipeline)

Claude Code skills: `/song-contract` → `/compose` (with profile feedback loop) → `/assess-quality` (optional).

| File | Purpose |
|------|---------|
| [compose/pipeline.md](compose/pipeline.md) | End-to-end composition workflow, skill interactions, feedback loop mechanics |
| [compose/musicxml-reference.md](compose/musicxml-reference.md) | MusicXML generation patterns, duration math, common templates |
| [compose/decisions.md](compose/decisions.md) | Skill design decisions |

## Dataset (PDMX + Canonical Corpora)

Training data analysis and canonical reference corpora.

| File | Purpose |
|------|---------|
| [dataset/pdmx-analysis.md](dataset/pdmx-analysis.md) | PDMX dataset analysis: rating distribution, filtering rationale, genre bias, selection bias |
| [dataset/pdmx-paper-notes.md](dataset/pdmx-paper-notes.md) | Notes from the PDMX paper (arXiv:2409.10831) |

**Canonical corpora** (in `data/`, not committed): OpenScore Lieder (1,462 art songs), OpenScore Orchestra (188), OpenScore Quartets (122), DCML (1,101 piano sonatas/quartets). ~2,873 pieces of definitionally good music with real notation markings. See experiment 006.

## Experiments

Experiment logs with setup, results, findings, and what we'd do differently.

| File | Purpose |
|------|---------|
| [experiments/001-baseline-training.md](experiments/001-baseline-training.md) | First training run: XGBoost + Isolation Forest on 25.6K PDMX files. Key finding: dynamics_count is #1 predictor, 60.2% accuracy is statistically significant (p < 0.0001) |
| [experiments/002-dedup-pdmx-features.md](experiments/002-dedup-pdmx-features.md) | Deduplication + PDMX metadata features (complexity, scale_consistency, groove_consistency). Accuracy 60.2% → 63.5%. Data quality > data quantity. |
| [experiments/003-performance-directives.md](experiments/003-performance-directives.md) | Disaggregated performance directives into 5 features. Binary accuracy dipped slightly but regressor R² jumped 41%. All new features in top half of importance. |
| [experiments/004-self-computed-features.md](experiments/004-self-computed-features.md) | Replaced PDMX metadata with self-computed scale_consistency + groove_consistency, dropped complexity. Models now work on new compositions. |
| [experiments/005-blind-abc-listening.md](experiments/005-blind-abc-listening.md) | **Blind A/B/C listening test.** 3 songs × 3 conditions. Profile feedback wins 2/3, +7.0 avg over baseline vs +1.3 for XGBoost. Profile set as default. |
| [experiments/006-canonical-corpus-pipeline.md](experiments/006-canonical-corpus-pipeline.md) | **Canonical MusicXML corpora.** MIDI inference → MusicXML insight. MuseScore version hack, 2,873 canonical pieces, v3 profile with 12x more hairpins than PDMX. |

## Report

| File | Purpose |
|------|---------|
| [../report/musiclaude.md](../report/musiclaude.md) | Full paper draft with sections 1-10, TODO placeholders for results |

## Listening Study

| File | Purpose |
|------|---------|
| [../analysis/listening_study.py](../analysis/listening_study.py) | Streamlit A/B listening study for classifier validation |

## Validator (Music Theory Checks)

Structural and music-theory validation.

| File | Purpose |
|------|---------|
| [validator/checks.md](validator/checks.md) | Complete list of validation checks, severity levels, and what triggers them |
