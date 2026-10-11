# Data, licensing, expert review and ethics

_2026-10-10. Evidence labels: **[checked]** verified this session; **[search]** from a search summary; **[PR]** background knowledge, to verify. Nothing has been downloaded._

## 1. Data sources

| Source | Content | Coverage | Licence / permitted use | Redistribution | Status |
|---|---|---|---|---|---|
| English Wiktionary | Etymology templates: inherited, learned, semi-learned; MIA chains | hi, bn, as, or (counts in `literature/review.md` §7) | CC BY-SA (plus GFDL) [PR: verify current terms] | Share-alike: derived label files must carry the same licence | Category counts [checked]; dump not downloaded |
| wiktextract / kaikki.org JSON | Machine-readable Wiktionary extraction | As Wiktionary | As Wiktionary [PR] | As Wiktionary | Not checked |
| EtymDB 2.0 (Fourrier & Sagot 2020) | Wiktionary-derived etymological relations | 2,536 languages [search] | CC BY-SA 4.0 [search] | Share-alike | Not checked; may be outdated relative to current Wiktionary |
| Jambu (Arora et al. 2023) | About 287k lemmata; CDIAL- and DEDR-derived cognate sets | 602 lects | **No licence file** in github.com/moli-mandala/data [checked, GitHub API]; CDIAL used "with SARVA project approval for academic purposes" [checked, paper] | **Not permitted without permission** | Blocked: contact the authors |
| Turner, CDIAL (DSAL edition) | OIA etyma; MIA and NIA reflexes | Indo-Aryan | © Turner estate; reproduction requires SOAS permission [search] | No | Blocked: contact SOAS |
| Cristea et al. 2021 Romance dataset | Inherited vs. learned Latin words | ro it fr es pt ca | Not checked | Unknown | Needed only for the replication arm |
| Pāli, Prakrit and Sanskrit dictionaries (e.g., PTS Pali–English Dictionary, Monier-Williams; DSAL editions) | Reference for annotators | — | Copyright varies [PR] | Consultation only | Annotators consult; nothing redistributed |

**Data-quality notes:**
- Wiktionary labels are community-edited and probably often derived from Turner, which creates circularity risk (protocol §3).
- Coverage is biased toward frequent words.
- Bengali and Assamese share a script but differ in orthographic conventions.
- Tatsamas retain Sanskrit spelling in native scripts, so orthographic input may make the task trivially easy (failure check F3). Phonological transcription is therefore an OPEN decision.

## 2. Historical-validity rules

- **OIA** means the dictionary headword layer, mostly Sanskrit. It is **not** a claim that Classical Sanskrit is the direct parent of any modern language.
- **MIA** attestations are Pāli and literary Prakrits. They are proxies for the intermediate stage, not direct ancestors of specific modern languages. Apabhraṃśa is unevenly documented.
- **Stage terminology** must be verified against Masica 1991, Cardona & Jain 2003 and Chatterji 1926 [PR] before the paper is written.
- **Geography is never used to infer genealogy.** Modern speaker locations are not historical distributions.

## 3. Expert review

- **Gold annotation:** at least two annotators trained in Indo-Aryan historical linguistics (ideally covering Bengali/Assamese/Odia and Hindi), plus one adjudicator.
- **Recruitment:** none recruited. Reviewers are recorded only after they agree to participate. Names are never assumed or invented.
- **Compensation and credit:** OPEN. Annotators should be acknowledged, or offered authorship where contribution warrants.
- **Confirmation-bias controls:**
  - blind to Wiktionary labels and model outputs;
  - independent first-pass labels;
  - contested items reported, not hidden.

## 4. Community and ethical considerations

- **First experiment:** major, well-documented languages (Hindi, Bengali, Assamese, Odia) and published scholarly data. The main obligations are licensing, attribution and share-alike compliance. There is no community-held or culturally sensitive material.
- **Assamese and Odia** have smaller Wiktionary coverage. Results there must not be presented as authoritative etymologies. Outputs are hypotheses for expert review.
- **Endangered and Indigenous languages are out of scope** for the first experiment. Any later stage requires:
  - community partnership and consent;
  - data-sovereignty agreements following the CARE principles (Carroll et al. 2020, doi:10.5334/dsj-2020-043);
  - access restrictions honoured;
  - benefit sharing;
  - no publication of restricted material.
- **Preservation claims:** producing a dataset or predictions is not "preserving a language". Preservation value would have to be evaluated with linguists and communities (a later stage), and is not claimed here.

## 5. Approvals needed before any data work

1. Download of a Wiktionary dump or extraction.
2. Contacting SOAS and the Jambu authors about licences.
3. Contacting Cristea et al. for their dataset (replication arm).
4. Any LLM API use (RQ3).
5. Annotator recruitment and compensation.
