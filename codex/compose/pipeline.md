# Composition Pipeline

## Workflow

```
User → /song-contract → song_contract.md
                              ↓
       /compose → output/score.musicxml + output/scratchpad.md
                              ↓
       /assess-quality → validation + feature extraction + quality assessment
                              ↓
                    ┌─── passes? ───┐
                    │               │
                   YES              NO
                    │               │
              render audio    format critique → /compose (revision)
              musescore3          ↓
                           loop (max 5 iterations)
```

## Skill Responsibilities

### `/song-contract`
- Conversational: asks about genre, mood, instrumentation, structure, tempo, key, etc.
- Outputs `song_contract.md` with quality targets (min chord vocab, target melodic range, etc.)
- These targets become the acceptance criteria for `/assess-quality`

### `/compose`
- Reads `song_contract.md` and optionally `output/scratchpad.md` (prior iteration context)
- Plans before writing: harmonic skeleton, melodic sketch, orchestration notes → scratchpad
- Generates valid MusicXML (divisions=4, proper attributes, complete measures)
- Self-validates with music21 parse check
- Outputs `output/score.musicxml` and updates `output/scratchpad.md`

### `/assess-quality`
- Runs the full validation pipeline: structural → features → XGBoost → distribution scorer
- Formats results into actionable critique with specific measures/features to fix
- Logs each iteration to `output/revision_log.jsonl`
- Decides: pass (render audio) or fail (provide revision instructions for another `/compose` cycle)

## Feedback Loop Mechanics

The feedback is designed to be **specific and actionable**, not vague:

- BAD: "Improve the harmony"
- GOOD: "chord_vocabulary_size=3, normal range is 6-15. Measures 5-12 only use I and V. Add ii, vi, or IV chords."

Each critique maps to a feature the classifier measured, with the current value and the normal range from the distribution scorer. Claude can directly address each point in the next revision.

## Output Files

| File | Purpose |
|------|---------|
| `song_contract.md` | User's musical specification |
| `output/score.musicxml` | Current version of the composition |
| `output/scratchpad.md` | Composition notes, plans, iteration log |
| `output/revision_log.jsonl` | Machine-readable log of all iterations with scores and critiques |
