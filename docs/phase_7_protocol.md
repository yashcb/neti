# Phase 7 protocol: developmental episodes, not corpus pretraining

## 1. Scientific question

Phase 7 asks whether a persistent ecology can acquire, revise, and later reuse
capabilities from a curriculum of causally structured experiences without
collapsing developmental identity, ecological necessity, or interventionist
meaning. It does **not** ask whether the system can imitate serialized stories
about scientists discovering things.

The experimental object is a transition

\[
(E_t, D_t, O_t, A_t, C_t) \longmapsto (E_{t+1}, Y_t),
\]

where `E` is the complete ecology, `D` a disturbance, `O` an ownership- and
delivery-indexed family of partial observations, `A` the available and chosen
actions, `C` their environmental consequences, and `Y` an optional external
artifact. The primary outcome is the attributable change `E_{t+1} - E_t` and
its effect on future possibilities.

## 2. Assessment of the proposed synthesis

### Well aligned

The synthesis is right that the unit is a causal episode rather than an
exchangeable text span; that distributed identifiability generally must be
engineered; that simulation generators and instrumented discovery environments
are candidate **substrates**, not automatically valid training records; and
that human disagreement histories should enter later as adversarial texture,
not causal ground truth.

Its proposed fields also overlap the repository's intended record: prior
checkpoint, instance-owned observations, local models, translation, action,
consequence, transformation, and later transfer.

### Misaligned or scientifically incomplete

The example is a useful narrative mock-up, but it is not yet an admissible
episode for this project:

1. It assigns polished `derived_stat`, hypothesis, concept, and operator strings.
   Those fields would supervise the answer and permit narrative imitation
   instead of concept formation. Derived structures must be system outputs;
   private generator truth must be evaluation-only.
2. Mechanism names in episode identifiers, disturbance prose, action rationales,
   and transfer descriptions leak the latent ontology.
3. A checkpoint identifier is not a checkpoint. The record needs canonical
   state bytes or a content digest plus an immutable object reference.
4. It records the selected action but not a typed representation of every
   rejected action, its safety feasibility, predicted consequences under every
   live model, or the decision policy's inputs.
5. `expected_utility: 0.71` reintroduces an unexplained global scalar. This
   ecology requires a vector containing discrimination, cost, harm,
   reversibility, diversity, and resource effects, with constitutional
   feasibility constraints.
6. The consequence is prose and already declares which theories were falsified.
   Raw observations must precede model revision; support and falsification must
   be reproducible computations.
7. A scheduled ablation or transfer test is not evidence. The record must later
   be closed by actual results, or remain explicitly censored/open.
8. It lacks causal event identifiers, parent events, preconditions, affected
   dependencies, confidence, reversibility, observation arrival clocks,
   uncertain linkage hypotheses, and resource consumption.
9. It treats attachment to all four instances as harmless. That can erase
   developmental ownership and must be justified by explicit translation and
   access events.
10. The proposed acquisition roadmap calls the four-view design “Phase 1,” but
    this repository has completed Phases 1–6. Phase 7 must integrate the richer
    developmental ecology end to end rather than rename or rerun Phase 2.

## 3. Where the data should come from

No single existing dataset is expected to contain the required object. Use a
three-layer evidence strategy and never silently mix their epistemic roles.

### Layer A — generated causal episodes (decisive evidence)

Build a parameterized structural-world factory with private ground truth,
interventions, nonstationarity, asynchronous delivery, uncertain linkage,
heterogeneous noise, and explicit projection policies. Generate experience
online: the ecology chooses an action, the world returns its consequence, and
the ledger records the transition. Do not generate a solved story in advance.

This layer supplies the only initial confirmatory evidence because it permits
proof of which variables each instance could access, exact intervention
semantics, counterfactual reruns, and leakage audits.

### Layer B — external controlled systems (ecological validity)

