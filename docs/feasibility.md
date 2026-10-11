# Feasibility: first experiment

_2026-10-10. The previous (sycophancy) feasibility document is archived at `archive/sycophancy_study_2026-10-10/docs/feasibility.md`. Estimates below are rough and labelled as such. Nothing has been run._

## 1. Minimum first experiment

**RQ1 on Hindi and Bengali only, using Wiktionary data:**
- silver labels for training and dev;
- an expert gold test set;
- WFST transducers;
- systems B1–B4, P-latent and P;
- no LLMs.

Assamese and Odia (smaller coverage) are added if the data audit shows enough labelled items. CDIAL/Jambu data are added only if licensed.

**Why this minimum.**
- It tests the one confirmatory claim (C1) with open data and local compute.
- It does not depend on API budget, licence negotiations or a second family.

## 2. Resources

| Resource | Need | Status / risk |
|---|---|---|
| Compute | WFST training by EM on thousands of short string pairs, and bootstrap ensembles. Expected to fit on the local M1 16 GB machine (estimate, unverified) | Low risk |
| Software | Python with `uv`; OpenFst/Pynini or an equivalent WFST library (new dependency, to justify); a transcription tool | Choose in the data-audit stage |
| Storage | Wiktionary extraction: several GB (estimate; size to confirm) | Low risk |
| Data | Wiktionary (open, share-alike); CDIAL/Jambu (blocked); Cristea data (unknown) | **Medium:** MIA coverage in Wiktionary chains is unknown until audited |
| Annotation | Two annotators plus an adjudicator; gold-set size from simulation (protocol §8) | **High:** the binding constraint; none recruited |
| LLM API | Only for RQ3 | Deferred; budget OPEN |

## 3. Sequence and dependencies

| Step | Depends on | Output | Needs approval? |
|---|---|---|---|
| 1. Novelty checks: round 2 done; remaining items in `docs/novelty_audit.md` §4 | — | Updated novelty audit | No (library access may need you) |
| 2. Source verification for Indo-Aryan terminology | Library access | Verified definitions | No |
| 3. Data audit: extract Wiktionary labels and MIA chains; count usable items per language and label; MIA coverage | Step 1 | Data report (counts only; no modelling) | **Yes** (download) |
| 3b. **Label audit:** expert audit of a stratified silver sample (confirmed / semi-learned / mixed-complex / disputed / wrong etymon; pathway justification) | Step 3; annotators | Silver–gold agreement; share of complex items. **Reported before any performance or novelty claim** | **Yes** (recruitment) |
| 4. Transcription and splits | Step 3 | Frozen split files and hashes | No |
| 5. Competitive baselines B1–B4, B6, B7 on dev | Step 4 | Dev metrics (silver labels); C1 comparator chosen and recorded | No |
| 6. P and controls (P-shuffled, P-wrong-stage, P-latent, capacity-matched B4) on dev | Step 4 | Dev metrics | No |
| 7. Power simulation | Steps 5–6 | Gold-set size | No |
| 8. Gold annotation | Step 7; annotators | Gold labels, κ | **Yes** (recruitment) |
| 9. Freeze and preregister | Step 8 | Frozen protocol | **Yes** (your sign-off) |
| 10. Single test evaluation | Step 9 | Confirmatory results | — |
| 11. RQ3 (LLMs), replication | Step 10 | Exploratory results | **Yes** (API, Cristea data) |

**Go/no-go checkpoints:**
- **After step 3:** stop or redesign if usable gold-eligible items or MIA coverage are too few. The thresholds are set from the step-7 simulation logic, not assumed.
- **After step 5:** if B1 is near ceiling on dev (F3), redefine the primary subset **before** any test evaluation.

## 4. Venue fit

Only assessable after results; no outcome is promised.

| Outcome | Possible venue |
|---|---|
| C1 and C2 both supported, plus a clean RQ3 contamination analysis | Plausible for ACL/EMNLP/NAACL main or Findings |
| C1 fails but the dataset and RQ3 are solid | Findings, or workshops (SIGTYP, SIGMORPHON, LChange) |
| Data or annotation fail | Not submittable as planned |

**What separates this from an incremental LLM application:**
- the confirmatory claim concerns a **structural modelling choice** (intermediate stage vs. none), tested by ablation against matched transducers;
- LLMs appear only as a measured, contamination-controlled comparison.
