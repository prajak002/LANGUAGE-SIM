# Supplementary analysis S10: three input conditions on identical items and grouped folds. Plan v1.0 (FROZEN)

_2026-10-12. Frozen after S8a and S8c were reported and before this comparison was computed. SHA-256 in `docs/decision_log.md` (entry 102). Added in response to an external review the project lead supplied, which asked for a direct test of what the intermediate form adds. The Jambu copy of Turner is downloaded again to a temporary folder, for analysis only, and deleted._

## Question

On the same items and the same folds, how does a model do with (A0) the modern word only, (A1) the word and the ancestor form, (A2) the word, the ancestor form and the intermediate form?

## Fixed here

- **Items:** the S8a linked items (seven Indo-Aryan languages; inherited or learned; a Pali or Prakrit form under the matched Turner head-word).
- **Folds:** per language, 5 folds stratified by route and **grouped by etymon**, so that items sharing an ancestor form are never split between training and test (`StratifiedGroupKFold`, seed 20261011). The same folds for all three conditions.
- **Models:** logistic regression, settings and seed of the baseline, nothing tuned.
  - A0: character 1–3-grams of the word (the baseline's B2).
  - A1: A0 plus character 1–3-grams of the ancestor form and the distance between word and ancestor (the baseline's B3).
  - A2: A1 plus character 1–3-grams of the intermediate form (transliterated and normalised as in S8a, the form closest to the word) and the two S8a link distances.
- **Reported:** pooled over languages and per language, from out-of-fold predictions: macro-F1, F1 for each route, and accuracy with Wilson 95% intervals on congruent, middle and dissociated items (S2 definition, unchanged); item counts everywhere.

## Reading fixed in advance

- S8a already found that two link distances do not help on dissociated items. If A2 is not clearly better than A1 on dissociated items (intervals overlap), that negative result stands with a richer model and grouped folds. If A2 is clearly better, the paper's statement that the link "does not repair the model" must be withdrawn.
- A0 against A1 shows what the ancestor form adds; it is the paper's existing comparison under grouped folds on this item set.
- The dissociated subset is defined from the distance to the ancestor and the label, a feature of A1 and A2. It is a diagnostic split, not an independent test set, and is described as such.
