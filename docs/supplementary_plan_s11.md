# Supplementary analysis S11: a character Transformer on the three input conditions. Plan v1.0 (FROZEN)

_2026-10-12. Frozen after S10 was reported and before any neural model was trained or any S11 number computed. SHA-256 in `docs/decision_log.md` (entry 105). Added because the project lead asked for a stronger model and offered a GPU. The Jambu copy of Turner is downloaded to a temporary folder on the machine that runs the script, for analysis only, and deleted there afterwards; no Turner form is written to an output file._

## Question

S10 found that a linear model given the intermediate form does no better on the dissociated items than one given the ancestor form only. Does a neural sequence model, which can learn correspondences between the three forms, change that?

## Not in this analysis

No route or path is predicted or scored: there are no reference paths. No pretrained model is used and none is downloaded. Nothing is tuned.

## Fixed here

- **Items:** the S10 items (seven Indo-Aryan languages; inherited or learned; a Pali or Prakrit form under the matched Turner head-word; the form closest to the word, chosen as in S8a).
- **Folds:** the seven languages are pooled. 5 folds, stratified by language and route together, **grouped by etymon over all languages**, so that an ancestor form never appears in both training and test, in any language (`StratifiedGroupKFold`, seed 20261011). These folds differ from S10's per-language folds, so the S10 logistic models are rerun on them as the reference (A0, A1, A2, settings unchanged, one model over the pooled languages).
- **Input:** Latin transliteration with diacritics kept (vowel length, retroflexion, sibilants, aspiration), decomposed to base letters and combining marks, one token each. Sequence: a start token, a language token, the word, a separator, the ancestor form, a separator, the intermediate form; each form has its own segment embedding. Vocabulary from the training fold only; unseen characters map to one unknown token. Length cut at 96 tokens.
- **Model:** Transformer encoder trained from random initialisation: 3 layers, width 128, 4 heads, feed-forward 256, dropout 0.1, learned positions; the start token's output goes to one logistic unit.
- **Training:** AdamW, learning rate 0.001, weight decay 0.01, batch 64, 30 epochs, gradient norm clipped at 1.0, no early stopping and no development set. 5 seeds (20261011 to 20261015) per fold and condition.
- **Conditions:** T0 word only; T1 word and ancestor form; T2 word, ancestor form and intermediate form.
- **Prediction:** the mean of the 5 seeds' probabilities, threshold 0.5. The range of macro-F1 over single seeds is also reported.
- **Reported:** for A0–A2 and T0–T2, pooled and per language, from out-of-fold predictions: macro-F1, F1 per route, accuracy with Wilson 95% intervals on congruent, middle and dissociated items (S2 definition, unchanged), with counts.
- **Abstention (T1 and T2):** items ranked by |p − 0.5|; at coverage 100, 90, 80, 70 and 50% of items: accuracy on the items kept, how many dissociated items are kept, and accuracy on those.

## Reading fixed in advance

- If T2 is not clearly better than T1 on the dissociated items (Wilson intervals overlap), the statement that the intermediate form does not repair the model stands for a neural model as well. If T2 is clearly better, the statement must be limited to linear models and the paper changed.
- If T1 is clearly better than A1 on the dissociated items, a stronger model recovers part of what the linear one misses, and the paper must say so.
- Abstention is useful only if the dissociated items are over-represented among the items dropped. If they are kept at about their overall rate, confidence does not identify them.
- The dissociated subset is a diagnostic split defined from the label and a distance; the labels are Wiktionary's and are not validated. A result here is about agreement with those labels.
- Whichever way it falls, the result is reported.
