# Feasibility report: source-grounded route labels for 48 Wiktionary lemmas

_2026-10-11. Pilot 1 (10 lemmas, protocol v1.0) plus round 2 (38 lemmas, protocol v1.1). Data: `data/annotation/pilot_1/`, `data/annotation/round_2/`. Decision log 58–69._

**Read this first.**
- **Counts only.** 48 lemmas chosen to over-sample hard cases; no rate here estimates anything about Hindi or Bengali vocabulary.
- Labels are **model-extracted** (extractor: Claude) from published dictionaries. They are not validated gold labels, and there is no inter-annotator agreement.
- **No human has checked the extraction yet.** The pilot 1 spot check is still blank, and the round-2 spot check has not started.
- `research.md` §13 stays empty. This is a feasibility finding about the method, not a result of the classifier study.

## 1. Answer to RQ-F in one paragraph

With the dictionaries that are freely consultable online, a route could be assigned to **26 of 58 sense rows**. Almost all of those are either inherited words that Turner lists, or Hindi words that Platts marks as Sanskrit. **The boundary the project cares about was not recoverable:** none of the 12 words Wiktionary calls semi-learned, and none of the 9 Bengali words it calls learned, could be labelled as such from the sources. Where the sources do decide, they agree with Wiktionary on 22 of 26 rows, but that agreement is not independent, because Wiktionary cites Turner on many of the same pages.

## 2. What was done

| | Pilot 1 | Round 2 |
|---|---|---|
| Protocol | v1.0 (lemma-level) | v1.1 (sense-level, frozen before items were seen) |
| Lemmas / sense rows | 10 / 12 | 38 / 46 |
| Source checks recorded | 23 | 111 |
| Labels frozen before Wiktionary was opened | yes (log 59) | yes (log 68) |
| Spot check by the project lead | pending | not started |

Sources used in round 2: Platts 1884 and Turner CDIAL (route sources); J. Dāsa's Bengali dictionary (route source for Bengali); Dāsa's *Hindī śabdasāgara* (lookup only, asserts no route under v1.1).

## 3. Outcomes

**Source-based labels (sense rows):**

| Label | Pilot 1 | Round 2 | Total |
|---|---|---|---|
| INH | 2 | 13 | 15 |
| LRN | 2 | 4 | 6 |
| EXT | 2 | 3 | 5 |
| SEMI / MIX / DIS | 0 | 0 | 0 |
| UNK (found, no route stated) | 5 | 17 | 22 |
| NSF (in no source) | 1 | 9 | 10 |
| **Total** | 12 | 46 | 58 |

**By language, round 2:**

| | INH | LRN | EXT | UNK | NSF |
|---|---|---|---|---|---|
| Hindi (23 rows) | 8 | 4 | 2 | 8 | 1 |
| Bengali (23 rows) | 5 | 0 | 1 | 9 | 8 |

**Evidence strength, all 58 rows:** explicit 5; structural 21; none 32. Every explicit row is an external loan. No inherited or learned label rests on an explicit statement.

## 4. Recoverability by Wiktionary's own category

The Wiktionary candidate is read from the etymology templates of each sense (v1.1 §5″).

| Wiktionary candidate | Rows | Source label matches | Source gives another label | UNK | NSF |
|---|---|---|---|---|---|
| Inherited | 16 | 12 | 0 | 3 | 1 |
| Learned | 19 | 5 (all Hindi) | 1 (INH) | 10 | 3 |
| Semi-learned | 12 | **0** | 2 (INH) | 7 | 3 |
| External | 8 | 5 | 0 | 0 | 3 |
| Unspecified, unknown or no counterpart | 3 | — | — | 2 | 0 |

The third unspecified row is कांड, which the sources label LRN (see §5).

**Three structural gaps explain most of this table:**
1. **No source marks semi-learned words.** The category cannot be recovered by this method at all.
2. **Bengali has no equivalent of Platts' S marker.** J. Dāsa gives a Sanskrit analysis for inherited-looking and learned-looking words alike, so no Bengali word could be labelled learned (0 of 9 across both rounds).
3. **Hindi learned labels rest on one 1884 source.** All 6 LRN rows come from Platts' S marker alone.

