# Cross-family extension: feasibility audit

_Date: 2026-10-10. Status: **exploratory proposal only**._

- No model calls, downloads or experiments were made.
- `research.md` (RQ1, its confirmatory contrasts, the pilot hold and Results) is **unchanged**.
- Nothing here is a finding about model behaviour.

Verification labels:
- **[full-text]**: read in full or the relevant section read.
- **[abstract]**: abstract or landing page only.
- **[search]**: search-result summary only, not opened. Treat as unverified.
- **[data]**: read directly from a database or dataset listing (Glottolog, WALS, Hugging Face).

---

## 0. Bottom line

1. **Adding Mandarin, Japanese and Korean is not novel by itself.**
   - Shah et al. 2026 [full-text, Table 6] already evaluate zh, ja and ko, plus 35 other languages. They use family and script as regressors, with machine-translated prompts (TowerInstruct or Gemmax for these three).
   - Aldahlawi et al. 2026 [full-text] include Chinese.
   - Ranaldi & Pucci 2026 [full-text] include Chinese and Swahili.
2. **Adding African languages is not novel by itself either.** AfriSyCo [full-text] already tests Hausa, Igbo, Kinyarwanda, Swahili, Twi and Yoruba, with English follow-up pushback.
3. **What the extension could add is identification, not coverage:**
   - It could separate genealogy (A), subword or tokenizer effects (B) and competence or resource effects (C).
   - The most useful levers are:
     - **same-language, different-script pairs** already in Belebele (e.g., `zho_Hans`/`zho_Hant`, `hin_Deva`/`hin_Latn`);
     - **several languages per African family** (Atlantic-Congo, Afro-Asiatic);
     - **CJK as typology-genealogy decorrelators.** Japanese and Korean share coarse word-order features with Hindi and Tamil (§2) but belong to four different Glottolog families.
4. **North American Indigenous languages: NO-GO for this paper** (§6).
5. **Recommendation:**
   - Keep the Eastern India study as the paper.
   - Specify the extension as a separate exploratory study, designed only after the Phase 1 gates pass (§8).
   - Do not fold it into RQ1's confirmatory family.

---

## 1. Literature audit (cross-lingual sycophancy and behavioural transfer, for these languages)

| Work | Languages relevant here | What it does | Bearing on the extension | Label |
|---|---|---|---|---|
| Shah, Beniwal, Singh, Silpasuwanchai 2026 (arXiv 2606.08451, preprint) | zh, ja, ko (all "High-Resource", script "CJK"); my (Sino-Tibetan); no African languages | 38-language sycophancy rates. Family and script in regression. Resource tiers after Joshi et al. 2020. Prompts translated by MT (NLLB, Gemmax, TowerInstruct) | Adding CJK to a family analysis is **already done** at rate level. They use MT; we would use Belebele's human translations | [full-text] (Table 6 language inventory) |
| Aldahlawi, Rahman, Ahmad 2026 (arXiv 2603.27664, preprint) | zh (with ar, fr, es, pt) | Language of opinion prompts affects agreement rate | Chinese already covered at rate level, monolingual | [full-text] |
| Ranaldi & Pucci 2026 (EACL 2026, peer-reviewed) | zh, sw (Table 3) | Cross-lingual action consistency; mitigation transfer | Item-level cross-lingual consistency including zh/sw already measured (uncontrolled) | [full-text] |
| Awuni, Gyening, Owusu 2026, AfriSyCo (arXiv 2609.17853, preprint) | ha, ig, rw, sw, tw, yo | English follow-up pushback on African-language MCQ; native layer with non-equivalent templates | **Closest prior design.** Any African extension must state what is new beyond it (§4) | [full-text] |
| Huang & Cheng 2026 (LaTeCH-CLfL workshop) | Japanese mentioned (Kyoto group); India, Morocco, Malaysia scenarios | Language prestige in GPT-4o persuasion role-play | Status hierarchy is India-specific in our use; no CJK test of correction language | [full-text] |
| Mainzinger & Brixey 2026, IndigiEval (AmericasNLP 2026 workshop) | Mvskoke, Choctaw, Cherokee, Cheyenne, Hawaiian | Qualitative LLM evaluation. Reports no model performs well across categories and frequent hallucinated orthography, grammar and vocabulary | Evidence against competence for Cherokee (§6) | [abstract] |
| Vasselli et al. 2026 (EACL 2026 short) | 13 Indigenous languages of the Americas (page names Bribri, Guarani, Nahuatl) | Probing: language ID, cloze, grammatical features; many results near chance | Competence for most Indigenous languages of the Americas is doubtful | [abstract] |
| arXiv 2411.11295 (Cherokee translation with LLMs) | Cherokee | Reports near-zero zero-shot BLEU for English→Cherokee | Supports the competence concern; **not opened** | [search] |
| Qi, Fernandez, Bisazza 2023 (EMNLP) | BMLAMA-17/53 | Cross-lingual factual consistency tracks subword overlap more than genealogy | Main prior for Hypothesis B | [full-text] |
| Mitrovic et al. 2025 (arXiv, preprint) | MultiQ | Genus effects conditioned on resources | Prior for Hypothesis C | [abstract] |

