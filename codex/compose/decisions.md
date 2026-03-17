# Composition Decisions

## CP1: Scratchpad as compositional memory

**What:** `/compose` writes planning notes and iteration history to `output/scratchpad.md` before and after generating MusicXML.

**Why:** MusicXML generation benefits from planning (harmonic skeleton → melody → orchestration). The scratchpad persists between iterations so revision context isn't lost. It also serves as a debugging aid — if a generated score has issues, the scratchpad shows what the model was trying to do.

---

## CP2: Song contract includes quality targets

**What:** The contract specifies minimum chord_vocabulary_size, target melodic_range, required dynamics, etc.

**Why:** These become concrete acceptance criteria for `/assess-quality`. Without them, "good enough" is undefined. The targets bridge the gap between subjective musical intent and objective feature thresholds.

---

## CP4: Canonical compositional wisdom in compose prompt (teacher, not grader)

**What:** The `/compose` skill prompt includes 9 compositional principles extracted from statistical analysis of 198 richly annotated canonical masterworks (Bach, Beethoven, Mozart, Schubert, Chopin). These teach the LLM HOW to write expressively before it writes any music.

**Why:** Experiment 007 showed that using canonical data as post-hoc feature targets (grading) fails — the LLM hits the numbers but produces incoherent music. The canonical data is more valuable as pre-composition guidance (teaching). Key principles: dynamics mark phrase boundaries (53%), staccatos cluster in passages (88%), accents fall on weak beats (67%), dynamic arcs are usually flat not building (55%), loudest moment in first quarter (median 26%).

**Source:** `scripts/analyze_canonical_patterns.py` analyzed 198 pieces with dynamics>=10 and hairpins>=5 from the 2,871 canonical corpus. The scratchpad template also now includes an "Expression Plan" section requiring the composer to plan how to apply these principles.

---

## CP3: Max 5 revision iterations

**What:** The feedback loop caps at 5 iterations before accepting the current version.

**Why:** Diminishing returns. If 5 rounds of targeted feedback haven't fixed the issues, further iteration likely won't help — the problem is probably structural (wrong approach, not wrong details). Also prevents infinite loops.
