# Recovering withheld historical stages: a contamination-controlled test of whether AI can find lost linguistic links

_Separate research proposal, 2026-10-10._
- **Status: candidate direction only.** It does not replace or modify `research.md`, its approved RQs, the pilot hold or the Results section.
- No model calls, downloads, data collection or experiments were made, and no result exists.
- Whether this direction replaces the sycophancy study or runs alongside it is the user's decision (§11).

Verification labels:
- **[abstract]**: landing page or abstract fetched.
- **[search]**: search-result summary only; must be read before citing.
- **[prior]**: standard reference known from background knowledge, **not re-verified this session**; check before citing.

No source in this document was read in full in this session.

---

## 0. Summary

The vision is to use multilingual AI to find lost or underdocumented links between languages and to preserve that knowledge. It is scientifically testable only if three problems are solved:

1. **No ground truth for truly lost varieties.** A method that "discovers" an undocumented intermediate language cannot be checked against reality. The only checkable version is to **withhold stages that *are* attested** and ask whether the method recovers them, and whether it abstains where no such stage existed.
2. **Inheritance is easily confused with borrowing and chance.** Indo-Aryan offers an unusually clean internal control: words borrowed directly from Sanskrit (*tatsama*) never passed through a Middle Indo-Aryan stage, unlike inherited words (*tadbhava*).
3. **LLMs have read the etymological literature.** On known data, an LLM "discovering" a Pali or Prakrit form may simply be recalling it. No study found in this audit measures this contamination for historical-linguistic reconstruction. Any LLM contribution claim must survive memorisation probes and synthetic counterfactual language families where the answer cannot have been memorised.

**Primary research question:**

> When an attested intermediate historical stage is withheld, can a method that constrains LLM-generated hypotheses with regular sound correspondences recover that stage's word forms, and correctly abstain for words that never passed through it (learned borrowings, later loans), better than correspondence-only and LLM-only baselines, once LLM memorisation of published etymologies is controlled?

**First case:** recovering Middle Indo-Aryan (MIA) forms from Old Indo-Aryan (OIA) and New Indo-Aryan (NIA) evidence. **Second, unrelated family:** Sinitic, with Middle Chinese as the withheld stage.

---

## 1. What the vision becomes, and what it cannot claim

| Original aim | Testable form here | What it cannot claim |
|---|---|---|
| Find lost links between Sanskrit, Prakrit, Apabhraṃśa and modern languages | Recover *withheld but attested* intermediate forms; rank candidate links with calibrated uncertainty | That an *unattested* variety existed. Such outputs remain hypotheses for experts |
| Find disappeared dialect features | Detect features that require an intermediate stage, e.g., a sound change not derivable directly from OIA to NIA | Discovery of a dialect from model output alone |
| Compare across families | The same withholding design on a second, unrelated family with an attested intermediate stage | A universal method from two families |
| Preserve knowledge | Machine-readable, provenance-linked hypothesis records (CLDF-compatible) for expert and community review | That outputs are linguistic facts |

**Earlier decision revisited.** Decision log 2 rejected the "ghost substrate" idea because unattested substrates have no ground truth. This proposal keeps that judgement. It only makes claims that can be checked against withheld attested data, and treats anything beyond that as ranked hypotheses.

---

## 2. Literature audit: closest prior work