**Searched and not found:**
- No Japanese-, Korean- or Chinese-specific sycophancy benchmark.
- No study that delivers the correction in a different language from the question for CJK.

Sources searched: four web searches, 2026-10-10, standard and extended modes. This is **not** evidence that none exists: native-language venues and terms (迎合, 아첨, 谄媚 in Chinese venues) were not systematically searched.

---

## 2. Genealogy and measured typology

### Genealogy

Glottolog, fetched 2026-10-10 [data].

| Language (Belebele config) | Glottocode | Glottolog top-level family > path (abridged) |
|---|---|---|
| Mandarin (`zho_Hans`, `zho_Hant`) | mand1415 | Sino-Tibetan > Sinitic > … > Mandarinic |
| Japanese (`jpn_Jpan`) | nucl1643 | Japonic > Japanesic |
| Korean (`kor_Hang`) | kore1280 | Koreanic (top-level family in Glottolog) |
| Yoruba (`yor_Latn`) | yoru1245 | Atlantic-Congo > … > Defoid > Yoruboid |
| Igbo (`ibo_Latn`) | nucl1417 | Atlantic-Congo > … > Igboid |
| Swahili (`swh_Latn`) | swah1253 | Atlantic-Congo > … > Narrow Bantu > East Bantu > … > Sabaki-Swahili |
| Kinyarwanda (`kin_Latn`) | kiny1244 | Atlantic-Congo > … > Narrow Bantu > East Bantu > Great Lakes Bantu |
| Ganda (`lug_Latn`) | gand1255 | Atlantic-Congo > … > Narrow Bantu > East Bantu > Great Lakes Bantu |
| Zulu (`zul_Latn`) | zulu1248 | Atlantic-Congo > … > Narrow Bantu > Southern Bantu > Nguni |
| Wolof (`wol_Latn`) | nucl1347 | Atlantic-Congo > North-Central Atlantic > Wolofic |
| Hausa (`hau_Latn`) | haus1257 | Afro-Asiatic > Chadic > West Chadic |
| Amharic (`amh_Ethi`) | amha1245 | Afro-Asiatic > Semitic > Ethiosemitic |
| Tigrinya (`tir_Ethi`) | tigr1271 | Afro-Asiatic > Semitic > Ethiosemitic |
| West Central Oromo (`gaz_Latn`) | west2721 | Afro-Asiatic > Cushitic > East Cushitic |
| Somali (`som_Latn`) | soma1255 | Afro-Asiatic > Cushitic > East Cushitic |
| Luo (`luo_Latn`) | luok1236 | Nilotic > Western Nilotic |
| Bambara (`bam_Latn`) | bamb1269 | Mande > Western Mande |
| Navajo (none) | nava1243 | Athabaskan-Eyak-Tlingit > … > Apachean |
| Cherokee (none) | cher1273 | Iroquoian |
| Plains Cree (none) | plai1258 | Algic > Algonquian |
| Eastern Huasteca Nahuatl (none) | east2538 | Uto-Aztecan > … > Aztec |

### Classification uncertainty

