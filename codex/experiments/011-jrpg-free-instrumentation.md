# 011: JRPG Theme, Free Instrumentation

**Date:** 2026-03-17
**Status:** Complete
**Result:** All scores down (60-73, avg 67.8). Full orchestral writing is beyond LLM capability.

## Question

Does a different vibe (JRPG main menu theme) with free instrumentation choice produce
good results? What instruments does the LLM choose?

## Answer

**No.** All four agents independently chose full orchestra (6-9 parts), and all four
produced bad music. The LLM knows JRPG orchestral vocabulary from text descriptions
(harp arpeggios, horn themes) but can't manage vertical relationships between 6-9
simultaneous voices. "No sound pyramid," "everything at once in the same pitch."

**Instrumentation ceiling hierarchy:** cello+piano (avg 87) > clarinet+piano (71) > orchestra (68).

The vibe triggered orchestral associations the LLM can't execute. The best track (73)
was the simplest: "simple, happy chords that are canonical." Simplicity wins, again.

See `experiment/011/RESULTS.md` for full verbatim feedback.
