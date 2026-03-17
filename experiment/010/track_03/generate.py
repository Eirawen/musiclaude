"""Generate a piece for Cello and Piano.

Vibe: A chess game between old friends in a park — the stakes are a bottle of wine.
Time signature: 3/4 (waltz-like, the genteel rhythm of a park afternoon).
Key: D minor (cerebral, slightly bittersweet, competitive friendship).
Tempo: Moderato — old friends take their time.

Character: The cello and piano trade ideas like chess moves. The cello plays long,
considered melodic lines (the thinker pondering the board). The piano punctuates
with rhythmic, pointed figures (placing pieces with a click). Moments of tension
(a good move), playfulness (friendly banter), and warm resolution (the wine
will be shared regardless).

Structure:
  A  (mm. 1-12)   Opening Game — Main theme: D-C-Bb-A descent, thoughtful gaze
  B  (mm. 13-24)  Middle Game — Tension builds, wider leaps, staccato clicks
  C  (mm. 25-32)  The Gambit — Surprise Bb major, bold ascending cello line
  A' (mm. 33-44)  Endgame — Theme returns richer, augmented, complex harmony
  Coda (mm. 45-50) The Handshake — Convergence, Picardy third to D major

REVISION 1 — Addressing profile feedback (35/42 features at/above median):
  - groove_consistency (0.784 → 0.839): regularize LH waltz pattern within sections
  - avg_range_utilization (0.264 → 0.328): extend cello up to A5, piano LH uses
    deeper bass more consistently
  - phrase_length_regularity (0.753 → 0.992): tighten 4-bar phrase groupings
  - hairpin_count (0 → 1+): add crescendo/diminuendo hairpins
  - expression_count (2 → 4+): add fermatas, trills on sustained notes
  - piano voice leading: smooth largest leaps in LH
  REJECTED:
  - modulation_count (5 → 10): 50-measure piece already has intentional key areas;
    more modulations would make it restless, not contemplative
"""

import os

from music21 import (
    stream, note, chord, meter, key, tempo, clef,
    instrument, dynamics, expressions, articulations,
    duration, pitch, spanner, layout, metadata,
)


def make_note(p, dur, **kwargs):
    """Create a note with pitch string p and quarterLength dur."""
    n = note.Note(p)
    n.duration = duration.Duration(dur)
    for k, v in kwargs.items():
        if k == "staccato":
            n.articulations.append(articulations.Staccato())
        elif k == "accent":
            n.articulations.append(articulations.Accent())
        elif k == "tenuto":
            n.articulations.append(articulations.Tenuto())
        elif k == "fermata":
            n.expressions.append(expressions.Fermata())
        elif k == "trill":
            n.expressions.append(expressions.Trill())
    return n


def make_rest(dur):
    r = note.Rest()
    r.duration = duration.Duration(dur)
    return r


def make_chord(pitches, dur, **kwargs):
    c = chord.Chord(pitches)
    c.duration = duration.Duration(dur)
    for k, v in kwargs.items():
        if k == "staccato":
            c.articulations.append(articulations.Staccato())
        elif k == "accent":
            c.articulations.append(articulations.Accent())
        elif k == "tenuto":
            c.articulations.append(articulations.Tenuto())
    return c