- **Korean and Japanese.** Glottolog treats Koreanic and Japonic as separate top-level families. Proposals linking them (e.g., "Altaic", "Transeurasian") are contested and are **not** assumed here. The extension codes them as different families and reports a sensitivity check that merges them.
- **Belebele `zho_*` label.** This is the macrolanguage code for written Standard Chinese. Mapping it to Mandarin (mand1415) is our assumption: written Standard Chinese is Mandarin-based.
- **Nilotic** is a top-level family in Glottolog, not part of a "Nilo-Saharan" family. Do not merge it.
- **Same region is not the same family.** Swahili, Somali and Luo are all East African but belong to three families. Japanese, Korean and Mandarin are all East Asian, also three families.

### Measured typology

WALS Online v2020.6, Dryer 2013 chapters, fetched 2026-10-10 [data]. Abbreviations: Prep. = prepositions, Postp. = postpositions, suff. = suffixing, pref. = prefixing.

| Language | 81A Order of S, O, V | 85A Adposition order | 26A Prefixing vs. suffixing |
|---|---|---|---|
| English | SVO | Prep. | Strongly suff. |
| Hindi | SOV | Postp. | Strongly suff. |
| Bengali | SOV | **missing** | **missing** |
| Assamese | SOV | **missing** | Strongly suff. |
| Oriya (Odia) | SOV | **missing** | Strongly suff. |
| Tamil | SOV | Postp. | Strongly suff. |
| Mandarin | SVO | No dominant order | Strongly suff. (as coded by WALS) |
| Japanese | SOV | Postp. | Strongly suff. |
| Korean | SOV | Postp. | Strongly suff. |
| Yoruba | SVO | Prep. | Little affixation |
| Igbo | SVO | Prep. | **missing** |
| Swahili | SVO | Prep. | Weakly pref. |
| Kinyarwanda | SVO | Prep. | **missing** |
| Zulu | SVO | Prep. | Strong pref. |
| Hausa | SVO | Prep. | Little affixation |
| Amharic | SOV | No dominant order | Weakly suff. |
| Oromo (Harar) | SOV | Postp. | Strongly suff. |
| Somali | SOV | No dominant order | Strongly suff. |
| Luo | SVO | Prep. | Equal pref./suff. |
| Bambara | SOV | Postp. | Strongly suff. |
| Wolof | SVO | Prep. | Little affixation |
| Navajo | SOV | Postp. | Strong pref. |
| Cherokee | No dominant order | Postp. | Weakly pref. |
| Plains Cree | No dominant order | No adpositions | Equal pref./suff. |

What the table supports:
- **Coarse typology and genealogy do come apart in this pool.**
  - Japanese, Korean, Hindi and Tamil share SOV order, postpositions and suffixing, yet belong to four families.
  - English, Yoruba and Swahili share SVO order and prepositions, yet belong to two families (Indo-European and Atlantic-Congo).
  - This is the main reason CJK is useful.
- **WALS is sparse.**
  - It lacks 85A for Bengali, Assamese and Odia, and 26A for Bengali, Igbo and Kinyarwanda.
  - Oromo is coded for the Harar variety, while Belebele has West Central Oromo.
  - Three features are far too few for a "typological distance".
  - URIEL/lang2vec-derived vectors are the usual alternative. They are **not vetted** here; some variants impute missing values, and that would need to be checked and reported.
  - This remains open item 7 in `research.md` §13.

### Endangerment

Glottolog AES, fetched 2026-10-10 [data]. The status is given only where Glottolog provides one, with its attributed source.
- **Not endangered** (Ethnologue 2025 via Glottolog): Mandarin, Japanese, Korean, Yoruba, Swahili, Amharic, Zulu.
- **Navajo:** Glottolog AES "not endangered", while its cited ELCat comment says "At risk (20 percent certain)".
- **Cherokee:** "shifting" (ELCat, "Threatened, 20 percent certain").
- **Plains Cree:** "moribund" (ELCat, "Severely Endangered, 20 percent certain").
- **Eastern Huasteca Nahuatl:** "threatened" (UNESCO Atlas 2010, "Vulnerable").
- No other endangerment or "under-resourced" claim is made in this document.

---

## 3. Data, script, tokenization, model coverage, competence and resource evidence

