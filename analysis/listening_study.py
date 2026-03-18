"""Rachmaniclaude 3-Axis Listening Study — Streamlit app for validating the classifier.

Based on the PDMX listening study design (arXiv:2409.10831). Each trial presents
a single audio clip rated on three axes: Correctness, Richness, Overall Quality.

Run:
    streamlit run analysis/listening_study.py                  # listener mode
    streamlit run analysis/listening_study.py -- --admin       # admin/analysis mode

Or toggle via sidebar in the app itself.
"""

import streamlit as st
import json
import os
import random
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Study configuration — edit these clips before running the study
# ---------------------------------------------------------------------------

# Each entry: (clip_path, metadata_dict)
# metadata_dict should contain at minimum the classifier score for the clip.
STUDY_CLIPS = [
    (
        "output/study/clip_01.mp3",
        {"clip_id": "clip_01", "classifier_score": 4.2, "anomaly_score": 0.12, "genre": "classical"},
    ),
    (
        "output/study/clip_02.mp3",
        {"clip_id": "clip_02", "classifier_score": 2.1, "anomaly_score": 0.65, "genre": "classical"},
    ),
    (
        "output/study/clip_03.mp3",
        {"clip_id": "clip_03", "classifier_score": 4.5, "anomaly_score": 0.08, "genre": "jazz"},
    ),
    (
        "output/study/clip_04.mp3",
        {"clip_id": "clip_04", "classifier_score": 3.0, "anomaly_score": 0.41, "genre": "jazz"},
    ),
    (
        "output/study/clip_05.mp3",
        {"clip_id": "clip_05", "classifier_score": 3.8, "anomaly_score": 0.22, "genre": "romantic"},
    ),
    (
        "output/study/clip_06.mp3",
        {"clip_id": "clip_06", "classifier_score": 1.5, "anomaly_score": 0.78, "genre": "romantic"},
    ),
    (
        "output/study/clip_07.mp3",
        {"clip_id": "clip_07", "classifier_score": 4.0, "anomaly_score": 0.15, "genre": "pop"},
    ),
    (
        "output/study/clip_08.mp3",
        {"clip_id": "clip_08", "classifier_score": 2.8, "anomaly_score": 0.50, "genre": "pop"},
    ),
    (
        "output/study/clip_09.mp3",
        {"clip_id": "clip_09", "classifier_score": 4.7, "anomaly_score": 0.05, "genre": "classical"},
    ),
    (
        "output/study/clip_10.mp3",
        {"clip_id": "clip_10", "classifier_score": 3.5, "anomaly_score": 0.33, "genre": "classical"},
    ),
    (
        "output/study/clip_11.mp3",
        {"clip_id": "clip_11", "classifier_score": 3.9, "anomaly_score": 0.18, "genre": "baroque"},
    ),
    (
        "output/study/clip_12.mp3",
        {"clip_id": "clip_12", "classifier_score": 1.8, "anomaly_score": 0.72, "genre": "baroque"},
    ),
    (
        "output/study/clip_13.mp3",
        {"clip_id": "clip_13", "classifier_score": 4.3, "anomaly_score": 0.10, "genre": "folk"},
    ),
    (
        "output/study/clip_14.mp3",
        {"clip_id": "clip_14", "classifier_score": 2.5, "anomaly_score": 0.55, "genre": "folk"},
    ),
    (
        "output/study/clip_15.mp3",
        {"clip_id": "clip_15", "classifier_score": 3.6, "anomaly_score": 0.28, "genre": "classical"},
    ),
]

NUM_TRIALS = len(STUDY_CLIPS)

AXES = ["correctness", "richness", "quality"]
AXIS_LABELS = {
    "correctness": "Correctness",
    "richness": "Richness",
    "quality": "Overall Quality",
}
AXIS_DESCRIPTIONS = {
    "correctness": "Is the music free of inharmonious notes, unnatural rhythms, and awkward phrasing?",
    "richness": "Is the sample musically and harmonically interesting?",
    "quality": "How would you rate this piece overall?",
}

