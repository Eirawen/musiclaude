"""Extract features from MAESTRO MIDI files.

Uses the standard feature extractor + MIDI velocity inference
to build a feature dataset from competition piano performances.
"""

import argparse
import json
import logging
import os
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def extract_one(midi_path: str) -> dict | None:
    """Extract features from a single MIDI file."""
    try:
        from music21 import converter
        from musiclaude.features.extract import extract_features_from_score
        from musiclaude.features.midi_inference import infer_all

        score = converter.parse(midi_path)

        # Standard feature extraction
        features = extract_features_from_score(score, filepath=midi_path)
        if features is None:
            return None

        # MIDI velocity inference for expressive features
        inferred = infer_all(score)
        features.update(inferred)

        return features
    except Exception as e:
        logger.error(f"Failed {midi_path}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Extract features from MAESTRO MIDI files")
    parser.add_argument("--maestro-dir", default="data/maestro/maestro-v3.0.0",
                        help="Path to MAESTRO MIDI directory")
    parser.add_argument("--metadata", default="data/maestro/maestro-v3.0.0.csv",
                        help="Path to MAESTRO metadata CSV")
    parser.add_argument("--output", default="data/maestro/maestro_features.csv",
                        help="Output features CSV")
    parser.add_argument("--workers", type=int, default=4,
                        help="Number of parallel workers")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of files (0 = all)")
    args = parser.parse_args()

    # Find all MIDI files
    midi_dir = Path(args.maestro_dir)
    midi_files = sorted(midi_dir.rglob("*.midi"))
    logger.info(f"Found {len(midi_files)} MIDI files")

    if args.limit > 0:
        midi_files = midi_files[:args.limit]
        logger.info(f"Limited to {args.limit} files")

    # Extract features in parallel
    results = []
    failed = 0
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(extract_one, str(f)): f for f in midi_files}
        for i, future in enumerate(as_completed(futures), 1):
            path = futures[future]
            try:
                features = future.result(timeout=120)
                if features:
                    results.append(features)
                else:
                    failed += 1
                if i % 50 == 0:
                    logger.info(f"Progress: {i}/{len(midi_files)} ({len(results)} ok, {failed} failed)")
            except Exception as e:
                failed += 1
                logger.error(f"Timeout/error on {path}: {e}")

    logger.info(f"Done: {len(results)} succeeded, {failed} failed out of {len(midi_files)}")

    # Build DataFrame
    df = pd.DataFrame(results)

    # Join MAESTRO metadata if available
    if os.path.exists(args.metadata):
        meta = pd.read_csv(args.metadata)
        # Create join key from filename
        df["midi_basename"] = df["filepath"].apply(lambda x: os.path.basename(x))
        meta["midi_basename"] = meta["midi_filename"].apply(lambda x: os.path.basename(x))
        df = df.merge(
            meta[["midi_basename", "canonical_composer", "canonical_title", "split", "duration"]],
            on="midi_basename", how="left"
        )

    df.to_csv(args.output, index=False)
    logger.info(f"Saved {len(df)} rows to {args.output}")

    # Quick summary of inferred features
    for feat in ["dynamics_count", "hairpin_count", "staccato_count", "accent_count"]:
        if feat in df.columns:
            logger.info(f"  {feat}: mean={df[feat].mean():.1f}, median={df[feat].median():.0f}, "
                        f"min={df[feat].min()}, max={df[feat].max()}")


if __name__ == "__main__":
    main()
