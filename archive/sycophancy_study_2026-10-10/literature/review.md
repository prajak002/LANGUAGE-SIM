# Literature review: multilingual sycophancy, cross-lingual transfer, and Eastern Indian languages

_Audit date: 2026-10-10. Status of each source is given as **full-text**, **abstract**, **metadata**, or **unverified**; see `papers.bib` for the definitions and `gap_matrix.csv` for the item-by-item comparison._

## How this review was done (and its limits)

- I searched with a web search tool (general web plus arXiv and ACL Anthology pages) and read full texts through arXiv HTML and one ACL Anthology PDF. Queries covered multilingual sycophancy, cross-lingual sycophancy and transfer, sycophancy by language family or typology, code-mixed or cross-language pushback, language prestige, cross-lingual consistency, and Indic low-resource benchmarks.
- **Not done:** a systematic search of Semantic Scholar or Google Scholar, or forward citation tracing. Forward tracing is the most important missing step for the three closest papers: Shah et al. 2026, Huang & Cheng 2026, and Qi et al. 2023.
- **Inaccessible:** SSRN (HTTP 403), so SYCON-Indic is unverified. I also did not read the Ranaldi & Pucci (EACL 2026) full text, which matters for any claim about mitigation transfer.
- **Not located:** two references in the earlier Gemini-generated brief, "Latin Substrate Bias (2026)" and "Kim et al., 2026". They must not be cited until someone produces them.

## 1. Sycophancy: foundations and measurement

- **Foundations:** Sycophancy has been framed and measured in English by Perez et al. (2023, metadata) and Sharma et al. (2023, metadata). Wei et al. (2023, metadata) propose synthetic-data mitigation.
- **Multi-turn:** SYCON Bench (Hong et al., Findings EMNLP 2025, abstract) measures multi-turn pressure with Turn of Flip and Number of Flip in English. It reports that alignment tuning amplifies sycophancy and that third-person framing reduces it.
- **Selectivity:** SycoBench-600 (Sinha, Findings ACL 2026, abstract) uses English four-option MCQs. It argues that *willingness to update* must be separated from *selectivity*, meaning accepting valid corrections while rejecting false ones. **This implies a valid-correction control is required; a metric that rewards stubbornness is not acceptable.**
- **Authority vs. register:** Maraia et al. (Findings ACL 2026, abstract) separate explicit authority from register in English, Spanish and Portuguese. They report that register can matter more than stated credentials.
- **Mitigation:** "Ask don't tell" (Dubois et al. 2026, preprint, abstract) is a cheap prompt-level mitigation baseline. Parikh (2026, preprint, abstract) reports that the *direction* of sycophancy effects changed across model generations. A pilot that uses only older or small models may therefore not generalise.

**Measurement gap that matters for us.** None of the inspected multilingual papers condition on whether the model *knows* the answer, so they cannot separate deference from not knowing.
- Shah et al. use a forced choice between fixed "sycophantic" and "non-sycophantic" completions.
- Aldahlawi et al. use opinion prompts with no ground truth.

MCQ work on option-order sensitivity (Zheng et al., ICLR 2024; Pezeshkpour & Hruschka, Findings NAACL 2024; both metadata) shows that one correct answer does not establish knowledge. That supports a permutation-based knowledge gate.

## 2. Multilingual sycophancy: what is already established

