"""Append-only event ledger with causal lineage and deterministic replay."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
import json
from typing import Any, Iterable


class EventType(StrEnum):
    SIGNAL_RECEIVED = "SIGNAL_RECEIVED"
    OBSERVATION_RECEIVED = "OBSERVATION_RECEIVED"
    ANCHOR_FOUND = "ANCHOR_FOUND"
    TENSION_BORN = "TENSION_BORN"
    COALITION_FORMED = "COALITION_FORMED"
    INQUIRY_SPAWNED = "INQUIRY_SPAWNED"
    BOUNDARY_OBJECT_CREATED = "BOUNDARY_OBJECT_CREATED"
    PATTERN_DETECTED = "PATTERN_DETECTED"
    CONCEPT_PROPOSED = "CONCEPT_PROPOSED"
    CONCEPT_CRYSTALLIZED = "CONCEPT_CRYSTALLIZED"
    ONTOLOGY_REWRITTEN = "ONTOLOGY_REWRITTEN"
    INTERPRETATION_COMMITTED = "INTERPRETATION_COMMITTED"
    INQUIRY_COMPLETED = "INQUIRY_COMPLETED"
    CONCEPT_ABLATED = "CONCEPT_ABLATED"


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: EventType
    actor_ids: tuple[str, ...]
    target_ids: tuple[str, ...]
    parent_event_ids: tuple[str, ...]
    preconditions: dict[str, Any]
    state_delta: dict[str, Any]
    evidence_refs: tuple[str, ...]
    timestamp: int
    confidence: float
    affected_dependencies: tuple[str, ...] = ()
    reversible: bool = True


@dataclass
class EventLedger:
    """A logical-clock ledger; state is rebuilt solely from recorded deltas."""

    events: list[Event] = field(default_factory=list)

    def append(
        self,
        event_type: EventType,
        *,
        actors: Iterable[str] = (),
        targets: Iterable[str] = (),
        parents: Iterable[str] = (),
        preconditions: dict[str, Any] | None = None,
        delta: dict[str, Any] | None = None,
        evidence: Iterable[str] = (),
        confidence: float = 1.0,
        dependencies: Iterable[str] = (),
        reversible: bool = True,
    ) -> Event:
        parent_ids = tuple(parents)
        known = {event.event_id for event in self.events}
        if any(parent not in known for parent in parent_ids):
            raise ValueError("event has an unknown causal parent")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between zero and one")
        event = Event(
            event_id=f"event-{len(self.events):05d}",
            event_type=event_type,
            actor_ids=tuple(actors),
            target_ids=tuple(targets),
            parent_event_ids=parent_ids,
            preconditions=preconditions or {},
            state_delta=delta or {},
            evidence_refs=tuple(evidence),
            timestamp=len(self.events),
            confidence=confidence,
            affected_dependencies=tuple(dependencies),
            reversible=reversible,
        )
        self.events.append(event)
        return event

    def validate(self) -> None:
        known: set[str] = set()
        for index, event in enumerate(self.events):
            if event.event_id in known or event.timestamp != index:
                raise ValueError("ledger identity or logical-clock invariant violated")
            if not set(event.parent_event_ids) <= known:
                raise ValueError("causal parent must precede its child")
            if not 0.0 <= event.confidence <= 1.0:
                raise ValueError("invalid event confidence")
            known.add(event.event_id)

    def lineage(self, event_id: str) -> tuple[str, ...]:
        by_id = {event.event_id: event for event in self.events}
        if event_id not in by_id:
            raise KeyError(event_id)
        found: set[str] = set()

        def visit(identifier: str) -> None:
            for parent in by_id[identifier].parent_event_ids:
                if parent not in found:
                    found.add(parent)
                    visit(parent)

        visit(event_id)
        return tuple(sorted(found, key=lambda value: by_id[value].timestamp))

    def to_json(self) -> str:
        return json.dumps(
            [asdict(event) for event in self.events],
            indent=2,
            default=lambda value: sorted(value) if isinstance(value, (set, frozenset)) else str(value),
        )
