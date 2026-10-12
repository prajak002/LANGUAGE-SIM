# Research plan: inherited or learned? Modelling the intermediate stage to attribute words to historical strata

_Canonical research document. Version 3.2, 2026-10-11 (scope narrowed to a source-grounded feasibility study; decision log 56–58). v3.1 is at `archive/superseded_2026-10-11/research.v3.1-2026-10-10.md`; v3.0 is at `archive/superseded_2026-10-10/`._

> **Status: plan only.**
> - No experiments have been run, no model has been called, and no data have been downloaded.
> - The Results section is intentionally empty.
> - The previous sycophancy study is archived intact at `archive/sycophancy_study_2026-10-10/` (see `archive/README.md`).

**Companion documents:**

| File | Content |
|---|---|
| `literature/review.md` | Literature audit |
| `literature/gap_matrix.csv` | Prior work vs. this project |
| `literature/papers.bib` | Verified bibliography |
| `docs/novelty_audit.md` | Novelty claims and their status |
| `docs/methodology.md` | Model, assumptions, alternatives |
| `docs/experimental_protocol.md` | Splits, baselines, metrics, statistics |
| `docs/data_and_ethics.md` | Sources, licences, review, ethics |
| `docs/feasibility.md` | First-experiment plan and resources |
| `docs/decision_log.md` | Decisions, appended from entry 31 |
| `docs/evidence_extraction_protocol.md` | **Current work:** source-grounded extraction and pilot |
| `docs/evidence_extraction_protocol_v1.1.md` | Protocol v1.1 (frozen), used for round 2 |
| `docs/feasibility_report.md` | **Counts-only feasibility report** over the 48 practice lemmas |
| `docs/crosslingual_audit_plan.md`, `docs/crosslingual_audit_report.md` | Frozen plan and report of the 17-pair audit of Wiktionary's route records |
| `docs/baseline_plan.md`, `docs/baseline_report.md` | Frozen plan and report of the minimal form-based baseline on Wiktionary's labels (not the RQ1–RQ3 study) |
| `data/annotation/expert_kit/` | Blind sheets and agreement script for two human annotators (unfilled) |
| `paper/main.tex` | Paper **draft** built from the feasibility report (spot check pending) |
| `README.md` | Division of work: Part 1 (assistant, done), Part 2 (project lead) |

---

## 0. Current scope (v3.2): source-grounded feasibility study

**Why the scope changed.** No expert annotators are available. Without them this project **cannot claim independently validated historical-etymology labels**, and it cannot report inter-annotator agreement.

**Current primary question (RQ-F):**

> Can published etymological evidence be turned into consistent inherited / learned / semi-learned / other categories for Hindi and Bengali words? Specifically:
> - How often is the historical route recoverable from accessible scholarly sources?
> - How often do sources agree with one another and with Wiktionary?
> - Which category boundaries fail?

**Method:** `docs/evidence_extraction_protocol.md`.
- Labels are **source-grounded and model-extracted**, with the source, entry and evidence recorded for every item.
- The project lead spot-checks extraction fidelity.
- Disputed, undecidable and no-source outcomes are findings.

**Claims this version will not make:**
- validated gold labels;
- inter-annotator agreement;
- model-generated labels as independent verification;
- any classifier result.

**RQ1–RQ3 below (the classifier study) are future work.** They are kept for reference and are pursued only if the feasibility study shows enough recoverable, consistently labelled items, and if a route to independent validation exists. Novelty remains provisional (`docs/novelty_audit.md` §3).

---

## 1. From the vision to a testable problem

**The vision.** Use multilingual AI to find overlooked historical links between linguistic varieties, distinguish inheritance from borrowing, and produce traceable evidence that helps preservation.

**What cannot be tested.** "Discovering" an undocumented language or intermediate variety has no ground truth. Model output alone cannot establish it (decision log 2). The five categories of "missing link" are kept distinct:
1. a documented variety with underexplored relationships;
2. a poorly documented but attested variety;
3. an intermediate stage supported by indirect evidence;
4. a reconstructed ancestral form;
5. a variety lacking sufficient evidence.

