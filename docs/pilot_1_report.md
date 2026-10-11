# Pilot 1: source-grounded extraction (10 items) — report

_2026-10-11. Protocol `docs/evidence_extraction_protocol.md` v1.0. Data: `data/annotation/pilot_1/`._

**Counts only. n = 10 supports no inference.**
- Labels are model-extracted and source-grounded (extractor: Claude).
- They are **not** independently validated, and the **spot check by the project lead is pending**.
- This is a pilot of the method, not a result of the study. `research.md` §13 stays empty.

## 1. What was done

1. The pilot rule was frozen (decision log 58).
2. Blind sheet: item ID, language and lemma only.
3. Sources were consulted on DSAL and Cologne at manual scale:
   - Platts 1884 (5 Hindi items);
   - Dāsa, *Hindī śabdasāgara* (2 items);
   - Turner CDIAL (8 lookups);
   - J. Dāsa, *Bāṅgālā bhāṣāra abhidhāna* (5 Bengali items);
   - Biswas, Samsad (4 items);
   - Monier-Williams (1 item).
4. Labels were frozen and hashed (decision log 59).
5. Only then were the stratum mapping and the Wiktionary records opened.

## 2. Coverage and outcomes

| | Hindi | Bengali |
|---|---|---|
| Lemmas found in at least one source | 4/5 | 5/5 |
| Lemmas with **homographs** (different words, one spelling) in the sources | 0 | **2** (কলা, বদ) |
| Sense-level rows | 5 | 7 |

**Source-based labels (12 sense rows):**

| Label | Count | Rows |
|---|---|---|
| LRN | 2 | उपवास, कांड |
| INH | 2 | কলা 'banana', খেত |
| EXT | 2 | कमउम्र, বদ 'bad' |
| UNK | 5 | मिर्गी, যশ, কিংবা, কলা 'lunar digit/art', বদ 'speak' |
| NSF | 1 | यक्षगान |

**Evidence strength:**
- explicit: 2;
- structural, with the convention verified (Platts' S/H/P markers, preface pp. v–vi): 2;
- structural-provisional, where the convention is not verified (Turner listing, Dāsa abbreviations): 2;
- none: 6.

**Recoverability:** 6 of 12 sense rows (5 UNK + 1 NSF) could not be assigned a route from the sources consulted.

## 3. Agreement with Wiktionary (after the freeze)

| Relation | Sense rows |
|---|---|
| Agree | 5: उपवास LRN; कमउम्र EXT; কলা 'banana' INH; খেত INH; বদ 'bad' EXT |
| **Disagree** | **1: कांड.** Source: LRN (Platts S; Turner 3023 lists different inherited Hindi forms). Wiktionary: inherited from Sanskrit काण्ड, with doublet काँड |
| Undecided by sources | 4: मिर्गी and যশ (Wiktionary: SEMI); কিংবা and কলা 'art' (Wiktionary: LRN) |
| No source found | 1: यक्षगान (Wiktionary: LRN) |
| No Wiktionary counterpart | 1: বদ 'speak' |

All four Wiktionary SEMI/LRN items left undecided are cases where the sources give only a Sanskrit equivalent. **This is the boundary the study is about, and the accessible sources do not settle it.**

## 4. Problems found in the method (changes for protocol v1.1)

1. **Homographs.** A lemma is not a well-defined item. কলা and বদ each cover unrelated words.
   - **Change:** the unit becomes (lemma, sense or etymology).
   - The blind sheet should give a short gloss. Glosses don't reveal the route.
2. **Category membership is not an etymology claim.** उपवास entered the hard-boundary (OVL) stratum only because `{{dercat|hi|sa|inh=1}}` adds an "inherited from Sanskrit" category; its etymology template is `lbor` (learned).
   - **Change:** candidate labels and strata for any further selection come from the etymology templates, not category membership.
   - The frozen selection v1.0 is kept as is, and this artefact is reported.
3. **Biswas (Samsad) gives no etymologies** for these items. It is useful only for confirming that a word exists, not for its route.
4. **Unverified conventions limit the evidence.**
   - Turner: whether learned forms appear among the reflexes. The DSAL front-matter PDF is only a bibliographic note.
   - J. Dāsa: the abbreviation list (e.g., গ্রা◦) was not located.
   - Until these are verified, INH evidence from these sources stays "structural-provisional".
5. **Single-source learned labels.** Both LRN rows rest on Platts (1884) alone. Platts marks language assignment, not historical route in the modern sense.
6. **Time per item:** not measured reliably for model extraction, and not comparable to human annotation time.

## 5. Spot check (pending)

The project lead checks each row of `data/annotation/pilot_1/source_checks.csv`:
- open the `query_url`;
- confirm the entry reference;
- confirm the paraphrase matches the entry.

Record discrepancies verbatim in `data/annotation/pilot_1/spot_check.md`. Corrections are logged, never silently overwritten.

## 6. What this pilot does and does not support

**Supports:**
- the extraction procedure is workable at small scale;
- the main obstacle is that accessible sources often do not state the route for Sanskrit-like words.

**Does not support:**
- any claim about the population;
- any accuracy of Wiktionary;
- any classifier feasibility;
- any novelty.

## 7. Addendum, 2026-10-11: conventions verified after the freeze

The frozen files are unchanged (hashes re-checked). This section re-reads the pilot rows under the conventions verified today. **No label changes.**

- **Turner (verified).** The DSAL front matter gives the conventions: italic forms are the head-word's descendants (Introduction p. x), and loans are marked `←` or `lw.` (p. xii). §4 item 4 above said the introduction was unavailable; that was wrong.
  - Entries 2712 and 3735 were re-opened: the Bengali forms carry no loan mark, while a Nepali form in 2712 is marked as a loan from Maithili.
  - Effect: the evidence for কলা 'banana' and খেত moves from "structural-provisional" to **structural**. The front matter does not say that every loan is marked, so it does not become explicit.
- **J. Dāsa (verified from page images of the 1937 edition).** গ্রা০ means "colloquial" (p. 26). It is a register label, not a route statement.
  - Effect: for খেত, J. Dāsa asserts no route beyond the Sanskrit source. The INH label rests on Turner alone.
  - বাং প্রাকৃ ("Bengali Prakritic form", example: loss of visarga, p. 28) is the dictionary's own term for the kind of adaptation seen in যশ. The যশ entry was not re-opened, so whether it carries this label is unknown. যশ stays UNK.
- **Evidence strength under the verified conventions:** explicit 2, structural 4, none 6 (was: explicit 2, structural 2, structural-provisional 2, none 6).

The revised rules are in `docs/evidence_extraction_protocol_v1.1.md` (draft, not frozen).
