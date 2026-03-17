# Rachmaniclaude

AI music composition and quality assessment. Claude composes MusicXML, a feature profile trained on 250K+ human-rated scores and 2,871 canonical masterworks provides feedback, and the results are rendered to audio via MuseScore.

**Best result:** 90/100 in a blind listening test, produced by a one-sentence vibe prompt with one round of advisory feedback. [Full report](report/musiclaude.md).

## Quick Start

### Prerequisites

- Python 3.10+
- [MuseScore 3](https://musescore.org/en/download) (for audio rendering)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (for composition)

### Install

```bash
git clone https://github.com/your-username/musiclaude.git
cd musiclaude
pip install -e ".[dev]"
```

### First-Time Setup

**1. Download the PDMX dataset** (for training your own models):

```bash
# Download from https://zenodo.org/records/14648209
# Place PDMX.csv in data/, extract mxl.tar.gz into data/
```

**2. Extract features and train models:**

```bash
musiclaude-extract --data-dir data/ --output features.csv
musiclaude-train --features features.csv --output models/
```

This produces the quality models in `models/` — the feature profile, XGBoost classifier/regressor, and Isolation Forest anomaly detector. These are required for the feedback loop.

**3. (Optional) Build the canonical profile:**

If you want the v3 canonical profile (trained on Bach, Beethoven, Mozart, etc. instead of MuseScore community ratings):

```bash
# Clone canonical corpora into data/
git clone https://github.com/OpenScore/Lieder.git data/openscore-lieder
git clone https://github.com/OpenScore/Quartets.git data/openscore-quartets
# ... see codex/experiments/006-canonical-corpus-pipeline.md for full list

# Extract features
python scripts/extract_canonical_features.py --workers 16

# Build profile
python scripts/build_canonical_profile.py
```

## Composing Music

### The Proven Approach: `/compose-minimal`

Our best results come from **minimal prompting** — give a vibe, let Claude compose freely, one round of advisory feedback. This was validated across 11 experiments.

In Claude Code:

```
/compose-minimal A chess game between old friends in a park
```

That's it. Claude will:
1. Choose instrumentation (2-3 parts, typically cello+piano)
2. Compose freely using music21
3. Run the quality profile for suggestions
4. Decide what feedback to incorporate or reject
5. Render to MP3

**Key findings from our experiments:**
- **2-3 parts max** — duos sound great (avg 87/100), full orchestra doesn't work (avg 68/100)
- **Cello+piano is the sweet spot** — the LLM writes idiomatically for cello
- **Feedback as suggestions, not mandates** — the model should reject feedback that would hurt coherence
- **One revision round** — more iterations degrade quality

### Use Any Coding Agent

The `/compose-minimal` skill is a Claude Code convenience, but MusicLaude's real value is the **quality assessment pipeline** — the feature profile, XGBoost importance ranking, and Isolation Forest anomaly detection. These work with any LLM-generated MusicXML, regardless of how it was produced.

You can compose with:
- **Claude Code** (via `/compose-minimal` or just asking Claude to write music)
- **OpenAI Codex** / ChatGPT
- **Any coding agent** that can write Python + music21

The workflow is always the same:
1. Have your agent generate a MusicXML score using music21
2. Run the MusicLaude feedback pipeline on it
3. Let the agent decide what to revise

```python
from musiclaude.compose.feedback import run_feedback_loop

result = run_feedback_loop(
    musicxml_path="path/to/score.musicxml",
    output_dir="output",
    profile_path="models/feature_profile_v3.joblib",
    quality_threshold=0.5,
    max_iterations=1,
)
print(result["critique_text"])  # Ranked suggestions for improvement
```

### Edit in MuseScore

Every generated `.musicxml` file can be opened directly in [MuseScore](https://musescore.org). This lets you:
- **See the full score** — notation, dynamics, articulations, everything the LLM wrote
- **Edit by hand** — fix wrong notes, adjust voicing, add expression marks
- **Re-render** — export to MP3/WAV/PDF from MuseScore's GUI
- **Iterate human + AI** — use MusicLaude for the first draft, polish in MuseScore

```bash
musescore3 output/score.musicxml  # Opens in MuseScore GUI
```

## Best Examples

Here are some highlights from our experiments — listen for yourself:

### "The Wager" — Cello + Piano (Experiment 010, 90/100)

*A chess game between old friends in a park — the stakes are a bottle of wine.*

- Score: [`examples/the_wager.musicxml`](examples/the_wager.musicxml)
- Audio: [`examples/the_wager.mp3`](examples/the_wager.mp3)
- Condition: v3 canonical profile + one revision round

### "The Bottle Gambit" — Cello + Piano (Experiment 010, 88/100)

*Same vibe, different agent, autonomous feedback.*

- Score: [`examples/the_bottle_gambit.musicxml`](examples/the_bottle_gambit.musicxml)
- Audio: [`examples/the_bottle_gambit.mp3`](examples/the_bottle_gambit.mp3)
- Condition: v3 canonical profile + autonomous feedback decisions

### "Matin de Boulangerie" — Clarinet + Piano (Experiment 009, 83/100)

*First love at 17, summer in a French village, working at a bakery.*

- Score: [`examples/matin_de_boulangerie.musicxml`](examples/matin_de_boulangerie.musicxml)
- Audio: [`examples/matin_de_boulangerie.mp3`](examples/matin_de_boulangerie.mp3)
- Condition: v1 PDMX profile + one revision round

### Legacy Skills

The original pipeline skills (`/compose`, `/song-contract`, `/assess-quality`) still exist but are not recommended. Experiments showed that rigid contract-to-skill pipelines consistently produce worse music than minimal prompting. See [experiment results](codex/INDEX.md) for details.

## Analysis Dashboard

```bash
streamlit run analysis/dashboard.py
```

Opens a Streamlit dashboard with interactive analysis of the PDMX dataset: rating distributions, feature importance, genre breakdowns, and more.

## Running Tests

```bash
pytest
```

40 tests covering feature extraction, classification, profile comparison, and validation.

## Project Structure

```
musiclaude/
  features/         Feature extraction from MusicXML (harmonic, melodic, structural, orchestration, coherence)
  classifier/        Quality assessment models (profile, XGBoost, Isolation Forest)
  validator/         Music theory structural validation
  compose/           Feedback loop infrastructure
  render.py          Audio rendering via MuseScore

.claude/skills/
  compose-minimal/   The experimentally validated approach (recommended)
  compose/           Legacy pipeline skill
  song-contract/     Legacy contract skill
  assess-quality/    Quality assessment skill

experiment/          Blind listening experiments (005-011)
codex/               Decision log, experiment writeups, gotchas
report/              Full research report with analysis plots
analysis/            Exploration scripts, plots, Streamlit dashboard
scripts/             Canonical corpus extraction and analysis
models/              Trained models (not committed, see setup)
data/                PDMX + canonical corpora (not committed)
```

## The Research

11 experiments
| Exp | What We Tested | Result |
|-----|---------------|--------|
| 001-004 | Feature extraction + classifier training | 60.2% accuracy, dynamics_count is #1 predictor |
| 005 | Blind A/B/C: profile vs XGBoost vs baseline | **Profile feedback wins** (+7 over baseline) |
| 006 | Canonical MusicXML corpus (2,871 pieces) | v3 profile built, 900% more hairpins than PDMX |
| 007 | Canonical feature targets | **REJECTED** — "clownhouse" music. The competence ceiling. |
| 008 | Canonical principles in prompt | **REJECTED** — "listening to nothing." Same problem. |
| 009 | Minimal prompting, 2x2 design | Minimal prompting works. Clarinet is weak. |
| 010 | Cello+piano, chess game vibe | **90/100!** Best result. v3 profile wins. |
| 011 | JRPG theme, free instrumentation | Full orchestra fails. 2 parts >> 6+ parts. |

**The central finding:** the less you constrain the LLM, the better it composes. Rigid pipelines, mandatory feature targets, and detailed contracts all produce worse music than a one-sentence vibe with advisory feedback.

Read the [full report](report/musiclaude.md) for the complete story.

## Citation

If you use this work, please cite:

```
MusicLaude: LLM Music Composition with Feature Profile Feedback
https://github.com/your-username/musiclaude
```

## License

MIT
