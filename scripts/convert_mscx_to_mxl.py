"""Batch convert .mscx files to .mxl using musescore3 with version downgrade hack.

MuseScore 3.6.2 files can't be read by musescore3 3.2.3 due to version check.
We patch the XML version header before conversion, then clean up.
"""

import argparse
import logging
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def convert_one(args_tuple: tuple) -> tuple[str, bool, str]:
    """Convert a single mscx file to mxl. Returns (path, success, error)."""
    mscx_path, output_dir = args_tuple
    try:
        # Read and patch the version
        with open(mscx_path, "r", encoding="utf-8") as f:
            content = f.read()

        patched = content.replace(
            '<museScore version="3.02">', '<museScore version="3.01">'
        ).replace(
            "<programVersion>3.6.2</programVersion>",
            "<programVersion>3.2.3</programVersion>",
        )

        # Write patched file to temp
        with tempfile.NamedTemporaryFile(suffix=".mscx", delete=False, mode="w") as tmp:
            tmp.write(patched)
            tmp_path = tmp.name

        # Determine output path (preserve relative structure)
        rel = os.path.relpath(mscx_path, start="data")
        out_path = os.path.join(output_dir, os.path.splitext(rel)[0] + ".mxl")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # Convert
        result = subprocess.run(
            ["musescore3", "-o", out_path, tmp_path],
            capture_output=True, text=True, timeout=120
        )

        os.unlink(tmp_path)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return (mscx_path, True, "")
        else:
            return (mscx_path, False, result.stderr[:200])
    except Exception as e:
        return (mscx_path, False, str(e)[:200])


def main():
    parser = argparse.ArgumentParser(description="Convert mscx files to mxl")
    parser.add_argument("--data-dir", default="data",
                        help="Base data directory")
    parser.add_argument("--workers", type=int, default=2,
                        help="Parallel workers (musescore3 is heavy, keep low)")
    args = parser.parse_args()

    # Find all mscx files
    mscx_files = []
    for corpus in ["dcml", "openscore-quartets"]:
        corpus_dir = Path(args.data_dir) / corpus
        if corpus_dir.exists():
            files = sorted(corpus_dir.rglob("*.mscx"))
            logger.info(f"{corpus}: {len(files)} mscx files")
            mscx_files.extend(files)

    if not mscx_files:
        logger.error("No mscx files found")
        return

    # Check which are already converted
    remaining = []
    for f in mscx_files:
        rel = os.path.relpath(f, start="data")
        out_path = os.path.join("data", os.path.splitext(rel)[0] + ".mxl")
        if not os.path.exists(out_path):
            remaining.append(str(f))

    logger.info(f"Total: {len(mscx_files)}, already converted: {len(mscx_files) - len(remaining)}, remaining: {len(remaining)}")

    if not remaining:
        logger.info("All files already converted")
        return

    # Convert in parallel
    tasks = [(fp, "data") for fp in remaining]
    success = 0
    failed = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(convert_one, t): t[0] for t in tasks}
        for i, future in enumerate(as_completed(futures), 1):
            path, ok, err = future.result()
            if ok:
                success += 1
            else:
                failed += 1
                if failed <= 10:
                    logger.error(f"Failed {path}: {err}")
            if i % 50 == 0:
                logger.info(f"Progress: {i}/{len(remaining)} ({success} ok, {failed} failed)")

    logger.info(f"Done: {success} converted, {failed} failed")


if __name__ == "__main__":
    main()
