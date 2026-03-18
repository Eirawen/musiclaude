"""Rachmaniclaude Analysis Dashboard — Streamlit + Plotly."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="Rachmaniclaude — PDMX Analysis",
    page_icon="🎵",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

@st.cache_data
def load_pdmx():
    return pd.read_csv(
        "PDMXDataset/PDMX.csv",
        usecols=[
            "rating", "n_ratings", "n_tracks", "n_notes", "genres",
            "song_name", "song_length.bars", "song_length.beats",
            "complexity", "n_favorites", "n_views",
        ],
    )


@st.cache_data
def load_features():
    path = "features.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


df = load_pdmx()
features_df = load_features()

rated = df[df["rating"] > 0].copy()
reliable = rated[rated["n_ratings"] >= 10].copy()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.title("Rachmaniclaude")
st.sidebar.markdown("PDMX Dataset Analysis & Quality Classifier")

min_ratings = st.sidebar.slider("Min ratings filter", 3, 50, 10)
filtered = rated[rated["n_ratings"] >= min_ratings]
threshold = st.sidebar.number_input(
    "Binary threshold", min_value=3.0, max_value=5.0,
    value=round(float(filtered["rating"].median()), 2), step=0.01,
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered dataset:** {len(filtered):,} pieces")
below = (filtered["rating"] < threshold).sum()
above = (filtered["rating"] >= threshold).sum()
st.sidebar.markdown(f"Below {threshold}: {below:,} ({100*below/len(filtered):.1f}%)")
st.sidebar.markdown(f"Above {threshold}: {above:,} ({100*above/len(filtered):.1f}%)")

page = st.sidebar.radio(
    "Page",
    ["Dataset Overview", "Rating Analysis", "Genre & Complexity", "Rated vs Unrated",
     "Feature Extraction Results"],
)

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

BLUE = "#4C72B0"
GREEN = "#55A868"
RED = "#C44E52"
PURPLE = "#8172B3"
ORANGE = "#DD8452"

# ---------------------------------------------------------------------------
# Page: Dataset Overview
# ---------------------------------------------------------------------------

if page == "Dataset Overview":
    st.title("PDMX Dataset Overview")
    st.markdown(
        "254K public domain MusicXML scores from MuseScore with user ratings. "
        "Source: [Zenodo](https://zenodo.org/records/14648209)"
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total files", f"{len(df):,}")
    col2.metric("Rated files", f"{len(rated):,}")
    col3.metric(f"n_ratings >= {min_ratings}", f"{len(filtered):,}")
    col4.metric("Threshold", f"{threshold}")

    # Filtering funnel
    st.subheader("Filtering Funnel")
    stages = ["All files", "Has rating", "n_ratings >= 3", f"n_ratings >= {min_ratings}"]
    counts = [
        len(df),
        len(rated),
        len(rated[rated["n_ratings"] >= 3]),
        len(filtered),
    ]
    colors = ["#CCCCCC", "#A8D5E2", "#7FB3D3", GREEN]

    fig = go.Figure(go.Bar(
        x=stages, y=counts,
        marker_color=colors,
        text=[f"{c:,}" for c in counts],
        textposition="outside",
    ))
    fig.update_layout(
        title="From 254K Files to Reliable Training Samples",
        yaxis_title="Number of Files",
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    **Why filter?** Most of the 254K files are unrated uploads — exercises, fragments, tests.
    Of the 14K rated files, many have only 3-5 ratings where a single outlier vote can swing
    the average significantly. At n_ratings >= {min_ratings}, the ratings stabilize and we get
    {len(filtered):,} reliable training samples with a rating std of {filtered.rating.std():.3f}.
    """)

    # Data quality table
    st.subheader("Filter Quality Tradeoff")
    rows = []
    for n in [3, 5, 10, 15, 20, 30, 50]:
        sub = rated[rated["n_ratings"] >= n]
        if len(sub) > 0:
            rows.append({
                "Min Ratings": n,
                "Files": f"{len(sub):,}",
                "Rating Std": f"{sub.rating.std():.3f}",
                "Rating Mean": f"{sub.rating.mean():.3f}",
                "Median": f"{sub.rating.median():.3f}",
            })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Rating Analysis