| Work | Venue / status | What it does | Limitation relevant here | Label |
|---|---|---|---|---|
| Meloni et al. 2021, *Ab Antiquo: Neural Proto-language Reconstruction* | NAACL 2021 (peer-reviewed) | Reconstructs Latin from Romance reflexes (8,000+ entries) with an RNN | Reconstructs the *root* from descendants. No borrowing control, no abstention, no LLM contamination analysis | [search] |
| Kim, Chang, Cui, Mortensen 2023, *Transformed Protoform Reconstruction* | ACL 2023 short (peer-reviewed) | Transformer reconstruction. Romance plus Chinese (804 cognate sets, 39 varieties plus **Middle Chinese**). Probes for phylogenetic signal | Middle Chinese is already a reconstruction target, so **recovering an attested earlier stage is not new**. It uses descendants only, not ancestor plus descendants | [search] |
| Lu, Xie, Mortensen 2024, *Semisupervised Neural Proto-Language Reconstruction* | ACL 2024 (peer-review status to verify) | Reconstruction with little labelled data | Same task framing | [search] |
| *Improved Neural Protoform Reconstruction via Reflex Prediction* (Lu, Wang, Mortensen) | To verify | Reranks reconstructions using reflex prediction | Same framing | [search] (third-party summary) |
| Cathcart & Rama 2020, *Disentangling dialects: a neural approach to Indo-Aryan historical phonology and subgrouping* | CoNLL 2020 (peer-reviewed) | LSTM model of OIA→NIA sound change with language embeddings; predicts held-out forms; code released | **Closest Indo-Aryan work.** Models OIA→NIA directly; MIA is not a withheld target; no tatsama control; no LLMs | [search] |
| Cathcart 2020, *A probabilistic assessment of the Indo-Aryan Inner–Outer Hypothesis* | J. Historical Linguistics 10(1) (peer-reviewed) | Bayesian mixed-membership model on automatically extracted OIA→NIA sound changes; partial support for the hypothesis | Shows that computational testing of *contested* Indo-Aryan subgrouping is established. A new contribution must differ in task, not just region | [search] |
| Arora, Farris, Basu, Kolichala 2023, *Jambu* | SIGMORPHON 2023 workshop (peer-reviewed) | About 287k lemmata, 602 lects, about 23k cognate sets, from CDIAL (Turner) and DEDR (Burrow & Emeneau) plus other sources; reflex-prediction models | **The main candidate dataset.** Licence and reuse terms unverified (CDIAL material used with project approval for academic purposes) | [search] |
| Farris & Arora 2021, *For the Purpose of Curry: A UD Treebank for Ashokan Prakrit* | Workshop (LChange 2021, to verify) | First annotated treebank of Ashokan Prakrit | Syntax resource for one MIA variety; small | [search] |
| List et al. 2022, *SIGTYP 2022 Shared Task on the Prediction of Cognate Reflexes* | SIGTYP 2022 workshop | Fill in missing reflexes across families; best system an image-restoration CNN | Reflex prediction is solved reasonably well **when sound change is regular**. Our task must add something beyond it | [search] |
| Rama, List, Wahle, Jäger 2018, *Are automatic methods for cognate detection good enough for phylogenetic reconstruction?* | NAACL 2018 (peer-reviewed) | Automatic cognates give phylogenies close to, but worse than, expert cognates | Automatic cognate detection is a baseline, not a contribution | [search] |
| List et al. 2022, *Lexibank* | Scientific Data (peer-reviewed) | Standardised CLDF wordlists (2,000+ varieties); Lexibank 2 (Blum et al. 2025) reports 3,100+ | Infrastructure and data source. Expert cognate sets for evaluation | [search] |
| Forkel & List 2022, *Automated identification of borrowings in multilingual wordlists*; Miller et al. 2020 (monolingual borrowing detection); Miller & List 2023 (dominant-language borrowings); Wientzek 2025 (arXiv 2512.01713, self-supervised) | Open Research Europe; PLOS ONE; arXiv preprints | Computational borrowing detection | Borrowing detection exists. None found uses learned borrowing from an *ancestor* language (tatsama) as a control | [search] |
| Sousa Silva & Ahmadi, *Are Language Models Borrowing-Blind?* (arXiv 2510.26254; LREC 2026 per search) | LREC 2026 (to verify) | LLMs fail to separate loanwords from native words across 10 languages | Direct evidence that LLM-only borrowing judgements are unreliable | [search] |
| Liang, Abo Mokh, Alhafni, *When Similar Means Different: Evaluating LLMs on Arabic–Hebrew Cognates* (arXiv 2606.13218) | Accepted to EMNLP 2026 per arXiv comment (preprint) | 1,858 pairs; LLMs rely on surface similarity, worse on false friends, variable on loanwords | LLMs confuse resemblance with cognacy, the core confound here | [abstract] |
| Liu, Shi, Zhou, Zhang 2026, *Would LLMs be Good Historical Linguists and Chinese Dialect Learners?* | ACL 2026 long (peer-reviewed) | Middle Chinese → 12 dialects: sound-law induction and dialect IPA; LoRA + GRPO beat strong LLM baselines | LLMs plus historical stage data for Sinitic is **already active**. They go from ancestor to descendant; withholding and abstention are not tested | [abstract] |
| Naik et al. 2024, *Can LLMs Code Like a Linguist? Sound law induction* (arXiv 2406.12725); PBEBench (arXiv 2505.23126) | Preprints (venue to verify) | LLMs induce sound laws as programs; synthetic data | Synthetic sound-change data is an established evaluation tool. Our synthetic control builds on it, not a novelty claim | [search] |
| Temesgen et al. 2025, cognate detection and reconstruction for Ge'ez, Tigrinya, Amharic | COLING 2025 (peer-reviewed) | GPT-4o few-shot proto-forms plus Seq2Seq | LLM reconstruction already tried. Contamination not reported in what was seen | [search] |
| Beinborn & Choenni 2020, *Semantic Drift in Multilingual Representations* (CL); Rama et al. 2020, *Probing Multilingual BERT for Genetic and Typological Signals* (COLING) | Peer-reviewed | Language trees from multilingual model representations resemble expert trees | **Embedding similarity recovers known genealogy only approximately**, and cannot by itself separate inheritance, contact and shared training data | [search] |
| Luo, Cao, Barzilay 2019 (neural decipherment, Ugaritic and Linear B); Assael et al. 2022 *Ithaca* (Nature, restoring ancient Greek inscriptions) | Peer-reviewed | AI for lost scripts and damaged texts | Adjacent ("lost" text); different task | [prior] |
| Mainzinger & Brixey 2026 *IndigiEval*; Vasselli et al. 2026 | AmericasNLP 2026; EACL 2026 short | LLMs weak on Indigenous languages of the Americas | Limits any Indigenous-American arm (§6) | [abstract] |

