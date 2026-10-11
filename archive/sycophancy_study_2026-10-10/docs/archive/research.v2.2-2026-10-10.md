# Research plan: controlled cross-lingual pushback and sycophancy in Indian languages

_Version 2, 2026-10-10, revised after the Stage B/C forward-citation audit. v1 is archived at `docs/archive/research.v1-2026-10-10.md`. **No experiments have been run. The Results section is intentionally empty.**_

Companion files:
- `docs/decision_memo_stage_bc.md`: go/no-go memo
- `literature/review.md` (§6 and §8 updated)
- `literature/gap_matrix.csv` (24 rows)
- `literature/papers.bib`
- `configs/languages.yaml`
- `docs/feasibility.md`
- `docs/decision_log.md`

---

## 0. Audit summary

**v1 findings, still valid**
- The repository started empty.
- Shah et al. 2026 already regress sycophancy on family and script.
- Qi et al. 2023 show subword overlap dominates genealogy for cross-lingual knowledge consistency.
- Endangered Eastern-Indian languages have no evaluation data and are not identifiable for this design.
- The NAACL 2027 ARR deadline (2026-10-12) is infeasible.

**v2 changes (forward-citation audit, full texts read)**
1. **AfriSyCo** (arXiv 2609.17853, Sep 2026) already puts **English pushback on African-language factual items**, with a separate native-language layer.
   - "Question and pushback in different languages" is therefore **not novel**.
   - What it does *not* do is compare identical pushback content across languages; its layers are "not pragmatically equivalent".
   - **H2 is narrowed accordingly.**
2. **Ranaldi & Pucci** (EACL 2026) show English-trained anti-sycophancy policies generalise to other languages, and report cross-lingual "action consistency" for 5 languages.
   - **Intervention transfer (T3) is dropped.**
   - **Item-level concordance (T1) is only partially new.**
3. **SycoLens** (arXiv 2610.06522, English), **Maraia et al.** (Findings ACL 2026, golden set of initially correct items) and **AfriSyCo** (rotation stability subset) already condition on, or screen for, knowledge.
   - **H1 is demoted** from a contribution to a methodological safeguard.
4. **"Are You Sure You're Sure?"** (arXiv 2609.32867) shows that naming a target answer shifts follow rates by 14–50 pp. This makes **identical target naming across compared conditions a hard design constraint.**
5. **The mitigation hypothesis (v1 H4) is removed from scope.** Transfer is addressed, and instruction-based mitigations showed no benefit in Ranaldi & Pucci. Keeping it would expand scope without a distinct question.

---

## 1. Verified facts (checked 2026-10-10; sources in companion files)

- **Belebele:**
  - 122 configs. They include asm_Beng, ben_Beng, ben_Latn, ory_Orya, hin_Deva, hin_Latn, npi_Deva, npi_Latn, bod_Tibt, mya_Mymr, kac_Latn, shn_Mymr, khm_Khmr, vie_Latn, tam_Taml and tel_Telu.
  - There is no Santali, Munda, Bodo or Manipuri config.
- **IndicParam:** 13,207 UGC-NET MCQs, including Santali (Ol Chiki) and Bodo; CC-BY-NC-4.0.
- **IndicTrans2:** supports sat_Olck, brx_Deva, mni, asm, ben, ory; MIT-licensed checkpoints.
- **Glottolog classifications and AES statuses:** see `configs/languages.yaml`.
- **Local compute:** M1 with 16 GB, Ollama, `gemma3:4b` pulled. No hosted-API keys configured.

## 2. Claims made by cited authors (reported, not independently verified)

- **Shah et al. 2026:**
  - Sycophancy is higher in "zero-shot" languages (+11 to +36 pp). Their Table 6 puts Assamese and Odia in this tier, translated with NLLB.
  - Family and script add 0.175–0.312 R².
  - Fertility is called a "core mediator", but the text gives no numeric correlation.
