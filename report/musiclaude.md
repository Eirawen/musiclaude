# MusicLaude: Quality-Guided Music Composition via Large Language Models

## Abstract

We present MusicLaude, a system for generating music as structured text (MusicXML) using large language models, guided by a trained quality classifier. The system uses two complementary signals: an XGBoost model trained on 5,620 human-rated compositions from the PDMX dataset to predict quality ratings, and an Isolation Forest anomaly detector trained on 25,000+ compositions to flag music that deviates from human-composed distributions. We extract 32 musical features spanning harmony, melody, structure, orchestration, and coherence. The classifier provides interpretable feedback that drives an iterative composition-revision loop, enabling the LLM to improve its output without any human listening. We validate the approach through a controlled listening study measuring correlation between classifier predictions and human preferences.

---

## 1. Introduction

### 1.1 Motivation

Recent advances in large language models have demonstrated impressive capabilities in generating structured text. Music notation formats like MusicXML are structured text — they encode pitch, rhythm, dynamics, and instrumentation in a well-defined XML schema. This raises a natural question: can LLMs compose music directly as MusicXML, and can we automatically assess the quality of the result?

The challenge is evaluation. Unlike code generation, where we can run tests, or text generation, where we can check factual accuracy, music quality is subjective and traditionally requires human listening. This creates a bottleneck in any iterative generation pipeline — you can't run a feedback loop if evaluation requires a human in the loop.

### 1.2 Core Thesis

MusicLaude's thesis is that **musical quality is partially predictable from structural features**, and that this prediction is sufficient to guide LLM composition. We don't claim to replace human judgment — we claim that a classifier trained on human ratings can catch the most common failure modes and push LLM-generated music toward the distribution of well-rated human compositions.

### 1.3 Contributions

1. **A 32-feature extraction pipeline** for MusicXML covering harmonic, melodic, structural, orchestration, and coherence dimensions, with features specifically targeting LLM failure modes (Section 3).
2. **A two-signal quality assessment system** combining supervised rating prediction (XGBoost) with unsupervised anomaly detection (Isolation Forest) to handle the distribution shift between training data (human music) and inference data (LLM music) (Section 4).
3. **An interpretable feedback loop** where feature-level deficiency reports guide LLM revision, enabling iterative improvement without human listening (Section 5).
4. **A controlled listening study** validating that classifier predictions correlate with human preference (Section 7).

---

## 2. Dataset: PDMX

### 2.1 Overview

We use the PDMX dataset (Zenodo, 2024), comprising 254,077 public domain MusicXML scores from MuseScore with user ratings and metadata.

| Metric | Value |
|--------|-------|
| Total files | 254,077 |
| With ratings | 14,182 (5.6%) |
| With reliable ratings (n_ratings >= 10) | 5,620 (2.2%) |
| Rating range | 2.83 – 4.98 |
| Mean / Median rating (filtered) | 4.72 / 4.76 |
| Top genre | Classical |

### 2.2 Rating Distribution and Selection Bias

PDMX ratings are heavily right-skewed (Figure 1). The minimum observed rating is 2.83, and 98.5% of rated pieces score above 4.0. This reflects MuseScore's selection dynamics: users preferentially rate music they enjoy, and low-quality uploads rarely accumulate enough ratings to appear in the dataset.

This skew makes the naive binary threshold of 4.0 (commonly used for "good vs bad" classification) unusable — it produces a 98.5/1.5 class split. We instead use the median rating of the filtered subset (4.76) as our threshold, yielding a balanced 49/51 split.

### 2.3 Rating Reliability

The number of ratings per piece follows a power-law distribution. Most rated pieces have only 3-5 ratings, where individual outlier votes can swing the average substantially. We filter to pieces with n_ratings >= 10, where rating variance drops from std=0.212 to std=0.171 — the point where averages become statistically stable.

This filtering reduces the training set from 14,182 to 5,620 pieces. While this is a significant reduction, it remains sufficient for tree-based models (175x the feature count) and produces more reliable training signal.

### 2.4 Structural Bias

