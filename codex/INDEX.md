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

## Validator (Music Theory Checks)

Structural and music-theory validation.

| File | Purpose |
|------|---------|
| [validator/checks.md](validator/checks.md) | Complete list of validation checks, severity levels, and what triggers them |