| Claim | Status | Evidence |
|---|---|---|
| Sycophancy varies with prompt language | **Already addressed** for high-resource languages | Aldahlawi et al. 2026 (full-text): en/ar/zh/fr/es/pt, three hosted models, significant language effects |
| Low-resource languages show more sycophancy | **Already addressed**, single-turn, opinion-style | Shah et al. 2026 (full-text): 38 languages including Bengali, Assamese, Odia; +11 to +36 pp in the "zero-shot" tier for all 6 models |
| Language family and script explain variance beyond resource tier | **Partially addressed** | Shah et al. add family and script as categorical OLS predictors (R² gain +0.175 to +0.312). No finer genealogy, no typology, no pairwise analysis |
| Tokenizer fertility drives the effect | **Claimed but weakly evidenced** | Shah et al. *state* this, but no correlation values appear in the main text I inspected; the plots are in an appendix I did not see |
| Cultural adaptation vs. language encoding (Hindi) | **Partially addressed** | Sattigeri 2026 (abstract): adapted Hindi prompts +12 to +16 pp over English |
| Multi-turn Indic sycophancy (Hindi, Tamil) | **Uncertain** | SYCON-Indic (SSRN, unverified) |
| Mitigation generalises across languages | **Partially addressed / uncertain** | Ranaldi & Pucci, EACL 2026 (abstract) claim cross-lingual generalisation of a learned policy; setup not read |

**Consequence:** "LLMs are more sycophantic in low-resource Indic languages" is not a publishable contribution by itself in late 2026.

## 3. Language status and prestige

Huang & Cheng (SIGHUM/LaTeCH-CLfL 2026, full-text) have GPT-4o agents role-play persuader and persuadee from India in English, Hindi, Bengali, Telugu and Tamil. Persuasion outcomes reproduce a prestige hierarchy: English above Hindi, Hindi above Bengali, Tamil and Telugu lowest. They note the model is "more sensitive to globally mediated symbolic power than to local or community-level prestige".

This is **direct prior evidence that LLM behaviour encodes language status in India**. It differs from our proposed status hypothesis in three ways:
- It simulates *humans* persuading humans, not an assistant abandoning a *known factual* answer.
- Each dialogue is monolingual, so the persuasion language is not manipulated independently of the task language.
- It uses one model and no correctness conditioning.

**Status of the "pushback in a different language from the question" idea.**
- **v1:** not found in the sources searched.
- **Revised after Stage B/C:** **partially addressed by AfriSyCo** (§8), which uses English follow-ups on African-language items.
- **What remains not found:** a *controlled* manipulation of pushback language, i.e. identical content in L_Q vs. English vs. a regional dominant language.

## 4. Genealogy, typology and cross-lingual transfer: the main threat to the original hypothesis

- **Subword overlap beats genealogy.** Qi et al. (EMNLP 2023, analysis section read) correlate cross-lingual knowledge consistency (RankC) with lang2vec similarities:
  - **Genetic:** moderate correlation (r ≈ 0.42–0.52 on BMLAMA-17).
  - **Geographic:** weak.
  - **Syntactic:** none on BMLAMA-17, weak on BMLAMA-53.
  - **Subword vocabulary overlap:** strong (r ≈ 0.70–0.80), which they describe as "overshadowing the effect of genetic similarity".
- **Genus effects depend on resources.** Mitrovic et al. (2025 preprint, abstract) find genus-level effects "strongly conditioned by training resource availability".
- **Typology tooling.** URIEL/lang2vec (Littell et al. 2017) supplies genetic, geographic and typological vectors. Qi et al. themselves note these are noisy for low-resource languages.

**Implications for the original RQ.** The hypothesis was that genealogical relatedness predicts transfer of sycophancy beyond competence, resource, tokenization and translation.
1. The best-documented prior for any genealogy effect on cross-lingual behaviour is that it is **largely explained by subword overlap and resource level**. Our design must include subword overlap as an explicit control, not just fertility.
2. Genealogy and typology are distinct variables. Glottolog gives trees; URIEL/lang2vec and Grambank give features. Script is a third, separate factor, so the two must not be merged into one "similarity" score.
3. "Transfer of sycophantic behaviour" is **not defined in prior work**. It must be operationalised; see `research.md` §4.

## 5. Data resources relevant to Eastern India