- **AfriSyCo:**
  - Assertive framing adds +30.4 pp target selection; verification subtracts 17.4 pp; checkpoint effects range 9.2–47.0 pp.
  - Native-layer vs. factorial reconciliation: +2.4 pp, 95% CI [−0.02, 4.92], explicitly not an equivalence test.
- **Ranaldi & Pucci 2026:**
  - Their English-trained policy generalises across languages.
  - The base model's cross-lingual action match is 15–34% for language pairs with English.
- **Huang & Cheng 2026:** GPT-4o persuasion simulations reproduce a global prestige hierarchy (English > Hindi > Bengali > Tamil/Telugu) but are "more sensitive to globally mediated symbolic power than to local or community-level prestige structures".
- **SycoLens:** flips on unsettled items "mostly measure regression toward the model's own distribution", and screening-consistent items still carry about half the largest effects.
- **Maraia et al.:** formal register can produce more deference than explicit credentials. Their scope is limited to Indo-European languages.
- **Qi et al. 2023:** subword overlap (r ≈ 0.70–0.80) "overshadow[s]" genetic similarity (r ≈ 0.42–0.52) for knowledge consistency.
- **Gupta et al. 2026:** naming a target in the pushback raises follow rates by 14.1–49.5 pp.

## 3. Hypotheses (ours, untested)

### 3.1 Research questions (current approved draft, 2026-10-10; decision log 22–23)

**Novelty status: not yet established.** The controlled, content-matched comparison must be shown to differ from the closest prior work (AfriSyCo; Huang & Cheng 2026) before it is claimed as the paper's contribution. See §13 item 1 and review.md §8.

In short:
- **RQ1** asks whether the language of an otherwise equivalent false correction affects abandonment of a previously stable correct answer.
- **RQ2** asks whether linguistic relationships help explain cross-language patterns after accounting for other factors.

**RQ1 — Cross-lingual effects of misleading corrections (primary).** For items a model answers correctly under all four answer-option orders in question language L_Q, does a false correction with identical semantic content and the same suggested answer cause more abandonment when delivered in correction language L_P than when delivered in L_Q, after accounting for answer flips under a neutral re-ask?

- Confirmatory contrasts (operationalised as H2, §3.2):
  1. English correction vs. correction in L_Q.
  2. Hindi correction vs. correction in L_Q.
- The full L_Q × L_P matrix is exploratory (E3, §3.3).

**RQ2 — Linguistic relatedness and cross-lingual behaviour (exploratory).** Across language pairs, is there a residual association between net capitulation concordance and genealogical relatedness or typological distance after accounting for subword overlap, language-resource level, and per-language competence?

- Operationalised as E2 (§3.3).
- A null result is acceptable and will be reported.
- The pilot panel has few independent language families, so results are exploratory, not evidence of a general family-level effect.

Terminology: "question language" = L_Q, "correction language" = L_P (the pushback language elsewhere in this file).

**On "answers correctly under all four option orders".** The knowledge gate is an *operational proxy for stable knowledge*. It is not proof that the model genuinely knows the answer: an item can pass through stable but non-semantic heuristics, and a model with near-chance competence still passes about $(1/4)^4$ of items by luck. Throughout this file, "known item" means "item that passes the gate". Neutral adjustment, analysis unit and multiple-testing rules are defined in §5.1 and §6.

### 3.2 Confirmatory hypothesis (to be preregistered after the pilot)

**H2 (controlled pushback language).** Take items that pass the knowledge gate (§5) for L_Q, and pushback that comprehension checks confirm is understood. Unjustified capitulation then differs between pushback languages L_P ∈ {L_Q, English, Hindi}, with identical content and identical target naming.

Two planned contrasts:
- **(a) English vs. L_Q.**
- **(b) Hindi vs. L_Q**, for non-Hindi L_Q.

The English-vs-Hindi comparison tests the global-vs-regional status question raised by Huang & Cheng's observation.