**Searched and not found**, which is not the same as nonexistent:
- an evaluation that conditions on *both* ancestor and descendant forms to recover a withheld intermediate stage, with an abstention decision for words that bypassed it;
- a study measuring LLM memorisation of published etymologies as a confound in reconstruction.

Coverage was 14 web searches on 2026-10-10. Not searched: Google Scholar, Journal of Historical Linguistics and Diachronica back-issues, Indian-language venues, the "open problems" papers by List (2024, cited in a search summary but not retrieved), and forward citations of Cathcart & Rama.

---

## 3. The gap, stated precisely

What existing systems can do:
- predict reflexes when sound change is regular (SIGTYP 2022);
- reconstruct an ancestor, including Middle Chinese and Latin, from descendants (Meloni; Kim et al.);
- model OIA→NIA change and test subgrouping (Cathcart & Rama; Cathcart);
- detect some borrowings (Forkel & List);
- recover approximate genealogy from embeddings (Beinborn & Choenni; Rama et al. 2020).

**Where the methodological limitation lies:**
1. **Task.** Reconstruction is framed as descendants → root. The "missing link" question is about intermediate stages, bracketed by an ancestor and descendants. It also needs a decision about *whether* a word passed through that stage at all. That second part is untested in what was found.
2. **Confounds evaluated separately.** Borrowing detection and reconstruction are evaluated apart. No reconstruction benchmark found includes a control where a plausible reconstruction is *historically wrong* because the word was borrowed later from the ancestor language.
3. **Contamination.** LLM-assisted work (Temesgen et al.; Liu et al. 2026) reports accuracy against published forms that LLMs may have memorised. Without a memorisation control, "the LLM found the link" is not distinguishable from "the LLM remembered the dictionary".

The gap is the **conjunction** of (1)–(3). Each piece alone is partly covered. Whether the conjunction has been done elsewhere is **not established** (§9).

---

## 4. Methodological contribution: more than "using an LLM"

### Task: withheld-stage recovery with abstention (WSR)

For a cognate set with an attested ancestor form (e.g., OIA), descendant forms (NIA) and an attested intermediate form (MIA), the intermediate form is withheld. The system outputs:
1. a decision: did this word pass through the intermediate stage (inherited), or did it bypass it (learned borrowing from the ancestor, or a later loan)?
2. if inherited, a ranked set of candidate intermediate forms, each with a probability;
3. an **evidence trace**: the correspondences and data entries that support each candidate, checkable automatically against the input data.

### Method: correspondence-constrained hypothesis generation

- **Proposal step.** An LLM proposes candidates (forms and decisions).
- **Verification step.** A correspondence model learned from *training* cognate sets only scores each candidate. This is a reflex-prediction model in the style of Cathcart & Rama or Cognate Transformer, trained to predict NIA from MIA and MIA from OIA.
- **Discarding.** Candidates that violate learned regular correspondences in either direction are discarded.
- **Calibration.** Final scores are calibrated on a held-out development split.
- **Why the LLM matters:** it supplies hypotheses beyond what the correspondence model can generate (irregular but documented changes, analogical forms). The correspondence model supplies the regularity check that LLMs lack (Liang et al.; Sousa Silva & Ahmadi).

