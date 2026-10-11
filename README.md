# Can dictionaries tell inherited from learned?

A feasibility study of tatsama / tadbhava labels for Hindi and Bengali words, with a paper draft.

**Status, 2026-10-11:** the study is finished and a paper draft compiles. **No human has checked the extraction yet**, and the draft has five gaps that only the authors can fill. Submission is planned for 2026-10-12.

| To read | File |
|---|---|
| The paper draft | `paper/main.pdf` (source: `paper/main.tex`) |
| The full results | `docs/feasibility_report.md` |
| Every decision, in order | `docs/decision_log.md` (entries 1–73) |

---

## 1. What this project is about

**Background.** A Hindi or Bengali word that comes from Sanskrit reached the modern language by one of three routes:

| Route | Traditional name | Meaning |
|---|---|---|
| Inherited | tadbhava | Passed down through Prakrit, changing its sounds on the way |
| Learned | tatsama | Borrowed later, directly from Sanskrit, form unchanged |
| Semi-learned | ardhatatsama | Borrowed later from Sanskrit, form partly adapted |

Wiktionary records one of these routes for thousands of Hindi and Bengali words. Such labels are an obvious source of training data for a classifier.

**The question.** Can those labels be checked against published dictionaries?

**What was done.**
1. 48 Wiktionary words were chosen by rules fixed in advance (24 Hindi, 24 Bengali). Some spellings cover two unrelated words, so the 48 words give 58 word senses.
2. Each sense was looked up in four dictionaries: Platts (1884), Turner's comparative dictionary, J. Dāsa's Bengali dictionary, and the *Hindī śabdasāgara*.
3. A route was assigned by written rules. The rules and the labels were frozen (file hashes recorded) before the Wiktionary etymology was opened.
4. Only then were the labels compared with Wiktionary.

**The lookups and labels were made by an AI assistant (Claude), not by a person.**

## 2. What the paper says

- **Main answer: mostly no, and least where it matters.** A route could be assigned to 26 of 58 senses.
- **Semi-learned words cannot be recovered:** 0 of 12. No dictionary has a marker for them.
- **Bengali learned words cannot be recovered:** 0 of 9. The Bengali dictionary gives a Sanskrit form for inherited and learned words alike.
- **Agreement is not fully independent.** Where the dictionaries decide, they agree with Wiktionary on 22 of 26 senses, but 7 of those 22 Wiktionary entries cite the very dictionary the label rests on.
- **The gap is in the dictionaries, not in the scholarship.** A check made afterwards, outside the frozen study, found that Chatterji's 1926 historical grammar calls 2 of the 6 Bengali semi-learned words semi-tatsama explicitly, and lists 2 more under that label.
- **The inherited rule is weak.** "Turner lists the form with no loan mark" also catches some forms identical to Sanskrit.
- **Take-away for readers:** anyone who trains or evaluates a model on Wiktionary's tatsama / tadbhava labels is using labels that cannot be verified from these sources.

**What the paper does not claim:** no classifier, no gold labels, no agreement between human annotators, and no rates for Hindi or Bengali as a whole. It is a small negative result about a labelling method.

---

## 3. Who does what

Three parties: the assistant (finished), and two authors, called **Person A** and **Person B** here. Swap A and B to fit who reads Hindi and Bengali best.

### 3.1 Done by the assistant

| Work | Where |
|---|---|
| Literature audit, novelty audit, research plan | `literature/`, `docs/novelty_audit.md`, `research.md` |
| Selection rules (frozen) and the 48 Wiktionary pages | `docs/practice_set_selection.md`, `scripts/fetch_practice_set.py` |
| Pilot on 10 words, protocol v1.0 | `docs/evidence_extraction_protocol.md`, `docs/pilot_1_report.md`, `data/annotation/pilot_1/` |
| Dictionary conventions read from the front matter | `docs/evidence_extraction_protocol_v1.1.md` §8′ |
| Round 2 on 38 words, protocol v1.1 (frozen) | `data/annotation/round_2/` |
| Comparison with Wiktionary after the freeze | `scripts/wiktionary_candidate.py`, `scripts/compare_round.py` |
| Feasibility report, counts only | `docs/feasibility_report.md` |
| Paper draft in ACL format | `paper/` |
| Spot-check forms | `data/annotation/pilot_1/spot_check.md`, `data/annotation/round_2/spot_check.md` |
| Check of which Wiktionary entries cite the dictionaries used | `scripts/sense_citation.py`, `data/annotation/sense_citation.csv` |
| Exploratory check of Chatterji 1926 (not part of the frozen study) | `data/annotation/exploratory_chatterji.csv` and its README |
| Dictionary references checked against the library's citation pages | `paper/refs.bib` |

### 3.2 Before submission: both authors together

This is the only human verification the paper will have, so it comes first.