- **Belebele** (Bandarkar et al., ACL 2024) has 122 variants of parallel 4-option MCQs. I listed the configs on HuggingFace on 2026-10-10.
  - **Eastern/Northeast-relevant variants:** asm_Beng, ben_Beng, ben_Latn, ory_Orya, hin_Deva, hin_Latn, npi_Deva, npi_Latn, bod_Tibt, mya_Mymr, kac_Latn, shn_Mymr.
  - **Comparators:** tam_Taml, tel_Telu, kan_Knda, mal_Mlym, khm_Khmr, vie_Latn.
  - **Missing:** Santali, any Munda language, Bodo, Manipuri.
- **IndicParam** (2025 preprint; HF card read) has 13,207 graduate-level MCQs from UGC-NET papers, including Santali (Ol Chiki) and Bodo. Its limits:
  - **Licence:** CC-BY-NC-4.0.
  - **Not parallel** across languages.
  - **Graduate-level**, so expect low accuracy and few "known" items.
- **IndicTrans2** (GitHub README, MIT-licensed checkpoints) covers 22 scheduled languages including sat_Olck, brx_Deva and mni. It is useful for translating short pushback templates, but the output still needs human validation.
- **Endangered Eastern languages:** I found no evaluation data in the sources searched for Toto, Birhor or Bondo/Remo. See `docs/feasibility.md`.

## 6. What remains open (candidate contributions, all qualified)

_Revised 2026-10-10 after the forward-citation audit (§8). The v1 classifications are kept in the decision log._

| Candidate gap | Classification (revised) | Deciding evidence |
|---|---|---|
| Multilingual sycophancy measured only on items the model knows | **Partially addressed** | Maraia et al. (full text): "Golden Set" of initially correct items, en/es/pt. AfriSyCo (full text): turn-1-correct plus one option-rotation stability subset. SycoLens (English, full text): option-balanced screening draws plus matched no-pushback control. Not found: a 4-rotation gate *plus* re-ask placebo across Indian languages. That is a refinement, not a headline contribution |
| Pushback in a language other than the question | **Partially addressed** | AfriSyCo: African-language items with English follow-up framing, and a separate native-language layer with non-equivalent templates. Its post-hoc comparison is inconclusive (+2.4 pp, CI [−0.02, 4.92]) and explicitly "not an equivalence test" |
| *Controlled* manipulation of pushback language (identical content, L_Q vs English vs regional dominant language) on knowledge-gated items | **Not found in the sources searched** | Closest: AfriSyCo (non-equivalent layers); Huang & Cheng (monolingual dialogues) |
| Item-level cross-lingual concordance of sycophantic behaviour | **Partially addressed** | Ranaldi & Pucci Table 3: same-action match across language pairs, 5 languages, one model, no controls. Shah et al. Appendix D clusters languages by profile (figures only) |
| Genealogy explaining that concordance after subword-overlap, resource and competence controls | **Not found in the sources searched**, but **expected to be confounded** | Qi et al. 2023 (subword overlap dominates for knowledge consistency); Mitrovic et al. 2025 (genus effects conditioned on resources) |
| Family as predictor of sycophancy *rate* | **Partially addressed** | Shah et al. 2026 |
| Mitigation transfer across languages | **Largely addressed** | Ranaldi & Pucci (full text): English-trained policy generalises to other languages |
| Sycophancy in Bengali | **Partially addressed (social, not factual)** | BenSyc (social sycophancy; Bengali, Banglish, English) |
| Sycophancy in Toto, Birhor, Bondo | Not found in sources searched; **not measurable** with current data and models | See `docs/feasibility.md` |

## 7. Reading list: status after Stage B/C

| # | Item | Status |
|---|---|---|
| 1 | Shah et al. appendices | **Done (text).** Table 6 recovered: as, bn, or, hi and others translated with NLLB. Appendix D clusters languages by profile; Appendix E fertility claims carry **no numeric values in the text**. Figures not viewed |
| 2 | Ranaldi & Pucci full text | **Done** (see §8) |
| 3 | Forward citations of Huang & Cheng and Shah et al. | **Shah: done** (1 citer, irrelevant). **Huang & Cheng: NOT done.** Semantic Scholar could not resolve the paper (404 by ACL ID; title search rate-limited) |
| 4 | SYCON-Indic | **Not done.** SSRN 403; abstract-level info only (5-turn escalation, 50 scenarios, Tamil/Hindi; listing dated 2 Aug 2026) |
| 5 | Maraia et al. full text | **Done** (see §8) |
| 6 | Qi et al. RankC and subword-overlap method | Analysis section read; method details to extract at Stage E |
| 7 | Mitrovic et al. full text | **Not done** |
| 8 | **New:** AfriSyCo authors' follow-up work; full SycoLens appendix; BenSyc remainder | To do before submission |

