# Inherited or learned? Checking the labels that etymology models are trained on

**Status, 2026-10-11.** The analyses are done except two that are still running (section 6). A paper draft compiles. **The paper is not ready to submit:** it has six red gaps for the authors, and no two-person human validation exists yet.

| If you want to… | Open |
|---|---|
| Read the paper | `paper/main.pdf` |
| Understand the project in ten minutes | This file |
| See what each author must do | Section 7 |
| Check a number | Section 8 lists the report and result file for each part |
| See every decision in order | `docs/decision_log.md` (entries 1–85) |

---

## 1. The question, in plain words

Many languages have two kinds of words from the same ancestor language.

| Kind | What happened | What it tends to look like |
|---|---|---|
| **Inherited** | Passed down from parent to child over many centuries, changing its sounds on the way | Worn down; often far from the old form |
| **Learned** | Borrowed later, straight out of the old language's books | Still close to the old form |
| **Semi-learned** | Borrowed later, then partly adapted | In between |

In Indian grammar the first two are called *tadbhava* and *tatsama*. Hindi and Bengali have them from Sanskrit; Spanish and French have them from Latin.

**Wiktionary labels tens of thousands of words this way**, and labels of this kind have been used to train models. This project asks three things:

1. **What are these labels like?** How big are the classes, are they consistent, do they cite a source?
2. **What is a model really learning from them?** History, or just "this word looks like the old form"?
3. **Can the labels be checked against something independent?**

---

## 2. What we found, in plain words

### Finding 1. The labels are tidy but rarely say where they come from
*(audit of 13,128 Wiktionary pages in 17 languages)*

- The label on a page almost always matches the page's own etymology (only 5 of 6,009 "learned" pages do not).
- **The semi-learned class is tiny in every language:** at most 129 pages.
- **A "learned borrowing" claim carries its own citation in at most 4% of cases** in 16 of 17 languages. Greek is the exception at 57%. Many entries list references elsewhere on the page.

### Finding 2. A model can predict the label from resemblance alone
*(simple models on 12,777 word senses in 16 languages)*

- For seven languages descended from Sanskrit, **one number**, how different the word is from its Sanskrit form, predicts Wiktionary's label with a macro-F1 score of 0.80 to 0.93. With letter patterns added: 0.86 to 0.96.
- For seven Romance languages: 0.75 to 0.91.
- For Greek and Armenian the label is barely predictable from form (0.62 and 0.59).

### Finding 3. Where the label goes against resemblance, the model fails
This is the sharpest result.

- Take the words where label and looks **agree** (inherited and worn down, or learned and close to the old form). The model is right on **about 100%** of them in the Sanskrit family and 98% in Romance.
- Take the few words where they **disagree** (inherited but almost identical to the old form, or learned but far from it). The model is right on **14%** and **19%**.
- So the model has learned "looks like the ancestor form", not history.
- **Two cautions.** This is partly built in, because the split uses a feature the model sees; a model that sees only the word still drops from 87% to 57%. And the disagreeing words are unchecked: each is either a real case or a mistake in Wiktionary.

