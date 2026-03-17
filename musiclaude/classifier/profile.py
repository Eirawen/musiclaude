"""Feature profile: compare compositions against high-rated music distributions.

Instead of predicting ratings (R² = 0.039, useless), use the training data
as a reference distribution. For each feature, compute where a composition
sits relative to high-rated music and generate ranked improvement suggestions
weighted by feature importance.
"""

import json
import logging
import os
from dataclasses import dataclass, field

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Human-readable descriptions and improvement instructions for each feature.
# Keys: feature name → (description, what "improve" means, direction: "higher"/"lower"/None)
FEATURE_GUIDANCE = {
    "dynamics_count": (
        "dynamic markings (pp, p, mp, mf, f, ff)",
        "Add dynamic markings throughout the score. Place them at phrase beginnings and at emotional shifts.",
        "higher",
    ),
    "hairpin_count": (
        "crescendo/decrescendo wedges",
        "Add crescendo and decrescendo hairpins to shape phrases dynamically.",
        "higher",
    ),
    "articulation_count": (
        "note articulations (staccato, accent, tenuto, etc.)",
        "Add articulation markings to notes — staccato for short notes, accents for emphasis, tenuto for sustained.",
        "higher",
    ),
    "staccato_count": (
        "staccato markings",
        "Add staccato dots to short, detached notes — especially in rhythmic passages.",
        "higher",
    ),
    "accent_count": (
        "accent markings",
        "Add accents to emphasize important melodic notes and rhythmic downbeats.",
        "higher",
    ),
    "expression_count": (
        "expressions (fermatas, trills, ornaments)",
        "Add fermatas at phrase endings, trills on sustained notes, and ornaments for melodic interest.",
        "higher",
    ),
    "tempo_count": (
        "tempo markings",
        "Include at least one tempo marking. Add tempo changes for contrasting sections.",
        "higher",
    ),
    "scale_consistency": (
        "scale adherence (lower = more chromatic = better)",
        "Add chromatic passing tones, borrowed chords, or brief tonicizations. Don't stay strictly diatonic.",
        "lower",
    ),
    "melodic_range": (
        "pitch range in semitones",
        "Expand the melodic range — use higher and lower notes for more dramatic contour.",
        "higher",
    ),
    "pitch_class_entropy": (
        "pitch variety (Shannon entropy)",
        "Use more of the chromatic scale. Avoid over-relying on a few pitches.",
        "higher",
    ),
    "chord_vocabulary_size": (
        "unique chord types",
        "Use more varied chord qualities — add 7ths, suspended, diminished, augmented chords.",
        "higher",
    ),
    "pct_extended_chords": (
        "fraction of 7th/9th/extended chords",
        "Replace some triads with 7th chords, especially on dominant and secondary dominants.",
        "higher",
    ),
    "melodic_autocorrelation": (
        "melodic self-similarity (motific development)",
        "Develop motifs — repeat and vary melodic ideas rather than writing entirely new material each phrase.",
        "higher",
    ),
    "rest_ratio": (
        "rest proportion",
        "Add rests between phrases. Let the music breathe. Don't fill every beat with notes.",
        "higher",
    ),
    "note_density": (
        "notes per beat",
        "Vary note density — use running passages in some sections and longer notes in others.",
        None,  # not clearly directional
    ),
    "rhythmic_variety": (
        "unique note durations",
        "Use more varied rhythms — mix eighth notes, quarters, dotted rhythms, triplets.",
        "higher",
    ),
    "modulation_count": (
        "key changes",
        "Add key changes between sections — even a brief tonicization adds harmonic interest.",
        "higher",
    ),
    "phrase_length_regularity": (
        "phrase structure regularity",
        "Use regular phrase lengths (4 or 8 bars) with clear cadences at phrase boundaries.",
        "higher",
    ),
    "avg_range_utilization": (
        "instrument range usage",
        "Use more of each instrument's comfortable range instead of staying in a narrow register.",
        "higher",
    ),
    "groove_consistency": (
        "rhythmic groove consistency",
        "Keep a consistent rhythmic pattern within sections. Vary between sections, not within them.",
        "higher",
    ),
}


@dataclass
class FeatureGap:
    """A single feature's gap from the high-rated target."""
    feature: str
    current_value: float
    target_percentile_50: float
    target_percentile_75: float
    percentile_in_high: float  # where the current value sits in the high-rated distribution
    importance: float
    priority_score: float  # importance × gap severity
    direction: str  # "higher", "lower", or "ok"
    instruction: str  # human-readable improvement instruction