This project works with **category 2–4 evidence** (attested Middle Indo-Aryan forms, reconstructed or latent intermediate forms). It makes **no claim about category 5**.

**What can be tested.** Every modern word with an ancestral etymon reached the modern language by one of two historical paths:
- **inherited:** through the intermediate stages (for Indo-Aryan, through Middle Indo-Aryan: *tadbhava*);
- **learned:** borrowed later, directly from the prestige ancestor language (*tatsama*), possibly partly adapted (*ardhatatsama*).

Whether a word passed through the intermediate stage is the concrete, checkable form of the "missing link" question. This question can be scored against expert labels.

### 1.1 The historical claim, stated precisely

A label in this project claims only the following:

- **inherited (tadbhava):** the scholarly consensus, as judged by expert annotators with the cited references, is that the word's form results from continuous transmission from OIA through some MIA variety into the modern language. The claim does **not** name a particular attested MIA variety as the ancestor.
- **learned (tatsama):** the consensus is that the word entered the modern language (or an earlier NIA stage) from Sanskrit after the MIA period, keeping a Sanskrit-like form.

Explicit non-claims:
- **Resemblance to Sanskrit is not evidence of borrowing.** Some inherited words remain close to their etymon (cf. Cristea et al. 2021's Romanian *suc*). Labels come from experts and references, never from similarity.
- **Histories may be mixed:** semi-learned reshaping, re-Sanskritisation of inherited words, analogy, and transmission via another NIA language. Such items are labelled **mixed/complex** and kept out of the primary binary test (§7.3).
- **The intermediate form is representational, not historical.** The latent MIA form in the model is a device for scoring the inherited hypothesis. Agreement with an attested Pāli or Prakrit form is a descriptive check, not a claim of ancestry.

---

## 2. Stage A: audit of the previous material

| Category | Items |
|---|---|
| **A. Verified, reusable** | Glottolog classifications and AES statuses (`archive/.../configs/languages.yaml`); verified bibliographic metadata method; Belebele/Glottolog/WALS access scripts (scratchpad); evaluation discipline from the sycophancy work (freeze before outcomes, clustered bootstrap, preregistration with open decisions, reviewer protocol); WALS data showing typology/genealogy decorrelation (cross-family doc) |
| **B. Unverified or weak** | Indo-Aryan stage terminology (never source-verified); the claim in the first new-direction draft that withheld-stage recovery was novel (**false**: Bouchard-Côté 2013; Cathcart & Rama 2020); the citation "Forkel & List 2022" (**wrong**: it is List & Forkel 2021); all novelty statements of the sycophancy study (narrow, partly pre-empted by AfriSyCo) |
| **C. Retired for this project** | The sycophancy RQs, pilot and code (archived, not deleted); the cross-family sycophancy extension; the "ghost substrate" idea (decision 2); embedding similarity as evidence of genealogy; withheld-stage recovery as a headline contribution |

---

## 3. Stage B/C: candidate directions compared

Full evidence is in `literature/review.md` and `docs/novelty_audit.md`.

| Candidate | Novelty vs. closest work | Falsifiable | Data | Ground truth | Baselines | Statistics | Resources | Method or application | Beyond one family | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| A. Discover and rank overlooked relationships | Unclear | **No** (no truth for "overlooked") | Partial | **None** | Weak | Not feasible | High | Mostly application | Unclear | Reject as primary |
| B. Joint inheritance / borrowing / typology / chance discrimination | Partly addressed (List & Forkel 2021; Cristea 2021) | Yes | Yes (Wiktionary, Cristea data) | Expert-checkable | Strong | Feasible | Moderate | Method possible | Yes | **Core, narrowed** |
| C. Uncertainty-aware reconstruction of intermediate links | **Largely addressed** (Bouchard-Côté 2013; Cathcart & Rama 2020) | Yes | Yes | Attested forms | Strong | Feasible | Moderate | Incremental | Yes | Use as a **component**, not the claim |
| D. Disappearing-feature detection and documentation priorities | Unknown | Weak (outcome lies in the future) | Sparse | Hard | None | Hard | High (community) | Application | Unclear | Defer to a later stage |
| E. Benchmark of justified vs. plausible-but-false relationships for LLMs | Partly addressed (Liang 2026; Sousa Silva & Ahmadi 2026) | Yes | Yes | Labels exist | LLMs | Feasible | Low | Resource | Yes | Fold in as the **LLM contamination arm** |
| F. Full multi-evidence fusion (lexicon, morphology, chronology, geography, contact) | Unknown | Yes in principle | Uneven | Partial | Unclear | Hard | **Very high** | Method | Yes | Too large; reject for the first paper |

**Selected:** B narrowed to *learned vs. inherited strata*, using C as its mechanism (a latent intermediate stage) and E as a secondary analysis (LLMs under contamination control).

---

## 4. Research questions

### Primary: RQ1 (future work; see §0)

> For modern Indo-Aryan words with an expert-confirmed Old Indo-Aryan etymon and an unambiguous stratum, does explicitly modelling a historically constrained Middle Indo-Aryan pathway improve calibrated **inherited (tadbhava)** vs. **learned (tatsama)** attribution beyond established direct word–etymon classifiers? Does any improvement come from the **historical content** of the intermediate stage rather than from extra parameters or extra fitting flexibility?

This is a **candidate contribution, not an established novelty** (`docs/novelty_audit.md` §3).

| Element | Specification |
|---|---|
| **Input** | (w, e, language L). Training also uses attested MIA forms (Pāli/Prakrit), but only for etymons outside the test split |
| **Target** | P(stratum = inherited \| w, e, L) |
| **Evidence conditions** | With vs. without the latent intermediate stage; everything else identical |
| **Comparison** | (C1) P vs. the **strongest competitive baseline** chosen on dev from B1–B7 (§7). (C3) P vs. **P-shuffled** (the same architecture and data size, with the historical content of the intermediate stage destroyed) |
| **Outcome** | Paired difference in Brier score on an expert-adjudicated gold test set; uncertainty clustered by etymon |

### Secondary questions

- **RQ2 (where the gain comes from; confirmatory via C3).** Is P better than P-shuffled? A positive answer means the intermediate stage contributes historical evidence, not just capacity. B4 (no intermediate) and P-latent (latent intermediate, no attested MIA forms) give the structure-vs.-data decomposition (exploratory).
- **RQ3 (LLMs and contamination; exploratory).** How well do LLMs attribute strata? How much of that performance disappears on items they cannot recall from published etymologies (recall probe), or on entries created after their training cutoff (temporal split)?
- **Replication (exploratory, stage 3).** Does the P-vs-B4 comparison replicate on Romance learned vs. inherited data (Cristea et al. 2021, if obtainable)? Romance is the same family, a different branch. **No family-level generalisation claim is possible** from two settings.

Semi-learned (*ardhatatsama*) words are a **diagnostic class**: where the model places them is reported descriptively. They are not part of the primary binary test, because the Wiktionary counts are small (Hindi 98, Bengali 44) and the category is graded.

---

## 5. Hypotheses (ours, untested)

- **H1 (RQ1).** Brier(P) < Brier(strongest competitive baseline).
- **H1b (RQ2).** Brier(P) < Brier(P-shuffled).
  - **Rationale:** inherited words carry MIA-mediated changes (e.g., consonant-cluster assimilation) that a learned-borrowing channel cannot produce, and that a direct ancestor→modern transducer must learn without the intermediate structure.
  - **Counter-expectation:** learned words are often near-identical to the etymon, so direct models may already separate the classes, leaving no room for gain.
- **No effect sizes are assumed.**

---

## 6. Method (summary; full detail in `docs/methodology.md`)

**Competing generative hypotheses for w given e:**
- **H_inh:** e → m → w, with m a latent MIA form.

  $P(w\mid e,\text{inh}) = \sum_m P_{\theta_1}(m\mid e)\,P_{\theta_2,L}(w\mid m)$

  - θ₁ is trained on attested OIA→MIA pairs.
  - θ₂,L is trained on attested MIA→NIA pairs, or on inherited OIA→NIA pairs with m latent.
- **H_lrn:** e → w directly, via a learned-adaptation transducer P_{θ₃,L}(w | e) trained on learned-borrowing pairs.

**Decision rule:**
- The posterior is computed as $P(\text{inh}\mid w,e)=\frac{\pi_L\,P(w\mid e,\text{inh})}{\pi_L\,P(w\mid e,\text{inh})+(1-\pi_L)\,P(w\mid e,\text{lrn})}$.
- The prior π_L is estimated per language on the training split.
- The output is calibrated on the development split.
- **Abstention** applies only in the selective-prediction analysis.

**Why a likelihood ratio and not an additive score.** In the brief's conceptual decomposition S(h) = Σ w·S, the phonological, cognate and lexical terms are computed from the *same strings* and are strongly dependent. Adding them double-counts evidence, and the weights have no training procedure. Comparing likelihoods under explicit generative hypotheses uses each piece of string evidence once. It also yields probabilities that can be calibrated and scored with proper scoring rules.

**Role of the LLM:**
- a baseline;
- optionally, a **proposal source** for latent m candidates, added to the transducer beam.

**The LLM never decides the label.** Whether its proposals change P's likelihood approximation is an ablation.

**Evidence records.** Every prediction stores the top latent m candidates, the per-hypothesis log-likelihoods, the alignment, the training-data provenance (source, entry IDs) and the model version. This is an audit layer, not an inference engine.

---

## 7. Experimental design (summary; full detail in `docs/experimental_protocol.md`)

- **Languages:**
  - Hindi, Bengali, Assamese, Odia: modern targets with Wiktionary labels.
  - Sanskrit: OIA etyma.
  - Pāli and Prakrits: attested MIA forms, from Wiktionary etymology chains and, if licensed, CDIAL/Jambu.
- **Splits:** by **etymon cluster**. All descendants of one OIA etymon, including learned/inherited doublets of the same etymon, stay in one split. A second split holds out an Eastern language (Bengali, Assamese, Odia) entirely.
- **Gold test set:** expert-adjudicated labels on a stratified sample, annotated blind to Wiktionary labels and model outputs. Its size comes from a pre-specified simulation using silver-label variance (`OPEN DECISION 1`).
### 7.1 Competitive baselines

The comparator for C1 is the best of these on dev, frozen before test:

| ID | Baseline | Why it is competitive |
|---|---|---|
| B1 | Surface similarity (several string distances, logistic) | Kanojia 2019 observed that orthographic similarity already isolates tatsamas |
| B2 | Cristea et al. 2021 best configuration re-implemented: SVM with character n-grams plus word–etymon alignment features, orthographic and phonetic | About 90% F1 on Romance |
| B3 | Phonotactic borrowing detector (Miller et al. 2020 style; no etymon) | Established borrowing method |
| B4 | Direct inherited vs. learned transducer likelihood ratio, no intermediate stage | Same machinery as P, minus the stage |
| B6 | Character-level neural pair classifier (encoder over aligned word–etymon pair, phonological features) | Strong learned representation |
| B7 | Stacked classifier: all B1–B4 and B6 features plus the B4 likelihood ratio | Strongest combination without an intermediate stage |
| B5 | LLM zero/few-shot (exploratory only; needs API approval) | — |

### 7.2 Controls for "historical content vs. capacity"

| Control | What changes | What it tests |
|---|---|---|
| **P-shuffled** | MIA forms permuted across etymons within the same length band; same data size, alphabet and architecture | Whether historical correspondence content matters (**C3**) |
| **P-wrong-stage** | The intermediate is replaced with modern forms of a different NIA language | Whether *any* plausible related string helps |
| **P-latent** | m latent; no attested MIA forms | Structure without extra data |
| **Capacity-matched B4** | B4 with parameters and states matched to P | Whether the gain is parameter count |

### 7.3 Label audit before any claim

Label definitions and annotation rules are in `docs/annotation_guidelines.md` (draft v0.1; to be revised by experts). Codes: INH, LRN, SEMI, MIX, NIA (via another NIA language), EXT, NON, ETY, DIS, UNK.

1. **Wiktionary labels are candidates, not gold.**
2. **Expert audit** of a stratified sample, giving each item one of:
   - confirmed tadbhava;
   - confirmed tatsama;
   - semi-learned;
   - **mixed/complex history** (re-Sanskritised, analogical, transmitted via another NIA language);
   - **disputed** (references disagree);
   - wrong etymon;
   - other origin.
3. **Pathway justification**, per confirmed-tadbhava item. Experts record whether the inherited route is representable as a regular OIA→MIA→NIA development, with or without an attested MIA form. Items needing irregular, analogical or contact explanations are flagged **complex**.
4. **The primary test uses only** confirmed tadbhava with a justified pathway, and confirmed tatsama. Everything else is reported separately.
5. Silver–gold agreement, and the share of complex or disputed items, are **reported before any performance or novelty claim**.

- **Other systems:** P (proposed); P-latent, P-shuffled and P-wrong-stage (controls).
- **Ablations (exploratory):**
  - without attested MIA training data (latent only);
  - without LLM proposals;
  - without calibration;
  - with alternative transcriptions (native script vs. IAST vs. broad IPA).

---

## 8. Evaluation (summary)

- **Primary metric:** Brier score of P(inherited) on the gold test set.
- **Confirmatory contrasts:**
  - **C1** = P vs. the strongest competitive baseline among B1–B4, B6 and B7, chosen on dev before testing (RQ1).
  - **C3** = P vs. P-shuffled (RQ2).
  - C2 (P vs. B4) is now exploratory.
- **Inference:**
  - item-level paired Brier differences;
  - 95% CIs by cluster bootstrap over etymons;
  - two-sided sign-flip permutation test on per-etymon summed differences;
  - Holm–Bonferroni over {C1, C3}.
- **Secondary metrics:**
  - AUROC;
  - F1 per class;
  - expected calibration error (reported with its binning caveats);
  - risk–coverage curve and area under it for abstention;
  - for etymons with an attested MIA form held out of training, edit distance between P's top latent m and that form (descriptive only).
- **Uncertainty reported separately:**
  - aleatoric (posterior entropy);
  - epistemic (disagreement across a seed/bootstrap ensemble);
  - documentation gaps (no attested MIA form for this etymon);
  - label uncertainty (annotator disagreement).

---

## 9. Stage E: skeptical review

| Likely reviewer objection | Response or required evidence |
|---|---|
| "This is Cristea et al. 2021 applied to Hindi/Bengali" | C1 compares against a re-implementation of Cristea's best configuration and stronger stacked baselines. C3 tests whether the intermediate stage carries historical content. If either fails, there is no method claim |
| "Kanojia et al. 2019 already discussed tatsama/tadbhava computationally" | Yes. They *observed* that orthographic similarity finds tatsamas but misses tadbhavas in cognate detection, with descriptive definitions and no attribution classifier. That observation motivates B1 and failure check F3 |
| "The intermediate stage just adds parameters" | C3 (P-shuffled), capacity-matched B4 and P-wrong-stage are designed for exactly this |
| "Learned words look like Sanskrit; edit distance solves this" | B1 is a baseline. If B1 is near ceiling, the task is too easy and the project must move to harder cases: ardhatatsama, doublets, and the held-out Eastern language. That is a planned failure check (F3) |
| "Wiktionary labels are circular: editors used Turner, and so did you" | The gold test set is expert-labelled blind to Wiktionary. Transducers never see test etymons. Agreement between silver and gold labels is reported |
| "LLMs memorised Wiktionary" | RQ3 measures this directly with a recall probe and a temporal split. LLM results are never confirmatory |
| "Two settings do not show cross-family generality" | Agreed; no such claim is made. Romance is a replication, not a generalisation |
| "Etymon given as input is unrealistic" | Yes, by design. The task is pathway attribution *given* an etymology, which is how documentation work proceeds. Etymon discovery is out of scope |
| "Few independent units" | The units are etymons, clustered. Language-level claims are limited to per-language descriptives |

---

## 10. Limitations

- The task assumes the etymon is known.
- The labels inherit the theoretical framing of the tatsama/tadbhava categories, which are graded in reality.
- Wiktionary coverage is biased toward common words.
- MIA attestations are literary and uneven; they are not the direct spoken ancestors of each modern language.
- Only one family is in the confirmatory scope.
- Preservation impact is not measured in the first experiment.

---

## 11. Open decisions

1. Gold test-set size (from simulation) and annotation budget, including the label-audit sample (§7.3).
2. Expert annotators: at least two with Indo-Aryan historical training, plus an adjudicator. **None available.** The scope was changed to source-grounded extraction (§0). The expert route can resume if experts become available.
3. Data access: Wiktionary dump (download approval needed); CDIAL/Jambu licence (contact SOAS and the Jambu authors); Cristea dataset availability.
4. Transcription scheme for model input (IAST vs. broad IPA) and conversion tools.
5. Transducer family (WFST vs. neural seq2seq vs. both) and the beam size for the latent sum.
6. LLM baseline models and API budget.
7. Whether the temporal (post-cutoff) Wiktionary split is feasible (needs revision history).
8. Where the preregistration is frozen (the project is not a git repository).
9. Whether the sycophancy study is resumed later. It is archived; the user's decision.

---

## 12. Staged workflow

| Stage | Status |
|---|---|
| A. Repository audit | ✅ Done (§2) |
| B. Literature audit | ✅ Done, with gaps (`literature/review.md`) |
| C. Question selection | ✅ Done (§3–§4) |
| D. Method and protocol | ✅ Drafted (`docs/methodology.md`, `docs/experimental_protocol.md`) |
| E. Skeptical review | ✅ Done (§9; `docs/novelty_audit.md`) |
| F. Documents updated | ✅ Done |
| Novelty checks, round 2 | ✅ Kanojia 2019 (via thesis), Cristea full results, forward citations. ⏳ Remaining items in `docs/novelty_audit.md` §4 |
| Annotation practice round | ⛔ Set aside: no experts (archived, `archive/superseded_2026-10-11/`) |
| Practice-set fetch (48 Wiktionary pages) | ✅ Done 2026-10-10; raw, read-only, candidates only |
| Source-grounded extraction pilot (10 items; `docs/evidence_extraction_protocol.md`) | ✅ Extracted and compared (`docs/pilot_1_report.md`); ⏳ spot check by the project lead pending |
| Protocol v1.1 (`docs/evidence_extraction_protocol_v1.1.md`) | ✅ Frozen 2026-10-11, with Turner and J. Dāsa conventions verified |
| Round 2 (38 items) and feasibility report (`docs/feasibility_report.md`) | ✅ Extracted, frozen, compared; ⏳ spot checks pending; ⏳ scale-up decision open (report §8 recommends against scaling this protocol) |
| Feasibility study (RQ-F, §0) | ⏳ After the pilot |
| Data-audit plan (`docs/data_audit_plan.md`) | ✅ Drafted; bulk collection **on hold** |
| Label audit (§7.3) | ⏳ After the practice round |
| Classifier experiment | ⏳ Future work, conditional on RQ-F and on independent validation |
| Data audit (download) | ⏳ Needs approval |
| Annotation | ⏳ Needs experts |
| Experiments | ⏳ Not started |

---

## 13. Results

_Empty. To be filled only from executed, logged experiments._