# ---------------------------------------------------------------------------

elif page == "Rating Analysis":
    st.title("Rating Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("All Rated Files")
        fig = px.histogram(
            rated, x="rating", nbins=60,
            color_discrete_sequence=[BLUE],
            labels={"rating": "Rating", "count": "Count"},
        )
        fig.add_vline(x=threshold, line_dash="dash", line_color="red",
                       annotation_text=f"Threshold ({threshold})")
        fig.add_vline(x=rated.rating.median(), line_dash="dash", line_color="orange",
                       annotation_text=f"Median ({rated.rating.median():.2f})")
        fig.update_layout(height=400, title=f"n={len(rated):,}")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"Reliable (n_ratings >= {min_ratings})")
        fig = px.histogram(
            filtered, x="rating", nbins=60,
            color_discrete_sequence=[GREEN],
        )
        fig.add_vline(x=threshold, line_dash="dash", line_color="red",
                       annotation_text=f"Threshold ({threshold})")
        fig.add_vline(x=filtered.rating.median(), line_dash="dash", line_color="orange",
                       annotation_text=f"Median ({filtered.rating.median():.2f})")
        fig.update_layout(height=400, title=f"n={len(filtered):,}")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Key insight:** Ratings are extremely right-skewed. MuseScore has selection bias —
    people rate things they like, and low-quality scores don't accumulate ratings.
    The classifier learns "great vs good" within an already-curated pool, not "music vs noise."
    """)

    # n_ratings distribution
    st.subheader("Number of Ratings per Piece")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            rated, x="n_ratings", nbins=100,
            color_discrete_sequence=[BLUE],
            range_x=[0, 200],
        )
        fig.add_vline(x=min_ratings, line_dash="dash", line_color="red",
                       annotation_text=f"Min filter ({min_ratings})")
        fig.update_layout(height=400, title="Linear Scale")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            rated, x="n_ratings", nbins=60,
            color_discrete_sequence=[GREEN],
            log_x=True,
        )
        fig.add_vline(x=min_ratings, line_dash="dash", line_color="red",
                       annotation_text=f"Min filter ({min_ratings})")
        fig.update_layout(height=400, title="Log Scale")
        st.plotly_chart(fig, use_container_width=True)

    # Rating vs n_ratings scatter
    st.subheader("Rating vs Number of Ratings")
    sample = rated.sample(min(5000, len(rated)), random_state=42)
    fig = px.scatter(
        sample, x="n_ratings", y="rating",
        log_x=True, opacity=0.3,
        color_discrete_sequence=[BLUE],
        hover_data=["song_name"],
    )
    fig.add_hline(y=threshold, line_dash="dash", line_color="red",
                   annotation_text=f"Threshold ({threshold})")
    fig.update_layout(
        height=500,
        title="Variance Funnel: More Ratings → More Reliable Scores",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    The variance funnel shows the central limit theorem in action.
    At 3-5 ratings, scores scatter from 2.8 to 5.0.
    By 50+ ratings, they converge to 4.5-4.9.
    Pieces with very high ratings (>4.9) almost always have few ratings —
    their scores haven't regressed to the mean yet.
    """)

    # Popularity vs quality
    st.subheader("Popularity vs Quality")
    col1, col2 = st.columns(2)

    pop = filtered[["n_views", "n_favorites", "rating"]].dropna()
    pop = pop[(pop["n_views"] > 0) & (pop["n_favorites"] > 0)]

    with col1:
        r_views = np.log10(pop["n_views"]).corr(pop["rating"])
        fig = px.scatter(
            pop, x="n_views", y="rating", log_x=True, opacity=0.3,
            color_discrete_sequence=[BLUE],
        )
        fig.add_hline(y=threshold, line_dash="dash", line_color="red", opacity=0.4)
        fig.update_layout(height=400, title=f"Views vs Rating (r={r_views:.3f})")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        r_favs = np.log10(pop["n_favorites"]).corr(pop["rating"])
        fig = px.scatter(
            pop, x="n_favorites", y="rating", log_x=True, opacity=0.3,
            color_discrete_sequence=[GREEN],
        )
        fig.add_hline(y=threshold, line_dash="dash", line_color="red", opacity=0.4)
        fig.update_layout(height=400, title=f"Favorites vs Rating (r={r_favs:.3f})")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Near-zero correlation** — ratings are not a popularity proxy.
    This validates using ratings as a genuine quality signal for training.
    """)


# ---------------------------------------------------------------------------
# Page: Genre & Complexity
# ---------------------------------------------------------------------------

elif page == "Genre & Complexity":
    st.title("Genre & Complexity Analysis")

    # Parse genres
    genre_rows = []
    for _, row in filtered.iterrows():
        if pd.isna(row["genres"]) or row["genres"] == "NA":
            genre_rows.append({"genre": "Unknown", "rating": row["rating"]})
        else:
            for g in str(row["genres"]).split(","):
                g = g.strip().strip("[]'\" ")
                if g:
                    genre_rows.append({"genre": g, "rating": row["rating"]})
    gdf = pd.DataFrame(genre_rows)
    top_genres = gdf["genre"].value_counts().head(15)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Genres")
        fig = px.bar(
            x=top_genres.values, y=top_genres.index,
            orientation="h",
            color_discrete_sequence=[BLUE],
            labels={"x": "Number of Pieces", "y": "Genre"},
        )
        fig.update_layout(height=500, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Rating by Genre")
        top_genre_data = gdf[gdf["genre"].isin(top_genres.index)]
        genre_order = top_genre_data.groupby("genre")["rating"].median().sort_values(ascending=False).index
        fig = px.box(
            top_genre_data, x="rating", y="genre",
            category_orders={"genre": list(genre_order)},
            color_discrete_sequence=[GREEN],
        )
        fig.add_vline(x=threshold, line_dash="dash", line_color="red", opacity=0.5)
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Classical dominates** the training set. Jazz-classical has the highest median rating.
    Genre is a confounder — some classifier signal may come from genre-correlated features
    rather than quality per se. We intentionally exclude genre as a feature to learn
    structural quality, not genre popularity.
    """)

    # Complexity
    st.subheader("Composition Complexity")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            filtered, x="n_notes", nbins=80,
            range_x=[0, 5000],
            color_discrete_sequence=[BLUE],
        )
        fig.update_layout(height=350, title=f"Notes per Piece (median={filtered.n_notes.median():.0f})")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        track_counts = filtered["n_tracks"].clip(upper=20).value_counts().sort_index().reset_index()
        track_counts.columns = ["n_tracks", "count"]
        fig = px.bar(
            track_counts, x="n_tracks", y="count",
            color_discrete_sequence=[GREEN],
        )
        fig.update_layout(height=350, title=f"Tracks per Piece (median={filtered.n_tracks.median():.0f})")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        bars_data = filtered["song_length.bars"].dropna().clip(upper=300)
        fig = px.histogram(
            x=bars_data, nbins=80,
            color_discrete_sequence=[RED],
        )
        fig.update_layout(height=350, title=f"Bars per Piece (median={filtered['song_length.bars'].median():.0f})",
                         xaxis_title="Bars")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        complexity = filtered["complexity"].dropna()
        fig = px.histogram(
            x=complexity, nbins=40,
            color_discrete_sequence=[PURPLE],
        )
        fig.update_layout(height=350, title=f"PDMX Complexity Score (median={complexity.median():.1f})",
                         xaxis_title="Complexity")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Median 1 track, 73 bars, 1,058 notes.** Most training data is single-instrument.
    LLM compositions (typically 16-32 bars, 1-3 tracks) are on the short/simple end
    of this distribution — the classifier may penalize brevity, which is correct behavior.
    """)


# ---------------------------------------------------------------------------
# Page: Rated vs Unrated
# ---------------------------------------------------------------------------

elif page == "Rated vs Unrated":
    st.title("Rated vs Unrated: Selection Bias")

    st.markdown("""
    Rated pieces are **systematically different** from unrated ones — longer, more notes,
    more tracks. This is selection bias: substantial compositions attract attention and ratings.
    The Isolation Forest trains on both populations to learn the full range of human music.
    """)

    for col_name, label, clip_max in [
        ("n_notes", "Notes", 5000),
        ("n_tracks", "Tracks", 30),
        ("song_length.bars", "Bars", 200),
    ]:
        data = df[[col_name, "rating"]].dropna().copy()
        data["group"] = np.where(data["rating"] > 0, "Rated (14K)", "Unrated (240K)")
        data[col_name] = data[col_name].clip(upper=clip_max)

        fig = px.histogram(
            data, x=col_name, color="group",
            barmode="overlay", nbins=60,
            histnorm="probability density",
            color_discrete_map={"Rated (14K)": GREEN, "Unrated (240K)": BLUE},
            opacity=0.6,
            labels={col_name: label},
        )
        fig.update_layout(height=350, title=f"{label}: Rated vs Unrated")
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Feature Extraction Results
# ---------------------------------------------------------------------------

elif page == "Feature Extraction Results":
    st.title("Feature Extraction Results")

    if features_df is None:
        st.warning(
            "No `features.csv` found yet. Run the extraction:\n\n"
            "```bash\n"
            "python -m rachmaniclaude.features.extract \\\n"
            "  --data-dir data/mxl \\\n"
            "  --pdmx-csv PDMXDataset/PDMX.csv \\\n"
            "  --output features.csv \\\n"
            "  --file-list data/target_basenames.txt \\\n"
            "  --workers 16\n"
            "```"
        )
        st.stop()

    non_feature = {"filepath", "rating", "n_ratings", "instrument_names", "basename"}
    feature_cols = [c for c in features_df.columns if c not in non_feature]
    numeric_features = features_df[feature_cols].apply(pd.to_numeric, errors="coerce")

    st.markdown(f"**{len(features_df):,}** files extracted, **{len(feature_cols)}** features")

    # Completeness
    st.subheader("Feature Completeness")
    completeness = numeric_features.notna().mean().sort_values(ascending=True)
    fig = px.bar(
        x=completeness.values * 100, y=completeness.index,
        orientation="h",
        color=completeness.values,
        color_continuous_scale="RdYlGn",
        labels={"x": "% Non-Null", "y": "Feature"},
    )
    fig.update_layout(height=max(400, len(feature_cols) * 18), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    # Feature distributions
    st.subheader("Feature Distributions")
    selected_feature = st.selectbox("Select feature", sorted(feature_cols))

    col1, col2 = st.columns(2)
    feat_data = numeric_features[selected_feature].dropna()

    with col1:
        fig = px.histogram(feat_data, nbins=60, color_discrete_sequence=[BLUE])
        fig.update_layout(
            height=350,
            title=f"{selected_feature} (n={len(feat_data):,})",
            xaxis_title=selected_feature,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        stats = feat_data.describe()
        st.dataframe(stats.to_frame().T, use_container_width=True)
        if "rating" in features_df.columns:
            merged = features_df[["rating", selected_feature]].dropna()
            merged = merged[merged["rating"] > 0]
            if len(merged) > 50:
                corr = merged["rating"].corr(merged[selected_feature])
                st.metric("Correlation with rating", f"{corr:.3f}")

    # Correlation heatmap (if features exist)
    if "rating" in features_df.columns:
        st.subheader("Feature Correlations with Rating")
        rated_features = features_df[features_df["rating"] > 0].copy()
        corrs = numeric_features.loc[rated_features.index].corrwith(rated_features["rating"]).dropna().sort_values()

        fig = px.bar(
            x=corrs.values, y=corrs.index,
            orientation="h",
            color=corrs.values,
            color_continuous_scale="RdBu_r",
            range_color=[-0.3, 0.3],
            labels={"x": "Pearson r with Rating", "y": "Feature"},
        )
        fig.update_layout(height=max(400, len(corrs) * 18), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Built with [Streamlit](https://streamlit.io) + [Plotly](https://plotly.com)"
)
