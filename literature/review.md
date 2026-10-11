# Literature audit: computational historical linguistics, borrowing strata and LLMs

_Audit date: 2026-10-10; round 2 added the same day (Kanojia 2019, Cristea full results, Dinu 2024, forward citations).  Stage B of the project reset (see `research.md`). The previous sycophancy review is archived at `archive/sycophancy_study_2026-10-10/literature/review.md`._

## Evidence levels

Every claim below carries one of these labels:

- **[FT]** Full text inspected this session. The relevant sections were extracted from the PDF and read: data, method, evaluation, and the passages paraphrased here.
- **[AB]** Abstract or landing page read. Metadata verified against Crossref or the ACL Anthology `.bib` file.
- **[MD]** Bibliographic metadata verified; content known only from search summaries. **Content claims must be checked before citing.**
- **[PR]** Standard reference from background knowledge, **not verified this session**.

**Peer-review status** is as recorded by the venue. arXiv "accepted to X" comments are reported as such; they are not independently confirmed.

**Search coverage.** About 25 web searches, plus Crossref, ACL Anthology, arXiv, Europe PMC, GitHub API and Wiktionary API lookups.

**Not searched:**
- Google Scholar forward citations;
- *Diachronica* and *Journal of Historical Linguistics* back issues;
- Indian-language venues (ICON, regional journals, theses);
- Chinese-language venues;
- List's "open problems" paper (mentioned in a search summary, not retrieved).

"Not found" below means **not found in these sources**.

---

## 1. Reconstruction and recovery of ancestral or intermediate stages

