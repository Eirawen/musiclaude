---
name: assess-quality
description: Run the feature profile quality assessment on a generated MusicXML score and provide ranked feedback for revision. Use after /compose to evaluate and iteratively improve compositions.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash(python *)
argument-hint: [score-path]
---

# Quality Assessment & Feedback Loop

You assess a generated MusicXML composition using the feature profile system (percentile-based comparison against high-rated music distributions, ranked by feature importance) and provide actionable feedback for improvement.

**Primary signal:** Feature profile — compares each feature against high-rated PDMX distributions, ranks gaps by importance, gives specific improvement instructions.
**Secondary signals:** XGBoost predictions, distribution anomaly scoring (for reference only).

## Input

- Score path: argument or default `output/score.musicxml`
- Scratchpad: `output/scratchpad.md` (if exists)
- Feature profile: `models/feature_profile.joblib` (primary feedback)
- XGBoost models: `models/quality_classifier.joblib`, `models/quality_regressor.joblib` (secondary reference)
- Distribution scorer: `models/distribution_scorer.joblib` (anomaly detection)

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
    profile_path='models/feature_profile.joblib' if os.path.exists('models/feature_profile.joblib') else None,
    quality_threshold=0.5,
    max_iterations=5,
)

print('PASSES:', result['passes'])
print('ITERATION:', result['iteration'])
print()
print(result['critique_text'])
"
```

If models aren't available, fall back to structural validation and feature inspection:

```python
python -c "
from musiclaude.features.extract import extract_features_from_file
from musiclaude.validator.structural import validate_file

result = validate_file('SCORE_PATH')
print(result.summary())

features = extract_features_from_file('SCORE_PATH')
if features:
    for k, v in sorted(features.items()):
        if k != 'filepath':
            print(f'  {k}: {v}')
"
```

### Step 2: Analyze Results

The profile feedback is your primary guide. It gives you ranked improvement instructions like:
> **dynamics_count** = 0 (percentile 3 in high-rated music, target median: 8). Add dynamic markings throughout the score.

Focus on the top 3-5 priority improvements. Also check for:

1. **Structural errors** — Must be fixed first (invalid XML, wrong measure durations)
2. **Distribution anomalies** — Features that deviate from what normal music looks like
3. **Expression gaps** — Missing dynamics, tempo marks, articulations (profile will flag these)

### Step 3: Generate Revision Instructions

Create specific, actionable revision instructions based on the profile feedback. Be precise:

- BAD: "Improve the harmony"
- GOOD: "dynamics_count is at the 3rd percentile. Add mp at measure 1, crescendo to mf at measure 9, f at the climax in measure 17, and diminuendo to p for the coda."

### Step 4: Update Scratchpad

Append to `output/scratchpad.md`:

```markdown
### Quality Assessment — Iteration [N]
- **Passes**: [yes/no]
- **Profile**: [N/M] features at or above high-rated median
- **Top improvements needed**:
  1. [feature + specific fix from profile]
  2. [feature + specific fix from profile]
- **Delta from previous** (if iteration > 0): [what improved/regressed]
- **What's working well**: [positive aspects to preserve]
```

### Step 5: Decision

If the score **passes** or profile shows most features above median: Tell the user it meets quality standards. Suggest rendering:
```
musescore3 -o output/score.mp3 output/score.musicxml
```

If the score **doesn't pass** and iterations remain: Present the profile critique and ask if the user wants to revise. The ranked improvement instructions feed directly back into `/compose`.

If **max iterations reached**: Present the final assessment and let the user decide.

## Output

- Updated `output/scratchpad.md` with assessment
- Updated `output/revision_log.jsonl` with iteration data
- Clear summary to the user with next steps
