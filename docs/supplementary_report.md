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

**Conclusion.** This small model cannot do the task, so the planned question, whether a language model leans on resemblance as the baseline does, **is not answered**. Nothing here supports or weakens the dissociation finding. A larger model was tested afterwards (S5b, below) and was more one-sided. The model's answers are not used for anything else.

## S5b. The same items with a larger model — a second null result

Plan: `docs/supplementary_plan_s5b.md` v1.0 (frozen before the model was queried). **One thing changed from S5, the model:** `gemma3:12b` (11.8 billion parameters, Q4_K_M, ID `b92b218582c5`) through Ollama 0.31.1, run locally on 2026-10-12. Same 2,180 items, same prompts, temperature 0, same seed; 4,360 answers, none unparsed. Results: `data/llm_s5b/s5_scores.csv`, `by_route.csv` and `balanced.csv` (`scripts/llm_by_route.py`); every raw answer is in `answers.jsonl`.

| Family | Condition | Agrees with Wiktionary: congruent | dissociated |
|---|---|---|---|
| Sanskrit (7 languages) | word only | 171/278 (62%) | 145/278 (52%) |
| Sanskrit | word and source form | 173/278 (62%) | 143/278 (51%) |
| Latin (7 languages) | word only | 199/273 (73%) | 187/273 (68%) |
| Latin | word and source form | 204/273 (75%) | 190/273 (70%) |
| Greek | word only | 17/285 (6%) | 268/285 (94%) |
| Greek | word and source form | 16/285 (6%) | 272/285 (95%) |
| Armenian | word only | 34/254 (13%) | 234/254 (92%) |
| Armenian | word and source form | 27/254 (11%) | 241/254 (95%) |

**How to read this table: as an answer bias again, and a stronger one.**

- **The model answers "inherited" in 4,213 of 4,360 answers (97%).** The 4-billion-parameter model did so about four times in five.
- **By route, pooled over the sixteen languages:** it agrees with Wiktionary on 97% to 99% of inherited items and on 5% to 6% of learned ones, in both subsets and both conditions. The agreement figures in the table are therefore the share of inherited items in each cell.
- **Balanced score** (mean of the share correct on inherited and on learned items; cells with at least 20 of each): Sanskrit family 0.50 to 0.51; Latin family 0.54 to 0.60. Greek and Armenian have too few items of one route in each subset for a balanced score.
- **The only movement is in the Latin family and it is small.** The model says "learned" for 12 of 83 congruent learned items and 8 of 92 dissociated ones (word only), and for 18 of 83 and 12 of 92 with the source form shown. The intervals overlap; no claim is made from it.
- **Not a letter bias:** the answer letters were assigned by a fixed hash, and the model chose the "inherited" option under either letter.
- **Its answers match the baseline's about half the time** (499 to 591 of 1,090).

**Run notes.** One request failed with a server error and was asked again. While the model was loaded the machine's swap grew quickly, so from about the 400th answer on the model was unloaded and reloaded every three minutes by a loop outside the script; prompts and settings were unchanged (decision log, entry 89).

**Conclusion.** By the reading fixed in the plan, a model that answers one way almost always gives a **second null result**. The planned question is still not answered, and nothing here supports or weakens the dissociation finding. **The prompts were not changed after S5 and should not be changed now without a new frozen plan**; a prompt adjusted until the bias disappears would be tuned on these results. The model's answers are not used as labels or for anything else.

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

## S7a. Turner's dictionary on the labels that go against resemblance

Plan: `docs/supplementary_plan_s7.md` v1.0 (frozen before the cross-tabulation was computed). Script: `scripts/s7a_turner_by_subset.py`. Results: `data/audit/s7_v1/s7a_turner_by_subset.csv` and `s7a_differences.csv`. Seven Indo-Aryan languages; the S4 flags; no new data.

**Question.** A dissociated item is either a word whose history and form disagree, or a labelling error. Among words that look almost like the Sanskrit form, does Turner's dictionary treat the ones Wiktionary calls inherited differently from the ones it calls learned?

