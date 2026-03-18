"""Rebuild the feature profile using PDMX + MAESTRO data.

PDMX provides: all features (from MusicXML with explicit markings)
MAESTRO provides: all features (with expressive features inferred from velocity)

Both are treated as "high-quality" reference distributions.
MAESTRO pieces are competition performances — implicitly high quality.
"""

import argparse
import logging
import os

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Rebuild feature profile with MAESTRO data")
    parser.add_argument("--pdmx-features", default="features_v3.csv",
                        help="PDMX features CSV")
    parser.add_argument("--maestro-features", default="data/maestro/maestro_features.csv",
                        help="MAESTRO features CSV")
    parser.add_argument("--regressor-path", default="models/quality_regressor.joblib",
                        help="XGBoost regressor (for feature importance)")
    parser.add_argument("--pdmx-csv", default="PDMXDataset/PDMX.csv",
                        help="PDMX metadata CSV")
    parser.add_argument("--output", default="models/feature_profile_v2.joblib",
                        help="Output profile path")
    parser.add_argument("--compare", action="store_true",
                        help="Compare v1 and v2 profiles")
    args = parser.parse_args()

    from rachmaniclaude.classifier.profile import FeatureProfile

    # Build v2 profile with combined data
    profile = FeatureProfile()

    # First, fit normally on PDMX to get the base stats + importance
    logger.info("Fitting base profile on PDMX...")
    pdmx_stats = profile.fit(
        args.pdmx_features,
        args.regressor_path,
        pdmx_csv=args.pdmx_csv,
    )
    logger.info(f"PDMX: {pdmx_stats['n_high']} high, {pdmx_stats['n_low']} low")

    # Load MAESTRO features
    if not os.path.exists(args.maestro_features):
        logger.error(f"MAESTRO features not found: {args.maestro_features}")
        return

    maestro = pd.read_csv(args.maestro_features)
    logger.info(f"MAESTRO: {len(maestro)} pieces")

    # MAESTRO is MIDI-sourced. Only some features transfer cleanly:
    # - dynamics_count, hairpin_count: inferred from velocity (calibrated)
    # - All non-expressive features: melodic, harmonic, rhythmic, structural
    # Skip: staccato_count, accent_count, expression_count, articulation_count
    #   (MIDI can't reliably infer explicit notation markings for these)
    SKIP_FROM_MIDI = {
        "staccato_count", "accent_count", "expression_count",
        "articulation_count", "tempo_count",
    }

    # MAESTRO pieces are all high-quality (competition performances)
    # Merge them into the high_stats distributions
    merged_count = 0
    skipped = []
    for feat in profile.feature_names:
        if feat not in maestro.columns or feat not in profile.high_stats:
            continue
        if feat in SKIP_FROM_MIDI:
            skipped.append(feat)
            continue

        maestro_vals = maestro[feat].dropna().values
        if len(maestro_vals) == 0:
            continue

        # Combine with existing high-rated values
        existing_vals = profile.high_stats[feat].get("values")
        if existing_vals is not None and len(existing_vals) > 0:
            combined = np.concatenate([existing_vals, maestro_vals])
        else:
            combined = maestro_vals

        combined = np.sort(combined)
        profile.high_stats[feat] = {
            "p25": float(np.percentile(combined, 25)),
            "p50": float(np.percentile(combined, 50)),
            "p75": float(np.percentile(combined, 75)),
            "mean": float(combined.mean()),
            "std": float(combined.std()),
            "values": combined,
        }

        merged_count += 1

    logger.info(f"Combined profile: merged {merged_count} features from {len(maestro)} MAESTRO pieces")
    if skipped:
        logger.info(f"Skipped MIDI-unreliable features: {skipped}")

    # Save
    profile.save(args.output)
    logger.info(f"Saved to {args.output}")

    # Compare v1 and v2 if requested
    if args.compare and os.path.exists("models/feature_profile.joblib"):
        v1 = FeatureProfile.load("models/feature_profile.joblib")
        v2 = FeatureProfile.load(args.output)

        print("\n=== Profile Comparison: v1 (PDMX only) vs v2 (PDMX + MAESTRO) ===\n")
        print(f"{'Feature':<30} {'v1 median':>12} {'v2 median':>12} {'v1 p75':>10} {'v2 p75':>10} {'shift':>8}")
        print("-" * 82)

        for feat in v1.feature_names:
            if feat not in v1.high_stats or feat not in v2.high_stats:
                continue
            v1_med = v1.high_stats[feat]["p50"]
            v2_med = v2.high_stats[feat]["p50"]
            v1_p75 = v1.high_stats[feat]["p75"]
            v2_p75 = v2.high_stats[feat]["p75"]
            shift = v2_med - v1_med
            arrow = "+" if shift > 0 else ""
            print(f"{feat:<30} {v1_med:>12.2f} {v2_med:>12.2f} {v1_p75:>10.2f} {v2_p75:>10.2f} {arrow}{shift:>7.2f}")


if __name__ == "__main__":
    main()
