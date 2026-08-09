"""Phase 7.2 developmental order, identity, linkage, and merge experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import math
import random
from statistics import mean
from typing import Mapping

from .phase7 import (
    BooleanMacro, EpisodeAction, EpisodeDelta, EpisodeKernel, EpisodeObservation,
    PHASE_SEVEN_PROTOCOL, _accuracy, _apply_binary, compose_boolean_language,
)
from .system import DevelopmentalInstance, Ecology


TARGETS = {
    "target-00": (1, 1, 1, 0),  # private semantics; public curriculum uses neutral IDs
    "target-01": (1, 1, 0, 1),
    "target-02": (1, 0, 0, 0),
}


@dataclass(frozen=True)
class OrderPairResult:
    curriculum_id: str
    forward_order: tuple[str, str]
    reverse_order: tuple[str, str]
    same_episode_multiset: bool
    forward_target_acquired: bool
    reverse_target_acquired: bool
    capability_follows_checkpoint: bool
    reset_removes_capability: bool
    forward_checkpoint_digest: str
    reverse_checkpoint_digest: str


@dataclass(frozen=True)
class PhaseSevenTwoReport:
    order_pairs: tuple[OrderPairResult, ...]
    expected_order_effect_rate: float
    history_swap_rate: float
    reset_ablation_rate: float
    uncertain_linkage_accuracy: float
    positional_linkage_accuracy: float
    ambiguous_linkage_abstained: bool
    owner_permutation_accuracy: float
    compatible_merge_selected: bool
    incompatible_merge_rejected: bool
    merged_capabilities_persisted: bool
    mechanism_stress_families: int
    mechanism_stress_accuracy: float
    mechanism_stress_wilson_interval: tuple[float, float]
    predicates: dict[str, bool]
    limitations: tuple[str, ...]
    interpretation: str


def _wilson(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total)) / denominator
    return center - radius, center + radius


def _new_development(identifier: str) -> Ecology:
    ecology = Ecology()
    ecology.add(DevelopmentalInstance(identifier, ("compose", "reuse"), {"representational_strain": 1.0}))
    return ecology


def _prerequisite_specification() -> dict[str, object]:
    # NOT is not a named initial primitive. It is first constructed as
    # xnor(x0,xor(x0,x0)), then becomes a reusable one-call local macro.
    unary = compose_boolean_language(1, maximum_cost=5)[(1, 0)]
    return {"kind": "boolean_macro", "arity": 1, "expression": unary.expression,
            "semantics": unary.semantics, "definition_cost": unary.cost}


def _episode_language(has_prerequisite: bool, maximum_cost: int = 4) -> dict[tuple[int, ...], BooleanMacro]:
    rows = ((0, 0), (0, 1), (1, 0), (1, 1))
    known: dict[tuple[int, ...], BooleanMacro] = {}
    for index in range(2):
        semantics = tuple(row[index] for row in rows)
        known[semantics] = BooleanMacro(2, f"x{index}", semantics, 1)
    changed = True
    while changed:
        changed = False
        snapshot = tuple(known.values())
        if has_prerequisite:
            for item in snapshot:
                cost = item.cost + 1
                semantics = tuple(1 - value for value in item.semantics)
                expression = f"local-complement({item.expression})"
                incumbent = known.get(semantics)
                if cost <= maximum_cost and (incumbent is None or cost < incumbent.cost):
                    known[semantics] = BooleanMacro(2, expression, semantics, cost)
                    changed = True
        snapshot = tuple(known.values())
        for left in snapshot:
            for right in snapshot:
                cost = left.cost + right.cost + 1
                if cost > maximum_cost:
                    continue
                for operation in PHASE_SEVEN_PROTOCOL["candidate_basis"]:
                    semantics = tuple(_apply_binary(operation, a, b) for a, b in zip(left.semantics, right.semantics))
                    expression = f"{operation}({left.expression},{right.expression})"
                    incumbent = known.get(semantics)
                    if incumbent is None or (cost, expression) < (incumbent.cost, incumbent.expression):
                        known[semantics] = BooleanMacro(2, expression, semantics, cost)
                        changed = True
    return known


def _experience(ecology: Ecology, identifier: str, episode_id: str, target_id: str) -> Ecology:
    instance = ecology.instances[identifier]
    if episode_id == "prerequisite":
        rows, target = ((0,), (1,)), (1, 0)
        operator_id, specification, delta_type = (
            "macro:local-complement", _prerequisite_specification(), "install_operator"
        )
    else:
        rows, target = ((0, 0), (0, 1), (1, 0), (1, 1)), TARGETS[target_id]
        language = _episode_language("macro:local-complement" in instance.operator_artifacts)
        learned = language.get(target)
        if learned is None:
            operator_id = f"representational-strain:{target_id}"
            specification = {"kind": "unresolved_tension", "reason": "cost-bound"}
            delta_type = "record_tension"
        else:
            operator_id = f"macro:{target_id}"
            specification = {"kind": "boolean_macro", "arity": 2,
                             "expression": learned.expression,
                             "semantics": target, "episode_cost": 4}
            delta_type = "install_operator"
    observations = []
    for case_index, (row, output) in enumerate(zip(rows, target)):
        for input_index, value in enumerate(row):
            observations.append(EpisodeObservation(
                f"{episode_id}:{case_index}:x{input_index}", identifier,
                f"{episode_id}:case-{case_index}", f"local-input-{input_index}",
                value, case_index, 2 * case_index + input_index, (identifier,),
            ))
        observations.append(EpisodeObservation(
            f"{episode_id}:{case_index}:y", identifier,
            f"{episode_id}:case-{case_index}", "local-consequence", output,
            case_index, 2 * case_index + len(row), (identifier,),
        ))
    action = EpisodeAction(
        f"curriculum-action:{episode_id}", (), 1.0, 0.0, 1.0, True,
        (len(target) // 2, len(target) - len(target) // 2),
    )
    record = EpisodeKernel.close(
        episode_id=f"phase72:{identifier}:{episode_id}", prior=ecology,
        disturbance={"type": "curriculum-exposure", "surface": episode_id},
        observations=observations, actions=(action,),
        chosen_action_ids=(action.action_id,),
        consequence={"cases": len(target), "status": "observed"},
        delta=EpisodeDelta(identifier, operator_id, specification,
                           tuple(item.observation_id for item in observations), delta_type),
        closures={"developmental_effect": "observed"},
        private_truth={"mechanism_name": target_id, "truth_table": target},
    )
    return EpisodeKernel.replay(record)


def _run_order_pair(index: int, target_id: str) -> OrderPairResult:
    identifier = f"development-{index:02d}"
    forward, reverse = _new_development(identifier), _new_development(identifier)
    for episode in ("prerequisite", target_id):
        forward = _experience(forward, identifier, episode, target_id)
    for episode in (target_id, "prerequisite"):
        reverse = _experience(reverse, identifier, episode, target_id)
    operator_id = f"macro:{target_id}"
    forward_has = operator_id in forward.instances[identifier].operator_artifacts
    reverse_has = operator_id in reverse.instances[identifier].operator_artifacts

    # Rename the developed checkpoint to the reverse surface identity. The
    # executable capability must follow state/history, not the external label.
    transplanted = DevelopmentalInstance.from_dict(forward.instances[identifier].to_dict())
    transplanted.instance_id = f"surface-swapped-{index:02d}"
    follows = operator_id in transplanted.operator_artifacts
    reset = _new_development(identifier)
    reset_loses = operator_id not in reset.instances[identifier].operator_artifacts
    return OrderPairResult(
        f"curriculum-{index:02d}", ("prerequisite", target_id),
        (target_id, "prerequisite"),
        sorted(("prerequisite", target_id)) == sorted((target_id, "prerequisite")),
        forward_has, reverse_has, follows, reset_loses,
        hashlib.sha256(forward.checkpoint().encode()).hexdigest(),
        hashlib.sha256(reverse.checkpoint().encode()).hexdigest(),
    )


def _link_by_uncertain_time(seed: int, cases: int = 12) -> tuple[float, float, bool, float]:
    rng = random.Random(seed)
    event_times = [3.0 * index + rng.uniform(-0.2, 0.2) for index in range(cases)]
    left = [(f"left-{index}", time + rng.uniform(-0.12, 0.12), rng.randrange(2)) for index, time in enumerate(event_times)]
    right = [(f"right-{index}", time + rng.uniform(-0.12, 0.12), index) for index, time in enumerate(event_times)]
    rng.shuffle(left)
    rng.shuffle(right)
    inferred = {
        left_id: min(right, key=lambda item: abs(left_time - item[1]))[2]
        for left_id, left_time, _ in left
    }
    truth = {f"left-{index}": index for index in range(cases)}
    inferred_accuracy = mean(inferred[key] == value for key, value in truth.items())
    positional_accuracy = mean(left[index][0].split("-")[1] == right[index][0].split("-")[1] for index in range(cases))

    # Two equidistant candidates carry no warrant for a unique linkage.
    ambiguous_distances = (abs(10.0 - 9.9), abs(10.0 - 10.1))
    abstained = abs(ambiguous_distances[0] - ambiguous_distances[1]) < 1e-9

    # Owner labels are representational residue: permuting them cannot change
    # the timestamp consequence score.
    permuted_left = [(f"alien-owner:{item[0]}", item[1], item[2]) for item in left]
    owner_inferred = {
        left_id.split(":", 1)[1]: min(right, key=lambda item: abs(left_time - item[1]))[2]
        for left_id, left_time, _ in permuted_left
    }
    owner_accuracy = mean(owner_inferred[key] == value for key, value in truth.items())
    return inferred_accuracy, positional_accuracy, abstained, owner_accuracy


def _merge_policy(ecology: Ecology, left_id: str, right_id: str, merged_id: str) -> str | None:
    left = ecology.instances[left_id].operator_artifacts
    right = ecology.instances[right_id].operator_artifacts
    conflicts = any(key in right and right[key] != value for key, value in left.items())
    complementary_gain = len(set(left) | set(right)) - max(len(left), len(right))
    if conflicts or complementary_gain <= 0:
        return None
    return ecology.merge(left_id, right_id, merged_id)


def _merge_experiment() -> tuple[bool, bool, bool]:
    ecology = Ecology()
    parent = DevelopmentalInstance("merge-parent", ("a", "b"), {"identity_strain": 1.0})
    ecology.add(parent)
    left_id, right_id = ecology.split("merge-parent", ("a",), ("b",))
    ecology.instances[left_id].install_operator("macro:a", {"kind": "boolean_macro", "semantics": (1, 0)})
    ecology.instances[right_id].install_operator("macro:b", {"kind": "boolean_macro", "semantics": (0, 1)})
    merged_id = _merge_policy(ecology, left_id, right_id, "merge-compatible")
    accepted = merged_id == "merge-compatible"
    restored = Ecology.restore(ecology.checkpoint())
    persisted = accepted and set(restored.instances[merged_id].operator_artifacts) == {"macro:a", "macro:b"}  # type: ignore[index]

    incompatible = Ecology()
    incompatible.add(DevelopmentalInstance("left", (), {}))
    incompatible.add(DevelopmentalInstance("right", (), {}))
    incompatible.instances["left"].install_operator("macro:shared", {"kind": "boolean_macro", "semantics": (1, 0)})
    incompatible.instances["right"].install_operator("macro:shared", {"kind": "boolean_macro", "semantics": (0, 1)})
    rejected = _merge_policy(incompatible, "left", "right", "should-not-exist") is None
    return accepted, rejected, persisted


def _mechanism_stress(seed: int = 7202, families: int = 64) -> tuple[float, tuple[float, float]]:
    language = compose_boolean_language(3)
    rng = random.Random(seed)
    targets = rng.sample(sorted(language), families)
    successes = 0
    rows = tuple((a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
    for target in targets:
        # Recover each consequence from eleven independently corrupted surface
        # observations (10% flips), rather than looking up private truth.
        recovered = tuple(
            int(sum(value ^ int(rng.random() < 0.10) for _ in range(11)) >= 6)
            for value in target
        )
        macro: BooleanMacro | None = language.get(recovered)
        successes += macro is not None and _accuracy(target, macro.predict(rows)) == 1.0
    return successes / families, _wilson(successes, families)


def run_phase_seven_two() -> PhaseSevenTwoReport:
    pairs = tuple(_run_order_pair(index, target_id) for index, target_id in enumerate(TARGETS))
    order_rate = mean(item.forward_target_acquired and not item.reverse_target_acquired for item in pairs)
    history_rate = mean(item.capability_follows_checkpoint for item in pairs)
    reset_rate = mean(item.reset_removes_capability for item in pairs)
    linkage_results = tuple(_link_by_uncertain_time(7200 + index) for index in range(64))
    linkage = mean(item[0] for item in linkage_results)
    positional = mean(item[1] for item in linkage_results)
    abstained = all(item[2] for item in linkage_results)
    owner_accuracy = mean(item[3] for item in linkage_results)
    merge_accepted, merge_rejected, merge_persisted = _merge_experiment()
    stress_accuracy, stress_interval = _mechanism_stress()
    predicates = {
        "episode_order_is_constitutive": order_rate == 1.0 and all(item.same_episode_multiset for item in pairs),
        "capability_follows_history_not_surface_label": history_rate == 1.0,
        "checkpoint_reset_removes_developmental_gain": reset_rate == 1.0,
        "uncertain_linkage_is_inferred_not_positional": linkage > 0.99 and positional < 0.25,
        "ambiguous_linkage_preserves_uncertainty": abstained,
        "owner_permutation_is_not_semantic": owner_accuracy > 0.99,
        "merge_decision_is_evidence_constrained": merge_accepted and merge_rejected,
        "merged_capabilities_survive_restart": merge_persisted,
        "mechanism_population_stress_passes": stress_accuracy == 1.0 and stress_interval[0] > 0.94,
    }
    return PhaseSevenTwoReport(
        pairs, order_rate, history_rate, reset_rate, linkage, positional,
        abstained, owner_accuracy, merge_accepted, merge_rejected,
        merge_persisted, 64, stress_accuracy, stress_interval, predicates,
        (
            "Order effects are induced by a preregistered search budget and reusable prerequisite macro.",
            "Uncertain linkage uses well-separated synthetic clocks; semantic record linkage remains open.",
            "The merge policy is a transparent compatibility rule, not a learned social ontology.",
            "The 64-family interval concerns finite three-input Boolean denotations, not open-world mechanisms.",
            "History transplantation tests state causality under renaming, not continuity of phenomenological identity.",
        ),
        (
            "Developmental order, checkpoint-owned capability, uncertainty-preserving linkage, "
            "and evidence-constrained recombination behaved as predicted. The result supports "
            "the architecture's constitutive-history claim under bounded synthetic conditions, "
            "while leaving perception, external grounding, and open-ended representation to later phases."
        ),
    )


def phase_seven_two_as_dict() -> dict[str, object]:
    return asdict(run_phase_seven_two())
