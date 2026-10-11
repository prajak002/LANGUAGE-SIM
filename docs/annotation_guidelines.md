# Annotation guidelines: historical stratum labels (DRAFT v0.1)

_2026-10-10. **Draft for expert review. Not validated; not used yet.** No annotators are recruited and no items are annotated. Expert annotators must revise these rules in a calibration round before any annotation counts._

## 0. Purpose and scope

These rules define the **target labels** before any classification contribution is claimed. Each label is a claim about **historical route of transmission** into a modern Indo-Aryan language (Hindi, Bengali, Assamese, Odia in v1). A label is **not** a judgement of how similar the word looks to Sanskrit.

**The labels are operational.** The traditional tatsama/tadbhava/deśī scheme is contested as an analytic framework. For example, work on Bangla loanword phonology argues that the tripartite division does not account for Bangla syllable-structure and gemination rules and proposes a core/periphery analysis (academia.edu paper, search summary only; to be verified). The labels below are used because they map onto testable routes, not because the scheme is assumed to be complete.

## 1. Labels

| Code | Label | Definition (historical route) | Enters primary test? |
|---|---|---|---|
| **INH** | Inherited (tadbhava) | Continuous transmission from OIA through some Middle Indo-Aryan variety into the language. No specific attested MIA variety is claimed as the ancestor | **Yes**, if the pathway is justified (§3) |
| **LRN** | Learned borrowing (tatsama) | Taken from Sanskrit after the MIA period. The form is Sanskrit apart from regular, language-wide nativisation of spelling and pronunciation (e.g., the language's general treatment of the inherent vowel), and not through MIA sound change | **Yes** |
| **SEMI** | Semi-learned (ardhatatsama) | Taken from Sanskrit after the MIA period, then partly adapted in ways that are not regular MIA development | No (diagnostic) |
| **MIX** | Mixed or complex history | E.g., an inherited word reshaped toward its Sanskrit form (re-Sanskritisation); a learned word reshaped by an inherited relative; analogy; contamination | No (reported) |
| **NIA** | Via another NIA language | Sanskrit-origin or inherited word that entered via another modern Indo-Aryan language (e.g., Hindi formal vocabulary taken via Bengali or Marathi, as noted in general references; search summary only, to be verified) | No (reported) |
| **EXT** | External loan | From a non-Indo-Aryan donor (e.g., Persian, Arabic, Portuguese, English) | No |
| **NON** | Non-Indo-Aryan origin | Deśī/deśaja, or from Dravidian, Munda, Tibeto-Burman or another language, or unknown | No |
| **ETY** | Wrong etymon | The given OIA etymon is not the accepted source | No (counted) |
| **DIS** | Disputed | References give conflicting routes | No (reported) |
| **UNK** | Cannot decide | Insufficient evidence | No (reported) |

## 2. Evidence hierarchy

1. **Primary:** an explicit etymological statement in a scholarly reference, recorded with the entry ID (§5).
2. **Supporting:** phonological diagnostics consistent with the stated route, such as MIA-type changes in INH, or the absence of such changes with Sanskrit-type clusters in LRN. **Diagnostics alone never decide a label.**
3. **Never sufficient:**
   - surface resemblance to Sanskrit;
   - Wiktionary's label;
   - spelling heuristics (e.g., exam-guide rules about particular conjunct letters);
   - any model output.
4. If references conflict, label **DIS** and record both positions.

## 3. Pathway justification (INH items only)

| Code | Meaning |
|---|---|
| **REG-A** | Regular development, and an MIA form is attested in a reference (record the variety, e.g., Pāli or Mahārāṣṭrī Prakrit, and the entry) |
| **REG-U** | Regular development, but no attested MIA form |
| **CPLX** | Requires irregular, analogical or contact explanations. Relabel as **MIX** if transmission itself is in doubt |

Only INH with REG-A or REG-U enters the primary test. An attested MIA form is recorded as **evidence that the stage existed**, never as the direct ancestor of the modern word.

## 4. Fields recorded per item

- `item_id`
- `annotator`
- `label`
- `confidence` (high / medium / low)
- `pathway` (INH only)
- `mia_form`, `mia_variety` (if attested)
- `references` (source and entry ID for each)
- `diagnostics` (free text)
- `notes`
- `time_spent`

## 5. Reference sources for annotators

[PR]: availability and editions to be confirmed. The final list is agreed with the annotators.
- Turner, *A Comparative Dictionary of the Indo-Aryan Languages*, DSAL edition, for consultation.
- Sanskrit dictionaries (e.g., Monier-Williams).
- Pāli dictionaries (e.g., the PTS Pali–English Dictionary).
- Prakrit dictionaries.
- Language-specific historical grammars and etymological dictionaries, e.g., Chatterji 1926 for Bengali. Equivalent works for Hindi, Assamese and Odia are to be named by the annotators.
- Masica 1991 and Cardona & Jain 2003, for terminology.

## 5b. Legitimate non-binary outcomes

- **DIS** and **UNK** are valid, expected outcomes, not annotation failures.
- The inherited-vs.-learned route may not be recoverable from the available documentation for some words.
- Annotators must not force a binary label. Rates of DIS, UNK and MIX are reported as findings about recoverability.

## 6. Procedure

**v3.2 (2026-10-11):** with no experts available, these labels are applied by **source-grounded extraction** (`docs/evidence_extraction_protocol.md`), with an added code **NSF** (no source found). The expert procedure below is kept for a possible later expert route; the practice-round plan is archived at `archive/superseded_2026-10-11/`.


1. **Calibration round.**
   - Annotators independently label a small calibration set, which is not part of any evaluation split.
   - They discuss disagreements.
   - They revise these guidelines (new version number, changes logged).
   - **Worked examples are written by the annotators here.** This draft deliberately contains no example etymologies, to avoid unverified claims.
2. **Independent annotation.**
   - Annotators are blind to Wiktionary labels, other annotators and model outputs.
   - Doublets (two descendants of one etymon) are separate items.
3. **Agreement:** Cohen's κ per language on the full label set and on the binary INH/LRN subset, computed **before** adjudication.
4. **Adjudication:** a third expert resolves disagreements. Unresolvable items are labelled **DIS**.
5. **Reporting:** the label distribution, κ, the share of MIX/DIS/CPLX, and the silver–gold confusion matrix are reported before any model result.

## 7. Open points for the expert calibration round

- How to treat LRN items with heavy but regular orthographic nativisation in Bengali and Assamese, whose spelling is etymological while pronunciation differs.
- Whether SEMI and MIX can be distinguished reliably, or must be merged.
- The minimum evidence needed for REG-U.
- Treatment of words attested only in older NIA stages (e.g., Old or Middle Bengali).