### Finding 4. The one expert check we could make came out in Wiktionary's favour
*(Romanian, against a specialist's published loanword list, open licence)*

- Of 684 words that Wiktionary calls inherited and the expert also covers, **the expert agrees on 651 (95%)**.
- Learned words could not be measured: the expert's list covers basic vocabulary and has only 28 of them.
- Six Romanian words are of the "label against resemblance" kind. **The expert sides with Wiktionary on all six; the model gets one right.** Six words are an illustration, not a measurement.

### Finding 5. For Hindi and Bengali, dictionaries cannot settle the hard cases
*(48 words looked up in four dictionaries)*

- A route could be read off the dictionaries for 26 of 58 word senses.
- **None of the 12 semi-learned cases and none of the 9 Bengali learned cases could be confirmed**: the dictionaries whose conventions were read have no marker for them.
- A historical grammar of Bengali (Chatterji 1926) does mark semi-learned words, and names 2 of the 6 Bengali cases explicitly. This was a look after the fact and needs a human check.

### What the project does **not** show
- It does not show which Wiktionary labels are right, except the small Romanian check.
- It has **no validation by two independent annotators**.
- The Hindi and Bengali dictionary lookups were made by an AI assistant and have not been checked by a person.

---

## 3. How the work was kept honest

- **Plans were frozen before data were seen.** Each analysis has a plan file with a recorded fingerprint (SHA-256) in the decision log. The plan files are read-only.
- **Changes after the fact are labelled.** Anything added later is called supplementary and says why.
- **Mistakes are recorded, not hidden.** A first audit run was wrong because of a reader defect and was redone. A claim that 8 of 17 pages cite Turner was wrong and was corrected to 7 of 22. Six overreaching sentences in the draft were corrected in a claim-by-claim audit.
- **Sites' access rules were respected.** Two dictionaries (French TLFi, Romanian DEX) forbid automated reading and were not used.
- **Copyrighted dictionary text is never stored**, only entry references and paraphrases.

---

## 4. The parts of the project

| Part | What it does | Size | Report |
|---|---|---|---|
| A. Cross-lingual audit | Describes Wiktionary's route labels | 13,128 pages, 17 language pairs | `docs/crosslingual_audit_report.md` |
| B. Form-based baseline | Predicts Wiktionary's label from word form | 12,777 senses, 16 languages | `docs/baseline_report.md` |
| C. Supplementary analyses | Dissociation split, citation check, Turner at scale, Romanian expert check, language model, label history | see section 6 | `docs/supplementary_report.md` |
| D. Hindi and Bengali source study | Looks 48 words up in dictionaries | 58 word senses | `docs/feasibility_report.md` |
| E. Annotation kit | Blind sheets for human annotators | unfilled | `data/annotation/expert_kit/README.md` |
| F. Release package | The benchmark as one file, with data sheet and licensing review | 12,777 rows; not published | `data/release/` |

Languages: Sanskrit → Hindi, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese, Urdu; Latin → Spanish, Portuguese, French, Italian, Romanian, Catalan, Galician; Ancient Greek → Greek; Old Armenian → Armenian. Urdu is in the audit only.

---

## 5. What is validated, and by whom

| Evidence | Checked against | Status |
|---|---|---|
| Wiktionary pages retrieved | Revision IDs stored for all 13,128 | Done |
| Audit and baseline code | Hand-worked test cases | Passing |
| Baseline leakage | Folds regrouped by ancestor form | Done; scores fell by at most 0.013 |
| Romanian inherited labels | One expert's published list | 651 of 684 agree |
| "Turner lists the form" rule by program | 38 hand records | 31 agree; gives candidates only |
| Hindi/Bengali dictionary lookups (134) | A person | **Not done** |
| Chatterji passages | Page images | **Not done** |
| Dissociated items | Two independent annotators | **Not done; sheets ready** |
| Learned and semi-learned labels in general | Anything independent | **Not done** |

---

## 6. Still running or blocked

| Item | State when this was written | What it will add |
|---|---|---|
| Language-model evaluation (Gemma 3, run locally, no cost) | **Finished: a null result.** The small model answered "inherited" about four times in five whatever the word and was near chance | Nothing. The question whether a language model leans on resemblance stays open; a larger model was not tested |
| Label history (past revisions of 2,575 pages) | Running slowly: about 400 of 5,150 requests. The first attempt was refused by Wikimedia | How often a label has changed over 2 and 5 years |
| French and Romanian dictionary checks by program | **Blocked** by the sites' rules | Manual lookup sheets are in the kit instead |

To finish the label history once its job ends:
```
python3 scripts/history_analysis.py data/raw/wiktionary/crosslingual_v1 data/raw/wiktionary/history_v1 data/audit/history_v1
```
**No label-history number may go in the paper until this has been run.**

---

## 7. Who does what

"Person A" and "Person B" are the two authors; swap to fit who reads which language.

### Both, separately and without comparing notes

1. **Annotate the dissociated items (highest value).** `data/annotation/expert_kit/<language>_dissociation_annotator_A.csv` and `_B.csv`: Hindi 78 rows, Bengali 120, Marathi 104, Gujarati 44, Punjabi 124, Odia 50, Assamese 36. Label each word from dictionaries, without opening Wiktionary. Then run the agreement script named in the kit's README. If most turn out to be real cases, the paper has a validated benchmark; if most are errors, it has an error rate for Wiktionary. Either result is worth reporting.
2. **Spot-check the assistant's dictionary lookups.** `data/annotation/pilot_1/spot_check.md` (23 rows) and the first *n* rows of `data/annotation/round_2/spot_check.md`. Agree *n* before starting.

### Person A: evidence and data

3. Check the Chatterji passages on the page images (Internet Archive item `OriginDevelopmentOfBengali`, vol. 1, pp. 308, 376, 380, 403, 470, 534).
4. Check the 130 "learned" and 21 "semi-learned" candidates where Turner seems to list the word (`data/audit/turner_scale_v1/`; **not for release**).
5. Sign off or amend `data/release/LICENSING_REVIEW.md`.

### Person B: paper and submission

6. Fill the six red `[LEAD: …]` gaps in `paper/main.tex` (search for `\lead{`). If a check was not done, the paper must say so.
7. Check the venue's page limit, anonymity rules, checklist and policy on AI assistance. The draft discloses that an AI assistant did the lookups and the labelling and helped draft the paper; say the same of the analyses.
8. Attach `data/audit/crosslingual_v1/tables.md` as supplementary material.
9. Obtain and read Kanojia et al. 2019, which the draft cites only through the author's thesis.

---

## 8. Where every number comes from

| Paper section | Result files | Script | Frozen plan |
|---|---|---|---|
| Audit | `data/audit/crosslingual_v1/measures.csv`, `tables.md` | `scripts/audit_crosslingual.py` | `docs/crosslingual_audit_plan.md` |
| Baseline | `data/baseline_v1/a1_cv.csv`, `a2_semi.csv`, `a3_transfer.csv`, `leakage_check.csv` | `scripts/baseline.py`, `scripts/baseline_leakage_check.py` | `docs/baseline_plan.md` |
| Dissociation, citation | `data/baseline_v1/s2_dissociation.csv`, `s3_citation.csv`, `oof_predictions.csv.gz` | `scripts/baseline_supplementary.py` | `docs/supplementary_plan.md` |
| Turner at scale | `data/audit/turner_scale_v1/` | `scripts/turner_scale.py` | `docs/supplementary_plan_s4.md` |
| Language model | `data/llm_s5/` | `scripts/llm_dissociation.py` | `docs/supplementary_plan_s5.md` |
| Romanian expert check | `data/audit/wold_romanian_v1/`, `data/external/wold_romanian/` | `scripts/wold_romanian.py` | `docs/supplementary_plan_s6.md` |
| Label history | `data/raw/wiktionary/history_v1/` | `scripts/fetch_history.py`, `scripts/history_analysis.py` | `docs/supplementary_plan.md` |
| Hindi/Bengali source study | `data/annotation/pilot_1/`, `data/annotation/round_2/` | `scripts/compare_round.py`, `scripts/sense_citation.py` | `docs/evidence_extraction_protocol_v1.1.md` |

**Rebuild and test**
```
python3 tests/test_audit_fixture.py
uv venv .venv && uv pip install --python .venv/bin/python scikit-learn
.venv/bin/python tests/test_baseline_helpers.py
python3 scripts/annotation_agreement.py --self-test
cd paper && tectonic main.tex
```

---

## 9. Honest assessment

- **What the evidence supports:** a careful audit of how Wiktionary records these labels in 17 languages; a clear demonstration that simple models reproduce the labels by resemblance and fail where resemblance misleads; one small expert check in Romanian; and a negative result on checking Hindi and Bengali labels in dictionaries.
- **What holds the paper back:** the "label against resemblance" items, which carry the main claim, are validated for six Romanian words only. Two qualified annotators working through the sheets in section 7 would change that.
- **Realistic placement today:** a workshop or Findings paper. A main-conference case needs the human annotation.

---

## 10. Rules for this repository

- Nothing is committed, pushed or published without the project lead saying so.
- Frozen files are read-only; corrections go in new files and in the decision log.
- No dictionary text is stored for copyrighted dictionaries. `data/audit/turner_scale_v1/item_flags.csv.gz` is not for release.
- External data kept with attribution: `data/external/wold_romanian/` (CC BY 4.0).
- Model output is never used as a label or as validation.
- `research.md` §13 (Results) stays empty; it belongs to a later classifier study that has not been run.

## 11. Words used in this file

| Term | Meaning |
|---|---|
| Route | How a word entered the language: inherited, learned, or semi-learned |
| Ancestor form (etymon) | The word in the old language (Sanskrit, Latin, …) that the modern word comes from |
| Edit distance | How many letter changes turn one form into the other, scaled to 0–1 |
| Congruent / dissociated | The label agrees with / goes against how close the word is to the ancestor form |
| Macro-F1 | A score from 0 to 1 that treats both classes equally; 0.5 is roughly chance here |
| Frozen plan | A written plan whose fingerprint was recorded before the data were looked at |
| Wilson interval | A 95% range of uncertainty around a percentage |
