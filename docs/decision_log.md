# Decision log

Format: date, decision, reason, evidence, reversible?

## 2026-10-10

1. **Audit the conversation plan, not a file.** No `research.md` existed and the repository was empty, so there was nothing to back up. The audited material is the ChatGPT plan and the Gemini "Algorithmic Paleolinguistics" brief pasted into the session. *Reversible: n/a.*

2. **Reject the "ghost substrate / residual vector field inversion" component.** Reasons:
   - E[h⁽ˡ⁾] "from a Glottolog path" is undefined: Glottolog gives labels, not vectors.
   - "Unrecorded" substrates have no ground truth, so discovered clusters cannot be validated.
   - The PMS formula conditions perplexity on a residual norm, which off-the-shelf models do not support.

   A falsifiable variant that tests *documented* contact effects (e.g., representational similarity vs. Glottolog genealogy vs. geographic distance) is possible but is **out of scope** for this paper. *Reversible: yes, as a separate project.*

3. **Do not cite "Latin Substrate Bias (2026)" or "Kim et al. (2026)"** (from the Gemini brief). Neither could be located. *Reversible if someone produces the papers.*

4. **Reframe the original RQ.** Family as a predictor of sycophancy *rate* is partially addressed by Shah et al. 2026 (arXiv 2606.08451; family and script in OLS). The genealogy effect is now tested on *item-level flip concordance* (T1), with subword overlap as a mandatory control because of Qi et al. 2023. *Reversible: yes.*

5. **Adopt the manipulated pushback language (L_Q ≠ L_P) as the primary hypothesis (H2).** It was not found in the sources searched. Huang & Cheng 2026 is the closest work (status effects in monolingual GPT-4o persuasion simulations). It must be re-checked by forward-citation search before claiming novelty. *Reversible: yes.*

6. **Adopt knowledge-conditioning (4-rotation gate) plus a re-ask placebo plus a valid-correction control.** Prior multilingual sycophancy work inspected does not condition on correctness, MCQ option-order sensitivity is documented (Zheng et al. 2024; Pezeshkpour & Hruschka 2024), and SycoBench-600 requires selectivity. *Reversible: yes.*

7. **Exclude Toto, Birhor and Bondo/Remo from the quantitative study.** There is no evaluation data, competence is likely near chance (so sycophancy cannot be identified), vitality evidence has 20% certainty, and community consent is required. They remain as a feasibility discussion. *Reversible if a community partnership and speaker-authored items materialise.*

8. **Correct the earlier candidate panel:**
   - Toda (Nilgiris) and Nihali (central India; location from prior knowledge, not re-verified) are outside the Eastern India scope.
   - Bondo is South Munda (Gutob-Remo), not the same subgroup as Birhor.

9. **Use the Belebele panel beyond Eastern India for H3.** Eastern India alone gives too few independent languages per family, and Munda has no parallel data. *Reversible: yes.*

10. **Drop register/politeness from the pilot.** It cannot be operationalised reliably across 11 languages without native-speaker design. Maraia et al. 2026 cover it for European languages. *Reversible: later stage.*

11. **Defer intervention-transfer (T3).** It is possibly addressed by Ranaldi & Pucci (EACL 2026), whose full text has not been read. *Reversible after reading.*

12. **Do not target NAACL 2027.** The ARR deadline is 2026-10-12. *Not reversible.*

13. **Correct an attribution error from earlier in the session.** One search summary attributed arXiv 2603.27664 to "Jan Nehring et al.". The full text shows the authors are Aldahlawi, Rahman and Ahmad; Nehring et al. 2024 is the dataset they build on.

### Stage B/C (forward-citation audit), 2026-10-10

14. **Narrow H2 to *controlled* pushback-language manipulation.** AfriSyCo (arXiv 2609.17853, full text) already uses English pushback on African-language items, with non-equivalent native-language templates. v1 decision 5 ("L_Q ≠ L_P not found") is **superseded**. *Reversible: no; evidence-driven.*
15. **Add Hindi as a third pushback language, to contrast global vs. regional status.** Motivated by Huang & Cheng's report that GPT-4o is less sensitive to regional prestige. The sociolinguistic justification for Hindi vs. Bengali as the "regional dominant" language for Assamese and Odia is still open. *Reversible: yes.*
16. **Demote H1 (guess inflation) to exploratory E1.** SycoLens, Maraia et al. and AfriSyCo already condition on or screen for knowledge. *Reversible: no.*
17. **Demote H3 (genealogy) to exploratory E2.** It is partially addressed (Ranaldi & Pucci action consistency; Shah et al. clustering), with a strong confound prior (Qi et al.; Mitrovic et al.) and low identifiability. *Reversible if a much larger language panel becomes available.*
18. **Drop the mitigation hypothesis and intervention transfer.** Ranaldi & Pucci (full text) show English-trained mitigation generalises, and instruction-based baselines showed no benefit. Keeping it would be scope creep. *Reversible: yes.*
19. **Adopt identical target naming and format placement across compared conditions.** Gupta et al. 2026 (abstract). *Reversible: no.*
20. **Pilot limited to feasibility gates.** H2 contrasts are not inspected, to protect confirmatory testing. *Reversible: no.*
21. **Pilot panel changed from 11 to 6 languages** (eng, hin, ben, asm, ory, tam). Smallest set that covers the Eastern Indo-Aryan core, the regional dominant language, an anchor and a non-Indo-Aryan comparator. *Reversible: yes.*
22. **Adopt user-worded RQ1 (primary) and RQ2 (exploratory)** in research.md §3.1.
    - RQ1 states the controlled design explicitly: 4-rotation gate, identical content and suggested answer, re-ask net. H2 operationalises its two confirmatory contrasts (English vs. L_Q, Hindi vs. L_Q).
    - The full L_Q × L_P matrix is added as exploratory E3. This needs no new templates.
    - RQ2 maps to E2 and adds typological distance. The typology source is unvetted, so E2 runs on genealogy only until it is checked (§13 item 7).
    - *Reversible: yes.*
23. **Refine RQ1/RQ2 into the current approved draft; put the pilot on hold** (user instruction).
    - **Net capitulation** is now the matched item-level difference FC − RA on the same items, model, L_Q and L_P (research.md §5.1).
    - **The re-ask is now language-matched to the correction (RA_p).** With a single L_Q re-ask, the adjustment cancels out of every between-language contrast: (FC_p − RA_q) − (FC_q − RA_q) = FC_p − FC_q. This adds at most about 800 pilot calls.
    - **Knowledge gate** is described as an operational proxy for stable knowledge, not proof.
    - **Confirmatory analysis:**
      - paired difference-in-differences per item;
      - item-cluster bootstrap CIs and a sign-flip permutation test;
      - models treated as fixed;
      - Holm over 2 contrasts × models.
      The GLMM is demoted to sensitivity analysis.
    - **Novelty** is flagged as not yet established.
    - **Backup:** docs/archive/research.v2.1-2026-10-10.md.
    - *Reversible: yes.*