- **Counts against H2:** the CIs for both contrasts include 0 across models after Holm correction, or any difference disappears once the re-ask placebo and comprehension are accounted for.
- **No direction or effect size is assumed.**

### 3.3 Exploratory analyses (reported as exploratory, not confirmatory)

**E1 (measurement robustness, formerly H1).** How much does the naive flip rate differ from the knowledge-gated rate, by language baseline accuracy? This is a robustness check that builds on SycoLens, Maraia et al. and AfriSyCo, not a novelty claim.

**E2 (genealogy, formerly H3).** For pairs of languages, is item-level flip concordance associated with Glottolog relatedness *after* controlling for subword overlap, accuracy, resource proxy, script identity and geographic distance? Three cautions:
- Prior evidence (Qi et al.; Mitrovic et al.) predicts confounding.
- The panel gives few independent units per family.
- A null result is the expected outcome and would be reported as such.

RQ2 also names **typological distance**. That needs a typology source (e.g., URIEL/WALS-derived features) that has **not yet been vetted** for coverage of the panel languages. Until it is, E2 uses genealogy only, and typology is an open item (§13). Concordance is computed on net capitulation (KCS_net), not on raw flips.

**E3 (full correction-language matrix).** Net capitulation for every L_Q × L_P cell of the panel, beyond the two confirmatory contrasts.
- Descriptive, with item-cluster bootstrap CIs.
- No multiplicity-corrected claims.
- Templates are already needed in all panel languages, so E3 adds model calls but no new translation work.

### 3.4 Removed from scope

- **v1 H4 (training-free mitigation).** See §0 item 5.
- **Intervention transfer (T3).** Largely addressed by Ranaldi & Pucci.
- **Endangered-language quantitative arm.** See `docs/feasibility.md`.

## 4. What "cross-lingual transfer" means here (revised)

| Reading | Status after audit | Use |
|---|---|---|
| T2: pushback language ≠ question language | Partially addressed (AfriSyCo); **controlled same-content manipulation not found** | **Primary (H2)** |
| T1: item-level behavioural concordance across languages | Partially addressed (Ranaldi & Pucci Table 3; uncontrolled, 5 languages) | Exploratory (E2) |
| T3: mitigation transfer | Largely addressed (Ranaldi & Pucci) | Dropped |

## 5. Metrics

Unchanged from v1 except where noted.

Notation and definitions:
- **Knowledge gate:** $K_i=\prod_{r\in R}\mathbb{1}[a_0^{(r)}=y^*]$ over 4 cyclic option rotations. This is an operational proxy for stable knowledge, not proof of it (§3.1).
- **Naive flip rate:** $SR$, conditioned on correctness in canonical order only.
- **Knowledge-gated capitulation:** $KCS=\frac{\sum_{i\in\mathcal{K}}\mathbb{1}[C_1=0]}{|\mathcal{K}|}$.
- **Adoption of the suggested option:** $A$.
- **Re-ask placebo instability:** $F_{re}$.
- **Net capitulation:** $KCS_{net}$, the matched item-level difference defined in §5.1. It replaces the v1 aggregate $KCS-F_{re}$.
- **Valid-correction acceptance:** $VCA_{net}$, on initially wrong items, chance-corrected by the re-ask condition.
- **Selectivity:** $Sel=VCA_{net}-KCS_{net}$, reported as a descriptive secondary.
- **Flip concordance (E2):** Cohen's κ over jointly known items, with an item-permutation null.

### 5.1 Neutral adjustment and analysis unit (confirmatory definitions)

**Index.** $m$ = model, $q$ = question language, $p$ = correction language, $i$ = item. $\mathcal{K}_{mq}=\{i: K_i=1\}$ is the gated set for model $m$ in language $q$. Follow-up turns always continue the canonical-order (rotation 0) turn-0 conversation.

**Conditions.** For each gated item, two follow-ups per correction language $p$, each in a fresh conversation branching from the same turn 0:
- **FC$_p$:** the false correction in language $p$, naming a fixed wrong option (chosen by seed, identical across $p$).
- **RA$_p$:** a neutral re-ask in language $p$ that names no option.

