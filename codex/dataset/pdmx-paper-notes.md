# PDMX Paper Notes

**Paper:** "PDMX: A Large-Scale Public Domain MusicXML Dataset for Symbolic Music Processing" (arXiv:2409.10831v1)

## Key Findings Relevant to MusicLaude

### They Validated Our Approach
- Higher-rated compositions have higher PCE (pitch class entropy) and lower SC (scale consistency)
- This matches our experiments 001 and 002 exactly: pitch_class_entropy is top-5, scale_consistency has r=-0.20 with rating
- Their fine-tuning threshold: 4.74 stars (top 50% of rated). Ours: 4.76. Arrived at independently.
- Their R∩D (rated + deduplicated) subset "consistently shows highest scores" — validates our exp 002 dedup decision

### Deduplication Strategy (how subset:rated_deduplicated works)
1. **Title matching**: Sentence-BERT embeddings with 80% similarity threshold on title/subtitle/artist/composer
2. **Instrumentation grouping**: Separate by instrument configuration
3. **Best selection**: Within each cluster, pick highest-rated; ties broken by note count
- Removed ~60% of the dataset (151K songs)
- 85% of all songs had no duplicates; 95% of rated songs were unique

### Their Model Training
- 20M parameter decoder-only transformer, REMI+ tokenization
- Single A6000 GPU, 100K steps, batch 12
- Fine-tuning: 5K steps at 5e-5 on top-50% rated
- Finding: rated subsets → more harmonically/rhythmically diverse generations
- After fine-tuning, models converged in quality regardless of base training subset

### Their Listening Study Design (STEAL THIS)
12 participants rated 30 samples on 3 axes (0-100 scale):
- **Correctness**: "Is the music free of inharmonious notes, unnatural rhythms, and awkward phrasing?"
- **Richness**: "Is the sample musically/harmonically interesting?"
- **Quality**: Overall subjective preference

This is better than our A/B preference design. Three axes give richer signal and separate "technically correct" from "musically interesting."

### MusicRender Format
Extended MusPy library that preserves what MusicXML has over MIDI:
- 12M performance directives (tempo text, dynamic hairpins, articulations)
- Section markings and phrase boundaries
- Lyrics (10M+ tokens)
- Note articulation and expression data

We're only counting dynamics_count. Could extract: hairpin_count, articulation_count, tempo_text_count, section_mark_count as separate features.

### Data Quality Notes
- 67% of songs lack genre tags (only 50% of total notes lack genre annotation — bigger pieces tend to have genres)
- Rating range 2.83-4.98 (not 0-5)
- >90% of pieces have <5 tracks; only ~3% exceed 5 (orchestral underrepresented)
- Groove consistency had minimal variation across subsets — rhythm is less differentiating than harmony

## Ideas for Future Experiments

1. **Update listening study to 3-axis** (Correctness / Richness / Quality, 0-100 scale)
2. **Disaggregate dynamics_count** into hairpins, spot dynamics, articulations, tempo text — the paper found 12M performance directives, suggesting this is rich signal
3. **Add lyrics/annotations as features** — has_lyrics, n_annotations might correlate with quality
4. **Try REMI+ tokenization** for LLM composition instead of raw MusicXML — more compact
5. **Compare our 35-feature XGBoost vs their 20M transformer** — different approaches to quality, could be complementary
