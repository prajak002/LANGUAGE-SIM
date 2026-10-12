# Form-based baseline on Wiktionary's route labels: report

_2026-10-11. Plan: `docs/baseline_plan.md` v1.0 (frozen, SHA-256 `9e3d39c7…b32d`). Script: `scripts/baseline.py`. Output: `data/baseline_v1/`. Decision log 76–77._

**Read this first.**
- **The labels are Wiktionary's and are not validated.** Every score says how well word form predicts Wiktionary's label, not how well it predicts history.
- Classes are roughly balanced by the sampling design (up to 400 pages per category), so scores do not describe performance on running vocabulary.
- This is not the classifier study of `research.md` RQ1–RQ3, and `research.md` §13 stays empty.

## 1. Data

12,777 items from the audit sample: senses that state exactly one route from the ancestor and give an ancestor form. Left out: 1,436 senses with no single route from the ancestor, 74 with an empty word or etymon, 28 duplicates, and all 648 Urdu pages (script). 16 languages remain.

## 2. A1: inherited against learned, 5-fold cross-validation (macro-F1)

| Ancestor | Language | Inherited | Learned | B0 | B1 distance | B2 word | B3 all | B1 transfer |
|---|---|---|---|---|---|---|---|---|
| Sanskrit | Assamese | 402 | 149 | 0.42 | 0.86 | 0.72 | 0.92 | 0.88 |
| Sanskrit | Bengali | 399 | 407 | 0.34 | 0.87 | 0.80 | 0.89 | 0.87 |
| Sanskrit | Gujarati | 372 | 401 | 0.34 | 0.93 | 0.87 | 0.96 | 0.93 |
| Sanskrit | Hindi | 390 | 410 | 0.34 | 0.89 | 0.80 | 0.93 | 0.90 |
| Sanskrit | Marathi | 394 | 358 | 0.34 | 0.87 | 0.83 | 0.90 | 0.89 |
| Sanskrit | Odia | 368 | 268 | 0.37 | 0.89 | 0.81 | 0.91 | 0.89 |
| Sanskrit | Punjabi | 353 | 222 | 0.38 | 0.80 | 0.80 | 0.86 | 0.74 |
| Latin | Catalan | 415 | 404 | 0.34 | 0.78 | 0.82 | 0.86 | 0.78 |
| Latin | French | 397 | 402 | 0.33 | 0.86 | 0.83 | 0.91 | 0.86 |
| Latin | Galician | 389 | 399 | 0.34 | 0.77 | 0.81 | 0.86 | 0.78 |
| Latin | Italian | 416 | 403 | 0.34 | 0.70 | 0.73 | 0.75 | 0.71 |
| Latin | Portuguese | 359 | 407 | 0.35 | 0.79 | 0.75 | 0.87 | 0.79 |
| Latin | Romanian | 415 | 401 | 0.34 | 0.81 | 0.81 | 0.87 | 0.78 |
| Latin | Spanish | 387 | 405 | 0.34 | 0.77 | 0.77 | 0.83 | 0.78 |
| Ancient Greek | Greek | 396 | 393 | 0.33 | 0.57 | 0.62 | 0.62 | – |
| Old Armenian | Armenian | 394 | 406 | 0.34 | 0.48 | 0.60 | 0.59 | – |

B0 is the majority class. "B1 transfer" is analysis A3: the one-feature model fitted on the other languages of the same ancestor. Accuracy and standard deviations are in `a1_cv.csv`.

- **Indo-Aryan:** one number, the edit distance between the word and its Sanskrit etymon, gives macro-F1 0.80 to 0.93. Adding character n-grams gives 0.86 to 0.96.
- **Romance:** the same feature gives 0.70 to 0.86; all features give 0.75 to 0.91.
- **Greek and Armenian:** form barely predicts the label (0.57 and 0.48 for the distance; 0.62 and 0.59 for all features). In both, inherited and learned words are almost equally close to the ancestor form (mean distance 0.10 against 0.04 for Greek, 0.12 against 0.11 for Armenian).

## 3. A2: where the semi-learned senses fall

