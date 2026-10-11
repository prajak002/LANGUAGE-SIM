# Experimental protocol (draft)

_2026-10-10, revised after novelty round 2 (decision log 39–43). **Not preregistered; not final.** Items marked OPEN must be resolved before freezing. Nothing has been run._

## 1. Population and units

- **Population:** modern words in Hindi, Bengali, Assamese and Odia with an attested Sanskrit (OIA) etymon and a stratum label.
- **Unit of analysis:** the item (w, e, L).
- **Unit of independence:** the **etymon cluster**. Items sharing an etymon (doublets, cross-language reflexes) are dependent.
- **Language-level claims** are descriptive only: there are 4 languages from one family.

## 2. Data pipeline

All downloads require approval first.

1. **Source A (silver):** English Wiktionary entries for hi, bn, as, or with etymology templates for inherited from Sanskrit (via MIA where given), learned borrowing from Sanskrit, and semi-learned borrowing from Sanskrit.
   - Category sizes on 2026-10-10: Hindi 1,337 learned / 2,241 inherited; Bengali 1,075 / 1,045; Assamese 149 learned; Odia 269 learned. See `literature/review.md` §7.
   - Extraction route (OPEN): the raw dump, or the wiktextract/kaikki JSON. Licence check required.
2. **Source B (MIA forms):** Pāli and Prakrit forms from Wiktionary etymology chains. If licensed, also CDIAL via Jambu (blocked: no licence file; SOAS copyright).
3. **Normalisation:** one transcription scheme (OPEN: IAST or broad IPA), plus native script retained. Items that cannot be transcribed are excluded **before** splitting and counted.
4. **Deduplication:** identical (w, L) entries with multiple etymologies are flagged. Conflicting labels go to the gold-annotation queue, not training.

## 3. Splits and leakage prevention

- **Split unit: the word family,** not the etymon alone. Families are the union-find closure of: shared OIA etymon (across all languages, so doublets and cross-language reflexes go together); derivative or compound relations between lemmas; and near-duplicates (transliterated normalised edit distance ≤ τ within a language, with a sample of merges checked by experts). See `docs/data_audit_plan.md` §4. τ is OPEN and will be reported.
- **Main split:** word families assigned to train / dev / test by seeded random assignment, stratified by language and label.
- **Calibration pool:** practice-round items are excluded from every split.
- **Held-out-language split:** one Eastern language (OPEN: Bengali, or Assamese plus Odia) removed entirely from θ₂/θ₃ training and from calibration. Used only for a transfer analysis.
- **Leakage rules:**
  - Test-cluster MIA forms never enter θ₁ or θ₂ training.
  - The same etymon never crosses splits.
  - Calibration uses dev only.
  - Hyperparameters are chosen on dev only.
  - Code, configuration and split files are hashed and frozen before test predictions are generated.
- **Circularity control:** test labels come from **expert gold annotation**, not Wiktionary (§4). Silver–gold agreement is reported.
- **LLM leakage:** measured, not prevented (RQ3). LLM results are never confirmatory.

## 4. Gold annotation

- **Sample:** stratified by language × silver label × doublet status, drawn from test clusters only. Size is OPEN (from the simulation in §8).
- **Annotators:** at least two with Indo-Aryan historical training, plus an adjudicator. **None recruited.**
- **Blinding:** annotators see (w, e, L) and may consult the references listed in `docs/data_and_ethics.md`. They do **not** see Wiktionary's label or any model output.
- **Label set and rules:** `docs/annotation_guidelines.md` (draft v0.1). The summary below is superseded by that file if they differ.
- **Label set:**
  - confirmed tadbhava;
  - confirmed tatsama;
  - semi-learned (ardhatatsama);
  - **mixed/complex history** (re-Sanskritised, analogical, via another NIA language);
  - **disputed** (references disagree);
  - wrong etymon;
  - other origin;
  - cannot decide.
- **Pathway justification,** for each confirmed tadbhava:
  - **regular-attested:** a regular development with an attested MIA form;
  - **regular-unattested:** regular, but no MIA form attested;
  - **complex:** needs irregular, analogical or contact explanations.
- **Primary binary test:** confirmed tatsama vs. confirmed tadbhava (regular-attested or regular-unattested). Complex, semi-learned and disputed items are reported separately and never silently dropped.
- **Label audit first:** before modelling results are inspected, a stratified expert audit of silver labels reports silver–gold agreement and the share of complex or disputed items. Wiktionary labels are **candidates**, never gold.
- **Agreement:** Cohen's κ per language before adjudication. Contested items are flagged for sensitivity analysis.

## 5. Systems

| ID | System | Role |
|---|---|---|
| B1 | Normalised edit distance (w, e) after transcription → logistic regression on dev | Surface-similarity baseline |
| B2 | Direct word–etymon feature classifier (character n-grams of the pair and its alignment), re-implementing Cristea et al. 2021's feature design | Existing-approach baseline |
| B3 | Monolingual phonotactic borrowing detector in the style of Miller et al. 2020 (no etymon) | Existing-approach baseline |
| B4 | Direct inherited vs. learned transducer likelihood ratio, **no** intermediate stage (plus a capacity-matched variant) | Competitive baseline; exploratory C2 |
| B6 | Character-level neural pair classifier over the aligned word–etymon pair, with phonological features | Competitive baseline |
| B7 | Stacked classifier on B1–B4 and B6 outputs and features | Strongest no-intermediate baseline |
| P | Proposed: historically constrained latent MIA pathway plus attested MIA forms plus calibration | Proposed |
| P-shuffled | As P, with MIA forms permuted across etymons within length bands | **Confirmatory control (C3)** |
| P-wrong-stage | As P, with a different NIA language's forms as the "intermediate" | Exploratory control |
| P-latent | Latent m, no attested MIA data | Exploratory (structure vs. data) |
| B5 | LLM zero/few-shot (models OPEN; needs API approval) | Exploratory (RQ3) |

