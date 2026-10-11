# Practice-set selection rules (FROZEN v1.0)

_Frozen 2026-10-10, **before** any category member list was retrieved or any selected item was inspected. The SHA-256 of this file is recorded in `docs/decision_log.md`. Any change needs a new version, a new hash and a logged reason, and must be made before a new selection run._

## 1. Purpose

Select about 50 Wiktionary candidates for annotation practice round 1 (`docs/annotation_practice_round.md`). The set deliberately covers hard category boundaries. **Selection must not depend on any item's content, its etymology, or whether it would support the proposed classifier.** Within each stratum, order is fixed by a keyed hash, not by inspection.

The only item-level information used is:
- the page title;
- membership in the categories listed below.

Membership is the Wiktionary candidate label. It is used for stratification only and is never shown to annotators.

## 2. Source

- English Wiktionary Action API (`https://en.wiktionary.org/w/api.php`), `list=categorymembers` with `cmnamespace=0`.
- Category existence and sizes were checked on 2026-10-10 (category metadata only) before freezing.

## 3. Strata (per language: Hindi `hi`, Bengali `bn`)

The `{L}` categories:

| Stratum | Definition | n per language |
|---|---|---|
| OVL | Titles in **two or more** of `{L} learned borrowings from Sanskrit`, `{L} semi-learned borrowings from Sanskrit`, `{L} terms inherited from Sanskrit` | 3 |
| SEMI | `{L} semi-learned borrowings from Sanskrit` | 6 |
| LRN | `{L} learned borrowings from Sanskrit` | 6 |
| INH | `{L} terms inherited from Sanskrit` | 6 |
| EXT-FA | `{L} terms borrowed from Classical Persian` | 1 |
| EXT-AR | `{L} terms borrowed from Arabic` | 1 |
| EXT-EN | `{L} terms borrowed from English` | 1 |

**Total: 24 per language, 48 overall.** OVL is the hard-boundary enrichment. SEMI is over-represented relative to its population share by design. A shortfall in OVL (fewer than 3 eligible titles) is recorded as a shortfall and is **not** back-filled.

## 4. Eligibility (title-only rules)

- Namespace 0.
- No space and no hyphen in the title (single-word lemmas).
- No ASCII letters or digits in the title.

## 5. Ordering and selection

1. **Seed:** `practice-round-1-2026-10-10`.
2. **Key** for each eligible title in a stratum: `SHA-256(seed + "|" + lang + "|" + stratum + "|" + title)`, as hex.
3. **Order:** ascending by key.
4. **Strata processed** in the order OVL, SEMI, LRN, INH, EXT-FA, EXT-AR, EXT-EN. A title already selected in an earlier stratum is skipped.
5. Take the first n titles.

## 6. Retrieval and replacement

1. Fetch the latest revision's wikitext for each selected title. Record:
   - page ID;
   - revision ID;
   - revision timestamp;
   - URL;
   - retrieval time;
   - HTTP and API status.
2. **The only replacement rule:** if retrieval fails, or the page has no level-2 section for the target language, the item is marked `replaced` and the next title in that stratum's order is taken. Each replacement is logged.
3. Items **without an Etymology section are kept** and recorded as a coverage finding. Content is never a reason to replace an item.

## 7. Storage

- **Raw source records:** `data/raw/wiktionary/practice_round_1/`. One JSON file per page (the API response, unmodified) plus `manifest.csv`. Raw records are never edited.
- **Selection log:** `data/raw/wiktionary/practice_round_1/selection_log.csv`, containing the stratum, rank, key, title, status and replacement chain.
- **Annotation-facing data** is derived later, in a separate directory (`data/annotation/practice_round_1/`), and contains no candidate label. It is not created in this step.

## 8. Access conduct

- Serial requests only (concurrency 1).
- At least 1 second between requests.
- `maxlag=5`, with a backoff on a maxlag error.
- A descriptive User-Agent.

This is within the unauthenticated Action API limits of the Wikimedia Robot policy: concurrency 1, fewer than 5 requests per second. Contact information in the User-Agent is recommended by the User-Agent policy; it is omitted pending the user's choice of contact.

## 9. Licence

Retrieved text is CC BY-SA 4.0 / GFDL. **Nothing derived is released until the licensing review (`docs/data_audit_plan.md` §2) is complete.**