| Ancestor | Language | Semi-learned items | Mean distance: inherited | semi-learned | learned | B1 predicts learned | B3 predicts learned |
|---|---|---|---|---|---|---|---|
| Sanskrit | Bengali | 43 | 0.58 | 0.43 | 0.10 | 12/43 (17–43%) | 14/43 (20–47%) |
| Sanskrit | Gujarati | 30 | 0.65 | 0.35 | 0.05 | 15/30 (33–67%) | 15/30 (33–67%) |
| Sanskrit | Hindi | 96 | 0.62 | 0.48 | 0.09 | 29/96 (22–40%) | 23/96 (17–33%) |
| Sanskrit | Punjabi | 35 | 0.75 | 0.65 | 0.31 | 9/35 (14–42%) | 12/35 (21–51%) |
| Latin | Catalan | 70 | 0.44 | 0.34 | 0.20 | 30/70 (32–55%) | 32/70 (35–57%) |
| Latin | French | 25 | 0.52 | 0.39 | 0.22 | 11/25 (27–63%) | 12/25 (30–66%) |
| Latin | Galician | 26 | 0.46 | 0.48 | 0.24 | 4/26 (6–34%) | 6/26 (11–42%) |
| Latin | Italian | 58 | 0.41 | 0.35 | 0.25 | 21/58 (25–49%) | 39/58 (54–78%) |
| Latin | Portuguese | 129 | 0.45 | 0.36 | 0.23 | 62/129 (40–57%) | 74/129 (49–66%) |
| Latin | Spanish | 128 | 0.45 | 0.36 | 0.24 | 56/128 (35–52%) | 73/128 (48–65%) |
| Old Armenian | Armenian | 31 | 0.12 | 0.21 | 0.11 | 19/31 (44–76%) | 17/31 (38–71%) |

Languages with fewer than 20 semi-learned items are skipped as planned (Greek, Romanian, Assamese, Marathi, Odia). Intervals are Wilson 95%.

- **In 9 of the 11 languages the semi-learned items lie between the inherited and the learned items in mean distance.** The exceptions are Galician and Armenian, where they are the farthest from the ancestor form.
- **A two-class model splits them.** The share called "learned" runs from 15% (Galician, B1) to 67% (Italian, B3); in no language does either model put the class clearly on one side. A model trained on inherited and learned senses has no stable answer for this class.

## 4. A3: transfer within a family

The one-feature model fitted on the other languages of the family scores within a few points of the model fitted on the language itself (table above, last column). Related languages are not independent, so this shows that the form signal is shared, and nothing more.

## 4b. Leakage check (added after the planned run; not in the frozen plan)

**Question:** do the scores depend on the same ancestor form, or the same word, falling in both the training and the test fold? `scripts/baseline_leakage_check.py` repeats A1 with folds grouped by etymon, so that all items sharing an ancestor form stay together. Output: `data/baseline_v1/leakage_check.csv`.

- **Shared forms are uncommon.** Items sharing an etymon with another item of the language: 1.2% (Italian) to 18.3% (Punjabi). Items sharing a normalised word: 0.3% to 7.6%.
- **Grouping changes little.** B3 macro-F1 falls by at most 0.013 (Hindi 0.935 to 0.922) and rises slightly in some languages; B1 changes by at most 0.041 (Armenian, upward) and by under 0.01 elsewhere. The ungrouped run reproduces A1 exactly.
- **What this does not rule out:** related words with different etyma (derivatives, compounds) can still fall on both sides of a split.

**Class distributions and features, for reference.** Items per class and language are in the A1 table (inherited 353–416, learned 149–410). B1 has one feature. B2 and B3 use `TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3))`, fitted on the training fold only. Folds: `StratifiedKFold(5, shuffle=True, random_state=20261011)`.

## 5. What this does and does not show

- **It shows** that Wiktionary's inherited/learned labels for Indo-Aryan and Romance are largely predictable from surface closeness to the ancestor form, that this is not so for Greek and Armenian, and that the semi-learned class is intermediate and small.
- **It does not show that the labels are right.** If editors mark a word "learned" partly because it looks like its etymon, a high score is circular. This is the same warning as in the audit: the route claim is rarely sourced.
- **It does not replicate any published system.** The models are deliberately minimal.

## 6. Limits

- The etymon comes from the same entry as the label.
- Senses with several routes were left out, which removes the hardest cases.
- Script mapping for Bengali, Gujarati, Gurmukhi and Odia is by code-point offset, which is approximate for a few letters. Assamese items use the Bengali block.
- No hyperparameter was tuned and no significance test was run; differences of a few points between models are within fold-to-fold variation in several languages.

## 7. Reproduce

```
uv venv .venv && uv pip install --python .venv/bin/python scikit-learn
.venv/bin/python tests/test_baseline_helpers.py
.venv/bin/python scripts/baseline.py data/raw/wiktionary/crosslingual_v1 data/baseline_v1
```
