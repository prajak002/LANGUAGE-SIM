# Research plan: inherited or learned? Modelling the intermediate stage to attribute words to historical strata

_Canonical research document. Version 3.0, 2026-10-10 (project reset)._

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

### Primary: RQ1

> For a modern Indo-Aryan word *w* paired with its attested Old Indo-Aryan etymon *e*, does a model that represents inheritance as an explicit path through a latent Middle Indo-Aryan stage, and compares it by likelihood against a direct learned-borrowing channel, give better-calibrated attribution of *w* to the **inherited (tadbhava)** vs. **learned (tatsama)** stratum than the same transducers without the intermediate stage?

| Element | Specification |
|---|---|
| **Input** | (w, e, language L). Training also uses attested MIA forms (Pāli/Prakrit), but only for etymons outside the test split |
| **Target** | P(stratum = inherited \| w, e, L) |
| **Evidence conditions** | With vs. without the latent intermediate stage; everything else identical |
| **Comparison** | Proposed pathway model **P** vs. ablation **B4** (identical transducers, no intermediate stage). This isolates the intermediate-stage contribution |
| **Outcome** | Paired difference in Brier score on an expert-adjudicated gold test set; uncertainty clustered by etymon |

### Secondary questions

- **RQ2 (comparison with existing approaches; confirmatory).** Does P beat the strongest existing-style baseline? Candidates are the direct word–etymon classifier in the style of Cristea et al. 2021, the phonotactic borrowing detector of Miller et al. 2020, and surface similarity. Same metric, same test set.
- **RQ3 (LLMs and contamination; exploratory).** How well do LLMs attribute strata? How much of that performance disappears on items they cannot recall from published etymologies (recall probe), or on entries created after their training cutoff (temporal split)?
- **Replication (exploratory, stage 3).** Does the P-vs-B4 comparison replicate on Romance learned vs. inherited data (Cristea et al. 2021, if obtainable)? Romance is the same family, a different branch. **No family-level generalisation claim is possible** from two settings.

Semi-learned (*ardhatatsama*) words are a **diagnostic class**: where the model places them is reported descriptively. They are not part of the primary binary test, because the Wiktionary counts are small (Hindi 98, Bengali 44) and the category is graded.

---

## 5. Hypotheses (ours, untested)

- **H1 (RQ1).** Brier(P) < Brier(B4).
  - **Rationale:** inherited words carry MIA-mediated changes (e.g., consonant-cluster assimilation) that a learned-borrowing channel cannot produce, and that a direct ancestor→modern transducer must learn without the intermediate structure.
  - **Counter-expectation:** learned words are often near-identical to the etymon, so direct models may already separate the classes, leaving no room for gain.
- **H2 (RQ2).** Brier(P) < Brier(best of B1–B3).
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
- **Baselines:**
  - **B1:** surface similarity (normalised edit distance word–etymon, logistic).
  - **B2:** direct word–etymon feature classifier (Cristea-style re-implementation).
  - **B3:** monolingual phonotactic borrowing detector (Miller et al. 2020-style).
  - **B4:** pathway transducers without the intermediate stage.
  - **B5:** LLM zero/few-shot (needs API approval).
  - **P:** proposed model.
- **Ablations (exploratory):**
  - without attested MIA training data (latent only);
  - without LLM proposals;
  - without calibration;
  - with alternative transcriptions (native script vs. IAST vs. broad IPA).

---

## 8. Evaluation (summary)

- **Primary metric:** Brier score of P(inherited) on the gold test set.
- **Confirmatory contrasts:** C1 = P vs. B4 (RQ1); C2 = P vs. the strongest of B1–B3, chosen on the dev split before testing (RQ2).
- **Inference:**
  - item-level paired Brier differences;
  - 95% CIs by cluster bootstrap over etymons;
  - two-sided sign-flip permutation test on per-etymon summed differences;
  - Holm–Bonferroni over {C1, C2}.
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
| "This is Cristea et al. 2021 applied to Hindi/Bengali" | The confirmatory test is about *method* (intermediate stage vs. none, C1), not language coverage. If C1 fails, the paper is a dataset and negative-result paper, not a method paper |
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

1. Gold test-set size (from simulation) and annotation budget.
2. Expert annotators: at least two with Indo-Aryan historical training, plus an adjudicator. **None recruited.**
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
| Novelty checks (`docs/novelty_audit.md` §5) | ⏳ Required before any experiment |
| Data audit (download) | ⏳ Needs approval |
| Annotation | ⏳ Needs experts |
| Experiments | ⏳ Not started |

---

## 13. Results

_Empty. To be filled only from executed, logged experiments._
