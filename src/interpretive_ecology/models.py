"""Typed research objects kept independently from orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field

from .ecology import BoundaryObject, LaggedCapacityOperator


@dataclass
class Tension:
    tension_id: str
    tension_type: str
    carrier_ids: tuple[str, ...]
    gap_profile: dict[str, float]
    persistence: float
    expected_fertility: dict[str, float]
    lineage: tuple[str, ...]
    status: str = "active"


@dataclass
class Concept:
    concept_id: str
    handle: str
    structural_signature: dict[str, float | int]
    operator: LaggedCapacityOperator
    positive_groundings: tuple[str, ...]
    counterexamples: tuple[str, ...]
    parent_concepts: tuple[str, ...]
    metrics: dict[str, float]
    lineage_event_id: str
    status: str = "crystallized"


@dataclass
class Inquiry:
    inquiry_id: str
    seed_event_id: str
    coalition_ids: tuple[str, ...]
    tensions: list[Tension]
    resource_budget: dict[str, int]
    boundary_objects: list[BoundaryObject] = field(default_factory=list)
    goal_genealogy: list[str] = field(default_factory=list)
    lifecycle_state: str = "active"
