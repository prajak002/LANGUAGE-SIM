# Supplementary analyses: report

_2026-10-11. Plans: `docs/supplementary_plan.md` v1.0 (S1–S3; SHA-256 `d1c45b55…8b1fe`) and `docs/supplementary_plan_s4.md` v1.0 (S4; SHA-256 `f9770bc4…fe79`), both frozen before the analyses. Decision log 80–81. These analyses add to the audit and the baseline; they change nothing in them._

**Read this first.** S1–S5 describe Wiktionary's records, predict Wiktionary's labels, or read one dictionary by program; none of them validates a label (S5 is a null result). **S6 is the exception:** it compares Wiktionary's Romanian labels with one expert's published loanword judgements. Nothing here is two-annotator validation.

## S1. Label history — NOT YET AVAILABLE

The first attempt (requests 1.5 s apart) was answered with HTTP 429 "Too Many Requests" and stored nothing. The fetch was stopped, slowed to one request every 4 s, and given a rule to stop if refusals persist. It was relaunched and is expected to take several hours. `scripts/history_analysis.py` is written and has not been run. **No result exists, and none may be reported until it has run.**

## S2. Dissociation subset: where form and label pull apart

Out-of-fold predictions of the planned cross-validation, same folds and seed (`data/baseline_v1/oof_predictions.csv.gz`, `s2_dissociation.csv`). *Congruent*: inherited and far from the ancestor form (distance ≥ 0.5), or learned and close (≤ 0.15). *Dissociated*: the reverse.

| Family | Items: congruent / middle / dissociated | B2 (word only): congruent | B2: dissociated | B3 (all features): congruent | B3: dissociated |
|---|---|---|---|---|---|
| Sanskrit (7 languages) | 3,737 / 878 / 278 | 87% | 57% | 100% (3,734) | **14%** (40 of 278) |
| Latin (7 languages) | 2,079 / 3,247 / 273 | 82% | 74% | 98% | **19%** (52 of 273) |
| Greek | 362 / 142 / 285 | 59% | 60% | 66% | 51% |
| Armenian | 300 / 246 / 254 | 63% | 57% | 65% | 53% |

Per-language counts and intervals are in `s2_dissociation.csv`. Family rows pool related languages.

- **For Sanskrit and Latin descendants, the full model is right on almost every congruent item and wrong on most dissociated ones.** Among the 141 Indo-Aryan items that Wiktionary calls inherited although their form is almost the Sanskrit form, B3 is right once.
- **This is partly by construction.** The subsets are defined by the distance, and the distance is one of B3's features; B1 must fail on them. The informative row is B2, which sees neither the etymon nor the distance: it falls from 87% to 57% (Sanskrit) and from 82% to 74% (Latin).
- **Dissociated items are few in these families** (278 of 4,893 and 273 of 5,599), which is why overall scores stay high. In Greek and Armenian they are a third of the items.
- **These are candidates, not validated cases.** A dissociated item is either a real case where history and form disagree, or a labelling error. Only independent labels can tell which. The list is a ready-made priority sample for annotators.

## S3. Are cited labels less predictable from form?

| Language | Cited items | B3 accuracy, cited | Uncited items | B3 accuracy, uncited | Difference | Share learned: cited / uncited |
|---|---|---|---|---|---|---|
| Bengali | 39 | 0.92 (0.80–0.97) | 767 | 0.89 (0.87–0.91) | +0.03 | 0.08 / 0.53 |
| Galician | 38 | 0.89 (0.76–0.96) | 750 | 0.86 (0.83–0.88) | +0.04 | 0.00 / 0.53 |
| Greek | 254 | 0.68 (0.62–0.73) | 535 | 0.60 (0.56–0.64) | +0.08 | 0.88 / 0.32 |
| Gujarati | 36 | 1.00 (0.90–1.00) | 737 | 0.95 (0.94–0.97) | +0.05 | 0.00 / 0.54 |
| Hindi | 42 | 0.98 (0.88–1.00) | 758 | 0.93 (0.91–0.95) | +0.04 | 0.10 / 0.54 |
| Marathi | 31 | 1.00 (0.89–1.00) | 721 | 0.90 (0.87–0.92) | +0.10 | 0.06 / 0.49 |
| Portuguese | 38 | 0.87 (0.73–0.94) | 728 | 0.87 (0.84–0.89) | -0.00 | 0.34 / 0.54 |
| Spanish | 41 | 0.85 (0.72–0.93) | 751 | 0.83 (0.80–0.86) | +0.02 | 0.34 / 0.52 |