RESULTS_PATH = Path(__file__).parent / "study_results.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_results() -> list[dict]:
    """Load all study results from disk."""
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, "r") as f:
            return json.load(f)
    return []


def save_result(entry: dict) -> None:
    """Append a single result entry and write back to disk."""
    results = load_results()
    results.append(entry)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)


def build_trial_order(seed: int) -> list[dict]:
    """Build a randomized trial order for a participant.

    Shuffles clip presentation order using a deterministic seed.

    Returns a list of dicts with keys:
        clip_index, clip_path, metadata
    """
    rng = random.Random(seed)
    indices = list(range(NUM_TRIALS))
    rng.shuffle(indices)

    trials = []
    for idx in indices:
        clip_path, meta = STUDY_CLIPS[idx]
        trials.append({
            "clip_index": idx,
            "clip_path": clip_path,
            "metadata": meta,
        })
    return trials


def participant_seed(participant_id: str) -> int:
    """Derive a deterministic seed from participant ID for reproducible ordering."""
    return hash(participant_id) & 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Rachmaniclaude Listening Study",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Mode selection: listener vs admin
# ---------------------------------------------------------------------------

query_params = st.query_params
is_admin = query_params.get("admin", "false").lower() == "true"

if not is_admin:
    show_admin = st.sidebar.checkbox("Admin view", value=False)
    if show_admin:
        is_admin = True

# =========================================================================
# ADMIN VIEW
# =========================================================================

