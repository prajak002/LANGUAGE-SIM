# Supplementary analysis S8: the missing link. Does the intermediate stage decide what resemblance cannot? Plan v1.0 (FROZEN)

_2026-10-12. Frozen before the Jambu forms file was downloaded again and before any distance to an intermediate form was computed. SHA-256 in `docs/decision_log.md` (entry 94). Approved by the project lead ("yes" to: re-downloading the Jambu copy of Turner for analysis only, running these analyses, and reframing the paper)._

## Why

Inherited and learned are claims about a path. An inherited word passed through the intermediate stage (Middle Indo-Aryan, Old French, Old Spanish) and carries its changes; a learned word did not. The baseline and the published classifiers compare the modern word with the ancestor only. S8 asks whether the intermediate form separates the two routes on the items where resemblance to the ancestor fails. **It validates no label.**

Seen before freezing: Jambu's `languages.csv` (language names and IDs); the S4 code and totals; a feasibility count of how many sampled Wiktionary entries name an intermediate-stage form, by language and category (e.g. Hindi 227 of 400 inherited, 9 of 400 learned; French 343 and 27), with no distance computed. Not seen: any Middle Indo-Aryan form of any item, any distance involving an intermediate form.

## S8a. Turner's Middle Indo-Aryan forms (seven Indo-Aryan languages)

- **Source.** The Jambu copy of Turner's dictionary, as in S4: analysis only, downloaded to a temporary folder and deleted, nothing from it stored or released except counts and per-item numbers.
- **Items.** Baseline items with route inherited or learned whose etymon matches a Turner head-word (S4's T1, same matcher), and whose matched article or articles list at least one form in **Pali or Prakrit** (Jambu IDs `Pa`, `Pk`). These are *linked items*. The source of the link is the etymon, so it does not depend on Wiktionary's route label.
- **Forms and distance.** Word and etymon are transliterated and normalised exactly as in S4 (`translit`, `norm`: Latin letters, diacritics removed); Turner's forms are normalised with the same `norm`. Distance is the baseline's normalised edit distance on these strings. For an item with word w and etymon a, the link m is the Pali or Prakrit form with the smallest distance to w (the choice most favourable to inheritance). Three numbers: d(w,a), d(w,m), d(a,m).
- **A1. Link-aware model.** Per language, logistic regression (same settings and seed as the baseline, nothing tuned), stratified 5-fold cross-validation on the linked items of that language:
  - L0: d(w,a) alone (resemblance to the ancestor, on the same items and folds);
  - L1: d(w,a), d(w,m), d(a,m);
  - B3 refitted on the same items and folds.
  A language is included if it has at least 10 linked items of each route. **Primary outcome: accuracy on the dissociated linked items** (S2 definition, unchanged), pooled over included languages, for L0, L1 and B3, with Wilson 95% intervals, and the paired table of L1 against B3 on those items. Also reported: accuracy on congruent and middle items, and macro-F1 per language.
- **A2. Three-way split, by a fixed rule and no model.** For each linked item:
  - *link unchanged*: d(a,m) ≤ 0.15. The intermediate form is itself almost the ancestor form, so form cannot decide the route even in principle;
  - *through the link*: d(a,m) > 0.15 and d(w,m) < d(w,a). The word is closer to the intermediate form than to the ancestor;
  - *skips the link*: d(a,m) > 0.15 and d(w,m) ≥ d(w,a). The intermediate form changed and the word does not show the change.
  Counts by Wiktionary route and subset, pooled and per language, with Wilson intervals.
- **Sensitivity, reported beside the main result:** the same with all Jambu languages of clade MIA except `Dard` and `NIA` as the link.
- **Reading fixed in advance.**
  - If L1 is clearly better than L0 and B3 on dissociated items (intervals do not overlap), the intermediate stage carries the information that resemblance lacks. If it is not, that is reported as a negative result.
  - Under A2, an inherited-labelled word that *skips the link* is a candidate for a wrong or semi-learned label; a learned-labelled word that *skips the link* is supported by the classical argument; *link unchanged* items are reported as undecidable by form.
  - Limits fixed here: the normalisation drops vowel length, retroflexion and the sibilant contrast, so real changes are under-counted; Prakrit and Pali are not the direct ancestors of each modern language; the matcher's errors (S4) apply; about 40% of items match several articles and the closest form over all of them is used; coverage is partial and is reported.

## S8b. The intermediate forms that Wiktionary itself records (all families)

- **Items.** Baseline items, inherited or learned, whose own Etymology section names a form in an intermediate language. Intermediate languages fixed here: Old and Middle French (`fro`, `frm`), Old Spanish (`osp`), Old Galician-Portuguese (`roa-opt`), Old Catalan (`roa-oca`), Old Italian (`roa-oit`), Medieval Greek (`gkm`), Middle Armenian (`axm`); for Indo-Aryan, `pi`, `omr`, and any code beginning with `pra` or `inc-` other than `inc-pro`. Forms are read with the audit's template reader.
- **Distance.** The baseline's `normalise` and distance, unchanged. An Indo-Aryan form is used only if all its letters fall in the Devanagari block after normalisation; others (e.g. Brahmi script) are skipped and counted.
- **Measure.** The A2 split, same thresholds, with m the recorded intermediate form closest to the word. Counts by route and subset per family, with Wilson intervals.
- **Reading fixed in advance.** These links were written by the same editors as the labels. S8b measures whether an entry is consistent with itself and cannot support a label. An inherited-labelled entry that skips its own stated link is an internal inconsistency worth a manual check. Spelling is not pronunciation, most of all for French. Learned-labelled entries rarely state an intermediate form; they are reported as counts.

## Conduct

Results are reported whichever way they fall, with coverage. No threshold is changed after results are seen. Per-item outputs from S8a hold only item keys, the three distances and the category; no Turner form is written to disk in the repository, and the per-item file is marked not for release. S8b per-item output derives from Wiktionary alone and may be released.
