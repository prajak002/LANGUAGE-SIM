# Route-label benchmark: data sheet (DRAFT, not published)

**Status: prepared locally on 2026-10-11. Not released. Release needs the project lead's sign-off on `LICENSING_REVIEW.md`.**

## What it is

12,777 word senses in 16 languages, each with the route that English Wiktionary records for it (inherited, learned borrowing, or semi-learned borrowing from the ancestor language), the ancestor form, and a measure of how close the word is to that form. Ancestors: Sanskrit (Assamese, Bengali, Gujarati, Hindi, Marathi, Odia, Punjabi), Latin (Catalan, French, Galician, Italian, Portuguese, Romanian, Spanish), Ancient Greek (Greek), Old Armenian (Armenian).

## The split that makes it a benchmark

Each inherited or learned item is in one of three subsets, by its normalised edit distance to the ancestor form:
- **congruent** (6,481): the label agrees with resemblance (inherited and far, or learned and close);
- **middle** (4,517);
- **dissociated** (1,083): the label goes against resemblance (inherited but almost identical to the ancestor form, or learned but far from it).

A system that has learned resemblance scores well on congruent items and badly on dissociated ones. Semi-learned items (696) are kept separately. (A few words occur twice with different ancestor forms; they share one subset and one set of predictions, which is why these counts differ by a handful from the paper's.)

## What is and is not validated

- **The labels are Wiktionary's. They are not gold labels.**
- **Romanian only:** 134 items also carry an expert class from the World Loanword Database (`NB` not borrowed, `BL` borrowed with Latin named). Wiktionary agrees with the expert on 131 of them, including all 6 dissociated ones.
- **No item has been labelled by two independent annotators.** Blind sheets for that are in `data/annotation/expert_kit/`.
- A dissociated item is therefore either a real case where history and form disagree, or a labelling error in Wiktionary. Users must not report accuracy on the dissociated subset as accuracy against history.

## Columns

`language`, `ancestor`, `word`, `ancestor_form_normalised` (lower case, diacritics removed; Bengali, Gujarati, Gurmukhi and Odia letters mapped to Devanagari), `wiktionary_route` (INH, LRN, SEMI), `norm_edit_distance`, `subset`, three baseline predictions (out-of-fold; 1 = learned), `expert_class_romanian_wold`, and the Wiktionary page ID, revision ID, timestamp and URL of the revision read.

## How it was made

Sampling plan, audit, baseline and supplementary plans were each frozen before use (`docs/*plan*.md`, hashes in `docs/decision_log.md`). Up to 400 pages per Wiktionary category and language pair were taken in keyed-hash order; an item is a sense that states exactly one route from the ancestor and gives an ancestor form. Urdu is excluded.

## Known limits

- Classes are balanced by the sampling design and do not reflect running vocabulary.
- Senses with several routes are left out.
- The distance and the subsets depend on a simple normalisation; script mapping for four Indic scripts is approximate.
- One snapshot of Wiktionary (2026-10-11); revision IDs fix what was read.

## Licence and attribution

Derived from English Wiktionary, **CC BY-SA 4.0**; this file must be shared under the same licence, with attribution to Wiktionary contributors and the revision IDs given. The Romanian expert column derives from Kim Schulte, "Romanian vocabulary", in Haspelmath & Tadmor (eds.) 2009, *World Loanword Database*, **CC BY 4.0**.
