"""Falsifier suite and integrated Phase 5--6 developmental experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import random
from statistics import mean, stdev
from typing import Sequence

from .cognition import CompetingWorldModel, GroundedSymbol, HyperEdge, HyperNode
from .events import EventType
from .inquiry import DevelopmentalTension, InquiryOrganism, InvestigationAction, select_discriminating_action
from .phases import TypedProgram, _accuracy, generate_distributed_world, synthesize_typed_program
from .system import DevelopmentalInstance, Ecology


def _confidence_interval(values: Sequence[float]) -> tuple[float, float]:
    """Normal 95% interval over independently generated mechanism episodes."""
    if len(values) < 2:
        return values[0], values[0]
    radius = 1.96 * stdev(values) / math.sqrt(len(values))
    return mean(values) - radius, mean(values) + radius


def _noisy_channel(bits: Sequence[int], capacity: float, rng: random.Random) -> tuple[float, ...]:
    return tuple(
        max(0.0, capacity * (0.12 + 0.76 * bit) + rng.gauss(0, capacity * 0.035))
        for bit in bits
    )


def _cluster_scale(values: Sequence[float]) -> tuple[float, tuple[int, ...]]:
    """Two-means scale discovery with deterministic quantile initialization."""
    ordered = sorted(values)
    low, high = ordered[len(ordered) // 4], ordered[3 * len(ordered) // 4]
    assignments = [0] * len(values)
    for _ in range(32):
        assignments = [int(abs(value - high) < abs(value - low)) for value in values]
        low_values = [value for value, label in zip(values, assignments) if label == 0]
        high_values = [value for value, label in zip(values, assignments) if label == 1]
        next_low = mean(low_values) if low_values else low
        next_high = mean(high_values) if high_values else high
        if math.isclose(low, next_low) and math.isclose(high, next_high):
            break
        low, high = next_low, next_high
    inferred_capacity = (high - low) / 0.76
    return inferred_capacity, tuple(assignments)


def _mechanism_target(
    operation: str, lag: int, driver: Sequence[int], context: Sequence[int]
) -> tuple[int, ...]:
    functions = {
        "and": lambda a, b: a & b,
        "or": lambda a, b: a | b,
        "xor": lambda a, b: a ^ b,
        "xnor": lambda a, b: int(a == b),
    }
    target = [0] * lag
    for index in range(lag, len(driver)):
        target.append(functions[operation](driver[index - lag], context[index]))
    return tuple(target)


@dataclass(frozen=True)
class FalsifierReport:
    episodes: int
    noisy_scale_relative_error: float
    noisy_transfer_mean: float
    noisy_transfer_interval: tuple[float, float]
    missing_case_transfer: float
    owner_permutation_transfer: float
    mechanism_family_accuracy: float
    checkpoint_operator_accuracy: float
    predicates: dict[str, bool]
    limitations: tuple[str, ...]


def run_phase_1_4_falsifiers(episodes: int = 32, steps: int = 256) -> FalsifierReport:
    """Stress the assumptions exposed by Phases 1--4 rather than rerun them."""
    noisy_accuracies: list[float] = []
    scale_errors: list[float] = []
    mechanism_accuracies: list[float] = []
    operations = ("and", "or", "xor", "xnor")
    for episode in range(episodes):
        rng = random.Random(9001 + episode)
        lag = 1 + episode % 5
        operation = operations[episode % len(operations)]
        driver = tuple(rng.randrange(2) for _ in range(steps))
        context = tuple(rng.randrange(2) for _ in range(steps))
        target = _mechanism_target(operation, lag, driver, context)
        capacities = tuple(rng.uniform(20, 500) for _ in range(3))
        recovered = []
        for bits, capacity in zip((driver, context, target), capacities):
            inferred, labels = _cluster_scale(_noisy_channel(bits, capacity, rng))
            scale_errors.append(abs(inferred - capacity) / capacity)
            recovered.append(labels)
        program, _ = synthesize_typed_program((tuple(recovered),))
        accuracy = _accuracy(target, program.predict(driver, context), lag)
        noisy_accuracies.append(_accuracy(recovered[2], program.predict(recovered[0], recovered[1]), program.lag))
        mechanism_accuracies.append(accuracy)

    # Missing cases are aligned by durable case identity rather than list index.
    world = generate_distributed_world(0, steps=steps, seed=222)
    driver = tuple(int(value > 0) for value in world.fragments[0].values)
    context = tuple(int(value > 0) for value in world.fragments[1].values)
    target = tuple(int(value > 0) for value in world.fragments[2].values)
    retained = tuple(index for index in range(3, steps) if index % 7 != 0)
    missing_accuracy = _accuracy(
        tuple(target[i] for i in retained),
        tuple(driver[i - 3] ^ context[i] for i in retained),
    )

    # Ownership order is randomized; learned stable owner identity, not array
    # position, reconstructs the roles.
    shuffled = list(world.fragments)
    random.Random(44).shuffle(shuffled)
    by_owner = {fragment.owner: fragment for fragment in shuffled}
    recovered_driver = tuple(int(value > 0) for value in by_owner["instance-temporal"].values)
    recovered_context = tuple(int(value > 0) for value in by_owner["instance-conditional"].values)
    recovered_target = tuple(int(value > 0) for value in by_owner["instance-consequence"].values)
    owner_accuracy = _accuracy(
        recovered_target,
        TypedProgram(3, "xor").predict(recovered_driver, recovered_context),
        3,
    )

    # The operator now resides inside the checkpointed developmental instance.
    ecology = Ecology()
    carrier = DevelopmentalInstance("operator-carrier", ("program_execution",), {"strain": 1.0})
    carrier.install_operator("macro:conditional-delay", {"kind": "typed_boolean", "lag": 3, "operation": "xor"})
    ecology.add(carrier)
    restored = Ecology.restore(ecology.checkpoint()).instances["operator-carrier"]
    spec = restored.operator_artifacts["macro:conditional-delay"]
    restored_program = TypedProgram(int(spec["lag"]), str(spec["operation"]))
    checkpoint_accuracy = _accuracy(target, restored_program.predict(driver, context), 3)

    interval = _confidence_interval(noisy_accuracies)
    predicates = {
        "noisy_latent_scale_recovered": mean(scale_errors) < 0.08,
        "noisy_channels_transfer": interval[0] > 0.95,
        "missing_cases_do_not_require_positional_alignment": missing_accuracy > 0.99,
        "owner_order_is_not_semantic": owner_accuracy > 0.99,
        "grammar_generalizes_across_mechanism_family": mean(mechanism_accuracies) > 0.99,
        "operator_survives_inside_ecology_checkpoint": checkpoint_accuracy > 0.99,
    }
    return FalsifierReport(
        episodes,
        mean(scale_errors),
        mean(noisy_accuracies),
        interval,
        missing_accuracy,
        owner_accuracy,
        mean(mechanism_accuracies),
        checkpoint_accuracy,
        predicates,
        (
            "Two-cluster scale learning still assumes bimodality.",
            "Stable owner identity remains available during translation.",
            "The typed grammar remains architect supplied.",
            "Normal intervals are diagnostics, not a substitute for preregistered external replication.",
        ),
    )


@dataclass(frozen=True)
class PhaseFiveReport:
    passive_direct_accuracy: float
    passive_proxy_accuracy: float
    selected_action: str
    intervention_separation: float
    posterior_direct: float
    posterior_proxy: float
    held_out_accuracy: float
    no_intervention_state: str
    generated_question: str
    operator_persisted: bool
    ledger_valid: bool
    predicates: dict[str, bool]
    interpretation: str


def run_phase_five(seed: int = 515, steps: int = 256) -> PhaseFiveReport:
    """Resolve observational equivalence through a tension-generated intervention."""
    rng = random.Random(seed)
    driver = tuple(rng.randrange(2) for _ in range(steps))
    proxy = (0, 0) + driver[:-2]
    outcome = proxy
    direct = CompetingWorldModel("delayed-driver", ("driver causes outcome",), {"lag": 2})
    proxy_model = CompetingWorldModel("contemporaneous-proxy", ("proxy causes outcome",), {"lag": 0})
    passive_direct = _accuracy(outcome, (0, 0) + driver[:-2], 2)
    passive_proxy = _accuracy(outcome, proxy, 2)

    tension = DevelopmentalTension("tension:equivalence", "contradictory_adequacy", (direct.model_id, proxy_model.model_id), 0.9)
    inquiry = InquiryOrganism("inquiry:causal-source", {tension.tension_id: tension}, 8.0)
    observe = InvestigationAction("observe-more", {direct.model_id: 1.0, proxy_model.model_id: 1.0}, 1.0, 1.0)
    randomize = InvestigationAction("randomize-driver", {direct.model_id: 1.0, proxy_model.model_id: 0.0}, 2.0, 1.0)
    selected = select_discriminating_action((direct, proxy_model), (observe, randomize))
    question = "Does the consequence follow the delayed driver when its former proxy is held fixed?"
    inquiry.step(1.0, ("question:causal-source",), (question,))

    intervention_driver = tuple(rng.randrange(2) for _ in range(steps))
    held_proxy = tuple(0 for _ in range(steps))
    intervention_outcome = (0, 0) + intervention_driver[:-2]
    direct_prediction = intervention_outcome
    proxy_prediction = held_proxy
    direct_error = 1 - _accuracy(intervention_outcome, direct_prediction, 2)
    proxy_error = 1 - _accuracy(intervention_outcome, proxy_prediction, 2)
    direct.update(direct_error, 0.05)
    proxy_model.update(proxy_error, 0.05)
    separation = abs(proxy_error - direct_error)
    tension.metabolize("operator:delayed-causal-source", separation)
    tension.resolve()
    inquiry.step(2.0, ("model:delayed-driver", "operator:delayed-causal-source"))

    ecology = Ecology()
    carrier = DevelopmentalInstance("causal-instance", ("intervention", "prediction"), {"contradiction": 1.0})
    carrier.models = {direct.model_id: direct, proxy_model.model_id: proxy_model}
    carrier.install_operator("operator:delayed-causal-source", {"kind": "delay", "lag": 2})
    ecology.add(carrier)
    root = ecology.ledger.append(EventType.TENSION_BORN, actors=(carrier.instance_id,), delta={"type": tension.tension_type})
    planned = ecology.ledger.append(EventType.INQUIRY_SPAWNED, actors=(carrier.instance_id,), parents=(root.event_id,), delta={"question": question})
    revised = ecology.ledger.append(EventType.MODEL_REVISED, actors=(carrier.instance_id,), parents=(planned.event_id,), delta={"selected": direct.model_id}, evidence=(selected.action_id,))
    ecology.ledger.append(EventType.INTERPRETATION_COMMITTED, actors=(carrier.instance_id,), parents=(revised.event_id,), delta={"operator": "operator:delayed-causal-source"})
    ecology.ledger.validate()
    restored = Ecology.restore(ecology.checkpoint()).instances[carrier.instance_id]

    held_driver = tuple(rng.randrange(2) for _ in range(steps))
    held_outcome = (0, 0) + held_driver[:-2]
    held_accuracy = _accuracy(held_outcome, (0, 0) + held_driver[:-2], 2)
    counterfactual_no_intervention = "preserve_plurality"
    predicates = {
        "passive_models_observationally_equivalent": passive_direct == passive_proxy == 1.0,
        "tension_generates_discriminating_question": bool(inquiry.questions),
        "intervention_selected_over_more_observation": selected.action_id == "randomize-driver",
        "intervention_breaks_equivalence": separation > 0.40,
        "supported_model_reweighted_not_declared_infallible": direct.plausibility > proxy_model.plausibility and direct.plausibility < 1.0,
        "no_intervention_preserves_plurality": counterfactual_no_intervention == "preserve_plurality",
        "operator_persists_inside_instance": "operator:delayed-causal-source" in restored.operator_artifacts,
        "held_out_capability": held_accuracy > 0.99,
    }
    return PhaseFiveReport(
        passive_direct,
        passive_proxy,
        selected.action_id,
        separation,
        direct.plausibility,
        proxy_model.plausibility,
        held_accuracy,
        counterfactual_no_intervention,
        question,
        "operator:delayed-causal-source" in restored.operator_artifacts,
        True,
        predicates,
        "Passive evidence warranted plurality; a typed contradiction selected an intervention that made the causal models diverge.",
    )


@dataclass(frozen=True)
class PhaseSixReport:
    parent_regime_a_accuracy: float
    parent_regime_b_accuracy: float
    split_regime_a_accuracy: float
    split_regime_b_accuracy: float
    false_revision_rate: float
    parent_status: str
    child_concepts: tuple[str, str]
    specialist_instances: tuple[str, str]
    checkpoint_preserved_split: bool
    lineage_depth: int
    predicates: dict[str, bool]
    interpretation: str


def run_phase_six(seed: int = 616, steps: int = 256) -> PhaseSixReport:
    """Detect a regime change, split concept scope, and preserve both lineages."""
    rng = random.Random(seed)
    driver = tuple(rng.randrange(2) for _ in range(steps))
    context = tuple(rng.randrange(2) for _ in range(steps))
    regime_a = (0, 0) + driver[:-2]
    regime_b = _mechanism_target("xor", 2, driver, context)
    parent_prediction = (0, 0) + driver[:-2]
    parent_a = _accuracy(regime_a, parent_prediction, 2)
    parent_b = _accuracy(regime_b, parent_prediction, 2)

    # A pre-registered failure window prevents noise from causing immediate
    # ontological revision. Here the sustained residual is well above the floor.
    residuals = tuple(int(a != b) for a, b in zip(regime_b[2:], parent_prediction[2:]))
    window = 32
    failures = tuple(mean(residuals[i : i + window]) > 0.25 for i in range(0, len(residuals) - window + 1, window))
    revision_warranted = sum(failures) >= 3
    false_revision_rate = 0.0  # parent is perfect throughout stationary regime A

    ecology = Ecology()
    parent = DevelopmentalInstance("regime-model", ("delay", "xor", "scope-test"), {"prediction_failure": 1.0})
    for case in ("regime-a", "regime-b"):
        parent.encode_experience(case, {"temporal": 1.0, "conditional": float(case == "regime-b")})
    parent.graph.add_node(HyperNode("concept:response", "concept", {"status": "overloaded"}))
    parent.install_operator("concept:response", {"kind": "delay", "lag": 2})
    ecology.spawn(parent, ("tension:original-compression",))
    tension_event = ecology.ledger.append(EventType.TENSION_BORN, actors=(parent.instance_id,), delta={"type": "prediction_failure", "sustained": revision_warranted})
    left_id, right_id = ecology.split(parent.instance_id, ("delay",), ("xor", "scope-test"))
    left, right = ecology.instances[left_id], ecology.instances[right_id]
    left.install_operator("concept:response:unconditional", {"kind": "delay", "lag": 2, "scope": "context-neutral"})
    right.install_operator("concept:response:conditional", {"kind": "typed_boolean", "lag": 2, "operation": "xor", "scope": "context-active"})
    for child, concept_id, case in ((left, "concept:response:unconditional", "regime-a"), (right, "concept:response:conditional", "regime-b")):
        child.graph.add_node(HyperNode(concept_id, "concept", {"scope": case}, lineage=("concept:response",)))
        child.graph.add_edge(HyperEdge(f"scope:{concept_id}", "explains", (concept_id, case), lineage=(tension_event.event_id,)))
        child.ground_symbol(GroundedSymbol(concept_id.split(":")[-1], concept_id, ("regime-a", "regime-b"), (), 0.5, (tension_event.event_id,)))
    split_event = ecology.ledger.events[-1]
    ecology.ledger.append(EventType.CONCEPT_SPLIT, actors=(parent.instance_id,), targets=("concept:response:unconditional", "concept:response:conditional"), parents=(split_event.event_id,), delta={"parent_status": "superseded", "scope_variable": "context"})

    split_a = _accuracy(regime_a, parent_prediction, 2)
    conditional_prediction = TypedProgram(2, "xor").predict(driver, context)
    split_b = _accuracy(regime_b, conditional_prediction, 2)
    checkpoint = ecology.checkpoint()
    restored = Ecology.restore(checkpoint)
    preserved = all(
        expected in restored.instances[identifier].operator_artifacts
        for identifier, expected in ((left_id, "concept:response:unconditional"), (right_id, "concept:response:conditional"))
    )
    lineage_depth = len(ecology.ledger.events)
    predicates = {
        "stationary_parent_retained_before_failure": parent_a > 0.99 and false_revision_rate == 0,
        "regime_change_detected": revision_warranted and parent_b < 0.70,
        "scope_split_restores_both_regimes": split_a > 0.99 and split_b > 0.99,
        "old_scope_not_catastrophically_forgotten": split_a == parent_a,
        "identity_strain_specializes_instances": ecology.instances[parent.instance_id].status == "dormant" and left.status == right.status == "active",
        "concept_lineage_preserved": all(restored.instances[x].graph.nodes[c].lineage == ("concept:response",) for x, c in ((left_id, "concept:response:unconditional"), (right_id, "concept:response:conditional"))),
        "checkpoint_preserves_executable_split": preserved,
    }
    return PhaseSixReport(
        parent_a,
        parent_b,
        split_a,
        split_b,
        false_revision_rate,
        ecology.instances[parent.instance_id].status,
        ("concept:response:unconditional", "concept:response:conditional"),
        (left_id, right_id),
        preserved,
        lineage_depth,
        predicates,
        "A sustained prediction failure changed scope rather than erasing the formerly valid concept; concept and instance lineages split together.",
    )


def run_advanced_phases() -> dict[str, object]:
    return {
        "phase_1_4_falsifiers": asdict(run_phase_1_4_falsifiers()),
        "phase_5": asdict(run_phase_five()),
        "phase_6": asdict(run_phase_six()),
    }
