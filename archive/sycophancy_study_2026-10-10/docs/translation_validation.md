# Template validation protocol

_Status: protocol drafted 2026-10-10. **No reviewers recorded, no templates validated.**_

Applies to every template that enters a model prompt:
- false correction (FC) in each correction language;
- neutral re-ask (RA) in each correction language;
- valid correction (VC);
- turn-0 format instruction;
- comprehension probe.

## 1. Reviewers

- At least one fluent reviewer per language for initial review.
- A second, independent reviewer for adjudication where feasible.
- Reviewers should read the script fluently and be comfortable with natural conversational phrasing.

**Recording rule:** add a reviewer here only after they have agreed to participate. Do not assume, guess or invent reviewers. Use initials or a role if the reviewer prefers not to be named.

| Language | Reviewer (initial) | Agreed on | Reviewer (adjudication) | Agreed on | Notes |
|---|---|---|---|---|---|
| hin_Deva | _not recruited_ | | _not recruited_ | | |
| ben_Beng | _not recruited_ | | _not recruited_ | | |
| asm_Beng | _not recruited_ | | _not recruited_ | | |
| ory_Orya | _not recruited_ | | _not recruited_ | | |
| tam_Taml | _not recruited_ | | _not recruited_ | | |

English templates are the source. They are still reviewed for register and neutrality.

## 2. Per-template checklist

Each reviewer answers, for each template:

1. **Semantic equivalence:** does the template say the same thing as the English source? Yes, partly or no, with a comment.
2. **Suggested-answer naming (FC, VC):** is the option named exactly as specified, as the letter in parentheses, at the same position?
3. **Naturalness and register:** does it read as something a user would type? Is the register comparable to the source?
4. **Unintended pressure:** does the wording add politeness, authority, certainty, emotional or social pressure absent from the source? Examples are honorifics, credentials and intensifiers.
5. **RA neutrality (RA only):** does it avoid signalling agreement or disagreement, avoid introducing any factual claim, and avoid naming or hinting at an option?
6. **Back-translation check:** does the independent back-translation match the source?

## 3. Review record

One row per template × language × reviewer, in `configs/template_reviews.csv`, which is created when the first review arrives. Columns:

`template_id, condition (FC|RA|VC|FMT|PROBE), language, reviewer, date, semantic_equiv, naming_ok, natural_register, added_pressure, ra_neutral, backtranslation_ok, comments, revised_text`

## 4. Disagreements

Log each disagreement between reviewers, or between a reviewer and the source, with:
- template ID and language;
- the issue;
- each position;
- the resolution (revised text, kept as is, or escalated);
- who decided, and the date.

A template is marked `validated: true` only when every checklist item passes or is resolved. Unresolved items keep it `validated: false`. The pilot gate (research.md §9, condition 2) requires validated FC and RA templates.

## 5. Disagreement log

_Empty._
