# Supplementary analysis S6: expert loanword labels for Romanian (World Loanword Database): plan v1.0 (FROZEN)

_2026-10-11. Frozen before any word row of the database was read. Seen before freezing: the repository's licence field (CC BY 4.0), its file list, the column names of its tables, the list of its 41 languages, and the citation line of the Romanian contribution. SHA-256 in `docs/decision_log.md` (entry 83)._

## Why

Nothing in the paper so far says whether a Wiktionary label is right. The World Loanword Database (Haspelmath & Tadmor, eds., 2009; CLDF edition `github.com/lexibank/wold`, CC BY 4.0) contains a Romanian vocabulary of 2,137 entries compiled by a specialist (Kim Schulte), in which each word carries a borrowed status and, for loanwords, the donor language. **It is the first source in this project that is expert-made, openly licensed, machine-readable and not Wiktionary.** Romanian is the only one of the 17 audited languages in it.

## What it can and cannot show

- It can show, for one language, how often Wiktionary's inherited / learned label agrees with one expert's borrowed status.
- **It is one expert, one language, and a list built around basic meanings**, so learned vocabulary is under-represented. It does not distinguish learned from semi-learned borrowing. It is not independent of the general Romanian dictionaries that both it and Wiktionary may draw on.
- It is not a substitute for the two-annotator validation; no agreement between annotators exists.

## Expert class of a word (fixed here, from the database's documented five-point scale)

For each database entry: `Borrowed` status 1 ("clearly borrowed") or 2 ("probably borrowed") is *borrowed*; 5 ("no evidence for borrowing") or 4 ("very little evidence") is *not borrowed*; 3 ("perhaps borrowed") is *uncertain*. For a borrowed entry, the donors are the `Source_languoid` values of its rows in `borrowings.csv`.

A **word** (all entries with the same form) gets one class:
- **NB** not borrowed: every entry is not borrowed;
- **BL** borrowed, Latin named: every entry is borrowed and each has a donor whose name contains "Latin";
- **BO** borrowed, Latin not named: every entry is borrowed and none has such a donor;
- **MIX**: anything else (entries disagree, or status 3, or a missing status).

## Matching

Database form (`Value`; alternatives separated by commas, slashes or semicolons are split; a leading verb particle `a ` and bracketed material are removed; lower case; Unicode NFC, with cedilla and comma-below forms of ș and ț unified) against the Wiktionary page title, exact match.

## Measures

- **V1, all of Wiktionary's Romanian categories** (the member lists already stored: learned borrowings from Latin, semi-learned borrowings from Latin, terms inherited from Latin). Reported: how many titles of each category are in the database; the cross-table of Wiktionary category by expert class; and, with Wilson 95% intervals,
  - of inherited-category words found: the share NB;
  - of learned-category words found: the share BL, and separately the share BO (the expert names another donor, such as French);
  - titles in two categories are reported separately.
- **V2, baseline items** (`oof_predictions.csv.gz`, Romanian) whose word is NB or BL: B3's out-of-fold prediction against the expert class (NB = inherited, BL = learned), overall and on the congruent, middle and dissociated subsets, with counts. For dissociated items: whether the expert class sides with Wiktionary's label or with resemblance.
- Everything is reported, including small or empty cells.

## Storage

The database is CC BY 4.0. The Romanian rows used (form, status, donors, entry ID) are stored under `data/external/wold_romanian/` with the citation and licence. The download is otherwise temporary.