The **C1 comparator** is the best of {B1, B2, B3, B4, B6, B7} by dev Brier score, chosen and recorded **before** test evaluation.

## 6. Outcomes and metrics

- **Primary:** Brier score, $\mathrm{BS}=\frac1n\sum_i(\hat p_i-y_i)^2$ with $y_i=1$ for tadbhava, on gold binary items.
- **Paired item difference:** $d_i=\mathrm{BS}_i(\text{P})-\mathrm{BS}_i(\text{comparator})$. Negative values favour P.
- **Secondary:**
  - log loss;
  - AUROC;
  - F1 per class at threshold 0.5;
  - ECE (15 equal-mass bins; reported with a bootstrap CI and the binning caveat);
  - risk–coverage curve and area under it (abstention);
  - edit distance of P's top m to a held-out attested MIA form (descriptive).
- **Diagnostic:** posterior distribution for ardhatatsama items; per-language and doublet-subset metrics.

## 7. Statistical analysis

- **Confirmatory contrasts:** C1 (P vs. the best competitive baseline) and C3 (P vs. P-shuffled). C2 (P vs. B4) is exploratory.
- **Estimate:** mean $d_i$, with 95% CIs from a **cluster bootstrap over etymons** (10,000 resamples).
- **Test:** two-sided **sign-flip permutation test** on per-cluster summed differences (10,000 permutations).
  - Exchangeability assumption: under H₀ (no difference between systems), the sign of each cluster's summed paired difference is symmetric.
  - Clusters are treated as independent of each other. This is plausible for distinct etymons. Shared roots across etymons are a residual dependence, reported as a limitation.
- **Multiplicity:** Holm–Bonferroni over {C1, C3} at α = 0.05.
- **Effect size:** report the mean difference in Brier score with its CI. Significance alone is not interpreted.
- **Why not a mixed-effects model as the primary analysis:**
  - The outcome is a per-item score difference.
  - The cluster bootstrap makes fewer assumptions.
  - With 4 languages, a language random effect is poorly estimated.
  - A mixed model (`d ~ 1 + (1|etymon) + language`) is a sensitivity analysis.
- **Exploratory:** P-latent decomposition; held-out-language transfer; RQ3 contamination splits; ablations; Romance replication. Reported with CIs and **no confirmatory claims**.

## 8. Sample size: simulation, no assumed effect

1. Fit P, B4 and B1–B3 on train; compute per-item Brier differences on **dev** (silver labels).
2. Estimate the variance of cluster-summed differences and the cluster-size distribution.
3. For candidate gold-set sizes, resample dev clusters and compute the expected 95% CI half-width. Compute the probability of excluding 0 under: (a) the observed dev difference; (b) half of it; (c) a quarter of it.
4. Choose the gold-set size from the CI-width target and the annotation budget (OPEN). Report this table in the paper.
   - Dev differences are on silver labels and may be optimistic; this is stated.
   - **No effect size is assumed before step 1.**

## 9. Stopping rule

- One evaluation on the test set after the freeze (§3).
- No re-tuning after test results.
- Gold annotation is completed in full before any test prediction is examined.
- Any re-run after a bug fix is logged as a deviation, and both results are reported.

## 10. Missing data

| Case | Handling |
|---|---|
| Item not transcribable | Excluded before split; counted |
| Gold label other than tadbhava/tatsama | Excluded from the primary test; reported |
| Both likelihoods underflow or are undefined | Assigned the calibrated prior; flagged; sensitivity analysis excludes them |
| LLM output unparseable | Counted as missing for B5. Never imputed as correct or incorrect |

## 11. Sensitivity analyses

- Silver-label test set (larger, noisier).
- Excluding contested gold items.
- Per language.
- Doublet-only subset.
- Native script vs. transcription.
- WFST vs. neural transducers.
- Mixed-effects model.
- Excluding items with the documentation-gap flag.

## 12. Failure criteria (fixed in advance)

| ID | Condition | Consequence |
|---|---|---|
| F1 | C1 CI includes 0 or favours the competitive baseline | No improvement over established methods; **no method claim** |
| F2 | C3 CI includes 0 (P ≈ P-shuffled) | Any gain is capacity or fitting, **not historical evidence** |
| F3 | B1 (surface similarity) Brier is near the ceiling on dev (threshold OPEN). Kanojia et al. 2019 observed that orthographic similarity readily isolates tatsamas | Task too easy as framed. Move the primary test to the hard subset (phonological input, doublets, held-out language) via a documented deviation, **before** test evaluation |
| F3b | Too few confirmed tadbhava items have a justified pathway (threshold from simulation) | The primary test is underpowered; redesign or stop |
| F4 | Gold κ below the threshold (OPEN) | Labels unreliable; no confirmatory test |
| F5 | Data licences unavailable for MIA forms | P cannot be trained as designed; P-latent only |
| F6 | LLM advantage only on recallable items | Reported as a contamination finding, not as LLM capability |