def build_cello_part():
    """Build the Cello part.

    3/4 time: one measure = 3.0 quarter lengths.
    Core motif: D-C-Bb-A (descending minor tetrachord — a pensive gaze at the board).
    Range: C2 to A5 (full cello range).
    Chromaticism: C#, Eb, F#, G#, Ab for tension and color.
    """
    vc = stream.Part()
    vc.insert(0, instrument.Violoncello())
    vc.partName = "Violoncello"

    # ================================================================
    # Section A: Opening Game (mm. 1-12)
    # Both players settle in. Cello states main theme.
    # ================================================================

    # m1: The first move. Cello enters alone with the motif.
    m1 = stream.Measure(number=1)
    m1.insert(0, meter.TimeSignature("3/4"))
    m1.insert(0, key.Key("d", "minor"))
    m1.insert(0, tempo.MetronomeMark("Moderato, con amicizia", 96, duration.Duration(1.0)))
    m1.insert(0, dynamics.Dynamic("mp"))
    m1.append(make_note("D4", 1.5, tenuto=True))   # D — long, deliberate
    m1.append(make_note("C4", 1.0))                 # C
    m1.append(make_note("Bb3", 0.5))                # Bb — the descent begins
    vc.append(m1)

    # m2: Completing the motif, settling on A
    m2 = stream.Measure(number=2)
    m2.append(make_note("A3", 2.0, tenuto=True, fermata=True))  # A — the thought lands
    m2.append(make_rest(1.0))                         # pause — considering the board
    vc.append(m2)

    # m3: Second phrase — motif varied, reaching up
    m3 = stream.Measure(number=3)
    m3.append(make_note("D4", 0.75))
    m3.append(make_note("E4", 0.25))                 # ornamental turn upward
    m3.append(make_note("F4", 1.0))                  # reaching to F
    m3.append(make_note("E4", 0.5))
    m3.append(make_note("D4", 0.5))
    vc.append(m3)

    # m4: Descending again with chromatic neighbor
    m4 = stream.Measure(number=4)
    m4.append(make_note("C#4", 0.5))                 # chromatic — sharpened leading tone
    m4.append(make_note("D4", 1.0))
    m4.append(make_note("Bb3", 1.0))
    m4.append(make_rest(0.5))
    vc.append(m4)

    # m5: Lower register — thinking deeper
    m5 = stream.Measure(number=5)
    m5.insert(0, dynamics.Dynamic("p"))
    m5.append(make_note("A3", 0.75))
    m5.append(make_note("G3", 0.25))
    m5.append(make_note("F3", 1.0, tenuto=True))
    m5.append(make_note("E3", 0.5))
    m5.append(make_rest(0.5))
    vc.append(m5)

    # m6: Motif in low register D3-C3-Bb2-A2
    m6 = stream.Measure(number=6)
    m6.append(make_note("D3", 1.0))
    m6.append(make_note("C3", 0.75))
    m6.append(make_note("Bb2", 0.25))
    m6.append(make_note("A2", 1.0))                  # deep — pondering
    vc.append(m6)

    # m7: Rising from the depths — a new idea forming
    m7 = stream.Measure(number=7)
    m7.insert(0, dynamics.Dynamic("mp"))
    m7.append(make_note("D3", 0.5))
    m7.append(make_note("F3", 0.5))
    m7.append(make_note("A3", 0.5))
    m7.append(make_note("D4", 1.0))
    m7.append(make_rest(0.5))
    vc.append(m7)

    # m8: Answering with a sigh — Eb chromatic color
    m8 = stream.Measure(number=8)
    m8.append(make_note("C4", 0.5))
    m8.append(make_note("Bb3", 0.5))
    m8.append(make_note("A3", 0.5))
    m8.append(make_note("G3", 1.0))
    m8.append(make_rest(0.5))
    vc.append(m8)

    # m9: Motif returns, slightly ornamented — the friend smiles
    m9 = stream.Measure(number=9)
    m9.insert(0, dynamics.Dynamic("mf"))
    m9.append(make_note("D4", 0.5))
    m9.append(make_note("Eb4", 0.25))                # chromatic upper neighbor
    m9.append(make_note("D4", 0.25))
    m9.append(make_note("C4", 0.5))
    m9.append(make_note("Bb3", 0.5))
    m9.append(make_note("A3", 1.0))
    vc.append(m9)

    # m10: A longer phrase, climbing — crescendo through here
    m10 = stream.Measure(number=10)
    cresc1 = dynamics.Crescendo()
    n10a = make_note("Bb3", 0.5)
    m10.append(n10a)
    m10.append(make_note("C4", 0.5))
    m10.append(make_note("D4", 0.5))
    n10d = make_note("F4", 1.0)
    m10.append(n10d)
    m10.append(make_rest(0.5))
    cresc1.addSpannedElements([n10a, n10d])
    vc.insert(0, cresc1)
    vc.append(m10)

    # m11: Pushing higher — excitement at a good position
    m11 = stream.Measure(number=11)
    m11.append(make_note("G4", 0.75))
    m11.append(make_note("F4", 0.25))
    m11.append(make_note("E4", 0.5))
    m11.append(make_note("D4", 0.5))
    m11.append(make_note("C#4", 0.5))                # leading tone
    m11.append(make_rest(0.5))
    vc.append(m11)

    # m12: Half cadence — both players pause, sip imaginary coffee
    m12 = stream.Measure(number=12)
    m12.append(make_note("D4", 2.0, tenuto=True))
    m12.append(make_rest(1.0))
    vc.append(m12)

    # ================================================================
    # Section B: Middle Game (mm. 13-24)
    # Tension builds. Wider leaps, more agitation.
    # ================================================================

    m13 = stream.Measure(number=13)
    m13.insert(0, dynamics.Dynamic("mf"))
    m13.insert(0, expressions.RehearsalMark("B"))
    # Transformed motif — now with wider leaps (the stakes are felt)
    m13.append(make_note("A3", 0.5))
    m13.append(make_note("D4", 0.5))                  # leap up — 4th
    m13.append(make_note("F4", 0.5, accent=True))     # leap to 6th
    m13.append(make_note("E4", 0.5))
    m13.append(make_note("C#4", 0.5))
    vc.append(m13)

    # m14: Driving forward
    m14 = stream.Measure(number=14)
    m14.append(make_note("D4", 0.5))
    m14.append(make_note("G4", 0.5))                  # leap up
    m14.append(make_note("F4", 0.5))
    m14.append(make_note("Eb4", 0.5))                 # chromatic — Neapolitan flavor
    m14.append(make_note("D4", 0.5))
    m14.append(make_rest(0.5))
    vc.append(m14)

    # m15: Rhythmic urgency — sixteenths
    m15 = stream.Measure(number=15)
    m15.append(make_note("A3", 0.25))
    m15.append(make_note("Bb3", 0.25))
    m15.append(make_note("C4", 0.25))
    m15.append(make_note("D4", 0.25))
    m15.append(make_note("E4", 0.5))
    m15.append(make_note("F4", 1.0, accent=True))
    m15.append(make_rest(0.5))
    vc.append(m15)

    # m16: Dropping back — regrouping after a captured piece
    m16 = stream.Measure(number=16)
    m16.append(make_note("E4", 0.5))
    m16.append(make_note("D4", 0.5))
    m16.append(make_note("C4", 0.5))
    m16.append(make_note("A3", 1.0))
    m16.append(make_rest(0.5))
    vc.append(m16)

    # m17-18: Modulating toward F major — the friend who's winning feels bright
    m17 = stream.Measure(number=17)
    m17.insert(0, dynamics.Dynamic("f"))
    m17.append(make_note("F4", 1.0, tenuto=True))
    m17.append(make_note("E4", 0.5))
    m17.append(make_note("F4", 0.5))
    m17.append(make_note("A4", 0.5))                  # reaching high — confidence
    m17.append(make_rest(0.5))
    vc.append(m17)

    m18 = stream.Measure(number=18)
    m18.append(make_note("G4", 0.75))
    m18.append(make_note("A4", 0.25))
    m18.append(make_note("Bb4", 1.0, accent=True))    # Bb — firmly in F major territory
    m18.append(make_note("A4", 0.5))
    m18.append(make_rest(0.5))
    vc.append(m18)

    # m19: Playful exchange — staccato, like banter
    m19 = stream.Measure(number=19)
    m19.append(make_note("C5", 0.5, staccato=True))
    m19.append(make_note("A4", 0.5, staccato=True))
    m19.append(make_note("F4", 0.5, staccato=True))
    m19.append(make_note("C4", 0.5))
    m19.append(make_rest(1.0))
    vc.append(m19)

    # m20: The other friend counters — back toward D minor
    m20 = stream.Measure(number=20)
    m20.insert(0, dynamics.Dynamic("mf"))
    m20.append(make_note("D4", 0.5))
    m20.append(make_note("E4", 0.5))
    m20.append(make_note("F4", 0.5))
    m20.append(make_note("G4", 0.5))
    m20.append(make_note("Ab4", 0.5))                 # chromatic — tension!
    m20.append(make_rest(0.5))
    vc.append(m20)

    # m21: Tension peaks
    m21 = stream.Measure(number=21)
    m21.insert(0, dynamics.Dynamic("f"))
    m21.append(make_note("A4", 1.0, accent=True))
    m21.append(make_note("G#4", 0.25))                # chromatic neighbors
    m21.append(make_note("A4", 0.25))
    m21.append(make_note("F4", 0.5))
    m21.append(make_note("E4", 0.5))
    m21.append(make_rest(0.5))
    vc.append(m21)

    # m22: Descending in frustration — a piece lost
    m22 = stream.Measure(number=22)
    m22.append(make_note("D4", 0.5))
    m22.append(make_note("C4", 0.5))
    m22.append(make_note("Bb3", 0.5))
    m22.append(make_note("A3", 0.5))
    m22.append(make_note("G3", 0.5))
    m22.append(make_rest(0.5))
    vc.append(m22)

    # m23: Sighing figure
    m23 = stream.Measure(number=23)
    m23.insert(0, dynamics.Dynamic("mp"))
    m23.append(make_note("F3", 1.5, tenuto=True))
    m23.append(make_note("E3", 0.5))
    m23.append(make_rest(1.0))
    vc.append(m23)

    # m24: Settling — preparing for the gambit
    m24 = stream.Measure(number=24)
    m24.append(make_note("D3", 1.5))
    m24.append(make_rest(1.5))
    vc.append(m24)

    # ================================================================
    # Section C: The Gambit (mm. 25-32)
    # A surprise move. Bold ascending line in Bb major territory.
    # ================================================================

    m25 = stream.Measure(number=25)
    m25.insert(0, dynamics.Dynamic("f"))
    m25.insert(0, expressions.RehearsalMark("C"))
    # Bold ascending line — the gambit is played!
    m25.append(make_note("Bb2", 0.5, accent=True))
    m25.append(make_note("D3", 0.5))
    m25.append(make_note("F3", 0.5))
    m25.append(make_note("Bb3", 0.5))
    m25.append(make_note("D4", 0.5))
    m25.append(make_rest(0.5))
    vc.append(m25)

    m26 = stream.Measure(number=26)
    m26.append(make_note("F4", 0.5))
    m26.append(make_note("G4", 0.5))
    m26.append(make_note("A4", 1.0, accent=True))     # triumph!
    m26.append(make_note("Bb4", 0.5))
    m26.append(make_rest(0.5))
    vc.append(m26)

    # m27: The opponent reacts — chromatic descent
    m27 = stream.Measure(number=27)
    m27.append(make_note("A4", 0.5))
    m27.append(make_note("Ab4", 0.5))                  # chromatic — shock
    m27.append(make_note("G4", 0.5))
    m27.append(make_note("F#4", 0.5))                  # more chromatic — scrambling
    m27.append(make_note("F4", 0.5))
    m27.append(make_rest(0.5))
    vc.append(m27)

    # m28: Landing on E — dominant of A — where are we going?
    m28 = stream.Measure(number=28)
    m28.append(make_note("E4", 2.0, trill=True))     # trill on suspense note
    m28.append(make_rest(1.0))
    vc.append(m28)

    # m29: Second gambit wave — higher still, pushing range
    m29 = stream.Measure(number=29)
    m29.insert(0, dynamics.Dynamic("ff"))
    cresc2 = dynamics.Crescendo()
    n29a = make_note("D4", 0.5)
    m29.append(n29a)
    m29.append(make_note("F4", 0.5))
    m29.append(make_note("A4", 0.5))
    m29.append(make_note("D5", 0.5, accent=True))
    n29e = make_note("E5", 0.5)
    m29.append(n29e)
    m29.append(make_rest(0.5))
    cresc2.addSpannedElements([n29a, n29e])
    vc.insert(0, cresc2)
    vc.append(m29)

    # m30: The peak — highest note of the piece, reaching A5
    m30 = stream.Measure(number=30)
    m30.append(make_note("A5", 0.5, accent=True))     # A5 — cello stratosphere!
    m30.append(make_note("F5", 0.25))
    m30.append(make_note("E5", 0.25))
    m30.append(make_note("D5", 0.5))
    m30.append(make_note("Bb4", 0.5))
    m30.append(make_note("A4", 0.5))
    vc.append(m30)

    # m31: Calming — the gambit is accepted
    m31 = stream.Measure(number=31)
    m31.insert(0, dynamics.Dynamic("mf"))
    m31.append(make_note("G4", 0.5))
    m31.append(make_note("F4", 0.5))
    m31.append(make_note("E4", 0.5))
    m31.append(make_note("D4", 0.5))
    m31.append(make_note("C#4", 0.5))                  # leading tone — back to D minor
    m31.append(make_rest(0.5))
    vc.append(m31)

    # m32: Transition — breath before the endgame
    m32 = stream.Measure(number=32)
    m32.append(make_note("D4", 1.5))
    m32.append(make_rest(1.5))
    vc.append(m32)

    # ================================================================
    # Section A': Endgame (mm. 33-44)
    # Theme returns, richer and more expansive. Both friends know
    # the game is nearly over.
    # ================================================================

    m33 = stream.Measure(number=33)
    m33.insert(0, dynamics.Dynamic("mf"))
    m33.insert(0, expressions.RehearsalMark("A'"))
    # Augmented motif: D-C-Bb-A now in longer values
    m33.append(make_note("D4", 3.0, tenuto=True))     # whole measure on D
    vc.append(m33)

    m34 = stream.Measure(number=34)
    m34.append(make_note("C4", 2.0))
    m34.append(make_note("Bb3", 1.0))
    vc.append(m34)

    m35 = stream.Measure(number=35)
    m35.append(make_note("A3", 2.5, tenuto=True))
    m35.append(make_rest(0.5))
    vc.append(m35)

    # m36: Ornamented continuation
    m36 = stream.Measure(number=36)
    m36.append(make_note("Bb3", 0.5))
    m36.append(make_note("C4", 0.5))
    m36.append(make_note("D4", 0.75))
    m36.append(make_note("Eb4", 0.25))                 # chromatic color
    m36.append(make_note("D4", 0.5))
    m36.append(make_rest(0.5))
    vc.append(m36)

    # m37: Reaching higher — the game intensifies one last time
    m37 = stream.Measure(number=37)
    m37.insert(0, dynamics.Dynamic("f"))
    m37.append(make_note("F4", 1.0))
    m37.append(make_note("G4", 0.5))
    m37.append(make_note("A4", 1.0, accent=True))
    m37.append(make_rest(0.5))
    vc.append(m37)

    # m38: But then gentling — acceptance
    m38 = stream.Measure(number=38)
    m38.append(make_note("G4", 0.5))
    m38.append(make_note("F4", 0.5))
    m38.append(make_note("E4", 1.0))
    m38.append(make_note("D4", 0.5))
    m38.append(make_rest(0.5))
    vc.append(m38)

    # m39: Low register — reflective, with diminuendo
    m39 = stream.Measure(number=39)
    m39.insert(0, dynamics.Dynamic("mp"))
    dim1 = dynamics.Diminuendo()
    n39a = make_note("A3", 0.75)
    m39.append(n39a)
    m39.append(make_note("G3", 0.25))
    m39.append(make_note("F3", 1.0))
    n39d = make_note("E3", 0.5)
    m39.append(n39d)
    m39.append(make_rest(0.5))
    dim1.addSpannedElements([n39a, n39d])
    vc.insert(0, dim1)
    vc.append(m39)

    # m40: Deep cello — old memories
    m40 = stream.Measure(number=40)
    m40.append(make_note("D3", 1.0))
    m40.append(make_note("C3", 0.5))
    m40.append(make_note("Bb2", 1.0))
    m40.append(make_rest(0.5))
    vc.append(m40)

    # m41: Motif one more time, climbing from the very bottom
    m41 = stream.Measure(number=41)
    m41.insert(0, dynamics.Dynamic("mf"))
    m41.append(make_note("C2", 0.5))                  # open C string — deepest note
    m41.append(make_note("D2", 0.5))
    m41.append(make_note("A2", 0.5))
    m41.append(make_note("D3", 0.5))
    m41.append(make_note("A3", 0.5))
    m41.append(make_note("D4", 0.5))
    vc.append(m41)

    # m42: Last echo of the motif — D-C-Bb-A one final time
    m42 = stream.Measure(number=42)
    m42.append(make_note("D4", 0.75))
    m42.append(make_note("C4", 0.75))
    m42.append(make_note("Bb3", 0.75))
    m42.append(make_note("A3", 0.75))
    vc.append(m42)

    # m43: Settling onto A — dominant pedal
    m43 = stream.Measure(number=43)
    m43.insert(0, dynamics.Dynamic("p"))
    m43.append(make_note("A3", 2.5, tenuto=True))
    m43.append(make_rest(0.5))
    vc.append(m43)

    # m44: Rising to D — resolution approaches
    m44 = stream.Measure(number=44)
    m44.append(make_note("C#4", 0.5))                  # leading tone
    m44.append(make_note("D4", 2.0))
    m44.append(make_rest(0.5))
    vc.append(m44)

    # ================================================================
    # Coda: The Handshake (mm. 45-50)
    # Both instruments converge. D minor → D major (Picardy third).
    # The wine is opened.
    # ================================================================

    m45 = stream.Measure(number=45)
    m45.insert(0, dynamics.Dynamic("p"))
    m45.insert(0, expressions.RehearsalMark("Coda"))
    m45.insert(0, tempo.MetronomeMark("Poco rit.", 80, duration.Duration(1.0)))
    m45.append(make_note("D4", 1.0))
    m45.append(make_note("C4", 0.5))
    m45.append(make_note("Bb3", 1.0))
    m45.append(make_rest(0.5))
    vc.append(m45)

    m46 = stream.Measure(number=46)
    m46.append(make_note("A3", 1.5))
    m46.append(make_note("G3", 0.5))
    m46.append(make_note("F3", 0.5))
    m46.append(make_rest(0.5))
    vc.append(m46)

    # m47: The Picardy begins — F# appears (D major!)
    m47 = stream.Measure(number=47)
    m47.insert(0, dynamics.Dynamic("pp"))
    m47.append(make_note("D3", 1.0))
    m47.append(make_note("F#3", 1.0))                  # F# — the sun breaks through
    m47.append(make_note("A3", 0.5))
    m47.append(make_rest(0.5))
    vc.append(m47)

    # m48: D major warmth
    m48 = stream.Measure(number=48)
    m48.append(make_note("D4", 1.5, tenuto=True))
    m48.append(make_note("A3", 1.0))
    m48.append(make_rest(0.5))
    vc.append(m48)

    # m49: Final descent, now major — D-C#-B-A (not Bb!)
    m49 = stream.Measure(number=49)
    m49.append(make_note("D4", 0.75))
    m49.append(make_note("C#4", 0.75))
    m49.append(make_note("B3", 0.75))
    m49.append(make_note("A3", 0.75))
    vc.append(m49)

    # m50: Final note — D, warm and long
    m50 = stream.Measure(number=50)
    m50.append(make_note("D3", 2.5, fermata=True))
    m50.append(make_rest(0.5))
    vc.append(m50)

    return vc


