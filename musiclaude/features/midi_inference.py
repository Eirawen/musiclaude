"""Infer expressive features from MIDI velocity data.

MIDI files lack explicit dynamic markings, hairpins, and articulations.
We can reliably infer *some* features from velocity patterns:

RELIABLE (window-based velocity → marking-scale):
- dynamics_count: transitions between dynamic levels in smoothed velocity
- hairpin_count: sustained directional velocity changes across phrases

UNRELIABLE (skipped — use MusicXML-source data for these):
- staccato_count: piano key release ≠ staccato marking
- accent_count: velocity variation ≠ notated accent
- expression_count: too sparse and varied to infer from velocity alone

These features are only applied when the score was parsed from MIDI
(no existing Dynamic/DynamicWedge objects in the score).
"""

import logging

import numpy as np
from music21 import stream

logger = logging.getLogger(__name__)

# Velocity-to-dynamic thresholds (standard 6-level mapping)
DYNAMIC_THRESHOLDS = [
    (0, 32, "pp"),
    (32, 48, "p"),
    (48, 64, "mp"),
    (64, 80, "mf"),
    (80, 96, "f"),
    (96, 128, "ff"),
]


def _get_notes_with_absolute_offsets(score: stream.Score) -> list[dict]:
    """Extract notes with absolute offsets using score.flatten()."""
    flat = score.flatten()
    notes = []
    for n in flat.getElementsByClass('Note'):
        if n.volume.velocity is not None:
            notes.append({
                'offset': float(n.offset),
                'velocity': n.volume.velocity,
                'duration': float(n.duration.quarterLength),
            })
    notes.sort(key=lambda x: x['offset'])
    return notes


def _velocity_to_dynamic(velocity: float) -> str:
    """Map a velocity value to a dynamic label."""
    for lo, hi, label in DYNAMIC_THRESHOLDS:
        if lo <= velocity < hi:
            return label
    return "ff"


def _build_windows(notes: list[dict], window_size: float) -> list[dict]:
    """Aggregate notes into fixed-size windows with mean velocity."""
    if not notes:
        return []

    max_offset = notes[-1]['offset']
    windows = []

    for start in np.arange(0, max_offset + 0.01, window_size):
        end = start + window_size
        vels = [n['velocity'] for n in notes
                if start <= n['offset'] < end]
        if vels:
            windows.append({
                'start': start,
                'mean_vel': np.mean(vels),
                'n_notes': len(vels),
            })

    return windows


def infer_dynamics_count(notes: list[dict]) -> int:
    """Approximate number of dynamic markings a human would notate.

    Uses 16-beat windows (~4 measures in 4/4) to smooth velocity into
    phrase-level dynamics. Counts stable transitions: a new dynamic
    level must persist for at least 2 windows to count (ignoring
    one-window blips that a human wouldn't mark).

    Calibration: Berg Sonata (2347 notes, ~400 measures) → 20 markings.
    PDMX high-rated median = 8, p75 = 19.
    """
    windows = _build_windows(notes, 16.0)
    if not windows:
        return 0

    labels = [_velocity_to_dynamic(w['mean_vel']) for w in windows]

    # Count stable transitions (new level must persist 2+ windows)
    count = 1  # the opening dynamic
    prev_stable = labels[0]
    for i in range(1, len(labels) - 1):
        if labels[i] != prev_stable and labels[i] == labels[i + 1]:
            count += 1
            prev_stable = labels[i]

    return count


def infer_hairpin_count(notes: list[dict]) -> int:
    """Approximate number of hairpin wedges a human would notate.

    Uses 8-beat windows. A hairpin requires:
    - At least 3 consecutive windows of sustained directional change
      (= 24+ beats, roughly 6+ measures)
    - Total velocity change >= 15 (about one dynamic level)

    Calibration: short piece (258 notes) → 2 hairpins.
    Berg Sonata → 20 hairpins (very dynamic piece).
    PDMX high-rated median = 1, p75 = 4.
    """
    windows = _build_windows(notes, 8.0)
    if len(windows) < 2:
        return 0

    means = np.array([w['mean_vel'] for w in windows])
    count = 0
    run_dir = 0
    run_len = 0
    run_start_vel = means[0]

    for i in range(1, len(means)):
        delta = means[i] - means[i - 1]
        if delta > 2:
            new_dir = 1
        elif delta < -2:
            new_dir = -1
        else:
            new_dir = 0

        if new_dir == run_dir and new_dir != 0:
            run_len += 1
        else:
            if run_len >= 3 and abs(means[i - 1] - run_start_vel) >= 15:
                count += 1
            run_dir = new_dir
            run_len = 1 if new_dir != 0 else 0
            run_start_vel = means[i - 1]

    # Final run
    if run_len >= 3 and abs(means[-1] - run_start_vel) >= 15:
        count += 1

    return count


def infer_all(score: stream.Score) -> dict:
    """Infer expressive features from a MIDI-parsed score.

    Only infers dynamics_count and hairpin_count — these can be reliably
    mapped from velocity patterns to the marking-scale used by MusicXML.
    Other expressive features (staccato, accent, expression) cannot be
    cleanly inferred from MIDI velocity and are left to the standard
    extractor (which will return 0 for MIDI files, as expected).
    """
    notes = _get_notes_with_absolute_offsets(score)

    if not notes:
        return {}

    return {
        "dynamics_count": infer_dynamics_count(notes),
        "hairpin_count": infer_hairpin_count(notes),
    }
