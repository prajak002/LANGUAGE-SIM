# Cross-lingual audit of Wiktionary route labels: plan v1.0 (FROZEN)

_2026-10-11. Frozen before any category size, member list or page for this audit was retrieved. SHA-256 in `docs/decision_log.md` (entry 74). Requested by the project lead ("add huge dataset, multiple cross-lingual work on more global languages")._

## 1. Purpose and limits

The 48-lemma study found three properties of Wiktionary's route labels for Hindi and Bengali: category membership is not the route the page asserts; one spelling often covers an inherited and a learned word; and agreement with a dictionary is not independent when the entry cites it. This audit measures the same properties **automatically, on a large sample, in many languages** that have an ancestor language from which words are both inherited and re-borrowed.

- **It measures Wiktionary's own records.** It does not decide which labels are historically correct. No dictionary is consulted, no model is called, and no label is validated.
- **It is descriptive.** No hypothesis test is planned. Every proportion is reported with its count and a Wilson 95% interval.
- `research.md` §13 stays empty.

## 2. Language pairs

A pair is (modern language L, ancestor A). The three categories are `{L} learned borrowings from {A}` (LRN), `{L} semi-learned borrowings from {A}` (SEMI) and `{L} terms inherited from {A}` (INH).

**Candidate pairs** (fixed here; ancestor code in brackets):
- Sanskrit [sa]: Hindi, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese, Nepali, Sinhalese, Urdu, Konkani, Maithili.
- Latin [la]: Spanish, Portuguese, French, Italian, Romanian, Catalan, Galician, Occitan.
- Ancient Greek [grc]: Greek.
- Old Armenian [xcl]: Armenian. Middle Persian [pal]: Persian. Old Irish [sga]: Irish. Old Norse [non]: Icelandic. Old Georgian [oge]: Georgian. Ottoman Turkish [ota]: Turkish. Old East Slavic [orv]: Russian. Old Javanese [kaw]: Javanese. Old Japanese [ojp]: Japanese. Biblical Hebrew [hbo]: Hebrew. Old English [ang]: English.

**Inclusion rule:** a pair is included if, by category metadata alone, both the LRN and the INH category exist and each holds at least 100 pages. The SEMI category is used if it exists, whatever its size. Excluded pairs are listed with their sizes.

## 3. Sampling

- Full member lists (namespace 0) are retrieved for every included category. No title filter.
- **Seed:** `crosslingual-audit-v1-2026-10-11`. Key: `SHA-256(seed|L|A|category|title)`. Within a category, titles are ordered by key and the first **400** are taken (all, if fewer). 400 gives a Wilson 95% half-width of at most 5 points.
- A title sampled in two categories is fetched once and counted in each.
- For each sampled page the latest revision is fetched. Stored: page ID, revision ID, timestamp, and the wikitext of the L section only.
- A page with no L section is recorded as such and not replaced.

## 4. Measures (fixed before data are seen)

The **route of a sense** is read from the etymology templates in that sense's own Etymology section, as in protocol v1.1 §5″, with A's language code (and its etymology-only variants, e.g. `la-vul`) as the ancestor: `inh` → INH, `lbor` → LRN, `slbor` → SEMI, plain `bor` from A → BOR (unspecified borrowing).

| # | Measure | Unit | Definition |
|---|---|---|---|
| M1 | Category sizes and semi-learned share | category | Pages in LRN, SEMI, INH; SEMI / (LRN + SEMI) |
| M2 | Category overlap | title, whole population | Titles in two or more of the three categories, as a share of their union |
| M3 | Category not supported by a template | sampled page, per category | No sense on the page has the route the category names |
| M4 | Multiple etymologies | sampled page | The L section has two or more Etymology sections |
| M5 | Conflicting routes under one spelling | sampled page | Two senses of the page have different routes from A among INH, LRN, SEMI |
| M6 | Entry cites any reference | sampled page | The L section has a `<ref>`, an `R:` template, or a References / Further reading heading |
| M7 | Etymology cites a reference inline | sampled sense with the category's route | The Etymology text of that sense has a `<ref>` or an `R:` template |
| M8 | Most-cited reference works | L | The five most frequent `R:` templates in sampled L sections |

## 5. Conduct

- English Wiktionary Action API, serial requests at least 1.5 s apart, `maxlag=5`, a descriptive User-Agent with no personal contact, back-off on 429/503.
- Raw responses for member lists and the stored sections go under `data/raw/wiktionary/crosslingual_v1/`. Wiktionary text is CC BY-SA.
- Any change to this plan after data are seen is a deviation and is logged as one.