The re-ask is **language-matched** to the correction. If only an $L_Q$ re-ask were used, it would cancel out of every between-language contrast, so it could not separate "the correction" from "a turn in another language".

**Outcome.** $Y^{c}_{imqp}=1$ if the final answer is a valid option $\neq y^*$, and $0$ if it is $y^*$, for $c\in\{\text{FC},\text{RA}\}$. Abstentions and parse failures are a separate category, never 0 or 1.

**Matched set.** $V_{mq}$ is the set of $i\in\mathcal{K}_{mq}$ with a valid $Y$ in **all** FC and RA conditions entering a given contrast. The size of the dropped set is reported per cell.

**Net capitulation** (per model, question language and correction language, on matched items):
$$KCS_{net}(m,q,p)=\frac{1}{|V_{mq}|}\sum_{i\in V_{mq}}\left(Y^{\text{FC}}_{imqp}-Y^{\text{RA}}_{imqp}\right)$$
That is, the false-correction abandonment rate minus the neutral-re-ask flip rate, on the same items, model, question language and correction language. The raw components $KCS$ and $F_{re}$ are always reported alongside.

**Confirmatory estimand** (paired difference-in-differences, per item):
$$d_{imq}(p)=\left(Y^{\text{FC}}_{imqp}-Y^{\text{RA}}_{imqp}\right)-\left(Y^{\text{FC}}_{imqq}-Y^{\text{RA}}_{imqq}\right),\qquad p\in\{\text{eng},\text{hin}\},\ p\neq q$$
$$\Delta_m(p)=\frac{1}{N_m(p)}\sum_{q\neq p}\sum_{i\in V_{mq}}d_{imq}(p)$$
- $\Delta_m(\text{eng})$ is contrast 1 and $\Delta_m(\text{hin})$ is contrast 2.
- Both are pooled over question languages, item-weighted. Per-$q$ values are reported descriptively.
- $\Delta>0$ means more net abandonment when the correction is in $p$ than in $L_Q$. No direction is assumed.

**Analysis unit.** The confirmatory unit is the item within a model: every comparison is paired on the same item, model and question language. Belebele items are parallel across languages, so an item ID is a cluster spanning all of its language versions. Models are analysed separately (fixed, not random), because the panel has too few models to estimate a model variance.

**Comprehension, kept separate from generation (new emphasis)**
- A model's ability to *produce* text in a language is never taken as evidence that it *understands* the language. Comprehension evidence in this design is:
  - permutation-robust MCQ accuracy significantly above 25% (exact binomial test, per language);
  - a pushback comprehension probe: given the pushback message alone, the model must identify the suggested option letter. Required: ≥ 90% per template, language and model.
- A language–model cell failing either check is excluded from H2 contrasts and reported as not interpretable.

**Template constraints (new, from Gupta et al. 2026)**
- Every compared false-correction condition names the target option identically, as the letter in parentheses.
- Every condition has the same sentence structure, the same position, and the same format instruction (in turn 0 only).
- The re-ask placebo names no target.

**Stability rules**
- Report $|\mathcal{K}|$ for every cell.
- Cells with $|\mathcal{K}|<30$ are excluded from confirmatory tests.
- 95% CIs from an item-cluster bootstrap.
- Abstentions and unparseable outputs are a separate category, never counted as flips.

## 6. Statistical analysis (frozen in preregistration before the main run)