@dataclass
class ProfileComparison:
    """Full comparison of a composition against the high-rated profile."""
    gaps: list[FeatureGap]
    top_instructions: list[str]  # the actual feedback for Claude
    delta_report: str | None = None  # comparison to previous iteration


class FeatureProfile:
    """Reference profile built from high-rated music distributions."""

    def __init__(self):
        self.high_stats: dict = {}  # feature -> {p25, p50, p75, mean, std}
        self.low_stats: dict = {}
        self.importances: dict = {}
        self.feature_names: list[str] = []

    def fit(self, features_csv: str, regressor_path: str, pdmx_csv: str | None = None,
            min_ratings: int = 10) -> dict:
        """Build profile from training data + regressor importance."""
        df = pd.read_csv(features_csv)

        # Join ratings if needed
        if pdmx_csv or "rating" not in df.columns:
            if pdmx_csv is None:
                import pathlib
                for candidate in [
                    pathlib.Path(features_csv).parent / "PDMXDataset" / "PDMX.csv",
                    pathlib.Path("PDMXDataset") / "PDMX.csv",
                ]:
                    if candidate.exists():
                        pdmx_csv = str(candidate)
                        break

            if pdmx_csv:
                meta = pd.read_csv(pdmx_csv, usecols=["path", "rating", "n_ratings", "subset:rated_deduplicated"])
                df["basename"] = df["filepath"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
                meta["basename"] = meta["path"].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
                merge_cols = ["basename", "rating", "n_ratings", "subset:rated_deduplicated"]
                merge_cols = [c for c in merge_cols if c in meta.columns]
                df = df.merge(meta[merge_cols], on="basename", how="left", suffixes=("", "_m"))
                if "rating_m" in df.columns:
                    df["rating"] = df["rating_m"].fillna(df.get("rating"))
                if "n_ratings_m" in df.columns:
                    df["n_ratings"] = df["n_ratings_m"].fillna(df.get("n_ratings"))

        # Filter
        df = df[df["rating"] > 0]
        if "n_ratings" in df.columns:
            df = df[df["n_ratings"] >= min_ratings]
        dedup_col = "subset:rated_deduplicated"
        if dedup_col in df.columns and df[dedup_col].notna().any():
            df = df[df[dedup_col].fillna(True) == True]

        # Load importance
        reg_data = joblib.load(regressor_path)
        self.feature_names = reg_data["metrics"]["feature_names"]
        self.importances = dict(zip(self.feature_names, reg_data["model"].feature_importances_))

        # Split high/low
        threshold = df["rating"].median()
        high = df[df["rating"] >= threshold]
        low = df[df["rating"] < threshold]

        # Compute stats
        for feat in self.feature_names:
            if feat not in df.columns:
                continue
            h = high[feat].dropna()
            l = low[feat].dropna()
            if len(h) > 0:
                self.high_stats[feat] = {
                    "p25": float(np.percentile(h, 25)),
                    "p50": float(np.percentile(h, 50)),
                    "p75": float(np.percentile(h, 75)),
                    "mean": float(h.mean()),
                    "std": float(h.std()),
                    "values": np.sort(h.values),  # for percentile lookups
                }
            if len(l) > 0:
                self.low_stats[feat] = {
                    "p25": float(np.percentile(l, 25)),
                    "p50": float(np.percentile(l, 50)),
                    "p75": float(np.percentile(l, 75)),
                }

        return {
            "n_high": len(high),
            "n_low": len(low),
            "threshold": float(threshold),
            "n_features": len(self.feature_names),
        }

    def compare(self, features: dict, previous_features: dict | None = None) -> ProfileComparison:
        """Compare a composition's features against the high-rated profile."""
        gaps = []

        for feat in self.feature_names:
            if feat not in features or feat not in self.high_stats:
                continue

            value = features[feat]
            if value is None or (isinstance(value, float) and np.isnan(value)):
                continue

            stats = self.high_stats[feat]
            imp = self.importances.get(feat, 0)
            guidance = FEATURE_GUIDANCE.get(feat)

            # Compute percentile in high-rated distribution
            values_arr = stats.get("values")
            if values_arr is not None and len(values_arr) > 0:
                pctile = float(np.searchsorted(values_arr, value) / len(values_arr) * 100)
            else:
                pctile = 50.0

            # Determine direction and gap severity
            expected_direction = guidance[2] if guidance else None

            if expected_direction == "higher":
                # Gap = how far below the median are we?
                gap_severity = max(0, (stats["p50"] - value) / max(stats["std"], 0.001))
            elif expected_direction == "lower":
                # Gap = how far above the median are we?
                gap_severity = max(0, (value - stats["p50"]) / max(stats["std"], 0.001))
            else:
                gap_severity = 0

            priority = imp * gap_severity

            if expected_direction == "higher" and value < stats["p50"]:
                direction = "higher"
            elif expected_direction == "lower" and value > stats["p50"]:
                direction = "lower"
            else:
                direction = "ok"

            # Build instruction
            if guidance and direction != "ok":
                desc, instruction_template, _ = guidance
                instruction = (
                    f"**{feat}** = {_fmt(value)} (percentile {pctile:.0f} in high-rated music, "
                    f"target median: {_fmt(stats['p50'])}). {instruction_template}"
                )
            else:
                instruction = ""

            gaps.append(FeatureGap(
                feature=feat,
                current_value=value,
                target_percentile_50=stats["p50"],
                target_percentile_75=stats["p75"],
                percentile_in_high=pctile,
                importance=imp,
                priority_score=priority,
                direction=direction,
                instruction=instruction,
            ))

        # Sort by priority (importance × gap)
        gaps.sort(key=lambda g: g.priority_score, reverse=True)

        # Top instructions: only features that need improvement
        top = [g.instruction for g in gaps if g.direction != "ok" and g.instruction][:8]

        # Delta report if we have previous features
        delta_report = None
        if previous_features:
            delta_report = self._delta_report(features, previous_features)

        return ProfileComparison(gaps=gaps, top_instructions=top, delta_report=delta_report)

    def _delta_report(self, current: dict, previous: dict) -> str:
        """Show what changed between iterations."""
        lines = []
        improved = []
        regressed = []
        unchanged = []

        for feat in self.feature_names:
            if feat not in current or feat not in previous:
                continue
            cur = current.get(feat)
            prev = previous.get(feat)
            if cur is None or prev is None:
                continue
            if isinstance(cur, str) or isinstance(prev, str):
                continue

            guidance = FEATURE_GUIDANCE.get(feat)
            expected_dir = guidance[2] if guidance else None

            delta = cur - prev
            if abs(delta) < 0.001:
                unchanged.append(feat)
                continue

            if expected_dir == "higher":
                is_improvement = delta > 0
            elif expected_dir == "lower":
                is_improvement = delta < 0
            else:
                is_improvement = None

            entry = f"{feat}: {_fmt(prev)} → {_fmt(cur)} ({'+' if delta > 0 else ''}{_fmt(delta)})"
            if is_improvement:
                improved.append(entry)
            elif is_improvement is False:
                regressed.append(entry)

        if improved:
            lines.append("**Improved:**")
            for e in improved[:6]:
                lines.append(f"  + {e}")
        if regressed:
            lines.append("**Regressed:**")
            for e in regressed[:4]:
                lines.append(f"  - {e}")
        if not improved and not regressed:
            lines.append("No significant changes detected.")

        return "\n".join(lines)

    def save(self, path: str):
        """Save profile including raw value arrays for percentile lookups."""
        data = {
            "importances": self.importances,
            "feature_names": self.feature_names,
            "high_stats": self.high_stats,
            "low_stats": self.low_stats,
        }
        joblib.dump(data, path)

    @classmethod
    def load(cls, path: str) -> "FeatureProfile":
        data = joblib.load(path)
        profile = cls()
        profile.importances = data["importances"]
        profile.feature_names = data["feature_names"]
        profile.high_stats = data["high_stats"]
        profile.low_stats = data["low_stats"]
        return profile

    def format_feedback(self, comparison: ProfileComparison) -> str:
        """Format comparison into LLM-readable feedback."""
        lines = []

        if comparison.delta_report:
            lines.append(comparison.delta_report)
            lines.append("")

        if comparison.top_instructions:
            lines.append("**Priority improvements** (ranked by impact):")
            lines.append("")
            for i, inst in enumerate(comparison.top_instructions, 1):
                lines.append(f"{i}. {inst}")
        else:
            lines.append("All features are within the high-rated range. Composition looks good.")

        # Summary stats
        n_ok = sum(1 for g in comparison.gaps if g.direction == "ok")
        n_total = len(comparison.gaps)
        lines.append(f"\n{n_ok}/{n_total} features at or above high-rated median.")

        return "\n".join(lines)


def _fmt(v) -> str:
    """Format a feature value for display."""
    if isinstance(v, float):
        if abs(v) >= 10:
            return f"{v:.1f}"
        elif abs(v) >= 1:
            return f"{v:.2f}"
        else:
            return f"{v:.3f}"
    return str(v)