| Group (pooled, 7 languages) | Items | Etymon is a Turner head-word | A listed form matches the word |
|---|---|---|---|
| **Near the Sanskrit form, Wiktionary says inherited** (dissociated) | 141 | 125 | **57 of 125 (46%)** |
| **Near the Sanskrit form, Wiktionary says learned** (congruent) | 1,557 | 996 | **100 of 996 (10%)** |
| Far from the Sanskrit form, Wiktionary says inherited (congruent) | 2,180 | 2,025 | 976 of 2,025 (48%) |
| Far from the Sanskrit form, Wiktionary says learned (dissociated) | 137 | 97 | 5 of 97 (5%) |

- **Main comparison (fixed in the plan): 46% against 10%, a difference of 36 points (95% interval 27 to 45).** The interval excludes zero.
- **The near-Sanskrit words that Wiktionary calls inherited look, in Turner, like any other inherited word** (46% against 48%), and not like learned words of the same closeness (10%).
- **Second comparison:** far from the Sanskrit form, 48% against 5% (difference 43 points; 36 to 47).
- **By language:** the difference is positive in all seven. Only Bengali (18 of 35 against 21 of 177) and Marathi (11 of 40 against 18 of 189) have at least 30 matched items in both groups; in both the interval excludes zero. The other five are reported as counts in the file without interpretation.

**What this shows.** On exactly the items where the form-based models fail (B3 is right on 40 of 278), Wiktionary's label goes with a scholarly dictionary and not with resemblance. Labelling error is an unlikely account of most of the dissociated inherited items.

**What it does not show.**
- **It is not independent confirmation.** Wiktionary's editors cite Turner; the label may have been taken from the same article.
- **The matcher is noisy.** It accepted 3 of 24 forms a hand record had rejected and missed 4 of 14 it had listed. The two groups compared have equally close forms, so the noise should fall on both alike, but a rate here is not a rate of true listings.
- **It concerns the Sanskrit family only**, and it says nothing about the dissociated learned items beyond the 5 of 97.
- No label is validated.

## S8. The missing link: does the intermediate stage decide what resemblance cannot?

Plan: `docs/supplementary_plan_s8.md` v1.0 (frozen before the forms were downloaded again and before any distance to an intermediate form was computed). Scripts: `scripts/s8a_missing_link.py`, `scripts/s8b_recorded_links.py`. Results: `data/audit/s8_v1/`. The Jambu files were held in a temporary folder and deleted after the two runs.

**The idea.** Inherited and learned are claims about a path. An inherited word passed through the intermediate stage and should carry its changes. For each word w with ancestor form a and intermediate form m, a fixed rule sorts it into one of three classes:

- **link unchanged:** m is itself almost the ancestor form (distance at most 0.15), so form cannot decide the route even in principle;
- **through the link:** m changed, and w is closer to m than to a;
- **skips the link:** m changed, and w does not show the change.

### S8a. Turner's Pali and Prakrit forms, seven Indo-Aryan languages

Coverage: 3,276 of 4,893 inherited and learned items have a Turner article with a Pali or Prakrit form (73% to 84% of inherited items by subset, 57% to 62% of learned ones).

| Wiktionary route, subset | Linked items | Link unchanged | Through the link | Skips the link |
|---|---|---|---|---|
| Inherited, all | 1,996 | 692 (35%) | 966 (48%) | 338 (17%) |
| Inherited, congruent (far from Sanskrit) | 1,594 | 437 (27%) | 893 (56%) | 264 (17%) |
| **Inherited, dissociated (near Sanskrit)** | **106** | **88 (83%)** | 0 | 18 (17%) |
| Learned, all | 1,280 | 732 (57%) | 38 (3%) | 510 (40%) |
| **Learned, congruent (near Sanskrit)** | **893** | **539 (60%)** | 1 | 353 (40%) |
| Learned, dissociated (far from Sanskrit) | 85 | 41 (48%) | 14 (16%) | 30 (35%) |

