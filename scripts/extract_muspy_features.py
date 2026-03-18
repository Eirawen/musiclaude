"""Extract scale_consistency and groove_consistency (MusPy-compatible) features
and merge them into an existing features CSV. Replaces PDMX metadata versions
with our own computed versions so models work on new compositions too."""

import argparse
import logging
import multiprocessing as mp

import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)


def extract_muspy_features(filepath: str) -> dict | None:
    """Extract scale_consistency and groove_consistency from a MusicXML file."""
    try:
        from music21 import converter
        score = converter.parse(filepath)

        features = {"filepath": filepath}

        # scale_consistency
        from rachmaniclaude.features.harmonic import _scale_consistency
        features["scale_consistency"] = _scale_consistency(score)

        # groove_consistency
        from rachmaniclaude.features.coherence import _groove_consistency
        features["groove_consistency"] = _groove_consistency(score)

        return features
    except Exception as e:
        return None


def _worker(filepath):
    import warnings
    warnings.filterwarnings("ignore")
    logging.disable(logging.WARNING)
    try:
        return extract_muspy_features(filepath)
    finally:
        logging.disable(logging.NOTSET)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features-csv", default="features_v2.csv")
    parser.add_argument("--output", default="features_v3.csv")
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    df = pd.read_csv(args.features_csv)

    # Drop PDMX-provided versions if present (we're replacing them)
    for col in ["scale_consistency", "groove_consistency", "complexity"]:
        if col in df.columns:
            logger.info(f"Dropping PDMX column: {col}")
            df = df.drop(columns=[col])

    filepaths = df["filepath"].tolist()
    logger.info(f"Extracting MusPy features for {len(filepaths)} files")

    n_workers = args.workers if args.workers > 0 else max(1, mp.cpu_count() - 1)

    if n_workers > 1:
        logger.info(f"Using {n_workers} workers")
        with mp.Pool(n_workers) as pool:
            results = list(tqdm(
                pool.imap_unordered(_worker, filepaths),
                total=len(filepaths),
                desc="MusPy features",
            ))
    else:
        results = [extract_muspy_features(f) for f in tqdm(filepaths)]

    results = [r for r in results if r is not None]
    new_df = pd.DataFrame(results)
    logger.info(f"Got MusPy features for {len(new_df)} files")

    merged = df.merge(new_df, on="filepath", how="left")
    merged.to_csv(args.output, index=False)
    logger.info(f"Saved to {args.output} ({len(merged)} rows, {len(merged.columns)} cols)")


if __name__ == "__main__":
    main()
