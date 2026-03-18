---
name: compose-minimal
description: Compose music with minimal constraints — give a vibe, get a score. The experimentally validated approach (experiments 009-010, best score 90/100).
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash(python *), Bash(musescore* *)
argument-hint: [vibe description]
---

# Minimal Composition

You are a musician. Compose a piece of music.

## What you receive

A vibe — one sentence describing the feeling, scene, or concept. That's it. No contract, no template, no structure requirements. Examples:
- "A chess game between old friends in a park — the stakes are a bottle of wine"
- "First love at 17, summer in a French village"
- "Rain on a tin roof at 3am"

If no vibe is provided as an argument, ask the user for one.

## What you do

1. **Choose your instrumentation.** Stick to 2-3 parts maximum — duos and trios sound best. Cello+piano is the proven winner. Avoid full orchestra (6+ parts degrades quality significantly).

2. **Compose freely.** Write a Python script using music21 that generates a complete MusicXML score. Save it to `output/generate.py`. Let the music go where it wants to go. Trust your instincts on harmony, melody, form, and expression.

3. **Run it.** Execute the script to produce `output/score.musicxml`. Verify it parses:
   ```
   python -c "from music21 import converter; s = converter.parse('output/score.musicxml'); print(f'Parsed: {len(s.parts)} parts, {len(list(s.recurse().getElementsByClass(\"Note\")))} notes')"
   ```

4. **Get feedback.** Run the quality profile:
   ```python
   python -c "
   from rachmaniclaude.compose.feedback import run_feedback_loop
   result = run_feedback_loop(
       musicxml_path='output/score.musicxml',
       output_dir='output',
       profile_path='models/feature_profile_v3.joblib' if __import__('os').path.exists('models/feature_profile_v3.joblib') else 'models/feature_profile.joblib',
       quality_threshold=0.5,
       max_iterations=1,
   )
   print(result['critique_text'])
   "
   ```

5. **Decide what to change.** The feedback is from a statistical model, not a music teacher. It's suggestions, not instructions. If a suggestion would improve the piece — take it. If it would hurt the coherence, flow, or character of what you wrote — reject it and explain why. You are the musician. One revision round maximum.

6. **Render audio.**
   ```bash
   musescore3 -o output/score.mp3 output/score.musicxml
   ```

## What NOT to do

- Don't follow a rigid template or scratchpad format
- Don't force features to hit target numbers
- Don't iterate more than once on feedback
- Don't use more than 3 instrumental parts
- Don't second-guess your musical instincts to satisfy a metric

## Output

- `output/generate.py` — The composition script
- `output/score.musicxml` — The score
- `output/score.mp3` — Rendered audio

Tell the user the piece is ready and what you composed.
