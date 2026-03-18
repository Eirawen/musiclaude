"""Build corpus-subset profiles for blind comparison experiment.

Creates profiles from different slices of canonical_features.csv:
- v3-lieder: Lieder + Orchestra only
- v3-dcml: DCML only
- v3-full already exists (all corpora)
"""

import logging
import os

import joblib
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def build_profile_from_df(df, feature_names, importances):
    """Build a FeatureProfile from a filtered DataFrame."""
    from rachmaniclaude.classifier.profile import FeatureProfile

    profile = FeatureProfile()
    profile.feature_names = feature_names
    profile.importances = importances

    for feat in feature_names:
        if feat not in df.columns:
            continue
        vals = df[feat].dropna().values
        if len(vals) == 0:
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
    return profile


def main():
    # Load canonical features
    df = pd.read_csv("data/canonical/canonical_features.csv")
    logger.info(f"Loaded {len(df)} canonical pieces")

    # Load feature names and importances from regressor
    reg_data = joblib.load("models/quality_regressor.joblib")
    feature_names = reg_data["metrics"]["feature_names"]
    importances = dict(zip(feature_names, reg_data["model"].feature_importances_))

    # Define subsets
    subsets = {
        "v3-lieder": df[df["corpus"].isin(["openscore-lieder", "openscore-orchestra"])],
        "v3-dcml": df[df["corpus"] == "dcml"],
    }

    for name, subset_df in subsets.items():
        logger.info(f"Building {name} from {len(subset_df)} pieces")
        profile = build_profile_from_df(subset_df, feature_names, importances)
        out_path = f"models/feature_profile_{name.replace('-', '_')}.joblib"
        profile.save(out_path)
        logger.info(f"  Saved to {out_path}")

        # Print key stats
        for feat in ["dynamics_count", "hairpin_count", "expression_count", "staccato_count"]:
            if feat in profile.high_stats:
                s = profile.high_stats[feat]
                print(f"  {name} {feat}: median={s['p50']:.0f}, p75={s['p75']:.0f}")


if __name__ == "__main__":
    main()
