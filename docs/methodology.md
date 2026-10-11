# Methodology

_2026-10-10. This is a design, not a validated model. Nothing has been implemented or run._

## 1. Task and notation

- An **item** is a triple (w, e, L): a modern word w in language L ∈ {Hindi, Bengali, Assamese, Odia}, and its attested Old Indo-Aryan etymon e as given by the source.
- **Label:** y ∈ {inh, lrn}. *inh* = tadbhava (inherited through MIA); *lrn* = tatsama (borrowed from Sanskrit after the MIA period).
- **Diagnostic only:** *ardhatatsama* (semi-learned).
- **Cluster:** all items sharing the same etymon e form one cluster c(e). Learned/inherited doublets of one etymon (e.g., a tatsama and a tadbhava descendant of the same Sanskrit word) fall in the same cluster.

**What "missing link" means here.** The intermediate MIA form m is a **latent variable** (category 4, a reconstructed form). Where an attested Pāli or Prakrit form exists (category 2), it is used for training but is never treated as the direct ancestor of a particular modern language. Attested MIA varieties are literary and stand in only as a **proxy** for the unobserved spoken intermediate stage (assumption A5). No output is interpreted as evidence that a variety existed (category 5).

## 2. Competing hypotheses

### Inherited pathway

$$P(w\mid e,\mathrm{inh},L)=\sum_{m}P_{\theta_1}(m\mid e)\;P_{\theta_{2,L}}(w\mid m)$$

- θ₁ (OIA→MIA) is trained on attested (e, m) pairs from training clusters only.
- θ₂,L (MIA→L) is trained on attested (m, w) pairs for inherited words in training clusters. Where m is unattested, it is treated as latent and fitted by EM over the composed model.

### Learned pathway

$$P(w\mid e,\mathrm{lrn},L)=P_{\theta_{3,L}}(w\mid e)$$

- θ₃,L models adaptation of Sanskrit forms into L.
- It is trained on learned-borrowing pairs from training clusters.
- Expected behaviour: near-identity with language-specific nativisation of pronunciation and orthography.

### Posterior and calibration

$$\Lambda=\log P(w\mid e,\mathrm{inh},L)-\log P(w\mid e,\mathrm{lrn},L),\qquad P(\mathrm{inh}\mid w,e,L)=\sigma\!\left(a\,\Lambda+b_L\right)$$

- (a, b_L) is a Platt-style calibration fitted on the development split.
- b_L absorbs the per-language prior log-odds.
- With a = 1 and b_L = log π_L/(1−π_L), this is the exact Bayes posterior. Calibration corrects for model misspecification.

### Why this formulation

- **Dependence is handled.** Correspondences, lexical similarity and "cognate evidence" are all functions of the same string pair. In a likelihood they enter **once**, through the generative model. An additive score Σ wᵢSᵢ over these terms would double-count correlated evidence and needs weights with no training procedure (rejected; §6).
- **Competing explanations are explicit.** The model compares two named histories rather than a related/unrelated label.
- **Outputs are probabilities,** evaluable with proper scoring rules (Brier score, log loss) and calibration.

## 3. Transducer choices

Open decision 5.

| Option | Pros | Cons |
|---|---|---|
| **Weighted finite-state transducers** (stochastic edit transducers, Ristad–Yianilos style, trained by EM) | **Exact** marginalisation over m by composition θ₁∘θ₂. Interpretable correspondences. Data-efficient | Weak context modelling. Needs OpenFst or Pynini (a new dependency) |
| **Neural seq2seq** (LSTM as in Cathcart & Rama 2020, or Cognate Transformer) | Context-sensitive. Strong published results | The sum over m must be approximated (k-best from θ₁: a lower bound). Overconfidence; needs calibration |

**Plan:** implement WFST first, for exactness and interpretability. Add neural transducers as a robustness check. The comparison P vs. B4 is always made **within** a transducer family.

## 4. Separating "intermediate structure" from "extra data"

P uses attested MIA forms, which B4 does not see, so C1 conflates two things:
- (i) modelling the intermediate stage;
- (ii) extra MIA training data.

The ablations separate them:

| System | Intermediate structure | Attested MIA data |
|---|---|---|
| B4 | no (direct OIA→L inherited transducer) | no |
| P-latent | yes (m latent, EM on OIA→L only) | no |
| P | yes | yes |

- P-latent vs. B4 isolates structure.
- P vs. P-latent isolates data.
- C1 (P vs. B4) is the preregistered confirmatory contrast. The decomposition is reported as exploratory.

## 4b. Controls for historical content vs. capacity

The central scientific question is whether the intermediate stage contributes **specific historical evidence** rather than extra parameters, or a convenient way to fit modern spellings.

