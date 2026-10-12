# Supplementary analysis S5b: a larger open-weight model on the same items: plan v1.0 (FROZEN)

_2026-10-12. Frozen before the model was downloaded or queried. SHA-256 in `docs/decision_log.md` (entry 86). Requested by the project lead after the S5 null result ("add a stronger language model"); open-weight, local, no API and no spend._

## Why

In S5 a 4-billion-parameter model answered "inherited" about four times in five and was near chance, so S5 could not say whether a language model leans on resemblance. S5b repeats S5 with a larger model. **It is a rerun with one thing changed, the model.**

## What stays exactly as in `docs/supplementary_plan_s5.md` v1.0

The 2,180 items, both prompt texts, the assignment of answer letters, temperature 0, seed 20261011, at most 8 output tokens, the parsing rule, and the scoring by family, condition and subset. **The prompts are not adjusted in the light of S5**, although S5 showed an answer bias; changing them now would be tuning on the results.

## What changes

- **Model.** The first of `gemma3:12b`, `qwen2.5:14b`, `phi4:14b` that downloads, fits in this machine's memory (16 GB) and answers the same unrelated test prompt as in S5. Its name and digest are recorded. These are the largest general open-weight models that this machine can run; larger ones were not available to this project.
- **Reported in addition, fixed here because S5 showed it is needed:** the share of "learned" answers by Wiktionary route within each subset, so that bias can be told from accuracy; and a balanced score per family and subset, the mean of the share correct on inherited items and on learned items, for cells with at least 20 items of each route.

## Reading fixed in advance

- If the model is again near chance or answers one way almost always, S5b is a second null result and is reported as such.
- If it is clearly above chance on congruent items, the comparison with dissociated items is read with the same cautions as in S5: Wiktionary's labels are unvalidated, the model has probably seen Wiktionary, and a high dissociated score cannot be told apart from memorisation.
- **Model output is never a label.**
