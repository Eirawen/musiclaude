# MusicLaude Codex

LLM-composed music as structured text (MusicXML), quality-assessed by a trained classifier, iteratively improved via feedback loop. Core thesis: XGBoost on 32 musical features predicts human ratings, and distribution anomaly detection catches LLM-specific failure modes.

## Top-Level

| File | Purpose |
|------|---------|
| [decisions.md](decisions.md) | Architectural decisions and their rationale |
| [gotchas.md](gotchas.md) | Known pitfalls, footguns, and things that surprised us |

## Features (Feature Extraction Pipeline)

32 features across 5 modules, extracted via music21 from MusicXML files.

| File | Purpose |
|------|---------|
| [features/feature-catalog.md](features/feature-catalog.md) | Complete catalog of all 32 features: name, module, range, what it measures, why it matters |
| [features/decisions.md](features/decisions.md) | Feature engineering decisions and rationale |
| [features/gotchas.md](features/gotchas.md) | music21 parsing pitfalls, edge cases in MusicXML |

## Classifier (Quality Assessment Models)

XGBoost binary/regression + Isolation Forest anomaly detection.

| File | Purpose |
|------|---------|
| [classifier/architecture.md](classifier/architecture.md) | Two-signal design: XGBoost (rating prediction) + distribution scorer (anomaly detection) |
| [classifier/decisions.md](classifier/decisions.md) | Model choices, hyperparameters, threshold decisions |
| [classifier/gotchas.md](classifier/gotchas.md) | Training pitfalls, PDMX data quality issues |

## Compose (LLM Composition Pipeline)

Claude Code skills: `/song-contract` → `/compose` → `/assess-quality`.

| File | Purpose |
|------|---------|
| [compose/pipeline.md](compose/pipeline.md) | End-to-end composition workflow, skill interactions, feedback loop mechanics |
| [compose/musicxml-reference.md](compose/musicxml-reference.md) | MusicXML generation patterns, duration math, common templates |
| [compose/decisions.md](compose/decisions.md) | Skill design decisions |

## Dataset (PDMX Analysis)

Exploration and statistical analysis of the training data.

| File | Purpose |
|------|---------|
| [dataset/pdmx-analysis.md](dataset/pdmx-analysis.md) | Full dataset analysis with plots: rating distribution, filtering rationale, genre bias, complexity profile, selection bias |
| [dataset/pdmx-paper-notes.md](dataset/pdmx-paper-notes.md) | Notes from the PDMX paper (arXiv:2409.10831): validates our approach, 3-axis listening study design, dedup strategy, MusicRender format |

## Experiments

Experiment logs with setup, results, findings, and what we'd do differently.

| File | Purpose |
|------|---------|
| [experiments/001-baseline-training.md](experiments/001-baseline-training.md) | First training run: XGBoost + Isolation Forest on 25.6K PDMX files. Key finding: dynamics_count is #1 predictor, 60.2% accuracy is statistically significant (p < 0.0001) |
| [experiments/002-dedup-pdmx-features.md](experiments/002-dedup-pdmx-features.md) | Deduplication + PDMX metadata features (complexity, scale_consistency, groove_consistency). Accuracy 60.2% → 63.5%. Data quality > data quantity. |
| [experiments/003-performance-directives.md](experiments/003-performance-directives.md) | Disaggregated performance directives into 5 features. Binary accuracy dipped slightly but regressor R² jumped 41%. All new features in top half of importance. |

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
