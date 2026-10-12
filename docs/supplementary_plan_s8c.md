# Supplementary analysis S8c: the intermediate stage with a phonetic distance. Plan v1.0 (FROZEN)

_2026-10-12. Frozen after S8a was run and reported, and before any phonetic distance was computed. SHA-256 in `docs/decision_log.md` (entry 97). Requested by the project lead (a phonetic rather than orthographic comparison). The Jambu copy of Turner is downloaded again to a temporary folder for analysis only and deleted._

## Why

S8a compared forms after a normalisation that drops vowel length, retroflexion and the sibilant contrast. It found that 83% of the dissociated inherited items have an intermediate form "unchanged" from Sanskrit and that a model given the link does no better. Both could be artefacts of the coarse comparison. S8c repeats S8a with one thing changed, the distance.

Seen before freezing: all S8a results.

## What stays as in S8a

Items, matcher, link languages (Pali and Prakrit), the choice of the link form closest to the word, the S2 subsets (defined on the baseline's distance, unchanged), the three-way rule and its 0.15 threshold, the models L0 and L1, folds, seed and settings.

## What changes: the distance

- **Segments.** Strings are lower-cased; accent marks are removed; macrons, underdots, tildes and the palatal and velar nasal signs are kept. A string is cut into segments: an aspirated stop (stop + h or ʰ) is one segment; `ai` and `au` are one segment; anusvara is a nasal segment; visarga is dropped; every other letter with its marks is one segment. Hyphens, asterisks and other signs are dropped.
- **Features.** Consonants: place (velar, palatal, retroflex, dental, labial, glottal), manner (stop, nasal, sibilant, liquid or glide, h), voicing, aspiration. Vowels: quality (a, i, u, e, o, vocalic r, ai, au), length, nasalisation.
- **Cost.** Substituting two consonants costs the share of the four consonant features on which they differ; two vowels, the share of the three vowel features; a vowel for a consonant, or a segment the table does not know for a different segment, costs 1; insertion and deletion cost 1. The distance is the minimum total cost divided by the number of segments in the longer string.
- No parameter is tuned.

## Reported

The S8a tables again: the three-way split by route and subset, the 80% agreement figure where the link changed, and L0 and L1 on dissociated items, each beside its S8a value.

## Reading fixed in advance

- If, among dissociated inherited items, the share with an unchanged link falls below one half, or L1 becomes clearly better than L0 on dissociated items (intervals do not overlap), then the S8a limit was largely an artefact of the coarse comparison, and the paper must say so.
- If neither happens, the S8a finding holds under a finer comparison.
- Either way: the feature table is the assistant's own and is not a validated phonological model; the forms are transliterations of spellings and not phonetic transcriptions; the 0.15 threshold has a different meaning on this scale.
- **Not done, and stated in the paper:** a phonetic comparison for the Romance languages, which would need transcriptions of Latin and of the medieval forms that the project does not have.
