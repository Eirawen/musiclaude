"""Extract only the new structural features (hairpins, articulations, expressions)
and merge them into an existing features.csv. Much faster than full re-extraction."""

import argparse
import csv
import glob
import logging
import multiprocessing as mp
import os

import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)


def extract_new_features(filepath: str) -> dict | None:
    """Extract only the new performance directive features."""
    try:
        from music21 import converter, dynamics as dyn_module, expressions as expr_module

        score = converter.parse(filepath)

        features = {"filepath": filepath}

        # Hairpins
        hairpins = list(score.recurse().getElementsByClass(dyn_module.DynamicWedge))
        features["hairpin_count"] = len(hairpins)

        # Articulations from notes
        total_arts = 0
        staccato = 0
        accent = 0
        for note in score.flatten().notes:
            for a in note.articulations:
                total_arts += 1
                name = type(a).__name__
                if name in ("Staccato", "Staccatissimo"):
                    staccato += 1
                elif name in ("Accent", "StrongAccent"):
                    accent += 1
        features["articulation_count"] = total_arts
        features["staccato_count"] = staccato
        features["accent_count"] = accent

        # Expressions (excluding RehearsalMarks)
        exprs = list(score.flatten().getElementsByClass(expr_module.Expression))
        exprs = [e for e in exprs if type(e).__name__ != "RehearsalMark"]
        features["expression_count"] = len(exprs)

        return features
    except Exception as e:
        return None


def _worker(filepath):
    import warnings
    warnings.filterwarnings("ignore")
    logging.disable(logging.WARNING)
    try:
        return extract_new_features(filepath)
    finally:
        logging.disable(logging.NOTSET)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features-csv", default="features.csv")
    parser.add_argument("--output", default="features_v2.csv")
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    df = pd.read_csv(args.features_csv)
    filepaths = df["filepath"].tolist()
    logger.info(f"Extracting new features for {len(filepaths)} files")

    n_workers = args.workers if args.workers > 0 else max(1, mp.cpu_count() - 1)

    if n_workers > 1:
        logger.info(f"Using {n_workers} workers")
        with mp.Pool(n_workers) as pool:
            results = list(tqdm(
                pool.imap_unordered(_worker, filepaths),
                total=len(filepaths),
                desc="New features",
            ))
    else:
        results = [extract_new_features(f) for f in tqdm(filepaths)]

    results = [r for r in results if r is not None]
    new_df = pd.DataFrame(results)
    logger.info(f"Got new features for {len(new_df)} files")

    # Merge on filepath
    merged = df.merge(new_df, on="filepath", how="left")
    merged.to_csv(args.output, index=False)
    logger.info(f"Saved to {args.output} ({len(merged)} rows, {len(merged.columns)} cols)")


if __name__ == "__main__":
    main()
