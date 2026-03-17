# Track 02: Farine et Lavande -- Revision Notes

## Profile feedback (v1, PDMX)

Initial score: 38/42 features at or above high-rated median.
After revision: 39/42. Passes quality threshold.

## What I incorporated

**Chromatic passing tones (scale_consistency, pitch_class_entropy):**
Took this seriously. Added Eb4 chromatic passing tone in clarinet m.19, C#5 upper
neighbor in m.22, G#4 chromatic approach in m.52, Ab4 and F#4 passing tones in m.57,
B-natural and Db5 in the closing section (mm.65-66), F#4 neighbor in m.68. In the
piano, added Ab3 borrowed-minor color in m.18, G#/B chromatic passing in m.54, a
Dbmaj7 Neapolitan chord in m.69, and Dm6 with B-natural (dorian color) in m.52.
Pitch class entropy went from 2.83 (34th percentile) to 2.97 (47th), nearly at median.

**Extended chords (pct_extended_chords):**
Converted several arpeggiated passages to explicit chord blocks so music21 can detect
them as 7th/9th chords: Bbmaj7 and C7 in mm.3-4, Gm7 in m.6, Bbmaj7 in m.8, Fmaj7
in m.17, Gm7 in m.19, Fmaj7 in m.45, Bbmaj7 in m.46. Improved from 35th to 38th
percentile (0.385 to 0.419).

**Melodic range:**
Pushed clarinet peak from A5 to Bb5 at the climax (m.45). Dropped piano bass to
Bb1 in the closing section (m.62, m.70) and Db2/C2 in the Neapolitan passage
(mm.69-71). This fixed the melodic range flag entirely -- no longer in priority list.

**Piano voice leading:**
Added bridge notes to the rocking accompaniment pattern so the leaps from bass to
treble are broken into two smaller intervals. Reduced leaps from 24 to 18.

## What I rejected

**More chromaticism beyond what I added:** The model still flags scale_consistency
at the 71st percentile ("add more chromatic passing tones"). I reject further changes
here. This is a piece about first love in a French village bakery -- the diatonic
warmth of F major is essential to the character. The chromatic moments I added (the
Eb blue note, the Neapolitan Db, the dorian B-natural) are surgical and emotionally
motivated. Adding more would make it sound like a conservatory exercise rather than
a memory of summer.

**Pushing pct_extended_chords to median:** The model wants 53.5% extended chords;
I'm at 41.9%. Many of my arpeggiated passages (the rocking figures, the waltz
patterns) imply 7th-chord harmony through their note content but are not detected
as chords by music21. The harmonic language is already rich with maj7, m7, m9, 9th,
and Neapolitan chords. Forcing more block chords would change the texture from
gentle arpeggiation to something heavier -- wrong for the mood.

**Piano leaps:** 18 remaining leaps are normal for a piano part that spans bass
and treble registers. This is idiomatic piano writing, not a problem.
