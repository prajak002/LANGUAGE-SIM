# Supplementary analysis S7: are the labels that go against resemblance backed by anything? Plan v1.0 (FROZEN)

_2026-10-12. Frozen before either cross-tabulation below was computed and before `scripts/history_analysis.py` was run on any data. SHA-256 in `docs/decision_log.md` (entry 92). Requested by the project lead ("work so that the central result is strong"). No new data is fetched for S7; no model is called._

## Why

S2 found that form-based models reproduce Wiktionary's label where it follows resemblance and fail where it does not. The dissociated items are either words whose history and form really disagree, or labelling errors. S7 asks two questions that bear on which, using data the project already holds. **Neither validates a label.**

Seen before freezing: the column names of `item_flags.csv.gz`, `oof_predictions.csv.gz`, `items.csv.gz` and `sample.csv`; the S4 totals already reported (a listed form matches for 49% of matched inherited items and 9.1% of matched learned ones); the code of `history_analysis.py`. Not seen: any Turner flag or any history state broken down by subset.

## S7a. Turner's dictionary on near-Sanskrit words (seven Indo-Aryan languages)

- **Items.** Baseline items of the Sanskrit family with route inherited or learned, joined to the S4 flags (`data/audit/turner_scale_v1/item_flags.csv.gz`) on language, title and route, and to the S2 subsets.
- **Main comparison, fixed here: words close to the Sanskrit form (distance at most 0.15).** Two groups have such forms: *dissociated inherited* (Wiktionary says inherited) and *congruent learned* (Wiktionary says learned). For each, pooled and per language: T1 / items and T3 / T1, with Wilson 95% intervals, and the difference in T3 / T1 between the groups with a 95% interval (Newcombe's method from the two Wilson intervals).
- **Second comparison: words far from the Sanskrit form (distance at least 0.5).** *Congruent inherited* against *dissociated learned*, same measures.
- **Reading fixed in advance.**
  - T3 is the S4 matcher: it accepted 3 of 24 forms a hand record had rejected and missed 4 of 14 it had listed. A T3 rate is not a rate of true listings; the comparison between two groups with equally close forms is what is read.
  - If, among near-Sanskrit words, Turner lists a matching form clearly more often for those Wiktionary calls inherited (interval of the difference excludes zero), then the labels that go against resemblance are **associated with an entry in a scholarly source**, and are not explained by resemblance. That is not independent confirmation: Wiktionary's editors cite Turner, so the label may come from the same entry.
  - If the two rates do not differ, nothing in Turner separates the two groups, and the dissociated inherited items remain unexplained candidates.
  - Pooled cells with fewer than 30 T1 items are reported as counts without interpretation.

## S7b. Label history by subset

- **Items.** Baseline items (inherited or learned) whose page is in the S1 history sample (rank 1 to 60 of its category), joined on language, title and route. The S1 state of the page at each snapshot (`absent`, `no route`, `same`, `changed`) is taken unchanged from the S1 definitions.
- **Measures, per ancestor family and pooled, for congruent, middle and dissociated items at each snapshot:** H1 = changed / (same + changed) and H2 = no route / (no route + same + changed), with Wilson 95% intervals; and the difference in H1 between dissociated and congruent items with a 95% interval (Newcombe).
- **Reading fixed in advance.**
  - If H1 is clearly higher for dissociated items, the labels that go against resemblance are the ones editors have changed more often: editorial uncertainty is concentrated there.
  - If it is not, no claim is made. A stable label is not a correct label.
  - Cells with fewer than 30 items in the H1 denominator are reported as counts without interpretation. The S1 sample was not drawn to be balanced by subset, so small dissociated cells are expected in the Sanskrit and Latin families.
- **Order of work.** `history_analysis.py` (S1, as planned) is run first on the complete fetch and reported whatever S7b shows.

## Conduct

Both results are reported whichever way they fall, with their denominators. No threshold above is changed after the results are seen. The paper's wording is changed only to state what was found.
