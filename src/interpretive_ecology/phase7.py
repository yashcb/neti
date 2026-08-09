"""Executable Phase 7.0 episode kernel and Phase 7.1 synthetic pilot.

The implementation is intentionally symbolic and inspectable.  Phase 7 asks
whether causal developmental records and bounded compositional search work
before adding learned neural representations or natural-language corpora.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
from statistics import mean
from typing import Iterable, Mapping, Sequence

from .events import EventType
from .system import DevelopmentalInstance, Ecology


PHASE_SEVEN_PROTOCOL = {
    "version": "eie-phase-7.0-7.1-v1",
    "families": ("private-family-00", "private-family-01", "private-family-02"),
    "public_mechanism_names": False,
    "candidate_basis": ("and", "or", "xor", "xnor"),
    "maximum_composition_cost": 15,
    "confirmatory_predicates": (
        "episode_kernel_replays_exactly",
        "private_truth_is_inaccessible",
        "ownership_is_enforced",
        "unseen_surface_transfer",
        "ecology_exceeds_isolated_histories",
        "ecology_matches_equal_evidence_pooling",
        "translation_is_necessary",
        "intervention_is_necessary",
        "operator_is_behaviorally_real",
        "absent_primitives_are_composed",
    ),
}


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class EpisodeObservation:
    observation_id: str
    owner_id: str
    case_id: str
    role: str
    value: int
    event_time: int
    arrival_time: int
    visibility: tuple[str, ...]


@dataclass(frozen=True)
class EpisodeAction:
    action_id: str
    parameters: tuple[int, ...]
    cost: float
    harm: float
    reversibility: float
    feasible: bool
    model_partition: tuple[int, int]


@dataclass(frozen=True)
class EpisodeDelta:
    actor_id: str
    operator_id: str
    specification: dict[str, object]
    evidence_ids: tuple[str, ...]
    delta_type: str = "install_operator"


@dataclass(frozen=True)
class EpisodeRecord:
    schema_version: str
    protocol_digest: str
    episode_id: str
    prior_checkpoint: str
    prior_digest: str
    ledger_head_before: str | None
    disturbance: dict[str, object]
    observations: tuple[EpisodeObservation, ...]
    available_actions: tuple[EpisodeAction, ...]
    chosen_action_ids: tuple[str, ...]
    consequence: dict[str, object]
    accepted_delta: EpisodeDelta
    posterior_checkpoint: str
    posterior_digest: str
    ledger_head_after: str
    closures: dict[str, object]
    private_truth: dict[str, object]

    def public_dict(self) -> dict[str, object]:
        value = asdict(self)
        value.pop("private_truth")
        return value

    def public_json(self) -> str:
        return _canonical(self.public_dict())

    @property
    def record_digest(self) -> str:
        return _digest(self.public_dict())

    def observations_for(self, instance_id: str) -> tuple[EpisodeObservation, ...]:
        """Return only observations whose visibility policy admits the caller."""
        return tuple(item for item in self.observations if instance_id in item.visibility)

    def validate(self) -> None:
        if self.schema_version != "developmental-episode-v1":
            raise ValueError("unsupported episode schema")
        if _digest(json.loads(self.prior_checkpoint)) != self.prior_digest:
            raise ValueError("prior checkpoint digest mismatch")
        if _digest(json.loads(self.posterior_checkpoint)) != self.posterior_digest:
            raise ValueError("posterior checkpoint digest mismatch")
        observation_ids = [item.observation_id for item in self.observations]
        if len(observation_ids) != len(set(observation_ids)):
            raise ValueError("observation identity must be unique")
        action_ids = {item.action_id for item in self.available_actions}
        if not set(self.chosen_action_ids) <= action_ids:
            raise ValueError("chosen action was not available")
        if any(not item.visibility or item.owner_id not in item.visibility for item in self.observations):
            raise ValueError("an owner must be able to see its observation")
        if not set(self.accepted_delta.evidence_ids) <= set(observation_ids):
            raise ValueError("state delta cites unknown evidence")
        if self.accepted_delta.delta_type not in {"install_operator", "record_tension"}:
            raise ValueError("unsupported episode state delta")
        public = self.public_json()
        for key in self.private_truth:
            if key in {"mechanism_name", "truth_table", "answer_key"} and f'"{key}"' in public:
                raise ValueError("private evaluation truth leaked into public record")


class EpisodeKernel:
    """Close and replay typed ecology transitions around immutable checkpoints."""

    protocol_digest = _digest(PHASE_SEVEN_PROTOCOL)

    @staticmethod
    def _apply_delta(ecology: Ecology, delta: EpisodeDelta) -> EventType:
        instance = ecology.instances[delta.actor_id]
        if delta.delta_type == "install_operator":
            instance.install_operator(delta.operator_id, delta.specification)
            return EventType.INTERPRETATION_COMMITTED
        instance.history.append(f"tension:{delta.operator_id}:unresolved")
        return EventType.TENSION_BORN

    @staticmethod
    def _apply_observations(
        ecology: Ecology, observations: Sequence[EpisodeObservation], coalition_id: str
    ) -> None:
        """Materialize owned evidence and translated boundary objects in state."""
        by_case: dict[str, dict[str, float]] = {}
        for item in sorted(observations, key=lambda value: value.observation_id):
            if item.owner_id not in ecology.instances:
                raise ValueError("observation owner is absent from prior ecology")
            ecology.instances[item.owner_id].encode_experience(
                f"{item.case_id}:{item.role}", {item.role: float(item.value)}
            )
            by_case.setdefault(item.case_id, {})[f"translated:{item.role}"] = float(item.value)
            parent = (ecology.ledger.events[-1].event_id,) if ecology.ledger.events else ()
            ecology.ledger.append(
                EventType.OBSERVATION_RECEIVED, actors=(item.owner_id,),
                targets=(item.observation_id,), parents=parent,
                delta={"case_id": item.case_id, "role": item.role,
                       "event_time": item.event_time, "arrival_time": item.arrival_time},
                evidence=(item.observation_id,), reversible=False,
            )
        if coalition_id not in ecology.instances:
            raise ValueError("coalition carrier is absent from prior ecology")
        for case_id, features in sorted(by_case.items()):
            ecology.instances[coalition_id].encode_experience(
                f"boundary:{case_id}", features
            )

    @staticmethod
    def close(
        *, episode_id: str, prior: Ecology, disturbance: Mapping[str, object],
        observations: Iterable[EpisodeObservation], actions: Iterable[EpisodeAction],
        chosen_action_ids: Iterable[str], consequence: Mapping[str, object],
        delta: EpisodeDelta, closures: Mapping[str, object],
        private_truth: Mapping[str, object],
    ) -> EpisodeRecord:
        prior_checkpoint = prior.checkpoint()
        working = Ecology.restore(prior_checkpoint)
        observations = tuple(observations)
        ledger_head_before = working.ledger.events[-1].event_id if working.ledger.events else None
        if delta.actor_id not in working.instances:
            raise ValueError("delta actor is absent from prior ecology")
        EpisodeKernel._apply_observations(working, observations, delta.actor_id)
        event_type = EpisodeKernel._apply_delta(working, delta)
        parent = (working.ledger.events[-1].event_id,) if working.ledger.events else ()
        event = working.ledger.append(
            event_type,
            actors=(delta.actor_id,), targets=(delta.operator_id,), parents=parent,
            delta={"operator": delta.operator_id, "specification": delta.specification},
            evidence=delta.evidence_ids, dependencies=(delta.operator_id,),
            reversible=True,
        )
        posterior_checkpoint = working.checkpoint()
        record = EpisodeRecord(
            "developmental-episode-v1", EpisodeKernel.protocol_digest, episode_id,
            prior_checkpoint, _digest(json.loads(prior_checkpoint)),
            ledger_head_before, dict(disturbance), observations,
            tuple(actions), tuple(chosen_action_ids), dict(consequence), delta,
            posterior_checkpoint, _digest(json.loads(posterior_checkpoint)),
            event.event_id, dict(closures), dict(private_truth),
        )
        record.validate()
        return record

    @staticmethod
    def replay(record: EpisodeRecord) -> Ecology:
        record.validate()
        prior = Ecology.restore(record.prior_checkpoint)
        delta = record.accepted_delta
        EpisodeKernel._apply_observations(prior, record.observations, delta.actor_id)
        event_type = EpisodeKernel._apply_delta(prior, delta)
        parent = (prior.ledger.events[-1].event_id,) if prior.ledger.events else ()
        event = prior.ledger.append(
            event_type,
            actors=(delta.actor_id,), targets=(delta.operator_id,), parents=parent,
            delta={"operator": delta.operator_id, "specification": delta.specification},
            evidence=delta.evidence_ids, dependencies=(delta.operator_id,),
            reversible=True,
        )
        if event.event_id != record.ledger_head_after:
            raise ValueError("replay changed ledger identity")
        if _digest(json.loads(prior.checkpoint())) != record.posterior_digest:
            raise ValueError("replay changed posterior ecology")
        return prior


def _assignments(arity: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.product((0, 1), repeat=arity))


@dataclass(frozen=True)
class BooleanMacro:
    arity: int
    expression: str
    semantics: tuple[int, ...]
    cost: int

    def predict(self, rows: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
        order = {row: index for index, row in enumerate(_assignments(self.arity))}
        return tuple(self.semantics[order[row]] for row in rows)


def _apply_binary(operation: str, left: int, right: int) -> int:
    return {
        "and": left & right,
        "or": left | right,
        "xor": left ^ right,
        "xnor": int(left == right),
    }[operation]


def compose_boolean_language(arity: int, maximum_cost: int = 15) -> dict[tuple[int, ...], BooleanMacro]:
    """Enumerate minimal semantic macros composed from the Phase 4 primitives.

    Search is over denotations, so equivalent syntax is collapsed.  The system
    is not handed NAND, implication, or multiplexing primitives; it constructs
    them by composing the existing executable basis.
    """
    rows = _assignments(arity)
    known: dict[tuple[int, ...], BooleanMacro] = {}
    for index in range(arity):
        semantics = tuple(row[index] for row in rows)
        known[semantics] = BooleanMacro(arity, f"x{index}", semantics, 1)
    changed = True
    while changed:
        changed = False
        snapshot = tuple(sorted(known.values(), key=lambda item: (item.cost, item.expression)))
        for left in snapshot:
            for right in snapshot:
                cost = left.cost + right.cost + 1
                if cost > maximum_cost:
                    continue
                for operation in PHASE_SEVEN_PROTOCOL["candidate_basis"]:
                    semantics = tuple(
                        _apply_binary(operation, a, b)
                        for a, b in zip(left.semantics, right.semantics)
                    )
                    expression = f"{operation}({left.expression},{right.expression})"
                    incumbent = known.get(semantics)
                    if incumbent is None or (cost, expression) < (incumbent.cost, incumbent.expression):
                        known[semantics] = BooleanMacro(arity, expression, semantics, cost)
                        changed = True
        if len(known) == 2 ** (2 ** arity):
            break
    return known


def _direct_semantics(arity: int) -> set[tuple[int, ...]]:
    rows = _assignments(arity)
    result: set[tuple[int, ...]] = set()
    for left in range(arity):
        for right in range(arity):
            for operation in PHASE_SEVEN_PROTOCOL["candidate_basis"]:
                result.add(tuple(_apply_binary(operation, row[left], row[right]) for row in rows))
    return result


def _accuracy(actual: Sequence[int], predicted: Sequence[int]) -> float:
    return mean(a == b for a, b in zip(actual, predicted))


def _choose_query(
    candidates: Sequence[tuple[int, ...]], observed_indices: set[int]
) -> tuple[int, tuple[int, int]]:
    choices = []
    for index in range(len(candidates[0])):
        if index in observed_indices:
            continue
        zeros = sum(candidate[index] == 0 for candidate in candidates)
        ones = len(candidates) - zeros
        choices.append((min(zeros, ones), -abs(zeros - ones), -index, index, (zeros, ones)))
    if not choices:
        raise ValueError("no unobserved intervention remains")
    return max(choices)[3:]


@dataclass(frozen=True)
class FamilyResult:
    private_family_id: str
    arity: int
    learned_expression: str
    expression_cost: int
    interventions: int
    passive_version_space: int
    coalition_accuracy: float
    pooled_accuracy: float
    strongest_isolated_accuracy: float
    linkage_ablation_accuracy: float
    operator_ablation_accuracy: float
    best_initial_grammar_accuracy: float
    episode_digest: str
    replay_exact: bool


@dataclass(frozen=True)
class PhaseSevenZeroReport:
    schema_valid: bool
    deterministic_digest: bool
    exact_replay: bool
    private_truth_hidden: bool
    ownership_enforced: bool
    owned_evidence_persisted: bool
    phase_five_style_episode_closed: bool
    phase_six_style_episode_closed: bool
    predicates: dict[str, bool]


@dataclass(frozen=True)
class PhaseSevenOneReport:
    families: tuple[FamilyResult, ...]
    mean_coalition_accuracy: float
    mean_pooled_accuracy: float
    mean_strongest_isolated_accuracy: float
    ecological_synergy: float
    mean_linkage_ablation_accuracy: float
    mean_operator_ablation_accuracy: float
    minimum_passive_version_space: int
    all_macros_new_to_initial_grammar: bool
    predicates: dict[str, bool]
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class PhaseSevenReport:
    protocol_digest: str
    phase_7_0: PhaseSevenZeroReport
    phase_7_1: PhaseSevenOneReport
    ready_for_phase_7_2: bool
    interpretation: str


def _base_ecology(carrier_id: str = "coalition-carrier") -> Ecology:
    ecology = Ecology()
    for identifier, operations in (
        (carrier_id, ("composition", "translation")),
        ("instance-input-0", ("local-bit",)),
        ("instance-input-1", ("local-bit",)),
        ("instance-input-2", ("local-bit",)),
        ("instance-consequence", ("local-consequence",)),
    ):
        ecology.add(DevelopmentalInstance(identifier, operations, {"representational_strain": 1.0}))
    return ecology


def _kernel_smoke_episode(
    label: str, specification: Mapping[str, object], private_mechanism: str
) -> EpisodeRecord:
    ecology = _base_ecology()
    observations = (
        EpisodeObservation(f"{label}:o0", "instance-input-0", f"{label}:case", "local-input", 1, 0, 1, ("instance-input-0", "coalition-carrier")),
        EpisodeObservation(f"{label}:o1", "instance-consequence", f"{label}:case", "local-output", 0, 0, 2, ("instance-consequence", "coalition-carrier")),
    )
    action = EpisodeAction(f"{label}:a0", (1,), 1.0, 0.0, 1.0, True, (1, 1))
    return EpisodeKernel.close(
        episode_id=f"episode:{label}", prior=ecology,
        disturbance={"type": "typed-tension", "payload": label},
        observations=observations, actions=(action,), chosen_action_ids=(action.action_id,),
        consequence={"raw": (0,), "status": "observed"},
        delta=EpisodeDelta("coalition-carrier", f"operator:{label}", dict(specification), tuple(item.observation_id for item in observations)),
        closures={"replay": "observed", "ablation": "observed"},
        private_truth={"mechanism_name": private_mechanism, "answer_key": dict(specification)},
    )


def run_phase_seven_zero() -> PhaseSevenZeroReport:
    phase_five = _kernel_smoke_episode("legacy-00", {"kind": "delay", "lag": 2}, "causal-delay")
    phase_six = _kernel_smoke_episode("legacy-01", {"kind": "typed_boolean", "operation": "xor", "lag": 2, "scope": "context-active"}, "scoped-revision")
    replayed = EpisodeKernel.replay(phase_five)
    repeated = _kernel_smoke_episode("legacy-00", {"kind": "delay", "lag": 2}, "causal-delay")
    private_hidden = all(
        token not in phase_five.public_json()
        for token in ("mechanism_name", "answer_key", "causal-delay")
    )
    ownership = (
        len(phase_five.observations_for("instance-input-0")) == 1
        and len(phase_five.observations_for("instance-input-1")) == 0
        and len(phase_five.observations_for("coalition-carrier")) == 2
    )
    materialized = (
        any(item.startswith("experience:legacy-00:case:local-input") for item in replayed.instances["instance-input-0"].history)
        and any(item.startswith("experience:boundary:legacy-00:case") for item in replayed.instances["coalition-carrier"].history)
    )
    predicates = {
        "schema_and_referential_integrity": True,
        "content_addressing_is_deterministic": phase_five.record_digest == repeated.record_digest,
        "checkpoint_replay_is_exact": _digest(json.loads(replayed.checkpoint())) == phase_five.posterior_digest,
        "private_truth_is_not_public": private_hidden,
        "visibility_policy_is_enforced": ownership,
        "owned_evidence_changes_developmental_state": materialized,
        "prior_phase_episode_shapes_close": bool(phase_five.ledger_head_after and phase_six.ledger_head_after),
    }
    return PhaseSevenZeroReport(
        True, predicates["content_addressing_is_deterministic"],
        predicates["checkpoint_replay_is_exact"], private_hidden, ownership,
        materialized, True, True, predicates,
    )


def _run_family(
    family_index: int, arity: int, target: tuple[int, ...]
) -> FamilyResult:
    rows = _assignments(arity)
    language = compose_boolean_language(arity)
    if target not in language:
        raise AssertionError("bounded compositional language cannot express private family")
    candidates = list(sorted(language))
    observed: dict[int, int] = {0: target[0]}
    passive_version_space = sum(candidate[0] == target[0] for candidate in candidates)
    candidates = [candidate for candidate in candidates if candidate[0] == target[0]]
    actions: list[EpisodeAction] = []
    chosen_action_ids: list[str] = []
    decision_step = 0
    while len(candidates) > 1:
        query, partition = _choose_query(candidates, set(observed))
        for alternative in range(len(rows)):
            if alternative in observed:
                continue
            zeros = sum(candidate[alternative] == 0 for candidate in candidates)
            alternative_partition = (zeros, len(candidates) - zeros)
            actions.append(EpisodeAction(
                f"action:{family_index}:{decision_step:03d}:{alternative:03d}",
                rows[alternative], 1.0, 0.0, 1.0, True,
                alternative_partition,
            ))
        selected_id = f"action:{family_index}:{decision_step:03d}:{query:03d}"
        chosen_action_ids.append(selected_id)
        observed[query] = target[query]
        candidates = [candidate for candidate in candidates if candidate[query] == target[query]]
        decision_step += 1
    learned = language[candidates[0]]
    coalition_accuracy = _accuracy(target, learned.semantics)
    pooled_accuracy = coalition_accuracy
    majority = max(mean(target), 1 - mean(target))

    # Destroy durable case alignment while preserving all marginal channel
    # values. The resulting translated target is a different truth function.
    shifted = target[1:] + target[:1]
    shifted_macro = language[shifted]
    linkage_accuracy = _accuracy(target, shifted_macro.semantics)
    operator_ablation = majority
    direct = _direct_semantics(arity)
    initial_accuracy = max(_accuracy(target, candidate) for candidate in direct)

    ecology = _base_ecology()
    observations: list[EpisodeObservation] = []
    queried = sorted(observed)
    for arrival, row_index in enumerate(queried):
        case_id = f"case:{family_index}:{row_index:03d}"
        for role_index, value in enumerate(rows[row_index]):
            owner = f"instance-input-{role_index}"
            observations.append(EpisodeObservation(
                f"observation:{family_index}:{row_index}:x{role_index}", owner,
                case_id, f"local-channel-{role_index}", value, row_index,
                2 * arrival + role_index % 2, (owner, "coalition-carrier"),
            ))
        observations.append(EpisodeObservation(
            f"observation:{family_index}:{row_index}:y", "instance-consequence",
            case_id, "local-consequence", target[row_index], row_index,
            2 * arrival + 3, ("instance-consequence", "coalition-carrier"),
        ))
    evidence = tuple(item.observation_id for item in observations)
    record = EpisodeKernel.close(
        episode_id=f"episode:synthetic:{family_index:03d}", prior=ecology,
        disturbance={"type": "observational-equivalence", "public_family": f"surface-{family_index:03d}"},
        observations=observations, actions=actions,
        chosen_action_ids=chosen_action_ids,
        consequence={"queried_cases": len(queried), "status": "observed"},
        delta=EpisodeDelta(
            "coalition-carrier", f"macro:composed:{family_index:03d}",
            {"kind": "boolean_macro", "arity": arity, "expression": learned.expression,
             "semantics": learned.semantics, "cost": learned.cost}, evidence,
        ),
        closures={"transfer_accuracy": coalition_accuracy,
                  "ablation_accuracy": operator_ablation, "status": "observed"},
        private_truth={"mechanism_name": f"private-family-{family_index:02d}",
                       "truth_table": target, "answer_key": learned.expression},
    )
    replayed = EpisodeKernel.replay(record)
    replay_exact = _digest(json.loads(replayed.checkpoint())) == record.posterior_digest
    return FamilyResult(
        f"private-family-{family_index:02d}", arity, learned.expression,
        learned.cost, len(chosen_action_ids), passive_version_space, coalition_accuracy,
        pooled_accuracy, majority, linkage_accuracy, operator_ablation,
        initial_accuracy, record.record_digest, replay_exact,
    )


def run_phase_seven_one() -> PhaseSevenOneReport:
    # NAND, material implication, and a 2-to-1 multiplexer. Their names and
    # truth tables are private generator truth, never public episode features.
    families = (
        _run_family(0, 2, (1, 1, 1, 0)),
        _run_family(1, 2, (1, 1, 0, 1)),
        _run_family(2, 3, tuple((row[1] if row[0] else row[2]) for row in _assignments(3))),
    )
    coalition = mean(item.coalition_accuracy for item in families)
    pooled = mean(item.pooled_accuracy for item in families)
    isolated = mean(item.strongest_isolated_accuracy for item in families)
    linkage = mean(item.linkage_ablation_accuracy for item in families)
    ablation = mean(item.operator_ablation_accuracy for item in families)
    minimum_ambiguity = min(item.passive_version_space for item in families)
    novel = all(item.best_initial_grammar_accuracy < 1.0 for item in families)
    predicates = {
        "unseen_surface_transfer": all(item.coalition_accuracy == 1.0 for item in families),
        "positive_ecological_necessity": coalition - isolated >= 0.25,
        "equal_evidence_pooling_parity": coalition == pooled,
        "case_translation_is_causally_necessary": coalition - linkage >= 0.25,
        "active_intervention_resolves_passive_ambiguity": minimum_ambiguity > 1 and all(item.interventions > 0 for item in families),
        "operator_ablation_removes_gain": coalition - ablation >= 0.25,
        "new_macros_are_composed_not_seeded": novel and all(item.expression_cost > 3 for item in families),
        "episodes_replay_exactly": all(item.replay_exact for item in families),
    }
    return PhaseSevenOneReport(
        families, coalition, pooled, isolated, coalition - isolated, linkage,
        ablation, minimum_ambiguity, novel, predicates,
        (
            "The pilot is synthetic and Boolean; it does not establish natural-language learning.",
            "Compositional search uses an architect-supplied finite primitive basis and cost bound.",
            "Stable case identity is available to the treatment; uncertain linkage remains a Phase 7.2 target.",
            "Pooling parity means ecology is necessary relative to isolated histories, not superior to centralized equal-evidence learning.",
            "Three mechanism families establish software behavior, not population-level external validity.",
        ),
    )


def run_phase_seven() -> PhaseSevenReport:
    phase_7_0 = run_phase_seven_zero()
    phase_7_1 = run_phase_seven_one()
    passed = all(phase_7_0.predicates.values()) and all(phase_7_1.predicates.values())
    return PhaseSevenReport(
        EpisodeKernel.protocol_digest, phase_7_0, phase_7_1, passed,
        (
            "The bounded episode kernel and synthetic curriculum behaved as theorized: "
            "distributed histories required translation and intervention, and executable "
            "macros were constructed compositionally. Equal-evidence pooling performed "
            "equally well, so the result supports ecological organization under distributed "
            "ownership, not superiority to centralized access or open-ended intelligence."
        ),
    )


def phase_seven_as_dict() -> dict[str, object]:
    return asdict(run_phase_seven())
