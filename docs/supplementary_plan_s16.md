# Supplementary analysis S16: the two model passes over the dissociation sheets, against Wiktionary. Plan v1.0 (FROZEN)

_2026-10-13, about 13:05. Frozen before any count below was computed. SHA-256 in `docs/decision_log.md`. The project lead asked for the model-filled sheets (decision log, entry 129) to be reported in the paper._

## Seen before freezing

The sheets' label and source tallies (entry 129), and, from the log of the branch that filled them, one result for Hindi: agreement with Wiktionary on 11 of 12 decided controls and 5 of 16 decided dissociated items. Nothing else.

## What the sheets are

Two passes of one language model (Claude Sonnet 4.6) under two instruction sets, made by the project lead in another session, over the first kit's sheets (word only). 728 of 879 rows of pass A give no source beyond "Linguistic analysis". They are a language model's labels, mostly from the form of the word; they are not expert annotation. **Blindness is not guaranteed:** the session that filled the Hindi sheet also regenerated a sealed key.

## Fixed here

- **Sheets:** the seven `*_dissociation_annotator_A.csv` (pass A) and `_B.csv` (pass B) in `data/annotation/expert_kit/` as merged into main. Keys: the first kit's sealed keys kept on the project machine.
- **Items kept:** rows whose key entry (language, word, Wiktionary route) is an item of `data/baseline_v2/items.csv.gz` with a single distance, and whose subset recomputed from that distance (0.15 and 0.5) equals the key's (congruent control or dissociated). This drops the items that were dissociated only through the reader defect.
- **Measured, pooled over the seven languages and per language, for each pass:** rows kept; rows with label INH or LRN ("decided"); among decided rows, the number whose label equals Wiktionary's route, with a Wilson 95% interval, for controls and for dissociated items, and for dissociated items by Wiktionary route. Also raw agreement and Cohen's kappa between the two passes on the kept rows that both labelled (Hindi left out of that, since its B sheet holds a different sample).
- **Output:** `data/annotation/model_passes_s16.csv`.

## Reading fixed in advance

- Descriptive only. If a pass agrees with Wiktionary on most controls and on a minority of dissociated items, the paper says that a large language model labelling from the word behaves like the form-based classifiers. If it agrees on most dissociated items, the paper says so, with the caveat that such a model may have seen Wiktionary.
- Agreement between the passes is the consistency of one model under two instruction sets and is called that.
- No claim about which labels are right.
