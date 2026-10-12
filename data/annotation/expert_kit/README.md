# Expert annotation kit (prepared 2026-10-11; nothing here has been annotated)

The paper has no independent human labels. This kit lets two people produce them. **The assistant cannot do this part**, and its own dictionary extraction does not count as independent annotation.

## Hindi and Bengali: independent route labels (90 senses each)

- **Sheets:** `hindi_annotator_A.csv`, `hindi_annotator_B.csv`, `bengali_annotator_A.csv`, `bengali_annotator_B.csv`. A and B are identical. Each row shows the word and a short gloss, and nothing else from Wiktionary.
- **Sample:** up to 30 senses per Wiktionary route (inherited, learned, semi-learned), drawn from the cross-lingual audit sample in keyed-hash order, then mixed. The annotators do not see the route.
- **Who:** two people who can read etymological dictionaries of the language. Each fills their own sheet without seeing the other's and without opening Wiktionary.
- **How:** follow `docs/annotation_guidelines.md` (draft v0.1; an expert should revise it before use). Put one label code in `label` (INH, LRN, SEMI, MIX, NIA, EXT, NON, DIS, UNK), a confidence, and the sources consulted with entry references.
- **Do not open** `_sealed_key_*.csv` until both sheets are complete.

## Priority sheets: the dissociated items (added 2026-10-11)

**Do these first.** They are the items where Wiktionary's label goes against the word's resemblance to Sanskrit (inherited but almost identical to the Sanskrit form, or learned but far from it), mixed with the same number of ordinary items as controls. The baseline models get 14% of them right in the Sanskrit family, so they decide whether the paper has a benchmark or an error rate.

- **Sheets:** `<language>_dissociation_annotator_A.csv` and `_B.csv` for Hindi (78 rows), Bengali (120), Marathi (104), Gujarati (44), Punjabi (124), Odia (50) and Assamese (36). They show the word only.
- **Sealed keys:** `_sealed_key_<language>_dissociation.csv` hold Wiktionary's route and whether the row is a dissociated item or a control. Do not open them before both sheets are complete.
- **Same rules as below:** two people, separately, from dictionaries, without opening Wiktionary. A word may be a homograph; label the sense you find and say which in `notes`.
- **Agreement:** `python3 scripts/annotation_agreement.py <sheet A> <sheet B> <sealed key>` (the key's route column is `wiktionary_route`).
- **What to report:** agreement between the two annotators; then, separately for dissociated items and controls, how often the annotators' agreed label matches Wiktionary.

## Romanian and French: manual dictionary lookups (63 and 85 senses)

Two dictionaries mark borrowing in their etymologies, but neither may be read by a program: CNRTL's robots file disallows its data interface, and dexonline's terms forbid crawling without written consent. A person may consult them in a browser.

- **Sheets:** `romanian_annotator_*.csv`, `french_annotator_*.csv`, each with a `lookup_url`.
- **Record in `etymology_marker_as_printed`** only the marker, not the entry text:
  - Romanian (DEX '09 on dexonline): how the etymology begins, e.g. `Lat.` or `Din fr., lat.` In the two entries the assistant looked at while testing access, an inherited word had a bare `Lat.` and a borrowed one had `Din …`. **This convention has not been verified from the dictionary's front matter; check it before relying on it.**
  - French (TLFi, section "Étymol. et Hist."): whether the etymology says `Empr. au lat.` (borrowed) or `Du lat.` (from Latin). The assistant has not seen any TLFi entry; the page is served by a program interface it may not use.
- **`label`:** LRN if the dictionary states borrowing from Latin, INH if it derives the word from Latin without stating borrowing, UNK otherwise.

## After both sheets are complete

```
python3 scripts/annotation_agreement.py data/annotation/expert_kit/hindi_annotator_A.csv \
        data/annotation/expert_kit/hindi_annotator_B.csv data/annotation/expert_kit/_sealed_key_hindi.csv
```

It prints raw agreement, Cohen's kappa and the confusion tables, between the annotators and of each with Wiktionary. Disagreements are then adjudicated and recorded in a new file; the sheets are kept as filled.

## Limits

- The sample is stratified by Wiktionary's route, so agreement with Wiktionary must be reported per stratum and not as one overall rate.
- 30 per route gives wide intervals. It is enough for a first agreement figure, not for per-class precision and recall.
- Rebuild the sheets (this overwrites them): `python3 scripts/make_expert_kit.py data/raw/wiktionary/crosslingual_v1 data/annotation/expert_kit`.