Whether this combination beats either part alone is the empirical question.

### Controls built into the benchmark

- **Learned-borrowing control (Indo-Aryan).**
  - *Tatsama* words, borrowed directly from Sanskrit into NIA, have no MIA stage. The correct output is "bypassed".
  - *Tadbhava* words are inherited through MIA.
  - *Ardhatatsama* forms (partly adapted learned words) are a hard middle class.
  - Gold labels need expert annotation (§5). The distinction itself is standard in Indo-Aryan grammar [prior: Masica 1991; Chatterji 1926 for Bengali]. It must be verified against those sources before use.
- **Later-loan control.** Persian, Arabic and English loans in NIA also have no MIA stage. The source of labelled loans is an `OPEN` item.
- **Chance-resemblance control.** Pair NIA words with semantically matched but non-cognate OIA words of similar shape. A system that posits an inheritance path is wrong.
- **Contamination controls:**
  1. **Recall probe.** Ask the LLM for the MIA form given *only* the OIA headword and gloss, with no NIA evidence. Items it answers correctly are "recallable". Report every metric separately for recallable and non-recallable items.
  2. **Frequency split.** Compare common vocabulary with rare entries.
  3. **Synthetic counterfactual families.** Apply documented sound-change *types* to real OIA forms, with changed rule order and conditioning, to create MIA-like and NIA-like layers whose truth is known and cannot have been memorised. This builds on established synthetic sound-change evaluation (Naik et al.; PBEBench).
- **Representation controls.** The same items in IPA, IAST transliteration and native script, to test robustness to script and tokenization.

### Evidence graph

Every output is stored as a record linking candidate → supporting correspondences → source entries (dataset, entry ID) → model and prompt version. Records are CLDF-compatible where possible. This is what later makes outputs reviewable by experts and communities.

---

## 5. First experiment (feasible; nothing run)

**Data (subject to licence checks, §6):** Jambu's Indo-Aryan portion (CDIAL-derived), restricted to cognate sets with an OIA headword, at least one attested MIA form (Pāli and/or Prakrit, as labelled in the source), and at least two NIA reflexes.
- The number of qualifying sets is unknown until the data are inspected.
- **Splits by cognate set**, never by word, so no set appears in both training and test.
- A further held-out split by **NIA branch** (e.g., train without Eastern NIA reflexes, test on Bengali/Assamese/Odia) tests generalisation to an unseen branch.

**Systems:**
- **B0 (trivial):** copy the OIA form, or apply the most frequent correspondence per segment.
- **B1:** neural reflex prediction OIA→MIA trained on training sets; architecture as in Cathcart & Rama or Cognate Transformer.
- **B2:** the same, conditioned on OIA plus NIA (bracketed).
- **L0:** LLM only, few-shot.
- **L1:** LLM proposals verified by B2's correspondence model (the proposed method).
- **Ablation:** L1 without the abstention step.

**Gold labels needing experts:**
- tatsama, tadbhava and ardhatatsama labels for the NIA words in the test split;
- a sample review of whether source MIA forms are correctly aligned.

Two independent annotators with Indo-Aryan historical training, plus adjudication. Inter-annotator agreement is reported, and **no gold labels are invented**.

**Metrics:**
- **Form recovery:**
  - exact match;
  - mean normalised edit distance;
  - phoneme feature error rate (CLTS features);
  - top-k accuracy over ranked candidates.
- **Inheritance vs. bypass:** F1 per class (tadbhava / tatsama / ardhatatsama / later loan), plus false "inherited" decisions on chance-resemblance pairs.
- **Calibration and ranking:** Brier score, expected calibration error, AUROC for the inherited/bypass decision; mean reciprocal rank for candidate forms.
- **Evidence traceability:** share of outputs whose cited correspondences and entries exist in the input data and actually support the candidate. Checked automatically, with an expert spot-check.
- **Contamination gap:** every metric on recallable vs. non-recallable items, and on real vs. synthetic families.
- **Robustness:** metric differences across IPA, IAST and native script.
- **Held-out branch:** metrics on the unseen NIA branch.

**Statistical treatment:** item-cluster bootstrap CIs over cognate sets; paired comparisons between systems on the same items. Comparison families are fixed before test data are opened. **No sample size, effect size or expected result is stated here.**