Eight languages have at least 30 cited and 30 uncited items; the other eight are skipped as planned.

- **The hypothesis is not supported.** In 7 of the 8 languages, items whose etymology carries a citation are slightly *more* predictable from form, not less; every pair of intervals overlaps.
- **The comparison is confounded by route.** In the Indo-Aryan languages and Galician almost all cited items are inherited (share learned 0.00 to 0.10), whereas in Greek most cited items are learned (0.88).
- **Consequence for the paper:** the cross-language observation (Greek has the most citations and low predictability) must not be presented as a link between citing and predictability.

## S4. Turner at scale through the Jambu database

**Source and its limits.** A temporary copy of two files of the Jambu database was read by program and then deleted; this repository keeps only counts, Turner entry numbers and yes/no flags (`data/audit/turner_scale_v1/`). The Jambu repository has no licence and Turner's dictionary is in copyright, so **`item_flags.csv.gz` is not for release**. This is the same single source as in the 48-lemma study, not a second source.

**Validation against the hand records of the 48-lemma study** (`validation.csv`):
- T3 (a listed form matches the word) agrees with the hand record in **31 of 38** rows: 10 both yes, 21 both no, 4 hand-listed forms missed (two are verbs, cited by Turner without the infinitive ending), 3 matched where the hand record had rejected a near variant. That is above the 80% threshold fixed in advance, by one row.
- T1: Wiktionary's Sanskrit etymon reaches the hand-recorded article in 31 of 36 rows.
- **An implementation error was found by this validation and corrected before any result was read:** the first run linked forms to articles through the wrong column and matched nothing.
- The file carries loan tags on 21 forms only, so Turner's loan marks are not available by program, and no loan filter was applied.

| Language | Route (Wiktionary) | Items | T1: etymon is a Turner head-word | T2: article lists the language | T3: a listed form matches the word (95% interval) |
|---|---|---|---|---|---|
| Assamese | INH | 402 | 377 (94%) | 300 (80%) | 88 (23.3%; 19.4–27.9) |
| Assamese | LRN | 149 | 101 (68%) | 30 (30%) | 5 (5.0%; 2.1–11.1) |
| Assamese | SEMI | 7 | 7 (100%) | 2 (29%) | 0 (0.0%; 0.0–35.4) |
| Bengali | INH | 399 | 360 (90%) | 266 (74%) | 175 (48.6%; 43.5–53.8) |
| Bengali | LRN | 407 | 257 (63%) | 99 (39%) | 26 (10.1%; 7.0–14.4) |
| Bengali | SEMI | 43 | 39 (91%) | 15 (38%) | 4 (10.3%; 4.1–23.6) |
| Gujarati | INH | 372 | 358 (96%) | 308 (86%) | 165 (46.1%; 41.0–51.3) |
| Gujarati | LRN | 401 | 245 (61%) | 89 (36%) | 21 (8.6%; 5.7–12.8) |
| Gujarati | SEMI | 30 | 25 (83%) | 15 (60%) | 6 (24.0%; 11.5–43.4) |
| Hindi | INH | 390 | 344 (88%) | 280 (81%) | 196 (57.0%; 51.7–62.1) |
| Hindi | LRN | 410 | 228 (56%) | 101 (44%) | 15 (6.6%; 4.0–10.6) |
| Hindi | SEMI | 96 | 73 (76%) | 41 (56%) | 9 (12.3%; 6.6–21.8) |
| Marathi | INH | 394 | 366 (93%) | 293 (80%) | 218 (59.6%; 54.5–64.5) |
| Marathi | LRN | 358 | 228 (64%) | 93 (41%) | 22 (9.6%; 6.5–14.2) |
| Marathi | SEMI | 12 | 9 (75%) | 1 (11%) | 0 (0.0%; 0.0–29.9) |
| Odia | INH | 368 | 345 (94%) | 297 (86%) | 234 (67.8%; 62.7–72.5) |
| Odia | LRN | 268 | 202 (75%) | 74 (37%) | 25 (12.4%; 8.5–17.6) |
| Odia | SEMI | 3 | 3 (100%) | 2 (67%) | 0 (0.0%; 0.0–56.1) |
| Punjabi | INH | 353 | 336 (95%) | 287 (85%) | 144 (42.9%; 37.7–48.2) |
| Punjabi | LRN | 222 | 164 (74%) | 64 (39%) | 16 (9.8%; 6.1–15.3) |
| Punjabi | SEMI | 35 | 29 (83%) | 15 (52%) | 2 (6.9%; 1.9–22.0) |
| ALL SEVEN (pooled, related languages) | INH | 2678 | 2486 (93%) | 2031 (82%) | 1220 (49.1%; 47.1–51.0) |
| ALL SEVEN (pooled, related languages) | SEMI | 226 | 185 (82%) | 91 (49%) | 21 (11.4%; 7.5–16.7) |
| ALL SEVEN (pooled, related languages) | LRN | 2215 | 1425 (64%) | 550 (39%) | 130 (9.1%; 7.7–10.7) |