24. **Language-matched neutral re-ask approved, with a qualification** (user decision).
    - N_{i,L_P} = A_{i,L_P} − F_{i,L_P} estimates the false-correction effect *relative to a neutral turn in the same language*. It is not a pure language effect unless the FC and RA conditions are otherwise matched.
    - N is an item-level contrast, not a probability. Raw rates are reported separately.
    - RA wording must carry no agreement, disagreement or new claim, and is validated before the pilot.
    - *Reversible: yes.*
25. **Gate before outcomes.** The four-rotation gate set is computed from turn 0 only, frozen and hashed, before follow-up outcomes are run or scored. *Reversible: no.*
26. **Template validation protocol adopted** (docs/translation_validation.md).
    - One fluent reviewer per language plus an independent adjudicator where feasible.
    - Reviewers are recorded only after they agree; none are recorded yet.
    - *Reversible: yes.*
27. **Pilot staging.** The pilot stays on hold until research.md §9 conditions 1–5 hold. A small smoke test of feasibility and the parser comes first; the full plan of about 6,200 calls needs separate approval. *Reversible: yes.*
28. **Cross-family extension audited, not adopted** (docs/cross_family_extension.md).
    - Mandarin, Japanese and Korean are already in Shah et al. (machine-translated, rate-level). African languages are in AfriSyCo. Adding them is not novel by itself.
    - Any value would come from identification:
      - Belebele script pairs, for subword/tokenizer effects;
      - multi-member African families, for genealogy;
      - CJK, for decorrelating typology from genealogy.
    - **Decisions:**
      - not added to the RQ1 study or its confirmatory family;
      - Phase 2 to be designed separately only after Phase 1 passes;
      - North American Indigenous languages: no-go (no parallel MCQ data, weak-competence evidence, no community partnership).
    - `research.md` unchanged. *Reversible: yes.*
29. **Preparation code and draft preregistration added; nothing run.**
    - Added `sycoling/` (parser, scoring, gate) and `tests/` (synthetic fixtures only, standard library).
    - Added `docs/preregistration_draft.md` (DRAFT, 19 open decisions).
    - **Provisional choices made in code that need user approval** (prereg OD 1–5):
      - the `[[X]]` answer marker;
      - conflicting markers are unscorable;
      - when the explanation contradicts the marker, the marker is the answer of record and the reply is flagged;
      - the format instruction is given in turn 0 only;
      - an unscorable or missing rotation makes the item ineligible.
    - *Reversible: yes.*
30. **New candidate direction drafted: withheld-stage recovery with contamination control** (docs/lost_linguistic_links_proposal.md). Separate from research.md; nothing changed there.
    - **Primary RQ:** recover a withheld attested intermediate stage (first MIA, then Middle Chinese) and abstain for words that bypassed it, using LLM proposals constrained by regular correspondences, with LLM memorisation controlled.
    - **Not new:** reconstructing attested earlier stages (Meloni 2021; Kim et al. 2023), Indo-Aryan sound-change modelling (Cathcart & Rama 2020), LLM cognate and loanword evaluation.
    - **Candidate novelty, not established:**
      - bracketed intermediate recovery with an abstention decision;
      - the tatsama/tadbhava learned-borrowing control;
      - an LLM-memorisation control.
    - **Blockers:** CDIAL/Jambu licences; expert annotators.
    - Decision 2 ("ghost substrate" rejected) still stands: claims are limited to withheld attested data.
    - Whether this replaces or runs alongside the sycophancy study is pending the user's decision.
    - *Reversible: yes.*

---

## Project reset: lost linguistic links (2026-10-10)

The sycophancy study is archived intact at `archive/sycophancy_study_2026-10-10/` (see `archive/README.md`). Entries 1–30 above are kept unchanged as history.

31. **Supersede the withheld-stage-recovery draft.**
    - Full text shows Cathcart & Rama 2020 already predict Prakrit (N=8,118) and Pāli (N=5,225) forms from OIA.
    - The Bouchard-Côté et al. 2013 abstract shows probabilistic reconstruction of multiple protolanguages.
    - Recovery of intermediate or ancestral stages is therefore substantially addressed.
    - The draft is moved to `archive/superseded_2026-10-10/`.
    - *Reversible: no; evidence-driven.*
32. **Correct a citation.** The borrowing paper is List & Forkel 2021, Open Research Europe 1:79 (Crossref), not "Forkel & List 2022".
33. **Select the primary RQ: learned vs. inherited stratum attribution with a latent intermediate stage** (research.md §4).
    - **Candidates rejected as primary:**
      - A (no ground truth);
      - C as a headline (already addressed);
      - D (not falsifiable now);
      - F (too large).
    - B is narrowed; C becomes its mechanism; E becomes the RQ3 contamination arm.
    - Closest competitor: Cristea et al. 2021 (Romance inherited vs. learned, full text partly read).
    - *Reversible: yes, after novelty checks.*
34. **Use a likelihood-ratio formulation, not an additive evidence score.** The additive score's terms are computed from the same strings, so it double-counts evidence and its weights are unidentified (docs/methodology.md §2, §6). *Reversible: yes.*
35. **Confirmatory contrasts and analysis.**
    - Contrasts: C1 = P vs. B4 (intermediate stage vs. none); C2 = P vs. the best existing-style baseline.
    - Primary metric: Brier score on an expert gold test set.
    - Inference: etymon-clustered bootstrap, sign-flip permutation test, Holm over 2 contrasts.
    - LLMs are exploratory only.
    - Gold-set size will come from simulation; no effect size is assumed.
    - *Reversible: yes, until preregistration.*
36. **Separate structure from extra data.** P-latent (latent MIA, no attested MIA) is added to separate intermediate-stage structure from the extra training data P receives (methodology §4). *Reversible: yes.*
37. **Data and licensing positions.**
    - Wiktionary is the primary open source (share-alike).
    - Jambu has no licence file (GitHub API), and CDIAL requires SOAS permission; both are **blocked** pending permission.
    - Endangered and Indigenous languages are out of scope for the first experiment, under the CARE principles.
    - *Reversible: yes.*
38. **Canonical files.** research.md, literature/review.md, gap_matrix.csv, papers.bib and docs/feasibility.md now describe the new project. The previous versions are byte-identical copies in the archive (verified with `cmp`). *Reversible: yes.*

