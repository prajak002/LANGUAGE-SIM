# Supplementary analysis S5: an open-weight language model on the dissociation subset: plan v1.0 (FROZEN)

_2026-10-11. Frozen before any model was downloaded or queried. SHA-256 in `docs/decision_log.md` (entry 82). Approved by the project lead ("you can use any open source LLM model"). Local inference only: no API, no spend._

## What it can and cannot show

- **Question.** Does a general-purpose language model reproduce Wiktionary's inherited / learned label, and does it, like the form-based baseline, do worse where the label goes against resemblance?
- **The labels are Wiktionary's and are not validated**, and the dissociated items are unvalidated candidates.
- **The model has very probably seen Wiktionary in training.** A high score on dissociated items therefore cannot be told apart from memorisation, and a low score cannot be told apart from Wiktionary being wrong.
- **Model output is never a label.** Nothing the model says is used to validate, correct or annotate any item.

## Items

From `data/baseline_v1/oof_predictions.csv.gz` (16 languages): **all dissociated items**, and, for each language, **as many congruent items as it has dissociated ones** (all, if fewer), taken in ascending order of `SHA-256("s5-v1|" + lang + "|" + title + "|" + route)`. Middle items are not used.

## Model and settings

- One open-weight model run locally through Ollama, chosen before any item is queried by this rule: the first of `gemma3:4b`, `qwen2.5:7b`, `llama3.1:8b` that downloads and answers a one-line test prompt unrelated to the items. Its name and digest are recorded.
- `temperature = 0`, `seed = 20261011`, at most 8 output tokens. One request per prompt; no retries on content; no prompt tuning after seeing any answer.

## Prompts (fixed)

Two conditions per item.

**Word only**
```
Language: {language}
Word: {word}
Question: Is this {language} word (A) {option_A}, or (B) {option_B}?
Answer with the single letter A or B.
```
**Word and source form**: the same, with the line `{ancestor} source form: {etymon}` after the word.

The two options are "inherited from {ancestor} by continuous transmission through the intermediate stages" and "a learned borrowing taken later directly from {ancestor}". Which one is A is fixed per item by the parity of the item's hash, so the answer letters are balanced.

## Scoring

- The answer is the first `A` or `B` in the output (upper-cased). Anything else is `unparsed`, counted as wrong, and reported.
- Per ancestor family and condition, on congruent and on dissociated items: agreement with Wiktionary's label, with counts and Wilson 95% intervals; the share of answers that are "learned"; the unparsed rate.
- Agreement between the model's answer and B3's out-of-fold prediction on the same items.
- Everything is reported, whatever it shows. If the model answers one letter for nearly everything, that is the result.