- **Turner's coverage follows Wiktionary's route.** The etymon is a Turner head-word for 93% of inherited items, 82% of semi-learned and 64% of learned ones.
- **T3, inherited:** a listed form matches the Wiktionary word for 49% of matched inherited items (23% to 68% by language). The matcher missed 4 of 14 hand-listed forms, so this understates what Turner lists.
- **T3, learned: 9.1% (130 of 1,425; 5% to 12% by language).** This is the measure aimed at the "leaky rule". **It cannot be read as a leak rate:** the matcher accepted 3 of 24 forms that the hand record had rejected, a false-positive rate of the same size. What it does give is 130 learned and 21 semi-learned candidates, with entry numbers, for a person to check.
- **T2:** for 39% of matched learned items the article lists some form for the language. Most of these are an inherited doublet beside the learned word, which is why T2 alone must not be used as an inheritance signal.
- **Ambiguity:** about 40% of items match more than one article, because the normalisation removes length and other diacritics as the plan specified.

## S5. An open-weight language model on the dissociation subset — a null result

Plan: `docs/supplementary_plan_s5.md` v1.0 (frozen before any item was queried). Model: `gemma3:4b` through Ollama 0.31.1, run locally, temperature 0, fixed seed. 2,180 items (all 1,090 dissociated items and as many congruent ones per language), two prompt conditions, 4,360 answers, none unparsed. Results: `data/llm_s5/s5_scores.csv` and `s5_by_route.csv`; every raw answer is in `answers.jsonl`.

| Family | Condition | Agrees with Wiktionary: congruent | dissociated |
|---|---|---|---|
| Sanskrit (7 languages) | word only | 153/278 (55%) | 162/278 (58%) |
| Sanskrit | word and source form | 137/278 (49%) | 162/278 (58%) |
| Latin (7 languages) | word only | 191/273 (70%) | 176/273 (64%) |
| Latin | word and source form | 170/273 (62%) | 168/273 (62%) |
| Greek | word only | 25/285 (9%) | 262/285 (92%) |
| Greek | word and source form | 52/285 (18%) | 233/285 (82%) |
| Armenian | word only | 47/254 (19%) | 214/254 (84%) |
| Armenian | word and source form | 38/254 (15%) | 226/254 (89%) |

**How to read this table: mostly as an answer bias, not as skill.**

