# Novelty audit

_Version 3, 2026-10-10. Updated after novelty rounds 2–3 (decision log 39–40 and 44–46). Evidence levels as in `literature/review.md`._

There is no numerical novelty score. Each claim is classified as one of:
- **Supported:** supported by direct comparative evidence.
- **Plausible, not established.**
- **Partly addressed.**
- **Already addressed:** substantially addressed by prior work.
- **Unknown:** the evidence is incomplete.

## 1. Checks performed in round 2

| Check | Result | Evidence |
|---|---|---|
| Kanojia, Kulkarni, Bhattacharyya, Haffari 2019, *Cognate Identification to improve Phylogenetic trees for Indian Languages*, CoDS-COMAD 2019 (Young Researchers' Symposium), pp. 297–300, doi:10.1145/3297001.3297045 | Found (pointed out by the user) | Metadata [Crossref]. ACM version **paywalled (HTTP 403; Unpaywall: not open access)**. Content read **only** in Kanojia's PhD thesis §4.1 (Monash 2021, doi:10.26180/14870082). The thesis states this work "was accepted at the Young Researcher's Symposium at CoDS-COMAD 2019". **That the thesis text matches the published paper is not verified.** Statements below are attributed to the thesis, not to the paper |
| Cristea et al. 2021, full results and error analysis | Read | [FT] |
| Dinu, Uban, Iordache, Cristea, Georgescu, Zoicas 2024, *Pater Incertus? There Is a Solution: Automatic Discrimination between Cognates and Borrowings for Romance Languages*, LREC-COLING 2024, pp. 12657–12667 | Found | [MD] (ACL Anthology `.bib`). Content from search summary only |
| Forward citations | Cathcart & Rama 2020: 9; Jambu 2023: 4; Cristea 2021: 8 (Semantic Scholar) | None does learned vs. inherited attribution for Indo-Aryan. Adjacent: "It takes two to borrow: a donor and a recipient. Who's who?" (ACL 2024, per Semantic Scholar), on borrowing direction; "What NLP Gets Wrong About Contact" (2026 workshop), not read |
| Bouchard-Côté et al. 2013 full text | **Not obtained.** PMC returned a CAPTCHA; Europe PMC has no open full text | Remains [AB]. Whether internal nodes or borrowing are modelled is unverified |
| Indian-venue search (ICON, Anthology) for tatsama/tadbhava classifiers | One extended search; nothing beyond Kanojia 2019 | Bengali/Hindi-language publications and theses not searched |

### What Kanojia et al. 2019 does (as reported in thesis §4.1)

All of the following comes from the thesis; check against the ACM paper before citing as the paper's findings.
- **Task:** orthographic **cognate detection** between Sanskrit and Hindi, Marathi and Punjabi (and Hindi with the others), using IndoWordNet wordlists. Methods were XDice, string similarity, and SVM/HMM alignment. Cognate sets were validated by lexicographers.
- **Purpose:** phylogenetic inference.
- **Main result:** negative. Orthographic measures do not detect cognates with high precision. Reported counts include, for Hindi–Sanskrit, 378 true positives and 211 false positives among 589 detected.
- **Tatsama/tadbhava appears as an observation:** orthographic similarity "could easily form pairs of cognate words which are Tatsama words", whereas "Tadbhava words were hardly detected" without phonetic methods.
- **No classifier labels words as tatsama or tadbhava.** There is no attribution evaluation, no Middle Indo-Aryan stage and no calibration.
- **Terminology differs:** the thesis defines tatsama and tadbhava descriptively (unchanged vs. changed form) and calls both "borrowed". This project uses the historical definition: inherited through MIA vs. borrowed after the MIA period.

**Consequences for this project:**
1. The previous claim "no computational work separates tatsama from tadbhava" was **too broad** and is withdrawn. Computational work has *discussed* the distinction and observed its effect on cognate detection.
2. Its observation is **direct prior evidence for our failure check F3:** orthographic similarity separates tatsamas easily, so the task may be easy in orthographic form. Strong surface baselines are mandatory, and the primary test may need to move to the hard subset (protocol §12).

### What Cristea et al. 2021 actually does (full results)

- **Labels** come from **Wiktionary** etymology templates (as planned here), plus DEX for Romanian. Sizes per language range from 2,425 to 4,672 words.
- **Mean normalised word–etymon distance** is lower for borrowed words (about 0.28–0.31) than for inherited ones (about 0.38–0.56), so surface distance is informative.
- **Systems:** RF, gradient boosting, SVM, RNN, and SVM with etymon features. F1 is reported as 84.5–92.1 (orthographic) and 81.3–92.2 (phonetic), with an average of about 90% at the orthographic level. The best systems are SVMs, improved by etymon features.
- **Error sources they report:**
  - no distinguishing features (e.g., Romanian *suc*);
  - **semi-learned** borrowings reshaped by inherited relatives (e.g., French *discourir*, Romanian *demn*);
  - transmission via another language.
- **No intermediate stage** is modelled.

**Consequence:** the competitive bar is high. Direct word–etymon classifiers already reach about 90% F1 on Romance Wiktionary data. Any gain from an intermediate stage must be shown **beyond** such a classifier, and specifically on the error classes they identify (semi-learned items, items without distinguishing features).

## 1b. Round 3 searches (2026-10-10)

| Search | Result |
|---|---|
| Sanskrit-derived vocabulary classification; loanword-origin identification (English; extended) | No computational classifier found. Found: a CNN language-modelling paper (not relevant); a linguistic critique of the tripartite scheme for Bangla (academia.edu, search summary) |
| Hindi and Bengali terms (तत्सम/तद्भव; তৎসম/তদ্ভব) | Only grammar and exam material, with hand-written spelling heuristics; no computational work |
| Shodhganga theses | No thesis on tatsama/tadbhava identification found among returned records (search engine coverage of Shodhganga is limited) |
| IITB–Monash research page (Kanojia) | Semantic cognate detection motivated by tatsama/tadbhava; **not** a classifier |
| Arora, Farris, Basu, Kolichala 2022, *Computational Historical Linguistics and Language Diversity in South Asia*, ACL 2022, pp. 1396–1409 [FT searched] | No mention of tatsama/tadbhava |
| List 2024, *Open Problems in Computational Historical Linguistics*, Open Research Europe 3:201 [FT, relevant section] | Names detection of **contact layers** ("group borrowings into different strata… identified with specific contact events in time") as a "truly hard problem". **Context for significance only:** that problem concerns contact layers across languages, broader than this project's inherited-vs.-learned-from-ancestor distinction |

## 2. Claim status (revised)

| # | Claim | Status | Closest work |
|---|---|---|---|
| N1 | AI discovers lost or undocumented languages | **Rejected** | n/a |
| N2 | Recovering intermediate or ancestral forms | **Already addressed** | Bouchard-Côté 2013; Cathcart & Rama 2020; Kim 2023 |
| N3 | Inherited vs. learned discrimination given an etymon | **Already addressed** (Romance) | Cristea 2021; Dinu et al. 2024 (cognates vs. borrowings) |
| N4 | Genealogy from representations | **Already addressed** | Rama 2020; Beinborn & Choenni 2020 |
| N5 | Attribution in which the inheritance hypothesis is an explicit, historically constrained MIA pathway, compared by likelihood with a learned-borrowing channel, **with controls showing that the gain comes from historical content rather than capacity** | **Plausible, not established** | Cristea 2021 (direct features); Cathcart & Rama 2020 (no learned pathway); Bouchard-Côté 2013 (full text unread) |
| N6 | Computational treatment of tatsama/tadbhava | **Distinction discussed in prior work, but not computationally classified in the inspected sources.** Kanojia 2019 (thesis §4.1): an observation within orthographic cognate detection. The IITB–Monash research page by Kanojia: semantic cognate detection motivated by the distinction; no classifier described; no publication cited. Arora et al. 2022 (ACL survey of South Asian computational historical linguistics, full text searched): no mention. **A classification contribution is not claimed until the labels are defined (`docs/annotation_guidelines.md`) and validated** | Kanojia 2019; IITB–Monash page |
| N7 | Calibrated etymological attribution with abstention | **Plausible, not established;** weak alone | None found |
| N8 | LLM memorisation of etymologies as a measured confound | **Plausible, not established** | Kim 2023 and Temesgen 2025 [FT]: none. Liang 2026 and Sousa Silva & Ahmadi 2026: full texts unread |
| N9 | Replication beyond Indo-Aryan | **Unknown** | Cristea 2021 data (Wiktionary-derived; licence unverified) |

## 3. Current defensible statement (search-bounded)

> The inspected sources discuss the tatsama–tadbhava distinction and computational cognate detection. The searches conducted have not identified a computational classifier specifically evaluating these historical transmission categories.

This is a **search-bounded finding, not proof** that no such classifier exists. The published-paper verification (ACM Kanojia 2019) and the broader literature audit remain **open**.

## 3b. Candidate contribution (not established)

> In the sources searched, no work tests whether explicitly modelling a historically constrained Middle Indo-Aryan pathway improves calibrated inherited-vs.-learned attribution for Indo-Aryan words beyond established direct word–etymon classifiers. No work tests whether any such gain reflects the historical content of the intermediate stage rather than extra model capacity.

## 4. Remaining checks before any novelty statement in a paper

1. Bouchard-Côté et al. 2013 full text and SI (library access, or ask the user).
2. Kanojia et al. 2019, ACM version (library access). The thesis is the current source.
3. Dinu et al. 2024 and the "It takes two to borrow" paper (ACL 2024): read in full.
4. Liang 2026 and Sousa Silva & Ahmadi 2026: check for contamination analysis.
5. A search in Bengali and Hindi terms (তৎসম/তদ্ভব; तत्सम/तद्भव) for computational work, and Indian theses (Shodhganga).
6. List's "open problems in computational historical linguistics" (not retrieved).

## 5. Ways the claim can still fail

- Bouchard-Côté's framework or its follow-ups may include borrowing pathways.
- A strong direct classifier may already reach the ceiling on Indo-Aryan, as orthographic similarity did for tatsamas in Kanojia 2019.
- The intermediate stage may help only through capacity: the shuffled-MIA control matches P.
- Too few items may have a historically justified simple MIA pathway.
- Silver labels may be too noisy, and expert labels too few.
