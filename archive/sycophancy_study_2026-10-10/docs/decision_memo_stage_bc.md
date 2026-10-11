# Decision memo: Stage B/C (forward-citation audit)

_Date: 2026-10-10. Scope: novelty of H2 and H3, recommendation on a pilot. No experiments run._

## 1. Strongest defensible research question

> Holding the question language and the pushback content fixed, does changing only the language of a false correction (the user's language, English, or Hindi) change how often a model abandons an answer it demonstrably knows? Does the English-versus-Hindi contrast show whether deference tracks global or regional language status?

- **Confirmatory:** H2, with two planned contrasts.
- **Exploratory:** E1 (gated vs. naive flip rate) and E2 (genealogy vs. item-level concordance, with subword-overlap control).

> **Superseded wording (2026-10-10):** the final RQ1/RQ2 text is in research.md §3.1 (decision log 22). The substance is unchanged.

## 2. Is H2 already directly tested?

**Answer: partially. The uncontrolled version exists; the controlled version was not found in the sources searched.**

| Evidence | What it shows | Effect on novelty |
|---|---|---|
| AfriSyCo (arXiv 2609.17853, full text) | Factual MCQ in 6 African languages; follow-up pushback in **English** in the factorial; a native-language layer with different templates; turn-1 correctness plus one rotation subset; neutral re-ask in the native layer. Same-content English vs. native comparison not done; post-hoc +2.4 pp, CI [−0.02, 4.92], "not an equivalence test" | **Against**: L_Q ≠ L_P is not new. **For**: the controlled contrast is explicitly left open |
| Huang & Cheng 2026 (full text) | Language prestige hierarchy in GPT-4o persuasion role-play (India: en > hi > bn > ta/te); monolingual dialogues; weaker regional prestige | **Against**: status effects in LLMs are known. **For**: no factual, assistant or manipulated-L_P test; motivates the English-vs-Hindi contrast |
| Shah et al. 2026; Aldahlawi et al. 2026 (full text) | Monolingual prompts per language | Neutral |
| Ranaldi & Pucci 2026 (full text) | Queries fully in one language | Neutral for H2 |

## 3. Is H3 distinguishable from existing work?

**Answer: distinguishable as a question, weak as a contribution. Demoted to exploratory (E2).**

- **For distinctness:** no paper found tests genealogy against *item-level sycophancy concordance* with subword-overlap, resource and competence controls.
- **Against:**
  - Ranaldi & Pucci already measure cross-lingual action consistency (uncontrolled, 5 languages).
  - Shah et al. cluster languages by sycophancy profile and include family in regression.
  - Qi et al. (subword overlap dominates genealogy) and Mitrovic et al. (genus effects conditioned on resources) make a confounded or null result the most likely outcome.
  - The Belebele panel gives few independent languages per family.
- **Translation quality** is controlled through Belebele's human translations for items. Pushback templates still need validation.

## 4. Other findings that changed the plan

- **H1 (guess inflation) is no longer a contribution.**
  - SycoLens (English, full text) shows flips on unsettled items mostly reflect "regression toward the model's own distribution", with option-balanced screening and matched controls.
  - Maraia et al. and AfriSyCo already condition on initial correctness.
  - **Decision:** H1 is kept only as an exploratory robustness check (E1).
- **The mitigation hypothesis and intervention transfer are dropped.** Ranaldi & Pucci show English-trained mitigation generalises, and instruction-based mitigations showed no benefit.
- **New design constraint.** Gupta et al. 2026 show target naming shifts follow rates by 14–50 pp, so all compared conditions must name the target identically.

## 5. Remaining uncertainties

1. **Incomplete forward-citation coverage:**
   - Huang & Cheng (Semantic Scholar could not resolve it).
   - Maraia et al. citers (rate-limited).
   - Mitrovic et al. citers (not traced).
   - No Google Scholar search.
   - Two key competitors appeared in Sep–Oct 2026, so the field is moving fast.
2. **SYCON-Indic** remains abstract-only (SSRN blocked).
3. **Partly read:** SycoLens and BenSyc were read to about two-thirds; their appendices were not inspected.
4. **Unknown competence:** gemma3:4b's comprehension of Assamese, Odia and Tamil is unknown. Shah et al. place Assamese and Odia in a "zero-shot" tier for other models.
5. **Contribution size:** after AfriSyCo, the contribution may be judged incremental. Venue fit cannot be assessed before results.
6. **Sociolinguistic choice:** Hindi as the regional dominant language for Assamese and Odia needs justification; Bengali may be a better regional L_P for Assamese.

## 6. Go / no-go

**Recommendation: CONDITIONAL GO for a small feasibility pilot only (research.md §9). NO-GO for any hypothesis-testing run.**

**Why a pilot is interpretable:**
- Its outputs are feasibility measurements: permutation-robust accuracy against chance, the knowledge-gated item count, pushback comprehension, re-ask instability, parse failures and variance components.
- These are meaningful even for a single 4B model.
- Comprehension is measured by MCQ accuracy and an explicit probe, **never inferred from fluent generation.**

**Why not more:**
- One small model cannot support claims about H2.
- Inspecting condition contrasts in the pilot would compromise the confirmatory test.

**Conditions before running it:**
1. You approve the narrowed RQ and the 6-language pilot panel.
2. Pushback templates are drafted and back-translated, and flagged unvalidated.
3. You accept that pilot output will report gates only, not H2 contrasts.

**Conditions before the main study:**
- the go criteria in research.md §9 are met;
- templates are validated by fluent speakers;
- the forward-citation gaps in §5.1 are closed;
- the preregistration is frozen in a timestamped commit.

**Stop criterion:** if gemma3:4b and one larger open model both fail the knowledge-gate or comprehension criteria for most non-English languages, the knowledge-gated design is not viable for these languages with accessible models. That would be documented as the outcome, and the project revisited.
