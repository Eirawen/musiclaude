"""Build v3 feature profile from canonical MusicXML corpora.

Key difference from PDMX-based profiles:
- No rating split — ALL canonical pieces are high-quality reference music
- Feature importance still from XGBoost (trained on PDMX) — this tells us
  which features matter most for distinguishing quality
- High_stats come from canonical repertoire distributions
- Low_stats are left empty (no "low quality" reference needed)

Output: models/feature_profile_v3.joblib
"""

import argparse
import logging
import os

import joblib
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Build canonical feature profile")
    parser.add_argument("--canonical-features", default="data/canonical/canonical_features.csv",
                        help="Canonical corpus features CSV")
    parser.add_argument("--regressor-path", default="models/quality_regressor.joblib",
                        help="XGBoost regressor (for feature importance rankings)")
    parser.add_argument("--output", default="models/feature_profile_v3.joblib",
                        help="Output profile path")
    parser.add_argument("--compare", action="store_true",
                        help="Compare v1 and v3 profiles")
    args = parser.parse_args()

    from rachmaniclaude.classifier.profile import FeatureProfile

    # Load regressor for feature names and importance rankings
    if not os.path.exists(args.regressor_path):
        logger.error(f"Regressor not found: {args.regressor_path}")
        return
    reg_data = joblib.load(args.regressor_path)
    feature_names = reg_data["metrics"]["feature_names"]
    importances = dict(zip(feature_names, reg_data["model"].feature_importances_))

    # Load canonical features
    if not os.path.exists(args.canonical_features):
        logger.error(f"Features not found: {args.canonical_features}")
        return
    df = pd.read_csv(args.canonical_features)
    logger.info(f"Loaded {len(df)} canonical pieces")
    if "corpus" in df.columns:
        for corpus, group in df.groupby("corpus"):
            logger.info(f"  {corpus}: {len(group)} pieces")

    # Build profile — ALL canonical pieces are high-quality
    profile = FeatureProfile()
    profile.feature_names = feature_names
    profile.importances = importances

    matched = 0
    missing = []
    for feat in feature_names:
        if feat not in df.columns:
            missing.append(feat)
            continue

        vals = df[feat].dropna().values
        if len(vals) == 0:
            missing.append(feat)
            continue

        vals = np.sort(vals)
        profile.high_stats[feat] = {
            "p25": float(np.percentile(vals, 25)),
            "p50": float(np.percentile(vals, 50)),
            "p75": float(np.percentile(vals, 75)),
            "mean": float(vals.mean()),
            "std": float(vals.std()),
            "values": vals,
        }
        matched += 1

    if missing:
        logger.warning(f"Missing features: {missing}")
    logger.info(f"Built profile from {len(df)} pieces, {matched} features")

    # Save
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    profile.save(args.output)
    logger.info(f"Saved to {args.output}")

    # Print key stats
    print(f"\n=== Canonical Profile v3 ({len(df)} pieces) ===\n")
    print(f"{'Feature':<30} {'median':>10} {'p25':>10} {'p75':>10} {'importance':>10}")
    print("-" * 72)
    ranked = sorted(feature_names, key=lambda f: importances.get(f, 0), reverse=True)
    for feat in ranked:
        if feat in profile.high_stats:
            s = profile.high_stats[feat]
            imp = importances.get(feat, 0)
            print(f"{feat:<30} {s['p50']:>10.2f} {s['p25']:>10.2f} {s['p75']:>10.2f} {imp:>10.4f}")

    # Compare with v1 if requested
    if args.compare:
        v1_path = "models/feature_profile.joblib"
        if os.path.exists(v1_path):
            v1 = FeatureProfile.load(v1_path)
            v3 = FeatureProfile.load(args.output)

            print(f"\n=== Profile Comparison: v1 (PDMX rated) vs v3 (Canonical) ===\n")
            print(f"{'Feature':<30} {'v1 median':>12} {'v3 median':>12} {'shift':>10} {'v3 richer?':>10}")
            print("-" * 76)

            for feat in ranked:
                if feat not in v1.high_stats or feat not in v3.high_stats:
                    continue
                v1_med = v1.high_stats[feat]["p50"]
                v3_med = v3.high_stats[feat]["p50"]
                shift = v3_med - v1_med
                arrow = "+" if shift > 0.5 else ("-" if shift < -0.5 else "=")
                print(f"{feat:<30} {v1_med:>12.2f} {v3_med:>12.2f} {shift:>+10.2f} {arrow:>10}")
        else:
            logger.warning(f"v1 profile not found: {v1_path}")


if __name__ == "__main__":
    main()