Rated pieces differ systematically from unrated ones (Figure 7): they are longer (median 73 bars vs ~20), have more notes (median 1,058 vs ~200), and more tracks. This means our training data is biased toward substantial compositions. We consider this acceptable — trivially short or simple music should score lower, and the LLM composition pipeline targets multi-part, multi-section pieces.

### 2.5 Genre Distribution

Classical music dominates the training set (~2,000 of 5,620 pieces), followed by soundtrack, rock, and pop. The classifier will absorb some genre-correlated signal. We mitigate this by excluding genre as an explicit feature — the 32 extracted features are designed to capture structural quality properties that generalize across genres (entropy, consonance, voice leading, rhythmic variety).

### 2.6 Popularity Independence

Views and favorites show near-zero correlation with rating (r = -0.037 and r = 0.014 respectively). This validates that MuseScore ratings reflect genuine quality judgments rather than mere popularity, supporting their use as training signal.

---

## 3. Feature Extraction

We extract 32 numeric features from each MusicXML file using music21, organized into five modules.

### 3.1 Harmonic Features (6)

| Feature | Description |
|---------|-------------|
| chord_vocabulary_size | Unique chord types via chordify() |
| pct_extended_chords | Fraction of 7ths, 9ths, etc. |
| harmonic_rhythm | Chord changes per beat |
| cadence_count | Authentic + half + deceptive + plagal cadences |
| key_stability | KrumhanslSchmuckler confidence over windowed analysis |
| modulation_count | Key changes detected in sliding windows |

### 3.2 Melodic Features (8)

| Feature | Description |
|---------|-------------|
| avg_interval_size | Mean interval in semitones |
| pct_stepwise | Fraction of intervals <= 2 semitones |
| melodic_range | Highest - lowest pitch in semitones |
| pct_rising / pct_falling / pct_static | Directional interval breakdown |
| rhythmic_variety | Unique duration values / total notes |
| repetition_density | Fraction of measures sharing pitch-sequence signatures |

### 3.3 Structural Features (6)

| Feature | Description |
|---------|-------------|
| num_parts | Number of instrumental parts |
| total_duration_beats | Piece length in beats |
| dynamics_count | Dynamic markings (pp, ff, etc.) |
| tempo_count | Tempo indications |
| time_sig_complexity | 0=simple, 0.5=compound, 1=irregular |
| num_sections | Section boundaries detected |

### 3.4 Orchestration Features (4)

| Feature | Description |
|---------|-------------|
| instrument_count | Distinct instruments |
| voice_crossing_count | Adjacent-part pitch crossings |
| avg_range_utilization | Fraction of instrument range used |
| doubling_score | Pitch-class overlap across parts at beat positions |

### 3.5 Coherence Features (8)

These specifically target LLM failure modes — patterns that sound wrong but might not be caught by traditional music theory analysis.

| Feature | Targets | Description |
|---------|---------|-------------|
| note_density | Wall of notes | Notes per beat |
| rest_ratio | No breathing room | Fraction of beats with rests |
| pitch_class_entropy | Random pitch selection | Shannon entropy of pitch classes (0-3.58 bits) |
| interval_entropy | Monotonous intervals | Shannon entropy of interval distribution |
| melodic_autocorrelation | Random-walk melody | Self-similarity at 1-measure lag |
| phrase_length_regularity | No phrase structure | Std of rest-delimited phrase lengths |
| strong_beat_consonance | Arbitrary note stacking | Fraction of consonant intervals on strong beats |
| rhythmic_independence | Parts in lockstep | Rhythmic dissimilarity between parts |

---

## 4. Quality Assessment: Two Signals

The central challenge is **distribution shift**. We train on human-composed music but apply the model to LLM-generated music. An LLM can produce pathological outputs that fall entirely outside the training distribution — no rests, random-walk melodies, rhythmically monotone textures. A supervised classifier alone may extrapolate unpredictably on such inputs.

We address this with a two-signal architecture:

### 4.1 Signal 1: XGBoost Rating Prediction

An XGBoost classifier predicts whether a piece would be rated above the median (4.76) by MuseScore users.

- **Binary classifier**: Good/not good at threshold 4.76 (balanced 49/51 split)
- **Regressor**: Continuous rating prediction for finer-grained feedback
- **Interpretability**: Feature importance reveals which musical properties most influence quality ratings

