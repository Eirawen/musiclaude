"""Analyze WHERE and HOW expressive features appear in canonical scores.

Instead of counting dynamics/hairpins/staccato, analyze their CONTEXT:
- Where do dynamics change? (phrase starts? peaks? section boundaries?)
- How do hairpins relate to pitch contour?
- Where does staccato cluster?
- How do expression markings relate to structure?

Output: compositional principles derived from data, not feature counts.
"""

import logging
import os
import random
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def analyze_one(filepath: str) -> dict | None:
    """Deep analysis of one score's expressive patterns."""
    try:
        import warnings
        warnings.filterwarnings("ignore")
        logging.disable(logging.WARNING)

        from music21 import converter, dynamics, expressions, articulations, tempo

        score = converter.parse(filepath)
        flat = score.flatten()
        notes = list(flat.getElementsByClass('Note'))

        if len(notes) < 20:
            return None

        total_ql = float(flat.highestTime) if flat.highestTime else 0
        if total_ql == 0:
            return None

        result = {
            "filepath": filepath,
            "total_notes": len(notes),
            "total_ql": total_ql,
        }

        # === 1. DYNAMICS: Where do they appear? ===
        dyns = list(flat.getElementsByClass(dynamics.Dynamic))
        result["dynamics_count"] = len(dyns)

        if dyns and total_ql > 0:
            # Position of each dynamic as fraction of piece (0.0 = start, 1.0 = end)
            dyn_positions = []
            for d in dyns:
                pos = float(d.offset) / total_ql
                dyn_positions.append(pos)

            result["dyn_positions"] = dyn_positions

            # How many dynamics in first 10%? Last 10%? Middle?
            first_10 = sum(1 for p in dyn_positions if p < 0.1)
            last_10 = sum(1 for p in dyn_positions if p > 0.9)
            result["dyn_pct_first_10"] = first_10 / len(dyns) if dyns else 0
            result["dyn_pct_last_10"] = last_10 / len(dyns) if dyns else 0

            # Dynamics per structural quarter (divide piece into 4 parts)
            quarters = [0, 0, 0, 0]
            for p in dyn_positions:
                q = min(3, int(p * 4))
                quarters[q] += 1
            result["dyn_by_quarter"] = quarters

            # Dynamic level changes
            dyn_levels = []
            level_map = {"ppp": 0, "pp": 1, "p": 2, "mp": 3, "mf": 4, "f": 5, "ff": 6, "fff": 7}
            for d in dyns:
                vol = d.volumeScalar
                if vol is not None:
                    dyn_levels.append(vol)
            if len(dyn_levels) > 1:
                # Average dynamic trajectory: rising or falling?
                mid = len(dyn_levels) // 2
                first_half_avg = np.mean(dyn_levels[:mid])
                second_half_avg = np.mean(dyn_levels[mid:])
                result["dyn_trajectory"] = "rising" if second_half_avg > first_half_avg + 0.05 else (
                    "falling" if second_half_avg < first_half_avg - 0.05 else "flat"
                )
                result["dyn_max_position"] = dyn_positions[np.argmax(dyn_levels)]
                result["dyn_range"] = max(dyn_levels) - min(dyn_levels)

        # === 2. HAIRPINS: How do they relate to pitch? ===
        wedges = list(flat.getElementsByClass('DynamicWedge'))
        # Also try Crescendo/Diminuendo directly
        from music21.dynamics import Crescendo, Diminuendo
        crescendos = [w for w in flat.getElementsByClass(Crescendo)]
        diminuendos = [w for w in flat.getElementsByClass(Diminuendo)]
        result["crescendo_count"] = len(crescendos)
        result["diminuendo_count"] = len(diminuendos)
        result["hairpin_count"] = len(crescendos) + len(diminuendos)

        if crescendos:
            cresc_positions = [float(c.offset) / total_ql for c in crescendos]
            result["cresc_avg_position"] = np.mean(cresc_positions)
        if diminuendos:
            dim_positions = [float(d.offset) / total_ql for d in diminuendos]
            result["dim_avg_position"] = np.mean(dim_positions)

        # === 3. PITCH CONTOUR around dynamics ===
        # For each dynamic marking, what's the pitch doing nearby?
        if dyns and notes:
            note_offsets = np.array([float(n.offset) for n in notes])
            note_pitches = np.array([n.pitch.midi for n in notes])

            dyn_pitch_context = []
            for d in dyns:
                d_offset = float(d.offset)
                # Find notes within 4 beats before and after
                nearby = (note_offsets >= d_offset - 4) & (note_offsets <= d_offset + 4)
                before = (note_offsets >= d_offset - 4) & (note_offsets < d_offset)
                after = (note_offsets > d_offset) & (note_offsets <= d_offset + 4)

                if np.any(before) and np.any(after):
                    avg_before = note_pitches[before].mean()
                    avg_after = note_pitches[after].mean()
                    contour = "rising" if avg_after > avg_before + 1 else (
                        "falling" if avg_after < avg_before - 1 else "static"
                    )
                    dyn_pitch_context.append(contour)

            if dyn_pitch_context:
                result["dyn_at_rising"] = dyn_pitch_context.count("rising") / len(dyn_pitch_context)
                result["dyn_at_falling"] = dyn_pitch_context.count("falling") / len(dyn_pitch_context)
                result["dyn_at_static"] = dyn_pitch_context.count("static") / len(dyn_pitch_context)

        # === 4. STACCATO: Where does it cluster? ===
        staccatos = []
        for n in notes:
            for art in n.articulations:
                if isinstance(art, articulations.Staccato):
                    staccatos.append(float(n.offset))
                    break
        result["staccato_count"] = len(staccatos)

        if staccatos and total_ql > 0:
            stac_positions = [s / total_ql for s in staccatos]
            # Is staccato clustered or spread?
            if len(stac_positions) > 5:
                # Compute clustering: what % of staccatos are within 2 beats of another?
                stac_arr = np.array(staccatos)
                clustered = 0
                for s in stac_arr:
                    nearby = np.sum(np.abs(stac_arr - s) < 2.0) - 1  # exclude self
                    if nearby > 0:
                        clustered += 1
                result["staccato_clustering"] = clustered / len(stac_arr)

            # Staccato in fast vs slow passages
            # Approximate: high note density = fast passage
            if notes:
                stac_densities = []
                for s_offset in staccatos:
                    window_notes = sum(1 for n in notes
                                      if abs(float(n.offset) - s_offset) < 4.0)
                    stac_densities.append(window_notes)
                result["staccato_avg_local_density"] = np.mean(stac_densities)

        # === 5. ARTICULATION PATTERNS ===
        accent_offsets = []
        tenuto_offsets = []
        for n in notes:
            for art in n.articulations:
                if isinstance(art, articulations.Accent):
                    accent_offsets.append(float(n.offset))
                elif isinstance(art, articulations.Tenuto):
                    tenuto_offsets.append(float(n.offset))

        result["accent_count"] = len(accent_offsets)
        result["tenuto_count"] = len(tenuto_offsets)

        # Are accents on strong beats?
        if accent_offsets:
            # In 6/8, strong beats at 0 and 3 (of 6 eighth-note measure)
            # In 4/4, strong beats at 0 and 2
            # Simplify: check if offset mod 3.0 is near 0
            strong_beat_accents = sum(1 for a in accent_offsets if a % 3.0 < 0.5 or a % 3.0 > 2.5)
            result["accent_on_strong_beat_pct"] = strong_beat_accents / len(accent_offsets)

        # === 6. TEMPO/EXPRESSION MARKINGS ===
        tempos = list(flat.getElementsByClass(tempo.MetronomeMark))
        result["tempo_marking_count"] = len(tempos)

        if len(tempos) > 1:
            tempo_positions = [float(t.offset) / total_ql for t in tempos]
            result["tempo_change_positions"] = tempo_positions

        # Expression texts
        expr_texts = []
        for e in flat.getElementsByClass(expressions.TextExpression):
            expr_texts.append(str(e.content).lower() if e.content else "")
        result["expression_texts"] = expr_texts

        # === 7. PHRASE BOUNDARY DETECTION (simple) ===
        # Look for rests > 1 beat as phrase boundaries
        rests = list(flat.getElementsByClass('Rest'))
        phrase_boundaries = [float(r.offset) for r in rests if float(r.duration.quarterLength) >= 1.0]
        result["n_phrase_boundaries"] = len(phrase_boundaries)

        # Do dynamics tend to appear near phrase boundaries?
        if dyns and phrase_boundaries:
            near_boundary = 0
            for d in dyns:
                d_off = float(d.offset)
                for pb in phrase_boundaries:
                    if abs(d_off - pb) < 2.0:
                        near_boundary += 1
                        break
            result["dyn_near_phrase_boundary_pct"] = near_boundary / len(dyns)

        return result

    except Exception as e:
        logging.disable(logging.NOTSET)
        logger.error(f"Failed {filepath}: {e}")
        return None
    finally:
        logging.disable(logging.NOTSET)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--sample", type=int, default=200,
                        help="Sample N richly-annotated pieces")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    import pandas as pd
    from pathlib import Path

    # Find richly annotated files (those with high dynamics/hairpin counts)
    features_csv = "data/canonical/canonical_features.csv"
    if not os.path.exists(features_csv):
        logger.error("Run extract_canonical_features.py first")
        return

    df = pd.read_csv(features_csv)
    # Pick pieces with rich expression (dynamics >= 10 AND hairpins >= 5)
    rich = df[(df["dynamics_count"] >= 10) & (df["hairpin_count"] >= 5)]
    logger.info(f"Found {len(rich)} richly annotated pieces (dynamics>=10, hairpins>=5)")

    if len(rich) > args.sample:
        rich = rich.sample(args.sample, random_state=42)
    logger.info(f"Analyzing {len(rich)} pieces")

    filepaths = rich["filepath"].tolist()

    # Analyze in parallel
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(analyze_one, fp): fp for fp in filepaths}
        for i, future in enumerate(as_completed(futures), 1):
            r = future.result(timeout=300)
            if r:
                results.append(r)
            if i % 25 == 0:
                logger.info(f"Progress: {i}/{len(filepaths)} ({len(results)} ok)")

    logger.info(f"Analyzed {len(results)} pieces successfully")

    # === AGGREGATE PATTERNS ===
    print("\n" + "=" * 70)
    print("COMPOSITIONAL PATTERNS FROM CANONICAL REPERTOIRE")
    print("=" * 70)

    # 1. Dynamic placement
    print("\n## 1. WHERE DO DYNAMICS APPEAR?")
    dyn_quarters = [r["dyn_by_quarter"] for r in results if "dyn_by_quarter" in r]
    if dyn_quarters:
        avg_quarters = np.mean(dyn_quarters, axis=0)
        total = avg_quarters.sum()
        for i, (q, pct) in enumerate(zip(avg_quarters, avg_quarters / total * 100)):
            label = ["Opening quarter", "Second quarter", "Third quarter", "Final quarter"][i]
            print(f"  {label}: {pct:.1f}% of dynamics")

    dyn_first = [r["dyn_pct_first_10"] for r in results if "dyn_pct_first_10" in r]
    dyn_last = [r["dyn_pct_last_10"] for r in results if "dyn_pct_last_10" in r]
    if dyn_first:
        print(f"  First 10% of piece: {np.mean(dyn_first)*100:.1f}% of dynamics")
    if dyn_last:
        print(f"  Last 10% of piece: {np.mean(dyn_last)*100:.1f}% of dynamics")

    # 2. Dynamic trajectory
    print("\n## 2. DYNAMIC TRAJECTORY (first half vs second half)")
    trajectories = [r["dyn_trajectory"] for r in results if "dyn_trajectory" in r]
    if trajectories:
        for t in ["rising", "falling", "flat"]:
            pct = trajectories.count(t) / len(trajectories) * 100
            print(f"  {t}: {pct:.1f}%")

    max_positions = [r["dyn_max_position"] for r in results if "dyn_max_position" in r]
    if max_positions:
        print(f"  Loudest moment avg position: {np.mean(max_positions)*100:.1f}% through piece")
        print(f"  Loudest moment median position: {np.median(max_positions)*100:.1f}% through piece")

    # 3. Dynamics and pitch contour
    print("\n## 3. PITCH CONTOUR AT DYNAMIC CHANGES")
    for key, label in [("dyn_at_rising", "Rising pitch"), ("dyn_at_falling", "Falling pitch"), ("dyn_at_static", "Static pitch")]:
        vals = [r[key] for r in results if key in r]
        if vals:
            print(f"  {label}: {np.mean(vals)*100:.1f}% of dynamics")

    # 4. Crescendo vs diminuendo placement
    print("\n## 4. CRESCENDO vs DIMINUENDO PLACEMENT")
    cresc_pos = [r["cresc_avg_position"] for r in results if "cresc_avg_position" in r]
    dim_pos = [r["dim_avg_position"] for r in results if "dim_avg_position" in r]
    if cresc_pos:
        print(f"  Crescendo avg position: {np.mean(cresc_pos)*100:.1f}% through piece")
    if dim_pos:
        print(f"  Diminuendo avg position: {np.mean(dim_pos)*100:.1f}% through piece")

    cresc_counts = [r["crescendo_count"] for r in results if "crescendo_count" in r]
    dim_counts = [r["diminuendo_count"] for r in results if "diminuendo_count" in r]
    if cresc_counts and dim_counts:
        ratio = np.mean(cresc_counts) / max(np.mean(dim_counts), 0.01)
        print(f"  Crescendo:Diminuendo ratio: {ratio:.2f}:1")
        print(f"  Avg crescendos per piece: {np.mean(cresc_counts):.1f}")
        print(f"  Avg diminuendos per piece: {np.mean(dim_counts):.1f}")

    # 5. Staccato patterns
    print("\n## 5. STACCATO PATTERNS")
    clustering = [r["staccato_clustering"] for r in results if "staccato_clustering" in r]
    if clustering:
        print(f"  Staccato clustering: {np.mean(clustering)*100:.1f}% of staccatos near another staccato")

    stac_density = [r["staccato_avg_local_density"] for r in results if "staccato_avg_local_density" in r]
    if stac_density:
        print(f"  Avg local note density at staccato: {np.mean(stac_density):.1f} notes/8-beat window")

    # 6. Accents on strong beats
    print("\n## 6. ACCENT PLACEMENT")
    accent_strong = [r["accent_on_strong_beat_pct"] for r in results if "accent_on_strong_beat_pct" in r]
    if accent_strong:
        print(f"  Accents on strong beats: {np.mean(accent_strong)*100:.1f}%")

    # 7. Dynamics near phrase boundaries
    print("\n## 7. DYNAMICS AND PHRASE STRUCTURE")
    near_boundary = [r["dyn_near_phrase_boundary_pct"] for r in results if "dyn_near_phrase_boundary_pct" in r]
    if near_boundary:
        print(f"  Dynamics near phrase boundaries: {np.mean(near_boundary)*100:.1f}%")

    # 8. Expression text analysis
    print("\n## 8. COMMON EXPRESSION MARKINGS")
    all_texts = []
    for r in results:
        all_texts.extend(r.get("expression_texts", []))
    text_counts = Counter(t for t in all_texts if t.strip())
    print(f"  Total expression texts found: {len(all_texts)}")
    for text, count in text_counts.most_common(25):
        print(f"    '{text}': {count}")

    # 9. Dynamic range
    print("\n## 9. DYNAMIC RANGE")
    dyn_ranges = [r["dyn_range"] for r in results if "dyn_range" in r]
    if dyn_ranges:
        print(f"  Avg dynamic range: {np.mean(dyn_ranges):.3f} (volumeScalar)")
        print(f"  Median dynamic range: {np.median(dyn_ranges):.3f}")

    print("\n" + "=" * 70)
    print(f"Analysis based on {len(results)} richly annotated canonical pieces")
    print("=" * 70)


if __name__ == "__main__":
    main()
