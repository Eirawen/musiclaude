# MusicLaude

Music generation and quality assessment system.

## Project Structure
- `musiclaude/features/` - Feature extraction from MusicXML
  - `harmonic.py` - Chord vocabulary, extended chords, cadences, key stability, modulations
  - `melodic.py` - Intervals, stepwise motion, range, contour, rhythm, repetition
  - `structural.py` - Parts, duration, dynamics, tempo, time signature complexity, sections
  - `orchestration.py` - Instruments, voice crossings, range utilization, doubling
  - `coherence.py` - LLM-targeted: note density, rest ratio, pitch/interval entropy, melodic autocorrelation, phrase regularity, strong-beat consonance, rhythmic independence
  - `extract.py` - Pipeline: directory → DataFrame with all features
- `musiclaude/classifier/` - Quality assessment models
  - `train.py` - XGBoost classifier + regressor + distribution scorer training
  - `predict.py` - QualityPredictor combining XGBoost + anomaly detection
  - `distribution.py` - Isolation Forest anomaly scorer for detecting "not real music"
- `musiclaude/validator/` - Music theory structural validation
- `musiclaude/compose/` - LLM composition pipeline (validation, feedback loop)
- `.claude/skills/` - Claude Code skills: `/song-contract`, `/compose`, `/assess-quality`
- `tests/` - Test suite (40 tests)
- `data/` - PDMX dataset (not committed)
- `models/` - Trained models (not committed)
- `output/` - Generated compositions (not committed)

## Dataset
PDMX dataset from Zenodo: https://zenodo.org/records/14648209
- Download `PDMX.csv` (index with ratings), `mxl.tar.gz` (MusicXML files), `metadata.tar.gz`
- Rating field: `rating` (0-5 stars, 0=unrated)
- Key fields: song_name, rating, n_ratings, n_tracks, n_notes, genres, tags

## Commands
- `pip install -e ".[dev]"` - Install in dev mode
- `pytest` - Run tests (40 tests)
- `musiclaude-extract --data-dir data/ --output features.csv` - Extract features
- `musiclaude-train --features features.csv --output models/` - Train classifier + distribution scorer

## Composition Workflow
1. `/song-contract` - Define what music to compose
2. `/compose` - Generate MusicXML from contract
3. `/assess-quality` - Evaluate with classifier + distribution scorer, iterate

## Quality Assessment: Two Signals
1. **XGBoost** - Predicts ratings from PDMX training data (good for general quality)
2. **Distribution Scorer** - Isolation Forest on feature distributions, flags music that doesn't look like human-composed music (catches LLM failure modes: no rests, monotone rhythm, random-walk melody)

## Tech Stack
- music21 for MusicXML parsing
- XGBoost for quality classification
- scikit-learn Isolation Forest for anomaly detection
- Claude for composition generation
