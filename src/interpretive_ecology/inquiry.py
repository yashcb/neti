"""Autopoietic inquiry metabolism, investigations, and sandboxed tool creation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Callable, Iterable, Mapping

from .cognition import CompetingWorldModel


class TensionState(StrEnum):
    ACTIVE = "active"
    TRANSFORMED = "transformed"
    RESOLVED = "resolved"
    SUSPENDED = "suspended"
    STERILE = "sterile"


@dataclass
class DevelopmentalTension:
    tension_id: str
    tension_type: str
    carriers: tuple[str, ...]
    fertility: float
    persistence: int = 0
    state: TensionState = TensionState.ACTIVE
    products: list[str] = field(default_factory=list)

    def metabolize(self, product: str | None, consequence_gain: float) -> None:
        self.persistence += 1
        if product and consequence_gain > 0:
            self.products.append(product)
            self.fertility = min(1.0, self.fertility + consequence_gain)
            self.state = TensionState.TRANSFORMED
        elif self.persistence >= 3 and self.fertility < 0.1:
            self.state = TensionState.STERILE

    def resolve(self) -> None:
        self.state = TensionState.RESOLVED


@dataclass(frozen=True)
class InvestigationAction:
    action_id: str
    observations: dict[str, float]
    cost: float
    reversibility: float


def select_discriminating_action(
    models: Iterable[CompetingWorldModel], actions: Iterable[InvestigationAction]
) -> InvestigationAction:
    """Choose consequences that maximally separate live model predictions per cost."""
    candidates = tuple(actions)
    live = tuple(models)
    if not candidates or len(live) < 2:
        raise ValueError("discrimination requires actions and competing models")

    def score(action: InvestigationAction) -> float:
        predictions = [action.observations.get(model.model_id, 0.0) for model in live]
        center = sum(predictions) / len(predictions)
        separation = sum((value - center) ** 2 for value in predictions) / len(predictions)
        return separation * action.reversibility / max(action.cost, 1e-9)

    return max(candidates, key=score)


@dataclass(frozen=True)
class SandboxedTool:
    tool_id: str
    operation_ids: tuple[str, ...]
    limits: dict[str, float]
    lineage: tuple[str, ...]

    def apply(self, value: float, operations: Mapping[str, Callable[[float], float]]) -> float:
        if not set(self.operation_ids) <= operations.keys():
            raise ValueError("tool references unavailable operations")
        lower, upper = self.limits.get("lower", -1e9), self.limits.get("upper", 1e9)
        result = value
        for operation_id in self.operation_ids:
            result = operations[operation_id](result)
            if not lower <= result <= upper:
                raise ValueError("tool exceeded sandbox limits")
        return result


def create_tool(
    tool_id: str,
    operation_ids: Iterable[str],
    validation_cases: Mapping[float, float],
    operations: Mapping[str, Callable[[float], float]],
    lineage: Iterable[str],
    tolerance: float = 1e-9,
) -> SandboxedTool:
    tool = SandboxedTool(tool_id, tuple(operation_ids), {"lower": -1e6, "upper": 1e6}, tuple(lineage))
    if not validation_cases:
        raise ValueError("a tool requires consequence-grounded validation")
    if any(abs(tool.apply(value, operations) - expected) > tolerance for value, expected in validation_cases.items()):
        raise ValueError("provisional tool failed sandbox validation")
    return tool


@dataclass
class InquiryOrganism:
    inquiry_id: str
    tensions: dict[str, DevelopmentalTension]
    resources: float
    transformations: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    consumed: float = 0.0
    state: str = "active"

    def step(self, cost: float, products: Iterable[str], new_questions: Iterable[str] = ()) -> bool:
        if self.state != "active" or cost < 0 or self.consumed + cost > self.resources:
            self.state = "suspended" if self.state == "active" else self.state
            return False
        products = tuple(products)
        self.consumed += cost
        self.transformations.extend(products)
        self.questions.extend(new_questions)
        if not products and all(tension.state in {TensionState.RESOLVED, TensionState.STERILE} for tension in self.tensions.values()):
            self.state = "completed"
        return True

    @property
    def generative_rate(self) -> float:
        return len(self.transformations) / self.consumed if self.consumed else 0.0

    def should_continue(self, minimum_rate: float = 0.05) -> bool:
        live = any(tension.state in {TensionState.ACTIVE, TensionState.TRANSFORMED} for tension in self.tensions.values())
        affordable = self.consumed < self.resources
        return self.state == "active" and live and affordable and self.generative_rate >= minimum_rate
