# Supplementary analysis S4: Turner at scale through the Jambu database: plan v1.0 (FROZEN)

_2026-10-11. Frozen before the Jambu forms file was downloaded. Seen before freezing: the repository's file list and README, the header of `cldf/forms.csv` with its first 11 rows (Sanskrit head-words only), and `cldf/languages.csv`. SHA-256 in `docs/decision_log.md` (entry 80). Approved by the project lead ("yes" to using the Jambu copy of Turner for analysis only, with nothing from it released)._

## Status of the source

- Jambu (`github.com/moli-mandala/data`) holds a machine-readable copy of Turner's dictionary. **The repository has no licence, and Turner's dictionary is in copyright.**
- **Use here: analysis only.** The file is downloaded to a temporary folder outside the repository and deleted afterwards. The repository keeps only counts and, per item, an entry number and yes/no flags. No entry text and no Turner form is stored or released.
- This is **the same single source** as in the 48-lemma study, read by a program at scale. It is not a second, independent source, and it is not expert annotation.

## Question

The 48-lemma study assigned "inherited" when Turner lists the modern form with no loan mark, and found that rule leaky on a handful of words. **How often does Turner list a form for words that Wiktionary calls learned or semi-learned?**

## Items

The baseline items (`data/baseline_v1/items.csv.gz`) of Hindi, Bengali, Marathi, Gujarati, Punjabi, Odia and Assamese, all three routes. Jambu language IDs: H (Hindi-Urdu), B, M, G, P, Or, A.

## Matching (fixed here)

- **Etymon → Turner article.** The item's Sanskrit etymon (Devanagari, as given by Wiktionary) is transliterated to Latin by a fixed table. It and Turner's head-words are normalised: accents and other combining marks removed, `ṁ`/`ṃ` and class nasals before a stop unified to `n`, `r̥`/`ṛ` unified, a leading `*` and trailing `-` removed, lower case. An item matches the article or articles whose normalised head-word equals its normalised etymon.
- **T1:** the etymon matches at least one article.
- **T2:** some matched article lists at least one form for the item's language.
- **T3:** some form listed for the language in a matched article has the same **consonant skeleton** as the Wiktionary word. The skeleton is the transliterated word with all vowels, nasalisation, length and aspiration marks removed and long/geminate consonants reduced to one.
- If the file marks loanwords in a machine-readable way, forms so marked are counted separately; if it does not, that is reported and no loan filter is applied.

## Validation before any result is read

The 48-lemma study recorded by hand, for 39 Turner checks in round 2 and 6 in the pilot, whether an article was found and whether the lemma's form was listed. **T1 and T3 are first compared with those hand records.** Agreement is reported as counts. If T3 agrees with the hand record on fewer than 80% of the comparable rows, T3 is reported as failed and only T1 and T2 are interpreted.

## Measures

Per language and Wiktionary route (inherited, semi-learned, learned), with Wilson 95% intervals: T1 / items; T2 / T1; T3 / T1.

## Limits fixed in advance

- A missed match (spelling, compound, derived form) lowers T1; T1 is not Turner's coverage.
- T2 does not show that Turner lists *this word*: an inherited doublet of a learned word satisfies it. T3 is the measure aimed at the leaky rule, and it is approximate.
- Agreement between Wiktionary and Turner is not independent: Turner is among the most-cited references in 7 of the 8 Indo-Aryan languages audited.