1. **Agree a sample size *n* for round 2** and write it down before either of you opens a link. 30 is a workable minimum.
2. **Each of you checks the same rows, separately:**
   - all 23 rows of `data/annotation/pilot_1/spot_check.md`;
   - the first *n* rows of `data/annotation/round_2/spot_check.md`, from the top, skipping none.
3. **For each row:** open the link, find the entry, and compare it with the recorded paraphrase and route. Record one of: correct, wrong, cannot tell.
4. **Keep your results in your own copy of the file.** Do not look at the other person's copy until both are finished.
5. **Compare.** Count the rows where both say correct, both say wrong, and where you differ. Report these counts in the paper.

### 3.3 Before submission: Person A (evidence and data)

1. **Corrections.** If a recorded label is wrong, do not edit the frozen CSV files. Write the correction in a new file, and recompute the counts in `docs/feasibility_report.md` and `paper/main.tex`.
2. **Numbers.** Check every number in the paper against the report and the CSV files.
3. **Data release.** Decide what goes out with the paper. Entry references and paraphrases can be released; dictionary text cannot. Fill the gap in Appendix A.

### 3.4 Before submission: Person B (paper and submission)

1. **Fill the gaps.** Search `paper/main.tex` for `\lead{`. There are six: abstract, §3.5, Discussion, Limitations, Ethical Considerations, Appendix A. If no spot check was done, the paper must say so.
2. **Check the Chatterji passages on the page images** (Discussion gap). Internet Archive item `OriginDevelopmentOfBengali`, vol. 1, pp. 308, 376, 380, 403, 470, 534. The assistant read an OCR copy only, and the page numbers may be off by one. If a passage does not say what `data/annotation/exploratory_chatterji.csv` records, correct the paper.
3. **References.** Kanojia et al. 2019 was not obtained; the draft cites only the 2021 thesis. The dictionary references are now verified.
4. **Venue rules.** Page limit, anonymity, any required checklist, and the policy on AI assistance. The draft states that an AI assistant did the lookups, the labelling and the drafting.
5. **Final read and build.** Read the whole draft once. Content must fit the page limit after the gaps are filled; it is at the 4-page mark now. Rebuild with `cd paper && tectonic main.tex`. On Overleaf, upload the whole `paper/` folder and use pdfLaTeX.

---

## 4. What a main-conference paper would need

**Where the draft stands.** With the spot check done and the gaps filled, it is an honest short or workshop paper. As a main-conference long paper it would probably be rejected as too small and unvalidated. An oral slot is decided by the committee, and no list of fixes guarantees it.

**None of the work below can be done by 2026-10-12.** It is weeks of work for two people. Every experiment, model call or new data fetch in it needs a decision first; none is authorised yet.

| Likely objection | What would answer it | Who |
|---|---|---|
| 58 hand-picked senses: no rate can be reported | A random sample of several hundred senses per language, with the rules frozen first and confidence intervals reported | A |
| No human annotation, no agreement figure | Two people label the same sample independently from the sources. A historical linguist adjudicates a subset | A + B |
| An AI assistant checks its own work | Human-versus-assistant extraction accuracy on the double-labelled sample | A |
| Only a negative result; nothing a reader can use | A released benchmark: senses separated, source references, evidence strength, and "undecidable" as a label | A |
| No experiment | Train a word-versus-etymon classifier on Wiktionary labels (as Cristea et al. 2021 do for Romance), and evaluate it on the verified subset versus the raw labels | B |
| The key sources are missing | Chatterji 1926 for Bengali: accessible, and it labels words ts., sts. and tbh. (seen for 2–4 of 6 test words). McGregor's Hindi dictionary: Wiktionary cites it in 20 of 28 Hindi entries; not consulted here. Both need a frozen rule and a blind run on new words | B |
| "Turner lists it" is a weak rule | On the larger sample, count how often Turner lists a form identical to Sanskrit with no loan mark | A |
| Circularity rests on 22 senses | Done for this sample (7 of 22 cite the source used). Repeat on the larger sample, and report agreement separately for citing and non-citing entries | A |
| Two languages only | One or two more (Marathi, Gujarati or Odia), if sources exist | B |
| Related work is thin | Read the borrowing-detection papers known here only by title and abstract (`literature/review.md`, marked [MD]) | B |

**The decision for the authors:** submit the short version on 2026-10-12, or hold the paper for a later deadline and do this table first.

---

## 5. Rules for this repository

- **Copyright.** Platts is in the public domain. For the other three dictionaries, only entry references and paraphrases are stored, never dictionary text.
- **Frozen files.** They are read-only, and their hashes are in the decision log. Corrections go in new files.
- **Results.** `research.md` §13 stays empty: this is a feasibility finding, not a classifier result.
- **Claims.** The labels are extracted by an AI assistant. Do not describe them as gold labels or as independently verified.
- **Still open:** the Kanojia et al. 2019 and Bouchard-Côté et al. 2013 full texts, the front matter of the *Hindī śabdasāgara*, and the licensing review.
