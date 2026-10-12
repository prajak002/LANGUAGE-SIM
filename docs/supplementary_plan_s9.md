# Supplementary analysis S9: expert loan judgements in thirteen languages (IE-CoR). Plan v1.0 (FROZEN)

_2026-10-12. Frozen before any word row of the database was read. Seen before freezing: the repository's licence field (CC BY 4.0), its README, its file list, the column names of its tables, and its list of languages. SHA-256 in `docs/decision_log.md` (entry 100). Requested by the project lead, who asked for stronger evidence; no human annotator is available, so a published expert source is used._

## Why

The paper compares a Wiktionary label with an expert's judgement for one language only (Romanian, S6). The Indo-European Cognate Relationships database (IE-CoR; Heggarty, Anderson & Scarborough 2024; CLDF edition `github.com/lexibank/iecor`, CC BY 4.0) records, for 170 basic meanings in 160 languages, the cognate set of each word and whether the word is a loan, as judged by a team of specialists. Thirteen of our sixteen baseline languages are in it: Assamese, Bengali, Hindi, Marathi, Punjabi; Catalan, French, Italian, Portuguese, Romanian, Spanish; Greek (Modern Standard); Armenian (Eastern). Gujarati, Odia and Galician are not.

## What it can and cannot show

- It can show, in thirteen languages and four families, how often Wiktionary's inherited or learned label agrees with these specialists' loan judgement, and what the specialists say about dissociated items.
- **It is a list of basic meanings**, where inherited words dominate, so learned words will be few. It does not distinguish learned from semi-learned borrowing. It is one team's judgement, not a two-annotator validation of our items, and it is not independent of the handbooks that Wiktionary's editors also use.

## Expert class of a word (fixed here)

A database lexeme is a **loan** if its `Loan` field is true, or if a cognate set it belongs to (`cognates.csv`) has a row in `loans.csv`. The donors are the `Source_languoid` values of those rows. How the `Loan` field is written (its set of values) is inspected first and reported.

A **word** (all lexemes of the language with the same spelling) gets one class:
- **NL** not a loan: no lexeme is a loan;
- **LA** loan, ancestor named: every lexeme is a loan and each has a donor whose name contains, without regard to case, "Sanskrit", "Vedic" or "Indo-Aryan" (Indo-Aryan languages), "Latin" (Romance), "Greek" (Greek), "Armenian" (Armenian);
- **LO** loan, other or no donor named: every lexeme is a loan and none has such a donor;
- **MIX**: anything else.

## Matching

The Wiktionary page title against the lexeme's `native_script` field and, where that is empty, its `Form` and `Value` fields, each after the baseline's `normalise`; exact match. Alternatives separated by commas, slashes or semicolons are split; bracketed material is removed. Language: the IE-CoR variety named above.

## Measures

- **E1, the audit sample** (rows of `sample.csv` in the inherited, learned and semi-learned categories of the thirteen languages). Reported per family and pooled: how many sampled titles are in the database; the cross-table of Wiktionary category by expert class; with Wilson 95% intervals, of inherited-category words found, the share NL; of learned-category words found, the share LA and the share LO. Titles sampled from two categories are reported separately.
- **E2, baseline items** whose word is NL or LA: Wiktionary's label and B3's out-of-fold prediction against the expert class (NL = inherited, LA = learned), on congruent, middle and dissociated items, per family and pooled, with counts. **For dissociated items: whether the expert class sides with Wiktionary's label or with resemblance.**
- Cells with fewer than 30 words are reported as counts without interpretation. Everything is reported, including empty cells.

## Reading fixed in advance

- A high share of NL among inherited-category words extends the Romanian finding to more languages, for basic vocabulary only.
- If the experts side with Wiktionary on most dissociated items found, labelling error is not what makes those items hard; if they side with resemblance, the opposite. If fewer than 30 dissociated items are found in a family, that family's figure is a count and not a rate.
- No claim is made about learned labels unless at least 30 learned-category words are found.

## Storage

The rows used (language, form, loan status, donors, lexeme ID) are stored under `data/external/iecor/` with the citation and licence. The download is otherwise temporary.
