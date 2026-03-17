"""PDMX Dataset Exploration — visualize what we're working with."""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_DIR = "analysis/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight"})


def load():
    df = pd.read_csv(
        "PDMXDataset/PDMX.csv",
        usecols=[
            "rating", "n_ratings", "n_tracks", "n_notes", "genres",
            "song_name", "song_length.bars", "song_length.beats",
            "complexity", "n_favorites", "n_views",
        ],
    )
    df["rated"] = df["rating"] > 0
    return df


def plot_rating_distribution(df):
    """Histogram of ratings with threshold lines."""
    rated = df[df.rated]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: full histogram
    ax = axes[0]
    ax.hist(rated["rating"], bins=50, color="#4C72B0", edgecolor="white", alpha=0.9)
    ax.axvline(4.76, color="red", linestyle="--", linewidth=2, label="Threshold (4.76)")
    ax.axvline(rated["rating"].median(), color="orange", linestyle="--", linewidth=2, label=f"Median ({rated.rating.median():.2f})")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.set_title("Rating Distribution (all rated, n=14,182)")
    ax.legend()

    # Right: only n_ratings >= 10
    reliable = rated[rated["n_ratings"] >= 10]
    ax = axes[1]
    ax.hist(reliable["rating"], bins=50, color="#55A868", edgecolor="white", alpha=0.9)
    ax.axvline(4.76, color="red", linestyle="--", linewidth=2, label="Threshold (4.76)")
    ax.axvline(reliable["rating"].median(), color="orange", linestyle="--", linewidth=2, label=f"Median ({reliable.rating.median():.2f})")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.set_title(f"Rating Distribution (n_ratings >= 10, n={len(reliable):,})")
    ax.legend()

    plt.suptitle("PDMX Ratings Are Heavily Skewed Toward High Scores", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/01_rating_distribution.png")
    plt.close()
    print("Saved 01_rating_distribution.png")


def plot_n_ratings_distribution(df):
    """How many ratings do pieces get?"""
    rated = df[df.rated]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Linear scale
    ax = axes[0]
    ax.hist(rated["n_ratings"], bins=100, color="#4C72B0", edgecolor="white", alpha=0.9)
    ax.axvline(10, color="red", linestyle="--", linewidth=2, label="Min filter (10)")
    ax.set_xlabel("Number of Ratings")
    ax.set_ylabel("Count")
    ax.set_title("n_ratings Distribution (linear)")
    ax.set_xlim(0, 200)
    ax.legend()

    # Log scale
    ax = axes[1]
    ax.hist(rated["n_ratings"], bins=np.logspace(np.log10(3), np.log10(7000), 60),
            color="#55A868", edgecolor="white", alpha=0.9)
    ax.set_xscale("log")
    ax.axvline(10, color="red", linestyle="--", linewidth=2, label="Min filter (10)")
    ax.set_xlabel("Number of Ratings (log)")
    ax.set_ylabel("Count")
    ax.set_title("n_ratings Distribution (log scale)")
    ax.legend()

    plt.suptitle("Most Rated Pieces Have Very Few Ratings", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/02_n_ratings_distribution.png")
    plt.close()
    print("Saved 02_n_ratings_distribution.png")


def plot_rating_vs_n_ratings(df):
    """Scatter: does more ratings = higher rating?"""
    rated = df[df.rated].copy()
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sample to avoid overplotting
    sample = rated.sample(min(5000, len(rated)), random_state=42)
    ax.scatter(sample["n_ratings"], sample["rating"], alpha=0.3, s=10, color="#4C72B0")
    ax.set_xscale("log")
    ax.set_xlabel("Number of Ratings (log)")
    ax.set_ylabel("Rating")
    ax.set_title("More Ratings → Slightly Higher Average Rating")
    ax.axhline(4.76, color="red", linestyle="--", alpha=0.7, label="Threshold (4.76)")
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/03_rating_vs_n_ratings.png")
    plt.close()
    print("Saved 03_rating_vs_n_ratings.png")


def plot_filtering_funnel(df):
    """Show how filtering narrows the dataset."""
    total = len(df)
    has_rating = (df.rating > 0).sum()
    nr_3 = ((df.rating > 0) & (df.n_ratings >= 3)).sum()
    nr_10 = ((df.rating > 0) & (df.n_ratings >= 10)).sum()
    nr_20 = ((df.rating > 0) & (df.n_ratings >= 20)).sum()

    stages = ["All files\n(254K)", "Has rating\n(rated > 0)", "n_ratings >= 3", "n_ratings >= 10\n(our filter)", "n_ratings >= 20"]
    counts = [total, has_rating, nr_3, nr_10, nr_20]
    colors = ["#CCCCCC", "#A8D5E2", "#7FB3D3", "#55A868", "#4C72B0"]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(stages, counts, color=colors, edgecolor="white", linewidth=2)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000,
                f"{count:,}", ha="center", va="bottom", fontweight="bold", fontsize=11)

    ax.set_ylabel("Number of Files")
    ax.set_title("Dataset Filtering Funnel: From 254K to 5.6K Reliable Training Samples",
                 fontsize=13, fontweight="bold")
    ax.set_ylim(0, 280000)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/04_filtering_funnel.png")
    plt.close()
    print("Saved 04_filtering_funnel.png")


def plot_genre_breakdown(df):
    """Top genres and their rating distributions."""
    rated = df[(df.rating > 0) & (df.n_ratings >= 10)].copy()
    # Genres can be comma-separated
    genre_rows = []
    for _, row in rated.iterrows():
        if pd.isna(row["genres"]) or row["genres"] == "NA":
            genre_rows.append({"genre": "Unknown", "rating": row["rating"]})
        else:
            for g in str(row["genres"]).split(","):
                g = g.strip().strip("[]'\" ")
                if g:
                    genre_rows.append({"genre": g, "rating": row["rating"]})

    gdf = pd.DataFrame(genre_rows)
    top_genres = gdf["genre"].value_counts().head(15)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Left: genre counts
    ax = axes[0]
    top_genres.plot.barh(ax=ax, color="#4C72B0", edgecolor="white")
    ax.set_xlabel("Number of Pieces")
    ax.set_title("Top 15 Genres (n_ratings >= 10)")
    ax.invert_yaxis()

    # Right: rating by genre (box plot)
    ax = axes[1]
    top_genre_names = top_genres.index.tolist()
    plot_data = gdf[gdf["genre"].isin(top_genre_names)]
    genre_order = plot_data.groupby("genre")["rating"].median().sort_values(ascending=False).index
    sns.boxplot(data=plot_data, y="genre", x="rating", order=genre_order, ax=ax,
                palette="viridis", fliersize=2)
    ax.axvline(4.76, color="red", linestyle="--", alpha=0.7, label="Threshold")
    ax.set_xlabel("Rating")
    ax.set_title("Rating by Genre")
    ax.legend()

    plt.suptitle("Genre Distribution in Training Data", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/05_genre_breakdown.png")
    plt.close()
    print("Saved 05_genre_breakdown.png")


def plot_complexity_profile(df):
    """Notes, tracks, length distributions for rated subset."""
    rated = df[(df.rating > 0) & (df.n_ratings >= 10)].copy()

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # n_notes
    ax = axes[0, 0]
    ax.hist(rated["n_notes"].clip(upper=5000), bins=60, color="#4C72B0", edgecolor="white", alpha=0.9)
    ax.set_xlabel("Number of Notes")
    ax.set_title(f"Notes per Piece (median={rated.n_notes.median():.0f})")

    # n_tracks
    ax = axes[0, 1]
    track_counts = rated["n_tracks"].clip(upper=20).value_counts().sort_index()
    ax.bar(track_counts.index, track_counts.values, color="#55A868", edgecolor="white")
    ax.set_xlabel("Number of Tracks")
    ax.set_title(f"Tracks per Piece (median={rated.n_tracks.median():.0f})")

    # song length (bars)
    ax = axes[1, 0]
    bars_col = rated["song_length.bars"].dropna()
    ax.hist(bars_col.clip(upper=200), bins=60, color="#C44E52", edgecolor="white", alpha=0.9)
    ax.set_xlabel("Number of Bars")
    ax.set_title(f"Bars per Piece (median={bars_col.median():.0f})")

    # complexity
    ax = axes[1, 1]
    complexity = rated["complexity"].dropna()
    ax.hist(complexity, bins=40, color="#8172B3", edgecolor="white", alpha=0.9)
    ax.set_xlabel("Complexity Score")
    ax.set_title(f"PDMX Complexity (median={complexity.median():.1f})")

    plt.suptitle("What Does the Training Data Look Like?", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/06_complexity_profile.png")
    plt.close()
    print("Saved 06_complexity_profile.png")


def plot_rated_vs_unrated(df):
    """Compare structural properties of rated vs unrated pieces."""
    df = df.copy()
    df["group"] = np.where(df["rated"], "Rated (14K)", "Unrated (240K)")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, col, label in zip(axes, ["n_notes", "n_tracks", "song_length.bars"],
                                    ["Notes", "Tracks", "Bars"]):
        data = df[[col, "group"]].dropna()
        if col == "n_notes":
            data = data[data[col] < 5000]
        elif col == "song_length.bars":
            data = data[data[col] < 200]

        for group, color in [("Rated (14K)", "#55A868"), ("Unrated (240K)", "#4C72B0")]:
            subset = data[data["group"] == group][col]
            ax.hist(subset, bins=50, alpha=0.6, color=color, label=group, density=True, edgecolor="white")
        ax.set_xlabel(label)
        ax.set_ylabel("Density")
        ax.legend()

    plt.suptitle("Rated vs Unrated Pieces: Structural Comparison", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/07_rated_vs_unrated.png")
    plt.close()
    print("Saved 07_rated_vs_unrated.png")


def plot_popularity_vs_quality(df):
    """Views/favorites vs rating — is popularity correlated?"""
    rated = df[(df.rating > 0) & (df.n_ratings >= 10)].copy()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, col, label in zip(axes, ["n_views", "n_favorites"], ["Views", "Favorites"]):
        data = rated[[col, "rating"]].dropna()
        data = data[data[col] > 0]
        ax.scatter(data[col], data["rating"], alpha=0.2, s=8, color="#4C72B0")
        ax.set_xscale("log")
        ax.set_xlabel(f"{label} (log)")
        ax.set_ylabel("Rating")
        ax.axhline(4.76, color="red", linestyle="--", alpha=0.5)

        corr = data[col].apply(np.log10).corr(data["rating"])
        ax.set_title(f"{label} vs Rating (r={corr:.3f})")

    plt.suptitle("Popularity Weakly Correlates with Rating", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/08_popularity_vs_quality.png")
    plt.close()
    print("Saved 08_popularity_vs_quality.png")


if __name__ == "__main__":
    print("Loading PDMX dataset...")
    df = load()
    print(f"Loaded {len(df):,} rows\n")

    plot_rating_distribution(df)
    plot_n_ratings_distribution(df)
    plot_rating_vs_n_ratings(df)
    plot_filtering_funnel(df)
    plot_genre_breakdown(df)
    plot_complexity_profile(df)
    plot_rated_vs_unrated(df)
    plot_popularity_vs_quality(df)

    print(f"\nAll plots saved to {OUTPUT_DIR}/")