| Work | Status | Evidence | Key content | Bearing |
|---|---|---|---|---|
| Bouchard-Côté, Hall, Griffiths, Klein 2013. *Automated reconstruction of ancient languages using probabilistic models of sound change.* PNAS 110(11):4224–4229. doi:10.1073/pnas.1204678110 | Peer-reviewed journal | [AB] (full text not obtained: Europe PMC not open; PMC returned a CAPTCHA) | Probabilistic models of sound change plus inference; reconstructs **protolanguages** (plural) for 637 Austronesian languages. The abstract reports that over 85% of reconstructions are within one character of an expert's | **Latent ancestral and intermediate forms on a tree, with probabilistic inference, are established.** Whether borrowing strata are modelled is unknown from the abstract |
| Meloni, Ravfogel, Goldberg 2021. *Ab Antiquo: Neural Proto-language Reconstruction.* NAACL 2021, pp. 4460–4473. https://aclanthology.org/2021.naacl-main.353 | Peer-reviewed | [MD] | Latin from Romance reflexes (8,000+ entries) | Root reconstruction from descendants is established |
| Kim, Chang, Cui, Mortensen 2023. *Transformed Protoform Reconstruction.* ACL 2023 (short), pp. 24–38. https://aclanthology.org/2023.acl-short.3 | Peer-reviewed | [FT] | Transformer. Romance (8,799 sets) and Chinese (804 sets, 39 varieties plus **Middle Chinese**). Random 70/10/20 split. Cites Chang et al. 2022 reconstructing Middle Chinese from Wiktionary (5,000+ sets). **No memorisation or leakage discussion found** | Recovering an attested earlier stage is established. Random splits; no contamination analysis |
| Lu, Xie, Mortensen 2024. *Semisupervised Neural Proto-Language Reconstruction.* arXiv 2406.05930 ("Accepted to ACL 2024") | Peer-reviewed per arXiv comment | [MD] | Low-label reconstruction | Same task family |
| Cui, Chen, Wang, Mortensen 2024. *Neural Proto-Language Reconstruction.* arXiv 2404.15690 | Preprint (no venue in record) | [MD] | Transformer, VAE and augmentation extensions | Same task family |
| Akavarapu & Bhattacharya 2023. *Cognate Transformer for Automated Phonological Reconstruction and Cognate Reflex Prediction.* arXiv 2310.07487 ("Accepted at EMNLP-2023 (Main)") | Peer-reviewed per arXiv comment | [MD] | Pretrained transformer for reflex prediction and reconstruction | Strong neural baseline family |
| Cathcart & Rama 2020. *Disentangling dialects: a neural approach to Indo-Aryan historical phonology and subgrouping.* CoNLL 2020, pp. 620–630. https://aclanthology.org/2020.conll-1.50 | Peer-reviewed | [FT] | OIA etyma → reflexes from Turner's CDIAL (DSAL). Targets include medieval **Prakrit (Mahārāṣṭrī) N=8,118 and Pāli N=5,225**. LSTM with language embeddings predicts held-out forms. Notes that Persian/Arabic loans reduce Hindi inherited data, and that contact and analogy cause irregularity. **"We do not explicitly model contact."** Code released | **OIA→MIA prediction is established.** Learned borrowing from Sanskrit is not modelled |
| Cathcart 2020. *A probabilistic assessment of the Indo-Aryan Inner–Outer Hypothesis.* J. Historical Linguistics 10(1):42–86. doi:10.1075/jhl.18038.cat | Peer-reviewed | [MD] | Bayesian mixed-membership model over extracted OIA→NIA sound changes; partial support (search summary) | Computational testing of contested Indo-Aryan subgrouping is established |
| Temesgen, Nigatu, Andargie 2025. *Cognate Detection for Historical Language Reconstruction of Proto-Sabean Languages: the Case of Ge'ez, Tigrinya, and Amharic.* COLING 2025, pp. 7415–7422. https://aclanthology.org/2025.coling-main.496 | Peer-reviewed | [FT] (relevant passages) | **GPT-4o few-shot proto-forms used as synthetic training data**; Seq2Seq reconstruction. Mentions mT5/AfriTeVa pretraining on Amharic, **but no analysis of LLM memorisation** | LLM-assisted reconstruction exists; contamination not analysed |
| List, Vylomova, Forkel, Hill, Cotterell 2022. *The SIGTYP 2022 Shared Task on the Prediction of Cognate Reflexes.* SIGTYP workshop, pp. 52–62. https://aclanthology.org/2022.sigtyp-1.7 | Peer-reviewed workshop | [FT] (data, metrics) | Fill missing reflexes; multi-family data plus surprise data; normalised edit distance (by alignment length) | Reflex prediction under regular change is a mature task; reuse its metric definitions |

## 2. Cognate detection, correspondences and phylogeny

