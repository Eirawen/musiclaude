"""Feature extraction pipeline for MusicXML files."""

import argparse
import csv
import glob
import os
import logging
import multiprocessing as mp

import pandas as pd
from music21 import converter
from tqdm import tqdm

from musiclaude.features.harmonic import extract_harmonic_features
from musiclaude.features.melodic import extract_melodic_features
from musiclaude.features.structural import extract_structural_features
from musiclaude.features.orchestration import extract_orchestration_features
from musiclaude.features.coherence import extract_coherence_features

logger = logging.getLogger(__name__)


def extract_features_from_score(score, filepath: str = "") -> dict | None:
    """Extract all features from a pre-parsed music21 Score object."""
    try:
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


def extract_features_from_file(filepath: str) -> dict | None:
    """Extract all features from a single MusicXML file."""
    try:
        score = converter.parse(filepath)
        return extract_features_from_score(score, filepath=filepath)
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
    target_basenames: set[str] | None = None,
    checkpoint_path: str | None = None,
    checkpoint_interval: int = 500,
) -> pd.DataFrame:
    """Extract features from all MusicXML files in a directory.

    Args:
        data_dir: Directory containing MusicXML files
        pdmx_csv: Optional path to PDMX.csv for joining ratings
        n_workers: Number of parallel workers (1=sequential, 0=auto)
        target_basenames: If set, only extract these files (by stem name)
        checkpoint_path: If set, incrementally write results to this CSV
        checkpoint_interval: Flush checkpoint every N results
    """
    mxl_files = glob.glob(os.path.join(data_dir, "**/*.mxl"), recursive=True)
    mxl_files += glob.glob(os.path.join(data_dir, "**/*.musicxml"), recursive=True)
    mxl_files += glob.glob(os.path.join(data_dir, "**/*.xml"), recursive=True)

    if not mxl_files:
        logger.warning(f"No MusicXML files found in {data_dir}")
        return pd.DataFrame()

    # Filter to target basenames if provided
    if target_basenames:
        mxl_files = [
            f for f in mxl_files
            if os.path.splitext(os.path.basename(f))[0] in target_basenames
        ]
        logger.info(f"Filtered to {len(mxl_files)} target files (from {len(target_basenames)} requested)")

    # Resume from checkpoint if it exists
    done_basenames = set()
    if checkpoint_path and os.path.exists(checkpoint_path):
        existing = pd.read_csv(checkpoint_path)
        done_basenames = set(
            existing["filepath"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
        )
        mxl_files = [
            f for f in mxl_files
            if os.path.splitext(os.path.basename(f))[0] not in done_basenames
        ]
        logger.info(f"Resuming: {len(done_basenames)} already done, {len(mxl_files)} remaining")

    if not mxl_files:
        logger.info("All files already processed")
        if checkpoint_path:
            return pd.read_csv(checkpoint_path)
        return pd.DataFrame()

    logger.info(f"Extracting features from {len(mxl_files)} MusicXML files")

    if n_workers == 0:
        n_workers = max(1, mp.cpu_count() - 1)

    # Set up incremental CSV writer
    csv_writer = None
    csv_file = None
    fieldnames = None
    results_buffer = []

    def _flush_results(results_to_write):
        nonlocal csv_writer, csv_file, fieldnames
        if not results_to_write or not checkpoint_path:
            return
        if csv_writer is None:
            fieldnames = list(results_to_write[0].keys())
            file_exists = os.path.exists(checkpoint_path) and len(done_basenames) > 0
            csv_file = open(checkpoint_path, "a", newline="")
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                csv_writer.writeheader()
        for r in results_to_write:
            csv_writer.writerow(r)
        csv_file.flush()

    try:
        if n_workers > 1 and len(mxl_files) > 10:
            logger.info(f"Using {n_workers} parallel workers for feature extraction")
            with mp.Pool(n_workers) as pool:
                for result in tqdm(
                    pool.imap_unordered(_worker_extract, mxl_files),
                    total=len(mxl_files),
                    desc="Extracting features",
                ):
                    if result is not None:
                        results_buffer.append(result)
                        if len(results_buffer) >= checkpoint_interval:
                            _flush_results(results_buffer)
                            results_buffer = []
        else:
            for filepath in tqdm(mxl_files, desc="Extracting features"):
                result = extract_features_from_file(filepath)
                if result is not None:
                    results_buffer.append(result)
                    if len(results_buffer) >= checkpoint_interval:
                        _flush_results(results_buffer)
                        results_buffer = []

        # Flush remaining
        _flush_results(results_buffer)
    finally:
        if csv_file:
            csv_file.close()

    # Load full results (checkpoint + new)
    if checkpoint_path and os.path.exists(checkpoint_path):
        df = pd.read_csv(checkpoint_path)
    else:
        all_results = results_buffer  # non-checkpoint mode
        df = pd.DataFrame(all_results)

    if pdmx_csv and os.path.exists(pdmx_csv) and len(df) > 0:
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
    parser.add_argument(
        "--file-list", default=None,
        help="Text file with target basenames (one per line), extracts only these"
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    target_basenames = None
    if args.file_list:
        with open(args.file_list) as f:
            target_basenames = {line.strip() for line in f if line.strip()}
        logger.info(f"Loaded {len(target_basenames)} target basenames from {args.file_list}")

    df = extract_features_from_directory(
        args.data_dir,
        args.pdmx_csv,
        n_workers=args.workers,
        target_basenames=target_basenames,
        checkpoint_path=args.output,
    )

    df.to_csv(args.output, index=False)
    logger.info(f"Saved {len(df)} feature rows to {args.output}")


if __name__ == "__main__":
    main()
