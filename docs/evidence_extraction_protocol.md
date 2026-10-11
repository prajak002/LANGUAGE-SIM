# Source-grounded evidence extraction: protocol v1.0

_2026-10-11. Replaces the expert practice round, which is archived at `archive/superseded_2026-10-11/annotation_practice_round.md` (decision log 56). **The pilot rule in §6 is frozen before any pilot item's title is seen.**_

## 1. What this produces, and what it does not

- **It produces source-grounded labels.** Each label is tied to a specific published source, an entry reference and the evidence used, so anyone can check it.
- **The labels are model-extracted.**
  - Extractor: Claude, an AI assistant.
  - Spot-checker: the project lead (agreed 2026-10-11).
- **It does not produce independently validated expert labels.** Neither the extraction nor the spot check is described that way.
- **No inter-annotator agreement is reported.** There is one extractor, and model output is not an independent annotator.
- **The spot check verifies extraction fidelity:** does the cited entry say what is recorded? It does not verify historical correctness.

## 2. Research question served (feasibility; `research.md` §0)

Can published etymological evidence be turned into consistent historical-route categories for Hindi and Bengali? Specifically:
- How often is the route recoverable from that evidence?
- How often do sources agree with each other and with Wiktionary?
- Which category boundaries break down?

## 3. Sources and handling rules

| Source | Access | Copyright status (as stated on the DSAL page, 2026-10-11) | Handling |
|---|---|---|---|
| Turner, *A Comparative Dictionary of the Indo-Aryan Languages* (1962–66; supplements 1969–85) | DSAL online | © Turner estate. "No part … may be stored, transmitted … or reproduced in any form … without the permission of" SOAS | **Consult only.** Record the entry number, headword and query URL, plus **our own paraphrase**. No verbatim text and no stored pages |
| Dāsa, *Hindī śabdasāgara* (1965–75) | DSAL | © Nāgarī Pracāriṇī Sabhā, same restriction | Consult only, as above |
| Biswas, *Samsad Bengali–English Dictionary* (3rd ed., 2000) | DSAL | © Shishu Sahitya Samsad, same restriction | Consult only, as above |
| Platts, *A Dictionary of Urdū, Classical Hindī, and English* (1884) | DSAL | Public domain (published 1884) | Short quotations of the etymology field are allowed |
| Dāsa, Jñānendramohana, *Bāṅgālā bhāṣāra abhidhāna* (2nd ed., preface 1937) | DSAL | No notice shown; status unverified | Treat as consult-only |
| Pali Text Society, *Pali–English Dictionary* (1921–25) | DSAL | No notice shown; status unverified | Consult only |
| Sheth, *Pāia-sadda-mahaṇṇavo* (1923–28) | DSAL | No notice shown; status unverified | Consult only |
| Monier-Williams, *Sanskrit–English Dictionary* (1899) | Cologne Digital Sanskrit Dictionaries | Licence of the digital edition not yet checked | Consult only until checked |
| Wiktionary (CC BY-SA 4.0 / GFDL) | Raw records already stored | — | **Candidate only.** Consulted **after** the source-based label is frozen (§5 step 4) |

Recording a cited word form (e.g., a Prakrit form as a fact) and an entry reference is citation, not reproduction of the dictionary.

**Access conduct:** manual-scale lookups only, at least 2 s apart, with a descriptive User-Agent. No crawling and no bulk queries.

## 4. Fields per item

| Field | Content |
|---|---|
| `item_id` | Hash-based ID; no stratum information |
| `lang`, `lemma` | — |
| `source_checks` | One row per source consulted, with: the source, the query made, `found` (yes/no), the entry reference, the route evidence (our paraphrase, or a short quotation for Platts only), and the route asserted (see below) |
| `label` | Annotation-guidelines label set, plus **NSF** (no source found). Assigned by the evidence hierarchy (guidelines §2); diagnostics never decide alone |
| `evidence_strength` | **explicit:** a source states the route. **structural:** the route follows from how the source treats the word, by a convention documented in its front matter. **none** |
| `extractor_confidence` | high / medium / low |
| `notes` | — |

The **route asserted** values are: inherited, learned, semi-learned, external, other, or not stated.

Conventions inferred from a source's layout (e.g., how Platts marks Sanskrit loans versus Prakrit-derived words, or whether Turner lists learned forms) count as **structural** evidence only after they are verified in that source's front matter and recorded in §8.

## 5. Procedure

1. **Blind sheet:** item ID, language and lemma only. It is generated from the raw records without the stratum or the Wiktionary etymology.
2. **Look up each item:**
   - Turner, searching for the modern form;
   - the language dictionary (Platts and Dāsa for Hindi; Dāsa (Bengali) and Biswas for Bengali);
   - MIA dictionaries when a cited MIA form needs confirming.
3. **Assign the label.** Conflicting sources give **DIS**. Insufficient evidence gives **UNK**. No entry anywhere gives **NSF**. A binary label is never forced.
4. **Freeze** the source-based labels with a SHA-256 hash in the decision log. **Only then** unblind the Wiktionary candidate (category plus etymology templates) and record agreement.
5. **Spot check:** the project lead checks the cited entries for a random sample (in the pilot, all items) and records any discrepancy verbatim. Corrections are logged and never silently overwritten.

## 6. Pilot (rule FROZEN before titles are seen)

- **Items:** for each language, the lowest-ranked `selected` item in each of the strata OVL, SEMI, LRN, INH and EXT-FA, from `data/raw/wiktionary/practice_round_1/selection_log.csv`. That gives 10 items.
- **Output:** `data/annotation/pilot_1/`, containing the blind sheet, `extraction.csv` and the post-freeze comparison.
- **Report:**
  - coverage per source;
  - the label distribution, including DIS, UNK and NSF;
  - the evidence-strength distribution;
  - source–source and source–Wiktionary agreement as raw counts;
  - time per item.
- **No statistics beyond counts.** n = 10 supports no inference.

## 7. Measures for the full feasibility study (after the pilot)

- **Coverage:** the share of items with any source, and with explicit evidence.
- **Recoverability:** the shares of DIS, UNK, NSF and MIX.
- **Inter-source agreement:** a contingency table between sources. This is a documentary finding, not annotator reliability.
- **Wiktionary–source agreement:** per candidate category.
- **Boundary failures:** which label pairs the evidence fails to separate.

## 8. Source conventions (to be filled from front matter, with page references)

**Platts 1884 (verified).** Source: Preface pp. v–vi, from the public-domain scan, archive.org `platts-a-dictionary-of-urdu-classical-hindi-and-english-1884`.
- The initial letter before a headword gives the language the word is *assigned to*: H (Hindustani/Hindi), S (Sanskrit), P (Persian), A (Arabic), T (Turkish).
- The source, when known, is given in brackets.
- "In the vast majority of instances, not being able to discover the Prakrit source of a Hindī word, I have contented myself by giving … the Sanskrit equivalent alone."
- **Use:**
  - S = structural evidence for LRN;
  - H with a Prk. form = structural support for INH;
  - H with only an S. equivalent = **no route evidence**.

**Turner CDIAL (not verified).** The main-volume introduction is not available on DSAL; the front-matter PDF is a one-paragraph note. Whether learned forms appear among the reflexes is unknown, so a Turner listing counts as structural-provisional.

**J. Dāsa, *Bāṅgālā bhāṣāra abhidhāna* (not verified).** The abbreviation list was not located (e.g., গ্রা◦, ফা◦, হি◦, প্রাকৃ◦).

**Biswas, Samsad.** No etymologies were observed for the pilot items. Not a route source.