| Work | Status | Evidence | Bearing |
|---|---|---|---|
| List 2019. *Automatic Inference of Sound Correspondence Patterns across Multiple Languages.* Computational Linguistics 45(1):137–161. doi:10.1162/coli_a_00344 | Peer-reviewed | [MD] | Correspondence-pattern inference exists. Component and baseline |
| Jäger, List, Sofroniev 2017. *Using support vector machines and state-of-the-art algorithms for phonetic alignment to identify cognates in multi-lingual wordlists.* EACL 2017, pp. 1205–1216. https://aclanthology.org/E17-1113 | Peer-reviewed | [MD] | Supervised cognate detection |
| Rama, List, Wahle, Jäger 2018. *Are Automatic Methods for Cognate Detection Good Enough for Phylogenetic Reconstruction in Historical Linguistics?* NAACL 2018, pp. 393–400. https://aclanthology.org/N18-2063 | Peer-reviewed | [MD] | Automatic cognates approach but do not match expert phylogenies (search summary) |
| Akavarapu & Bhattacharya 2024. *Automated Cognate Detection as a Supervised Link Prediction Task with Cognate Transformer.* arXiv 2402.02926 ("Accepted to EACL-2024 main") | Peer-reviewed per arXiv comment | [MD] | Supervised cognate detection |
| Hruschka et al. 2015. *Detecting Regular Sound Changes in Linguistics as Events of Concerted Evolution.* Current Biology 25(1):1–9. doi:10.1016/j.cub.2014.10.064 | Peer-reviewed | [MD] | Phylogenetic modelling of sound change |
| Jäger 2018. *Global-scale phylogenetic linguistic inference from lexical resources.* Scientific Data 5. doi:10.1038/sdata.2018.189 | Peer-reviewed | [MD] | Large-scale automatic phylogeny |
| Bouckaert et al. 2012. *Mapping the Origins and Expansion of the Indo-European Language Family.* Science 337(6097):957–960. doi:10.1126/science.1219669 | Peer-reviewed | [MD] | Bayesian phylogeography |
| Chang, Cathcart, Hall, Garrett 2015. *Ancestry-constrained phylogenetic analysis supports the Indo-European steppe hypothesis.* Language 91(1):194–244. doi:10.1353/lan.2015.0005 | Peer-reviewed | [MD] | **Attested ancestors used as constraints** in phylogenetic inference |
| Kolipakam et al. 2018. *A Bayesian phylogenetic study of the Dravidian language family.* Royal Society Open Science 5(3):171504. doi:10.1098/rsos.171504 | Peer-reviewed | [MD] | Dravidian phylogeny |
| List, Forkel, Greenhill, Rzymski, Englisch, Gray 2022. *Lexibank, a public repository of standardized wordlists with computed phonological and lexical features.* Scientific Data 9. doi:10.1038/s41597-022-01432-0 | Peer-reviewed | [MD] | CLDF infrastructure; 2,000+ varieties (search summary) |

## 3. Borrowing, learned strata and inheritance vs. borrowing

