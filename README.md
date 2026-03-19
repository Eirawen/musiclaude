# Rachmaniclaude

Language model music composition and quality assessment. Claude composes MusicXML, a feature profile trained on 250K+ human-rated scores and 2,871 canonical masterworks provides feedback, and the results are rendered to audio via MuseScore.

See the [Full report](report/rachmaniclaude.md).

## Examples on Soundcloud (also in this repository)
[Claude's Chess Wager](https://soundcloud.com/khaled-messai-665379541/claudes-the_wager?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing&si=b7ba9e9fdb9a4c5ab34bb5da8f694c91)

[Claude's Piano Waltz](https://soundcloud.com/khaled-messai-665379541/claudes-piano_waltz?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing&si=9659beb362f2436da33da3dc205ccbfc) 

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

```
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
- **Feedback as suggestions, not mandates** — the agent must be free to reject feedback, and when it does, the music is better for it
- **One revision round** — more iterations degrade quality.
- **Less constraint = better music** — rigid pipelines, contracts, and mandatory targets all make things worse

### How It Thinks About Music

These are the unedited revision notes from [one of the agents](experiment/010/track_03/notes.md) — what it chose to accept and reject from the quality profile feedback:

What it accepted:

```
Hairpin count (0 -> 5): Added crescendo and diminuendo hairpins in the cello
(mm. 10, 29, 39) and piano (mm. 29-30). These genuinely improve the phrasing —
the crescendo into the gambit's peak and the diminuendo into the endgame's
reflection are more expressive now.

Range utilization (0.264 -> 0.305): Extended the cello down to C2 (open string,
m. 41) and up to A5 (stratosphere, m. 30 — the peak of the gambit). Extended
piano RH up to A5/G5 in the endgame climax (m. 37), and piano LH down to D1
for the final note (m. 50). These extensions are dramatic moments that earn
the extreme registers.

Groove consistency (partial): Regularized the piano LH in Section A to a
consistent bass-fifth-octave waltz pattern, and Section B to a consistent
staccato bass-fifth-rest pattern. This makes the piano's role as "the board"
more stable — the consistency lets the cello's expressive freedom stand out
against it.
```

What it rejected:

```
Modulation count (5 vs target 10): The piece has clear key areas — D minor,
F major tonicization, Bb major gambit, return to D minor, Picardy to D major.
Ten modulations in 50 measures would make it frantic. The chess game is focused
and deliberate, not a tour of key signatures.

Phrase length regularity (0.753 vs target 0.992): The sections are
12+12+8+12+6 measures. The 8-bar gambit is intentionally short — it's a
surprise move, quick and decisive. The 6-bar coda is a handshake — warm,
brief, final. Forcing 4/8-bar regularity would kill the narrative pacing.

Groove consistency (remaining gap, 0.784 vs 0.839): The cello is a singing
melodic voice — its rhythmic variety is the whole point. The model wants all
parts to have regular rhythmic patterns, but that would turn the cello into
an accompaniment instrument. The piano provides the rhythmic backbone; the
cello provides the soul.
```

[Listen to the result.](examples/010-chess-cello/track_03.mp3)

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

Highlights up top, then everything from every experiment — good and bad. All files are MusicXML + MP3.

### Highlights

| Piece | Instrumentation | Vibe |
|-------|----------------|------|
| [The Wager](examples/the_wager.mp3) ([score](examples/the_wager.musicxml)) | Cello + Piano | A chess game between old friends in a park |
| [Piano Waltz](examples/piano_waltz.mp3) ([score](examples/piano_waltz.musicxml)) | Solo Piano | The piece that proved the feedback loop works |
| [Matin de Boulangerie](examples/matin_de_boulangerie.mp3) ([score](examples/matin_de_boulangerie.musicxml)) | Clarinet + Piano | First love at 17, summer bakery — the clarinet doesn't quite work |

### Everything Else

All compositions from all experiments, including the bad ones. Download and listen — form your own opinions.

**[005 — Blind A/B/C](examples/005-blind-abc/)**: 3 songs × 3 conditions (baseline, profile feedback, XGBoost feedback). Solo piano prelude, piano waltz, violin+piano duet. The experiment that validated profile feedback.

**[007 — Canonical Targets](examples/007-canonical-targets/)**: 4 tracks. Clarinet + piano, targeting Beethoven-level feature counts. The "clownhouse" experiment — numerically correct, musically empty. [Listen to the clownhouse track.](examples/007-canonical-targets/track_04.mp3)

**[008 — Canonical Principles](examples/008-canonical-principles/)**: 2 tracks. Same bakery vibe, with compositional wisdom injected into the prompt. Also bad.

**[009 — Minimal Prompting, Clarinet](examples/009-minimal-clarinet/)**: 4 tracks. Clarinet + piano, one-sentence vibe, 2×2 design. The music improved dramatically but the clarinet writing is rough.

**[010 — Chess Game, Cello](examples/010-chess-cello/)**: 4 tracks. Cello + piano, same minimal approach. The best experiment — switching to cello made all the difference.

**[011 — JRPG Orchestra](examples/011-jrpg-orchestra/)**: 4 tracks. Full orchestra (6-9 parts), Final Fantasy main menu theme. The orchestration ceiling — every agent independently chose full orchestra and every result was bad.

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

Read the [full report](report/rachmaniclaude.md) for the complete story.

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
