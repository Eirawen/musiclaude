"""Extract features from canonical MusicXML corpora.

Processes OpenScore Lieder, Orchestra, Quartets (if mxl available), and DCML
corpora. All pieces are treated as definitionally high-quality reference music.

Output: data/canonical/canonical_features.csv
"""

import argparse
import csv
import logging
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def extract_one(filepath: str) -> dict | None:
    """Extract features from a single MusicXML file."""
    try:
        import warnings
        warnings.filterwarnings("ignore")
        logging.disable(logging.WARNING)

        from music21 import converter
        from rachmaniclaude.features.extract import extract_features_from_score

        score = converter.parse(filepath)
        features = extract_features_from_score(score, filepath=filepath)
        return features
    except Exception as e:
        logging.disable(logging.NOTSET)
        logger.error(f"Failed {filepath}: {e}")
        return None
    finally:
        logging.disable(logging.NOTSET)


def find_mxl_files(data_dir: str) -> list[str]:
    """Find all MusicXML files across canonical corpora."""
    corpora = {
        "openscore-lieder": "**/*.mxl",
        "openscore-orchestra": "**/*.mxl",
        "openscore-quartets": "**/*.mxl",  # if converted
        "dcml": "**/*.mxl",  # if converted
    }

    files = []
    for corpus, pattern in corpora.items():
        corpus_dir = Path(data_dir) / corpus
        if not corpus_dir.exists():
            logger.warning(f"Corpus not found: {corpus_dir}")
            continue

        corpus_files = sorted(corpus_dir.rglob("*.mxl"))
        # Also grab .musicxml and .xml (but not metadata xml)
        corpus_files += sorted(corpus_dir.rglob("*.musicxml"))

        logger.info(f"  {corpus}: {len(corpus_files)} files")
        for f in corpus_files:
            files.append((str(f), corpus))

    return files


def main():
    parser = argparse.ArgumentParser(description="Extract features from canonical MusicXML corpora")
    parser.add_argument("--data-dir", default="data",
                        help="Base data directory containing corpus subdirs")
    parser.add_argument("--output", default="data/canonical/canonical_features.csv",
                        help="Output features CSV")
    parser.add_argument("--workers", type=int, default=4,
                        help="Number of parallel workers")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit total files (0 = all)")
    parser.add_argument("--checkpoint-interval", type=int, default=100,
                        help="Flush results every N files")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Find all MusicXML files
    logger.info("Scanning for MusicXML files...")
    file_tuples = find_mxl_files(args.data_dir)
    logger.info(f"Found {len(file_tuples)} total MusicXML files")

    if args.limit > 0:
        file_tuples = file_tuples[:args.limit]
        logger.info(f"Limited to {args.limit} files")

    # Resume from checkpoint
    done_files = set()
    if os.path.exists(args.output):
        existing = pd.read_csv(args.output)
        done_files = set(existing["filepath"].tolist())
        logger.info(f"Resuming: {len(done_files)} already done")

    remaining = [(fp, corpus) for fp, corpus in file_tuples if fp not in done_files]
    logger.info(f"{len(remaining)} files to process")

    if not remaining:
        logger.info("All files already processed")
        return

    # Extract features in parallel
    filepaths = [fp for fp, _ in remaining]
    corpus_map = {fp: corpus for fp, corpus in remaining}

    results = []
    failed = 0
    csv_file = None
    csv_writer = None

    try:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(extract_one, fp): fp for fp in filepaths}
            for i, future in enumerate(as_completed(futures), 1):
                path = futures[future]
                try:
                    features = future.result(timeout=300)
                    if features:
                        features["corpus"] = corpus_map[path]
                        results.append(features)
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
                    logger.error(f"Error on {path}: {e}")

                if i % 25 == 0:
                    logger.info(f"Progress: {i}/{len(filepaths)} ({len(results)} ok, {failed} failed)")

                # Checkpoint
                if len(results) >= args.checkpoint_interval:
                    _flush(results, args.output, done_files)
                    done_files.update(r["filepath"] for r in results)
                    results = []

        # Final flush
        if results:
            _flush(results, args.output, done_files)
    except KeyboardInterrupt:
        logger.info("Interrupted — flushing remaining results")
        if results:
            _flush(results, args.output, done_files)

    # Final stats
    if os.path.exists(args.output):
        final_df = pd.read_csv(args.output)
        logger.info(f"Done: {len(final_df)} total rows in {args.output}")
        if "corpus" in final_df.columns:
            for corpus, group in final_df.groupby("corpus"):
                logger.info(f"  {corpus}: {len(group)} pieces")
    else:
        logger.info(f"Done: {len(results)} succeeded, {failed} failed")


def _flush(results: list[dict], output_path: str, done_files: set):
    """Append results to CSV."""
    if not results:
        return

    df_new = pd.DataFrame(results)
    if os.path.exists(output_path):
        df_existing = pd.read_csv(output_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(output_path, index=False)
    logger.info(f"Checkpoint: flushed {len(results)} results ({len(df_combined)} total)")


if __name__ == "__main__":
    main()