if is_admin:
    st.title("Listening Study — Admin Dashboard")

    results = load_results()

    if not results:
        st.info("No responses collected yet.")
        st.stop()

    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    from scipy import stats as scipy_stats

    BLUE = "#4C72B0"
    GREEN = "#55A868"
    RED = "#C44E52"
    PURPLE = "#8172B3"
    ORANGE = "#DD8452"

    rdf = pd.DataFrame(results)

    # --- Overview metrics ---
    st.subheader("Overview")
    n_participants = rdf["participant_id"].nunique()
    n_responses = len(rdf)
    n_complete = 0
    for pid, group in rdf.groupby("participant_id"):
        if len(group) >= NUM_TRIALS:
            n_complete += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Total responses", f"{n_responses:,}")
    col2.metric("Unique participants", f"{n_participants:,}")
    col3.metric("Completed full study", f"{n_complete:,}")

    # --- Per-clip average scores ---
    st.subheader("Per-Clip Average Scores")

    clip_stats = []
    for clip_path, meta in STUDY_CLIPS:
        clip_id = meta["clip_id"]
        clip_responses = rdf[rdf["trial_id"] == clip_id]
        row = {
            "Clip": clip_id,
            "Genre": meta.get("genre", ""),
            "Classifier Score": meta["classifier_score"],
            "Anomaly Score": meta.get("anomaly_score", ""),
            "N": len(clip_responses),
        }
        for axis in AXES:
            if not clip_responses.empty and axis in clip_responses.columns:
                row[f"Mean {AXIS_LABELS[axis]}"] = clip_responses[axis].mean()
                row[f"Std {AXIS_LABELS[axis]}"] = clip_responses[axis].std()
            else:
                row[f"Mean {AXIS_LABELS[axis]}"] = None
                row[f"Std {AXIS_LABELS[axis]}"] = None
        clip_stats.append(row)

    clip_stats_df = pd.DataFrame(clip_stats)

    # Format for display
    display_cols = ["Clip", "Genre", "Classifier Score", "N"]
    for axis in AXES:
        display_cols.append(f"Mean {AXIS_LABELS[axis]}")
    st.dataframe(
        clip_stats_df[display_cols].style.format(
            {f"Mean {AXIS_LABELS[a]}": "{:.1f}" for a in AXES},
            na_rep="--",
        ),
        hide_index=True,
        use_container_width=True,
    )

    # --- Scatter plots: classifier score vs each axis ---
    st.subheader("Classifier Validation: Score vs Human Ratings")

    # Build per-clip aggregated data for correlation
    corr_rows = []
    for clip_path, meta in STUDY_CLIPS:
        clip_id = meta["clip_id"]
        clip_responses = rdf[rdf["trial_id"] == clip_id]
        if clip_responses.empty:
            continue
        row = {"clip_id": clip_id, "classifier_score": meta["classifier_score"]}
        for axis in AXES:
            if axis in clip_responses.columns:
                row[axis] = clip_responses[axis].mean()
            else:
                row[axis] = None
        corr_rows.append(row)

    corr_df = pd.DataFrame(corr_rows)

    if len(corr_df) >= 3:
        axis_colors = {
            "correctness": BLUE,
            "richness": GREEN,
            "quality": PURPLE,
        }

        scatter_cols = st.columns(3)
        for i, axis in enumerate(AXES):
            with scatter_cols[i]:
                valid = corr_df.dropna(subset=[axis])
                if len(valid) < 3:
                    st.info(f"Not enough data for {AXIS_LABELS[axis]}.")
                    continue

                r, p = scipy_stats.pearsonr(valid["classifier_score"], valid[axis])

                fig = px.scatter(
                    valid,
                    x="classifier_score",
                    y=axis,
                    hover_data=["clip_id"],
                    color_discrete_sequence=[axis_colors[axis]],
                    labels={
                        "classifier_score": "Classifier Score",
                        axis: AXIS_LABELS[axis],
                    },
                )

                # Add trend line
                if len(valid) >= 2:
                    z = np.polyfit(valid["classifier_score"], valid[axis], 1)
                    x_range = np.linspace(
                        valid["classifier_score"].min(),
                        valid["classifier_score"].max(),
                        50,
                    )
                    fig.add_trace(go.Scatter(
                        x=x_range,
                        y=np.polyval(z, x_range),
                        mode="lines",
                        line=dict(dash="dash", color=RED),
                        name="Trend",
                        showlegend=False,
                    ))

                fig.update_layout(
                    height=350,
                    title=f"{AXIS_LABELS[axis]}<br><sub>r = {r:.3f}, p = {p:.3f}</sub>",
                    yaxis_range=[0, 105],
                    margin=dict(t=60, b=40),
                )
                st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "Each point is one clip (averaged across raters). "
            "A positive Pearson r indicates the classifier aligns with human perception on that axis."
        )
    else:
        st.info("Need rated responses for at least 3 clips to compute correlations.")

    # --- Per-axis distribution histograms ---
    st.subheader("Rating Distributions by Axis")

    hist_cols = st.columns(3)
    hist_colors = [BLUE, GREEN, PURPLE]
    for i, axis in enumerate(AXES):
        with hist_cols[i]:
            if axis in rdf.columns:
                fig = px.histogram(
                    rdf,
                    x=axis,
                    nbins=20,
                    color_discrete_sequence=[hist_colors[i]],
                    labels={axis: AXIS_LABELS[axis]},
                )
                fig.update_layout(
                    height=300,
                    title=AXIS_LABELS[axis],
                    xaxis_range=[0, 100],
                    margin=dict(t=40, b=40),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No data for {AXIS_LABELS[axis]}.")

    # --- Inter-rater agreement (per axis) ---
    st.subheader("Inter-Rater Agreement (Per Axis)")

    st.caption(
        "Standard deviation of ratings within each clip, averaged across clips. "
        "Lower values indicate stronger agreement."
    )

    agreement_data = []
    for axis in AXES:
        within_clip_stds = []
        for clip_path, meta in STUDY_CLIPS:
            clip_id = meta["clip_id"]
            clip_responses = rdf[rdf["trial_id"] == clip_id]
            if len(clip_responses) < 2 or axis not in clip_responses.columns:
                continue
            within_clip_stds.append(clip_responses[axis].std())

        if within_clip_stds:
            agreement_data.append({
                "Axis": AXIS_LABELS[axis],
                "Mean within-clip SD": np.mean(within_clip_stds),
                "Clips with 2+ raters": len(within_clip_stds),
            })

    if agreement_data:
        agree_df = pd.DataFrame(agreement_data)
        st.dataframe(
            agree_df.style.format({"Mean within-clip SD": "{:.1f}"}),
            hide_index=True,
            use_container_width=True,
        )

        # Also compute ICC-like metric: ratio of between-clip variance to total variance
        icc_data = []
        for axis in AXES:
            if axis not in rdf.columns:
                continue
            clip_means = []
            all_ratings = []
            for clip_path, meta in STUDY_CLIPS:
                clip_id = meta["clip_id"]
                clip_responses = rdf[rdf["trial_id"] == clip_id]
                if len(clip_responses) < 1:
                    continue
                clip_means.append(clip_responses[axis].mean())
                all_ratings.extend(clip_responses[axis].tolist())

            if len(clip_means) >= 2 and len(all_ratings) >= 2:
                between_var = np.var(clip_means)
                total_var = np.var(all_ratings)
                if total_var > 0:
                    icc_data.append({
                        "Axis": AXIS_LABELS[axis],
                        "Between-clip variance ratio": between_var / total_var,
                    })

        if icc_data:
            st.caption(
                "Between-clip variance ratio: proportion of total variance explained by "
                "clip identity. Higher is better (raters agree on which clips differ)."
            )
            icc_df = pd.DataFrame(icc_data)
            st.dataframe(
                icc_df.style.format({"Between-clip variance ratio": "{:.3f}"}),
                hide_index=True,
                use_container_width=True,
            )
    else:
        st.info("Need at least 2 raters per clip to compute agreement.")

    # --- Correlation matrix: do the 3 axes correlate with each other? ---
    st.subheader("Axis Correlation Matrix")

    axis_cols_present = [a for a in AXES if a in rdf.columns]
    if len(axis_cols_present) >= 2:
        # Compute per-clip means for axis correlation
        clip_axis_means = []
        for clip_path, meta in STUDY_CLIPS:
            clip_id = meta["clip_id"]
            clip_responses = rdf[rdf["trial_id"] == clip_id]
            if clip_responses.empty:
                continue
            row = {"clip_id": clip_id}
            for axis in axis_cols_present:
                row[AXIS_LABELS[axis]] = clip_responses[axis].mean()
            clip_axis_means.append(row)

        if len(clip_axis_means) >= 3:
            cam_df = pd.DataFrame(clip_axis_means)
            axis_label_cols = [AXIS_LABELS[a] for a in axis_cols_present]
            corr_matrix = cam_df[axis_label_cols].corr()

            # Annotated heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns.tolist(),
                y=corr_matrix.index.tolist(),
                text=[[f"{v:.2f}" for v in row] for row in corr_matrix.values],
                texttemplate="%{text}",
                colorscale="RdBu_r",
                zmin=-1,
                zmax=1,
                colorbar=dict(title="r"),
            ))
            fig.update_layout(
                height=400,
                title="Pearson Correlations Between Axes (per-clip means)",
                margin=dict(t=60, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                "This matrix shows how the three axes relate to each other across clips. "
                "High correlations between Correctness and Quality suggest that technical "
                "accuracy drives overall perception. Low correlation between Richness and "
                "Correctness would mean they capture distinct aspects of quality."
            )
        else:
            st.info("Need data for at least 3 clips to compute axis correlations.")
    else:
        st.info("Need data for at least 2 axes to compute correlations.")

    # --- Response timeline ---
    st.subheader("Response Timeline")
    rdf["timestamp_dt"] = pd.to_datetime(rdf["timestamp"])
    rdf_sorted = rdf.sort_values("timestamp_dt")
    rdf_sorted["cumulative"] = range(1, len(rdf_sorted) + 1)

    fig = px.line(
        rdf_sorted, x="timestamp_dt", y="cumulative",
        color_discrete_sequence=[GREEN],
        labels={"timestamp_dt": "Time", "cumulative": "Cumulative Responses"},
    )
    fig.update_layout(height=350, title="Data Collection Progress")
    st.plotly_chart(fig, use_container_width=True)

    # --- Raw data download ---
    st.subheader("Raw Data")
    st.download_button(
        "Download results JSON",
        data=json.dumps(results, indent=2),
        file_name="study_results.json",
        mime="application/json",
    )

    st.stop()


# =========================================================================
# LISTENER VIEW
# =========================================================================

# --- Session state initialization ---
if "study_started" not in st.session_state:
    st.session_state.study_started = False
if "participant_id" not in st.session_state:
    st.session_state.participant_id = ""
if "current_trial" not in st.session_state:
    st.session_state.current_trial = 0
if "trial_order" not in st.session_state:
    st.session_state.trial_order = []
if "study_complete" not in st.session_state:
    st.session_state.study_complete = False


# --- Welcome screen ---
if not st.session_state.study_started:
    st.title("Music Listening Study")

    st.markdown("""
    Thank you for participating in this study. You will hear **{n} audio clips**
    one at a time. For each clip, rate it on three axes using the sliders provided:

    1. **Correctness** -- Is the music free of wrong notes, unnatural rhythms, and
       awkward phrasing?
    2. **Richness** -- Is the sample musically and harmonically interesting?
    3. **Overall Quality** -- How would you rate this piece overall?

    There are no right or wrong answers. We are interested in your genuine perception.

    The study takes approximately **10-15 minutes**.
    """.format(n=NUM_TRIALS))

    st.markdown("---")

    pid = st.text_input(
        "Enter your participant ID",
        placeholder="e.g., your initials + a number",
        max_chars=50,
    )

    if st.button("Start Study", type="primary", disabled=(len(pid.strip()) == 0)):
        st.session_state.participant_id = pid.strip()
        st.session_state.study_started = True
        seed = participant_seed(pid.strip())
        st.session_state.trial_order = build_trial_order(seed)
        st.session_state.current_trial = 0
        st.session_state.study_complete = False
        st.rerun()

    st.stop()


# --- Thank you screen ---
if st.session_state.study_complete:
    st.title("Study Complete")

    st.markdown("""
    Thank you for completing the listening study. Your responses have been recorded.

    You may close this tab now.
    """)

    if st.button("Start Over (new participant)"):
        st.session_state.study_started = False
        st.session_state.participant_id = ""
        st.session_state.current_trial = 0
        st.session_state.trial_order = []
        st.session_state.study_complete = False
        st.rerun()

    st.stop()


# --- Trial screen ---
trial_idx = st.session_state.current_trial
trial = st.session_state.trial_order[trial_idx]

# Progress
st.progress(trial_idx / NUM_TRIALS)
st.caption(f"Trial {trial_idx + 1} of {NUM_TRIALS}")

st.markdown("---")

st.markdown("Listen to the clip, then rate it on each axis.")

# Audio player
clip_path = trial["clip_path"]
if os.path.exists(clip_path):
    st.audio(clip_path)
else:
    st.info(f"Audio file not found: `{clip_path}`")
    st.caption("(Placeholder -- add audio files to run the study)")

st.markdown("---")

# Rating sliders
correctness = st.slider(
    "**Correctness** -- Is the music free of inharmonious notes, unnatural rhythms, "
    "and awkward phrasing?",
    min_value=0,
    max_value=100,
    value=50,
    key=f"slider_correctness_{trial_idx}",
)

richness = st.slider(
    "**Richness** -- Is the sample musically and harmonically interesting?",
    min_value=0,
    max_value=100,
    value=50,
    key=f"slider_richness_{trial_idx}",
)

quality = st.slider(
    "**Overall Quality** -- How would you rate this piece overall?",
    min_value=0,
    max_value=100,
    value=50,
    key=f"slider_quality_{trial_idx}",
)

st.markdown("---")

# Submit button
col_left, col_center, col_right = st.columns([2, 3, 2])

with col_center:
    if st.button("Submit Ratings", use_container_width=True, type="primary"):
        trial_data = st.session_state.trial_order[st.session_state.current_trial]
        entry = {
            "participant_id": st.session_state.participant_id,
            "trial_id": trial_data["metadata"]["clip_id"],
            "clip_path": trial_data["clip_path"],
            "clip_metadata": trial_data["metadata"],
            "correctness": correctness,
            "richness": richness,
            "quality": quality,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        save_result(entry)

        next_trial = st.session_state.current_trial + 1
        if next_trial >= NUM_TRIALS:
            st.session_state.study_complete = True
        else:
            st.session_state.current_trial = next_trial

        st.rerun()