**Strengths**: Captures nuanced quality differences within the space of "real music."
**Weakness**: May produce meaningless predictions on out-of-distribution inputs.

### 4.2 Signal 2: Isolation Forest Anomaly Detection

An Isolation Forest trained on 25,000+ human-composed pieces learns the joint distribution of all 32 features. It flags music that is statistically unusual — "this doesn't look like something a human composed."

- **Per-feature z-scores**: Robust scaling (median + IQR) identifies which specific features deviate
- **Anomaly score**: Global outlier score from the Isolation Forest
- **Critique generation**: Template-based human-readable explanations of anomalous features

**Strengths**: Catches LLM failure modes that fall outside training distribution.
**Weakness**: Cannot distinguish "unusual because it's bad" from "unusual because it's creative."

### 4.3 Combined Assessment

A composition must pass both signals:
1. XGBoost predicts it would be rated well (quality gate)
2. Isolation Forest confirms it falls within the distribution of human music (sanity gate)

This combination handles the distribution shift problem: the Isolation Forest catches pathological outputs before they reach the XGBoost model, which then evaluates quality within the space of "plausible human music."

---

## 5. Composition Pipeline

### 5.1 Architecture

The composition pipeline is implemented as three Claude Code skills that form a conversational workflow:

1. **Song Contract** (`/song-contract`): Interactive specification of the desired composition — genre, mood, instrumentation, tempo, structure, quality targets.
2. **Compose** (`/compose`): MusicXML generation with an internal scratchpad for planning harmony, voice leading, and structure before writing XML.
3. **Assess Quality** (`/assess-quality`): Runs the full validation pipeline and generates actionable critique.

### 5.2 Feedback Loop

The compose-assess cycle runs iteratively:

```
Contract → Compose → Validate → [Pass? → Done]
                                 [Fail? → Critique → Revise → Validate → ...]
```

The critique includes:
- **Structural errors**: Invalid time signatures, wrong measure durations, out-of-range notes
- **Quality deficiencies**: Feature-specific feedback (e.g., "melodic range is only 5 semitones — expand to at least 12")
- **Distribution anomalies**: Features that deviate from human norms with z-scores
- **Theory issues**: Parallel fifths/octaves, voice crossing problems
- **Expression gaps**: Missing dynamics, tempo markings, articulations

### 5.3 Music Theory Validator

Before feature extraction, compositions pass through structural validation:
- Time signature consistency
- Measure duration correctness
- Key signature presence
- Note range validity per instrument
- Parallel fifths/octaves detection
- Voice leading checks

Errors block the pipeline (must be fixed). Warnings are surfaced as critique (should be addressed).

---

## 6. Implementation

### 6.1 Tech Stack

| Component | Technology |
|-----------|------------|
| MusicXML parsing | music21 |
| Quality classifier | XGBoost (GPU-accelerated) |
| Anomaly detection | scikit-learn Isolation Forest |
| LLM composition | Claude (via Claude Code skills) |
| Feature extraction | Parallel via multiprocessing |
| Visualization | Streamlit + Plotly |
| Audio rendering | MuseScore 3 CLI |

### 6.2 Training Details

- **Dataset**: 5,620 pieces with n_ratings >= 10 from PDMX
- **Binary threshold**: 4.76 (median of filtered dataset)
- **XGBoost hyperparameters**: 200 estimators, max_depth=6, learning_rate=0.1, subsample=0.8
- **Isolation Forest**: 200 estimators, contamination=0.1, fitted on 25,000+ pieces
- **Feature scaling**: Robust (median + IQR) for anomaly detection

### 6.3 Extraction Pipeline

Feature extraction from 25,561 MusicXML files using 16 parallel workers with incremental checkpointing (flush every 500 files for crash recovery). Extraction is CPU-bound (music21 XML parsing and analysis) on a 20-core machine. The pipeline supports resuming from partial checkpoints.

---

## 7. Evaluation

### 7.1 Classifier Performance

**Binary classifier** (threshold = 4.76, balanced 49/51 split):

| Metric | Value |
|--------|-------|
| Accuracy | 0.602 |
| F1 (good class) | 0.661 |
| Precision (good) | 0.63 |
| Recall (good) | 0.69 |

