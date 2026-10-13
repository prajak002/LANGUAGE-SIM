# Supplementary analysis S13: sensitivity of the dissociated split to its two thresholds. Plan v1.0 (FROZEN)

_2026-10-13. Frozen before any count below was computed. SHA-256 in `docs/decision_log.md`. Added in response to a review the project lead supplied, which called the thresholds 0.15 and 0.5 arbitrary and asked for a sensitivity analysis. No model is trained and nothing is fetched: this is a recount of the stored out-of-fold predictions._

## Question

Does the accuracy of B3 on dissociated items depend on where the near and far thresholds are put?

## Fixed here

- **Input:** `data/baseline_v2/oof_predictions.csv.gz`, unchanged (columns `norm_edit_distance`, `wiktionary_route`, `B3_learned`, `B2_learned`).
- **Grid:** near threshold in {0.05, 0.10, 0.15, 0.20, 0.25}; far threshold in {0.40, 0.50, 0.60}. All 15 pairs; (0.15, 0.50) is the reported one.
- **Definition:** as S2. Dissociated: inherited with distance at most the near threshold, or learned with distance at least the far threshold. Congruent: the reverse.
- **Families:** the seven languages descended from Sanskrit pooled; the seven Romance languages pooled; Greek and Armenian are not reported.
- **Reported, for every pair and family:** number of dissociated items, B3 correct with Wilson 95% interval, B2 (word only) correct, and B3 accuracy on congruent items. Written to `data/baseline_v2/s13_threshold_sensitivity.csv`.
- **Also reported, with no new computation:** the largest standard deviation of B3 macro-F1 across the five folds, read from `data/baseline_v2/a1_cv.csv`.

## Reading fixed in advance

- The paper may say the finding does not depend on the thresholds only if B3 accuracy on dissociated items stays below 50% for every one of the 15 pairs in both families, and the full range is given. If any pair reaches 50%, the paper says so and names it.
- This does not answer the objection that the split is defined by a feature of the model. It remains a diagnostic.
