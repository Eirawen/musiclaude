# Feature Extraction Gotchas

## music21 `activeSite.offset` for absolute positioning

When getting a note's absolute offset in the score, you need `note.offset + note.activeSite.offset` (measure-relative + measure offset). Just `note.offset` gives you the offset within the measure, not the score.

## `score.chordify()` can be slow on large scores

Chordification collapses all parts into a single chord stream. On scores with 10+ parts and 200+ measures, this can take several seconds. It's called once and reused across all harmonic features.

## `chord.commonName` can return surprising values

music21's `commonName` for chords with unusual voicings may return things like "incomplete major-seventh chord" or "enharmonic equivalent of...". The chord vocabulary size counts these as distinct types, which may inflate the count.

## `score.analyze('key')` sometimes returns wrong key

Krumhansl-Schmuckler is a statistical method. Short pieces or pieces with lots of accidentals may get the wrong key. This cascades to `key_stability` (will be low even if the piece is coherent) and `cadence_count` (roman numerals will be wrong).

## Empty measures and pickup measures

Pickup (anacrusis) measures have fewer beats than the time signature specifies. The validator allows measures shorter than expected but flags those longer. Feature extraction treats them normally.

## `Rest` objects don't always appear explicitly

Some MusicXML files use `<forward>` elements instead of explicit rests. music21 sometimes converts these to rests and sometimes doesn't. `rest_ratio` may undercount in such cases.
