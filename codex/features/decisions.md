# Feature Engineering Decisions

## F1: Cadence detection uses all consecutive chord pairs, not just phrase endings

**What:** Ideally cadences are detected at phrase boundaries. We approximate by scanning all consecutive roman numeral pairs.

**Why:** Reliable phrase boundary detection in arbitrary MusicXML is hard (no standard markup). Scanning all pairs overcounts but still provides a useful relative signal — scores with more V→I patterns do have more cadential structure.

**Risk:** Inflated cadence counts. If this proves noisy, could filter to only check pairs at measure boundaries divisible by 4 or 8.

---

## F2: Modulation detection uses 4-measure windows with Krumhansl-Schmuckler

**What:** The score is windowed into 4-measure chunks. Each chunk's key is analyzed. A change in detected key = a modulation.

**Why:** Global key detection misses modulations. Windowed analysis catches them. 4 measures is standard phrase length, small enough to detect short modulations but big enough to avoid noise.

**Risk:** Short pieces (< 8 measures) get 0 modulations by default. Brief tonicizations within a phrase may be missed or over-counted.

---

## F3: Repetition density compares pitch sequences, ignoring rhythm

**What:** Two measures are "repeats" if they have the same sequence of MIDI pitches regardless of rhythm.

**Why:** Catches melodic repetition which is the most audible form. Including rhythm would miss "same melody, different rhythm" variations which are musically equivalent.

---

## F4: Melodic autocorrelation uses lag = notes-per-measure

**What:** We compute autocorrelation at a lag of approximately one measure's worth of notes.

**Why:** Musical structure repeats at the measure level (motifs, sequences). A lag of 1 beat would be too short; a lag of 4 measures too long for detecting motifs. Measure-level is the sweet spot.

---

## F5: Strong beat consonance checks all pairs of sounding notes

**What:** At each strong beat position, we collect all sounding pitches across all parts and check if every pair forms a consonant interval.

**Why:** A single dissonant pair on a strong beat is noticeable. This is stricter than "majority consonant" but matches music theory practice where accidental dissonance on downbeats is considered an error.
