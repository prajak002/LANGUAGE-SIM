# Can dictionaries tell inherited from learned?

A source-grounded feasibility study of tatsama / tadbhava route labels for Hindi and Bengali. Status on 2026-10-11: study finished, paper **draft** compiled, **no human check done yet**.

- Paper draft: `paper/main.pdf` (source `paper/main.tex`, ACL style, anonymous review mode, about 4 pages of content).
- Full results: `docs/feasibility_report.md`.
- Every decision: `docs/decision_log.md` (entries 1–70).

**Headline counts (48 lemmas, 58 word senses).** A route was assigned to 26. Semi-learned recovered: 0 of 12. Bengali learned recovered: 0 of 9. Agreement with Wiktionary on decided senses: 22 of 26, not independent.

The work is divided into two parts.

---

## Part 1: done by the assistant (Claude). Complete.

| # | Work | Where |
|---|---|---|
| 1 | Literature audit, novelty audit, research plan | `literature/`, `docs/novelty_audit.md`, `research.md` |
| 2 | Selection rules, frozen before any item was seen; 48 Wiktionary pages fetched | `docs/practice_set_selection.md`, `scripts/fetch_practice_set.py` |
| 3 | Extraction protocol v1.0 and pilot 1 (10 lemmas) | `docs/evidence_extraction_protocol.md`, `docs/pilot_1_report.md`, `data/annotation/pilot_1/` |
| 4 | Turner and J. Dāsa conventions read from the front matter | protocol v1.1 §8′ |
| 5 | Protocol v1.1, frozen; round 2 (38 lemmas, 46 senses, 111 source checks) | `docs/evidence_extraction_protocol_v1.1.md`, `data/annotation/round_2/` |
| 6 | Labels frozen with SHA-256 before Wiktionary was opened; comparison | `scripts/wiktionary_candidate.py`, `scripts/compare_round.py` |
| 7 | Counts-only feasibility report | `docs/feasibility_report.md` |
| 8 | Paper draft in ACL format, built only from the frozen counts | `paper/` |
| 9 | Spot-check forms with a link and a paraphrase per row | `data/annotation/*/spot_check.md` |

**What Part 1 is not.** The labels are model-extracted. They are not gold labels, there is no inter-annotator agreement, and the assistant cannot check its own extraction independently.

---

## Part 2: the project lead's. Needed before submission.

In order. Items 1–4 are required; without them the paper has red `[LEAD: ...]` gaps.

1. **Spot check (the only human verification in the paper).**
   - `data/annotation/pilot_1/spot_check.md`: 23 rows. Open each link, compare with the paraphrase, fill the `Result:` line.
   - `data/annotation/round_2/spot_check.md`: 111 rows in a fixed order. **Write down a sample size first**, then check that many from the top.
   - If a label is wrong, do not edit the frozen CSVs. Note it; the counts in the report and the paper must then be recomputed.
2. **Fill the five `\lead{...}` gaps in `paper/main.tex`**: abstract, §3.5, Limitations, Ethical Considerations, Appendix A. If no spot check was done, the paper must say so.
3. **Read the whole draft and own it.** Check every number against `docs/feasibility_report.md`.
4. **Venue requirements**: page limit, anonymity, the policy on AI assistance (the draft discloses that a language-model assistant did the lookups, the labelling and the drafting), and any required checklist.
5. **Two references were not read in this project**: Masica 1991 and Chatterji 1926 (`paper/refs.bib`). Verify the claims they support, or remove them. The bibliographic details of the four dictionaries are from memory of the library's catalogue; check them.
6. **Decide what data is released.** Entry references and paraphrases can be; dictionary text cannot. The licensing review is still open.

Rebuild the PDF: `cd paper && tectonic main.tex` (on Overleaf: pdfLaTeX, upload the whole `paper/` folder).

### Honest assessment for the submission decision

- The contribution is a small negative result: 58 senses, hand-stratified, no second annotator.
- It fits a short paper or a workshop better than a main-conference long paper.
- Submitting without any spot check means the paper reports unverified model output. That is the lead's decision, and the paper must state it either way.

### Open after submission

- A source that states routes for Bengali and semi-learned words (Chatterji 1926 is unread).
- Kanojia et al. 2019 and Bouchard-Côté et al. 2013 full texts.
- The front matter of the *Hindī śabdasāgara*.

---

## Rules that hold for this repository

- No dictionary text is stored for the three consult-only dictionaries; only entry references and paraphrases.
- Frozen files are read-only and hashed in the decision log. Corrections go in new files, not edits.
- `research.md` §13 (Results) stays empty: this is a feasibility finding, not a classifier result.