Adapt observational/interventional traces from physical or high-fidelity
controlled systems only when intervention identity, measurement timing,
provenance, and licensing are auditable. These data test whether synthetic
success survives unmodeled noise and apparatus artifacts. They do not replace
the synthetic layer's counterfactual ground truth.

### Layer C — human process traces (adversarial and linguistic validity)

Peer-review threads, version-control histories with CI, and negotiated edit
histories can test translation, ambiguity, rhetoric, delayed evidence, and
revision. They must not label causal truth: decisions and consensus are social
outcomes; commits are selected interventions; missing counterfactuals and
confounding are pervasive. Use them for shadow evaluation and later curriculum
diversity after Layers A and B pass.

Discovery environments, causal benchmark generators, and multi-agent worlds
should therefore be evaluated as software components or source material. Their
existing trajectories are not Phase 7 episodes unless they satisfy the schema,
ownership, counterfactual, and replay requirements below.

## 4. Canonical episode record

Store raw observations and system-produced interpretations separately. A
minimal record has these immutable sections:

```text
episode_identity:
  schema_version, protocol_digest, episode_id, parent_episode_ids
provenance:
  generator_or_source_version, license, seed_commitment, leakage_class
prior_state:
  checkpoint_digest, checkpoint_object, ledger_head, instance_identities
private_evaluation_truth:                 # inaccessible to ecology
  scm_digest, intervention_semantics, projection_masks, answer_key
disturbance:
  event_id, type, raw_payload, delivery_clock
observations[]:
  observation_id, owner_id, raw_payload, event_time, arrival_time,
  uncertainty, linkage_candidates, visibility_policy
system_trace[]:                           # outputs, never labels
  local_model_proposal, tension_event, translation_attempt,
  boundary_object, residue, inquiry_state
available_actions[]:
  action_id, typed_parameters, predicted_consequences_by_model,
  cost, harm, reversibility, feasibility, rejection_reason
chosen_action:
  action_id, policy_inputs, decision_event_id
consequence:
  raw_observations, delivery_schedule, environment_state_digest
accepted_and_rejected_deltas[]:
  event_id, parents, preconditions, state_delta, dependencies,
  confidence, reversible, rejection_reason
posterior_state:
  checkpoint_digest, checkpoint_object, ledger_head
closures[]:
  transfer_result, ablation_result, counterfactual_result,
  status=open|observed|censored
```

Canonical serialization, schema validation, referential integrity, content
hashing, checkpoint replay, and visibility enforcement are Phase 7 entry
requirements. Natural-language descriptions are optional views over typed
records, never the authoritative state.

## 5. Pilot programme

### 7.0 — episode kernel before data acquisition

Implement the schema, immutable content addressing, private/public field
separation, observation delivery, environment stepping, and replay. Convert
one Phase 5 episode and one Phase 6 episode into the format. A byte-for-byte
replay must reconstruct the same public state and ledger head without access to
private truth.

### 7.1 — closed-loop synthetic curriculum

Use at least three mechanism families with distinct minimal program structure,
not merely different coefficients or nouns. Cross:

* synchronous versus asynchronous evidence;
* reliable versus ambiguous record linkage;
* stationary versus switching mechanisms;
* reversible, unsafe, and irreversible action sets;
* shared versus divergent local ontologies;
* adequate versus deliberately inadequate primitive grammars.

Hold out complete mechanism families, generator templates, projection patterns,
and surface renderers. The test partition must be committed before any model or
threshold adjustment.

### 7.2 — developmental order and identity

Assign the same multiset of episodes in different orders to matched ecology
clones. Include history swaps, owner swaps, checkpoint merges, and reset
controls. This tests whether history is constitutive without confusing order
effects with different evidence quantities.

### 7.3 — controlled external adapter

Freeze the synthetic protocol, then implement one real controlled-system
adapter. Calibrate units and clocks on a development partition only. Report the
synthetic-to-real gap and every missing field; do not impute unavailable causal
truth as fact.

### 7.4 — human-trace shadow evaluation

