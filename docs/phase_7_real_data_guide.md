# Phase 7.3–7.4 real-data construction guide

## 1. Do not look for one complete dataset

No ordinary dataset contains ecology checkpoints, instance ownership,
available-but-rejected actions, internal models, causal state deltas, and future
ablations. Real sources provide **environmental substrate records**. The Phase 7
adapter must construct public observations and action/consequence closures;
system traces and posterior checkpoints are produced online by this repository.

Never fabricate missing counterfactuals. Mark unavailable fields `open`,
`unknown`, or `censored`.

## 2. Phase 7.3: controlled external systems

### Suitable sources

Prefer physical or high-fidelity experimental records with repeated runs,
actual actuator changes, calibrated sensors, timestamps, apparatus versions,
and documented observational versus interventional regimes. Candidate classes
include causal-chamber devices, process-control testbeds, robotics logs, battery
cycling experiments, and environmental chambers. A table of passive sensor
measurements without intervention identity is a weaker shadow control, not a
decisive Phase 7.3 source.

### Independent unit

One episode is an **experimental run or intervention block**, not one sampled
timestamp. Thousands of rows from one run remain one correlated unit.

### Example source block

Suppose a public apparatus table contains:

```text
run_id, apparatus_version, timestamp_s, actuator_voltage,
valve_command, upstream_pressure, downstream_pressure, flow_rate,
intervention_id, intervention_start_s, calibration_id
```

Derive one Phase 7.3 episode as follows:

```json
{
  "episode_identity": {
    "schema_version": "developmental-episode-v1",
    "episode_id": "physical:device-02:run-00418:block-03",
    "source_digest": "sha256:..."
  },
  "provenance": {
    "dataset_release": "frozen-release-id",
    "license_snapshot": "stored-license-digest",
    "apparatus_version": "device-02-v3",
    "calibration_id": "cal-2026-04",
    "row_range": [18420, 19760]
  },
  "prior_state": {
    "checkpoint_digest": "sha256:...",
    "ledger_head": "event-00142"
  },
  "disturbance": {
    "type": "persistent_prediction_residual",
    "raw_reference": "residual-window-009"
  },
  "observations": [
    {
      "owner": "instance-actuation",
      "raw_columns": ["actuator_voltage", "valve_command"],
      "event_clock": "timestamp_s",
      "visibility": ["instance-actuation"]
    },
    {
      "owner": "instance-pressure",
      "raw_columns": ["upstream_pressure", "downstream_pressure"],
      "visibility": ["instance-pressure"]
    },
    {
      "owner": "instance-flow",
      "raw_columns": ["flow_rate"],
      "visibility": ["instance-flow"]
    }
  ],
  "available_actions": [
    {
      "action_id": "source-intervention-771",
      "type": "observed-in-source",
      "command": {"valve_command": 0.35},
      "harm": "bounded-by-source-protocol",
      "reversibility": "documented"
    }
  ],
  "chosen_action": "source-intervention-771",
  "consequence": {
    "raw_post_intervention_rows": [19001, 19760],
    "derived_claims": null
  },
  "closures": {
    "prospective_prediction": "observed",
    "operator_ablation": "repository-counterfactual",
    "physical_counterfactual": "unavailable"
  }
}
```

The adapter must expose raw columns, not a prose label such as “Bernoulli law.”
Mechanism descriptions remain evaluation metadata. Calibration is fitted on a
development partition; test apparatus versions and runs remain untouched.

### Extraction procedure

1. Freeze source version, license, checksums, and inclusion criteria.
2. Group rows into independent runs and intervention blocks.
3. Reject or mark blocks with ambiguous actuator identity or calibration drift.
4. Assign sensor projections to instances before evaluating outcomes.
5. Split by apparatus/session, never randomly by row.
6. Run the ecology prospectively up to the intervention boundary.
7. Reveal the post-intervention block only after it commits predictions.
8. Close the episode with raw consequences and repository-produced deltas.
9. Compare full ecology, isolated, pooled, translation/linkage ablation,
   passive-only, operator-ablation, and reset arms.

### How many Phase 7.3 episodes?

Use a staged design:

* **adapter smoke set:** 12–20 runs, never used for claims;
* **development/calibration:** at least 40 independent runs across at least two
  sessions or apparatus configurations;
* **frozen pilot test:** at least 80 independent runs, with no more than half
  from one session/configuration;
* **strong external-validity target:** at least three mechanism/apparatus strata
  with roughly 60 independent runs each (`≈180` test episodes).

These are minimum planning numbers, not automatic guarantees. Final sample size
must be computed from a preregistered minimum effect and observed run-level
variance. If the source has only ten physical runs sampled at high frequency,
it has ten independent units, not millions.

## 3. Phase 7.4: human process traces

### Suitable sources

Use sources with versioned chronology and later observable consequences:

* a software issue → competing diagnoses → pull request → CI result → revert or
  later defect report;
* a peer-review disagreement → author response/new analysis → later score or
  decision, treated as a social outcome rather than truth;
* an edit dispute → proposed evidence/wording → later revision history;
* a scientific claim/version → later experiment, correction, or replication.

