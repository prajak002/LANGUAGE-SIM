# Supplementary analysis S12: a pretrained character-level model on the three input conditions. Plan v1.0 (FROZEN)

_2026-10-12. Frozen after S11 was reported and before any pretrained model was loaded or any S12 number computed. SHA-256 in `docs/decision_log.md` (entry 108). Added because the project lead asked for a Transformer run on a GPU; S11 trained a small one from random initialisation, and the open question a GPU can answer is whether a pretrained model behaves differently. The run is on a hosted GPU notebook. The Jambu copy of Turner is downloaded there to a temporary folder, for analysis only, and deleted there at the end of the run; no Turner form is written to an output file._

## Question

Does a pretrained multilingual character-level model, fine-tuned on the same items and folds as S11, do better on the dissociated items, and does the intermediate form help it?

## Not in this analysis

No route or path is predicted or scored. Nothing is tuned: one model, one set of settings, fixed here.

## Fixed here

- **Items and folds:** exactly those of S11 (3,276 linked items; seven languages pooled; 5 folds stratified by language and route, grouped by etymon over all languages; seed 20261011). The script stops if the item count differs.
- **Model:** `google/canine-s` (Clark et al. 2022), all weights fine-tuned, one linear output unit on the pooled output.
- **Input:** one string: the language name, the word, the ancestor form and the intermediate form, in the S11 transliteration with diacritics, joined by the tokenizer's separator; cut at 128 characters.
- **Training:** AdamW, learning rate 3e-5, weight decay 0.01, linear warm-up over the first 10% of steps and linear decay after, batch 32, 8 epochs, gradient norm clipped at 1.0, mixed precision on a GPU, no early stopping and no development set. 3 seeds (20261011 to 20261013) per fold and condition.
- **Conditions:** C0 word only; C1 word and ancestor form; C2 word, ancestor form and intermediate form.
- **Prediction and reporting:** as in S11 (mean probability over seeds, threshold 0.5; macro-F1, F1 per route, accuracy with Wilson 95% intervals by subset, the range of macro-F1 over single seeds; abstention table for C1 and C2).

## Reading fixed in advance

- If C2 is not clearly better than C1 on the dissociated items (Wilson intervals overlap), the statement that the intermediate form does not repair the model stands for a pretrained model too. If it is clearly better, the paper must say so and the statement is limited to the models where it holds.
- If C1 or C2 clearly beats the word-only models (A0, T0, C0) on the dissociated items, a pretrained model recovers something from the forms that the others do not, and the paper's claim that form does not decide these items must be weakened accordingly.
- Fine-tuning on a few thousand items can fail for some seeds (a model that predicts one class). Such runs are kept and counted; the single-seed range shows them.
- The paper cites the model only if the result is reported in it, and the citation is checked against the published record first.
- Whichever way it falls, the result is reported. If the run cannot be completed and checked before the submission deadline, the paper is submitted without it and this plan stays open.
