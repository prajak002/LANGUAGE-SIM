# Source-grounded evidence extraction: protocol v1.1 (FROZEN)

_2026-10-11. Revision of `docs/evidence_extraction_protocol.md` v1.0 (SHA-256 `4417cffa…cbf71`), which stays unchanged as the record for pilot 1. **Frozen 2026-10-11 on the project lead's approval, before any round-2 item was seen.** The SHA-256 of this file is in `docs/decision_log.md` (entry 67)._

Only the changes from v1.0 are listed. Everything not mentioned here (§1 claims, §3 copyright handling and access conduct, the freeze-before-unblinding order) carries over unchanged.

## Changes from v1.0, and why

| # | Change | Reason (pilot 1 report §4) |
|---|---|---|
| 1 | The unit is **(language, lemma, sense)**, not the lemma | Homographs: কলা and বদ each cover unrelated words |
| 2 | The Wiktionary candidate comes from **etymology templates**, not category membership | `{{dercat|hi|sa|inh=1}}` put उपवास in the "inherited" category although its etymology template is a learned borrowing |
| 3 | **Biswas (Samsad) is dropped** as a source | It gave no etymology for any pilot item |
| 4 | **Turner and J. Dāsa conventions are verified** (§8), so "structural-provisional" is abolished | Both front matters were located and read on 2026-10-11 |
| 5 | Each Turner check records **whether the form carries a loan mark** | Needed to apply the verified convention |
| 6 | Dāsa's *Hindī śabdasāgara* is a **lookup source only** until its conventions are verified | Its front matter has not been read |

## 4′. Unit and fields

- **Item:** one row per (language, lemma, sense). For a lemma with several Wiktionary Etymology sections, each section is a separate item.
- **Blind sheet:** item ID, language, lemma and a **short gloss**. A script takes the gloss from the first definition line under each Etymology section of the stored raw record. The script prints nothing else; the etymology text, templates and categories stay unseen until the freeze.
- **Source-only senses:** a homograph found in a source but absent from Wiktionary is recorded as an extra row flagged `source_only`. It is counted separately and has no Wiktionary comparison.
- **New field in each Turner source check:** `loan_mark` = none / `←` (with the stated donor) / `lw.` / form not listed.
- **`evidence_strength`** is now one of: explicit, structural, none.

## 5′. Label rules by source

These rules decide the label. Phonological diagnostics never decide it alone (guidelines §2).

| Source observation | Route asserted | Strength |
|---|---|---|
| Turner lists the modern form, in that language, among the italic forms of an article, with no loan mark | inherited | structural |
| Turner marks the form `←` or `lw.` | as stated (learned if the donor is Sanskrit; NIA if another modern Indo-Aryan language; external otherwise) | explicit |
| Turner has the etymon but lists no form for the language | not stated | none |
| Platts marks the word S | learned | structural |
| Platts marks the word H and cites a Prakrit form | inherited | structural |
| Platts marks the word H and cites only a Sanskrit equivalent | not stated | none |
| Platts marks the word P, A or T | external | explicit |
| J. Dāsa cites a Pali (পা০) or Prakrit (প্রাকৃ০) form in the etymology | inherited | structural |
| J. Dāsa labels the form বাং প্রাকৃ (Bengali Prakritic form) | adapted Sanskrit form; **route not stated** (candidate SEMI boundary case, recorded in notes) | none |
| J. Dāsa cites only Sanskrit (সং) | not stated | none |
| J. Dāsa cites Persian, Arabic, English or another non-Indo-Aryan language | external | explicit |
| J. Dāsa's register labels (গ্রা০ 'colloquial', প্রা০ 'old', প্রাদে০ 'regional') | **not route evidence** | — |

**Combining sources into a label:**
- **INH:** at least one source asserts inherited, and none asserts another route for the same form.
- **LRN:** at least one source asserts learned, and none asserts another route. A label resting on Platts alone is flagged `single_source_1884`.
- **EXT:** a source states a non-Indo-Aryan donor.
- **DIS:** sources assert different routes for the same form and sense.
- **UNK:** the word is found, but no source asserts a route.
- **NSF:** the word is found in no source.
- **SEMI and MIX** are assigned only on an explicit statement in a source. None of the sources in use has a marker for semi-learned words, so these labels are expected to be unrecoverable. That is reported as a finding and is not worked around.

