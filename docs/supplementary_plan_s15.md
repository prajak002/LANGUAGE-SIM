# Supplementary analysis S15: when the learned labels were set, and by how many accounts. Plan v1.0 (FROZEN)

_2026-10-13. Frozen before any revision list was requested. SHA-256 in `docs/decision_log.md`. Added because the project lead asked to reduce the stated limits of the label-history finding (S1), one of which is that "we did not examine who made the edits or why"._

## Seen before freezing

The S1 and S7b results; the creation dates of three templates (decision log, entry 124). No revision list of any sampled page.

## Question

For the sampled pages whose learned label named a different route in October 2024, when was the label set to learned, and were the changes the work of a few accounts or of many?

## Fixed here

- **Pages:** sample rows of rank at most 60 in a learned category whose state at the 2024-10-11 snapshot is "changed" under `scripts/history_analysis.py` (284 rows expected over the four families).
- **Requests:** one per page to the English Wiktionary interface, at least 4 seconds apart, with the audit's User-Agent: the revisions after the stored 2024 revision, oldest first, at most 50, with text, timestamp and account name. If the server answers 429 or 503 eight times, stop.
- **The change:** the first of those revisions in which the audit's template reader gives the learned route from the ancestor for the language section. If none of the 50 does, the page is "not located".
- **Bots:** one request per 50 distinct account names for their user groups; an account is a bot if it is in the group `bot`.
- **Stored:** per page, the language, the month of the change, a pseudonym of the account (a hash with a random salt that is not kept), and the bot flag, in `data/audit/history_v1/s15_changes.csv`; and the counts in `s15_summary.csv`. **No account name and no page text is stored.**
- **Reported, per family:** pages located; the distribution over months, with the share in the busiest month and in the busiest three; the number of distinct accounts; the share of changes made by the most active account and by the three most active; the share made by bots.

## Reading fixed in advance

- If the most active account or bots together made at least half of the located changes in a family, the paper says that the relabelling there was largely the work of one account or of automated edits. Otherwise it says the changes were spread, and gives the figures.
- This shows when and by how many, not why, and nothing about whether a label is right.
- If fewer than 80% of the pages are located, the figures are given with that share and no reading is made.
