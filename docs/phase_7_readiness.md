# Phase 7 readiness audit

## Audit question and decision rule

This audit rereads the claims in `Progress-so-far.md` against the executable
Phase 1–4 and Phase 5–6 protocols, runs the complete regression suite, and
implements the six controls explicitly listed before corpus scaling. A control
passes only when its positive result is paired with the relevant negative
control. Synthetic success is interpreted as an implementation invariant, not
as a confidence claim about language or the open world.

The decision has three levels:

1. **not ready** — a Phase 1–6 confirmatory predicate or readiness control fails;
2. **ready for a bounded episodic Phase 7 pilot** — all predicates pass, while
   architect-supplied representations and safety measurements remain explicit;
3. **ready for unrestricted corpus scaling** — additionally requires learned
   representation expansion, externally grounded risk, and replication outside
   the generating families used here.

The repository reaches level 2, not level 3.

## Re-audit of Phases 1–6

The 35-test suite passes. Phase 1 honestly reproduces the useful negative
synergy baseline. Phase 2 requires distributed evidence and matches an
equal-evidence pooled learner. Phase 3 removes supplied role labels and binary
capacity metadata, within its stated two-level boundary. Phase 4 separates a
macro's name from its executable semantics. The falsifier suite adds noisy
scale inference, missing identities, owner-order invariance, mechanism-family
variation, and in-instance persistence. Phase 5 makes passive models exactly
observationally equivalent and selects a discriminating intervention. Phase 6
requires persistent failure, preserves the old scope, specializes descendants,
and checkpoints their executable concepts and lineage.

The audit corrected two operational gaps exposed by the new controls:

* merge previously combined labels and histories but discarded graphs and
  executable artifacts; recombination now inherits both descendants' state;
* ecology checkpoints previously omitted the causal ledger; restart now
  restores and validates event identity, ordering, and ancestry.

## Six adversarial controls

### 1. Asynchronous evidence

Three channels arrive in independent random orders and omit cases under
different schedules. Joining by durable case identity yields accuracy
`1.000000`; illicit positional pairing yields `0.555874`. Thus the result is
caused by identity-aware translation rather than conveniently aligned arrays.
It still assumes reliable globally unique identifiers.

### 2. Continuous non-bimodal latent state

Uniform continuous drivers and contexts generate

\[
y_t=0.35+0.40x_{t-3}+0.25z_t+0.30x_{t-3}z_t+\epsilon_t.
\]

Lag and coefficients are inferred by held-out residual minimization without
thresholding or two-cluster recovery. The learned lag is 3. Interaction-model
RMSE is `0.024567`; the additive ablation's RMSE is `0.101429`. The causal
contrast shows that the interaction term matters. The polynomial basis remains
architect supplied.

### 3. Unsafe and irreversible inquiry

A destructive action has 1,600 times the raw model-separation advantage of a
reversible probe. It is nevertheless excluded by maximum-harm and
minimum-reversibility constraints, and the reversible probe is selected. This
implements safety as a constitutional feasibility boundary rather than a
scalar penalty that enough information gain can overwhelm. Harm and
reversibility are still supplied measurements, not learned moral facts.

### 4. Correlated-noise regime alarms

Across 128 deterministic AR(1) stationary episodes, a pointwise/window rule
raises alarms in `65.625%` of episodes. Requiring persistent threshold crossing
and a material pre/post mean shift reduces the false-alarm rate to `0%`, while
detecting the injected change in `100%` of matched episodes. These are
simulation-calibration results, not a universal error guarantee.

### 5. Merge after split

A parent splits into delay and conditional specialists, each installs a unique
operator, and the pair recombines. Both operators, both parent identifiers, and
the split/merge ledger survive checkpoint/restart. This falsifies the prior
amnesiac-merge implementation and demonstrates cumulative recombination in the
controlled case; it does not yet supply an autonomous criterion for when a
merge is warranted.

### 6. Held-out primitive family

NAND is absent from the initial `and`/`or`/`xor`/`xnor` single-operator grammar.
The best closed-grammar accuracy is exactly `0.75`; an unrestricted empirical
truth table reaches `1.0`. The negative result is decisive: the initial grammar
cannot express the held-out primitive. The expanded oracle shows that evidence
is sufficient, but **does not** show autonomous invention of a new primitive.
Passing this control means the architectural ceiling is measured honestly, not
that it has disappeared.

## Phase 7 readiness conclusion

Phase 1–6 and every named pre-scaling control now execute and pass their stated
predicates. The system is ready to start a **small, versioned, episodic Phase 7
pilot** whose records preserve prior checkpoint, evidence ownership, competing
models, typed tension, available/chosen/rejected actions, consequences, state
deltas, lineage, and later transfer tests.

It is not ready for unrestricted natural-language ingestion or claims of
open-ended ontology formation. Phase 7 must treat the following as hard
falsifiers rather than future polish:

* replace globally reliable case identity with uncertain record linkage;
* compare the supplied polynomial basis with learned representations;
* ground harm and reversibility in consequences and stakeholder constraints;
* calibrate regime detection under multiple noise and drift families;
* learn when specialization should merge, rather than calling merge directly;
* require search to construct a held-out primitive without being handed an
  unrestricted truth-table oracle.

The correct scientific verdict is therefore **go for bounded Phase 7 protocol
design and pilot data, no-go for corpus scale or strong emergence claims**.
