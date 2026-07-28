"""Persistent instances, resonance, boundary objects, and executable concepts."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
from typing import Iterable

from .worlds import Observation, normalized


def _correlation(left: Iterable[float], right: Iterable[float]) -> float:
    xs, ys = tuple(left), tuple(right)
    if len(xs) != len(ys) or not xs:
        return 0.0
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denominator = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return numerator / denominator if denominator else 0.0


def _mae(actual: Iterable[float], predicted: Iterable[float]) -> float:
    pairs = tuple(zip(actual, predicted))
    return sum(abs(a - p) for a, p in pairs) / len(pairs) if pairs else math.inf


@dataclass(frozen=True)
class LocalTrace:
    instance_id: str
    world_id: str
    best_lag: int
    lag_evidence: float
    saturation_rate: float
    oscillation: float
    vocabulary: frozenset[str]


@dataclass
class InterpretiveInstance:
    instance_id: str
    bias: str
    observations: list[Observation] = field(default_factory=list)
    traces: list[LocalTrace] = field(default_factory=list)
    concepts: set[str] = field(default_factory=set)
    history: list[str] = field(default_factory=list)
    status: str = "active"

    def observe(self, observation: Observation) -> LocalTrace:
        inputs, states = normalized(observation)
        correlations = {
            lag: abs(_correlation(inputs[:-lag], states[lag:])) for lag in range(1, 7)
        }
        best_lag = max(correlations, key=correlations.get)
        changes = [states[i] - states[i - 1] for i in range(1, len(states))]
        turns = sum(a * b < 0 for a, b in zip(changes, changes[1:])) / max(1, len(changes) - 1)
        saturation = sum(value >= 0.985 or value <= 0.015 for value in states) / len(states)
        vocabulary = {
            "temporal" if best_lag > 1 else "immediate",
            "boundary" if saturation > 0.05 else "unbounded",
            "rhythm" if turns > 0.12 else "trend",
        }
        trace = LocalTrace(
            self.instance_id,
            observation.world_id,
            best_lag,
            correlations[best_lag] - correlations[1],
            saturation,
            turns,
            frozenset(vocabulary),
        )
        self.observations.append(observation)
        self.traces.append(trace)
        self.history.append(f"observed:{observation.world_id}")
        return trace

    def resonate(self, cue: str) -> dict[str, float]:
        tokens = set(re.findall(r"[a-z]+", cue.lower()))
        anchors = {
            "temporal": {"before", "delay", "later", "memory", "now"},
            "boundary": {"boundary", "limit", "capacity", "edge"},
            "rhythm": {"rhythm", "oscillation", "cycle", "pulse"},
        }
        evidence = set().union(*(trace.vocabulary for trace in self.traces)) if self.traces else set()
        overlaps = sum(bool(tokens & anchors[word]) for word in evidence if word in anchors)
        relevance = overlaps / max(1, len(evidence))
        distinctiveness = 1.0 if self.bias in {"causal", "relational", "temporal"} else 0.7
        tension = max((trace.lag_evidence for trace in self.traces), default=0.0)
        return {
            "relevance": relevance,
            "distinctiveness": distinctiveness,
            "fertility": max(0.0, tension),
            "cost": 1.0,
        }


@dataclass(frozen=True)
class BoundaryObject:
    world_ids: tuple[str, ...]
    aligned_roles: tuple[str, str, str]
    normalized_sequences: tuple[tuple[tuple[float, ...], tuple[float, ...]], ...]
    translation_residue: tuple[str, ...]


@dataclass(frozen=True)
class LaggedCapacityOperator:
    """Executable semantics learned from aligned roles, not surface labels."""

    lag: int
    inertia: float
    response: float
    lower: float = 0.0
    upper: float = 1.0

    def predict(self, observation: Observation) -> tuple[float, ...]:
        inputs, states = normalized(observation)
        predictions = list(states[: self.lag])
        for index in range(self.lag, len(states)):
            value = self.inertia * states[index - 1] + self.response * inputs[index - self.lag]
            predictions.append(min(self.upper, max(self.lower, value)))
        return tuple(predictions)

    def error(self, observation: Observation) -> float:
        _, states = normalized(observation)
        return _mae(states[self.lag :], self.predict(observation)[self.lag :])


def _solve_2x2(a: float, b: float, c: float, d: float, e: float) -> tuple[float, float]:
    determinant = a * c - b * b
    if abs(determinant) < 1e-12:
        return 0.0, 0.0
    return ((d * c - b * e) / determinant, (a * e - b * d) / determinant)


def discover_operator(boundary: BoundaryObject, candidate_lags: range = range(1, 7)) -> LaggedCapacityOperator:
    """Select lag and coefficients by pooled leave-domain-in residual error."""
    best: tuple[float, LaggedCapacityOperator] | None = None
    for lag in candidate_lags:
        x1: list[float] = []
        x2: list[float] = []
        targets: list[float] = []
        for inputs, states in boundary.normalized_sequences:
            for index in range(lag, len(states)):
                x1.append(states[index - 1])
                x2.append(inputs[index - lag])
                targets.append(states[index])
        inertia, response = _solve_2x2(
            sum(v * v for v in x1),
            sum(a * b for a, b in zip(x1, x2)),
            sum(v * v for v in x2),
            sum(a * y for a, y in zip(x1, targets)),
            sum(b * y for b, y in zip(x2, targets)),
        )
        predictions = [min(1.0, max(0.0, inertia * a + response * b)) for a, b in zip(x1, x2)]
        operator = LaggedCapacityOperator(lag, inertia, response)
        score = _mae(targets, predictions) + 0.0001 * lag
        if best is None or score < best[0]:
            best = score, operator
    assert best is not None
    return best[1]


def baseline_error(observation: Observation, lag: int) -> float:
    _, states = normalized(observation)
    return _mae(states[lag:], states[lag - 1 : -1])