| Control | Construction | If P ≈ control |
|---|---|---|
| **P-shuffled** (confirmatory C3) | θ₁ trained on (e, m′) pairs where each attested MIA form m′ is permuted to another etymon in the same length band. Same alphabet, data size and architecture | The gain is capacity or flexibility, not history |
| **P-wrong-stage** | The intermediate replaced by forms of another NIA language (e.g., Hindi forms as the "intermediate" for Bengali) | A related string helps, but not specifically MIA history |
| **Capacity-matched B4** | Direct transducer with parameters and states matched to the composed θ₁∘θ₂ | Parameter count explains the gain |
| **P-latent** | m latent, no attested forms | Separates structure from attested-data content |

**Historically constrained pathway.** θ₁ and θ₂ are trained only on items whose inherited route experts marked as regular (protocol §4). Complex-history items never train the pathway. The pathway therefore encodes regular OIA→MIA→NIA correspondences, not arbitrary string-to-string fits.

## 5. Role of LLMs

- **B5 baseline:** the LLM is given (w, e, L) and asked for P(inherited), in zero- and few-shot settings.
- **Proposal ablation:** the LLM proposes candidate MIA forms m, which are added to the k-best list (neural option only; the WFST is exact).
- **The LLM never assigns the label in P.**
- **Contamination probes (RQ3):**
  1. **Recall probe.** Ask for the etymology or stratum of w with no form evidence. Items answered correctly are "recallable".
  2. **Temporal split.** Use Wiktionary entries whose etymology was added after the model's training cutoff. Feasibility depends on revision history (open decision 7).

  All LLM metrics are reported separately on recallable/non-recallable and pre-/post-cutoff items.

## 6. Alternatives considered

| Alternative | Decision | Reason |
|---|---|---|
| Additive evidence score S(h) = Σ wᵢSᵢ − penalties (from the brief) | **Rejected** | Correlated terms double-count; weights unidentified; uncalibrated |
| Discriminative classifier on hand-crafted features | **Kept as baseline B2** | Represents the current approach (Cristea 2021) |
| Full Bayesian phylogenetic model | Rejected for v1 | The question is per-word pathway, not tree topology. Much higher cost |
| Hierarchical model sharing θ across L with language-specific deviations | **Possible extension** | May help low-data Assamese/Odia; adds complexity |
| Evidence graph as the inference engine | Rejected | Adds no inferential power. Kept as an **audit layer** only |
| Embedding similarity as evidence of ancestry | Rejected | Confounds inheritance, contact and training data (Rama 2020; Beinborn & Choenni 2020) |
| LLM as judge of history | Baseline only | LLMs are weak at borrowing and cognate judgements (Sousa Silva & Ahmadi 2026; Liang 2026) and contamination is likely |
| Morphology, chronology, geography features | Deferred | Attestation dates and geography are sparse and uneven at word level. Include only if a source with coverage is verified |

## 7. Uncertainty

Reported separately, never merged into one number:

| Type | Estimate |
|---|---|
| **Aleatoric** | Entropy of the calibrated posterior |
| **Epistemic** | Mutual information across an ensemble of K transducer fits on bootstrap resamples of training clusters |
| **Documentation gap** | Flag whether any attested MIA form exists for e. Report metrics split by this flag |
| **Label uncertainty** | Annotator disagreement on gold items; analyses with and without contested items |

## 8. Assumptions

| # | Assumption | Status | Consequence if wrong |
|---|---|---|---|
| A1 | Stratum labels are categorical | Approximation: strata are graded | Ardhatatsama handled diagnostically; contested items reported |
| A2 | The given etymon is correct | Source-dependent | Gold annotators may flag a wrong etymon; such items are excluded and counted |
| A3 | Inherited change is approximately regular per language | Standard, imperfect (contact, analogy: Cathcart & Rama 2020) | Irregularity is absorbed as transducer noise, which lowers likelihood separation |
| A4 | The learned-adaptation channel is stationary over time | Likely false (older vs. newer tatsamas) | Possible extension: time-varying channel |
| A5 | Attested MIA varieties approximate the intermediate stage | Literary Prakrits are not direct ancestors | Treat m as a proxy; never claim direct ancestry |
| A6 | Wiktionary MIA forms and labels are mostly correct | Unknown | Gold labels for evaluation; silver–gold agreement reported |

## 9. Evidence record (audit layer)

Each prediction stores:
- the item (w, e, L) with source IDs;
- the transcription used;
- the top-k latent m with scores;
- log P under each hypothesis;
- Λ and the calibrated probability;
- the ensemble spread;
- the documentation-gap flag;
- the training-data provenance (which sources and entries trained θ₁, θ₂, θ₃);
- code and model version.

The format will be CLDF-compatible where possible. These records are what an expert or community reviewer would audit.
