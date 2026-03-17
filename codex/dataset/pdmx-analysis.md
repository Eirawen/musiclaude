# PDMX Dataset Analysis

Source: [Zenodo](https://zenodo.org/records/14648209) — 254,077 public domain MusicXML scores scraped from MuseScore, with user ratings and metadata.

## Dataset at a Glance

| Metric | Value |
|--------|-------|
| Total files | 254,077 |
| Files with ratings (rating > 0) | 14,182 (5.6%) |
| Files with reliable ratings (n_ratings >= 10) | 5,620 (2.2%) |
| Rating range (rated) | 2.83 – 4.98 |
| Rating mean / median (n_ratings >= 10) | 4.72 / 4.76 |
| Rating std (n_ratings >= 10) | 0.171 |
| Top genre | Classical (~2,000 pieces) |
| Median notes per piece (rated) | 1,058 |
| Median tracks per piece (rated) | 1 |
| Median bars per piece (rated) | 73 |

---

## Plot 01 — Rating Distribution

![Rating Distribution](../analysis/plots/01_rating_distribution.png)

**What it shows:** Histogram of all ratings (left) vs. only reliably-rated pieces with n_ratings >= 10 (right). Red dashed line = our binary classification threshold (4.76).

**Key insight:** PDMX ratings are *extremely* right-skewed. Almost nothing is rated below 4.0. This is classic MuseScore selection bias — people tend to rate things they like, and low-quality scores don't accumulate enough ratings to appear in the dataset at all. The original default threshold of 4.0 would have given a 98.5/1.5 class split, which is useless for training. Using the median (4.76) gives a clean ~49/51 split.

**Implication for training:** The classifier isn't learning "good vs bad" music. It's learning "great vs good" within an already-curated pool. This is fine for our use case — LLM-generated music needs to clear the bar of "sounds like something a skilled human would upload to MuseScore," not "is this music at all." The Isolation Forest handles the latter.

---

## Plot 02 — Number of Ratings Distribution

![n_ratings Distribution](../analysis/plots/02_n_ratings_distribution.png)

**What it shows:** How many ratings each rated piece received. Left is linear scale, right is log scale. Red line = our minimum filter (10 ratings).

**Key insight:** Massively power-law distributed. Most rated pieces have only 3-5 ratings. The log-scale view reveals a long tail stretching to ~7,000 ratings (viral pieces). Our n_ratings >= 10 filter sits at the elbow of the distribution — it cuts the dataset from 14K to 5.6K but dramatically improves label reliability.

**Why n_ratings >= 10:** With only 3 ratings, a single troll or superfan can swing the average by 0.5+ points. At 10+ ratings, the variance drops from std=0.212 to std=0.171 — the law of large numbers starts kicking in. We chose 10 as the sweet spot between data quantity (5.6K samples, still plenty for XGBoost) and label quality.

| Min Ratings | Files | Rating Std | Tradeoff |
|-------------|-------|------------|----------|
| 3 | 14,182 | 0.212 | Noisy — 3 people can be random |
| 5 | 9,907 | 0.199 | Better, but still unreliable |
| **10** | **5,620** | **0.171** | **Sweet spot — reliable signal, good sample size** |
| 20 | 2,864 | 0.143 | More reliable but dataset shrinks fast |
| 50 | 1,054 | 0.116 | Very reliable but too few for ML |

---

## Plot 03 — Rating vs Number of Ratings

![Rating vs n_ratings](../analysis/plots/03_rating_vs_n_ratings.png)

**What it shows:** Scatter plot of each piece's average rating against how many ratings it received (log scale).

**Key insight:** The variance funnel. At 3-5 ratings, scores scatter from 2.8 to 5.0. By 50+ ratings, they've all converged to the 4.5-4.9 range. This is the central limit theorem in action — average ratings regress toward the population mean as sample size increases. The few pieces with 1000+ ratings cluster tightly around 4.6-4.8.

**Implication:** Pieces with very high ratings (>4.9) almost always have few ratings — their scores haven't had time to regress to the mean. Pieces with many ratings are genuinely "consensus good" but rarely "perfect." This asymmetry is why the threshold must be set relative to the filtered subset, not the raw data.

---

## Plot 04 — Filtering Funnel

![Filtering Funnel](../analysis/plots/04_filtering_funnel.png)

**What it shows:** How each filter stage narrows the dataset from 254K total files down to our training set.

**Key insight:** 94.4% of the dataset is unrated. Of the rated pieces, the jump from "has rating" (14,182) to "n_ratings >= 3" (14,182) shows that MuseScore already applies a minimum of 3 ratings before publishing an average — so the >=3 filter is redundant. The real cut happens at >=10, which drops us to 5,620.

**Why this matters for the distribution scorer:** The Isolation Forest trains on ALL 25.6K files (5.6K rated + 20K unrated sample), not just the rated subset. It needs to learn what "normal human-composed music" looks like regardless of whether it was rated. The XGBoost classifier trains on only the 5.6K rated files.

---

## Plot 05 — Genre Breakdown

![Genre Breakdown](../analysis/plots/05_genre_breakdown.png)

**What it shows:** Left: top 15 genres by count in the rated training set. Right: box plots of rating distributions per genre, ordered by median rating.

**Key insights:**
- **Classical dominates** — ~2,000 of our 5,620 training pieces are classical. This means the classifier will be biased toward what makes *classical* music good. Whether this generalizes to other genres depends on whether the 32 features are genre-agnostic (mostly yes — entropy, consonance, and rhythmic variety are universal).
- **Jazz-classical has highest median rating** (~4.9). Makes sense — these are transcriptions by skilled arrangers.
- **Folk and pop have lowest median ratings** — but still above 4.5. The "worst" music in our dataset is still decent by absolute standards.
- **Genre is a confounder** — some of the classifier's signal may come from genre-correlated features (e.g., classical pieces have more voice crossings, jazz has more extended chords) rather than quality per se. We don't include genre as a feature, which is intentional — we want the classifier to learn structural quality, not genre popularity.

---

## Plot 06 — Complexity Profile

![Complexity Profile](../analysis/plots/06_complexity_profile.png)

**What it shows:** Distributions of notes, tracks, bars, and PDMX's own complexity score for the rated training set.

**Key insights:**
- **Median 1 track** — Most pieces in the training set are single-instrument (piano, guitar, or solo instrument). Multi-track orchestral pieces exist but are the minority. The spike at 20 tracks is orchestral arrangements.
- **Median 1,058 notes** — Substantial pieces, not toy examples. The long tail extends past 5,000.
- **Median 73 bars** — Typical song length. The spike at 200 is the histogram bin catching everything >=200.
- **PDMX complexity is mostly 0** — This is PDMX's own metadata field and appears to be unreliable or sparsely populated. We don't use it.

**Implication for LLM composition:** Claude typically generates 16-32 bar pieces with 1-3 tracks. This is on the short/simple end of the training distribution. The classifier may rate shorter pieces lower simply because they have less harmonic development, fewer cadences, etc. This is a known bias we accept — it correctly penalizes trivially short compositions.

---

## Plot 07 — Rated vs Unrated Structural Comparison

![Rated vs Unrated](../analysis/plots/07_rated_vs_unrated.png)

**What it shows:** Density plots comparing rated (green) vs unrated (blue) pieces across notes, tracks, and bars.

**Key insight:** Rated pieces are systematically different from unrated ones:
- **More notes** — rated pieces skew toward 500-3000 notes, unrated peaks sharply at <200
- **More tracks** — unrated pieces are overwhelmingly single-track; rated pieces have a wider distribution
- **More bars** — rated pieces are longer (peak ~30-50 bars vs ~10-20 for unrated)

**Why this matters:** There's a **selection bias** in what gets rated. Longer, more complex pieces attract more attention and ratings. Simple exercises, fragments, and test uploads don't get rated. This means our training data is biased toward "substantial" music. The distribution scorer partially compensates — it trains on both rated and unrated files, so it learns the full range of what human-composed music looks like.

---

## Plot 08 — Popularity vs Quality

![Popularity vs Quality](../analysis/plots/08_popularity_vs_quality.png)

**What it shows:** Views and favorites (log scale) vs rating for pieces with n_ratings >= 10.

**Key insight:** Almost zero correlation. Views vs rating: r = -0.037. Favorites vs rating: r = 0.014. **Popularity does not predict quality** in this dataset.

**Why this is good news:** It means MuseScore ratings are not just a popularity contest. A piece with 100 views and 10 ratings can have the same score as a viral piece with 100,000 views. The ratings reflect some genuine quality judgment, not just exposure. This validates using ratings as our training signal — if they were just popularity proxies, the classifier would learn "what gets clicks" rather than "what sounds good."

---

## Summary: What This Means for the Classifier

1. **We're training on the cream of MuseScore** — 5,620 pieces, all with 10+ ratings, skewed toward classical/soundtrack, longer and more complex than average.
2. **The binary threshold (4.76) is the median of this subset** — balanced classes, but both classes are "objectively decent" music. The classifier learns subtle quality signals.
3. **Genre bias toward classical is real but acceptable** — our 32 features are mostly genre-agnostic (entropy, intervals, consonance). We'll verify with feature importance analysis.
4. **Popularity is orthogonal to quality** — ratings carry genuine signal about musical quality.
5. **The Isolation Forest covers the gap** — trained on 25K+ files (rated + unrated), it catches "this doesn't look like human music at all," which the XGBoost classifier can't do since it only saw good-to-great music.
