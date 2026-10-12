# Supplementary analyses: plan v1.0 (FROZEN)

_2026-10-11. Frozen before any past revision was retrieved and before any of the analyses below was computed. SHA-256 in `docs/decision_log.md` (entry 80). Approved by the project lead ("yes" to starting the label-history study and the dissociation set). These analyses are **supplementary**: they add to, and do not replace, the audit plan v1.0 and the baseline plan v1.0, which stay unchanged._

**All of them describe Wiktionary's records or predict Wiktionary's labels. None validates a label.**

## S1. Label history: how stable is a route label over time?

- **Why.** If labels were settled facts copied from sources, they would rarely change. Changes between routes are a direct, annotator-free sign of editorial uncertainty.
- **Sample.** From the audit sample (`sample.csv`), the rows with rank 1–60 in each category of each of the 17 pairs (all rows if fewer).
- **Snapshots.** For each sampled page, the last revision at or before **2024-10-11T00:00:00Z** and at or before **2021-10-11T00:00:00Z**, one request per page and snapshot. Stored: revision ID, timestamp, and the wikitext of the language section.
- **Reading.** The same template reader as the audit, unchanged. For a page sampled from category C with route r(C):
  - `absent`: no such page or no language section at the snapshot;
  - `no route`: the section exists and states no route from the ancestor;
  - `same`: r(C) is among the routes stated from the ancestor;
  - `changed`: one or more routes are stated from the ancestor, and r(C) is not among them.
- **Measures, per language and category, and pooled by ancestor**, each with a Wilson 95% interval:
  - H1 = changed / (same + changed): of the labels that existed then, the share that named a different route;
  - H2 = no route / (no route + same + changed): of the entries that existed then, the share whose route was added later;
  - the direction of each change (e.g. INH → LRN), as counts.
- **Known limit, fixed in advance.** Old revisions may use template names or styles the reader does not know; these count as `no route`, so H2 is an upper bound and H1 uses only labels the reader can read.

## S2. Dissociation subset: where form and label pull apart

- **Why.** A model that learned resemblance will be wrong exactly where the label and the surface form disagree.
- **Definition, on the baseline items (`data/baseline_v1/items.csv.gz`).** With d = normalised edit distance to the ancestor form:
  - *congruent*: inherited with d ≥ 0.5, or learned with d ≤ 0.15;
  - *dissociated*: inherited with d ≤ 0.15, or learned with d ≥ 0.5;
  - everything else is *middle*.
- **Analysis.** The A1 cross-validation of the baseline plan is rerun with the same folds and seed, saving one out-of-fold prediction per item. Reported per language, for B1, B2 and B3: accuracy on congruent, middle and dissociated items, with counts and Wilson intervals; and the size of each subset. By construction B1 must fail on dissociated items; the question is whether B2 and B3 do.
- **Status of the subset.** These are items where Wiktionary's label is unexpected given the form. They are **candidates for validation, not validated cases**; some will be labelling errors.

## S3. Are cited labels less predictable from form?

- **Why.** Greek has both the lowest form-predictability and the highest inline-citation rate. Across languages that is one observation. Within a language it can be checked.
- **Analysis.** For each language with at least 30 baseline items (inherited or learned) whose etymology carries an inline citation and at least 30 without: B3 out-of-fold accuracy for cited and for uncited items, with Wilson intervals, and the difference.
- **Reading fixed in advance.** A difference is an association within Wiktionary's records. It does not show that citing a source makes a label right, and no causal claim will be made.

## Conduct

English Wiktionary Action API, serial requests at least 1.5 s apart, `maxlag=5`, no personal contact in the User-Agent. Raw snapshots under `data/raw/wiktionary/history_v1/`. Everything planned is reported, whatever it shows.
