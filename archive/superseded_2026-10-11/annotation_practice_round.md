# Annotation practice round: protocol (PLAN)

_2026-10-10. **Not started.** No experts are recruited. Items are selected and raw sources retrieved (§3); none are annotated. This round validates `docs/annotation_guidelines.md`. It produces no evaluation data._

## 1. Goal

**This round answers a feasibility question, not a novelty question:**
1. Can experts apply the categories consistently?
2. Which historical distinctions are genuinely recoverable from the available evidence?
3. Which categories need revised definitions?
4. How often are items disputed (DIS) or impossible to classify (UNK)?

**No classifier training or confirmatory evaluation begins until these questions have defensible answers.**

Specifically, find:
- ambiguous etymologies;
- unclear boundaries between categories (especially SEMI vs. MIX, LRN with nativisation vs. SEMI, INH vs. NIA);
- cases where historical evidence is insufficient.

## 2. Annotators

- **At least 2**, ideally 3:
  - training in Indo-Aryan historical linguistics or etymology;
  - reading competence in the language(s) annotated, and Sanskrit;
  - access to the reference works in guidelines §5.
- **Recorded only after they agree to participate.** The record includes name or initials (as they prefer), qualifications, the languages covered, and the agreement date. **No one is named here until then.**
- **Compensation and credit:** OPEN (the user's decision).

## 3. Materials

- **Practice set:** 48 candidates (24 Hindi, 24 Bengali), selected under **frozen rules**, `docs/practice_set_selection.md` v1.0.
  - The rules were fixed and hashed **before** any category member list was retrieved or any selected item's label was inspected.
  - The set deliberately covers hard boundaries: the OVL stratum and over-sampled SEMI.
  - Order within strata is hash-keyed, so selection cannot depend on whether an item supports the proposed classifier.
  - Retrieved 2026-10-10. All 48 pages have the target-language section and an Etymology section; there were no replacements.
  - The set goes into a calibration pool that is **excluded from all evaluation splits**.
- **Each item shows:** the modern lemma in native script, the language, and the OIA etymon as given by the source. **Not** shown: the Wiktionary label, the template type or any model output.
- The guidelines draft v0.1.
- A feedback form per item:
  - label;
  - confidence;
  - pathway code;
  - references;
  - "boundary unclear between ___ and ___";
  - "evidence insufficient because ___";
  - suggested rule change.

## 4. Procedure

1. A briefing on the guidelines. No example items are discussed beforehand.
2. **Independent labelling.** Annotators do not communicate with each other until they submit.
3. **Freeze the independent labels** (hashed file) **before** any discussion.
4. **Agreement analysis on the independent labels, before adjudication:**
   - overall Cohen's κ (2 annotators) or Fleiss' κ (3+), on the full 10-label set and on the binary INH/LRN subset (items both labelled INH or LRN);
   - **per-category agreement:** positive specific agreement and one-vs-rest κ per label;
   - a confusion matrix between annotators;
   - the rate of DIS and UNK per annotator.

   This is a small set, so these statistics are **descriptive**, with wide intervals (bootstrap CIs reported). No threshold decision rests on the practice round alone.
5. **Record all feedback verbatim** in `docs/annotation_feedback/practice_round_1.md` (to be created) **before** revising anything.
6. **Discussion and adjudication:** a third expert, or consensus discussion, resolves disagreements. Unresolvable items stay DIS.
7. **Revise the guidelines** to v0.2, with each change linked to the feedback item that motivated it, logged in the decision log.
8. **Second round:** if overall or key per-category agreement looks inadequate, run a new practice set before any audit labelling.

## 5. Outputs

- Frozen independent labels.
- An agreement report: overall and per-category, with CIs.
- The feedback record.
- Guidelines v0.2 and a change log.
- An estimate of annotation time per item (for budgeting the label audit).

## 6. What this round does not do

It does not:
- produce training or test labels;
- establish the label distribution in the population;
- support any novelty or performance claim.
