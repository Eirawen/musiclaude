# Rachmaniclaude

Language model music composition and quality assessment. Claude composes MusicXML, a feature profile trained on 250K+ human-rated scores and 2,871 canonical masterworks provides feedback, and the results are rendered to audio via MuseScore.

**Best result:** a blind listening test favorite, from a one-sentence vibe prompt with one round of advisory feedback. [Full report](report/rachmaniclaude.md).

## Get Started

```bash
git clone https://github.com/Eirawen/musiclaude.git
cd musiclaude
conda env create -f environment.yml
conda activate rachmaniclaude
pip install -e .
```

You'll also need:
- [MuseScore 3](https://musescore.org/en/download) — renders MusicXML to MP3
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — or any coding agent that can write Python

Pre-trained models ship in `models/` — you're ready to compose immediately.

## Compose Your First Piece

Open Claude Code in the repo and run:

```bash

~/musiclaude claude

/compose-minimal your example here

/compose-minimal A chess game between old friends in a park

```

That's it. Claude will:
1. Choose instrumentation (2-3 parts, typically cello+piano)
2. Compose freely using music21
3. Run the quality profile for feedback
4. Decide what suggestions to accept or reject
5. Render to MP3 via MuseScore

Your score lands in `output/` as both `.musicxml` and `.mp3`.

### What We Learned 

After 11 experiments and a lot of blind listening:
- **2-3 parts max** — duos sound good, full orchestra falls apart. The LLM can't orchestrate.
- **Cello+piano is the sweet spot for duets**
- **Feedback as suggestions, not mandates** — the agent must be instructed that it can freely reject validator advice
- **One revision round** — more iterations degrade quality.
- **Less constraint = better music** — rigid pipelines, contracts, and mandatory targets all make things worse

## Use Any Coding Agent

`/compose-minimal` is a Claude Code convenience, but the real value is the **quality assessment pipeline**. It works with any LLM-generated MusicXML:

1. Have your agent generate a MusicXML score using music21
2. Run the feedback pipeline on it
3. Let the agent decide what to revise

```python
from rachmaniclaude.compose.feedback import run_feedback_loop

result = run_feedback_loop(
    musicxml_path="path/to/score.musicxml",
    output_dir="output",
    profile_path="models/feature_profile_v3.joblib",
    quality_threshold=0.5,
    max_iterations=1,
)
print(result["critique_text"])  # Ranked suggestions for improvement
```

Works with Claude Code, OpenAI Codex, Cursor, or anything that can write Python + music21.

## Edit in MuseScore

Every `.musicxml` file opens in [MuseScore](https://musescore.org) — see the full score, fix notes by hand, add expression, re-export to MP3/PDF. Use Rachmaniclaude for the first draft, polish in MuseScore.

```bash
musescore3 output/score.musicxml
```

## Examples

### "The Wager" — Cello + Piano

*A chess game between old friends in a park — the stakes are a bottle of wine.*

- Score: [`examples/the_wager.musicxml`](examples/the_wager.musicxml) | Audio: [`examples/the_wager.mp3`](examples/the_wager.mp3)

### "Piano Waltz" — Solo Piano

*The piece that proved the feedback loop works — from experiment 005's blind A/B/C test.*

- Score: [`examples/piano_waltz.musicxml`](examples/piano_waltz.musicxml) | Audio: [`examples/piano_waltz.mp3`](examples/piano_waltz.mp3)

### "Matin de Boulangerie" — Clarinet + Piano

*First love at 17, summer in a French village, working at a bakery. An example of the clarinet not quite working — the model struggles with wind instrument idiom in a way it doesn't with strings or piano.*

- Score: [`examples/matin_de_boulangerie.musicxml`](examples/matin_de_boulangerie.musicxml) | Audio: [`examples/matin_de_boulangerie.mp3`](examples/matin_de_boulangerie.mp3)

## The Research

11 blind listening experiments over the course of this project:

| Exp | What We Tested | Result |
|-----|---------------|--------|
| 001-004 | Feature extraction + classifier training | 60.2% accuracy, dynamics_count is #1 predictor |
| 005 | Blind A/B/C: profile vs XGBoost vs baseline | **Profile feedback wins** over both alternatives |
| 006 | Canonical MusicXML corpus (2,871 pieces) | v3 profile built, 900% more hairpins than PDMX |
| 007 | Canonical feature targets | **REJECTED** — "clownhouse" music. The competence ceiling. |
| 008 | Canonical principles in prompt | **REJECTED** — "listening to nothing." Same problem. |
| 009 | Minimal prompting, 2x2 design | Minimal prompting works. Clarinet is weak. |
| 010 | Cello+piano, chess game vibe | **Best result.** v3 profile wins. |
| 011 | JRPG theme, free instrumentation | Full orchestra fails. 2 parts >> 6+ parts. |

**The central finding:** the less you constrain the LLM, the better it composes.

**An honest caveat about the features:** the top predictors (dynamics count, hairpins, articulation variety) are confounded — better composers naturally use more of these markings, so the features correlate with quality but don't necessarily *cause* it. Telling the LLM "add more hairpins" works to some degree because it forces the model to think about expression, but it's not the same as genuine musical intent. The profile is a useful proxy, not ground truth.

Read the [full report](report/musiclaude.md) for the complete story.

## Retraining Models (Optional)

The shipped models work out of the box. If you want to retrain on your own data:

```bash
# Download PDMX from https://zenodo.org/records/14648209
# Place PDMX.csv in data/, extract mxl.tar.gz into data/
musiclaude-extract --data-dir data/ --output features.csv
musiclaude-train --features features.csv --output models/
```

To rebuild the canonical profile from source corpora, see `codex/experiments/006-canonical-corpus-pipeline.md`.

## Project Structure

```
musiclaude/
  features/         Feature extraction from MusicXML (42+ features)
  classifier/        Quality models (profile, XGBoost, Isolation Forest)
  validator/         Music theory structural validation
  compose/           Feedback loop infrastructure
  render.py          Audio rendering via MuseScore

models/              Pre-trained models (included)
examples/            Best compositions with audio
experiment/          Blind listening experiments (005-011)
codex/               Decision log, experiment writeups
report/              Full research report with plots
analysis/            Exploration scripts, Streamlit dashboard
scripts/             Canonical corpus extraction and analysis
```

## Running Tests

```bash
pytest  # 40 tests
```

## Citation

```
Rachmaniclaude: LLM Music Composition with Feature Profile Feedback
https://github.com/Eirawen/musiclaude
```

## License

MIT
