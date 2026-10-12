# Cross-lingual audit of Wiktionary route labels: report

_2026-10-11. Plan: `docs/crosslingual_audit_plan.md` v1.0 (frozen, SHA-256 `fb4a595e…acbd1`). Data: `data/raw/wiktionary/crosslingual_v1/` (raw) and `data/audit/crosslingual_v1/` (derived). Decision log 74–75._

**Read this first.**
- **This audit describes Wiktionary's own records. It validates no label.** It cannot say which words are really inherited or learned.
- **The 17 language pairs are not 17 independent tests.** Eight share Sanskrit, seven share Latin, and languages in a family share editors, templates and reference works. Results are given per language and grouped by ancestor; pooled figures are sums over samples, not population estimates.
- All shares are sample proportions with Wilson 95% intervals in `data/audit/crosslingual_v1/tables.md`. `research.md` §13 stays empty.

## 1. What was retrieved

| | Count |
|---|---|
| Candidate pairs fixed in the plan | 32 |
| Pairs passing the size rule (learned and inherited categories each ≥ 100 pages) | 17 |
| Categories with member lists retrieved | 50 (Greek has no semi-learned category) |
| Sample rows (up to 400 per category per pair, hash order) | 13,565 |
| Distinct page titles requested | 13,128 |
| Retrieved, with a revision ID | 13,128 |
| Sample rows whose page lacks the language section | 0 |
| Redirects | none possible (titles come from category member lists) |
| Senses (etymology sections) read | 15,118 |

- **Sampling.** 400 means up to 400 pages per category, per language pair. Smaller categories are taken whole (all semi-learned categories, and the learned categories of Assamese, Marathi, Odia, Punjabi and Urdu). A title in two samples is fetched once and counted in each.
- **Excluded pairs** (sizes in `sizes.csv`): Nepali, Sinhalese, Konkani, Maithili, Occitan, Persian, Irish, Icelandic, Georgian, Turkish, Russian, Javanese, Japanese, Hebrew, English. Each lacks a learned-borrowing category of 100 pages from the named ancestor.
- **Revisions.** Fetched 2026-10-11, 15:18–15:54 UTC. The page ID, revision ID and timestamp of every page are in `sections.jsonl.gz`.

## 2. Deviations from the frozen plan

1. **The template reader was corrected after the first run.** The first run reported that up to 28% of pages in an inherited category had no supporting template. Inspection showed a defect in the reader, not in Wiktionary: the newer `ety` / `etymon` template nests its chain (`<ety:inh<la:…>>`) and can contain other templates, and the reader missed both. The reader was fixed, the fixture was extended to cover these forms (17 hand-worked checks, all passing), and the audit was rerun. **The first-run figures are kept in `measures_parser_v1_as_run.csv` and are not used.**
2. **One measure was added:** M3c, the share of inherited-category pages where the page states inheritance from an intermediate stage only.
3. Nothing else changed: the pairs, the sample, and measures M1–M8 are as planned.

## 3. Summary

