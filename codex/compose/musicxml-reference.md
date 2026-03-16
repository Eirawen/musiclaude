# MusicXML Quick Reference

## Duration Math (divisions=4)

With `<divisions>4</divisions>`, one quarter note = 4 duration units.

| Duration | Units | Type | Dotted |
|----------|-------|------|--------|
| Whole | 16 | `whole` | 24 |
| Half | 8 | `half` | 12 |
| Quarter | 4 | `quarter` | 6 |
| Eighth | 2 | `eighth` | 3 |
| 16th | 1 | `sixteenth` | — |

**Measure duration check:** In 4/4, each measure = 16 units. In 3/4 = 12 units. In 6/8 = 12 units.

## Minimal Valid Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN"
  "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
  <part-list>
    <score-part id="P1"><part-name>Piano</part-name></score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>4</divisions>
        <key><fifths>0</fifths></key>
        <time><beats>4</beats><beat-type>4</beat-type></time>
        <clef><sign>G</sign><line>2</line></clef>
      </attributes>
      <!-- notes here, durations must sum to 16 -->
    </measure>
  </part>
</score-partwise>
```

## Common Patterns

### Note
```xml
<note>
  <pitch><step>C</step><octave>4</octave></pitch>
  <duration>4</duration>
  <type>quarter</type>
</note>
```

### Sharp/Flat
```xml
<pitch><step>F</step><alter>1</alter><octave>4</octave></pitch>  <!-- F# -->
<pitch><step>B</step><alter>-1</alter><octave>4</octave></pitch> <!-- Bb -->
```

### Rest
```xml
<rest/><duration>4</duration><type>quarter</type>
```

### Dotted Note
```xml
<note>
  <pitch><step>D</step><octave>5</octave></pitch>
  <duration>12</duration>
  <type>half</type>
  <dot/>
</note>
```

### Chord (notes sharing same beat)
```xml
<note>
  <pitch><step>C</step><octave>4</octave></pitch>
  <duration>4</duration><type>quarter</type>
</note>
<note>
  <chord/>  <!-- this note is part of a chord with the previous note -->
  <pitch><step>E</step><octave>4</octave></pitch>
  <duration>4</duration><type>quarter</type>
</note>
```

### Dynamics
```xml
<direction placement="below">
  <direction-type><dynamics><mf/></dynamics></direction-type>
  <sound dynamics="80"/>
</direction>
```

### Tempo
```xml
<direction placement="above">
  <direction-type>
    <metronome>
      <beat-unit>quarter</beat-unit>
      <per-minute>120</per-minute>
    </metronome>
  </direction-type>
  <sound tempo="120"/>
</direction>
```

### Key Signatures (fifths)
| Key | Fifths |
|-----|--------|
| C major / A minor | 0 |
| G major / E minor | 1 |
| D major / B minor | 2 |
| F major / D minor | -1 |
| Bb major / G minor | -2 |

### MIDI Program Numbers (common instruments)
| Instrument | Program |
|-----------|---------|
| Piano | 1 |
| Harpsichord | 7 |
| Flute | 74 |
| Oboe | 69 |
| Clarinet | 72 |
| Violin | 41 |
| Viola | 42 |
| Cello | 43 |
| Trumpet | 57 |
| French Horn | 61 |
| Harp | 47 |
