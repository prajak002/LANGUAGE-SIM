# What Form Cannot Tell

**Do models trained on Wiktionary's "inherited" and "learned" labels learn word history, or only resemblance?**
An audit of the labels in 17 languages, a form-based baseline, and a set of checks on the words where the label and the resemblance disagree.

| | |
|---|---|
| Paper draft | `paper/main.pdf` (14 pages; main text 8) |
| Every decision, in order | `docs/decision_log.md` |
| Every analysis report | `docs/supplementary_report.md`, `docs/crosslingual_audit_report.md`, `docs/baseline_report.md`, `docs/feasibility_report.md` |
| Status, 2026-10-13 | All planned analyses run except S12 (a pretrained model; plan frozen, not run). No human expert has labelled the project's own items |

---

<p align="center"><img src="docs/figures/label_by_resemblance.svg" alt="Accuracy of the form-based model by label and by resemblance to the ancestor form" width="760"></p>

**In sixty seconds**

1. Wiktionary says, for tens of thousands of words, whether a word was *inherited* from the ancestor language or *borrowed back* from it later.
2. A simple model predicts that label very well from the spelling alone.
3. It does so by measuring **resemblance**: close to the old form means "learned", far means "inherited".
4. On the words where that shortcut is wrong (the red cells above), the model is wrong almost every time.
5. Giving the model more history (the intermediate form) or a bigger architecture (a Transformer) does not fix those words.
6. So a high score on these labels shows agreement with Wiktionary. It does not show that a model has learned word history.

---

## 1. The question

Many languages have two kinds of words from the same ancestor language.

| Kind | What happened | What it tends to look like |
|---|---|---|
| **Inherited** (*tadbhava*) | Passed down over many centuries, changing its sounds on the way | Worn down; often far from the old form |
| **Learned** (*tatsama*) | Borrowed later, straight from the old language's books | Still close to the old form |
| **Semi-learned** | Borrowed later, then partly adapted | In between |

Wiktionary labels tens of thousands of words this way, and such labels have been used to train classifiers. A high score on them can mean two different things:

<p align="center"><img src="docs/figures/what_the_model_learns.svg" alt="A modern word and its ancestor form go into a model. Hoped for: the model learns the word's history. What we find: it learns how much the word looks like the ancestor form." width="900"></p>

### Four real Hindi words

These are items from the data, with the ancestor form as our reader normalised it. Distance runs from 0 (same spelling) to 1.

| Word | Sanskrit form | Distance | Wiktionary says | Model says | |
|---|---|---|---|---|---|
| पात (its inherited sense) | पत्त्र | 0.67 | inherited | inherited | right: far, so "inherited" |
| भवन | भवन | 0.00 | learned | learned | right: identical, so "learned" |
| जल | जल | 0.00 | **inherited** | learned | **wrong**: identical, but Wiktionary says it was inherited |
| छंद | छन्दस् | 0.67 | **learned** | inherited | **wrong**: far, but Wiktionary says it was borrowed |

The last two rows are the *dissociated* items. Nothing in the spelling of जल tells you whether it came down through Prakrit unchanged or was taken from Sanskrit books. That is a fact about records, not about letters.

<details>
<summary><b>Why does the model fail on exactly these words?</b></summary>

```mermaid
flowchart TD
    A["Training data:<br/>most inherited words are worn down,<br/>most learned words are intact"] --> B["Cheapest rule that fits:<br/>near the ancestor form = learned"]
    B --> C["Works on about 99% of ordinary words"]
    B --> D["Fails on words that were inherited<br/>without changing, and on learned words<br/>that are far from the form on record"]
    D --> E["Those words need evidence from outside the word:<br/>attestation dates, a dictionary's judgement"]
```

</details>

<details>
<summary><b>What do "congruent" and "dissociated" mean?</b></summary>

- **Congruent:** the label agrees with resemblance. Inherited and far from the ancestor form (distance at least 0.5), or learned and near it (at most 0.15).
- **Dissociated:** the reverse. Inherited but near, or learned but far.
- Words in between are left out of this split.
- The split is a **diagnostic**: it is built from the label and a distance, so it shows where a model leans on resemblance. It is not an independent test set, and the labels in it have not been checked by a person.

</details>

## 2. The study in one picture

<p align="center"><img src="docs/figures/pipeline.svg" alt="The pipeline: Wiktionary categories in 17 language pairs; a sample of 13,128 pages; an audit; 12,778 word senses and a form-based baseline; congruent items where the model is right on about 100% and dissociated items where it is right on 10% and 19%; four checks of the dissociated items; label history; and 48 Hindi and Bengali words looked up in four dictionaries." width="900"></p>

## 3. Results

