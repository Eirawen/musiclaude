# Composition Decisions

## CP1: Scratchpad as compositional memory

**What:** `/compose` writes planning notes and iteration history to `output/scratchpad.md` before and after generating MusicXML.

**Why:** MusicXML generation benefits from planning (harmonic skeleton → melody → orchestration). The scratchpad persists between iterations so revision context isn't lost. It also serves as a debugging aid — if a generated score has issues, the scratchpad shows what the model was trying to do.

---

## CP2: Song contract includes quality targets

**What:** The contract specifies minimum chord_vocabulary_size, target melodic_range, required dynamics, etc.

**Why:** These become concrete acceptance criteria for `/assess-quality`. Without them, "good enough" is undefined. The targets bridge the gap between subjective musical intent and objective feature thresholds.

---

## CP3: Max 5 revision iterations

**What:** The feedback loop caps at 5 iterations before accepting the current version.

**Why:** Diminishing returns. If 5 rounds of targeted feedback haven't fixed the issues, further iteration likely won't help — the problem is probably structural (wrong approach, not wrong details). Also prevents infinite loops.