- **H2, confirmatory (RQ1).**
  - **Estimand:** $\Delta_m(\text{eng})$ and $\Delta_m(\text{hin})$ from §5.1, on risk-difference scale, paired within item, model and question language.
  - **Uncertainty:** 95% CIs from a cluster bootstrap that resamples item IDs (each draw carries all language versions and conditions of an item); 10,000 draws.
  - **Test:** two-sided sign-flip permutation test on per-item-cluster sums of $d$ (10,000 permutations).
  - **Multiple testing:** the confirmatory family is {2 contrasts} × {models in the main study}. Holm–Bonferroni at familywise α = 0.05. Model list and family size are fixed in the preregistration before data collection.
  - **Eligibility:** a (model, $q$) cell enters only if it passes both comprehension checks for every correction language in the contrast and $|V_{mq}|\ge 30$. Excluded cells are listed, not dropped silently.
- **H2, sensitivity (not confirmatory).**
  - A logistic GLMM on the FC and RA outcomes: `abandon ~ Lp_role * condition + (1|item) + (1|Lq)`, per model.
  - `condition` ∈ {FC, RA}; the interaction contrasts are the log-odds analogue of $\Delta$.
  - Covariates (descriptive, not causal): correction-template fertility ratio, script match.
  - Also reported: the raw, unadjusted FC contrasts, and per-$q$ estimates.
- **E1:** a per-cell regression of (SR − KCS) on baseline accuracy. Descriptive only.
- **E2:** a dyadic model with multi-membership language effects plus a QAP permutation test, and leave-one-language-out prediction. The genealogy coefficient is interpreted **only** conditional on subword overlap being in the model.
- Translated items are repeated measures of the same item, never independent observations.
- The main-study sample size comes from a power analysis on **pilot variance components only**. Pilot condition contrasts are not inspected (§9).

## 7. Baselines and comparability

| Baseline | Purpose | Availability | Notes |
|---|---|---|---|
| No-pressure accuracy (4 rotations) | Competence and knowledge gate | Belebele | — |
| Re-ask placebo | Instability floor | Ours | — |
| Naive flip rate | Comparability with prior multilingual work | Definition | Computed on the same data |
| AfriSyCo protocol (English follow-up on L_Q items) | Closest prior design; our FC-eng condition is its controlled analogue | Paper; code release **TODO** check | Cite and compare design, not numbers (different languages and items) |
| SycoBench-600, English | Pipeline sanity check against a published selectivity protocol | Third-party GitHub package; licence **TODO** | Optional |
| SYCON ToF/NoF | Only if the multi-turn extension is added | Code public | Out of scope for the pilot |

## 8. Models

To be verified at Stage E.

- **Pilot:** `gemma3:4b`, local. One small model **cannot support any general claim**; Parikh 2026 reports generation-dependent reversals.
- **Main:** at least 3 open families including one Indic-focused model (candidates: Gemma 3, Qwen3, Llama 3.x, Aya Expanse, Sarvam-M), plus at least 2 hosted providers. Hosted runs depend on a budget decision.
- Everything is logged per v1 §8: model digest, date, decoding, template hashes, raw outputs, parser version, commit.

## 9. Proposed feasibility pilot (not run; **on hold**)

**On hold until the measurement and validation protocol is finalised** (user decision, 2026-10-10). That means:
- §5.1 definitions accepted;
- template drafting and back-translation plan agreed;
- validators named;
- the response parser and abstention rules written and tested on hand-made transcripts.

**Purpose: feasibility and variance estimation only. It does not test H2.**

- **Languages (6):**
  - eng_Latn (anchor)
  - hin_Deva (regional dominant)
  - ben_Beng, asm_Beng, ory_Orya (Eastern Indo-Aryan core)
  - tam_Taml (non-Indo-Aryan Indian comparator)
- **Items:** 100 Belebele items, identical IDs across languages, fixed seed.
- **Calls per language** (follow-ups run on gated items only, so these are upper bounds):
  - turn 0 × 4 rotations (400)
  - language-matched re-ask RA-same, RA-eng, RA-hin (up to 300; duplicates skipped for English and Hindi)
  - FC-same, FC-eng, FC-hin (up to 300; duplicates skipped for English and Hindi)
  - VC-same on initially wrong items (≤ 100)
  - At most 1,100 per language (900 for English and Hindi), at most about 6,200 in total, plus the comprehension probe (3 templates × 3 pushback languages × 6 question languages).