## 5. Agreement with Wiktionary

| Relation | Pilot 1 | Round 2 | Total |
|---|---|---|---|
| Agree | 5 | 17 | 22 |
| Disagree | 0 | 3 | 3 |
| Candidate unspecified | 1 | 0 | 1 |
| Undecided by sources | 4 | 17 | 21 |
| No source found | 1 | 9 | 10 |
| No Wiktionary counterpart | 1 | 0 | 1 |

- **Disagreements (round 2):**
  - बाँचना 'to read': sources INH (Platts cites a Prakrit form); Wiktionary semi-learned.
  - अमावस 'new moon': sources INH (Turner lists it); Wiktionary semi-learned "through" a Prakrit form.
  - ভাল 'forehead': sources INH (Turner lists it); Wiktionary learned.
- **कांड (pilot 1) is reclassified here.** The pilot report counted it as a disagreement (sources LRN, Wiktionary inherited). Read by templates, the page carries both a borrowing template and an inheritance template, so the candidate is "unspecified". The pilot report is left as written.
- **The agreement is not independent.** In round 2, 8 of the 17 agreeing rows are on pages that cite Turner's dictionary themselves (checked at page level, not per sense).

## 6. Weaknesses found in the label rules

1. **Turner's unmarked listing is a leaky signal for "inherited".** The verified convention is that listed forms are descendants and that loans are marked. But Turner lists forms identical to the Sanskrit word without a loan mark (H. *hāni*, B. *kamalā* 'orange', B. *bhāl*). The front matter does not say that every loan is marked. 11 of the 13 round-2 INH labels use this rule, and 10 of them have no other support.
2. **"Form listed" needed judgement.** Near variants were not counted (পাহারা vs *paharā*; ठंड vs *ṭhaṇḍh*; জ্বী vs *ji*). A looser rule would move 2 rows from UNK to INH.
3. **The Turner head-word was often the extractor's choice**, taken from the language dictionary's etymology where one was given. A wrong guess produces a false "not listed".
4. **Spelling and encoding cost coverage.** J. Dāsa uses older spellings (সর্ব্বদা, ইহুদী); 8 of 23 Bengali rows are NSF, and some of those may be search failures, not absences.
5. **Two Wiktionary sections had no definition line** (সোয়াদ etymology 1, অর্পিতা), so the blind sheet had no gloss for them. Both are NSF.

## 7. The selection strata did not mean what they were designed to mean

- **OVL ("hard boundary") is mostly homographs.** Of the 6 OVL lemmas, 5 are two unrelated words under one spelling, one inherited and one learned (কলা, पुरा, नाक, কমলা, ভাল). The sixth (उपवास) is the `dercat` artefact. None is a single word with a contested route.
- **Category and template disagree for 4 of the 46 round-2 rows:** সোয়াদ (two Arabic homographs in the semi-learned stratum), सेंत 'free' (marked unknown), and सैर 'plough' (learned, in the Arabic stratum).

## 8. Recommendation on scaling up

**Do not scale up this protocol as it stands.** A larger sample would mostly measure how many inherited words Turner lists. It would add nothing on the learned / semi-learned boundary, because the sources have no way to express it.

Three options, in the order I would consider them:

1. **Add a source that states routes for Bengali and for semi-learned words, then rerun on these same 48 lemmas.** Chatterji's *Origin and Development of the Bengali Language* is the obvious candidate: Turner cites it in several of the entries consulted. I have not read it, and I do not know whether an accessible copy exists. This is a small, reversible check.
2. **Write the feasibility finding up as it is**, as a short negative-result paper: what freely accessible etymological dictionaries can and cannot decide. It would need the spot check done and a sample that is not hand-stratified. 58 rows is thin for a venue like NAACL.
3. **Stop here** and return to the question of expert annotators, since the classifier study (RQ1–RQ3) needs labels this method cannot supply.

## 9. What must happen before any of this is cited

- The project lead completes the pilot 1 spot check (`data/annotation/pilot_1/spot_check.md`, 23 rows).
- The project lead fixes a sample size and checks that many rows from the top of `data/annotation/round_2/spot_check.md` (the 111 checks in hash order).
- Discrepancies are logged, and the counts above are recomputed if any label changes.