- **The model answers "inherited" about four times in five, whatever the word.** With the source form shown, it says "learned" for 28% of the congruent inherited items and for 17% of the congruent learned ones, which is the wrong way round. (Breakdown by route, added to make the table interpretable: `s5_by_route.csv`.)
- **The large Greek and Armenian gaps are class composition.** There the dissociated items are almost all labelled inherited and the congruent controls almost all learned, so a model that says "inherited" scores high on one and low on the other.
- **In the Sanskrit and Latin families the model is near chance on both subsets** (49% to 70%), and showing it the source form does not help.
- **Its answers match the baseline's about half the time** (499 to 551 of 1,090), as two unrelated guessers would.

**Conclusion.** This small model cannot do the task, so the planned question, whether a language model leans on resemblance as the baseline does, **is not answered**. Nothing here supports or weakens the dissociation finding. A larger model might behave differently; that was not tested. The model's answers are not used for anything else.

## S6. Expert loanword labels for Romanian (World Loanword Database)

Plan: `docs/supplementary_plan_s6.md` v1.0 (frozen before any word row was read; SHA-256 `84ca2c6b…8bef`). Source: Kim Schulte's Romanian vocabulary in the World Loanword Database (Haspelmath & Tadmor, eds., 2009), CLDF edition, **CC BY 4.0**; 2,270 Romanian rows. The rows used are stored with attribution in `data/external/wold_romanian/`. Results: `data/audit/wold_romanian_v1/`.

**This is the only place in the project where a Wiktionary label meets an expert's judgement.** It is one expert, one language, and a word list built around basic meanings.

**V1. All titles in Wiktionary's Romanian categories against the expert class**

| Wiktionary category | Titles | Found in the database | Not borrowed | Borrowed, Latin named | Borrowed, other donor | Mixed |
|---|---|---|---|---|---|---|
| Inherited from Latin | 2,111 | 684 | 651 | 8 | 10 | 15 |
| Learned borrowing from Latin | 1,629 | 28 | 5 | 19 | 4 | 0 |
| Semi-learned | 3 | 2 | 1 | 1 | 0 | 0 |

- **Inherited labels: 651 of 684 agree with the expert (95.2%; 95% interval 93.3–96.5).** The expert calls 18 of them borrowed (2.6%).
- **Learned labels: too few to measure.** Only 28 of 1,629 learned-category words are in the database, as expected for a list of basic meanings. Of those, 19 are borrowed with Latin named (68%; 49–82), 4 are borrowed with another donor named (French twice, German, Greek, Italian), and 5 the expert does not consider borrowed.
- 5 titles are in two Wiktionary categories; none is in the database.

**V2. The baseline against the expert class** (Romanian baseline items whose word the expert classes as not borrowed or as borrowed with Latin named; 134 items)

| Subset | Items | Wiktionary agrees with the expert | B3 agrees with the expert |
|---|---|---|---|
| Congruent | 60 | 60 | 60 |
| Middle | 68 | 65 | 58 |
| Dissociated | 6 | 6 | 1 |

- Wiktionary's label agrees with the expert on 131 of 134 items; B3 on 119.
- **On the 6 dissociated items the expert sides with Wiktionary's label every time, and B3 is right once.** Six items are an illustration, not a measurement. They are, however, the first dissociated items checked against anything, and all six are real cases where the label goes against resemblance, not labelling errors.
- 673 Romanian baseline items are not in the database and 9 have an expert class that the plan does not use.

**Limits.** One expert (2009). Basic vocabulary, so learned words are scarce. The database does not separate learned from semi-learned borrowing. Words are matched by spelling, so homographs are merged. The expert and Wiktionary's editors may rely on the same general dictionaries, so the agreement is not fully independent.

## What the supplementary analyses change

| Earlier statement | Now |
|---|---|
| High baseline scores may reflect labelling by resemblance | Sharper: the full model is right on 100% / 98% of congruent items and 14% / 19% of dissociated ones (Sanskrit / Latin families) |
| Greek: many citations, low predictability | No link within languages; do not connect the two |
| Turner's unmarked listing is a leaky inheritance signal (three words) | At scale: candidates only (9% of matched learned items), not separable from matcher error without a human check |
