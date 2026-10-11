# Data-audit plan: Wiktionary as a candidate source (PLAN; nothing downloaded)

_2026-10-10. **Status: plan for approval.** No bulk download or collection has been done. This plan replaces "download a Wiktionary dump" with a **targeted, versioned, small-scope** collection of candidates. **Wiktionary is never ground truth**; expert labels are (`docs/annotation_guidelines.md`)._

## 1. Source, version and scope

| Item | Specification |
|---|---|
| **Source** | English Wiktionary (en.wiktionary.org), accessed through the **MediaWiki Action API**: category membership, then the wikitext of those pages only. **Not** a full dump, and **not** third-party extractions (kaikki/wiktextract), unless separately approved |
| **Version pinning** | Every page is stored with its **page ID, revision ID and revision timestamp**. A snapshot timestamp is recorded for the whole collection, which is reproducible by revision ID |
| **Scope (languages)** | Hindi, Bengali first. Assamese and Odia only if the counts justify it (§6) |
| **Scope (pages)** | Members of these categories per language. Sizes observed 2026-10-10: |
| | • `{Lang} learned borrowings from Sanskrit` (hi 1,337 / bn 1,075) |
| | • `{Lang} semi-learned borrowings from Sanskrit` (hi 98 / bn 44) |
| | • `{Lang} terms inherited from Sanskrit` (hi 2,241 / bn 1,045) |
| | • A **control pool** of `{Lang} terms borrowed from` Persian, Arabic and English (category names to be verified), for the EXT label and negative controls |
| **Fields extracted** | Lemma (native script); the language section's etymology wikitext only; template calls (`inh`, `lbor`, `slbor`, `bor`, `der`) with their arguments (etymon, intermediate forms such as Pāli or Prakrit, language codes); pronunciation section if present |
| **Not collected** | Definitions, usage examples, quotations, images, audio, other language sections |
| **Volume** | Approximately the category totals above (thousands of pages, not millions), fetched politely: a descriptive User-Agent, serial requests, respecting `maxlag` and rate limits |
| **Storage** | `data/raw/wiktionary/` (git-ignored if a repository is created), with a manifest of page and revision IDs |

## 2. Licence and attribution

- **Licence:** Wiktionary text is dual-licensed **CC BY-SA 4.0 and GFDL** (1.1 or later), per `Wiktionary:Copyrights`, read 2026-10-10. That page is marked outdated or draft, so **current terms must be confirmed against the Wikimedia Terms of Use before any release.**
- **Obligations for any released derivative** (candidate lists, extracted etymology fields):
  - license it under CC BY-SA 4.0 (share-alike);
  - attribute by linking each item to its Wiktionary page and **revision ID**;
  - do not imply endorsement.
- **Expert gold labels** are our own work, but are distributed with the derivative under compatible terms (OPEN decision for the release).
- **No CDIAL/Jambu material** is collected: SOAS copyright, and no licence file in the Jambu repository.

## 3. Candidate discovery, not ground truth

- The Wiktionary-derived tag is stored as `candidate_label` with its source template and revision ID. It is **never** written to `gold_label`.
- `candidate_label` is used **only** for stratified sampling and for reporting silver–gold agreement.
- Experts annotate blind to `candidate_label`.
- Dataset size is reported as the number of **expert-labelled** items. Candidate counts are reported separately and never presented as dataset scale.

## 4. Normalisation, deduplication and word families

1. **Normalisation:** Unicode NFC; strip Wiktionary markup; keep the native script as-is. A separate transliteration field (scheme OPEN) is used only for grouping.
2. **Exact duplicates:** the same (language, lemma) with multiple etymology sections is kept as **separate candidates** with a shared `lemma_group`, and flagged.
3. **Word families** (union-find over items), linked when they share any of:
   - the same OIA etymon, across all four languages (cross-language reflexes and doublets);
   - the same modern base, where one lemma is a derivative or compound of another lemma in the pool;
   - **near-duplicates**: transliterated normalised edit distance ≤ τ within a language, with an expert check of a sample of the merges (τ OPEN; reported).
4. **The split unit is the word family** (`docs/experimental_protocol.md` §3). No family crosses train, dev and test.

## 5. Sampling

**For the practice round:** about 30–50 items in total (exact number OPEN, set with the experts). This is the only collection proposed now, and requires approval.
- **Stratified by** language × candidate_label (INH, LRN, SEMI, EXT control) × doublet status.
- **Deliberately enriched** with candidates likely to be hard: semi-learned items, doublets, and items whose etymology mentions another NIA language.
- These items go into a **calibration pool excluded from all later evaluation splits.**

**For the label audit** (later, after the practice round):
- a stratified random sample of word families;
- size set by the agreement-precision target and the annotator budget (OPEN);
- frequency banding if a licensed frequency list is identified (OPEN).

## 6. Expert verification and disputed cases

- **Every evaluation label is expert-assigned**, following `docs/annotation_guidelines.md`.
- **DIS (disputed) and UNK (cannot decide) are legitimate outcomes.**
  - They are never forced into INH or LRN.
  - Their rates are reported as findings about **recoverability**: how often documentation does not allow the route to be determined.
- If DIS + UNK + MIX dominate a language, that language is not used for the primary test. This is reported, not hidden.

## 7. Decision points

| After | Decision | By |
|---|---|---|
| Practice round | Revise the guidelines; set annotation-time estimates | Experts, then the user |
| Category counts plus the practice round | Whether Assamese and Odia are feasible | The user |
| Label-audit agreement | Whether a classifier experiment is feasible (enough INH-REG and LRN items with acceptable κ) | The user |
| Novelty checks (ACM Kanojia paper; broader audit) | Whether the classification contribution is sufficiently novel | The user |

## 7b. Practice-set fetch: done 2026-10-10 (conditionally approved)

- **Access policy verified before fetching:**
  - Wikimedia Robot policy (unauthenticated Action API: concurrency 1, fewer than 5 requests per second);
  - User-Agent policy;
  - API:Etiquette (serial requests, `maxlag`).
- **Run:** serial, at least 3 s between requests, `maxlag=5`, with a 429/503 backoff.
  - The first attempt hit HTTP 429 on a member-list request. Its partial output (member lists only, no pages) was discarded, and the run was repeated from scratch.
  - **The UA carries no contact information yet** (the user's choice is pending). This should be fixed before any larger fetch.
- **Category coverage:** all six target categories per language exist.
  - The Persian control uses `terms borrowed from Classical Persian`; `terms borrowed from Persian` has only 8 Hindi and 1 Bengali pages.
  - Eligible pool sizes: Hindi OVL 44, SEMI 98, LRN 1,318, INH 2,190; Bengali OVL 11, SEMI 44, LRN 1,055, INH 1,005.
- **Result:**
  - 48 of 48 retrieved, with no replacements;
  - every page has its target-language section and an Etymology section;
  - revision timestamps range from 2023-06-29 to 2026-10-05.
- **Storage:** raw records are read-only in `data/raw/wiktionary/practice_round_1/` (manifest SHA-256 `f98f6d38…379b03d`), kept separately from any annotation data. The script is `scripts/fetch_practice_set.py`.
- **Not done:** no annotation-facing sheet, no parsing of etymologies, no release.

## 8. Approval requested now

- **Only** the practice-round candidate fetch: about 50 pages via the API, with revision IDs.
- **Not** the full candidate pool.
- **Not** any modelling.