**Benchmark data.** Belebele: 122 configs, listed from the Hugging Face datasets server on 2026-10-10 [data].
- **Present:** `zho_Hans`, `zho_Hant`, `jpn_Jpan`, `kor_Hang`, and African `afr amh bam fuv gaz hau ibo kin lin lug luo nso nya plt sna som sot ssw swh tir tsn tso wol xho yor zul` (plus Arabic varieties).
- **Absent:** Twi (in AfriSyCo but not Belebele), and **every Indigenous language of North America**. Belebele does include `grn_Latn` (Guarani, South America) and `mri_Latn` (Māori), which are outside scope.

**Script pairs inside Belebele** (same language, same items, different script): `zho_Hans`/`zho_Hant`, `hin_Deva`/`hin_Latn`, `ben_Beng`/`ben_Latn`, `npi_Deva`/`npi_Latn`, `urd_Arab`/`urd_Latn`, `sin_Sinh`/`sin_Latn`, `arb_Arab`/`arb_Latn`.
- These hold genealogy and typology fixed while changing tokenization. They are the cleanest available lever for Hypothesis B.
- Caveats:
  - Romanised Hindi and Bengali are less standardised in use than in Belebele's renderings.
  - Simplified vs. Traditional Chinese also differ in regional training-data sources, so the pair is not a pure tokenizer manipulation.
- Whether prior work has used Belebele script pairs this way was **not checked**.

**Tokenization.** Not measured; that would need each model's tokenizer, and nothing was downloaded. Planned measures:
- fertility (tokens per word, or per character for CJK, where "word" is ill-defined) on Belebele passages;
- subword-vocabulary overlap between language pairs, following Qi et al. 2023, per model.

CJK and Ethiopic (`amh_Ethi`, `tir_Ethi`) are the scripts where fertility is most likely to differ from Latin-script languages. That is an expectation to measure, not a measured fact.

**Model coverage.** Unknown for the candidate models; no model was queried.
- Shah et al. classify zh, ja and ko as "High-Resource" using Joshi et al. 2020's taxonomy.
- No resource class was verified here for the African candidates. Joshi et al.'s class assignments must be looked up per language before any "low-resource" label is used.

**Competence.**
- Must be measured per (model, language) by the existing gates: four-order gate pass rate, exact binomial against chance, and the correction-comprehension probe.
- It is **never inferred** from fluent output.
- For Indigenous languages of the Americas, published evaluations (IndigiEval; Vasselli et al.) report weak or near-chance performance for many model-language pairs [abstract]. So gate pass counts would likely be too small to identify capitulation (cf. `docs/feasibility.md` on Toto, Birhor and Bondo).

---

## 4. Language-selection matrix

Columns: G = genealogy, T = coarse typology, S = subword or script, R = resource, C = competence. "+" = this candidate adds leverage on that factor; "–" = adds little; "?" = unknown until measured.

| Candidate | G | T | S | R | C | What it contributes | Main risk |
|---|---|---|---|---|---|---|---|
| Mandarin (`zho_Hans` + `zho_Hant`) | + (Sino-Tibetan singleton in panel) | + (SVO, no dominant adposition order) | **++** (script pair) | likely high (Shah tier) | ? | Script-pair test of B; a family absent from the core panel | Singleton family: no within-family contrast |
| Japanese | + (Japonic singleton) | **+** (shares SOV/Postp./suffixing with hin and tam) | + (mixed scripts) | likely high | ? | Typology-genealogy decorrelation | Singleton family |
| Korean | + (Koreanic singleton) | **+** (as Japanese) | + (Hangul, alphabetic) | likely high | ? | With Japanese, a typologically similar, genealogically distinct pair | Debated links to Japanese must not be assumed |
| Swahili, Yoruba | + (Atlantic-Congo) | + (SVO/Prep.) | – (Latin) | ? | ? | **Replication anchors against AfriSyCo** | Overlap with AfriSyCo |
| Zulu, Ganda (non-AfriSyCo Bantu) | **++** (several Atlantic-Congo members) | + (prefixing) | – | ? | ? | Within-family variation, beyond AfriSyCo's set | Competence unknown |
| Amharic, Tigrinya (Semitic) + Somali, Oromo (Cushitic) | **++** (several Afro-Asiatic members across branches) | + (SOV vs. Hausa SVO within one family) | + (Ethiopic vs. Latin within a family) | ? | ? | Within-family script and order variation | Competence unknown; dialect choice for Oromo |
| Luo (Nilotic), Bambara (Mande), Wolof | + (additional families) | + | – | ? | ? | More independent families | Singletons |
| Navajo, Cherokee, Plains Cree, Nahuatl | + | + | + | – | likely low ([abstract] evidence) | Not identifiable without competence | Ethics, data, competence: **NO-GO** (§6) |

