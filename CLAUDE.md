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
  - `profile.py` - **Primary feedback**: percentile-based comparison against high-rated PDMX distributions, ranked by feature importance
  - `train.py` - XGBoost classifier + regressor + distribution scorer training
  - `predict.py` - QualityPredictor combining XGBoost + anomaly detection (secondary reference)
  - `distribution.py` - Isolation Forest anomaly scorer for detecting "not real music"
- `musiclaude/validator/` - Music theory structural validation
- `musiclaude/compose/` - LLM composition pipeline (validation, feedback loop)
- `.claude/skills/` - Claude Code skills: `/song-contract`, `/compose`, `/assess-quality`
- `experiment/` - Blind A/B/C listening experiment (3 songs × 3 feedback conditions)
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
1. `/song-contract` - Conversation to define what music to compose → outputs `song_contract.md`
2. `/compose` - Generate MusicXML from contract, run profile feedback loop (up to 3 iterations), render MP3
3. `/assess-quality` - Run additional assessment iterations if needed

## Quality Assessment
**Primary signal:** Feature Profile (`models/feature_profile.joblib`) — compares each extracted feature against high-rated PDMX distributions using percentile ranks, weighted by XGBoost feature importance. Gives ranked, specific improvement instructions (e.g., "your dynamics_count=0 is at the 3rd percentile, target median is 8").

**Secondary signals (reference only):**
- XGBoost regressor/classifier — predicts ratings, but R²=0.039 on narrow rating range makes absolute scores unreliable
- Isolation Forest distribution scorer — flags music that deviates from human-composed distributions

Profile feedback was validated in a blind A/B/C experiment (2026-03-16): profile-revised compositions scored +7 points over baselines on average, vs +1.3 for XGBoost feedback. See `experiment/RESULTS.md`.

## Tech Stack
- music21 for MusicXML parsing
- XGBoost for quality classification
- scikit-learn Isolation Forest for anomaly detection
- Claude for composition generation