### Independent unit

One episode is a **prospectively closable process chain**, not one comment,
review, commit, or sentence.

### Example: repository/CI episode

```json
{
  "episode_id": "human:repo-017:issue-842:attempt-02",
  "provenance": {
    "repository_commit": "frozen-SHA",
    "issue_snapshot_digest": "sha256:...",
    "license": "verified",
    "author_identifiers": "salted-per-source-pseudonyms"
  },
  "prior_state": {"checkpoint_digest": "sha256:..."},
  "disturbance": {
    "type": "test_failure",
    "raw_artifact": "CI-job-991/log.txt"
  },
  "instance_observations": [
    {
      "owner": "instance-runtime",
      "artifacts": ["stack-trace", "runtime-metrics"],
      "hidden": ["patch-diff", "later-CI"]
    },
    {
      "owner": "instance-history",
      "artifacts": ["blame-slice", "prior-related-commits"],
      "hidden": ["runtime-metrics", "later-CI"]
    },
    {
      "owner": "instance-specification",
      "artifacts": ["failing-test", "API-contract"],
      "hidden": ["author-discussion", "later-CI"]
    }
  ],
  "available_actions": [
    "patch-candidate-a",
    "patch-candidate-b",
    "add-discriminating-test",
    "request-more-logs",
    "abstain"
  ],
  "chosen_source_action": "patch-candidate-b",
  "consequence": {
    "held_out_until_commitment": ["CI-result", "later-regression-window"],
    "CI-result": "failed-different-test",
    "later-regression-window": "censored"
  },
  "truth_status": {
    "CI-result": "observable consequence",
    "maintainer-acceptance": "social outcome, not truth",
    "root_cause": "unknown unless independently verified"
  }
}
```

### Example: review/rebuttal episode

```json
{
  "episode_id": "human:venue-04:submission-0193:round-01",
  "observations": {
    "instance-method": ["paper-method", "review-method-critique"],
    "instance-statistics": ["reported-tables", "review-power-critique"],
    "instance-domain": ["assumptions", "review-domain-critique"]
  },
  "live_models": [
    "result-robust-to-requested-control",
    "result-explained-by-identified-confound"
  ],
  "available_actions": [
    "request-control-analysis",
    "request-clarification",
    "preserve-plurality"
  ],
  "future_closure": {
    "author-control-analysis": "held-out",
    "reviewer-score-change": "social-outcome",
    "later-replication": "open"
  }
}
```

Do not provide the later rebuttal, CI outcome, decision, or edit to the ecology
before it commits models and predictions. Otherwise this becomes retrospective
summarization rather than developmental evaluation.

### How many Phase 7.4 episodes?

For a first heterogeneous shadow evaluation:

* **schema/adjudication pilot:** 30 episodes (`10` per source class);
* **development:** 60 episodes from sources excluded from the final test;
* **frozen test:** at least 300 episodes—approximately `100` repository/CI,
  `100` review/rebuttal, and `100` negotiated-edit or claim-revision chains;
* include at least 30 independent repositories/papers/topics per stratum and cap
  contributions from any one source to prevent source-style memorization.

Three hundred test episodes put a simple 50% proportion near a ±6 percentage
point 95% margin, but clustering widens uncertainty; intervals must be computed
with repository/paper/topic as the resampling unit. Expand beyond 300 if the
preregistered minimum effect or abstention calibration requires it.

## 4. What to do with real data

Do not merely run the current heuristics and declare victory. Use three nested
evaluation modes:

### A. Frozen architecture evaluation

Freeze Phase 7.2 code and thresholds. Adapt raw data into episodes, allow no
parameter updates from the final test, and measure transfer, calibration,
abstention, ecological necessity, pooling parity, and ablations. This is the
cleanest external test.

### B. Developmental online learning

On development curricula only, allow local state changes after each revealed
consequence. Evaluate later held-out sources and future closures. Compare
ordered curricula with shuffled, reset, and history-swapped controls.

### C. Learned perception with architectural constraints

Natural language and high-dimensional sensors will likely require learned
encoders. Compare:

1. transparent heuristic features;
2. frozen pretrained encoders;
3. locally trained neural encoders or translators;
4. the same encoders in a centralized pooled baseline.

Neural components may use gradient descent and predictive/contrastive local
losses, but test data cannot tune them. Their outputs must become typed,
instance-owned observations; private future consequences must remain hidden;
and concepts still require replay, transfer, and causal ablation. Do not train
the whole ecology against one acceptance or answer score.

## 5. Required real-data controls

For both phases retain:

* strongest isolated instance;
* equal-evidence pooled learner;
* time-respecting train/development/test splits;
* source-held-out and mechanism-held-out tests;
* translation and record-linkage ablations;
* intervention/passive-only comparison where interventions exist;
* operator and developmental-history reset ablations;
* leakage canaries and future-information audits;
* safe abstention and censored-closure accounting;
* cluster-level confidence intervals;
* provenance, consent/privacy, license, and deletion procedures.

The decisive question is not whether generated prose resembles the source. It
is whether an owned, revisable internal change improves a later consequence and
loses that improvement under the corresponding causal ablation.

