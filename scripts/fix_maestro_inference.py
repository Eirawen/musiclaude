"""Re-compute dynamics_count and hairpin_count with calibrated inference.

Run after extract_maestro_features.py completes — the initial extraction
used note-level inference which produces inflated values. This script
re-runs the window-based inference and updates just those two columns.
"""

import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def reinfer_one(midi_path: str) -> dict | None:
    """Re-run calibrated inference on one MIDI file."""
    try:
        from music21 import converter
        from musiclaude.features.midi_inference import infer_all

        score = converter.parse(midi_path)
        result = infer_all(score)
        result["filepath"] = midi_path
        return result
    except Exception as e:
        logger.error(f"Failed {midi_path}: {e}")
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/maestro/maestro_features.csv")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    logger.info(f"Loaded {len(df)} rows from {args.input}")

    # Re-infer for all filepaths
    filepaths = df["filepath"].tolist()
    results = {}
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(reinfer_one, fp): fp for fp in filepaths}
        for i, future in enumerate(as_completed(futures), 1):
            r = future.result(timeout=120)
            if r:
                results[r["filepath"]] = r
            if i % 50 == 0:
                logger.info(f"Progress: {i}/{len(filepaths)}")

    # Update columns
    old_dyn = df["dynamics_count"].copy()
    old_hair = df["hairpin_count"].copy()

    for idx, row in df.iterrows():
        fp = row["filepath"]
        if fp in results:
            df.at[idx, "dynamics_count"] = results[fp]["dynamics_count"]
            df.at[idx, "hairpin_count"] = results[fp]["hairpin_count"]

    # Remove old inference columns if present
    for col in ["staccato_count", "accent_count", "expression_count"]:
        if col in df.columns:
            # Keep the standard extractor values (which will be 0 for MIDI)
            pass  # They're already there from the standard extractor

    df.to_csv(args.input, index=False)
    logger.info(f"Updated {len(results)} rows in {args.input}")

    # Show the diff
    logger.info(f"dynamics_count: old mean={old_dyn.mean():.1f} -> new mean={df['dynamics_count'].mean():.1f}")
    logger.info(f"hairpin_count: old mean={old_hair.mean():.1f} -> new mean={df['hairpin_count'].mean():.1f}")


if __name__ == "__main__":
    main()