## 5″. Wiktionary candidate (computed only after the freeze)

A script reads the etymology templates in the item's own Etymology section:

| Template evidence | Candidate |
|---|---|
| `inh` / `inh+` with Sanskrit or a Prakrit as source | INH |
| `lbor` from Sanskrit | LRN |
| `slbor` from Sanskrit | SEMI |
| `bor` / `bor+` from a non-Indo-Aryan language | EXT |
| `bor` / `bor+` from Sanskrit with no learned or semi-learned marking | SKT-BOR (unspecified) |
| `der` only, or templates pointing to more than one route | UNSPEC |
| no etymology template | NOETY |

Category membership is ignored for the candidate. The category-based stratum from the frozen selection v1.0 is kept as a record, and the two are cross-tabulated to size the `dercat` artefact.

## 6′. Round 2

- **Items:** the 38 selected items of practice round 1 not used in pilot 1, split into sense rows by rule 4′. No new Wiktionary fetch.
- **Lookups:** Turner for every item; Platts and Dāsa (Hindi) for Hindi; J. Dāsa for Bengali; Monier-Williams only to confirm an etymon. About 2–3 manual lookups per item, at least 2 s apart.
- **Order of work:** freeze this protocol → blind sheet with glosses → lookups → freeze labels (hash) → unblind → comparison.
- **Report:** raw counts only, pilot 1 and round 2 shown separately. Pilot 1 was labelled under v1.0 and is not relabelled; its rows are re-read under §5′ in a clearly marked secondary table.
- **Spot check:** the project lead checks all pilot 1 rows (pending) and a hash-ordered sample of round-2 source checks. The sample size is the lead's choice and is fixed before the sample is drawn.

## 8′. Source conventions (verified 2026-10-11 unless marked)

**Platts 1884 (verified in v1.0).** Unchanged.

**Turner CDIAL (verified).** Source: DSAL front matter, `https://dsal.uchicago.edu/dictionaries/soas/new_frontmatter.html`, read 2026-10-11. This corrects v1.0 §8, which said the introduction was not available on DSAL.
- Introduction p. x: head-words are in heavy type, and their Middle and New Indo-Aryan descendants are in italic.
- Signs p. xii: `←` means "is a loanword from"; `→` means "is a loanword into"; `<` means derived from; `X` means contaminated by; `*` means hypothetical. Abbreviations p. xii: `lw.` = loanword.
- Preface p. vii: the dictionary presents New Indo-Aryan vocabulary so far as it derives from Sanskrit.
- **Not stated in the front matter:** whether learned Sanskrit loans are systematically excluded, or whether every loan is marked. The inherited reading of an unmarked listing is therefore structural, never explicit.
- Observed use of the marks in the two pilot entries re-checked on 2026-10-11: 2712 marks a Nepali form `←` Maithili; the Bengali forms in 2712 and 3735 carry no mark.

**J. Dāsa, *Bāṅgālā bhāṣāra abhidhāna*, 2nd ed. (verified from page images).** Source: Internet Archive scan `in.ernet.dli.2015.354931` (part 1, 1937), list of abbreviations of the second edition, front matter pp. 26–30. Read from the page images on 2026-10-11; the OCR text of these pages is unusable. No image or text is stored.
- p. 26: গ্রা০ = গ্রাম্য (colloquial or rustic). **A register label.**
- p. 28: পা০ = Pali; প্রাকৃ০ = Prakrit; প্রা০ = প্রাচীন (old), **not Prakrit**; প্রাদে০ = regional use; ফা০ = Persian; বাং প্রাকৃ = Bengali Prakritic form, with loss of visarga given as the example.
- p. 30: হি০ = Hindi.
- First-edition preface (read from OCR only, so **lower confidence**): where no derivation can be given, the word is marked as Sanskrit, Pali or other Prakrit; nothing is written where the origin is unknown; a question mark is used where it is doubtful.
- The scan's copyright status is not stated on its Internet Archive page. The dictionary remains consult-only.

**Dāsa, *Hindī śabdasāgara* (not verified).** Front matter not read. Its entries are recorded, but they assert no route under this protocol.

**Biswas, Samsad.** Dropped.
