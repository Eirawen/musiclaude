# Classifier Architecture

## Three-Signal Design

Quality assessment uses three signals. The feature profile is the primary feedback mechanism; XGBoost and distribution scoring are secondary references.

```
MusicXML → Feature Extraction (42+ features)
                ↓
    ┌───────────┼───────────────────┐
    │           │                   │
Signal 1:    Signal 2:          Signal 3:
Feature      XGBoost             Isolation Forest
Profile      (supervised)        (unsupervised)
(primary)    (secondary ref)     (anomaly gate)
    │           │                   │
"Where does  "Predicted         "Does this look
 this sit     rating: 4.6"       like real music?"
 vs high-
 rated music?"
    │           │                   │
    ↓           └─────────┬─────────┘
Ranked                    ↓
improvement          Pass/fail gate
instructions         (both must pass)
(the actual
 feedback)
```

### Signal 1: Feature Profile (Primary — the actual feedback)

- **What:** Compares each feature against percentile distributions from high-rated PDMX music
- **Ranking:** Gaps weighted by XGBoost feature importance → priority-ordered improvement list
- **Output:** Specific instructions like "dynamics_count=0, percentile 3, target median 8. Add dynamic markings."
- **Delta tracking:** Shows what improved/regressed between iterations
- **Code:** `musiclaude/classifier/profile.py`
- **Model:** `models/feature_profile.joblib`
- **Strengths:** Gives Claude actionable, specific, ranked instructions. Validated in blind listening test: +7.0 avg improvement over baseline (experiment 005).
- **Weakness:** Limited to features we can extract. Can't assess compositional structure, thematic development, or voice leading quality.

### Signal 2: XGBoost (Secondary reference — pass/fail gate)

- **Binary classifier:** good (rating >= 4.0) vs not good
- **Regressor:** predicts continuous 1-5 rating (R²=0.039 — unreliable as absolute score)
- **Trained on:** 5,207 deduplicated PDMX scores with >= 10 user ratings
- **Strengths:** Feature importance is stable across experiments and drives the profile ranking
- **Weakness:** Predictions are near-useless (narrow rating range, noisy labels). Blind test showed XGBoost feedback can *hurt* compositions (waltz: 88→82). Keep as reference only.

### Signal 3: Distribution Scorer (Anomaly detection gate)

- **Isolation Forest:** fitted on ALL 25.6K PDMX feature data (not just rated scores)
- **Per-feature z-scores:** robust statistics (median + IQR) for interpretability
- **Human-readable critiques:** template-based explanations for deviations > 2 IQR
- **Strengths:** Catches LLM failure modes — missing rests, no dynamics, random-walk melody
- **Weakness:** Can't distinguish "unusual but good" from "unusual and bad"

### Why This Hierarchy?

The blind A/B/C experiment (005) proved that profile feedback produces substantially better compositions than XGBoost score feedback. XGBoost predictions are noisy (R²=0.039) because PDMX ratings measure popularity, not quality. But XGBoost feature importance is stable and meaningful — it tells us *which features matter*, even if it can't predict ratings. The profile system uses this importance ranking to weight its feedback. The distribution scorer remains as a safety gate to catch compositions that look nothing like real music.

## Model Artifacts

All saved to `models/` as `.joblib` files:

| File | Contents | Role |
|------|----------|------|
| `feature_profile.joblib` | High/low stats, percentile arrays, feature importance | **Primary feedback** |
| `quality_classifier.joblib` | XGBoost binary model + metrics + feature names | Secondary reference |
| `quality_regressor.joblib` | XGBoost regression model + metrics + feature names | Secondary reference (importance source) |
| `distribution_scorer.joblib` | Fitted scaler, Isolation Forest, medians, IQRs | Anomaly gate |