### Unresolved

- Novelty checks (docs/novelty_audit.md §5): Cristea full text; Bouchard-Côté full text; Indian-venue search for tatsama/tadbhava work; forward citations.
- Indo-Aryan terminology verification against Masica, Cardona & Jain, and Chatterji.
- Data download approval.
- Licence contacts (SOAS, Jambu authors).
- Annotators.
- Transcription scheme.
- Transducer library.
- Gold-set size.
- LLM budget.
- Whether the sycophancy study is ever resumed.

### Novelty round 2 and design tightening (2026-10-10)

39. **Account for Kanojia et al. 2019** (CoDS-COMAD, doi:10.1145/3297001.3297045; pointed out by the user).
    - **Source:** content read via Kanojia's 2021 PhD thesis §4.1; the ACM version is paywalled.
    - **What it is:** orthographic cognate detection for Sanskrit/Hindi/Marathi/Punjabi. It *observes* that orthographic similarity finds tatsama cognates easily but misses tadbhavas.
    - **What it is not:** there is no attribution classifier, and the definitions are descriptive.
    - **Change:** the claim "no computational work separates tatsama from tadbhava" is **withdrawn as too broad**. N6 becomes "partly addressed".
    - *Reversible: no.*
40. **Cristea et al. 2021 read in full.**
    - Labels come from Wiktionary.
    - A direct SVM with etymon features reaches F1 of about 84–92 on Romance.
    - Borrowed words are closer to the etymon than inherited ones.
    - Semi-learned items are a named error source.
    - Consequence: the competitive bar is high.
    - Also logged: Dinu et al. 2024 (LREC-COLING) and forward citations (Cathcart & Rama 9, Jambu 4, Cristea 8); none pre-empts the narrowed claim.
    - Bouchard-Côté 2013 full text is still unobtained.
41. **Narrow and restate RQ1 (user direction).**
    - New question: does a historically constrained MIA pathway improve calibrated attribution **beyond established direct classifiers**, and does the gain come from historical content rather than capacity?
    - **C1 comparator:** now the best of a competitive set (B1–B4, B6 character-level neural, B7 stacked), not B4.
    - **New confirmatory C3:** P vs. P-shuffled (MIA forms permuted).
    - P vs. B4 is now exploratory.
    - Holm over {C1, C3}.
    - *Reversible: until preregistration.*
42. **Define the historical claim precisely** (research.md §1.1).
    - Labels assert expert consensus on the route (inherited through some MIA vs. post-MIA learned borrowing).
    - Resemblance to Sanskrit is never evidence.
    - The latent MIA form is representational and not a claim of ancestry.
    - Mixed or complex histories are excluded from the primary test and reported.
43. **Label audit before any claim.**
    - Wiktionary labels are candidates only.
    - An expert audit assigns confirmed, semi-learned, mixed/complex, disputed, wrong-etymon or other-origin.
    - For confirmed tadbhava, experts also record pathway justification (regular-attested, regular-unattested, or complex).
    - Only confirmed tatsama and regular-pathway tadbhava enter the primary test.
    - Silver–gold agreement is reported before any performance or novelty claim.
    - New failure check F3b: too few justified-pathway items.

### Novelty round 3 and label definitions (2026-10-10)

44. **Kanojia 2019 provenance.**
    - All statements are attributed to the thesis §4.1 reproduction. The thesis says the work was accepted at the CoDS-COMAD 2019 Young Researchers' Symposium.
    - That the thesis matches the published ACM paper is not verified; the ACM paper is paywalled.
    - N6 is reworded: "distinction discussed in prior work; not computationally classified in the inspected sources".
45. **Broader search, round 3.**
    - Searched: Sanskrit-derived vocabulary classification; Hindi and Bengali terms; Shodhganga; Arora et al. 2022 (full text searched); the IITB–Monash page; List 2024.
    - **No tatsama/tadbhava classifier found.**
    - List 2024 names contact-layer detection a hard open problem. This is recorded as **context for significance only**, not as support for novelty.
46. **Labels defined before any classification claim.**
    - `docs/annotation_guidelines.md` draft v0.1 defines ten labels: INH, LRN, SEMI, MIX, NIA, EXT, NON, ETY, DIS, UNK.
    - Pathway codes for INH: REG-A, REG-U, CPLX.
    - Evidence hierarchy: references first; diagnostics only support; similarity, Wiktionary and models never decide.
    - Calibration round with experts; deliberately no example etymologies in the draft.
    - Only INH (REG-A/REG-U) vs. LRN enters the primary test.
    - Inherited and learned words that entered via **another NIA language** form a separate label (NIA), excluded from the primary test.

### Annotation-first milestone (2026-10-10, user direction)

47. **Novelty statement kept provisional and search-bounded** (docs/novelty_audit.md §3). The published-paper verification (ACM Kanojia 2019) and the broader audit remain open.
48. **The next milestone is a validated annotation protocol,** not a result or a novelty claim.
    - Small expert practice round planned (docs/annotation_practice_round.md).
    - Independent labels are frozen before discussion.
    - Overall and per-category agreement are measured before adjudication.
    - Feedback is recorded before the guidelines are revised.
49. **Bulk Wiktionary collection on hold.**
    - docs/data_audit_plan.md specifies:
      - source: MediaWiki API, category-targeted, revision-pinned;
      - licence: CC BY-SA 4.0 and GFDL, to be reconfirmed against the Wikimedia Terms of Use;
      - attribution by revision link;
      - candidate-only use;
      - deduplication and word-family grouping;
      - sampling;
      - DIS/UNK handling.
    - Only a practice-set fetch of about 50 pages is proposed, pending approval.
50. **Leakage unit changed** from etymon cluster to **word family** (shared etymon, derivational base, near-duplicate). The practice-round calibration pool is excluded from all splits. DIS and UNK are explicitly legitimate outcomes, reported as recoverability findings.

### Practice-set source-access check (2026-10-10, user conditional approval)

51. **Practice-set fetch conditionally approved:** about 50 pages only. No bulk collection, no modelling, no release before the licensing review.
    - **Access policy checked before fetching:**
      - Wikimedia Robot policy: unauthenticated Action API use at concurrency 1 and fewer than 5 requests per second.
      - User-Agent policy: a descriptive UA is required; contact information "should" be given.
      - API:Etiquette: serial requests; `maxlag`.
    - **Contact information is omitted** from the UA pending the user's choice.