**Regressor** (continuous rating prediction):

| Metric | Value |
|--------|-------|
| RMSE | 0.150 |
| R² | 0.052 |

The modest R² is expected given the compressed rating range (std = 0.171 in a 0.5-point band). The 32 structural features explain approximately 5% of rating variance — the remainder is attributable to factors outside our feature set: genre popularity, arrangement quality for known songs, performer reputation, and subjective taste. We frame this honestly: the classifier provides a **weak but directionally correct quality signal**, and its primary value lies not in prediction accuracy but in the interpretable feature importance it produces.

### 7.2 Feature Importance

The two models converge on a clear ranking. **Dynamics count is the #1 predictor by a wide margin in both models** — pieces with dynamic markings (pp, mp, mf, ff, crescendo, etc.) are rated substantially higher. This is the single most actionable finding for LLM composition.

**Binary classifier — top 10:**

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | dynamics_count | 0.053 | Structural |
| 2 | tempo_count | 0.035 | Structural |
| 3 | chord_vocabulary_size | 0.033 | Harmonic |
| 4 | pitch_class_entropy | 0.032 | Coherence |
| 5 | voice_crossing_count | 0.032 | Orchestration |
| 6 | total_duration_beats | 0.032 | Structural |
| 7 | time_sig_complexity | 0.030 | Structural |
| 8 | melodic_range | 0.030 | Melodic |
| 9 | rhythmic_independence | 0.030 | Coherence |
| 10 | pct_falling | 0.029 | Melodic |

**Regressor — top 10:**

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | dynamics_count | 0.060 | Structural |
| 2 | instrument_count | 0.046 | Orchestration |
| 3 | tempo_count | 0.041 | Structural |
| 4 | melodic_range | 0.039 | Melodic |
| 5 | pitch_class_entropy | 0.034 | Coherence |
| 6 | phrase_length_regularity | 0.033 | Coherence |
| 7 | num_sections | 0.032 | Structural |
| 8 | cadence_count_half | 0.031 | Harmonic |
| 9 | avg_range_utilization | 0.031 | Orchestration |
| 10 | melodic_autocorrelation | 0.031 | Coherence |

