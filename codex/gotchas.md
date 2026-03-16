# Gotchas

Things that bit us or will bite future agents.

## G1: sklearn removed `squared` param from `mean_squared_error`

**What:** `mean_squared_error(y, y_pred, squared=False)` raises `TypeError` in scikit-learn >= 1.8.

**Fix:** Use `mean_squared_error(y, y_pred) ** 0.5` instead.

---

## G2: numpy bools are not Python bools

**What:** `isinstance(np.True_, bool)` returns `False` in some numpy versions. Isolation Forest's `.predict()` returns numpy scalars.

**Fix:** Always wrap with `bool()` when storing results that need to be Python-native (e.g., for JSON serialization or `isinstance` checks).

---

## G3: MuseScore 4 CLI audio export is broken

**What:** `musescore4 -o output.mp3 score.musicxml` produces silent MP3 files. Known bug since MuseScore 4.1.1 (GitHub issue #19160).

**Fix:** Use `musescore3` for CLI audio rendering. MuseScore 4 works fine for GUI viewing.

---

## G4: music21 `converter.parse()` is slow and not thread-safe

**What:** Parsing a single MusicXML file takes 0.5-2s. music21 uses global state internally, so threading doesn't help — must use multiprocessing.

**Fix:** `multiprocessing.Pool` with `imap_unordered` for parallel extraction. Worker processes suppress music21's verbose logging.

---

## G5: PDMX rating=0 means unrated, not zero stars

**What:** The `rating` column in PDMX.csv uses 0 to indicate "no ratings received", not "rated zero." Must filter these before training.

**Fix:** `df = df[df["rating"] > 0]` and also filter by `n_ratings >= 3` for reliability.

---

## G6: MusicXML `<divisions>` math

**What:** Duration values in MusicXML are relative to `<divisions>`, which defines how many units equal one quarter note. With divisions=4: quarter=4, eighth=2, half=8, dotted half=12, whole=16.

**Fix:** Always set divisions in the first measure's `<attributes>` and be consistent. Mismatched divisions between parts will cause MuseScore import warnings.

---

## G7: pyproject.toml build backend

**What:** `setuptools.backends._legacy:_Backend` doesn't exist in current setuptools. Causes `BackendUnavailable` error on `pip install -e`.

**Fix:** Use `setuptools.build_meta` as the build backend. Also need `[tool.setuptools.packages.find]` with `include = ["musiclaude*"]` or setuptools can't discover the package.

---

## G8: XGBoost GPU prediction device mismatch warning

**What:** When XGBoost trains on CUDA but predicts on a CPU DataFrame, it warns about "mismatched devices" and falls back to CPU for prediction.

**Impact:** Harmless for inference (prediction is fast regardless). Only matters for training throughput.
