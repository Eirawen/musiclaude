# MusicLaude

AI music composition and quality assessment system.

## Composition — The Right Way

**Use `/compose-minimal`** — give a one-sentence vibe, get a score. This is the experimentally validated approach (11 experiments, best score 90/100).

```
/compose-minimal A chess game between old friends in a park
```

Key rules from our experiments:
- **2-3 parts max** — duos (cello+piano) score avg 87. Full orchestra (6+ parts) scores avg 68. The LLM can't orchestrate.
- **Feedback is advisory** — the model should reject suggestions that would hurt coherence
- **One revision round** — more iterations degrade quality
- **Don't use rigid pipelines** — no contracts, no templates, no forced iteration loops. They consistently produce worse music.

The legacy skills (`/compose`, `/song-contract`, `/assess-quality`) still exist but are not recommended.

## Project Structure
- `musiclaude/features/` - Feature extraction from MusicXML (42+ features)
  - `harmonic.py` - Chord vocabulary, extended chords, cadences, key stability, modulations
  - `melodic.py` - Intervals, stepwise motion, range, contour, rhythm, repetition
  - `structural.py` - Parts, duration, dynamics, tempo, time signature complexity, sections
  - `orchestration.py` - Instruments, voice crossings, range utilization, doubling
  - `coherence.py` - LLM-targeted: note density, rest ratio, pitch/interval entropy, melodic autocorrelation, phrase regularity, strong-beat consonance, rhythmic independence
  - `extract.py` - Pipeline: directory → DataFrame with all features
- `musiclaude/classifier/` - Quality assessment models
  - `profile.py` - **Primary feedback**: percentile-based comparison, ranked by feature importance
  - `train.py` - XGBoost classifier + regressor + distribution scorer training
  - `predict.py` - QualityPredictor combining XGBoost + anomaly detection (secondary reference)
  - `distribution.py` - Isolation Forest anomaly scorer
- `musiclaude/validator/` - Music theory structural validation
- `musiclaude/compose/` - Feedback loop infrastructure
- `.claude/skills/compose-minimal/` - **Recommended**: minimal vibe → compose → advisory feedback
- `.claude/skills/compose/` - Legacy pipeline skill (not recommended)
- `experiment/` - 11 blind listening experiments (005-011)
- `codex/` - Decision log, experiment writeups, gotchas
- `report/` - Full research report with analysis plots
- `analysis/` - Exploration scripts, plots, Streamlit dashboard
- `scripts/` - Canonical corpus extraction and analysis
- `tests/` - Test suite (40 tests)
- `data/` - PDMX + canonical corpora (not committed)
- `models/` - Trained models (not committed)
- `output/` - Generated compositions (not committed)

## Dataset
- **PDMX** from Zenodo: https://zenodo.org/records/14648209 — 254K MusicXML files with user ratings
- **Canonical corpora** — 2,871 masterworks from OpenScore Lieder/Orchestra/Quartets + DCML

## Commands
- `pip install -e ".[dev]"` - Install in dev mode
- `pytest` - Run tests (40 tests)
- `musiclaude-extract --data-dir data/ --output features.csv` - Extract features
- `musiclaude-train --features features.csv --output models/` - Train classifier + distribution scorer
- `streamlit run analysis/dashboard.py` - Launch analysis dashboard

## Quality Assessment
**Primary signal:** Feature Profile (`models/feature_profile_v3.joblib` or `models/feature_profile.joblib`) — compares each feature against reference distributions using percentile ranks, weighted by XGBoost feature importance. v3 (canonical) outperforms v1 (PDMX) under minimal prompting.

**Secondary signals (reference only):**
- XGBoost regressor/classifier — R²=0.039, useful for feature importance ranking not predictions
- Isolation Forest — flags music outside human-composed distributions

## Tech Stack
- music21 for MusicXML parsing and score generation
- XGBoost for quality classification + feature importance
- scikit-learn Isolation Forest for anomaly detection
- Claude Opus for composition via Claude Code
- MuseScore 3 CLI for audio rendering