def build_piano_part():
    """Build the Piano part (RH and LH).

    The piano is the other player — punctuating, responding, sometimes leading.
    Harmony: Dm, Gm, Am, Bb, C, F — with 7th chords, chromatic passing tones.
    RH: Chordal and arpeggiated figures.
    LH: Bass notes and walking bass lines.
    """
    rh = stream.Part()
    rh.insert(0, instrument.Piano())
    rh.partName = "Piano"

    lh = stream.Part()
    lh.insert(0, instrument.Piano())
    lh.insert(0, clef.BassClef())

    # ================================================================
    # Section A: Opening Game (mm. 1-12)
    # Piano enters gently, supporting the cello.
    # ================================================================

    # m1: Piano enters with a soft chord — placing the first piece
    rm1 = stream.Measure(number=1)
    rm1.insert(0, meter.TimeSignature("3/4"))
    rm1.insert(0, key.Key("d", "minor"))
    rm1.insert(0, dynamics.Dynamic("p"))
    rm1.append(make_chord(["F4", "A4", "D5"], 1.5))    # Dm
    rm1.append(make_chord(["E4", "G4", "C5"], 1.0))    # C
    rm1.append(make_rest(0.5))
    rh.append(rm1)

    rm2 = stream.Measure(number=2)
    rm2.append(make_chord(["D4", "F4", "A4"], 2.0))     # Dm
    rm2.append(make_rest(1.0))
    rh.append(rm2)

    # m3: Arpeggiated answer
    rm3 = stream.Measure(number=3)
    rm3.append(make_note("D4", 0.5))
    rm3.append(make_note("F4", 0.5))
    rm3.append(make_note("A4", 0.5))
    rm3.append(make_note("D5", 0.5))
    rm3.append(make_note("C5", 0.5))
    rm3.append(make_rest(0.5))
    rh.append(rm3)

    # m4: Chromatic chord — A7 (C# leading tone)
    rm4 = stream.Measure(number=4)
    rm4.append(make_chord(["C#4", "E4", "G4", "A4"], 1.5))  # A7
    rm4.append(make_chord(["D4", "F4", "Bb4"], 1.0))         # Bb/D
    rm4.append(make_rest(0.5))
    rh.append(rm4)

    # m5: Gentle arpeggios — F major color
    rm5 = stream.Measure(number=5)
    rm5.append(make_note("A4", 0.5))
    rm5.append(make_note("C5", 0.5))
    rm5.append(make_note("F5", 0.5))
    rm5.append(make_note("E5", 0.5))
    rm5.append(make_note("C5", 0.5))
    rm5.append(make_rest(0.5))
    rh.append(rm5)

    # m6: Dm7 arpeggio — deeper
    rm6 = stream.Measure(number=6)
    rm6.append(make_note("D4", 0.5))
    rm6.append(make_note("F4", 0.5))
    rm6.append(make_note("A4", 0.5))
    rm6.append(make_note("C5", 0.5))
    rm6.append(make_note("A4", 0.5))
    rm6.append(make_rest(0.5))
    rh.append(rm6)

    # m7: Gm7 — the friend leans forward
    rm7 = stream.Measure(number=7)
    rm7.append(make_chord(["Bb3", "D4", "F4"], 1.0))     # Gm first inv.
    rm7.append(make_chord(["G3", "Bb3", "D4", "F4"], 1.5))  # Gm7
    rm7.append(make_rest(0.5))
    rh.append(rm7)

    # m8: C7 — dominant function
    rm8 = stream.Measure(number=8)
    rm8.append(make_chord(["C4", "E4", "G4", "Bb4"], 1.5))  # C7
    rm8.append(make_chord(["C4", "E4", "A4"], 1.0))          # Am/C
    rm8.append(make_rest(0.5))
    rh.append(rm8)

    # m9: Dm with upper voice singing
    rm9 = stream.Measure(number=9)
    rm9.append(make_note("D5", 0.5))
    rm9.append(make_note("Eb5", 0.25))
    rm9.append(make_note("D5", 0.25))
    rm9.append(make_note("C5", 0.5))
    rm9.append(make_note("Bb4", 0.5))
    rm9.append(make_note("A4", 0.5))
    rm9.append(make_rest(0.5))
    rh.append(rm9)

    # m10: Bb major 7 arpeggio
    rm10 = stream.Measure(number=10)
    rm10.append(make_note("Bb4", 0.5))
    rm10.append(make_note("D5", 0.5))
    rm10.append(make_note("F5", 0.5))
    rm10.append(make_note("A5", 0.5))                       # BbMaj7 top
    rm10.append(make_note("F5", 0.5))
    rm10.append(make_rest(0.5))
    rh.append(rm10)

    # m11: A7 — dominant of D
    rm11 = stream.Measure(number=11)
    rm11.append(make_chord(["C#4", "E4", "G4", "A4"], 1.5))   # A7
    rm11.append(make_chord(["D4", "F4", "A4"], 1.0))           # Dm
    rm11.append(make_rest(0.5))
    rh.append(rm11)

    # m12: Resolution — Dm sustained
    rm12 = stream.Measure(number=12)
    rm12.append(make_chord(["D4", "F4", "A4", "C5"], 2.0))    # Dm7
    rm12.append(make_rest(1.0))
    rh.append(rm12)

    # ================================================================
    # Section B: Middle Game (mm. 13-24)
    # More rhythmic, staccato — pieces clicking on the board.
    # ================================================================

    rm13 = stream.Measure(number=13)
    rm13.insert(0, dynamics.Dynamic("mf"))
    rm13.append(make_chord(["D4", "F4", "A4"], 0.5, staccato=True))
    rm13.append(make_rest(0.5))
    rm13.append(make_chord(["E4", "G4", "Bb4"], 0.5, staccato=True))
    rm13.append(make_rest(0.5))
    rm13.append(make_chord(["F4", "A4", "C5"], 0.5, accent=True))
    rm13.append(make_rest(0.5))
    rh.append(rm13)

    rm14 = stream.Measure(number=14)
    rm14.append(make_chord(["D4", "G4", "Bb4"], 0.5, staccato=True))
    rm14.append(make_chord(["Eb4", "G4", "Bb4"], 0.5))          # Eb color
    rm14.append(make_chord(["D4", "F4", "A4"], 1.0))
    rm14.append(make_rest(1.0))
    rh.append(rm14)

    rm15 = stream.Measure(number=15)
    # Matching cello's urgency
    rm15.append(make_chord(["C4", "E4", "G4"], 0.5, staccato=True))
    rm15.append(make_chord(["D4", "F4", "A4"], 0.5, staccato=True))
    rm15.append(make_chord(["E4", "G4", "Bb4", "C5"], 1.0, accent=True))   # C7
    rm15.append(make_rest(1.0))
    rh.append(rm15)

    rm16 = stream.Measure(number=16)
    rm16.append(make_chord(["F4", "A4", "C5"], 0.5))
    rm16.append(make_chord(["E4", "G4", "C5"], 0.5))
    rm16.append(make_chord(["D4", "F4", "A4"], 1.5))
    rm16.append(make_rest(0.5))
    rh.append(rm16)

    # m17-18: F major territory
    rm17 = stream.Measure(number=17)
    rm17.insert(0, dynamics.Dynamic("f"))
    rm17.append(make_chord(["F4", "A4", "C5", "E5"], 1.5))     # FMaj7
    rm17.append(make_chord(["G4", "Bb4", "D5"], 1.0))           # Gm
    rm17.append(make_rest(0.5))
    rh.append(rm17)

    rm18 = stream.Measure(number=18)
    rm18.append(make_note("C5", 0.5))
    rm18.append(make_note("D5", 0.5))
    rm18.append(make_note("E5", 0.5))
    rm18.append(make_note("F5", 1.0, accent=True))
    rm18.append(make_rest(0.5))
    rh.append(rm18)

    rm19 = stream.Measure(number=19)
    rm19.append(make_chord(["F4", "A4", "C5"], 0.5, staccato=True))
    rm19.append(make_chord(["E4", "G4", "C5"], 0.5, staccato=True))
    rm19.append(make_chord(["D4", "F4", "Bb4"], 0.5, staccato=True))
    rm19.append(make_rest(1.5))
    rh.append(rm19)

    rm20 = stream.Measure(number=20)
    rm20.insert(0, dynamics.Dynamic("mf"))
    rm20.append(make_chord(["D4", "F4", "A4", "C5"], 1.0))    # Dm7
    rm20.append(make_chord(["Eb4", "G4", "Bb4"], 1.0))         # Eb — chromatic
    rm20.append(make_rest(1.0))
    rh.append(rm20)

    rm21 = stream.Measure(number=21)
    rm21.insert(0, dynamics.Dynamic("f"))
    rm21.append(make_chord(["C#4", "E4", "A4"], 0.5, accent=True))   # A major
    rm21.append(make_note("G#4", 0.25))
    rm21.append(make_note("A4", 0.25))
    rm21.append(make_chord(["D4", "F4", "A4"], 1.0))
    rm21.append(make_rest(1.0))
    rh.append(rm21)

    rm22 = stream.Measure(number=22)
    rm22.append(make_note("D5", 0.5))
    rm22.append(make_note("C5", 0.5))
    rm22.append(make_note("Bb4", 0.5))
    rm22.append(make_note("A4", 0.5))
    rm22.append(make_note("G4", 0.5))
    rm22.append(make_rest(0.5))
    rh.append(rm22)

    rm23 = stream.Measure(number=23)
    rm23.insert(0, dynamics.Dynamic("mp"))
    rm23.append(make_chord(["A3", "C4", "F4"], 1.5))           # F/A
    rm23.append(make_chord(["G3", "Bb3", "E4"], 1.0))          # Gm/E? — color
    rm23.append(make_rest(0.5))
    rh.append(rm23)

    rm24 = stream.Measure(number=24)
    rm24.append(make_chord(["D4", "F4", "A4"], 1.5))           # Dm
    rm24.append(make_rest(1.5))
    rh.append(rm24)

    # ================================================================
    # Section C: The Gambit (mm. 25-32)
    # Dramatic chords answering the cello's boldness.
    # ================================================================

    rm25 = stream.Measure(number=25)
    rm25.insert(0, dynamics.Dynamic("f"))
    rm25.append(make_chord(["Bb3", "D4", "F4", "A4"], 1.5, accent=True))  # BbMaj7
    rm25.append(make_chord(["A3", "C4", "F4"], 1.0))                       # F/A
    rm25.append(make_rest(0.5))
    rh.append(rm25)

    rm26 = stream.Measure(number=26)
    rm26.append(make_chord(["G3", "Bb3", "D4", "F4"], 1.0))    # Gm7
    rm26.append(make_chord(["A3", "C#4", "E4", "G4"], 1.5, accent=True))  # A7
    rm26.append(make_rest(0.5))
    rh.append(rm26)

    rm27 = stream.Measure(number=27)
    rm27.append(make_note("Ab4", 0.5))
    rm27.append(make_note("G4", 0.5))
    rm27.append(make_note("F#4", 0.5))
    rm27.append(make_note("F4", 0.5))
    rm27.append(make_note("E4", 0.5))
    rm27.append(make_rest(0.5))
    rh.append(rm27)

    rm28 = stream.Measure(number=28)
    rm28.append(make_chord(["C#4", "E4", "G4", "Bb4"], 2.0))    # dim/A7b9 — suspense
    rm28.append(make_rest(1.0))
    rh.append(rm28)

    rm29 = stream.Measure(number=29)
    rm29.insert(0, dynamics.Dynamic("ff"))
    cresc_rh = dynamics.Crescendo()
    ch29a = make_chord(["D4", "F4", "A4", "D5"], 1.0, accent=True)   # Dm
    rm29.append(ch29a)
    rm29.append(make_chord(["C4", "F4", "A4", "C5"], 1.0))            # F
    ch29c = make_chord(["Bb3", "D4", "F4", "Bb4"], 0.5)               # Bb
    rm29.append(ch29c)
    rm29.append(make_rest(0.5))
    cresc_rh.addSpannedElements([ch29a, ch29c])
    rh.insert(0, cresc_rh)
    rh.append(rm29)

    rm30 = stream.Measure(number=30)
    dim_rh = dynamics.Diminuendo()
    ch30a = make_chord(["C4", "E4", "G4", "Bb4"], 1.0)    # C7
    rm30.append(ch30a)
    ch30b = make_chord(["D4", "F4", "A4"], 1.5)            # Dm
    rm30.append(ch30b)
    rm30.append(make_rest(0.5))
    dim_rh.addSpannedElements([ch30a, ch30b])
    rh.insert(0, dim_rh)
    rh.append(rm30)

    rm31 = stream.Measure(number=31)
    rm31.insert(0, dynamics.Dynamic("mf"))
    rm31.append(make_note("G4", 0.5))
    rm31.append(make_note("F4", 0.5))
    rm31.append(make_note("E4", 0.5))
    rm31.append(make_chord(["A3", "C#4", "E4"], 1.0))           # A major — V of D
    rm31.append(make_rest(0.5))
    rh.append(rm31)

    rm32 = stream.Measure(number=32)
    rm32.append(make_chord(["D4", "F4", "A4", "C5"], 1.5))      # Dm7
    rm32.append(make_rest(1.5))
    rh.append(rm32)

    # ================================================================
    # Section A': Endgame (mm. 33-44)
    # Richer harmony, supporting the cello's augmented theme.
    # ================================================================

    rm33 = stream.Measure(number=33)
    rm33.insert(0, dynamics.Dynamic("mf"))
    rm33.append(make_chord(["D4", "F4", "A4", "C5"], 1.5))     # Dm7
    rm33.append(make_chord(["E4", "G4", "Bb4", "D5"], 1.0))    # Gm7/E
    rm33.append(make_rest(0.5))
    rh.append(rm33)

    rm34 = stream.Measure(number=34)
    rm34.append(make_chord(["C4", "E4", "G4", "Bb4"], 2.0))     # C7
    rm34.append(make_chord(["Bb3", "D4", "F4"], 0.5))            # Bb
    rm34.append(make_rest(0.5))
    rh.append(rm34)

    rm35 = stream.Measure(number=35)
    rm35.append(make_chord(["A3", "C#4", "E4", "G4"], 2.0))     # A7
    rm35.append(make_rest(1.0))
    rh.append(rm35)

    rm36 = stream.Measure(number=36)
    rm36.append(make_note("Bb4", 0.5))
    rm36.append(make_note("A4", 0.5))
    rm36.append(make_note("G4", 0.5))
    rm36.append(make_chord(["D4", "F4", "A4"], 1.0))            # Dm
    rm36.append(make_rest(0.5))
    rh.append(rm36)

    rm37 = stream.Measure(number=37)
    rm37.insert(0, dynamics.Dynamic("f"))
    rm37.append(make_chord(["F4", "A4", "C5", "E5", "A5"], 1.5))   # FMaj7, high A5
    rm37.append(make_chord(["G4", "Bb4", "D5", "F5", "G5"], 1.0))  # Gm7, high G5
    rm37.append(make_rest(0.5))
    rh.append(rm37)

    rm38 = stream.Measure(number=38)
    rm38.append(make_chord(["C4", "E4", "G4", "Bb4"], 1.0))     # C7
    rm38.append(make_chord(["D4", "F4", "A4"], 1.5))             # Dm
    rm38.append(make_rest(0.5))
    rh.append(rm38)

    rm39 = stream.Measure(number=39)
    rm39.insert(0, dynamics.Dynamic("mp"))
    rm39.append(make_note("A4", 0.5))
    rm39.append(make_note("F4", 0.5))
    rm39.append(make_note("D4", 0.5))
    rm39.append(make_note("A3", 0.5))
    rm39.append(make_rest(1.0))
    rh.append(rm39)

    rm40 = stream.Measure(number=40)
    rm40.append(make_chord(["Bb3", "D4", "F4", "A4"], 1.5))     # BbMaj7
    rm40.append(make_chord(["G3", "Bb3", "D4"], 1.0))            # Gm
    rm40.append(make_rest(0.5))
    rh.append(rm40)

    rm41 = stream.Measure(number=41)
    rm41.append(make_chord(["A3", "C#4", "E4"], 1.0))            # A major
    rm41.append(make_chord(["D4", "F4", "A4"], 1.5))             # Dm
    rm41.append(make_rest(0.5))
    rh.append(rm41)

    rm42 = stream.Measure(number=42)
    rm42.append(make_note("D5", 0.75))
    rm42.append(make_note("C5", 0.75))
    rm42.append(make_note("Bb4", 0.75))
    rm42.append(make_note("A4", 0.75))
    rh.append(rm42)

    rm43 = stream.Measure(number=43)
    rm43.insert(0, dynamics.Dynamic("p"))
    rm43.append(make_chord(["C#4", "E4", "G4", "A4"], 2.5))     # A7
    rm43.append(make_rest(0.5))
    rh.append(rm43)

    rm44 = stream.Measure(number=44)
    rm44.append(make_chord(["D4", "F4", "A4"], 2.0))             # Dm
    rm44.append(make_rest(1.0))
    rh.append(rm44)

    # ================================================================
    # Coda: The Handshake (mm. 45-50)
    # D minor → D major (Picardy third). The wine is opened.
    # ================================================================

    rm45 = stream.Measure(number=45)
    rm45.insert(0, dynamics.Dynamic("p"))
    rm45.append(make_chord(["D4", "F4", "A4"], 1.0))              # Dm
    rm45.append(make_chord(["C4", "E4", "G4", "Bb4"], 1.5))       # C7
    rm45.append(make_rest(0.5))
    rh.append(rm45)

    rm46 = stream.Measure(number=46)
    rm46.append(make_chord(["Bb3", "D4", "F4"], 1.5))              # Bb
    rm46.append(make_chord(["A3", "C#4", "E4"], 1.0))              # A major
    rm46.append(make_rest(0.5))
    rh.append(rm46)

    # m47: The Picardy — F# appears!
    rm47 = stream.Measure(number=47)
    rm47.insert(0, dynamics.Dynamic("pp"))
    rm47.append(make_chord(["D4", "F#4", "A4"], 2.0))              # D MAJOR!
    rm47.append(make_rest(1.0))
    rh.append(rm47)

    rm48 = stream.Measure(number=48)
    rm48.append(make_chord(["D4", "F#4", "A4", "D5"], 1.5))        # D major, fuller
    rm48.append(make_chord(["E4", "G4", "A4"], 1.0))                # A/E
    rm48.append(make_rest(0.5))
    rh.append(rm48)

    rm49 = stream.Measure(number=49)
    rm49.append(make_note("D5", 0.75))
    rm49.append(make_note("C#5", 0.75))
    rm49.append(make_note("B4", 0.75))
    rm49.append(make_note("A4", 0.75))
    rh.append(rm49)

    rm50 = stream.Measure(number=50)
    final_chord = make_chord(["D4", "F#4", "A4", "D5"], 2.5, tenuto=True)  # D major final
    final_chord.expressions.append(expressions.Fermata())
    rm50.append(final_chord)
    rm50.append(make_rest(0.5))
    rh.append(rm50)

    # ================================================================
    # Left Hand
    # ================================================================

    # --- Section A (mm. 1-12) ---
    # Consistent waltz pattern: bass on beat 1, fifth on beat 2, octave on beat 3.

    # m1
    lm1 = stream.Measure(number=1)
    lm1.insert(0, meter.TimeSignature("3/4"))
    lm1.insert(0, key.Key("d", "minor"))
    lm1.insert(0, dynamics.Dynamic("p"))
    lm1.append(make_note("D2", 1.0))
    lm1.append(make_note("A2", 1.0))
    lm1.append(make_note("D3", 1.0))
    lh.append(lm1)

    # m2: same waltz shape, rests for phrase end
    lm2 = stream.Measure(number=2)
    lm2.append(make_note("D2", 1.0))
    lm2.append(make_note("A2", 1.0))
    lm2.append(make_rest(1.0))
    lh.append(lm2)

    # m3
    lm3 = stream.Measure(number=3)
    lm3.append(make_note("D2", 1.0))
    lm3.append(make_note("A2", 1.0))
    lm3.append(make_note("F3", 1.0))
    lh.append(lm3)

    # m4: A bass — chromatic walk preserves color but stays in waltz rhythm
    lm4 = stream.Measure(number=4)
    lm4.append(make_note("A1", 1.0))
    lm4.append(make_note("E2", 1.0))
    lm4.append(make_note("A2", 1.0))
    lh.append(lm4)

    # m5
    lm5 = stream.Measure(number=5)
    lm5.append(make_note("F2", 1.0))
    lm5.append(make_note("C3", 1.0))
    lm5.append(make_rest(1.0))
    lh.append(lm5)

    # m6
    lm6 = stream.Measure(number=6)
    lm6.append(make_note("D2", 1.0))
    lm6.append(make_note("A2", 1.0))
    lm6.append(make_note("D3", 1.0))
    lh.append(lm6)

    # m7: Gm bass — consistent waltz shape
    lm7 = stream.Measure(number=7)
    lm7.append(make_note("G2", 1.0))
    lm7.append(make_note("D3", 1.0))
    lm7.append(make_note("G3", 1.0))
    lh.append(lm7)

    # m8: C bass — dominant pedal
    lm8 = stream.Measure(number=8)
    lm8.append(make_note("C2", 1.0))
    lm8.append(make_note("G2", 1.0))
    lm8.append(make_rest(1.0))
    lh.append(lm8)

    # m9
    lm9 = stream.Measure(number=9)
    lm9.append(make_note("D2", 1.0))
    lm9.append(make_note("A2", 1.0))
    lm9.append(make_note("D3", 1.0))
    lh.append(lm9)

    # m10: Bb bass
    lm10 = stream.Measure(number=10)
    lm10.append(make_note("Bb1", 1.0))
    lm10.append(make_note("F2", 1.0))
    lm10.append(make_note("Bb2", 1.0))
    lh.append(lm10)

    # m11: A bass — dominant
    lm11 = stream.Measure(number=11)
    lm11.append(make_note("A1", 1.0))
    lm11.append(make_note("E2", 1.0))
    lm11.append(make_note("A2", 1.0))
    lh.append(lm11)

    # m12: D bass — resolution
    lm12 = stream.Measure(number=12)
    lm12.append(make_note("D2", 2.0))
    lm12.append(make_rest(1.0))
    lh.append(lm12)

    # --- Section B (mm. 13-24) ---
    # More rhythmic, walking bass, staccato

    # Section B LH: consistent staccato waltz pattern (bass-fifth-rest)
    lm13 = stream.Measure(number=13)
    lm13.append(make_note("D2", 1.0, staccato=True))
    lm13.append(make_note("A2", 1.0, staccato=True))
    lm13.append(make_rest(1.0))
    lh.append(lm13)

    lm14 = stream.Measure(number=14)
    lm14.append(make_note("G2", 1.0, staccato=True))
    lm14.append(make_note("D3", 1.0, staccato=True))
    lm14.append(make_rest(1.0))
    lh.append(lm14)

    lm15 = stream.Measure(number=15)
    lm15.append(make_note("C2", 1.0, staccato=True))
    lm15.append(make_note("G2", 1.0, staccato=True))
    lm15.append(make_rest(1.0))
    lh.append(lm15)

    lm16 = stream.Measure(number=16)
    lm16.append(make_note("F2", 1.0, staccato=True))
    lm16.append(make_note("C3", 1.0, staccato=True))
    lm16.append(make_rest(1.0))
    lh.append(lm16)

    # m17-18: F major territory — same staccato pattern
    lm17 = stream.Measure(number=17)
    lm17.append(make_note("F2", 1.0, staccato=True))
    lm17.append(make_note("C3", 1.0, staccato=True))
    lm17.append(make_rest(1.0))
    lh.append(lm17)

    lm18 = stream.Measure(number=18)
    lm18.append(make_note("C2", 1.0, staccato=True))
    lm18.append(make_note("G2", 1.0, staccato=True))
    lm18.append(make_rest(1.0))
    lh.append(lm18)

    lm19 = stream.Measure(number=19)
    lm19.append(make_note("F2", 1.0, staccato=True))
    lm19.append(make_note("C3", 1.0, staccato=True))
    lm19.append(make_rest(1.0))
    lh.append(lm19)

    lm20 = stream.Measure(number=20)
    lm20.append(make_note("D2", 1.0, staccato=True))
    lm20.append(make_note("A2", 1.0, staccato=True))
    lm20.append(make_rest(1.0))
    lh.append(lm20)

    lm21 = stream.Measure(number=21)
    lm21.append(make_note("A1", 1.0, staccato=True))
    lm21.append(make_note("E2", 1.0, staccato=True))
    lm21.append(make_rest(1.0))
    lh.append(lm21)

    lm22 = stream.Measure(number=22)
    lm22.append(make_note("D2", 1.0, staccato=True))
    lm22.append(make_note("A2", 1.0, staccato=True))
    lm22.append(make_rest(1.0))
    lh.append(lm22)

    lm23 = stream.Measure(number=23)
    lm23.append(make_note("F2", 1.0, staccato=True))
    lm23.append(make_note("C3", 1.0, staccato=True))
    lm23.append(make_rest(1.0))
    lh.append(lm23)

    lm24 = stream.Measure(number=24)
    lm24.append(make_note("D2", 1.5))
    lm24.append(make_rest(1.5))
    lh.append(lm24)

    # --- Section C: The Gambit (mm. 25-32) ---

    lm25 = stream.Measure(number=25)
    lm25.append(make_note("Bb1", 1.0, accent=True))
    lm25.append(make_note("F2", 1.0))
    lm25.append(make_note("Bb2", 1.0))
    lh.append(lm25)

    lm26 = stream.Measure(number=26)
    lm26.append(make_note("G2", 1.0))
    lm26.append(make_note("D3", 1.0))
    lm26.append(make_note("A2", 1.0))
    lh.append(lm26)

    lm27 = stream.Measure(number=27)
    lm27.append(make_note("D2", 0.5))
    lm27.append(make_note("Eb2", 0.5))                  # chromatic
    lm27.append(make_note("E2", 0.5))
    lm27.append(make_note("F2", 0.5))
    lm27.append(make_note("F#2", 0.5))                  # chromatic
    lm27.append(make_note("G2", 0.5))                   # stepwise resolution
    lh.append(lm27)

    lm28 = stream.Measure(number=28)
    lm28.append(make_note("A2", 1.0))                    # dominant pedal (smoother)
    lm28.append(make_note("E2", 1.0))
    lm28.append(make_rest(1.0))
    lh.append(lm28)

    lm29 = stream.Measure(number=29)
    lm29.append(make_note("D2", 1.0, accent=True))
    lm29.append(make_note("A2", 1.0))
    lm29.append(make_note("D3", 1.0))
    lh.append(lm29)

    lm30 = stream.Measure(number=30)
    lm30.append(make_note("C2", 1.0))
    lm30.append(make_note("G2", 1.0))
    lm30.append(make_note("D2", 1.0))
    lh.append(lm30)

    lm31 = stream.Measure(number=31)
    lm31.append(make_note("G2", 0.5))
    lm31.append(make_note("F2", 0.5))
    lm31.append(make_note("E2", 0.5))
    lm31.append(make_note("C#2", 0.5))                  # leading tone, stepwise
    lm31.append(make_note("A1", 0.5))
    lm31.append(make_rest(0.5))
    lh.append(lm31)

    lm32 = stream.Measure(number=32)
    lm32.append(make_note("D2", 1.5))
    lm32.append(make_rest(1.5))
    lh.append(lm32)

    # --- Section A': Endgame (mm. 33-44) ---

    lm33 = stream.Measure(number=33)
    lm33.append(make_note("D2", 1.0))
    lm33.append(make_note("A2", 1.0))
    lm33.append(make_note("D3", 1.0))
    lh.append(lm33)

    lm34 = stream.Measure(number=34)
    lm34.append(make_note("C2", 1.0))
    lm34.append(make_note("G2", 1.0))
    lm34.append(make_note("C3", 1.0))
    lh.append(lm34)

    lm35 = stream.Measure(number=35)
    lm35.append(make_note("A1", 1.0))
    lm35.append(make_note("E2", 1.0))
    lm35.append(make_rest(1.0))
    lh.append(lm35)

    lm36 = stream.Measure(number=36)
    lm36.append(make_note("Bb1", 1.0))
    lm36.append(make_note("F2", 1.0))
    lm36.append(make_note("Bb2", 1.0))
    lh.append(lm36)

    lm37 = stream.Measure(number=37)
    lm37.append(make_note("F2", 1.0))
    lm37.append(make_note("C3", 1.0))
    lm37.append(make_note("F3", 1.0))
    lh.append(lm37)

    lm38 = stream.Measure(number=38)
    lm38.append(make_note("C2", 1.0))
    lm38.append(make_note("G2", 1.0))
    lm38.append(make_note("C3", 1.0))
    lh.append(lm38)

    lm39 = stream.Measure(number=39)
    lm39.append(make_note("D2", 1.0))
    lm39.append(make_note("A2", 0.5))
    lm39.append(make_note("D3", 0.5))
    lm39.append(make_rest(1.0))
    lh.append(lm39)

    lm40 = stream.Measure(number=40)
    lm40.append(make_note("Bb1", 1.0))
    lm40.append(make_note("F2", 1.0))
    lm40.append(make_note("G2", 0.5))
    lm40.append(make_rest(0.5))
    lh.append(lm40)

    lm41 = stream.Measure(number=41)
    lm41.append(make_note("A1", 1.0))
    lm41.append(make_note("E2", 0.5))
    lm41.append(make_note("D2", 1.0))
    lm41.append(make_rest(0.5))
    lh.append(lm41)

    lm42 = stream.Measure(number=42)
    lm42.append(make_note("D2", 1.0))
    lm42.append(make_note("E2", 0.5))
    lm42.append(make_note("F2", 0.5))
    lm42.append(make_note("G2", 0.5))
    lm42.append(make_rest(0.5))
    lh.append(lm42)

    lm43 = stream.Measure(number=43)
    lm43.append(make_note("A1", 2.5))                    # dominant pedal
    lm43.append(make_rest(0.5))
    lh.append(lm43)

    lm44 = stream.Measure(number=44)
    lm44.append(make_note("D2", 2.0))
    lm44.append(make_rest(1.0))
    lh.append(lm44)

    # --- Coda (mm. 45-50) ---

    lm45 = stream.Measure(number=45)
    lm45.append(make_note("D2", 1.0))
    lm45.append(make_note("C2", 1.5))
    lm45.append(make_rest(0.5))
    lh.append(lm45)

    lm46 = stream.Measure(number=46)
    lm46.append(make_note("Bb1", 1.5))
    lm46.append(make_note("A1", 1.0))
    lm46.append(make_rest(0.5))
    lh.append(lm46)

    # m47: Picardy — bass on D
    lm47 = stream.Measure(number=47)
    lm47.append(make_note("D2", 2.0))
    lm47.append(make_note("A2", 0.5))
    lm47.append(make_rest(0.5))
    lh.append(lm47)

    lm48 = stream.Measure(number=48)
    lm48.append(make_note("D2", 1.5))
    lm48.append(make_note("A1", 1.0))
    lm48.append(make_rest(0.5))
    lh.append(lm48)

    lm49 = stream.Measure(number=49)
    lm49.append(make_note("D2", 1.0))
    lm49.append(make_note("E2", 0.5))
    lm49.append(make_note("F#2", 0.5))                   # F# in the bass too!
    lm49.append(make_note("A2", 0.5))
    lm49.append(make_rest(0.5))
    lh.append(lm49)

    # m50: Final D — deep and warm
    lm50 = stream.Measure(number=50)
    lm50.append(make_note("D1", 2.5, fermata=True))     # very deep D1
    lm50.append(make_rest(0.5))
    lh.append(lm50)

    return rh, lh


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "score.musicxml")

    s = stream.Score()
    s.insert(0, metadata.Metadata())
    s.metadata.title = "The Wine Gambit"
    s.metadata.composer = "MusicLaude"
    s.metadata.movementName = "A chess game between old friends"

    vc_part = build_cello_part()
    piano_rh, piano_lh = build_piano_part()
    piano_lh.partName = "Piano"

    s.insert(0, vc_part)
    s.insert(0, piano_rh)
    s.insert(0, piano_lh)

    # Create staff group for piano
    sg = layout.StaffGroup([piano_rh, piano_lh], symbol="brace")
    s.insert(0, sg)

    s.write("musicxml", fp=out_path)
    print(f"Score written to {out_path}")


if __name__ == "__main__":
    main()
