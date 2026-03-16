# Classifier Architecture

## Two-Signal Design

Quality assessment uses two independent signals that must both pass:

```
MusicXML → Feature Extraction (32 features)
                ↓
    ┌───────────┴───────────┐
    │                       │
Signal 1: XGBoost        Signal 2: Isolation Forest
(supervised)             (unsupervised)
    │                       │
"Is this rated          "Does this look
 highly by humans?"      like real music?"
    │                       │
    └───────────┬───────────┘
                ↓
         Combined Assessment
         (both must pass)
```

### Signal 1: XGBoost (Rating Prediction)

- **Binary classifier:** good (rating ≥ 4.0) vs not good
- **Regressor:** predicts continuous 1-5 rating
- **Trained on:** PDMX scores with ≥ 3 user ratings
- **GPU accelerated:** auto-detects CUDA, uses `device="cuda"` with `tree_method="hist"`
- **Strengths:** Directly optimizes for the target variable. Feature importance is interpretable.
- **Weakness:** Distribution shift — trained on human music, applied to LLM music. May learn proxies (longer = better) rather than musical quality.

### Signal 2: Distribution Scorer (Anomaly Detection)

- **Isolation Forest:** fitted on ALL PDMX feature data (not just rated scores)
- **Per-feature z-scores:** robust statistics (median + IQR) for interpretability
- **Human-readable critiques:** template-based explanations for deviations > 2 IQR
- **Strengths:** Catches LLM-specific failure modes that XGBoost can't — missing rests, no phrase structure, random-walk melody. Works regardless of rating quality.
- **Weakness:** Can't distinguish "unusual but good" (intentional avant-garde) from "unusual and bad" (LLM artifact).

### Why Both?

XGBoost alone might pass a score that's "typical" but actually bad (generic, uninspired). The distribution scorer alone might flag intentionally unusual music. Together, a composition needs to both look like real music AND match patterns of highly-rated music.

## Model Artifacts

All saved to `models/` as `.joblib` files:

| File | Contents |
|------|----------|
| `quality_classifier.joblib` | XGBoost binary model + metrics + feature names |
| `quality_regressor.joblib` | XGBoost regression model + metrics + feature names |
| `distribution_scorer.joblib` | Fitted scaler, Isolation Forest, medians, IQRs, feature ranges |
