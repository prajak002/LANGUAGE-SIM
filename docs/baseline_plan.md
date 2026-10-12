# Form-based baseline on Wiktionary's route labels: plan v1.0 (FROZEN)

_2026-10-11. Frozen before any feature was computed or any model was fitted. SHA-256 in `docs/decision_log.md` (entry 76). Approved by the project lead ("a simple baseline on these labels … please make it perfect")._

## 1. What it tests, and what it cannot

**The labels are Wiktionary's and are not validated.** A score here says how well word form predicts *Wiktionary's label*. It is not accuracy against history. Three questions are fixed in advance:

- **Q1.** How well does word form separate Wiktionary's inherited from learned senses, per language?
- **Q2.** Where do Wiktionary's semi-learned senses fall for a model trained only on inherited and learned senses? If the class is intermediate in form, a two-class model has no stable answer for it.
- **Q3.** Does the simplest form signal transfer between languages that share an ancestor?

No large model is used, nothing is downloaded except the scikit-learn package, and no API is called. `research.md` §13 stays empty: this is not the classifier study of RQ1–RQ3.

## 2. Data

- The senses of the cross-lingual audit sample (`data/raw/wiktionary/crosslingual_v1/`, plan v1.0), read with the corrected template reader.
- **An item** is a sense that states exactly one route from the ancestor (INH, LRN or SEMI) and gives an ancestor form (the etymon). If a sense gives several ancestor forms, the first is used. Duplicate (language, word, etymon, route) items are dropped. A word whose senses have different routes contributes one item per route and is kept.
- **Excluded:** Urdu (its script cannot be compared with Devanagari etyma by the method below); items with an empty etymon after normalisation; reconstructed etyma keep their form with the asterisk removed.
- **Normalisation, applied to word and etymon:** Unicode NFD, combining marks removed, lower case, hyphens and spaces removed. Bengali, Gujarati, Gurmukhi and Odia letters are mapped to Devanagari by code-point offset; Indic vowel signs and the virama are kept (they are not combining marks of category Mn in the sense used here: all characters of the Devanagari block are kept after mapping).
- The sample has up to 400 pages per category, so **classes are roughly balanced by design and do not reflect their share of the vocabulary.**

## 3. Models

| Name | Input | Model |
|---|---|---|
| B0 | none | majority class |
| B1 | normalised edit distance between word and etymon (Levenshtein distance divided by the longer length) | logistic regression on one feature |
| B2 | the word only: character 1–3-grams with word boundaries, TF-IDF | logistic regression |
| B3 | B1's feature, B2's features, and the same n-grams of the etymon | logistic regression |

scikit-learn defaults, `max_iter=1000`, `random_state=20261011`. No tuning.

## 4. Analyses

- **A1 (Q1).** Per language, inherited against learned, stratified 5-fold cross-validation (`random_state=20261011`). Reported: accuracy and macro-F1 as mean and standard deviation over folds, for B0–B3. A language needs at least 50 items in each class.
- **A2 (Q2).** Per language with at least 20 semi-learned items: B1 and B3 are fitted on all inherited and learned items, then applied to the semi-learned items. Reported: the share predicted "learned" with a Wilson 95% interval, and the mean normalised edit distance of the inherited, semi-learned and learned items.
- **A3 (Q3).** For Sanskrit and Latin: B1 fitted on all languages of the ancestor but one, tested on the held-out language. Reported: accuracy and macro-F1 per held-out language.
- Everything planned is reported, whatever the outcome.

## 5. Limits fixed in advance

- Wiktionary may assign "learned" partly because a word looks like its etymon. A high score can therefore be circular, and is not evidence that the labels are right.
- The etymon is taken from the same entry that gives the label.
- Languages of one family are related, so A3 is not an independent test.
