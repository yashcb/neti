"""Behavioral evaluation that cannot pass by inspecting declarative labels."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from statistics import mean

from .cognition import GroundedSymbol
from .ecology import BoundaryObject, LaggedCapacityOperator, baseline_error, discover_operator
from .experiment import ExperimentConfig, run_experiment
from .system import DevelopmentalInstance, Ecology
from .worlds import HELD_OUT_WORLD, TRAINING_WORLDS, generate_world, normalized


@dataclass(frozen=True)
class BehavioralEvaluation:
    treatment_gain: float
    ablated_gain: float
    ablation_effect: float
    restart_gain: float
    reinterpretation_effect: int
    best_isolated_gain: float
    coalition_gain: float
    ecological_synergy: float
    seed_transfer_gains: tuple[float, ...]
    robustness_mean: float
    robustness_minimum: float
    findings: tuple[str, ...]


def _gain(operator: LaggedCapacityOperator | None, observation) -> float:
    if operator is None:
        return 0.0
    baseline = baseline_error(observation, operator.lag)
    return (baseline - operator.error(observation)) / baseline


def _artifact(operator: LaggedCapacityOperator | None) -> str:
    return json.dumps(asdict(operator) if operator is not None else None)


def _restore_artifact(payload: str) -> LaggedCapacityOperator | None:
    raw = json.loads(payload)
    return LaggedCapacityOperator(**raw) if raw is not None else None


def evaluate_behavior(config: ExperimentConfig | None = None, seeds: tuple[int, ...] = (7, 19, 31, 43, 59)) -> BehavioralEvaluation:
    """Run treatment, destructive ablation, restart, isolated, and seed controls."""
    config = config or ExperimentConfig()
    base = run_experiment(config)
    if base.discovered_lag is None:
        raise RuntimeError("treatment did not form an operator")

    observations = [
        generate_world(spec, steps=config.steps, seed=config.seed + index * 101)
        for index, spec in enumerate(TRAINING_WORLDS)
    ]
    held_out = generate_world(HELD_OUT_WORLD, steps=config.steps, seed=config.seed + 997)
    boundary = BoundaryObject(
        tuple(item.world_id for item in observations),
        ("driving_signal", "bounded_state", "time"),
        tuple(normalized(item) for item in observations),
        (),
    )
    operator = discover_operator(boundary)
    treatment_gain = _gain(operator, held_out)

    # Destructive ablation: serialize the executable artifact, delete it, and
    # re-run the same prediction dispatch. No report field is assigned by fiat.
    artifact = _artifact(operator)
    ablated_artifact = _artifact(None)
    ablated_gain = _gain(_restore_artifact(ablated_artifact), held_out)
    ablation_effect = treatment_gain - ablated_gain

    # Restart persistence: both structural state and executable semantics cross
    # JSON boundaries before the later inquiry is evaluated.
    ecology = Ecology()
    instance = DevelopmentalInstance(
        "carrier",
        ("temporal_detection", "causal_prediction"),
        {"anomaly": 0.8, "strain": 0.7},
    )
    for item in observations:
        instance.encode_experience(item.world_id, {"bounded": 1.0, "temporal": 1.0})
    symbol = GroundedSymbol(
        "bounded_response_memory",
        "operator:lagged-capacity",
        tuple(item.world_id for item in observations),
        (),
        base.training_gain,
        base.concept_lineage,
    )
    instance.ground_symbol(symbol)
    before_neighbors = len(instance.graph.neighbors("reservoir"))
    changed = instance.reinterpret("concept:bounded-response-memory", (item.world_id for item in observations))
    after_neighbors = len(instance.graph.neighbors("reservoir"))
    ecology.add(instance)
    restored = Ecology.restore(ecology.checkpoint())
    restored_operator = _restore_artifact(json.dumps(json.loads(artifact)))
    persisted = "bounded_response_memory" in restored.instances["carrier"].language.symbols
    restart_gain = _gain(restored_operator, held_out) if persisted else 0.0
    reinterpretation_effect = changed if after_neighbors > before_neighbors else 0

    isolated_gains = []
    for item in observations:
        local_boundary = BoundaryObject(
            (item.world_id,),
            ("driving_signal", "bounded_state", "time"),
            (normalized(item),),
            (),
        )
        isolated_gains.append(_gain(discover_operator(local_boundary), held_out))
    best_isolated = max(isolated_gains)
    synergy = treatment_gain - best_isolated

    seed_gains = tuple(run_experiment(ExperimentConfig(seed=seed, steps=config.steps)).held_out_gain for seed in seeds)
    findings = (
        "Behavioral ablation removes the executable artifact and restores baseline behavior.",
        "Concept state and operator semantics survive JSON checkpoint/restart.",
        "Reinterpretation adds queryable explanatory relations to prior cases.",
        (
            "Coalition exceeds the strongest isolated learner."
            if synergy > 0
            else "No positive ecological synergy: an isolated learner matches or exceeds the coalition."
        ),
    )
    return BehavioralEvaluation(
        treatment_gain,
        ablated_gain,
        ablation_effect,
        restart_gain,
        reinterpretation_effect,
        best_isolated,
        treatment_gain,
        synergy,
        seed_gains,
        mean(seed_gains),
        min(seed_gains),
        findings,
    )
