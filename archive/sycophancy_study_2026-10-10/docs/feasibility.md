# Feasibility assessment

_2026-10-10. Language facts are sourced in `configs/languages.yaml`. Anything marked TODO is unverified._

## 1. Languages

| Language | Data for parallel MCQ | Expected model competence | Vitality (Glottolog AES, as attributed) | Annotators | Ethics / governance | Verdict |
|---|---|---|---|---|---|---|
| Bengali (ben) | Belebele (Beng + Latn) | Measurable | not endangered | Likely available (large speaker base) | Low risk | **Include** |
| Assamese (asm) | Belebele | Measurable (Shah et al. call it "zero-shot" tier) | not endangered | Recruit | Low risk | **Include** |
| Odia (ory) | Belebele | Measurable ("zero-shot" tier in Shah et al.) | not endangered | Recruit | Low risk | **Include** |
| Hindi, Nepali | Belebele (+ Latn twins) | Measurable | not endangered | Likely available | Low risk | **Include** |
| Santali (sat) | IndicParam only (non-parallel, graduate-level, CC-BY-NC) | Unknown, likely low | threatened (UNESCO Atlas 2010: "Vulnerable") | Recruit; Ol Chiki literacy needed | Moderate; consult community organisations before publishing data | **Exploratory arm** |
| Bodo (brx) | IndicParam only | Unknown, likely low | threatened (UNESCO Atlas 2010: Bodo "Vulnerable") | Recruit | Moderate | **Exploratory arm** |
| Mundari, Ho | None found | Unknown | not endangered (Campbell et al. 2022, 20% certainty comments) | Unknown | Moderate | Exclude (no data) |
| Birhor, Bondo/Remo, Toto | None found | Almost certainly near chance (untested) | shifting (Campbell et al. 2022; "Threatened, 20 percent certain") | Requires community partnership | **High**: small communities, consent, data sovereignty | **Exclude from main study** |

**Why the endangered languages are excluded.** This is about identifiability, not interest.
- KCS needs items the model answers correctly under every option rotation.
- With near-chance competence, the expected number of such items is roughly n·(1/4)⁴ from luck alone, about 0.8 out of 200. Real knowledge would also be near zero.
- So no estimate of sycophancy is possible.

A responsible future study would need:
- a community partner;
- informed consent covering any model-facing use of the language;
- items authored by speakers, not machine-translated;
- an agreement on whether data may be released.

## 2. Annotation needs (pilot)

- Pushback templates: 3 per language × 11 languages. Each needs back-translation plus one fluent validator. The **user** may cover Bengali if fluent; this needs confirming, not assuming.
- Hand audit: 50 random transcripts per model, checked against the scorer.
- Main study: a second validator per language, with agreement reported.

## 3. Data

- **Belebele:** public on HuggingFace (facebook/belebele). Licence TODO: check the dataset card before redistributing derived files.
- **IndicParam:** CC-BY-NC-4.0, so research use only; record this in the paper.
- **IndicTrans2:** MIT checkpoints, used for template drafting only.

## 4. Compute

- **Local:** Apple M1, 16 GB, Ollama. Comfortable for models up to about 4–8B (quantised); 12B is borderline; 27B+ is not practical.
- **Pilot cost:** about 17,600 short calls for one model. Time is estimated at hours, not days, but must be measured, not assumed.
- **Hosted APIs:** no keys configured. The budget is the user's decision. A cost estimate will be produced from pilot token counts before any paid run.

## 5. Schedule

- NAACL 2027 ARR deadline: 2026-10-12, which is **not feasible**.
- Next target: a later ARR cycle (feeding ACL or EMNLP 2027). Dates TODO from aclrollingreview.org.
