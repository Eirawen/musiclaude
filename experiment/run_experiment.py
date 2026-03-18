"""Run the blind A/B/C listening experiment.

For each song:
  A (baseline): Raw first draft, no feedback
  B (xgboost): Revised using XGBoost prediction-based feedback
  C (profile): Revised using percentile-based profile feedback

Then randomize filenames so the listener doesn't know which is which.
"""

import json
import logging
import os
import random
import shutil
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SONGS = ["waltz", "duet", "prelude"]
CONDITIONS = ["baseline", "xgboost", "profile"]
EXPERIMENT_DIR = os.path.dirname(os.path.abspath(__file__))
SONGS_DIR = os.path.join(EXPERIMENT_DIR, "songs")
BLIND_DIR = os.path.join(EXPERIMENT_DIR, "blind")


def extract_features(musicxml_path: str) -> dict | None:
    """Extract features from a MusicXML file."""
    from rachmaniclaude.features.extract import extract_features_from_file
    return extract_features_from_file(musicxml_path)


def get_xgboost_feedback(features: dict) -> str:
    """Get feedback using the old XGBoost prediction system."""
    from rachmaniclaude.classifier.predict import QualityPredictor

    predictor = QualityPredictor(
        "models/quality_classifier.joblib",
        "models/quality_regressor.joblib",
        "models/distribution_scorer.joblib",
    )
    quality = predictor.predict_from_features(features)
    critiques = predictor.get_feature_deficiencies(features)

    lines = []
    rating = quality.get("predicted_rating")
    if rating:
        lines.append(f"Predicted rating: {rating:.1f}/5.0")
    prob = quality.get("good_probability", 0)
    lines.append(f"Probability of 'good': {prob:.0%}")

    anomaly_report = quality.get("anomaly_report")
    if anomaly_report:
        if anomaly_report.is_anomalous:
            lines.append(f"ANOMALOUS (score: {anomaly_report.score:.2f})")
        lines.extend(anomaly_report.critiques)

    if critiques:
        lines.append("\nFeature deficiencies:")
        lines.extend(critiques)

    return "\n".join(lines)


def get_profile_feedback(features: dict) -> str:
    """Get feedback using the new percentile-based profile system."""
    from rachmaniclaude.classifier.profile import FeatureProfile

    profile = FeatureProfile.load("models/feature_profile.joblib")
    comparison = profile.compare(features)
    return profile.format_feedback(comparison)


def convert_to_mp3(musicxml_path: str, mp3_path: str) -> bool:
    """Convert MusicXML to MP3 using musescore3."""
    try:
        result = subprocess.run(
            ["musescore3", "-o", mp3_path, musicxml_path],
            capture_output=True, text=True, timeout=60
        )
        return os.path.exists(mp3_path)
    except Exception as e:
        logger.error(f"MP3 conversion failed: {e}")
        return False


def randomize_and_copy():
    """Copy all MP3s to blind/ with randomized numeric filenames."""
    os.makedirs(BLIND_DIR, exist_ok=True)

    # Collect all MP3 files with their metadata
    entries = []
    for song in SONGS:
        for condition in CONDITIONS:
            mp3_path = os.path.join(SONGS_DIR, song, condition, "score.mp3")
            if os.path.exists(mp3_path):
                entries.append({
                    "song": song,
                    "condition": condition,
                    "source": mp3_path,
                })

    # Shuffle
    random.seed(42)  # reproducible for the answer key
    random.shuffle(entries)

    # Copy with numeric names
    answer_key = {}
    for i, entry in enumerate(entries, 1):
        blind_name = f"{i:02d}.mp3"
        blind_path = os.path.join(BLIND_DIR, blind_name)
        shutil.copy2(entry["source"], blind_path)
        answer_key[blind_name] = {
            "song": entry["song"],
            "condition": entry["condition"],
        }
        logger.info(f"{blind_name} <- {entry['song']}/{entry['condition']}")

    # Save answer key (DON'T show to the user!)
    key_path = os.path.join(EXPERIMENT_DIR, ".answer_key.json")
    with open(key_path, "w") as f:
        json.dump(answer_key, f, indent=2)
    logger.info(f"Answer key saved to {key_path} (DO NOT SHOW TO USER)")

    return answer_key


def print_status():
    """Print current experiment status."""
    print("\n=== Experiment Status ===\n")
    for song in SONGS:
        print(f"Song: {song}")
        for condition in CONDITIONS:
            base_dir = os.path.join(SONGS_DIR, song, condition)
            xml_exists = os.path.exists(os.path.join(base_dir, "score.musicxml"))
            mp3_exists = os.path.exists(os.path.join(base_dir, "score.mp3"))
            feedback_exists = os.path.exists(os.path.join(base_dir, "feedback.txt"))
            status = []
            if xml_exists:
                status.append("XML")
            if feedback_exists:
                status.append("feedback")
            if mp3_exists:
                status.append("MP3")
            print(f"  {condition:>10}: {' + '.join(status) if status else 'pending'}")
        print()

    blind_files = sorted(f for f in os.listdir(BLIND_DIR) if f.endswith(".mp3")) if os.path.exists(BLIND_DIR) else []
    if blind_files:
        print(f"Blind test: {len(blind_files)} files ready in experiment/blind/")
    else:
        print("Blind test: not yet randomized")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print_status()
    elif len(sys.argv) > 1 and sys.argv[1] == "randomize":
        randomize_and_copy()
    elif len(sys.argv) > 1 and sys.argv[1] == "convert":
        # Convert all existing MusicXML to MP3
        for song in SONGS:
            for condition in CONDITIONS:
                xml = os.path.join(SONGS_DIR, song, condition, "score.musicxml")
                mp3 = os.path.join(SONGS_DIR, song, condition, "score.mp3")
                if os.path.exists(xml) and not os.path.exists(mp3):
                    logger.info(f"Converting {song}/{condition}...")
                    convert_to_mp3(xml, mp3)
    else:
        print("Usage: python run_experiment.py [status|randomize|convert]")
