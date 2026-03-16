"""Feature extraction pipeline for MusicXML files."""

import argparse
import glob
import os
import logging
import multiprocessing as mp
from functools import partial

import pandas as pd
from music21 import converter
from tqdm import tqdm

from musiclaude.features.harmonic import extract_harmonic_features
from musiclaude.features.melodic import extract_melodic_features
from musiclaude.features.structural import extract_structural_features
from musiclaude.features.orchestration import extract_orchestration_features
from musiclaude.features.coherence import extract_coherence_features

logger = logging.getLogger(__name__)


def extract_features_from_file(filepath: str) -> dict | None:
    """Extract all features from a single MusicXML file."""
    try:
        score = converter.parse(filepath)
        features = {"filepath": filepath}
        features.update(extract_harmonic_features(score))
        features.update(extract_melodic_features(score))
        features.update(extract_structural_features(score))
        features.update(extract_orchestration_features(score))
        features.update(extract_coherence_features(score))
        return features
    except Exception as e:
        logger.warning(f"Failed to extract features from {filepath}: {e}")
        return None


def _worker_extract(filepath: str) -> dict | None:
    """Wrapper for multiprocessing — suppresses music21 logging in workers."""
    import warnings
    warnings.filterwarnings("ignore")
    logging.disable(logging.WARNING)
    try:
        return extract_features_from_file(filepath)
    finally:
        logging.disable(logging.NOTSET)


def extract_features_from_directory(
    data_dir: str,
    pdmx_csv: str | None = None,
    n_workers: int = 1,
) -> pd.DataFrame:
    """Extract features from all MusicXML files in a directory.

    Args:
        data_dir: Directory containing MusicXML files
        pdmx_csv: Optional path to PDMX.csv for joining ratings
        n_workers: Number of parallel workers (1=sequential, 0=auto)
    """
    mxl_files = glob.glob(os.path.join(data_dir, "**/*.mxl"), recursive=True)
    mxl_files += glob.glob(os.path.join(data_dir, "**/*.musicxml"), recursive=True)
    mxl_files += glob.glob(os.path.join(data_dir, "**/*.xml"), recursive=True)

    if not mxl_files:
        logger.warning(f"No MusicXML files found in {data_dir}")
        return pd.DataFrame()

    logger.info(f"Found {len(mxl_files)} MusicXML files")

    if n_workers == 0:
        n_workers = max(1, mp.cpu_count() - 1)

    if n_workers > 1 and len(mxl_files) > 10:
        logger.info(f"Using {n_workers} parallel workers for feature extraction")
        with mp.Pool(n_workers) as pool:
            results = list(tqdm(
                pool.imap_unordered(_worker_extract, mxl_files),
                total=len(mxl_files),
                desc="Extracting features",
            ))
    else:
        results = []
        for filepath in tqdm(mxl_files, desc="Extracting features"):
            results.append(extract_features_from_file(filepath))

    # Filter None results (failed extractions)
    results = [r for r in results if r is not None]

    df = pd.DataFrame(results)

    if pdmx_csv and os.path.exists(pdmx_csv):
        metadata = pd.read_csv(pdmx_csv)
        # Join on filename stem matching
        df["basename"] = df["filepath"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
        if "path" in metadata.columns:
            metadata["basename"] = metadata["path"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
            df = df.merge(metadata[["basename", "rating", "n_ratings"]], on="basename", how="left")
            df = df.drop(columns=["basename"])

    return df


def main():
    """Entry point for musiclaude-extract command."""
    parser = argparse.ArgumentParser(description="Extract musical features from MusicXML files")
    parser.add_argument("--data-dir", required=True, help="Directory containing MusicXML files")
    parser.add_argument("--pdmx-csv", default=None, help="Path to PDMX.csv for ratings")
    parser.add_argument("--output", default="features.csv", help="Output CSV path")
    parser.add_argument(
        "--workers", type=int, default=0,
        help="Number of parallel workers (0=auto, 1=sequential)"
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    df = extract_features_from_directory(args.data_dir, args.pdmx_csv, n_workers=args.workers)

    df.to_csv(args.output, index=False)
    logger.info(f"Saved {len(df)} feature rows to {args.output}")


if __name__ == "__main__":
    main()