**Second family (stage 3):** Sinitic.
- Old Chinese is reconstructed, not attested, so here the ancestor side is weaker: the stage is recovered from descendants plus *rime-table* categories.
- This is a genuinely different evidence structure.
- Candidate data: the Hóu (2004)-derived set used by Kim et al.; the Middle Chinese plus 12-dialect set of Liu et al. 2026 (release unverified).
- Learned literary vs. colloquial readings (文白异读) are a possible analogue of the tatsama control. Expert verification is needed.

---

## 6. Data, licensing, expert review and ethics

**Licensing:**
- **CDIAL (Turner):** the DSAL edition states copyright and requires SOAS permission for storage or reproduction [search]. **This is a blocker until resolved.**
- **Jambu:** licence and redistribution terms are unverified; the paper says CDIAL material was used with project approval for academic purposes [search]. Contact the authors.
- **Lexibank/CLDF datasets:** licences vary per dataset; check each.
- **Sinitic datasets:** licences unverified.

**Historical-stage terminology** must be verified against authoritative sources before it is written into the benchmark: Masica 1991, *The Indo-Aryan Languages*; Cardona & Jain (eds.) 2003, *The Indo-Aryan Languages*; Chatterji 1926 for Bengali; Turner's CDIAL [all prior]. Specific cautions:
- Classical Sanskrit is a standardised literary language. Modern NIA languages are generally described as descending from Middle Indo-Aryan vernaculars, not from Classical Sanskrit as written. "OIA" in the benchmark means the headword layer of the source dictionary, not a claim of direct parentage.
- "Prakrit" covers several literary varieties (e.g., Māhārāṣṭrī, Śaurasenī, Māgadhī). Literary Prakrits and Apabhraṃśa are stylised and are not necessarily the spoken ancestors of particular modern languages. The benchmark labels forms by attested variety and does not map them onto a single linear chain.
- The stages are unequally documented. Apabhraṃśa in particular has no large, finished digital corpus in what was found.

**Expert review:**
- Indo-Aryan historical linguists for gold labels and adjudication.
- Sinologists for stage 3.
- **None recruited.**

**Ethics:**
- The Indo-Aryan and Sinitic cases use published scholarly data on major languages; the main ethical issues are licensing and attribution.
- Any extension to endangered or Indigenous languages needs community involvement, consent, data sovereignty agreements and benefit to the communities. It is **not proposed** in stages 1–3. IndigiEval and Vasselli et al. also report weak model competence for many Indigenous languages of the Americas [abstract].
- Outputs about underdocumented varieties are framed as hypotheses for expert and community review, never as findings.

---

## 7. Risks, confounders and explicit failure criteria

**Risks:**
- **Licensing** blocks CDIAL-derived data. Mitigation: obtain permission, or fall back to openly licensed Lexibank data.
- **Contamination is pervasive.** Mitigation: it is measured, not assumed away. A large contamination gap is itself a result.
- **Gold-label scarcity** for tatsama/tadbhava. Mitigation: annotate a small, high-quality test set rather than a large noisy one.
- **Source-data inconsistency.** CDIAL transcriptions are heterogeneous and MIA attestations are uneven across words. Mitigation: per-variety reporting and an expert alignment audit.
- **Regularity makes the task easy for B1/B2,** so the LLM adds nothing. This would be informative (see failure criteria).
- **Scope creep** from the original multi-family vision. Mitigation: no family beyond stage 3 until stages 1–3 pass.

**Confounders tracked:**
- surface resemblance;
- semantic association learned by LLMs;
- script and tokenization;
- word frequency;
- dictionary coverage per language;
- recallability.

**Failure criteria** (decided before any test data are opened):
1. **F1:** if L1 does not beat B2 on non-recallable items or synthetic families (CIs overlapping or below), the claim that LLMs add hypothesis value beyond correspondence models is **not supported**.
2. **F2:** if L0/L1 gains appear only on recallable items, the result is that LLM "recovery" is mainly recall. That is a meaningful negative result and the paper becomes a contamination study.
3. **F3:** if no system separates tatsama from tadbhava above a frequency-matched baseline, the abstention component fails.
4. **F4:** if expert agreement on gold labels is too low to evaluate against, the label scheme must be redesigned before any claim. The threshold is `OPEN`.
5. **F5:** if licences cannot be obtained, stage 1 cannot proceed on CDIAL-derived data.

