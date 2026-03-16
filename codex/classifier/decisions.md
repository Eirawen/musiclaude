# Classifier Decisions

## C1: Binary threshold at 4.0 stars

**What:** "Good" = rating ≥ 4.0 out of 5.0.

**Why:** 4.0 is the natural breakpoint for "clearly good" on a 5-star scale. Need to check PDMX rating distribution — if 80%+ of rated scores are ≥ 4.0, the threshold needs to move up or we need to rebalance.

---

## C2: Minimum 3 ratings filter

**What:** Training data excludes scores with fewer than 3 user ratings.

**Why:** A single rating is unreliable. 3 ratings provides some confidence that the rating reflects actual quality rather than one person's preference.

---

## C3: Isolation Forest contamination = 0.1

**What:** The anomaly detector assumes ~10% of PDMX data is "low quality."

**Why:** Default heuristic. With 250K scores, many will be incomplete, poorly arranged, or test uploads. 10% is conservative. Can tune after seeing the actual distribution.

---

## C4: RobustScaler instead of StandardScaler

**What:** Feature scaling uses median and IQR rather than mean and std.

**Why:** Musical features often have outliers (a score with 50 modulations, or 0 notes). Robust statistics aren't distorted by these extremes.

---

## C5: Distribution scorer fits on ALL data, not just rated data

**What:** The Isolation Forest is fitted on every score in PDMX, including unrated ones.

**Why:** We want the distribution of "what normal music looks like," not "what highly-rated music looks like." Unrated music is still human-composed music. More data = better distribution estimate.