- **Where the link changed, the rule agrees with Wiktionary without any training.** Of the 1,852 linked items whose Pali or Prakrit form differs from the Sanskrit form, 966 inherited ones go through the link and 510 learned ones skip it: 1,476 of 1,852 (80%).
- **The hard items are the ones with nothing to change.** Of the near-Sanskrit words that Wiktionary calls inherited, 83% have a Pali or Prakrit form that is itself almost the Sanskrit form. These are conservative words. Their label can be right, and no comparison of forms can show it.
- **The same holds for most learned words that look like Sanskrit:** 60% have an unchanged link. For the other 40% the classical argument applies (the intermediate form changed, the modern word did not), and it agrees with the learned label.
- **Candidates, with a reason attached:** 18 near-Sanskrit words are labelled inherited although the Pali or Prakrit form changed and the word does not show the change; 338 inherited words in all skip the link. These are candidates for a wrong or semi-learned label, and also include cases where Pali or Prakrit is not the direct ancestor.
- **A1, the planned model comparison: a negative result.** Adding the two link distances to the model does not help on dissociated items: 33 of 191 correct (17%; 13 to 23) against 35 of 191 (18%) for the distance to Sanskrit alone and 19 of 191 (10%) for B3 on the same items and folds. On the 106 dissociated inherited items each model is right on 2. Macro-F1 by language is unchanged or within 0.03. **By the plan's reading, the intermediate form does not rescue the model**, and the split above says why: on these items the link carries no change to detect.
- **Sensitivity (all Middle Indo-Aryan languages as the link):** 86% of dissociated inherited items and 63% of congruent learned ones have an unchanged link; the model result is the same.

### S8b. The intermediate forms Wiktionary itself records, four families

These links were written by the same editors as the labels, so this measures self-consistency only.

| Family | Inherited items with a recorded intermediate form | Through the link | Skips the link | Dissociated inherited: link unchanged |
|---|---|---|---|---|
| Latin (Old French, Old Spanish, Old Galician-Portuguese, Old Catalan) | 1,006 of 2,778 | 917 (91%) | 35 (3%) | 42 of 47 (89%) |
| Sanskrit (forms in a supported script only) | 354 of 2,678 | 291 (82%) | 42 (12%) | 11 of 12 |
| Ancient Greek (Medieval Greek) | 49 of 396 | 36 (73%) | 2 | 4 of 4 |
| Old Armenian (Middle Armenian) | 27 of 394 | 12 (44%) | 1 | 13 of 14 |

- **Inherited entries are consistent with their own stated link** in the Latin family: 99% of congruent ones (531 of 538) go through it.
- **The pattern of S8a repeats in every family:** the inherited words that resemble the ancestor are those whose intermediate form is unchanged (89% in the Latin family; the other families have 4 to 14 such items and are counts only).
- Learned entries almost never state an intermediate form (4 of 2,821 in the Latin family), so nothing is said about them here.
- 1,633 Indo-Aryan intermediate forms were skipped because they are in a script the baseline's normaliser does not handle (mostly Brahmi for Prakrit). Italian and Romanian entries record almost no intermediate form.

### What S8 shows, and what it does not