**What is new beyond AfriSyCo, if African languages are added:**
- the same-content, same-target-naming manipulation of correction language (RQ1 contrast 1);
- the language-matched neutral re-ask;
- the four-order gate;
- several families with several members each.

An African set that is mostly non-AfriSyCo (e.g., Zulu, Ganda, Amharic, Tigrinya, Somali), plus one or two AfriSyCo languages (Swahili, Yoruba) as replication anchors, keeps the overlap explicit and limited.

---

## 5. Can the expanded design identify A vs. B vs. C?

- **Independent units are languages, not items or pairs.** Item-level data give precise estimates per (model, language) cell. But A/B/C are claims about between-language variation, so their effective sample size is the number of languages, and for A, the number of families with more than one member.
- **Language pairs are not independent.** With k languages there are k(k−1)/2 dyads sharing members. Dyadic inference therefore needs the planned multi-membership model plus a QAP or permutation test (`research.md` §6, E2). Treating dyads as independent would overstate certainty.
- **CJK add families but no within-family contrast.**
  - Each is a singleton, so a family random effect cannot be estimated from them.
  - They help separate typology from genealogy, and (via `zho_Hans`/`zho_Hant`) script from both.
  - They cannot establish a family-level effect.
- **Families with several members come mainly from Africa:** Atlantic-Congo and Afro-Asiatic, alongside Indo-European from the core. Without several such families, Hypothesis A cannot be tested in the sense the user stated it ("languages from the same family exhibit more similar capitulation patterns").
- **The factors are confounded.**
  - Script, subword overlap, resource level and competence co-vary with family; for example, Ethiopic script appears only within Semitic.
  - Script pairs and within-family script variation (Amharic vs. Somali) are the main ways to break this.
  - The rest must be handled by covariate adjustment, which supports only *conditional association*, not causal attribution.
- **Competence gating shrinks the panel non-randomly.** Languages failing the gate drop out, and they are likely the lower-resource ones. Survivors then over-represent high-competence languages, which biases any resource or competence conclusion (Hypothesis C). Drop-outs must be reported as a result in their own right.
- **Multiplicity.** The full L_Q × L_P matrix grows quadratically with k. No confirmatory claims from it unless a separate preregistered plan defines the family of tests.
- **Power.** No sample size or power is claimed here. A power analysis needs variance components from Phase 1 and is required before Phase 2.

**Assessment:** a CJK + multi-family African extension can *in principle* give conditional evidence on B (script pairs) and partial evidence on A vs. T. A firm test of A requires more multi-member families than Belebele plus feasible competence is likely to supply. Conclusions should be phrased as "after adjustment, associated / not associated", never as a general family-level law.

---

## 6. Translation validation, reviewers and ethics

- **Same protocol as the core** (`docs/translation_validation.md`):
  - every FC, RA, VC, format and probe template in every new language;
  - one fluent reviewer plus an independent adjudicator where feasible.
- **No reviewers are recruited or assumed.**
  - Recruitment for Mandarin, Japanese, Korean, Swahili and Amharic is *plausibly* easier given large speaker populations, but this is unverified.
  - For Tigrinya, Somali, Oromo, Ganda and Luo it is unknown.
- **Item quality.** Belebele items are human-translated. The new burden is only the correction and re-ask templates, which must name the target identically and avoid added politeness or authority. This is harder in languages with grammaticalised honorific registers (Japanese and Korean speech levels), where "the same register" must be defined explicitly per language with reviewers.
- **Regional-status contrast does not transfer.** RQ1 contrast 2 (Hindi) is India-specific. A regional analogue elsewhere would need its own sociolinguistic justification and citation, such as a regional lingua franca. **Unresolved; no analogue is proposed here.**
- **North American Indigenous languages: NO-GO for this paper.**
  1. No Belebele or other parallel MCQ data were found.
  2. Published evaluations report weak or near-chance competence [abstract].
  3. Glottolog AES lists Cherokee as shifting and Plains Cree as moribund (each with 20% certainty in the cited source).
  4. Meaningful work requires community collaboration, speaker-authored items and agreed data governance, which this project does not have.

  Testing whether a model abandons answers it does not know is not interpretable. This should be revisited only through a community-led partnership with its own design.