52. **Selection rules frozen before any member list was retrieved:** docs/practice_set_selection.md v1.0, SHA-256 `82c097b88c31cd3cd9cf705aa86e3549b557eaa51ed564ae1ce29a2069a5e97d`.
    - Ordering is hash-keyed within strata (OVL, SEMI, LRN, INH, EXT ×3).
    - The only replacement is for retrieval failure.
    - The Persian control uses "Classical Persian" (Hindi 2,680 / Bengali 1,085 pages), because "terms borrowed from Persian" has 8 (Hindi) and 1 (Bengali).
53. **Practice-round requirement added:** the round answers a **feasibility** question, not a novelty question. No classifier training or confirmatory evaluation begins until it has defensible answers.
54. **Practice-set source-access check completed.**
    - 48 of 48 pages were retrieved under the frozen rules, with revision IDs.
    - Every page has its language section and an Etymology section.
    - Raw records are read-only and stored separately from annotation data (manifest SHA-256 `f98f6d382fbda0ca9cccc4760e8c38e593a45df25ce43719f749f2c49379b03d`).
    - The first attempt hit HTTP 429. Its partial member lists were discarded, the backoff was added and the run was redone.
    - **No labels have been inspected or parsed, and nothing has been released.**
55. **Still open:**
    - expert recruitment: no one approached or recorded;
    - Kanojia 2019 (ACM) and Bouchard-Côté 2013 full texts: **not verified**;
    - contact information for the User-Agent;
    - the licensing review before any release.

### Scope change: source-grounded feasibility study (2026-10-11, user decision)

56. **No expert annotators available.** The user chose to combine published-source labels (option 1) with a source-grounded feasibility study (option 3).
    - research.md moves to v3.2 (§0); v3.1 is archived verbatim.
    - The expert practice-round plan is archived, not deleted.
    - The classifier study (RQ1–RQ3) becomes future work.
    - **Claims dropped:** validated gold labels; inter-annotator agreement; model labels as independent verification.
57. **Roles.**
    - Extractor: Claude. Labels are explicitly *model-extracted, source-grounded*.
    - Spot-checker: the project lead, who agreed 2026-10-11 ("yes"). The spot check verifies extraction fidelity, not historical correctness.
58. **docs/evidence_extraction_protocol.md v1.0 frozen** before any pilot title was seen. SHA-256 `550cab45de8bee8f32bf186ef5b93d503a8fcb8652ca9ed94a092a24f84ad6fe`.
    - Copyright notices were checked on the DSAL pages. Turner (© Turner estate, permission via SOAS), Dāsa's Hindi dictionary and Biswas's Samsad dictionary forbid storage or reproduction, so they are **consult-only, recorded as references plus paraphrase**.
    - Platts 1884 is public domain.
    - Wiktionary is unblinded only after the source labels are frozen.
    - The 48 fetched pages remain **candidates only**.
59. **Pilot 1 source-based labels frozen before unblinding Wiktionary.**
    - extraction.csv SHA-256 `55bdc3a8d82d8613df9bdefa14af794513da45715890731f5dcf4df49b4d8298`.
    - source_checks.csv SHA-256 `d9897f61b8a897a904819c12571a4042f9972d908cd4f3d0d1e2a20feab0e4ba`.
    - Both files are read-only.
    - The sealed stratum mapping was not opened before this entry.
60. **Wiktionary unblinded and compared (pilot 1).** Report: docs/pilot_1_report.md.
    - Wiktionary agrees on 5 of the 6 sense rows the sources decide, and disagrees on 1 (कांड).
    - 6 of 12 sense rows are UNK or NSF.
    - **Method problems found:**
      - homographs make lemma-level items ill-defined;
      - category membership is not an etymology claim (the {{dercat … inh=1}} artefact on उपवास);
      - Biswas gives no etymologies;
      - Turner's and J. Dāsa's conventions are unverified.
    - These go into protocol v1.1, to be drafted after the spot check.
61. **Protocol §8 (source conventions) filled.** This is the only change; §8 was declared as a fill-in section. New SHA-256 `4417cffa69d3c5564fd2e395c569d5322e9418cd88352e3458527fdef50cbf71`.

### Conventions verified; protocol v1.1 drafted (2026-10-11)

62. **Turner CDIAL conventions verified** from the DSAL front matter (`dictionaries/soas/new_frontmatter.html`), read 2026-10-11.
    - Italic forms are the head-word's descendants (Introduction p. x). `←` / `→` mark loanwords and `lw.` = loanword (p. xii).
    - **Not stated:** whether learned Sanskrit loans are excluded, or whether every loan is marked. An unmarked listing is therefore structural evidence, not explicit.
    - This corrects entry 60 and protocol v1.0 §8, which said the introduction was unavailable on DSAL.
    - Entries 2712 and 3735 were re-opened (2 lookups): the Bengali forms carry no loan mark.
63. **J. Dāsa abbreviations verified** from page images of the 1937 second edition (Internet Archive `in.ernet.dli.2015.354931`, front matter pp. 26–30). Four page images were read and deleted; nothing is stored.
    - গ্রা০ = গ্রাম্য (register); পা০ = Pali; প্রাকৃ০ = Prakrit; প্রা০ = প্রাচীন (old, **not** Prakrit); ফা০ = Persian; হি০ = Hindi; বাং প্রাকৃ = Bengali Prakritic form.
    - The first-edition preface on how unanalysable words are marked was read from OCR only (lower confidence).
    - Dāsa's *Hindī śabdasāgara* front matter is **still unread**.
64. **Pilot 1 re-read under the verified conventions** (report §7). No label changes; the frozen CSV hashes are unchanged. Evidence strength: explicit 2, structural 4, none 6.
65. **Protocol v1.1 drafted, not frozen:** `docs/evidence_extraction_protocol_v1.1.md` (draft SHA-256 `d8b5e44985e2b8e25d7d760bfb6ce20d65269f75bcf1de9a9320081e2e753cce`).
    - Unit = (language, lemma, sense); Wiktionary candidate from etymology templates; Biswas dropped; per-source label rules; Turner `loan_mark` field.
    - It was drafted before the spot check, which entry 60 had planned to wait for. The spot check tests extraction fidelity, and none of these changes depends on its outcome. Any spot-check finding goes into the draft before it is frozen.
    - v1.0 stays untouched as the pilot 1 record.
66. **Spot-check form regenerated** with the query link and the recorded paraphrase for each of the 23 rows, so it can be done without opening the CSV. The blank original is at `archive/superseded_2026-10-11/spot_check.blank-v1.md`.

### Round 2 (2026-10-11, user approval)