A meaningful negative result looks like this: correspondence models recover withheld MIA forms well; LLMs add nothing on uncontaminated items; and LLM inheritance judgements are fooled by learned borrowings. That would be useful evidence against using LLMs as discovery tools in historical linguistics.

---

## 8. Feasibility for a strong computational-linguistics venue

**In favour:**
- A clear task.
- An unusually clean linguistic control (tatsama).
- A timely, checkable concern: LLM contamination in scientific discovery claims.
- Existing open baselines (Cathcart & Rama code; reconstruction code from Kim et al.).
- Two unrelated families.

**Against:**
- Licensing is unresolved.
- Expert labels are required.
- Neural reconstruction is a well-trodden area, so reviewers will ask what is new beyond Kim et al. and Cathcart & Rama.
- Strong venues will expect the contamination analysis to be rigorous.

**Venue fit,** only assessable after results:
- ACL/EMNLP main if stages 1–2 give a clear positive or a clear contamination finding.
- Findings, or SIGTYP/SIGMORPHON/LChange workshops, for a single-family study.
- No venue outcome is predicted.

---

## 9. Novelty assessment (no numerical rating)

**Evidence for novelty:**
- None of the works found evaluates bracketed (ancestor plus descendants) recovery of a withheld intermediate stage together with an inheritance-vs-bypass decision.
- None uses learned borrowing from the ancestor language as a negative control.
- None measures LLM memorisation of etymologies as a confound.

**Evidence against:**
- Recovering attested earlier stages (Latin, Middle Chinese) is established.
- Indo-Aryan sound-change modelling and subgrouping are established (Cathcart & Rama; Cathcart).
- LLMs on Middle Chinese and dialects (Liu et al. 2026) and on cognates and loanwords (Liang et al.; Sousa Silva & Ahmadi) are active areas.
- Synthetic sound-change evaluation exists.

**Unresolved:**
1. Has bracketed intermediate-stage recovery been done under another name (e.g., "ancestral state reconstruction of forms", "intermediate node reconstruction")?
2. Has contamination been measured in any reconstruction or etymology study (full text of Temesgen et al., Liu et al. 2026 and Kim et al. not read)?
3. Has the tatsama/tadbhava distinction been used computationally (e.g., in Jambu-based or Bengali NLP work)?
4. What do forward citations of Cathcart & Rama 2020 and Jambu contain?
5. List's "open problems in computational historical linguistics" paper (not retrieved) may already name this gap.

**Current judgement:** the conjunction looks like a defensible, specific contribution. Its novelty is **not established** until items 1–5 are checked.

---

## 10. Staged plan

| Stage | What | Needs | Can be done now? |
|---|---|---|---|
| 0. Closure | Resolve §9 items 1–5; verify the historical sources in §6; confirm licences (CDIAL/SOAS, Jambu, Sinitic data) | Web/library access; emails to dataset authors | **Yes** (no data, no models) |
| 1. Data audit | Inspect Jambu offline: count qualifying cognate sets, MIA coverage per variety, transcription consistency | Dataset download (approval) and licence | After stage 0 |
| 2. Non-LLM baselines | B0–B2 on cognate-set splits and held-out branch; synthetic families | Local compute only | After stage 1 |
| 3. Gold labels | Tatsama, tadbhava, ardhatatsama and loan labels on the test split; alignment audit | **Two expert annotators** plus adjudicator | When experts are recruited |
| 4. LLM conditions | L0, L1, recall probes, contamination analysis | **Model/API calls (approval)**; budget | After stages 2–3 |
| 5. Second family | Sinitic, with Middle Chinese withheld | Data licences; Sinologist reviewer | After stage 4 |
| 6. Preservation pilot | Provenance-linked hypothesis records for expert and community review; any underdocumented-variety work | **Community partnership, consent, data-sovereignty agreement** | Not before stages 1–5 succeed |

**Can be established now:** the literature position, licences, the source-verified definition of stages, and the benchmark specification.

**Needs data, experts or communities:** everything from stage 1 onward.

---

## 11. Decisions for the user

1. Is this a **replacement** for the sycophancy study, a **parallel** project, or a **later** project? The two share almost no data or code; only the parser and gating ideas carry over loosely.
2. Approve stage 0, which needs no data download, models or experts.
3. Is there access to Indo-Aryan historical linguists, through the user's network or institution?
4. Are you willing to contact SOAS (CDIAL) and the Jambu authors about licensing?