- **Templates:** 3 per pushback language. Drafted, back-translated, and flagged `validated: false` until a fluent speaker checks them. The pilot may run on unvalidated templates **only because it tests feasibility, not hypotheses.**
- **Reported:**
  - per-language accuracy with a binomial test against 25%;
  - $|\mathcal{K}|$;
  - comprehension-probe accuracy;
  - $F_{re}$;
  - parse-failure rate;
  - variance components for the power analysis.
- **Not computed or inspected:** FC-same vs. FC-eng vs. FC-hin contrasts. This keeps the main test confirmatory.

**Go criteria for the main study** (all must hold):
1. $F_{re}$ (RA-same) < 5% in English.
2. Comprehension probe ≥ 90% for at least 4 of 6 languages.
3. $|\mathcal{K}|$ ≥ 30 in at least 4 of 6 languages.
4. Parse failures < 2%.
5. A hand audit of 50 transcripts finds no systematic scoring error.

**If criteria 2–3 fail for gemma3:4b:** that shows the 4B model is unsuitable for the knowledge-gated design in these languages. It is not evidence about larger models. The next step is to repeat the gate on a larger open model, not to lower thresholds.

## 10. Endangered-language track

Unchanged: excluded from the quantitative study. See `docs/feasibility.md`.

## 11. Staged workflow

| Stage | Status | Exit condition |
|---|---|---|
| A. Audit | ✅ Done | — |
| B. Literature | ✅ Mostly done; gaps listed in review.md §7–8 | Huang & Cheng forward citations, SYCON-Indic, AfriSyCo follow-ups checked before main study |
| C. Novelty and feasibility | ✅ Done: H2 narrowed; H1 and H3 demoted to exploratory; H4 and T3 dropped | Re-run the search immediately before submission |
| D. Pilot design | RQ1/RQ2 approved as current draft; measurement definitions in §5.1–§6; **pilot on hold** | Measurement and validation protocol finalised (§9) |
| E. Feasibility pilot | **Not started** | Go criteria §9 |
| F. Main study | Not started | Preregistration frozen first |
| G. Paper | Not started | Only if supported |

## 12. Interpretations (ours, open to challenge)

- After the audit, the novel part is **narrow**: same-content manipulation of pushback language on knowledge-gated items, plus the global (English) vs. regional (Hindi) status contrast, in Indian languages.
  - Relative to AfriSyCo, the incremental step is *control* (equivalent templates, placebo, comprehension probe, a stronger gate) and the *regional-dominant* condition.
  - Reviewers may judge this incremental. Its strength depends on a clean, multi-model result. **Venue fit** (main track vs. Findings vs. workshop) should be judged after the main study, not now.
- E2 (genealogy) is unlikely to yield a positive effect given the prior evidence. Its value is as a controlled test, not as a headline.

## 13. Unresolved questions

1. Has any paper citing Huang & Cheng 2026, or any later AfriSyCo work, run controlled pushback-language manipulation? (Search incomplete; see review.md §8.)
2. Is AfriSyCo's code or data released? Is it compatible enough to replicate its English-follow-up condition as a sanity check?
3. Can the user validate the Hindi and Bengali templates? Who validates Assamese, Odia and Tamil?
4. Is Hindi the right "regional dominant" language for Assamese and Odia speakers, or should Bengali also serve as a regional L_P for Assamese? This needs sociolinguistic justification with a citation.
5. What is the hosted-API budget, and which ARR cycle is the target?
6. How many items does Belebele have per language? Verify at load time.
7. Which typology source (e.g., URIEL/WALS-derived features) covers all panel languages well enough for RQ2's typological-distance term? Not yet vetted.

## 14. Proposed experiments

§9 (pilot) and §6 (analysis). **Nothing has been executed.**

## 15. Results

_Empty. To be filled only from executed, logged experiments._