- **It shows a limit.** For most words that resemble the ancestor, the intermediate stage resembles it too. The route of such a word is a documentary fact (attestation, dating, a dictionary's judgement) and not a property of its form. A classifier scored on these labels cannot be expected to recover it, with or without the intermediate form.
- **It shows where form is enough.** When the intermediate form changed, a rule with no training agrees with the label for 80% of Indo-Aryan items.
- **It does not validate a label.** The rule is orthographic; the normalisation drops vowel length, retroflexion and the sibilant contrast, so changes are under-counted and "link unchanged" is over-counted; Pali and Prakrit are not the direct ancestors of each language; the S4 matcher's errors apply.
- **Note on counts:** subset sizes here differ by up to 7 items from S2 because a few homograph items share a language, title and route.

### S8c. The same with a phonetic distance

Plan: `docs/supplementary_plan_s8c.md` v1.0 (frozen after S8a and before any phonetic distance was computed). Script: `scripts/s8c_phonetic_link.py`. One thing changes from S8a: the distance now works on segments and keeps vowel length, retroflexion, the sibilants, aspiration and nasalisation, with a substitution cost equal to the share of features that differ.

| | S8a (coarse) | **S8c (phonetic, as planned)** | Unit cost on the same segments (added afterwards) |
|---|---|---|---|
| Dissociated inherited items with an unchanged link | 88 of 106 (83%) | **88 of 106 (83%)** | 69 of 106 (65%) |
| Congruent learned items with an unchanged link | 539 of 893 (60%) | 657 of 893 (74%) | 426 of 893 (48%) |
| Rule agrees with the label where the link changed | 1,476 of 1,852 (80%) | 1,266 of 1,499 (84%) | 1,731 of 2,263 (76%) |
| Dissociated items: distance to Sanskrit alone | 35 of 191 | 37 of 191 | 20 of 191 |
| Dissociated items: with the link distances | 33 of 191 | 39 of 191 | 19 of 191 |

- **By the reading fixed in the plan, the S8a finding holds under a finer comparison:** the share of hard inherited items with an unchanged link stays far above one half, and the link-aware model is not better than the distance to Sanskrit alone.
- **Addition, not in the plan:** because a feature-weighted cost makes every distance smaller, the 0.15 threshold is more lenient on that scale. The strictest version (same segments, every substitution costs 1) is given in the last column. Under it 65% of the hard inherited items still have an unchanged link and the models are no better.
- **One implementation error, caught before any result was used:** the first run removed the acute accent from every letter and so turned ś into s. The accent rule was corrected to apply to vowels only, as the plan says, and the analysis rerun. The figures above are from the corrected run; the uncorrected run gave 89 of 106.
- **Limits:** the feature table is the assistant's own and is not a validated phonological model; the strings are transliterated spellings, not transcriptions. **No phonetic comparison was made for the Romance languages**, for lack of transcriptions of Latin and of the medieval forms.

## S9. Expert loan judgements in thirteen languages (IE-CoR)

Plan: `docs/supplementary_plan_s9.md` v1.0 (frozen before any word row was read). Script: `scripts/iecor_expert.py`. Results: `data/audit/iecor_v1/`; the rows used are stored with attribution in `data/external/iecor/` (CC BY 4.0). Source: Heggarty, Anderson & Scarborough 2024, IE-CoR 1.1, a database of 170 basic meanings in which a team of specialists records each word's cognate set and whether it is a loan.

Languages covered: Assamese, Bengali, Hindi, Marathi, Punjabi; Catalan, French, Italian, Portuguese, Romanian, Spanish; Greek; Armenian. (2,231 lexemes. The `Loan` field is empty throughout, so loan status comes from the loan table, as the plan allows.)

**E1. Sampled titles against the experts**

| Wiktionary category | Sampled titles found | Not a loan | Loan, ancestor named | Loan, other donor |
|---|---|---|---|---|
| Inherited | 291 of 5,192 | **277 (95.2%; 92.1 to 97.1)** | 1 | 13 |
| Learned | 21 of 4,721 | 11 | 7 | 3 |
| Semi-learned | 5 of 645 | 4 | 1 | 0 |

- **Inherited labels:** the experts treat 95.2% of the inherited-category words they cover as not a loan. This is the same share as in the Romanian check (S6), now across four families: Sanskrit 107 of 110, Latin 120 of 126, Greek 20 of 21, Armenian 30 of 34.
- **Learned labels:** only 21 words found, below the plan's threshold of 30. Counts only, no claim. (Eleven of them are not loans for the experts; with so few words, and matching by spelling, this cannot be read.)

**E2. Baseline items the experts class as not a loan or as a loan from the ancestor**

| Subset | Items | Wiktionary's label agrees with the experts | B3 agrees with the experts |
|---|---|---|---|
| Congruent | 142 | 137 (96%) | 137 (96%) |
| Middle | 88 | 83 (94%) | 68 (77%) |
| **Dissociated** | **48** | **45 (94%; 83 to 98)** | **22 (46%; 33 to 60)** |

- **On the hard items the experts side with Wiktionary and not with resemblance.** Of the 48 dissociated items, 46 are near-ancestor words that Wiktionary calls inherited; the experts treat 44 of those as not a loan.
- By family (counts only, each below 30): Armenian 20 of 20, Greek 11 of 12, Latin 8 of 9, Sanskrit 6 of 7.
- 32 of the 48 are Greek or Armenian, where dissociated items are common; the Sanskrit and Latin families contribute 16.

**Limits.** Basic vocabulary only, where inherited words dominate. One team's judgement. Matched to Wiktionary by spelling, so a homograph can be mismatched. It does not separate learned from semi-learned borrowing and says nothing usable about learned labels. Romanian is in both expert sources, so the two checks overlap there. This is not a two-annotator validation of the project's items.

## S10. Three input conditions on the same items, with folds grouped by etymon

Plan: `docs/supplementary_plan_s10.md` v1.0 (frozen before it was computed). Script: `scripts/s10_three_conditions.py`. Results: `data/audit/s10_v1/`. Items: the 3,276 linked items of S8a (1,996 inherited, 1,280 learned). Folds keep all items with the same ancestor form together.

| Condition | Macro-F1 | F1 inherited | F1 learned | Congruent (2,487) | Middle (598) | **Dissociated (191)** |
|---|---|---|---|---|---|---|
| A0: word only | 0.781 | 0.852 | 0.711 | 84.1% | 71.6% | **114 (59.7%; 53 to 66)** |
| A1: word and ancestor form | 0.899 | 0.920 | 0.877 | 99.6% | 77.6% | **17 (8.9%; 6 to 14)** |
| A2: word, ancestor and intermediate form | 0.901 | 0.922 | 0.881 | 99.3% | 79.6% | **21 (11.0%; 7 to 16)** |

- **The intermediate form adds nothing on the hard items.** A2 against A1: 21 against 17 of 191, intervals overlapping; on the 106 dissociated inherited items each is right on 2. By the plan's reading the negative result of S8a stands with a richer model and grouped folds.
- **The ancestor form buys the overall score at the cost of the hard items.** Giving the model the ancestor raises macro-F1 from 0.78 to 0.90 and takes it from 60% to 9% on dissociated items: once it can measure resemblance, it follows resemblance.
- **A small gain in the middle band** for learned words (226 to 241 of 302), with overlapping intervals; no claim is made.
- **The dissociated subset is a diagnostic split.** It is defined from the label and the distance to the ancestor, which A1 and A2 see. It is not an independent test set, and the word-only model's 60% is not evidence that it knows the route.

## S11. A character Transformer on the three input conditions

Plan: `docs/supplementary_plan_s11.md` (frozen before any training). Script: `scripts/s11_transformer.py`. Output: `data/audit/s11_v1/`. Run on 2026-10-12 on the project laptop (Apple GPU), 75 trainings, in a temporary environment with PyTorch 2.14.1. The labels are Wiktionary's and are not validated.

Items: 3,276 linked Indo-Aryan items (1,996 inherited, 1,280 learned), seven languages pooled, 5 folds grouped by etymon over all languages. A0–A2 are the S10 logistic models rerun on these folds; T0–T2 are the Transformer (mean of 5 seeds).

| Input | Logistic macro-F1 | Transformer macro-F1 (single seeds) | Logistic, dissociated | Transformer, dissociated |
|---|---|---|---|---|
| Word | 0.789 | 0.777 (0.735–0.765) | 115/191 (60%) | 114/191 (60%) |
| Word and ancestor | 0.900 | 0.858 (0.820–0.836) | 12/191 (6%) | 97/191 (51%; 44–58) |
| Word, ancestor and intermediate | 0.902 | 0.851 (0.815–0.822) | 16/191 (8%) | 102/191 (53%; 46–60) |

- **Planned reading 1 (T2 against T1 on dissociated items):** 102 against 97 of 191, intervals overlap. The statement that the intermediate form does not repair the model stands for the neural model.
- **Planned reading 2 (T1 against A1 on dissociated items):** 97 against 12 of 191, clearly different. As the plan requires, the paper now says so. The Transformer is not the stronger model overall: its macro-F1 is lower and it is right on 92.3% of congruent items where the logistic model is right on 99.8%. It follows resemblance less closely, which leaves it near chance on the dissociated items instead of far below chance. It does not beat the word-only model there (114/191).
- **By route, dissociated:** inherited 45/106 (T1) and 44/106 (T2); learned 52/85 and 58/85.
- **Abstention (planned reading 3):** dissociated items are dropped more often than others: at 90% coverage 153 of 191 are kept (80%), at 50% coverage 41 of 191 (21%; T2: 39). The ones kept are still at chance (21 of 41; T2 21 of 39). Confidence partly identifies these items and does not make the model right on them.
- **Limits:** one architecture and one set of settings, nothing tuned, small data; a different or pretrained model could behave differently. No route or path was predicted.

## S1. Label history (run on the complete fetch, 2026-10-12)

Plan: `docs/supplementary_plan.md` S1 (frozen before any past revision was retrieved). Script: `scripts/history_analysis.py`, unchanged. Output: `data/audit/history_v1/`. Sample: 3,250 sample rows, 2,575 distinct pages, two snapshots each (5,150 stored); no sample row lacks a stored snapshot.

H1 = changed / (same + changed), at the 2024-10-11 snapshot and the 2021-10-11 snapshot, pooled by ancestor:

| Ancestor | Category now | 2024: changed / readable | 2021: changed / readable |
|---|---|---|---|
| Sanskrit | inherited | 2/373 (0.5%) | 1/128 |
| Sanskrit | learned | 22/376 (5.9%; 3.9–8.7) | 50/126 (40%; 32–48) |
| Sanskrit | semi-learned | 28/164 (17%) | 45/57 (79%) |
| Latin | inherited | 2/394 (0.5%) | 1/339 |
| Latin | learned | 259/370 (70%; 65–74) | 171/178 (96%) |
| Latin | semi-learned | 18/265 (6.8%) | 42/120 (35%) |
| Ancient Greek | inherited | 0/53 | 0/46 |
| Ancient Greek | learned | 2/34 | 13/17 |
| Old Armenian | inherited | 0/53 | 0/39 |
| Old Armenian | learned | 1/48 | 2/31 |
| Old Armenian | semi-learned | 1/12 | 3/3 |

- **Inherited labels are stable:** 4 of 873 readable in 2024 named a different route (all four a plain borrowing).
- **Romance learned labels are recent as learned labels:** of the 259 changed in 2024, 258 were then a plain borrowing from Latin (`bor` or `bor+`) and 1 was inherited. A look at six stored 2024 texts confirmed the reading (e.g. `{{bor+|ro|la|Claudius}}`). In every Romance language but Galician (1) between 29 and 59 sampled pages changed this way.
- **Sanskrit:** 20 of the 22 changes in 2024 were from a plain borrowing; 47 of 50 in 2021.
- **Reversals between inherited and learned are rare:** 5 pages now learned were inherited in 2024 (Sanskrit 2, Latin 1, Greek 1, Armenian 1). In 2021, 12 Greek pages now learned were inherited.
- **Semi-learned:** of the pages now semi-learned that named another route in 2024, the Sanskrit family has 15 inherited, 6 learned, 6 plain borrowing and 1 with two routes; the Latin family 9 inherited, 3 learned and 6 plain borrowing.
- **H2 (route added later):** see `history_measures.csv`; an upper bound, as the plan says.
- **Not examined:** who made the edits, when exactly, and on what grounds. "Changed" here mostly means refined from "borrowed" to "learned borrowing", not reversed.

## S7b. Label history by subset

Plan: `docs/supplementary_plan_s7.md` S7b. Script: `scripts/s7b_history_by_subset.py`. Output: `data/audit/s7_v1/s7b_*.csv`.

| Family | Snapshot | Dissociated: changed / n | Congruent: changed / n | Difference in H1 (95%) | Interpreted |
|---|---|---|---|---|---|
| All | 2024 | 8/145 | 87/815 | −0.05 (−0.09 to 0.00) | yes |
| All | 2021 | 11/97 | 74/388 | −0.08 (−0.14 to 0.01) | yes |
| Sanskrit | 2024 | 2/42 | 12/471 | 0.02 (−0.02 to 0.13) | yes |
| Latin | 2024 | 6/34 | 73/275 | −0.09 (−0.20 to 0.08) | yes |
| Ancient Greek | 2024 | 0/37 | 1/33 | −0.03 (−0.15 to 0.07) | yes |
| Old Armenian | 2024 | 0/32 | 1/36 | −0.03 (−0.14 to 0.08) | yes |
| Sanskrit | 2021 | 7/14 | 26/156 | counts only (fewer than 30) | no |

**Reading, as fixed in the plan:** H1 is not clearly higher for dissociated items in any interpretable cell. No claim is made that editors were less certain of them. A stable label is not a correct label.

## Known defect in S8a, S8c, S10 and S11 (found 2026-10-12, not rerun)

These scripts attach the subset by (language, title, route). Where two senses share that key, one can carry the other's subset: at most 21 of 4,893 Indo-Aryan items, of which at most 3 are wrongly counted as dissociated and 6 wrongly left out. No stated conclusion depends on a difference that small. See decision log entry 110.

## Known defect in the template reader (found 2026-10-13, not rerun)

Where a template gives `tr=` before the ancestor form, the reader takes `tr` as the form: 21 baseline items (18 Hindi, 2 Marathi, 1 Romance). Eighteen were counted as dissociated learned items. Without them B3 is right on 27 of 260 dissociated items in the Sanskrit family, against the reported 40 of 278. None is among the linked items or the expert comparisons. See decision log entry 114.