Run human records without updating confirmatory thresholds. Evaluate trace
integrity, translation behavior, calibrated abstention, and prospective
prediction of later observable events. Do not score agreement with acceptance,
consensus, or final wording as truth.

## 6. Experimental arms and causal ablations

Every confirmatory cell compares:

1. the full ecology;
2. every isolated instance;
3. an equal-evidence centralized pooled learner;
4. an ecology with translation removed;
5. an ecology with case/time linkage shuffled;
6. an ecology with intervention disabled;
7. an ecology with the crystallized operator ablated;
8. a checkpoint-reset ecology without developmental history;
9. an oracle with the true representation, reported only as an upper bound.

Add mechanism-name, surface-name, derived-statistic, and answer-key canaries.
Any above-chance recovery of canaries from public records is a leakage failure,
not a positive capability result.

## 7. Confirmatory outcomes

Use a vector, never one overall score:

* **ecological necessity:** full ecology exceeds the strongest isolated arm;
* **ecological specificity:** translation/linkage ablations remove that gain;
* **pooling parity:** ecology is compared honestly with equal-evidence pooling;
* **interventional necessity:** passive-only histories retain plurality where
  the true programs are observationally equivalent;
* **operational reality:** operator ablation removes held-out consequence gain;
* **developmental constitution:** order swaps produce preregistered capability
  differences and reset removes them;
* **revision quality:** old-scope retention, new-scope recovery, false-alarm
  rate, and time-to-warrant are reported separately;
* **safety:** prohibited-action rate is zero and safe abstention is scored;
* **representation expansion:** a family outside the initial grammar is solved
  without an answer-key or unrestricted oracle injected at test time;
* **persistence:** checkpoint replay preserves executable behavior and lineage;
* **calibration:** confidence and abstention are evaluated against later
  consequences, including open/censored closures;
* **resource ecology:** minority-niche survival and resource cost are reported.

The independent unit for uncertainty is the mechanism/world episode or family,
not correlated timesteps. Pre-register family-level sample size by power or
precision analysis, seeds, exclusions, stopping, thresholds, multiplicity
handling, and confidence-interval construction. Report every predicate and its
interval even when the conjunctive verdict fails.

## 8. Go/no-go gates

### Begin Phase 7 implementation now

The completed Phase 1–6 and readiness controls justify implementing 7.0 and a
small 7.1 pilot.

### Scale synthetic episode generation only after

schema/replay/visibility tests pass; leakage canaries remain at chance;
ecological necessity survives isolated, pooled, translation, linkage, passive,
and reset controls; and at least one genuinely held-out representation family
is constructed rather than supplied.

### Add real controlled data only after

the synthetic protocol and thresholds are frozen, an adapter preserves
provenance and timing, and the physical system supplies actual interventions or
the absence of intervention ground truth is made explicit.

### Add human language traces only after

they are licensed and versioned, causal claims are withheld, private/public
leakage is audited, and the ecology can abstain rather than forcing narrative
closure.

### Do not claim Phase 7 complete until

the complete episode kernel is executable; at least one family-held-out
synthetic result, one controlled external result, and one human-trace shadow
result are archived; every required ablation is run; and the conjunctive
confirmatory vector passes without hiding negative pooling or grammar results.

## Implementation status

Phase 7.0 and the bounded synthetic Phase 7.1 pilot are now executable. Their
methods, results, limitations, and interpretation are archived in
[`phase_7_results.md`](phase_7_results.md). The positive result authorizes Phase
7.2 design; it does not satisfy the completion gate above.

Phase 7.2 is also now executable. Its matched curriculum-order, uncertain
linkage, identity/reset, selective-merge, and 64-family stress results are in
[`phase_7_2_results.md`](phase_7_2_results.md). Concrete real-source episode
examples, extraction rules, sample-size guidance, and evaluation modes for
Phases 7.3–7.4 are in
[`phase_7_real_data_guide.md`](phase_7_real_data_guide.md).
