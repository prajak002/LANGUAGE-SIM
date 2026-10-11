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
