# Phase 7.0–7.1 implementation and results

## Scope and preregistered interpretation

This implementation evaluates the first two stages of the Phase 7 protocol:

* **7.0:** an immutable developmental-episode kernel with content addressing,
  visibility, private evaluation truth, checkpoint closure, and exact replay;
* **7.1:** a closed-loop synthetic pilot in which separately owned evidence is
  translated, active queries reduce observational ambiguity, and new executable
  Boolean macros are composed from the existing primitive basis.

Passing these stages warrants preparation for Phase 7.2. It does not establish
natural-language learning, real-world causal discovery, autonomous primitive
invention without a supplied basis, or superiority to a centralized learner
with the same total evidence.

## Phase 7.0 — episode kernel

### Implementation

The canonical record separates public developmental data from private generator
truth. It stores the prior and posterior ecology checkpoints and their SHA-256
digests; typed observations with owner, case, role, event time, arrival time,
and visibility; all available actions and the chosen subset; raw consequence;
an evidence-grounded executable delta; ledger heads; and closure state.

Validation rejects checkpoint tampering, duplicate observation identity,
unavailable chosen actions, ownerless observations, unknown evidence, and
private truth keys in the public record. A caller sees only observations whose
visibility tuple admits its identity.

Closing an episode restores the prior checkpoint and installs the accepted
state transition. Each observation first changes its owner's graph/history and emits a
causally linked receipt event; case-aligned translated features then become a
boundary object in the coalition carrier. The kernel installs the accepted
operator, appends a causally linked interpretation event, checkpoints the
posterior, and content-addresses the transition. Replay begins solely from the
recorded prior state and accepted delta and must reproduce the same posterior
digest and ledger head.

Phase 5-style causal-delay and Phase 6-style scoped-revision transitions were
converted to neutral, non-mechanism-named records. Both close and replay.

### Results

All seven kernel predicates pass:

| Predicate | Result |
|---|---:|
| schema and referential integrity | pass |
| deterministic content addressing | pass |
| exact checkpoint/ledger replay | pass |
| private truth absent from public record | pass |
| per-instance visibility enforced | pass |
| owned evidence persists in developmental state | pass |
| Phase 5/6 transition shapes close | pass |

This shows that an episode is now an executable causal state transition rather
than a narrative JSON document.

## Phase 7.1 — closed-loop synthetic curriculum

### Why synthetic data are correct here

Phase 7.1 does **not** require user-curated real data. Its confirmatory questions
require private truth, exact observation masks, active counterfactual queries,
and destructive linkage/operator ablations. A parameterized synthetic world is
the appropriate scientific instrument. Real controlled data enter in Phase
7.3, after this protocol is frozen; human traces enter only as Phase 7.4 shadow
evaluation.

### Mechanisms and representational expansion

The pilot contains three private families: two-input NAND, two-input material
implication, and a three-input multiplexer. Their semantic names and truth
tables are private evaluation data. None is expressible by one Phase 4
`and`/`or`/`xor`/`xnor` operation: the best initial-grammar accuracy is `0.75`.

The learner enumerates the denotations of bounded compositions, collapses
semantically equivalent syntax, and retains the minimum-cost expression for
each behavior. It therefore constructs, rather than receives, macros such as:

* `xnor(and(x0,x1),xor(x0,x0))`;
* `or(x1,xnor(x0,x1))`;
* `xnor(or(x0,xnor(x1,x2)),x1)`.

This is real but bounded representational expansion: new executable functions
are composed from architect-supplied primitives under an architect-supplied
cost ceiling.

### Closed-loop inquiry

Initially one passive case leaves 8, 8, and 128 observationally adequate truth
functions respectively. For every inquiry step, all still-available input
interventions and their model partitions are recorded. The selected action
maximizes the smaller side of the predicted version-space partition. The world
returns separately owned input and consequence observations; case identity is
the boundary object that permits the coalition to reconstruct each experiment.

The two-input families require three active queries and the multiplexer seven.
These exhaustive counts are expected because the version space initially
contains every Boolean denotation: without a stronger prior, an unqueried truth
table cell can always differ. The intervention is epistemically necessary, not
efficient evidence of broad generalization.

### Confirmatory controls and results

| Measurement | Result |
|---|---:|
| mean coalition accuracy | `1.000000` |
| mean equal-evidence pooled accuracy | `1.000000` |
| mean strongest isolated accuracy | `0.666667` |
| ecological necessity gain | `0.333333` |
| mean shuffled-linkage accuracy | `0.416667` |
| mean operator-ablation accuracy | `0.666667` |
| minimum passive version space | `8` |
| new to initial single-operation grammar | yes, all 3 |
| exact episode replay | yes, all 3 |

Every confirmatory predicate passes. The coalition exceeds isolated histories,
and shuffling case linkage removes the gain. Removing the installed operator
returns performance to the strongest no-feature baseline. The equal-evidence
pooled learner exactly matches the ecology, which is the correct result: the
experiment demonstrates the necessity of combining distributed evidence, not
a computational advantage over centralized access to that evidence.

## What succeeded

### Technically

* Developmental episodes have immutable identity, ownership, closure, and exact
  replay.
* Private evaluation truth can be withheld from the public developmental trace.
* Active inquiry transforms a live version space rather than merely appending a
  claim that an experiment happened.
* Coalition evidence has a behavioral advantage over every isolated history.
* Translation, intervention, and executable semantics have causal ablation
  effects.
* The system constructs executable macros outside its initial one-operation
  vocabulary and preserves them through checkpoint/restart.

### Philosophically

The narrow interventionist claim succeeds: internal history, translation, and
operators matter because removing them changes later capability. The ecology
is more than several decorative names around one isolated learner in this
distributed setting.

The stronger claim remains open. A centralized learner with lawful access to
all evidence performs equally well. The representations are finite Boolean
denotations, the primitive basis and search bound are supplied, stable case
identity is available, and only three families were evaluated. This is not yet
open-ended ontology formation, real-world metaphysics, or general intelligence.

### In layman's terms

Several investigators each received pieces of an experiment that were useless
alone. By matching which pieces belonged to the same case and deliberately
asking the missing questions, the group built working rules none of the
individual notebooks supported. Deleting the matching or the working rule made
the advantage disappear. A single analyst given all notebooks could build the
same rule, so we have shown that collaboration over divided evidence works—not
that a society is magically better than complete centralized knowledge.

## Algorithms, neural networks, and learning

Phase 7.0–7.1 is programmatic and symbolic by design. It uses deterministic
serialization, event-sourced state transitions, version-space elimination,
active experiment selection, denotational program synthesis, minimum
description cost, and causal ablations. It uses no neural network, gradient
descent, embedding model, or global differentiable loss.

That is consistent with the architecture, not a rejection of neural learning.
The architecture specifies heterogeneous substrates and consequence criteria,
not one mandatory optimizer. Later associative fields, perceptual encoders, or
language interfaces may use neural networks and local predictive or contrastive
objectives. Their outputs must still enter typed owned state, survive lineage
and replay, and pass intervention tests. A single end-to-end global loss should
not be allowed to erase minority models, translation residue, safety
constraints, or developmental identity.

## Decision

The bounded Phase 7.0 and 7.1 hypotheses pass. Begin designing Phase 7.2, but
retain a no-go on claims of external validity or corpus-scale language learning.
Phase 7.2 should add matched curriculum-order experiments, uncertain linkage,
owner/history swaps, reset controls, and autonomous merge decisions. Phase 7.3
is the first stage requiring a carefully selected controlled real source; Phase
7.4 then adds licensed human process traces as non-ground-truth shadow data.
