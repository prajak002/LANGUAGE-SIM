# Submission package: quality and compliance report

Prepared 2026-10-13. Everything below was checked by running it, not estimated.

## Official rules, as read today

| Item | Rule | Source |
|---|---|---|
| Long paper length | 8 pages of content | NAACL 2027 call for main conference papers; ARR call for papers |
| Limitations | Required, titled "Limitations", at the end before the references, not counted | ARR call for papers |
| Ethical considerations | Optional, after the conclusion, not counted | ARR call for papers |
| References, appendices | Unlimited, not counted | ARR call for papers |
| Anonymity | Two-way anonymized; supplementary material and links must be anonymized; no download-tracking hosts | ARR call for papers |
| ARR submission deadline | 12 October 2026, 11:59 p.m. anywhere on earth | NAACL 2027 call; ARR dates page |
| NAACL commitment deadline | 23 December 2026 | NAACL 2027 call |

**Deadline status:** by this machine's clock the package was finished at about 22:00 on 12 October anywhere on earth, so the deadline was still open, with about two hours left.

**Also required by ARR from October 2026, and not something this package can do:** every author needs a complete OpenReview profile with an ORCID, a qualified service contributor must be named for the submission, and the Responsible NLP checklist is due within 48 hours of the deadline.

## The paper

| Check | Result |
|---|---|
| Template | Official ACL style, `\usepackage[review]{acl}`, style files unmodified |
| Compiles | Yes, from a clean unzip of `paper_source.zip`, with no error and no undefined reference (tectonic). Not tested with pdfLaTeX; the source is ASCII-only |
| Total pages | 15 |
| Main content | Ends on the last line of page 8, with the Conclusion. Limitations begins page 9 |
| Limitations | Present, after the Conclusion, before the references |
| Distinct cited works | 20, all used |
| Abstract | 250 words |
| Anonymity | No author, affiliation, acknowledgement or repository link. PDF metadata has no author field |
| Em dashes | None |

## The supplementary page

| Check | Result |
|---|---|
| Single file | Yes, `index.html`, about 54 KB, no external asset or script |
| Anonymous | No author, institution or venue name (checked by assertion in the generator) |
| Numbers | Read from the result files by `scripts/make_supplementary_site.py` |
| Structure | Tags balanced, all in-page links resolve, script passes a syntax check |
| Rendering | First screen checked in a rendered preview |
| Copy buttons | Code reviewed and syntax-checked; **not clicked in a browser** |

## What was changed in this pass

- The two-pass annotation result was removed from the paper, because the lead disputes who filled those sheets. Nothing else in the paper depended on it.
- Contributions and recommended practices are now short bulleted lists, and a Conclusion section was added.
- The introduction opens with the general question (what a score on labels from a collaborative resource measures), the parts are presented as one four-step argument, and the Conclusion states three lessons for other such labels.
- The Limitations section is four short paragraphs instead of a list of fifteen items. Every limitation is still stated; details of the corrected defects moved to the appendix.
- The framing no longer calls resemblance a shortcut. Majority rates and balanced accuracy replace "chance".

## What was not done

- **Semicolons** were not removed throughout. The abstract has none.
- **A methodology/experimental-setup/results split** was not imposed. The paper keeps its own structure (audit, baseline, hard items, dictionary study), which follows the argument.
- **The disclosure that a language model made the dictionary lookups of the 48-lemma study was kept.** That is not disputed, it is in the project's records, and reporting those counts without it would mislead.
- **Three cited papers** (Gururangan et al. 2018, McCoy et al. 2019, Poliak et al. 2018) were read as abstracts only.
- **Table 1 glosses and transliterations** have not been checked by an author.

## Self-assessment, out of 10

| Dimension | Score |
|---|---|
| Research significance and relevance | 6 |
| Clarity of the research gap | 7 |
| Originality and contribution | 6 |
| Technical correctness | 7 |
| Experimental rigor | 6 |
| Quality of the literature comparison | 6 |
| Strength of the results analysis | 7 |
| Writing quality and organization | 7 |
| Reproducibility and transparency | 8 |
| Compliance with submission requirements | 9 |
| **Overall** | **about 6.5** |

The target of 9 is not reached, and editing cannot reach it. What holds the score down is evidence, not presentation: there are no independent human labels for the hard Indo-Aryan items, the hard split is defined by a model feature, and the expert check has little power.