| Work | Status | Evidence | Key content | Bearing |
|---|---|---|---|---|
| **Cristea, Dinu, Georgescu, Mihai, Uban 2021.** *Automatic Discrimination between Inherited and Borrowed Latin Words in Romance Languages.* Findings of EMNLP 2021, pp. 2845–2855. https://aclanthology.org/2021.findings-emnlp.243 | Peer-reviewed (Findings) | [FT] | Labels from **Wiktionary** templates (plus DEX for Romanian), 2,425–4,672 words per language. Normalised word–etymon distance is lower for borrowed (about 0.28–0.31) than inherited (about 0.38–0.56). SVM with etymon features is best; F1 84.5–92.1 (orthographic), 81.3–92.2 (phonetic), average about 90%. Errors: no distinguishing features (Romanian *suc*), **semi-learned** reshaping (French *discourir*, Romanian *demn*), transmission via another language. No intermediate stage | **Closest competitor and a high bar.** Learned vs. inherited attribution is established for Romance |
| Dinu, Uban, Iordache, Cristea, Georgescu, Zoicas 2024. *Pater Incertus? There Is a Solution: Automatic Discrimination between Cognates and Borrowings for Romance Languages.* LREC-COLING 2024, pp. 12657–12667. https://aclanthology.org/2024.lrec-main.1108 | Peer-reviewed | [MD] | Cognates vs. borrowings between Romance language pairs; graphic vs. phonetic features (search summary) | Same group; borrowing between contemporary languages, not ancestor re-borrowing |
| **Kanojia, Kulkarni, Bhattacharyya, Haffari 2019.** *Cognate Identification to improve Phylogenetic trees for Indian Languages.* CoDS-COMAD 2019 (Young Researchers' Symposium), pp. 297–300. doi:10.1145/3297001.3297045 | Young Researchers' Symposium short paper (review process not verified) | [Thesis §4.1 only: Kanojia's Monash PhD thesis 2021, doi:10.26180/14870082, which states the work was accepted at CoDS-COMAD 2019. ACM version paywalled; **correspondence with the published paper not verified**] | Orthographic cognate detection, Sanskrit/Hindi/Marathi/Punjabi (IndoWordNet). Validated by lexicographers; a negative result on precision. **Observes** that orthographic similarity readily finds tatsama cognates but hardly detects tadbhavas. Descriptive (unchanged vs. changed form) definitions; no attribution classifier; no MIA stage | **Prior computational discussion of tatsama/tadbhava.** Our earlier "not found" claim was too broad. Motivates strong surface baselines (failure check F3) |
| List & Forkel 2021. *Automated identification of borrowings in multilingual wordlists.* Open Research Europe 1:79. doi:10.12688/openreseurope.13843.2 | Peer-reviewed (open post-publication review) | [MD] | Borrowing across multiple languages (48 South-East Asian languages per search summary) | Borrowing between contemporary lineages, not learned borrowing from an ancestor |
| Miller, Tresoldi, Zariquiey, Beltrán Castañón, Morozova, List 2020. *Using lexical language models to detect borrowings in monolingual wordlists.* PLOS ONE 15(12):e0242709. doi:10.1371/journal.pone.0242709 | Peer-reviewed | [MD] | Phonotactic language models, no donor needed | Baseline that sees no etymon |
| Miller & List 2023. *Detecting Lexical Borrowings from Dominant Languages in Multilingual Wordlists.* EACL 2023, pp. 2599–2605. https://aclanthology.org/2023.eacl-main.190 | Peer-reviewed | [MD] | Supervised detection with a known donor | Baseline family |
| Wientzek 2025. *Self-Supervised Borrowing Detection on Multilingual Wordlists.* arXiv 2512.01713 | Preprint | [MD] | Self-supervised borrowing detection | Recent baseline candidate |
| Sousa Silva & Ahmadi 2026. *Are Language Models Borrowing-Blind? A Multilingual Evaluation of Loanword Identification across 10 Languages.* LREC 2026, pp. 3394–3401. https://aclanthology.org/2026.lrec-1.269 | Peer-reviewed | [MD] | LLMs fail to separate loanwords from native words (search summary) | LLM-only attribution likely weak |
| Liang, Abo Mokh, Alhafni 2026. *When Similar Means Different: Evaluating LLMs on Arabic–Hebrew Cognates.* arXiv 2606.13218 ("Accepted to EMNLP 2026") | Peer-reviewed per arXiv comment | [AB] | 1,858 pairs; LLMs rely on surface similarity; worse on false friends; variable on loanwords | LLMs confuse resemblance with history |
| Fourrier & Sagot 2020. *Methodological Aspects of Developing and Managing an Etymological Lexical Resource: Introducing EtymDB-2.0.* LREC 2020, pp. 3207–3216. https://aclanthology.org/2020.lrec-1.392 | Peer-reviewed | [MD] | Wiktionary-derived etymology database (1.8M lexemes, 700k+ relations per search summary); repository licence reported as CC BY-SA 4.0 (search summary) | Data infrastructure and label source |
| Dinu et al. 2023, RoBoCoP | Unknown | [search only] | Romance cognate and borrowing database | To verify |
| Rahman et al. 2022. *CNN for Modeling Sanskrit Originated Bengali and Hindi Language.* AACL 2022, pp. 47–56 | Peer-reviewed | [FT] | **Language modelling, not tatsama/tadbhava classification** | Excluded as a competitor |

**Searched and not found:** a **supervised, calibrated attribution** model for tatsama/tadbhava under historical definitions. Kanojia et al. 2019 discuss the distinction computationally (observation within cognate detection) but do not classify or evaluate attribution.

**Forward citations checked** (Semantic Scholar, 2026-10-10): Cathcart & Rama 2020 (9), Jambu 2023 (4), Cristea 2021 (8). None addresses Indo-Aryan learned vs. inherited attribution. Adjacent, unread: "It takes two to borrow: a donor and a recipient. Who's who?" (ACL 2024) and "What NLP Gets Wrong About Contact: Implications for Field Linguistic Evidence" (2026 workshop).

### Round 3 additions

| Work | Status | Evidence | Bearing |
|---|---|---|---|
| List 2024. *Open Problems in Computational Historical Linguistics.* Open Research Europe 3:201. doi:10.12688/openreseurope.16804.2 | Open-peer-reviewed journal | [FT] (borrowing section) | Calls the detection of contact layers (stratifying borrowings by contact event) a "truly hard problem". Context for significance; broader than this project's task |
| Arora, Farris, Basu, Kolichala 2022. *Computational Historical Linguistics and Language Diversity in South Asia.* ACL 2022, pp. 1396–1409. https://aclanthology.org/2022.acl-long.99 | Peer-reviewed | [FT] (searched) | Survey; argues data scatteredness is the main obstacle; **no mention of tatsama/tadbhava** |
| IITB–Monash Research Academy page by D. Kanojia (iitbmonash.org/researchStoriesInternal/2) | Web page, not peer-reviewed | [read] | Semantic cognate detection motivated by the tatsama/tadbhava distinction; no classifier or publication cited |
| Bangla loanword phonology critique of the tripartite scheme (academia.edu, "Constraints through the ages: loanwords in Bangla") | Unknown | [search only] | Argues tatsama/tadbhava/other does not fit Bangla phonology; supports treating labels as operational |

## 4. LLMs and multilingual representations for historical linguistics

| Work | Status | Evidence | Bearing |
|---|---|---|---|
| Liu, Shi, Zhou, Zhang 2026. *Would LLMs be Good Historical Linguists and Chinese Dialect Learners?* ACL 2026 (long), pp. 18231–18256. https://aclanthology.org/2026.acl-long.831 | Peer-reviewed | [AB] | Middle Chinese → 12 dialects; sound-law induction and dialect IPA; LoRA + GRPO beat DeepSeek-V3.2 and ChatGPT-5.2 baselines |
| Naik et al. 2024. *Can Large Language Models Code Like a Linguist?: A Case Study in Low Resource Sound Law Induction.* arXiv 2406.12725 | Preprint | [MD] | Sound-law induction as program synthesis |
| Naik et al. 2025. *PBEBench.* arXiv 2505.23126 | Preprint | [MD] | Synthetic sound-change reasoning benchmark |
| Rama, Beinborn, Eger 2020. *Probing Multilingual BERT for Genetic and Typological Signals.* COLING 2020, pp. 1214–1228 | Peer-reviewed | [MD] | mBERT distances give trees close to reference trees (search summary) |
| Beinborn & Choenni 2020. *Semantic Drift in Multilingual Representations.* Computational Linguistics 46(3):571–603. doi:10.1162/coli_a_00382 | Peer-reviewed | [MD] | Phylogeny-like trees from representations (search summary) |

Embedding-based genealogy recovery is established and only approximate. It cannot separate inheritance, contact and shared training data, so this project does not use embedding similarity as evidence of ancestry.

## 5. Manuscripts, decipherment and documentation (adjacent)

| Work | Status | Evidence | Bearing |
|---|---|---|---|
| Luo, Cao, Barzilay 2019. *Neural Decipherment via Minimum-Cost Flow: From Ugaritic to Linear B.* ACL 2019, pp. 3146–3155. https://aclanthology.org/P19-1303 | Peer-reviewed | [MD] | Lost-script decipherment; different task |
| Assael et al. 2022. *Restoring and attributing ancient texts using deep neural networks.* Nature 603:280–283. doi:10.1038/s41586-022-04448-z | Peer-reviewed | [MD] | Inscription restoration; different task |
| Farris & Arora 2021. *For the Purpose of Curry: A UD Treebank for Ashokan Prakrit.* arXiv 2111.12783 (UDW 2021 per arXiv) | Workshop | [MD] | Small MIA syntactic resource |
| Arora, Farris, Basu, Kolichala 2023. *Jambu: A historical linguistic database for South Asian languages.* SIGMORPHON 2023, pp. 68–77. https://aclanthology.org/2023.sigmorphon-1.8 | Peer-reviewed workshop | [FT] (data and licensing passages) | Data at github.com/moli-mandala/data. CDIAL material scraped "with SARVA project approval for academic purposes". **The GitHub API reports no licence file** (checked 2026-10-10). GRU/Transformer reflex-prediction baselines |

## 6. Uncertainty, ethics and data governance

- Carroll et al. 2020. *The CARE Principles for Indigenous Data Governance.* Data Science Journal 19. doi:10.5334/dsj-2020-043 [MD].
- Mainzinger & Brixey 2026, *IndigiEval* (AmericasNLP 2026) [AB] and Vasselli et al. 2026 (EACL 2026 short) [AB]. Both report weak LLM competence for many Indigenous languages of the Americas.
- **No work found reports calibration** (Brier score, ECE) for etymological attribution.

## 7. Indo-Aryan historical background

Not verified this session; each item must be checked against the source before use:
- Masica 1991, *The Indo-Aryan Languages* (Cambridge) [PR].
- Cardona & Jain (eds.) 2003, *The Indo-Aryan Languages* (Routledge) [PR].
- Chatterji 1926, *The Origin and Development of the Bengali Language* [PR].
- Turner 1962–1966, *A Comparative Dictionary of the Indo-Aryan Languages*. The DSAL edition carries a SOAS copyright notice [search].

**Working distinctions, to be verified against these sources:**
- *tadbhava*: inherited through MIA.
- *tatsama*: borrowed from Sanskrit after MIA, retaining the Sanskrit form.
- *ardhatatsama*: semi-learned, partly adapted.
- *deśī*: non-Indo-Aryan origin.
- Classical Sanskrit is not the direct parent of modern NIA languages. Literary Prakrits and Apabhraṃśa are stylised, not linear ancestors.

**Machine-readable silver labels on Wiktionary.** Category sizes from the Wiktionary API, 2026-10-10:

| Category | Pages |
|---|---|
| Hindi learned borrowings from Sanskrit | 1,337 |
| Hindi semi-learned borrowings from Sanskrit | 98 |
| Hindi terms inherited from Sanskrit | 2,241 |
| Hindi terms inherited from Sauraseni Prakrit | 734 |
| Bengali learned borrowings from Sanskrit | 1,075 |
| Bengali semi-learned borrowings from Sanskrit | 44 |
| Bengali terms inherited from Sanskrit | 1,045 |
| Bengali terms inherited from Magadhi Prakrit | 219 |
| Assamese learned borrowings from Sanskrit | 149 |
| Odia learned borrowings from Sanskrit | 269 |

Further queries hit rate limits. These labels are community-edited, often derived from CDIAL, and of **unknown accuracy**.

## 8. Synthesis

**Established:**
- latent ancestral and intermediate reconstruction (Bouchard-Côté 2013);
- OIA→MIA/NIA prediction (Cathcart & Rama 2020);
- recovery of attested earlier stages (Kim 2023; Chang et al. 2022, per Kim);
- learned vs. inherited discrimination in Romance with etymon features (Cristea 2021);
- borrowing detection between lineages (List & Forkel 2021; Miller 2020/2023);
- LLM weakness on cognates and loanwords (Liang 2026; Sousa Silva & Ahmadi 2026);
- embedding-based approximate genealogy (Rama 2020; Beinborn & Choenni 2020).

**Not found in the sources searched:**
1. Learned vs. inherited attribution using an **explicit latent intermediate-stage model** as the inheritance hypothesis.
2. **Supervised, calibrated tatsama/tadbhava attribution** under historical definitions (the distinction itself is discussed computationally by Kanojia et al. 2019).
3. **Calibrated** etymological attribution (proper scoring rules, abstention).
4. Measurement of **LLM memorisation of published etymologies** as a confound.

Their status is assessed in `docs/novelty_audit.md`.