---

## 7. Proposed exploratory design (no sizes, no expected results)

- **Phase gating.**
  - Phase 2 starts only after Phase 1 meets its go criteria (`research.md` §9).
  - Phase 2 has its own preregistration and its own multiplicity plan.
  - It is never added to RQ1's confirmatory family.
- **Languages (candidate, subject to gates):**
  - CJK: `zho_Hans`, `zho_Hant`, `jpn_Jpan`, `kor_Hang`.
  - African: Swahili and Yoruba as AfriSyCo anchors; Zulu, Ganda, Amharic, Tigrinya and Somali as non-overlapping, multi-member families.
  - Script-pair controls: `hin_Latn`, `ben_Latn`.
  - The final list depends on competence gates and reviewer availability.
- **Conditions.** Per question language L_Q:
  - FC and RA in L_Q and in English (contrast 1 generalisation);
  - optionally, the full matrix among a *small* subset chosen to maximise A/B/T separation.
  - Same templates, gate, matched re-ask, parser and scoring as the core.
- **Measures.**
  - Per (model, language): N = A − F, raw rates, gate pass counts, probe accuracy.
  - Per pair: concordance of net capitulation (E2).
  - Covariates measured per model: fertility and subword overlap from each model's tokenizer; resource class from a cited taxonomy; competence from the gates.
- **Analyses (exploratory).**
  - Dyadic multi-membership model with QAP.
  - Script-pair contrasts (Hans/Hant, Deva/Latn) as the primary B probe.
  - Leave-one-family-out prediction.
  - Korean–Japanese merged vs. separate sensitivity.
  - Drop-out analysis of gate failures.

---

## 8. Go / no-go and cost

**Recommendation:**
- **NO-GO** for adding any of these languages to the current study or its confirmatory family.
- **CONDITIONAL GO** for *designing* Phase 2 as a separate exploratory study after Phase 1 passes its gates, built around the identification levers in §4–§5.
- **NO-GO** for North American Indigenous languages in this project.

**Additional cost (no calls executed).** Per model, per added question language, with n items, follow-ups on gated items only (upper bounds):
- turn 0: 4n;
- FC and RA in L_Q and English: 4n (2n for English itself);
- VC: up to n.

That is ≤ 9n calls per language per model; at the pilot's n = 100 this is ≤ 900.
- The full L_Q × L_P matrix over a subset of size s adds 2n(s − 2) per L_Q.
- Human cost per new language: template drafting and back-translation, plus two reviewers. This cost scales with languages, not calls, and is the binding constraint.
- Tokenizer measurements need tokenizer files for each model. That is a download, to be approved separately.

---

## 9. Would this strengthen or dilute the paper?

**Dilute, if merged into the current paper.**
- RQ1 is a narrow, controlled contrast whose novelty over AfriSyCo is already thin.
- Adding many languages would:
  - multiply templates and reviewers;
  - delay Phase 1;
  - inflate the contrast family;
  - invite the reading that this is "a new collection of language comparisons", which Shah et al. and AfriSyCo already partly provide.

**Strengthen, as a separately designed follow-up.** That holds only if it is built to separate A, B and C:
- script pairs for B;
- multi-member families for A;
- typology-genealogy decorrelation via CJK;
- explicit competence gating and drop-out reporting for C.

That would be a different contribution: an identification design rather than broader coverage. Whether it is novel must be audited separately: script-pair designs and multi-family sycophancy decompositions were **not** searched for in this audit.

## 10. Open items

1. Literature search in native-language venues and terms for CJK sycophancy.
2. Whether Belebele script pairs have been used to separate tokenization from language in behavioural studies.
3. Vetting a typology vector source (URIEL/lang2vec variants: coverage, imputation).
4. Verified resource class per African candidate (Joshi et al. 2020).
5. Reviewer availability per language.
6. Whether any regional-status analogue outside India is justified.
7. Full text of IndigiEval, Vasselli et al., and arXiv 2411.11295 (currently [abstract]/[search]).
