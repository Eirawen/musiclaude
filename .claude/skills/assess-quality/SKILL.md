---
name: assess-quality
description: Run the quality classifier on a generated MusicXML score and provide feedback for revision. Use after /compose to evaluate and iteratively improve compositions.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash(python *)
argument-hint: [score-path]
---

# Quality Assessment & Feedback Loop

You assess a generated MusicXML composition using the trained quality classifier and structural validator, then provide actionable feedback for improvement.

## Input

- Score path: argument or default `output/score.musicxml`
- Scratchpad: `output/scratchpad.md` (if exists)
- Trained models: `models/quality_classifier.joblib`, `models/quality_regressor.joblib`, and `models/distribution_scorer.joblib` (if available)

## Process

### Step 1: Run Validation Pipeline

```python
python -c "
import json
from musiclaude.compose.feedback import run_feedback_loop

import os
result = run_feedback_loop(
    musicxml_path='SCORE_PATH',
    output_dir='output',
    classifier_path='models/quality_classifier.joblib' if os.path.exists('models/quality_classifier.joblib') else None,
    regressor_path='models/quality_regressor.joblib' if os.path.exists('models/quality_regressor.joblib') else None,
    distribution_scorer_path='models/distribution_scorer.joblib' if os.path.exists('models/distribution_scorer.joblib') else None,
    quality_threshold=0.5,
    max_iterations=5,
)

print('PASSES:', result['passes'])
print('ITERATION:', result['iteration'])
print()
print(result['critique_text'])
"
```

If the classifier models aren't available yet, fall back to structural validation and manual feature inspection:

```python
python -c "
from musiclaude.features.extract import extract_features_from_file
from musiclaude.validator.structural import validate_file
from musiclaude.classifier.predict import QualityPredictor

# Structural validation
result = validate_file('SCORE_PATH')
print(result.summary())

# Feature extraction
features = extract_features_from_file('SCORE_PATH')
if features:
    for k, v in sorted(features.items()):
        if k != 'filepath':
            print(f'  {k}: {v}')
"
```

### Step 2: Analyze Results

Read the output and compare against the song contract's quality targets. Identify:

1. **Structural errors** — Must be fixed (invalid XML, wrong measure durations)
2. **Quality deficiencies** — Below target thresholds from the contract
3. **Distribution anomalies** — Features that deviate from what normal music looks like (no rests, low pitch variety, monotone rhythm, random-walk melody). These are LLM-specific failure modes.
4. **Theory issues** — Parallel fifths/octaves, poor voice leading, range violations
5. **Expression gaps** — Missing dynamics, tempo marks, articulations

### Step 3: Generate Revision Instructions

If the score doesn't pass, create specific, actionable revision instructions. Be precise:

- BAD: "Improve the harmony"
- GOOD: "Measures 8-12 use only I and V chords. Add ii-V-I progressions and a secondary dominant (V/V) in measure 10 to increase harmonic variety from 2 to 5+ chord types."

### Step 4: Update Scratchpad

Append to `output/scratchpad.md`:

```markdown
### Quality Assessment — Iteration [N]
- **Passes**: [yes/no]
- **Predicted rating**: [if available]
- **Key issues**:
  1. [issue + specific fix]
  2. [issue + specific fix]
- **What's working well**: [positive aspects to preserve]
```

### Step 5: Decision

If the score **passes**: Tell the user it meets quality standards. Suggest rendering:
```
musescore4 -o output/score.mp3 output/score.musicxml
```

If the score **doesn't pass** and iterations remain: Present the critique and ask if the user wants to revise. If yes, the revision instructions should be specific enough to feed directly back into `/compose`.

If **max iterations reached**: Present the final assessment and let the user decide whether to accept or continue manually.

## Output

- Updated `output/scratchpad.md` with assessment
- Updated `output/revision_log.jsonl` with iteration data
- Clear summary to the user with next steps