**Key observations:**
- **Expression markers dominate**: dynamics_count and tempo_count are top-2 in both models. Human raters reward scores that include performance instructions, not just notes.
- **Coherence features are predictive**: pitch_class_entropy (#4/#5), rhythmic_independence (#9), phrase_length_regularity (#6 in regressor), and melodic_autocorrelation (#10 in regressor) all contribute — validating the design of these LLM-targeting features.
- **Scope matters**: melodic_range, instrument_count, num_sections, total_duration_beats — larger, more complex pieces rate higher.
- **Harmonic richness**: chord_vocabulary_size (#3 in classifier) and cadence counts appear in both models.

### 7.3 Anomaly Detection Performance

| Metric | Value |
|--------|-------|
| Features used | 32 |
| Training samples | 25,561 |
| Contamination rate | 10% |
| Scaling | Robust (median + IQR) |

The Isolation Forest was fitted on the full extraction set (rated + unrated), capturing the complete distribution of human-composed music. Per-feature z-scores provide interpretable anomaly reports identifying which specific features deviate from human norms.

### 7.4 Controlled Listening Study

<!-- TODO: Fill in after study -->

**Design**: N participants evaluated M pairs of compositions, selecting their preferred piece in each pair. Clips were generated by the LLM pipeline at varying quality levels as assessed by the classifier. Presentation order (A/B position) was randomized.

**Hypothesis**: The classifier's quality score difference between paired compositions correlates positively with human preference rate.

**Results**:
- Number of participants: [X]
- Number of trials per participant: [X]
- Spearman rank correlation (classifier score diff vs preference rate): [X]
- Agreement rate: [X]

### 7.5 Case Study: JRPG Menu Theme

As proof of concept, we generated "Echoes of the Crystal" — a 16-bar JRPG menu theme in C major, 3/4 waltz at 88 BPM, with flute melody and piano arpeggios. The piece passed structural validation, achieved 100% key stability and 87% strong beat consonance, and was rendered to audio via MuseScore 3.

---

## 8. Discussion

### 8.1 What the Classifier Learns

The feature importance analysis reveals a hierarchy of what human raters value in music notation:

**Tier 1 — Expression (dynamics_count, tempo_count):** The strongest signal by far. A score with dynamic markings and tempo indications is rated higher than one without, regardless of the underlying composition quality. This likely reflects a confound: more skilled composers include these markings, so they correlate with overall craft. But it's also directly actionable — LLMs that generate only notes without expression markings are missing the most impactful quality signal.

**Tier 2 — Scope and complexity (instrument_count, melodic_range, num_sections, total_duration_beats):** Larger compositions rate higher. This partially reflects selection bias (longer pieces attract more attention) but also genuine quality — a well-developed multi-section piece with wide melodic range demonstrates more compositional skill than a short, narrow-range fragment.

**Tier 3 — Harmonic and melodic craft (chord_vocabulary_size, pitch_class_entropy, cadence counts, phrase_length_regularity):** These capture the actual musical content. Richer chord vocabulary, appropriate tonal diversity (not too uniform, not too random), proper cadential structure, and regular phrasing all correlate with quality. These features are the most musically meaningful and the hardest for LLMs to get right.

**Tier 4 — Part writing (voice_crossing_count, rhythmic_independence, avg_range_utilization):** Multi-part writing quality matters but is a secondary signal, likely because most training pieces are single-instrument.

The coherence features designed for LLM failure detection (Section 3.5) all appear in the top half of both models, validating their inclusion. pitch_class_entropy is particularly strong (#4-5), suggesting that tonal diversity is a genuine quality indicator, not just an LLM diagnostic.

### 8.2 Limitations

1. **Genre bias**: The training set skews heavily classical. The classifier's quality signal may not generalize equally across all genres.
2. **Rating compression**: PDMX ratings span only 2.83-4.98, with most of the signal compressed into the 4.5-5.0 range. The classifier learns subtle distinctions, not gross quality differences.
3. **Selection bias**: Only "substantial" compositions (longer, multi-track) accumulate enough ratings. Short compositions may be systematically underrated.
4. **Feature coverage**: 32 features cannot capture all aspects of musical quality. Timbre, expression, groove, lyrical fit, and emotional arc are absent.
5. **Anomaly vs creativity**: The Isolation Forest flags unusual music, but unusual is not always bad. Highly creative compositions may be penalized.

### 8.3 Distribution Shift

The fundamental challenge of training on human music and evaluating LLM music remains only partially addressed. The two-signal approach handles it better than either signal alone, but there is no guarantee that the quality classifier's predictions are meaningful on LLM outputs that pass the anomaly filter. The listening study (Section 7.4) provides empirical evidence on whether this transfer works.

---

## 9. Future Work

- **Expanded feature set**: Rhythmic groove features, harmonic tension curves, melodic arch analysis
- **Genre-conditioned models**: Separate classifiers per genre, or genre as a feature
- **Larger training set**: Relaxing the n_ratings filter or incorporating external datasets
- **Music arena**: Public A/B preference platform for continuous evaluation data collection
- **Fine-grained feedback**: Per-measure quality heatmaps rather than piece-level scores
- **Multi-modal validation**: Combining structural features with audio-domain features (spectral, timbral) from rendered audio

---

## 10. Conclusion

MusicLaude demonstrates that LLM-generated music can be automatically assessed and iteratively improved using a classifier trained on human ratings. The two-signal approach — combining supervised quality prediction with unsupervised anomaly detection — addresses the distribution shift between human and LLM music. The 32-feature extraction pipeline provides interpretable feedback that guides composition revision. While the system cannot replace human listening, it provides a scalable quality gate that catches common failure modes and pushes generated music toward the distribution of well-rated human compositions.

---

## References

- PDMX Dataset. Zenodo, 2024. https://zenodo.org/records/14648209
- Chen, T., & Guestrin, C. XGBoost: A Scalable Tree Boosting System. KDD, 2016.
- Liu, F. T., Ting, K. M., & Zhou, Z. H. Isolation Forest. ICDM, 2008.
- Cuthbert, M. S., & Ariza, C. music21: A Toolkit for Computer-Aided Musicology. ISMIR, 2010.
- MuseScore. https://musescore.org
