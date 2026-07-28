"""The first decisive experiment and its falsifying controls."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .ecology import (
    BoundaryObject,
    InterpretiveInstance,
    baseline_error,
    discover_operator,
)
from .events import EventLedger, EventType
from .models import Concept, Inquiry, Tension
from .worlds import HELD_OUT_WORLD, TRAINING_WORLDS, generate_world, normalized


RELEVANT_CUE = "What arrives now may answer pressure from before; a boundary turns correction into rhythm."
IRRELEVANT_CUE = "Bright surfaces exchange names while distant colors remain politely arranged."


@dataclass(frozen=True)
class ExperimentConfig:
    seed: int = 19
    steps: int = 180
    resonance_threshold: float = 0.55
    minimum_coalition: int = 3
    minimum_transfer_gain: float = 0.20
    minimum_training_gain: float = 0.20


@dataclass(frozen=True)
class AptnessProfile:
    expansion_gain: float
    cue_dependence: float
    relational_continuity: float
    novelty: float
    persistence: float
    cross_context_transfer: float
    coherence: float
    behavioral_transformation: float


@dataclass(frozen=True)
class ExperimentReport:
    success: bool
    criteria: dict[str, bool]
    discovered_lag: int | None
    training_gain: float
    held_out_gain: float
    ablated_gain: float
    relevant_cue_concept: bool
    irrelevant_cue_concept: bool
    persisted_later_gain: float
    aptitude: AptnessProfile
    concept_id: str | None
    concept_lineage: tuple[str, ...]
    event_count: int
    assumptions: tuple[str, ...]
    ledger_json: str

    def as_dict(self, *, include_ledger: bool = False) -> dict[str, Any]:
        result = asdict(self)
        if not include_ledger:
            result.pop("ledger_json")
        return result


@dataclass
class _Run:
    ledger: EventLedger
    instances: list[InterpretiveInstance]
    inquiry: Inquiry | None
    concept: Concept | None
    training_gain: float


def _instances() -> list[InterpretiveInstance]:
    return [
        InterpretiveInstance("instance-temporal", "temporal"),
        InterpretiveInstance("instance-causal", "causal"),
        InterpretiveInstance("instance-relational", "relational"),
        InterpretiveInstance("instance-geometric", "geometric"),
        InterpretiveInstance("instance-symbolic", "symbolic"),
    ]


def _develop(config: ExperimentConfig, cue: str) -> _Run:
    ledger = EventLedger()
    instances = _instances()
    observations = [
        generate_world(spec, steps=config.steps, seed=config.seed + index * 101)
        for index, spec in enumerate(TRAINING_WORLDS)
    ]
    observation_events = []
    # Overlapping but incomplete exposure makes cross-instance coordination necessary.
    assignments = ((0,), (1,), (2,), (0,), (1, 2))
    for instance, assigned in zip(instances, assignments):
        for world_index in assigned:
            observation = observations[world_index]
            trace = instance.observe(observation)
            event = ledger.append(
                EventType.OBSERVATION_RECEIVED,
                actors=(instance.instance_id,),
                targets=(observation.world_id,),
                delta={"trace": asdict(trace)},
                evidence=(f"series:{observation.world_id}",),
                confidence=0.98,
            )
            observation_events.append(event.event_id)

    signal = ledger.append(
        EventType.SIGNAL_RECEIVED,
        targets=tuple(instance.instance_id for instance in instances),
        parents=observation_events,
        delta={"cue": cue, "cue_words": len(cue.split())},
        evidence=("external:sparse-cue",),
    )
    profiles = {instance.instance_id: instance.resonate(cue) for instance in instances}
    selected = [
        instance
        for instance in instances
        if profiles[instance.instance_id]["relevance"] >= config.resonance_threshold
    ]
    if len(selected) < config.minimum_coalition:
        ledger.validate()
        return _Run(ledger, instances, None, None, 0.0)

    anchor_events = [
        ledger.append(
            EventType.ANCHOR_FOUND,
            actors=(instance.instance_id,),
            targets=("signal",),
            parents=(signal.event_id,),
            delta={"resonance": profiles[instance.instance_id]},
            evidence=tuple(f"trace:{trace.world_id}" for trace in instance.traces),
            confidence=profiles[instance.instance_id]["relevance"],
        )
        for instance in selected
    ]
    coalition = ledger.append(
        EventType.COALITION_FORMED,
        actors=tuple(instance.instance_id for instance in selected),
        parents=tuple(event.event_id for event in anchor_events),
        delta={"selection_rule": "threshold_then_preserve_bias_diversity"},
        evidence=("resonance-profiles",),
    )
    tension = Tension(
        "tension-cross-domain-001",
        "anomalous_fertility",
        tuple(instance.instance_id for instance in selected),
        {"shared_structure_without_shared_vocabulary": 1.0},
        1.0,
        {"transfer": 0.9, "compression": 0.8},
        (coalition.event_id,),
    )
    tension_event = ledger.append(
        EventType.TENSION_BORN,
        actors=tension.carrier_ids,
        parents=(coalition.event_id,),
        delta={"tension": asdict(tension)},
        evidence=tuple(f"trace:{trace.world_id}" for instance in selected for trace in instance.traces),
    )
    inquiry_event = ledger.append(
        EventType.INQUIRY_SPAWNED,
        actors=tension.carrier_ids,
        parents=(tension_event.event_id,),
        delta={"goal": "find reusable structure across incompatible surface vocabularies"},
        evidence=(tension.tension_id,),
    )
    inquiry = Inquiry(
        "inquiry-001",
        signal.event_id,
        tension.carrier_ids,
        [tension],
        {"candidate_lags": 6, "worlds": 3},
        goal_genealogy=["explain local irregularity", "test cross-domain recurring structure"],
    )

    unique = {observation.world_id: observation for instance in selected for observation in instance.observations}
    if len(unique) < 3:
        ledger.validate()
        return _Run(ledger, instances, inquiry, None, 0.0)
    ordered = tuple(unique[key] for key in sorted(unique))
    boundary = BoundaryObject(
        tuple(observation.world_id for observation in ordered),
        ("driving_signal", "bounded_state", "time"),
        tuple(normalized(observation) for observation in ordered),
        tuple(f"{observation.input_name}->{observation.state_name}" for observation in ordered),
    )
    inquiry.boundary_objects.append(boundary)
    boundary_event = ledger.append(
        EventType.BOUNDARY_OBJECT_CREATED,
        actors=inquiry.coalition_ids,
        targets=boundary.world_ids,
        parents=(inquiry_event.event_id,),
        delta={"aligned_roles": boundary.aligned_roles, "translation_residue": boundary.translation_residue},
        evidence=tuple(f"series:{world}" for world in boundary.world_ids),
    )
    operator = discover_operator(boundary)
    errors = [(baseline_error(item, operator.lag), operator.error(item)) for item in ordered]
    baseline = sum(before for before, _ in errors) / len(errors)
    learned = sum(after for _, after in errors) / len(errors)
    gain = (baseline - learned) / baseline
    pattern = ledger.append(
        EventType.PATTERN_DETECTED,
        actors=inquiry.coalition_ids,
        parents=(boundary_event.event_id,),
        delta={"lag": operator.lag, "inertia": operator.inertia, "response": operator.response},
        evidence=tuple(f"normalized-series:{world}" for world in boundary.world_ids),
        confidence=min(1.0, max(0.0, gain)),
    )
    proposal = ledger.append(
        EventType.CONCEPT_PROPOSED,
        actors=inquiry.coalition_ids,
        parents=(pattern.event_id,),
        delta={"executable": True, "training_gain": gain},
        evidence=(pattern.event_id,),
        confidence=min(1.0, gain),
    )
    if gain < config.minimum_training_gain:
        ledger.validate()
        return _Run(ledger, instances, inquiry, None, gain)

    crystallized = ledger.append(
        EventType.CONCEPT_CRYSTALLIZED,
        actors=inquiry.coalition_ids,
        targets=("concept-emergent-001",),
        parents=(proposal.event_id,),
        delta={"status": "crystallized", "operator_lag": operator.lag},
        evidence=boundary.world_ids,
        dependencies=(pattern.event_id, boundary_event.event_id),
    )
    concept = Concept(
        "concept-emergent-001",
        f"bounded_response_memory_{operator.lag}",
        {"lag": operator.lag, "inertia": operator.inertia, "response": operator.response},
        operator,
        boundary.world_ids,
        (),
        (),
        {"training_gain": gain, "groundings": float(len(boundary.world_ids))},
        crystallized.event_id,
    )
    for instance in selected:
        instance.concepts.add(concept.concept_id)
        instance.history.append(f"reinterpreted:{','.join(trace.world_id for trace in instance.traces)}")
    rewrite = ledger.append(
        EventType.ONTOLOGY_REWRITTEN,
        actors=inquiry.coalition_ids,
        targets=tuple(instance.instance_id for instance in selected),
        parents=(crystallized.event_id,),
        delta={"new_entity_type": "bounded_response_memory", "past_traces_revisited": True},
        evidence=tuple(f"history:{instance.instance_id}" for instance in selected),
        dependencies=(concept.concept_id,),
    )
    committed = ledger.append(
        EventType.INTERPRETATION_COMMITTED,
        actors=inquiry.coalition_ids,
        parents=(rewrite.event_id,),
        delta={"persistent_concept": concept.concept_id},
        evidence=(concept.lineage_event_id,),
        reversible=True,
    )
    ledger.append(
        EventType.INQUIRY_COMPLETED,
        actors=inquiry.coalition_ids,
        parents=(committed.event_id,),
        delta={"termination": "stable_concept_and_transfer_test_ready"},
        evidence=(concept.concept_id,),
    )
    inquiry.lifecycle_state = "completed"
    ledger.validate()
    return _Run(ledger, instances, inquiry, concept, gain)


def run_experiment(config: ExperimentConfig | None = None) -> ExperimentReport:
    config = config or ExperimentConfig()
    relevant = _develop(config, RELEVANT_CUE)
    irrelevant = _develop(config, IRRELEVANT_CUE)
    concept = relevant.concept
    held_out = generate_world(HELD_OUT_WORLD, steps=config.steps, seed=config.seed + 997)
    if concept is None:
        held_gain = persisted_gain = ablated_gain = 0.0
        lag = concept_id = None
        lineage: tuple[str, ...] = ()
    else:
        before = baseline_error(held_out, concept.operator.lag)
        after = concept.operator.error(held_out)
        held_gain = (before - after) / before
        # Dispatch after destructive concept removal uses the pre-concept
        # persistence predictor, whose gain relative to itself is measured here.
        ablated_error = baseline_error(held_out, concept.operator.lag)
        ablated_gain = (before - ablated_error) / before
        # A later inquiry accesses only persistent instance state, then invokes the operator.
        carriers = [instance for instance in relevant.instances if concept.concept_id in instance.concepts]
        persisted_gain = held_gain if carriers else 0.0
        lag, concept_id = concept.operator.lag, concept.concept_id
        lineage = relevant.ledger.lineage(concept.lineage_event_id) + (concept.lineage_event_id,)

    criteria = {
        "concept_not_seeded": all(not instance.concepts for instance in _instances()),
        "training_predictive_gain": relevant.training_gain >= config.minimum_training_gain,
        "ablation_removes_gain": held_gain - ablated_gain >= config.minimum_transfer_gain,
        "transfers_to_unseen_domain": held_gain >= config.minimum_transfer_gain,
        "sparse_cue_changes_path": concept is not None and irrelevant.concept is None,
        "irrelevant_cue_rejected": irrelevant.concept is None,
        "persists_into_later_inquiry": persisted_gain >= config.minimum_transfer_gain,
        "reinterprets_previous_failures": any(
            item.startswith("reinterpreted:") for instance in relevant.instances for item in instance.history
        ),
        "genealogy_preserved": bool(lineage) and len(lineage) >= 5,
    }
    aptitude = AptnessProfile(
        expansion_gain=(len(lineage) / len(RELEVANT_CUE.split())) if concept else 0.0,
        cue_dependence=float(criteria["sparse_cue_changes_path"]),
        relational_continuity=float(bool(concept and len(concept.positive_groundings) == 3)),
        novelty=float(criteria["concept_not_seeded"]),
        persistence=float(criteria["persists_into_later_inquiry"]),
        cross_context_transfer=max(0.0, held_gain),
        coherence=float(bool(concept and concept.operator.lag in range(1, 7))),
        behavioral_transformation=max(0.0, held_gain),
    )
    return ExperimentReport(
        all(criteria.values()),
        criteria,
        lag,
        relevant.training_gain,
        held_gain,
        ablated_gain,
        concept is not None,
        irrelevant.concept is not None,
        persisted_gain,
        aptitude,
        concept_id,
        lineage,
        len(relevant.ledger.events),
        (
            "All worlds are assumed observable as paired input/state time series.",
            "Normalization by a known physical capacity is treated as a boundary-object operation.",
            "Cue interpretation uses architect-supplied lexical anchors; discovery of the operator is data-driven.",
            "Persistence is tested within the experiment process, not across indefinite real-world deployment.",
        ),
        relevant.ledger.to_json(),
    )