| # | Finding | Key numbers | Report |
|---|---|---|---|
| 1 | The labels are tidy but rarely cite a source | A learned-borrowing claim has its own citation in at most 4% of senses in 16 of 17 languages; the semi-learned class never exceeds 129 pages | `docs/crosslingual_audit_report.md` |
| 2 | Form predicts the label | Macro-F1 0.86 to 0.96 (Sanskrit family), 0.75 to 0.91 (Romance), 0.62 and 0.59 (Greek, Armenian) | `docs/baseline_report.md` |
| 3 | The models fail where label and resemblance disagree | Right on 27 of 260 (10%) and 52 of 272 (19%) dissociated items | `docs/supplementary_report.md` S2 |
| 4 | Those labels follow a dictionary | Turner lists a matching form for 57 of 125 near-Sanskrit words called inherited (46%) and 100 of 1,001 called learned (10%) | S7a |
| 5 | The intermediate stage explains the failure and does not repair it | A rule with no training agrees with the label on 1,484 of 1,864 items (80%) where the intermediate form changed; for 92 of 110 hard inherited items (84%) it did not change | S8 |
| 6 | Expert sources agree with Wiktionary's inherited labels | Not loans: 651 of 684 Romanian words, 277 of 291 in thirteen languages; on 48 hard items the specialists side with Wiktionary on 45, the model on 22 | S6, S9 |
| 7 | Most Romance learned labels are recent | In October 2024, 258 of 370 sampled ones were plain "borrowed from Latin"; inherited labels changed in 4 of 873 | S1 |
| 8 | Dictionaries cannot settle the hard Hindi and Bengali cases | A route could be assigned to 26 of 58 senses, and to none of the 12 semi-learned ones | `docs/feasibility_report.md` |

<p align="center"><img src="docs/figures/baseline_by_language.svg" alt="Macro-F1 of the form-based model in sixteen languages" width="760"></p>

**The three-input experiment** (3,289 Indo-Aryan items, pooled folds grouped by ancestor form):

| Model input | Logistic: macro-F1 | Logistic: hard items right (of 194) | Transformer: macro-F1 | Transformer: hard items right (of 194) |
|---|---|---|---|---|
| Word only | 0.78 | 113 | 0.78 | 123 |
| Word + ancestor form | 0.90 | 11 | 0.86 | 91 |
| Word + ancestor + intermediate form | 0.90 | 12 | 0.86 | 95 |

