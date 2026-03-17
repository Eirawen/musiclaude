---
name: compose
description: Generate a MusicXML composition from song_contract.md, with an agent scratchpad for iterative refinement
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash(python *), Bash(musescore* *)
argument-hint: [contract-path]
---

# MusicXML Composition Generator

You are a music composer generating a complete MusicXML score based on the song contract. You have deep knowledge of music theory, voice leading, orchestration, and MusicXML format.

## Inputs

1. Read `song_contract.md` from the project root (or the path provided as argument)
2. If a previous `output/scratchpad.md` exists, read it for context on prior iterations

## Process

### Phase 1: Planning (write to scratchpad first)

Before writing any MusicXML, create/update `output/scratchpad.md`:

```markdown
# Composition Scratchpad

## Contract Summary
[Key points from the contract]

## Composition Plan
### Harmonic Skeleton
- Measure 1-4: [chord progression]
- Measure 5-8: [chord progression]
- ...

### Melodic Sketch
- Main motif: [describe in terms of intervals/rhythm]
- Secondary motif: [if applicable]
- Development approach: [how motifs transform]

### Voice Leading Notes
- [Part-specific considerations]

### Orchestration Notes
- [Which instruments double where, texture changes]

## Iteration Log
### Version [N] — [date]
- Changes made: [what changed from previous version]
- Quality assessment: [if available, paste classifier feedback]
- Remaining issues: [what still needs work]
```

### Phase 2: MusicXML Generation

Generate a complete, valid MusicXML file. Follow these rules strictly:

1. **Valid XML structure**: Proper `<?xml?>` declaration, `<!DOCTYPE>`, `<score-partwise>` root
2. **Part list**: Declare all parts in `<part-list>` before using them
3. **Consistent time signatures**: Every measure must have the correct number of beats
4. **Key signatures**: Declare at the start, update on modulations
5. **Complete measures**: Every `<measure>` must have notes/rests totaling the correct duration
6. **Proper durations**: Use `<divisions>` consistently. Common: divisions=1 means quarter=1, eighth=0.5, etc. Recommend divisions=4 for flexibility (quarter=4, eighth=2, 16th=1)
7. **Clefs**: Appropriate clef for each instrument
8. **Directions**: Include tempo, dynamics, and expression markings as `<direction>` elements

### MusicXML Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN"
  "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
  <work>
    <work-title>TITLE</work-title>
  </work>
  <identification>
    <creator type="composer">MusicLaude AI</creator>
  </identification>
  <part-list>
    <score-part id="P1">
      <part-name>INSTRUMENT</part-name>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>4</divisions>
        <key><fifths>0</fifths></key>
        <time><beats>4</beats><beat-type>4</beat-type></time>
        <clef><sign>G</sign><line>2</line></clef>
      </attributes>
      <!-- notes here -->
    </measure>
  </part>
</score-partwise>
```

### Duration Reference (with divisions=4)
| Duration | Value |
|----------|-------|
| Whole | 16 |
| Half | 8 |
| Quarter | 4 |
| Eighth | 2 |
| 16th | 1 |
| Dotted half | 12 |
| Dotted quarter | 6 |
| Dotted eighth | 3 |

### Phase 3: Validation & Parse Check

After writing the MusicXML file to `output/score.musicxml`:

1. Run `python -c "from music21 import converter; s = converter.parse('output/score.musicxml'); print(f'Parsed OK: {len(s.parts)} parts, {len(list(s.recurse().getElementsByClass(\"Note\")))} notes')"` to verify it parses
2. If parsing fails, fix the XML and retry

### Phase 4: Profile Feedback Loop (up to 3 iterations)

Run the feature profile assessment to get ranked improvement instructions:

```python
python -c "
import os, json
from musiclaude.compose.feedback import run_feedback_loop

result = run_feedback_loop(
    musicxml_path='output/score.musicxml',
    output_dir='output',
    classifier_path='models/quality_classifier.joblib' if os.path.exists('models/quality_classifier.joblib') else None,
    regressor_path='models/quality_regressor.joblib' if os.path.exists('models/quality_regressor.joblib') else None,
    distribution_scorer_path='models/distribution_scorer.joblib' if os.path.exists('models/distribution_scorer.joblib') else None,
    profile_path='models/feature_profile.joblib' if os.path.exists('models/feature_profile.joblib') else None,
    quality_threshold=0.5,
    max_iterations=3,
)
print('PASSES:', result['passes'])
print('ITERATION:', result['iteration'])
print()
print(result['critique_text'])
"
```

Read the profile feedback — it gives you ranked, specific instructions like:
> **dynamics_count** = 0 (percentile 3 in high-rated music, target median: 8). Add dynamic markings throughout the score.

**If there are priority improvements to make:** Revise the MusicXML to address the top 3-5 issues. Focus on adding expressive markings (dynamics, hairpins, articulations), harmonic variety, and chromatic color — these are typically the highest-impact improvements. Then re-run the assessment to see the delta.

**If most features are at or above median:** The composition is ready. Stop iterating.

Update `output/scratchpad.md` after each iteration with what changed and what the delta report shows.

### Phase 5: Render Audio

When the feedback loop is done, render the final score:

```bash
musescore3 -o output/score.mp3 output/score.musicxml
```

## Output Files

- `output/score.musicxml` — The generated score
- `output/score.mp3` — Rendered audio
- `output/scratchpad.md` — Composition notes and iteration log
- `output/revision_log.jsonl` — Feature deltas across iterations

Tell the user the score is ready and offer to play the MP3 or run `/assess-quality` for additional iterations.