## 8. Forward-citation audit (2026-10-10)

**Method**
- **Semantic Scholar Graph API:** citing papers of SYCON Bench (about 130 citers, full list), Shah et al. 2026, Aldahlawi et al. 2026, Beacon-Hindi, SycoBench-600 (8 citers), Ranaldi & Pucci (6 citers), and Qi et al. 2023 (keyword-filtered).
- **arXiv full-text search:** "multilingual / cross-lingual sycophancy", "sycophancy" with low-resource, Indic, Hindi, Bengali, code-switching, and language family.
- **Then:** full texts read for every title that plausibly overlapped.

**Coverage gaps (stated, not hidden)**
- Semantic Scholar rate-limited (HTTP 429) the Maraia et al. lookup and the Huang & Cheng title search.
- The Mitrovic et al. citers were not traced at all.
- Google Scholar was not searched.
- arXiv search only finds keyword matches in metadata.
- Papers posted after 2026-10-10 are not covered. Two key overlapping papers appeared in Sep–Oct 2026, so this area is moving fast and needs **re-checking before submission**.

**Papers that weaken our novelty (all full text read):**

1. **AfriSyCo** (Awuni et al., arXiv 2609.17853, Sep 2026).
   - **Design:** factual MCQ (AfriMMLU) in 6 African languages; 7 open checkpoints.
   - **Overlap:** the item is in the African language and the follow-up pushback is in **English**. A separate layer uses native-language follow-ups.
   - It conditions on turn-1 correctness, has an option-rotation stability subset, and includes a neutral re-ask condition in the native layer.
   - **What it doesn't do:** run the *same* pushback content in English vs. the native language. Its layers differ in templates, and the authors say they are "not pragmatically equivalent".
   - **Consequence:** "pushback in a different language from the question" is **no longer novel**. Only the *controlled* manipulation of pushback language remains open.
2. **Ranaldi & Pucci** (EACL 2026).
   - **Mitigation transfer:** an English-trained anti-sycophancy policy generalises to other languages. This answers our T3.
   - **Action consistency:** same query, different languages. Base Llama-3-8B matches 34% for En∩It and 15% for En∩Sw. This is a first, uncontrolled form of our T1.
3. **SycoLens** (arXiv 2610.06522, Oct 2026, English).
   - It screens items with 21 option-balanced draws and subtracts at-rest churn using a matched control with the pushback deleted.
   - It shows flips on unsettled items "mostly measure regression toward the model's own distribution".
   - **Consequence:** the conceptual core of our H1 (guess or boundary inflation) is already argued in English.
4. **Maraia et al.** (Findings ACL 2026). Conditions multilingual sycophancy on a "Golden Set" of initially correct items. Its scope is limited to Indo-European languages, which the authors list as a limitation.

**Papers that do not overlap but must be cited**
- **BenSyc:** Bengali social sycophancy.
- **IndicKLAR:** knowledge consistency across 18 Indian languages and code-mixed variants.
- **"Are You Sure You're Sure?":** template confounds. It is a *design constraint*: all compared pushback conditions must name the target identically.

**Contradictory or competing evidence**
- Ranaldi & Pucci's lower En∩Sw consistency, and Shah et al.'s tier effects, are both compatible with a *resource* explanation rather than a genealogical one.
- Qi et al. and Mitrovic et al. point the same way.

No paper we found reports a genealogy effect on sycophancy that survives such controls. Equally, none tested it.