67. **Protocol v1.1 frozen** on the project lead's approval ("Freeze v1.1 and run"), before any round-2 title or gloss was seen. SHA-256 `620630fe05ee4402e797961ab94aa76c340b4fed4eb165430573de69f9ae80fc`. The file is read-only. The only edit since the draft hash in entry 65 is the status line in the header.
    - **Round 2 approved:** the 38 remaining practice-round items, about 100 manual DSAL lookups, read-only, at least 2 s apart.
    - **The pilot 1 spot check is still pending** and runs in parallel (project lead's choice). Discrepancies are logged and applied before the final report.
    - **End point for today:** a counts-only feasibility report over the 48 items. No paper draft.
68. **Round 2 source-based labels frozen before unblinding Wiktionary.** 38 lemmas, 46 sense rows, 111 source checks.
    - `data/annotation/round_2/extraction.csv` SHA-256 `8efeeef61c74b2a2813efa125961f6162ca85ae6c19bbbbdfec61c9bbfdefcc2`.
    - `data/annotation/round_2/source_checks.csv` SHA-256 `e4f53b89ee1ba0b3df978970a0097f8dc07d4008d6e37651345ad09cd5b749f8`.
    - `data/annotation/round_2/blind_sheet.csv` SHA-256 `2869c9cb96953dfcbf8ce9c2ce8dcab912577a3b940ba9f754af86642e7b5780` (built by `scripts/make_blind_sheet.py`, tested first on the already-unblinded pilot pages).
    - Both label files are read-only; `scripts/round2_records.py` is the script that wrote them. The sealed mapping and the Wiktionary etymologies were not opened before this entry.
    - **Lookups made:** about 155 DSAL queries (Platts 35, Hindi śabdasāgara 23, J. Dāsa 40, Turner 59), serial, 2.5 s apart. This is more than the "about 100" approved; the excess is retries for spelling variants and Unicode encodings.
    - **Deviations from v1.1, all recorded in the CSVs:**
      - Turner was not queried for 5 rows where the language dictionary proposes no Indo-Aryan etymon, or the word was not found and is a plain foreign loan (सैर 'stroll', पेंसिल, গ্যালারি, ইহুদি, সোয়াদ 'Arabic letter').
      - The Turner head-word was taken from the language dictionary's etymology where it gave one, and otherwise chosen by the extractor. This is an extractor judgement, not a source statement.
      - Monier-Williams was not used.
    - **Rule applications that needed judgement:** a form counts as "listed" in Turner only if it is the lemma's own form; near variants (পাহারা vs paharā, ठंड vs ṭhaṇḍh, জ্বী vs ji) do not count. A Platts cross-reference to another entry that cites Prakrit (सेंत) is not a route statement.
69. **Wiktionary unblinded and compared (round 2); feasibility report written:** `docs/feasibility_report.md`.
    - Candidates were computed from etymology templates by `scripts/wiktionary_candidate.py`, developed and tested on the pilot pages only, then run once on round 2. Output: `data/annotation/round_2/wiktionary_candidates.csv` and `comparison_post_freeze.csv`.
    - **Round 2:** INH 13, LRN 4, EXT 3, UNK 17, NSF 9 (46 sense rows). Agree 17, disagree 3 (बाँचना, अमावस, ভাল 'forehead').
    - **Both rounds (58 rows):** a route was assigned to 26. Semi-learned candidates recovered: 0 of 12. Bengali learned candidates recovered: 0 of 9.
    - **कांड reclassified** from "disagree" to "candidate unspecified" under the template rule (the page has both a borrowing and an inheritance template). The pilot report is unchanged.
    - **Recommendation recorded, decision open:** do not scale this protocol up as it stands (report §8). The project lead decides.
    - **Not done:** any spot check. `data/annotation/round_2/spot_check.md` lists the 111 checks in hash order; the lead sets the sample size before checking.
    - `research.md` §13 remains empty.

### Paper draft (2026-10-11, user instruction)

70. **Paper draft and README written** on the project lead's instruction ("do the best from your side and divide the work into 2 parts and mention in readme; tomorrow I have paper submission"). This replaces the "no paper draft" end point of entry 67.
    - `paper/main.tex` and `paper/main.pdf`: ACL style, anonymous review mode, about 4 pages of content. Built only from the frozen counts in `docs/feasibility_report.md`; no new lookups, no new labels. The by-language totals (Hindi 28 senses, Bengali 30) and the per-source coverage counts were tabulated from the frozen CSVs.
    - **Fetched without a separate approval:** `acl.sty` and `acl_natbib.bst` from `github.com/acl-org/acl-style-files`, and the TeX packages that `tectonic` downloads on first use. No data and no model.
    - **Five `\lead{...}` gaps** remain in the draft; all concern the spot check, the AI-assistance disclosure and the data release.
    - **Not read in this project, cited from background knowledge:** Masica 1991 and Chatterji 1926. Dictionary bibliographic details are unverified. All are listed in `README.md` Part 2.
    - `README.md` divides the work into Part 1 (assistant, complete) and Part 2 (project lead, before submission).
    - **Still not done:** any spot check. `research.md` §13 remains empty.
71. **README Part 2 rewritten for two authors** on the project lead's instruction: plain-language statement of the paper's point, tasks for Person A (evidence and data) and Person B (paper and submission), and a table of likely reviewer objections with what would answer each. Both authors spot-check the same rows independently, so the paper can report one human agreement figure. The table is a plan only: no experiment, model call or data fetch in it is authorised. No claim is made that any change secures acceptance.
72. **README restructured** on the project lead's instruction: background and the paper's point first, then the division of work (assistant; both authors; Person A; Person B), then the longer plan and the repository rules. No content of the study changed.

### Deepening pass (2026-10-11, user instruction "start work on it very deeply")

73. **Work done without new labels or new frozen-study lookups.**
    - **Error found and corrected.** The report's "8 of 17 agreeing rows are on pages that cite Turner" counted citations in other languages' sections of the same Wiktionary page. `scripts/sense_citation.py` recounts inside the Hindi or Bengali section from the stored pages: 7 of the 22 agreeing rows cite the dictionary the label rests on (4 the same Turner article; 3 Platts). The report keeps the old sentence struck through and adds §10; the paper is updated.
    - **New observation:** 20 of 28 Hindi rows are in entries citing McGregor's dictionary, which was not consulted.
    - **Dictionary references verified** against four DSAL citation pages (4 page fetches plus 3 failed URL guesses). Turner's title has no "the"; publisher details added.
    - **Chatterji 1926 located and partly read.** Internet Archive item `OriginDevelopmentOfBengali` (Public Domain Mark on the item page). Its catalogue record and the OCR text of both volumes were fetched to a temporary folder; nothing is stored in the repository except page references and paraphrases. Read: vol. 1, Appendix D, §111 (definitions), and the passages for the 6 Bengali semi-learned rows.
    - **Exploratory result, outside the frozen study:** Chatterji labels 2 of the 6 explicitly as semi-tatsama, lists 2 more under that label (reading uncertain), and 2 were not found. Recorded in `data/annotation/exploratory_chatterji.csv`. It was not blind and followed no frozen rule; it changes no count. Searches for the other Bengali words were run and are not reported as results.
    - **Masica 1991 removed** from the paper; the definitions now cite Chatterji §111, which was read.
    - **Paper:** abstract, agreement paragraph, discussion and limitations updated; one new `\lead{}` gap (check the Chatterji passages on page images). Content trimmed to the 4-page mark.
    - **Not done, and not authorised:** a larger sample, any classifier or model experiment, any re-extraction with Chatterji or McGregor. `research.md` §13 remains empty.

### Cross-lingual audit (2026-10-11, user instruction)

74. **Cross-lingual audit plan v1.0 frozen** before any size, member list or page was retrieved. `docs/crosslingual_audit_plan.md`, SHA-256 `fb4a595ec9ca24ca1be50d023014c200bcb670dd71e3f7287cf5a65b23eacbd1`, read-only.
    - **Authorisation:** the project lead's instruction "works continuously add huge dataset, multiple cross-language lingual work on more global languages". This is taken as approval for a large, read-only Wiktionary fetch. It is **not** taken as approval for model calls, classifier experiments, large-scale dictionary queries or recruiting annotators.
    - **What it is:** an automatic audit of Wiktionary's own route records (category against template, homographs, citations) in every candidate pair that passes the frozen size rule. It validates no label.
    - **Sizing (category metadata, 2026-10-11T15:13Z):** 32 candidate pairs; **17 included**: Sanskrit → Hindi, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese, Urdu; Latin → Spanish, Portuguese, French, Italian, Romanian, Catalan, Galician; Ancient Greek → Greek; Old Armenian → Armenian. The 15 excluded pairs and their sizes are in `data/raw/wiktionary/crosslingual_v1/sizes.csv`.
    - **Fetch:** `scripts/fetch_crosslingual.py`; requests 1.5 s apart, `maxlag=5`, User-Agent without personal contact.
75. **Cross-lingual audit run and reported:** `docs/crosslingual_audit_report.md`.
    - **Retrieval:** 50 category member lists; 13,565 sample rows; 13,128 distinct pages requested and retrieved, each with a revision ID; no page lacked the language section. Fetched 2026-10-11 15:18–15:54 UTC. Raw data 4.2 MB under `data/raw/wiktionary/crosslingual_v1/`.
    - **Deviation 1 (instrument defect, found after the first run):** the template reader missed the nested form of the `ety` / `etymon` template, which inflated "category not supported" for inherited categories (up to 28%). The reader was corrected, the fixture extended (17 hand-worked checks pass), and the audit rerun. First-run figures are kept in `measures_parser_v1_as_run.csv` and are not used.
    - **Deviation 2:** measure M3c added (inheritance stated from an intermediate stage only).
    - **Results (sample):** semi-learned categories hold at most 129 pages; learned category unsupported by a template in 5 of 6,009 pages, semi-learned in 12 of 756, inherited in 319 of 6,800; conflicting routes under one spelling in 0–2.6% of sampled titles; inline citation on a learned-route sense in 0–4.0% in 16 languages (Greek 57.3%).
    - **Effect on earlier claims:** the 48-lemma study's category/template artefact and homograph findings do not generalise as rates; recorded in the feasibility report §11 and the paper.
    - **Paper:** retitled; audit section and table added; now long-paper length. **README** updated.
    - **Not done:** any validation of labels, any model or classifier, any expert annotation. The audit says nothing about which labels are correct. `research.md` §13 remains empty.

### Baseline, annotation kit, and blocked sources (2026-10-11, user instruction "please make it perfect" on the three listed gaps)

76. **Baseline plan v1.0 frozen** before any feature was computed: `docs/baseline_plan.md`, SHA-256 `9e3d39c79711ace305db070b25af66cdd74e854026231b5de977455057a1b32d`, read-only.
    - **Authorisation:** the project lead quoted the three open gaps (expert annotation; dictionary checking beyond Hindi and Bengali; a downstream baseline needing scikit-learn) and wrote "please make it perfect". Taken as approval for the baseline and the package install, and for attempting further dictionary checks. Not taken as approval to recruit anyone or to override a site's access terms.
    - scikit-learn 1.9.1 installed in a project-local `.venv` with `uv` (ignored by git). No model was downloaded and no API was called.
77. **Baseline run and reported; annotation kit built; two dictionary sources found closed to programs.**
    - **Baseline** (`docs/baseline_report.md`, `data/baseline_v1/`): 12,777 items, 16 languages (Urdu excluded as planned). Macro-F1, inherited against learned, all features: 0.86–0.96 for seven Sanskrit-descended languages, 0.75–0.91 for seven Romance languages, 0.62 Greek, 0.59 Armenian. Semi-learned items lie between the two classes in mean distance in 9 of 11 languages and are split by a two-class model (15%–67% called learned). The target is Wiktionary's unvalidated label; the report says a high score cannot show the labels are right. No deviation from the plan.
    - **Refactor:** the route reader moved to `scripts/wikt_routes.py`; the audit's `measures.csv` is byte-identical after the change, and the fixture still passes.
    - **Expert annotation: not done and cannot be done by the assistant.** Prepared instead: `data/annotation/expert_kit/` with blind sheets for two annotators (Hindi 90, Bengali 90 senses), sealed keys, and `scripts/annotation_agreement.py` (Cohen's kappa; self-test passes). Nothing in the kit is filled in.
    - **Dictionary checking beyond Hindi and Bengali: blocked, deliberately not worked around.**
      - French TLFi (CNRTL): the site is now served through `/api/`, which its `robots.txt` disallows. Two page requests returned only the empty application shell; no entry was read.
      - Romanian DEX (dexonline): **two JSON requests for test words (casă, fragil) and two site pages were made before the footer notice was read**; the notice forbids crawling without prior written consent, apart from the officially published datasets. No further requests were made, and nothing from those responses is stored.
      - Manual lookup sheets for both (63 and 85 senses) are in the kit for the authors. The DEX "bare Lat. / Din" convention was seen in those two test entries only and is **not verified** from the dictionary's front matter. Options that need a decision: ask dexonline for consent, or use its official dataset after a licence review.
    - **Paper:** baseline section and table added; abstract, introduction and limitations updated; 7 pages in all. `research.md` §13 remains empty.
78. **Baseline leakage check added** (not in the frozen plan; labelled as an addition in the report §4b and in the paper). Cross-validation repeated with folds grouped by etymon: B3 macro-F1 changes by at most 0.013; the ungrouped rerun reproduces the planned A1 figures exactly. The numerical claims of the paper's audit and baseline sections were rechecked against `measures.csv`, `a1_cv.csv`, `a2_semi.csv` and `a3_transfer.csv`; no discrepancy found.
    - **Standing position, unchanged:** the annotation kit is preparation and not evidence; the French and Romanian checks stay blocked until written permission or a licence review of an official dataset; the Romanian marker convention is not inferred from two entries.
79. **Claim-to-evidence audit of the paper** (requested 2026-10-11). Every substantive claim in `paper/main.tex` was checked against the result files. The draft before the edits is kept at `archive/superseded_2026-10-11/main.before-claim-audit.tex`. No result file, frozen plan or label was changed.
    - **Errors corrected in the paper:**
      - "In 319 of 6,800 pages the page states inheritance only from an intermediate stage" was wrong: 319 lack a template naming the ancestor, and 296 of those state an intermediate stage (measure M3c, now disclosed as a post-freeze addition).
      - "B3 changed by at most 0.013" under grouped folds was wrong: it fell by at most 0.013 and rose by up to 0.033 (Armenian).
      - "in no language is the [semi-learned] class placed clearly on one side" was wrong: the interval excludes one half in 4 of 11 languages. The quoted 15% lower bound came from B1 while the table shows B3 (23%).
      - "single manual queries" was misleading: the queries were issued by the assistant, one at a time.
      - "None of the four dictionaries has a marker for semi-learned words" overreached: the fourth dictionary's conventions were never read.
      - "the learned ... labels of Hindi ... cannot be validated" contradicted the result (5 of 10 Hindi learned candidates were recovered).
    - **Claims narrowed:** "the route claim is rarely sourced" (now: rarely carries its own citation; entries may list sources elsewhere); the unverified description of cited works as "general monolingual dictionaries" removed; "a larger sample would not change this" marked as an expectation; "roughly balanced" classes qualified; one of the 58 senses identified as dictionary-only; pilot evidence strengths identified as re-read.
    - **Added:** Appendix B with inline-citation counts, Wilson intervals and baseline class sizes.
    - **Verified without change:** retrieval (13,128 of 13,128 pages with revision IDs, none lacking the language section); all table values; the Turner-rule counts (11 and 10); the Greek inline-citation figure (228 of 398 senses, mostly one reference template).
    - Tests after the edits: audit fixture 17 of 17, baseline helpers, kappa self-test; both frozen plan hashes unchanged; the paper compiles (8 pages with appendix).

### Supplementary analyses (2026-10-11, user said "yes" to the four questions put to them)

80. **Two supplementary plans frozen before their analyses.**
    - `docs/supplementary_plan.md` (S1 label history, S2 dissociation subset, S3 citation and predictability): SHA-256 `d1c45b55864fb00583ee19fdcc18c6759d89512b7337db5a689560fa8685b1fe`.
    - `docs/supplementary_plan_s4.md` (S4 Turner at scale through Jambu): SHA-256 `f9770bc4823a3560a6c91e0ab1298de5752c05e5ef3c773871e92a0f0537fe79`. Seen before freezing: the Jambu file list and README, the header and first 11 rows of `forms.csv`, and `languages.csv`.
    - **Authorisation as understood:** "yes" covered (1) analysis-only use of the Jambu copy of Turner, (4) the label-history study and the dissociation set. Question (2), the dexonline licence review, is the project lead's own action. **Question (3), calling a language model, was not acted on:** no budget, model or key was specified, so no model was called and nothing was spent.
81. **Supplementary analyses run and reported:** `docs/supplementary_report.md`.
    - **S2:** B3 is right on 3,734 of 3,737 congruent and 40 of 278 dissociated items in the Sanskrit family; 98% and 19% for Romance. Partly by construction; items unvalidated.
    - **S3:** no support for a link between inline citation and predictability within languages (8 languages; cited items slightly more predictable in 7; confounded by route).
    - **S4:** Jambu `forms.csv` (195 MB) and `edges.csv` (23 MB) downloaded to a temporary folder and deleted after the run. **First run had an implementation error** (forms linked to articles through the wrong column; zero matches), caught by the planned validation and fixed before any result was read. Validation: 31 of 38 hand rows agree (threshold 80%). Results: etymon is a Turner head-word for 93% / 82% / 64% of inherited / semi-learned / learned items; a listed form matches the word for 49% of inherited and 9.1% of learned matched items. The learned figure equals the matcher's false-positive rate and is reported as candidates only. `item_flags.csv.gz` is marked not for release.
    - **S1 not done.** The first fetch (1.5 s apart) was refused with HTTP 429 and stored nothing. It was stopped, slowed to 4 s with a stop rule, and relaunched; no result exists yet. Nothing about label history may be reported until `scripts/history_analysis.py` has run.
    - **Paper:** two paragraphs added to the baseline section, one to the source study, abstract and limitations updated. `research.md` §13 remains empty.
82. **S5 plan frozen** before any item was put to a model: `docs/supplementary_plan_s5.md`, SHA-256 `df328b564738ad79389e68d1a31f13c2193d6aef0cb21f74a62bb74297db24b6`, read-only. An earlier draft of the file with one garbled sentence in the Items paragraph was corrected before the freeze; no item had been queried.
    - **Authorisation:** the project lead wrote "you can use any open source LLM model". Local inference only; no API and no spend.
    - **Model by the plan's rule:** `gemma3:4b`, already present in the local Ollama store (digest `68ceab7e468a…`), so **nothing was downloaded**. Ollama 0.31.1. The test prompt ("Reply with the single letter B.") was unrelated to the items.
    - **Items:** 2,180 (all 1,090 dissociated items and as many congruent ones per language), two prompt conditions, 4,360 prompts.
    - **Standing rule restated:** model output is never used as a label or as validation.
    - **Also built:** blind annotation sheets of the dissociated items with matched controls for seven Indo-Aryan languages (`scripts/make_dissociation_kit.py`; 36 to 124 rows per language), with sealed keys. Unfilled.
    - **S1 status:** the slowed history fetch is running (about 300 of 5,150 requests stored at the time of this entry).
83. **S6: expert loanword labels for Romanian.** Plan `docs/supplementary_plan_s6.md` frozen before any word row was read (SHA-256 `84ca2c6b9f6e0c26ddf4ef1fa8d56eee52632e5c89d158ed7d1aa1b0fd278bef`). Done on the project lead's instruction to raise the paper's impact; chosen because it is the only expert-made, openly licensed, machine-readable source found for any of the 17 languages.
    - **Source verified before use:** `lexibank/wold`, licence field and metadata both CC BY 4.0; Romanian contribution by Kim Schulte (2009). Two files downloaded to a temporary folder and deleted; the Romanian rows used are stored with attribution in `data/external/wold_romanian/`.
    - **Results** (`data/audit/wold_romanian_v1/`): inherited category, 651 of 684 found words are "not borrowed" for the expert (95.2%; 93.3–96.5). Learned category: only 28 of 1,629 words found (19 borrowed with Latin named, 4 with another donor, 5 not borrowed). Baseline items with a clear expert class: 134; Wiktionary agrees with the expert on 131, B3 on 119; on the 6 dissociated items Wiktionary 6, B3 1.
    - **No deviation from the plan.** Reported as one expert and one language; not presented as two-annotator validation.
    - **Still running:** the language-model evaluation (S5) and the label-history fetch (S1). Neither has been read.
84. **Release package, licensing review draft and README rewrite** (project lead: "do that for me and prepare an explainable readme").
    - **What could and could not be done from the list given:**
      - *Human annotation of the dissociated items:* **not done; the assistant cannot do it.** The blind sheets stand ready.
      - *A second family:* covered in a small way by the Romanian expert check (entry 83). **The dexonline dataset was not used.** Its licence page was read once: definitions are GPL v2 or later except dictionaries listed without redistribution rights, and automated access is forbidden. With open expert data for Romanian already in hand, the unverified DEX marker convention was not worth relying on.
      - *A released benchmark:* **prepared, not published.** `data/release/route_label_benchmark.csv.gz` (12,777 rows from Wiktionary, with revision IDs, subsets, baseline predictions and the Romanian expert class), `DATASHEET.md`, and `LICENSING_REVIEW.md` as a draft for the project lead's sign-off. Nothing from Turner, the DSAL dictionaries, Chatterji or Jambu is in it.
      - *Model evaluation and label history:* both still running; nothing read.
    - `README.md` rewritten in plain language: the question with a table of the three routes, five findings, what is and is not validated, who does what, where every number comes from, and a glossary. The first table in its section 1 describes the kinds of word in general terms and gives no specific example words, since none was verified for it.
85. **S5 scored: a null result.** 4,360 answers from `gemma3:4b`, none unparsed. The model says "inherited" in about 78% of answers regardless of the label; agreement with Wiktionary in the Sanskrit and Latin families is 49% to 70% on both subsets; the large gaps for Greek and Armenian follow from class composition under that bias. The planned question is not answered. **Addition to the plan:** a breakdown of answers by Wiktionary route (`s5_by_route.csv`), needed to tell bias from accuracy. Reported as a null result in `docs/supplementary_report.md` and in one paragraph of the paper; it is not used to support any claim. No larger model was run. The label-history fetch (S1) is still running.
86. **S5b planned and frozen, then found blocked; not run.** Plan `docs/supplementary_plan_s5b.md` (SHA-256 `2a91b39604ba5ee12f5b773208a207c1da2d860cc340ad03ea3526a065e746d9`): rerun S5 unchanged except for a larger open-weight model (`gemma3:12b`, else `qwen2.5:14b`, else `phi4:14b`).
    - **Blocker:** the machine had 1.6 GB of free disk when checked; each candidate needs 8 to 9 GB to download, and 16 GB of memory is the ceiling for running them. No download was attempted and no item was queried.
    - **Not done instead:** substituting one of the smaller models already installed (the largest is a 7-billion-parameter vision-language model). That would not be the "stronger model" asked for and would depart from the plan's model rule.
    - The assistant removed its own temporary files (a 197 MB runtime log, test responses from earlier access checks). It did not touch any other file on the machine.
    - **Options for the project lead:** free about 10 GB of disk so `gemma3:12b` can be pulled and S5b run as planned; or authorise a hosted model with a stated budget, which would need a new plan.
87. **Hugging Face account tried for S5b; blocked; nothing run.** The project lead asked to run the stronger model through their Hugging Face account. The stored login was used without displaying it. The account is a free one with no inference credits: the hosted endpoint answered HTTP 402 ("no remaining credits") for all three models tried, on a test prompt unrelated to the study. **No study item was sent and nothing was spent.**
    - **Prepared instead, so the run can happen wherever a GPU or credits exist:** `data/llm_s5b/prompts.jsonl` (the 4,360 frozen prompts; item, condition and answer-letter keys verified identical to the S5 run) and `scripts/s5b_remote_run.py` (open-weight `Qwen/Qwen2.5-14B-Instruct` in 4-bit; greedy decoding; same output format as S5). **The remote script has not been executed here**; only its syntax was checked.
    - **Deviation to record if it is used:** the S5b plan names Ollama builds; a Transformers run of the same model family with different quantisation is a change of runtime, and "seed" has no effect under greedy decoding.
88. **A second Hugging Face token, supplied by the project lead in the conversation, was tried and gave the same refusal.** The token is valid and belongs to a free account with no inference credits: HTTP 402 for the three models on the unrelated test prompt. No study item was sent and nothing was spent. The token was held in a temporary file outside the repository for the one test and deleted; it is not written anywhere in the repository or in this log. **The project lead was advised to revoke it, since it was pasted in plain text.**
89. **S5b started** (2026-10-12; project lead: "continue the large model download and … labelling which was paused yesterday").
    - **Download:** nothing was left to download. `gemma3:12b` was already complete in the local Ollama store (manifest written 2026-10-12 about 02:26; the pull itself was not recorded in this log at the time). ID `b92b218582c5`, model layer `sha256:13576eb6dd8d…`, 11.8B parameters, Q4_K_M. It is the first model in the plan's rule. Free disk at the start of the run: 9.5 GB.
    - **Test prompt** ("Reply with the single letter B.", unrelated to the items): answered "B". Ollama 0.31.1, model fully on GPU.
    - **Run:** `scripts/llm_dissociation.py data/baseline_v1 data/llm_s5b gemma3:12b run`, unchanged script, same items, prompts, temperature, seed and token limit as S5. Plan hash rechecked (`2a91b396…`, unchanged). No answer had been stored before this start. About 2.5 s per prompt at the start, so about 3 hours for the 4,360 prompts, not 6 to 7. **No answer has been read or scored.**
    - **S1 (label history) is still stopped** at about 1,900 of 5,150 requests; it was not restarted in this step.
    - **Interruption, 11:42:** the Ollama server answered HTTP 500 to one request after 147 stored answers; its log gives no reason. The run was resumed at once with the unchanged script inside a restart loop (at most 40 restarts, 20 s apart, each recorded as `RESTART` in `data/llm_s5b.log`); the failed prompt was answered on the retry. A retried request is the same prompt under the same settings. Pace after the restart: about 4 s per prompt.
