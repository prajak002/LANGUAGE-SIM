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
