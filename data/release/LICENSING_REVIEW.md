# Licensing review (DRAFT for the project lead's sign-off)

_Prepared by the assistant on 2026-10-11 from the licence statements it read. **It is not legal advice, and nothing is released until the project lead signs it off.**_

| Source | What the project took | Licence or terms, as read | In the release package? |
|---|---|---|---|
| English Wiktionary | Wikitext of 13,128 pages (latest revision), category member lists, 48 earlier pages | Text is CC BY-SA 4.0 (stated on the site). Attribution and share-alike required | **Yes.** Words, routes, ancestor forms, revision IDs. Release under CC BY-SA 4.0 |
| World Loanword Database (Romanian) | Form, borrowed status and donor for 2,270 rows | CC BY 4.0 (repository licence field and dataset metadata, read 2026-10-11) | **Yes**, the expert class for 134 items, with citation |
| Platts 1884 (via DSAL) | Entry references and paraphrases | Public domain by age; the DSAL presentation has its own terms, not reviewed | No. Could be released as references and paraphrases after review |
| Turner's comparative dictionary (via DSAL) | Entry references and paraphrases | Copyright notice on the DSAL page: no storing or reproducing without permission of SOAS | **No** |
| J. Dāsa's Bengali dictionary; Dāsa's Hindi dictionary (via DSAL) | Entry references and paraphrases | Hindi dictionary: copyright notice on the DSAL page. Bengali dictionary: status not stated | **No** |
| Chatterji 1926 (Internet Archive scan) | Page references and paraphrases | Item page carries a Public Domain Mark; not independently checked | No. Cited only |
| Jambu database (copy of Turner) | Counts, entry numbers and yes/no flags | **No licence in the repository** | **No.** `data/audit/turner_scale_v1/item_flags.csv.gz` must not be released |
| dexonline (Romanian DEX) | Nothing stored | Licence page read once on 2026-10-11: definitions are under GNU GPL v2 or later, **except** dictionaries listed as having no redistribution right; automated access by robots or scripts is forbidden | No. Not used |
| CNRTL / TLFi (French) | Nothing | Its data interface is disallowed by `robots.txt` | No. Not used |
| Gemma 3 (4b) through Ollama | Model answers to 4,360 prompts | Model terms not reviewed here; only its answers are stored | Not in the package. Review the model's terms before releasing answers |

## Open points for the project lead

1. Confirm the release licence of the benchmark file: **CC BY-SA 4.0** (required by Wiktionary's share-alike).
2. Decide whether the dictionary references and paraphrases of the 48-lemma study are released; the review above only clears Platts on age.
3. The Wikimedia requests used a User-Agent with no contact address. Decide on a contact for future requests.
4. Check the venue's rules on releasing data during anonymous review.
