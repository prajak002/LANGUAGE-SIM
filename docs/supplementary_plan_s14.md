# Supplementary analysis S14: can anything other than form do better on the dissociated items? Plan v1.0 (FROZEN)

_2026-10-13, about 12:25. Frozen before any number below was computed. SHA-256 in `docs/decision_log.md`. Added because the project lead asked for better performance on the hard items. Nothing is fetched and no pretrained model is used: the inputs are the stored audit pages, the corrected baseline items and the stored Turner flags of S4._

## Seen before freezing

S2, S10, S11, S12 and S13 results, including that three models with the ancestor form are at or below chance on the dissociated items; the S7a counts (among near-Sanskrit words whose etymon heads a Turner article, a matching form is listed for 57 of 125 called inherited and 100 of 1,001 called learned); and 36 dissociated inherited items read by the assistant earlier today. No S14 feature had been computed.

## Question

On the items where label and resemblance disagree, does a model do better when it is given (a) the meaning of the word, (b) a dictionary record, or (c) training weights that stop it from leaning on the distance?

## Fixed here

- **Items and folds:** the S2 items of `data/baseline_v2/items.csv.gz` (inherited or learned) in the seven languages descended from Sanskrit and the seven Romance languages; per language, the S2 folds (`StratifiedKFold(5, shuffle=True, random_state=20261011)`). Subsets as S2 (0.15 and 0.5).
- **Model:** logistic regression with the baseline's settings and seed; nothing tuned.
- **Meaning features (M):** from the item's own etymology chunk of the stored page, the definition lines (lines beginning `# `), with templates removed, links reduced to their text and markup stripped, lower-cased; TF-IDF of word 1–2-grams fitted on the training fold; plus the part-of-speech headings of the chunk as tokens. The Etymology section itself, usage examples, and quotations are not read.
- **Record features (T), Sanskrit family only:** the stored S4 flags T1, T2, T3 of the item, and the product of T3 with an indicator that the distance is at most 0.15. An item with no flag row gets zeros.
- **Weights (W):** each training item is weighted by the inverse of the size, in the training fold, of its group, where a group is route by distance band (at most 0.15; between; at least 0.5); weights are scaled to mean 1.
- **Conditions:** B2 and B3 (reference; B3 must reproduce 27 of 260 and 52 of 272, otherwise stop); M alone; B2+M; B3+M; B3+W; B3+M+W; and for the Sanskrit family B3+T and B3+M+T+W.
- **Reported, per family and per language, from out-of-fold predictions:** macro-F1, and accuracy with Wilson 95% intervals on congruent, middle and dissociated items, also split by route. Written to `data/baseline_v2/s14_scores.csv`, `s14_by_subset.csv`, and per-item predictions to `s14_oof.csv.gz` (no Turner form is in it; the flags are not written).

## Reading fixed in advance

- A condition is said to do better on the dissociated items only if the Wilson interval of its accuracy there lies wholly above B3's in that family. Its accuracy on congruent items and its macro-F1 are always given beside it. All conditions are reported; none is chosen afterwards as "the model".
- Meaning and weights are not form. If either helps, the paper says that a cue other than form helps, and that meaning is a correlate of the label (basic vocabulary against learned vocabulary) and not evidence of the route of a word.
- The Turner flags are the dictionary that Wiktionary's editors cite, read by a matcher that errs in both directions. If T helps, that is agreement with the labels' own source and is described so. Given the S7a counts (57 inherited against 100 learned among near-Sanskrit words with a listed form), T is not expected to help.
- If nothing clears the bar, that is reported as a further negative result.
- The labels are unvalidated. A higher score on the dissociated items is closer agreement with Wiktionary, not historical accuracy.