| Ancestor | Language | Learned pages | Semi-learned pages | Inherited pages | M3 inherited: category not supported on the page (%) | M4 multiple etymologies (%) | M5 conflicting routes (%) | M6 entry cites any reference (%) | M7 learned: inline citation (%) | M7 inherited: inline citation (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| Sanskrit | Assamese | 149 | 7 | 1082 | 3.2 | 7.7 | 0.0 | 19.6 | 0.0 | 1.5 |
| Sanskrit | Bengali | 1075 | 44 | 1045 | 4.0 | 6.8 | 1.1 | 37.7 | 0.8 | 9.0 |
| Sanskrit | Gujarati | 466 | 30 | 1161 | 6.8 | 4.1 | 0.6 | 44.9 | 0.0 | 10.1 |
| Sanskrit | Hindi | 1337 | 98 | 2241 | 7.8 | 9.7 | 2.6 | 82.9 | 1.0 | 8.7 |
| Sanskrit | Marathi | 358 | 12 | 955 | 3.0 | 4.2 | 0.4 | 84.2 | 0.6 | 7.5 |
| Sanskrit | Odia | 269 | 3 | 655 | 5.5 | 0.7 | 0.1 | 81.7 | 0.0 | 1.9 |
| Sanskrit | Punjabi | 224 | 36 | 1453 | 14.2 | 8.2 | 0.3 | 90.0 | 0.4 | 8.4 |
| Sanskrit | Urdu | 209 | 48 | 769 | 9.8 | 12.2 | 1.9 | 72.8 | 0.5 | 22.7 |
| Latin | Catalan | 3614 | 70 | 2118 | 0.2 | 10.6 | 0.6 | 90.1 | 4.0 | 2.9 |
| Latin | French | 2697 | 25 | 2191 | 3.8 | 9.8 | 0.0 | 89.9 | 0.5 | 1.8 |
| Latin | Galician | 885 | 26 | 2397 | 3.8 | 12.2 | 0.7 | 86.7 | 0.0 | 9.4 |
| Latin | Italian | 2025 | 64 | 3499 | 0.0 | 17.5 | 0.6 | 46.6 | 1.5 | 5.3 |
| Latin | Portuguese | 4206 | 129 | 2479 | 11.2 | 16.6 | 0.5 | 93.4 | 3.2 | 6.7 |
| Latin | Romanian | 1634 | 3 | 2116 | 0.0 | 7.0 | 0.4 | 30.0 | 0.0 | 5.0 |
| Latin | Spanish | 3345 | 129 | 2815 | 5.2 | 15.7 | 0.5 | 93.3 | 3.5 | 6.7 |
| Ancient Greek | Greek | 1225 | 0 | 3427 | 0.2 | 2.4 | 0.4 | 64.7 | 57.3 | 8.5 |
| Old Armenian | Armenian | 1753 | 32 | 1363 | 1.0 | 5.4 | 1.6 | 21.5 | 0.2 | 1.3 |

Columns M4–M6 pool the distinct sampled titles of a language; they are not weighted to the population.

## 4. Findings, measure by measure

**M1. Semi-learned categories are small everywhere.** They hold 0 to 129 pages. As a share of learned plus semi-learned pages they range from 0% (Greek) and 0.2% (Romanian) to 13.9% (Punjabi) and 18.7% (Urdu).

**M2. Few titles are in two categories.** 0.0% to 1.3% of titles (Hindi 45 of 3,630; Urdu 13 of 1,012).

**M3. Learned and semi-learned categories are almost always backed by a template on the page.** Unsupported: 5 of 6,009 sampled learned pages and 12 of 756 semi-learned pages. **Inherited categories are different:** 319 of 6,800 pages (0% to 14.2% by language) have no inheritance template naming the ancestor. In almost all of these (M3c) the page states inheritance from an intermediate stage, such as Old Spanish or a Prakrit, and the ancestor is reached only through another entry's etymology.

**M4. Multiple etymologies under one spelling are common in some languages.** 0.7% (Odia) to 17.5% (Italian) of sampled titles.

**M5. Conflicting routes under one spelling are rare.** 0.0% to 2.6% of sampled titles. The highest single figure is Hindi semi-learned pages: 13 of 98 also carry a sense with another route.

**M6. Whether an entry cites any reference varies widely:** from 19.6% (Assamese) and 21.5% (Armenian) to 93.4% (Portuguese).

**M7. The route claim itself is rarely sourced.** For senses marked as learned borrowings, the etymology carries an inline citation in 0.0% to 4.0% of cases in 16 of the 17 languages. Greek is the exception at 57.3% (228 of 398). For inherited senses the range is 1.3% to 10.1%, with Urdu at 22.7%.

**M8. Reference works.** The most-cited works are general monolingual dictionaries in most languages (full list in `tables.md`). Turner's comparative dictionary is among the five most-cited templates in 7 of the 8 Indo-Aryan languages (all except Bengali).

## 5. What this does to the claims of the 48-lemma study

| Claim from the 48 lemmas | At scale |
|---|---|
| Category membership is not the route the page asserts | **Not supported as a general rate** for learned and semi-learned categories (under 2%). It holds in a narrower form for inherited categories: 0–14% depend on another entry |
| One spelling often covers an inherited and a learned word | **Rare** (0–2.6%). The "overlap" stratum of the 48-lemma study selected exactly these rare pages, by design |
| The semi-learned category is the weak point | **Supported in a different way:** it is tiny in every language, at most 129 pages |
| Agreement with a dictionary is not independent when the entry cites it | Consistent: Turner is a top-five reference in 7 of 8 Indo-Aryan languages. Not tested directly |
| (new) | **Route claims are almost never sourced inline**, outside Greek |

## 6. Limits

- **No label is validated.** A page can be internally consistent and wrong, or unsourced and right.
- **M7 counts inline citations only.** An etymology may rest on a reference listed at the foot of the entry (M6) without an inline mark. M6 cannot tell an etymological source from a general dictionary.
- **The reader recognises a fixed set of templates.** Etymologies written as plain text, or with templates outside that set, count as "no route". The fixture tests the reader's logic, not its coverage of Wiktionary's template variety.
- **Category sizes are from category metadata**; samples are from member lists of namespace 0.
- **Languages differ in size and editing practice**, so differences between languages may reflect editors, not the languages.
- **One snapshot.** Wiktionary changes; the revision IDs fix what was read.
- **Data release prerequisites are open:** no contact was given in the User-Agent, and the licensing review is not done. Wiktionary text is CC BY-SA.

## 7. Reproduce

```
python3 tests/test_audit_fixture.py
python3 scripts/audit_crosslingual.py data/raw/wiktionary/crosslingual_v1 data/audit/crosslingual_v1
python3 scripts/crosslingual_tables.py data/audit/crosslingual_v1 > data/audit/crosslingual_v1/tables.md
```
