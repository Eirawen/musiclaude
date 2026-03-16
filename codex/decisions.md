# Architectural Decisions

## D1: MusicXML over MIDI as the generation format

**Decision:** Claude generates MusicXML, not MIDI or ABC notation.

**Why:** MusicXML preserves full symbolic structure — key signatures, time signatures, dynamics, instrument assignments, articulations, rehearsal marks. MIDI loses most of this. ABC is simpler but can't represent multi-part orchestration well. MusicXML also means we can validate music theory properties (voice leading, parallel fifths) that are invisible in MIDI.

**Trade-off:** MusicXML is verbose (~10x more tokens than equivalent MIDI or ABC). Generation cost is higher. But the richer representation enables the entire classifier feedback loop.

---

## D2: Two-signal quality assessment (XGBoost + Isolation Forest)

**Decision:** Quality assessment combines supervised rating prediction AND unsupervised anomaly detection.

**Why:** We're training on PDMX (human-composed music rated by humans) but applying to LLM-generated music. Distribution shift is the core risk. XGBoost might learn "longer pieces with more instruments get higher ratings" — useful but doesn't catch LLM failure modes (no rests, random-walk melody, rhythmic monotony). The Isolation Forest catches "this doesn't look like music a human would write" regardless of rating prediction accuracy.

**Implication:** A composition must pass BOTH signals. This is intentionally conservative — false negatives (rejecting decent music) are cheaper than false positives (accepting bad music and breaking the feedback loop).

---

## D3: Coherence features targeting LLM failure modes

**Decision:** Added 8 features specifically designed to catch what LLMs get wrong: note_density, rest_ratio, pitch_class_entropy, interval_entropy, melodic_autocorrelation, phrase_length_regularity, strong_beat_consonance, rhythmic_independence.

**Why:** Standard music features (chord vocabulary, key stability) describe what's IN the music. Coherence features describe whether the music has STRUCTURE — motifs, phrases, breathing room, part independence. LLMs can produce technically valid MusicXML that has none of these.

---

## D4: Parallel feature extraction, GPU for XGBoost

**Decision:** Feature extraction uses multiprocessing (CPU-bound, music21 parsing). XGBoost training uses CUDA GPU auto-detection.

**Why:** 250K PDMX files × ~1s per file = ~70 hours single-threaded. Parallelism across CPU cores cuts this to ~8-12 hours. XGBoost on GPU is a modest win for 32 features (minutes not hours) but free performance.

---

## D5: Claude Code skills as the composition interface

**Decision:** Three skills (`/song-contract`, `/compose`, `/assess-quality`) rather than a single monolithic pipeline.

**Why:** Each step benefits from human-in-the-loop. The user reviews the contract before composition starts. The user hears the result before requesting quality assessment. The user decides whether to iterate. A fully automated pipeline would hide bad intermediate results.

---

## D6: MuseScore 3 for audio rendering (not MuseScore 4)

**Decision:** Use `musescore3` CLI in WSL for audio export.

**Why:** MuseScore 4's CLI audio export has been broken since 4.1.1 (produces silent files). MuseScore 3's CLI works reliably for mp3/wav/midi/pdf export. MuseScore 4 can still be used on Windows for viewing scores in the GUI.