The ancestor form buys the overall score at the cost of the hard items, and the intermediate form restores nothing, in either model. (The paper's main text gives the per-language-fold version of the logistic run: 120, 15 and 23 of 194.)

<p align="center"><img src="docs/figures/three_inputs.svg" alt="Hard items right by model input, logistic model against Transformer" width="760"></p>

<details>
<summary><b>How to read this chart</b></summary>

- **Word only:** both models are a little above chance. They cannot measure resemblance, so they cannot be misled by it.
- **Word + ancestor form:** the logistic model now measures resemblance directly and drops to 6%. Its overall score rises from 0.78 to 0.90 at the same time. The Transformer follows resemblance less closely, scores lower overall, and sits at chance.
- **+ intermediate form:** no real change in either model. For 84% of the hard inherited words the intermediate form is itself almost the Sanskrit form, so it carries nothing to learn from.

</details>

<p align="center"><img src="docs/figures/label_history.svg" alt="Share of labels that named a different route in October 2024" width="760"></p>

<details>
<summary><b>How to read this chart</b></summary>

- Inherited labels hardly move.
- Most Romance "learned" labels were plain "borrowed from Latin" two years ago: 258 of the 259 changes are that refinement, not a reversal.
- We did not look at who made the edits or why. A stable label is not a correct label.

</details>

**Null results, reported as such:** two local language models (Gemma 3, 4 and 12 billion parameters) answered "inherited" whatever the word; hard items were not edited more often than easy ones.

## 4. What is shown and what is not

```mermaid
flowchart LR
    C1["Claim 1<br/>A model predicts<br/>Wiktionary's labels"] --> S1["SHOWN<br/>including where it fails"]
    C2["Claim 2<br/>The labels agree with<br/>evidence outside Wiktionary"] --> S2["PARTLY<br/>inherited labels, where sources cover them;<br/>learned labels are not validated"]
    C3["Claim 3<br/>A word's historical route<br/>can be reconstructed"] --> S3["NOT ATTEMPTED<br/>no reference routes exist"]
```

- **No human expert has labelled the project's own items.** Blank blind sheets for the hard items are ready in `data/annotation/expert_kit_v2/`. The sheets in `data/annotation/expert_kit/` were filled by a language model in two passes; they are not expert annotation and nothing from them is in the paper (see the note in that folder).
- **The dictionary lookups for the 48 words were made by an AI assistant.** A person compared 23 of the 134 source records with the dictionaries.
- **The hard subset is a diagnostic split**, defined from the label and a distance. It is not an independent test set.
- **Two defects were found late and corrected.** The template reader took a transliteration parameter for the ancestor form in 21 items, and four analyses attached items to their subset by spelling. Both were fixed and everything built on the baseline was rerun into `v2` folders; the first-run files are kept beside them (decision log, entries 110, 114 and 116). Not redone: the language-model check and the annotation sheets.

## 5. How the work was kept honest

```mermaid
sequenceDiagram
    participant P as Plan
    participant L as Decision log
    participant D as Data
    participant R as Report
    P->>L: Plan frozen, SHA-256 recorded
    L->>D: Only then is the data read or the model run
    D->>R: Result reported whichever way it falls
    R->>L: Deviations and corrections logged
```

- **Plans frozen before outcomes.** Each analysis has a plan file in `docs/` whose hash is in the decision log.
- **Mistakes are recorded.** A reader defect in the first audit run, a wrong citation count and a transliteration bug were each corrected and logged.
- **Sites' access rules were respected.** Two dictionaries that forbid automated reading were not used.
- **Copyrighted dictionary text is never stored**, only entry references and paraphrases.
- **Model output is never used as a label.**

## 6. Reproduce

**Set up** (Python 3.13):
```
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
```

**Tests:**
```
.venv/bin/python tests/test_audit_fixture.py
.venv/bin/python tests/test_baseline_helpers.py
.venv/bin/python scripts/annotation_agreement.py --self-test
```

**Offline analyses.** These read only files in this repository. Rerun on 2026-10-12, they gave output identical to the committed result files, except the order of two tied rows in `references.csv`.
```
R=data/raw/wiktionary/crosslingual_v1
.venv/bin/python scripts/audit_crosslingual.py      $R out/audit
.venv/bin/python scripts/baseline.py                $R out/baseline
.venv/bin/python scripts/baseline_supplementary.py  $R out/baseline
.venv/bin/python scripts/history_analysis.py        $R data/raw/wiktionary/history_v1 out/history
.venv/bin/python scripts/s8b_recorded_links.py      $R out/s8b
```

**Analyses that need a temporary copy of the Jambu database** (S4, S7a, S8a, S8c, S10, S11). Jambu's copy of Turner's dictionary has no licence, so it is not stored here: download it to a temporary folder, run, and delete it.
```
T=$(mktemp -d)
curl -sL -o $T/forms.csv https://media.githubusercontent.com/media/moli-mandala/data/main/cldf/forms.csv
curl -sL -o $T/edges.csv https://raw.githubusercontent.com/moli-mandala/data/main/cldf/edges.csv
.venv/bin/python scripts/s8a_missing_link.py     $T/forms.csv $T/edges.csv data/baseline_v2 out/s8
.venv/bin/python scripts/s10_three_conditions.py $T/forms.csv $T/edges.csv data/baseline_v2 out/s10
rm -rf $T
```

**The Transformer** (S11; about 30 minutes on a laptop GPU, PyTorch 2.14.1). Results vary slightly by device.
```
uv pip install --python .venv/bin/python -r requirements-neural.txt
.venv/bin/python scripts/s11_transformer.py $T/forms.csv $T/edges.csv data/baseline_v2 out/s11
```

**The charts in this file:** `.venv/bin/python scripts/make_readme_figures.py .`

**The paper:** `cd paper && tectonic main.tex`

**Not needed to reproduce:** the fetch scripts (`scripts/fetch_*.py`). The retrieved pages are stored with their revision IDs under `data/raw/wiktionary/`.

## 7. Repository map

| Path | What is there |
|---|---|
| `paper/` | LaTeX source, bibliography, PDF |
| `scripts/` | One script per analysis; the first line of each gives its plan and usage |
| `tests/` | Hand-worked test cases for the template reader and the distance |
| `docs/` | Frozen plans, reports, protocols, decision log |
| `data/raw/wiktionary/` | Retrieved pages and past revisions, with revision IDs |
| `data/audit/`, `data/baseline_v2/` | Result files |
| `data/annotation/` | The 48-word dictionary study and the unfilled expert sheets |
| `data/external/` | Rows used from two open expert databases, with attribution |
| `data/release/` | Draft benchmark file, data sheet and licensing review (not published) |
| `archive/` | Superseded drafts and plans, kept and never deleted |

## 8. Where every number comes from

Folders ending in `_v2` hold the corrected run that the paper reports; the matching `_v1` folders hold the first run and are kept for the record.

| Paper section | Result files | Script | Frozen plan |
|---|---|---|---|
| Audit | `data/audit/crosslingual_v1/measures.csv`, `tables.md` | `scripts/audit_crosslingual.py` | `docs/crosslingual_audit_plan.md` |
| Baseline | `data/baseline_v2/a1_cv.csv`, `a2_semi.csv`, `a3_transfer.csv`, `leakage_check.csv` | `scripts/baseline.py`, `scripts/baseline_leakage_check.py` | `docs/baseline_plan.md` |
| Dissociation, citation | `data/baseline_v2/s2_dissociation.csv`, `s3_citation.csv`, `oof_predictions.csv.gz` | `scripts/baseline_supplementary.py` | `docs/supplementary_plan.md` |
| Turner at scale | `data/audit/turner_scale_v2/` | `scripts/turner_scale.py` | `docs/supplementary_plan_s4.md` |
| Dictionary on the hard items | `data/audit/s7_v2/` | `scripts/s7a_turner_by_subset.py`, `scripts/s7b_history_by_subset.py` | `docs/supplementary_plan_s7.md` |
| The missing link | `data/audit/s8_v2/` | `scripts/s8a_missing_link.py`, `scripts/s8b_recorded_links.py` | `docs/supplementary_plan_s8.md` |
| Language model | `data/llm_s5/` | `scripts/llm_dissociation.py` | `docs/supplementary_plan_s5.md` |
| Language model, larger | `data/llm_s5b/` | `scripts/llm_dissociation.py`, `scripts/llm_by_route.py` | `docs/supplementary_plan_s5b.md` |
| Expert check, thirteen languages | `data/audit/iecor_v2/`, `data/external/iecor/` | `scripts/iecor_expert.py` | `docs/supplementary_plan_s9.md` |
| Three input conditions, grouped folds | `data/audit/s10_v2/` | `scripts/s10_three_conditions.py` | `docs/supplementary_plan_s10.md` |
| The same with a character Transformer (needs PyTorch) | `data/audit/s11_v2/` | `scripts/s11_transformer.py` | `docs/supplementary_plan_s11.md` |
| Label history, two past snapshots | `data/audit/history_v1/`, `data/audit/s7_v2/s7b_*.csv` | `scripts/history_analysis.py`, `scripts/s7b_history_by_subset.py` | `docs/supplementary_plan.md` (S1), `docs/supplementary_plan_s7.md` (S7b) |
| Romanian expert check | `data/audit/wold_romanian_v1/`, `data/external/wold_romanian/` | `scripts/wold_romanian.py` | `docs/supplementary_plan_s6.md` |
| Hindi/Bengali source study | `data/annotation/pilot_1/`, `data/annotation/round_2/` | `scripts/compare_round.py`, `scripts/sense_citation.py` | `docs/evidence_extraction_protocol_v1.1.md` |

## 9. Data and licences

| Source | Terms as read | In this repository |
|---|---|---|
| English Wiktionary | CC BY-SA 4.0 | Page text with revision IDs |
| World Loanword Database, Romanian (Schulte 2009) | CC BY 4.0 | Rows used |
| IE-CoR 1.1 (Heggarty, Anderson and Scarborough 2024) | CC BY 4.0 | Rows used |
| Turner's comparative dictionary; two of the three other dictionaries | In copyright | Entry references and paraphrases only |
| Jambu database (copy of Turner) | No licence stated | Nothing. Files derived from it are named `NOT_FOR_RELEASE` and are ignored by git |

The full review is `data/release/LICENSING_REVIEW.md`. It is a draft and is not legal advice. No licence file for the code has been chosen yet.

## 10. Open work

1. Two qualified annotators fill the blind sheets for the hard items (`data/annotation/expert_kit/README.md`). This is the largest gap.
2. Spot-check the remaining 111 dictionary lookups of round 2.
3. S12: fine-tune a pretrained character-level model on the three inputs (`docs/supplementary_plan_s12.md`; notebook `docs/s12_kaggle_notebook.ipynb`).
4. Rebuild the draft release file and the annotation sheets from the corrected baseline (`data/baseline_v2/`).

## 11. Rules for this repository

- Frozen files are not edited; corrections go in new files and in the decision log.
- Nothing is deleted: superseded files go to `archive/`.
- No dictionary text is stored for copyrighted dictionaries.
- Model output is never used as a label or as validation.
- `research.md` §13 (Results) stays empty; it belongs to a later study that has not been run.

## 12. Words used in this file

| Term | Meaning |
|---|---|
| Route | How a word entered the language: inherited, learned, or semi-learned |
| Ancestor form (etymon) | The word in the old language (Sanskrit, Latin, …) that the modern word comes from |
| Edit distance | How many letter changes turn one form into the other, scaled to 0–1 |
| Congruent / dissociated | The label agrees with / goes against how close the word is to the ancestor form |
| Macro-F1 | A score from 0 to 1 that treats both classes equally; 0.5 is roughly chance here |
| Frozen plan | A written plan whose fingerprint was recorded before the data were looked at |
| Wilson interval | A 95% range of uncertainty around a percentage |
