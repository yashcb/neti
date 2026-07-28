"""Persistent developmental ecology and executable ecological transitions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import Iterable, Mapping, cast

from .cognition import (
    AssociativeField,
    CompetingWorldModel,
    GroundedSymbol,
    HyperEdge,
    HyperNode,
    InternalLanguage,
    RelationalHypergraph,
)
from .events import EventLedger, EventType


@dataclass
class DevelopmentalInstance:
    instance_id: str
    operations: tuple[str, ...]
    tension_sensitivities: dict[str, float]
    graph: RelationalHypergraph = field(default_factory=RelationalHypergraph)
    associative_field: AssociativeField = field(default_factory=AssociativeField)
    models: dict[str, CompetingWorldModel] = field(default_factory=dict)
    language: InternalLanguage = field(default_factory=InternalLanguage)
    history: list[str] = field(default_factory=list)
    parent_ids: tuple[str, ...] = ()
    viability: dict[str, float] = field(
        default_factory=lambda: {"grounding": 0.0, "revision": 0.0, "uniqueness": 1.0, "cost": 1.0}
    )
    status: str = "active"

    def encode_experience(self, case_id: str, features: Mapping[str, float]) -> None:
        if case_id not in self.graph.nodes:
            self.graph.add_node(HyperNode(case_id, "case", dict(features)))
        feature_nodes = []
        for feature, value in features.items():
            identifier = f"feature:{feature}"
            if identifier not in self.graph.nodes:
                self.graph.add_node(HyperNode(identifier, "feature", {"name": feature}))
            feature_nodes.append(identifier)
            edge_id = f"experience:{case_id}:{feature}"
            if edge_id not in self.graph.edges:
                self.graph.add_edge(
                    HyperEdge(edge_id, "exhibits", (case_id, identifier), {"strength": value})
                )
        self.associative_field.learn((case_id, *feature_nodes))
        self.history.append(f"experience:{case_id}")

    def ground_symbol(self, symbol: GroundedSymbol) -> bool:
        accepted = self.language.propose(symbol)
        if accepted:
            self.history.append(f"symbol:{symbol.symbol}")
            self.viability["grounding"] += symbol.predictive_gain
        return accepted

    def reinterpret(self, concept_id: str, cases: Iterable[str]) -> int:
        """Create real graph relations that change future neighbor queries."""
        changed = 0
        if concept_id not in self.graph.nodes:
            self.graph.add_node(HyperNode(concept_id, "concept"))
        for case in cases:
            if case not in self.graph.nodes:
                continue
            edge_id = f"reinterpretation:{concept_id}:{case}"
            if edge_id not in self.graph.edges:
                self.graph.add_edge(HyperEdge(edge_id, "explains", (concept_id, case)))
                changed += 1
        self.history.append(f"reinterpretation:{concept_id}:{changed}")
        return changed

    def concept_changes_retrieval(self, concept_id: str) -> bool:
        return concept_id in self.graph.nodes and bool(self.graph.neighbors(concept_id, "explains"))

    def to_dict(self) -> dict[str, object]:
        return {
            "instance_id": self.instance_id,
            "operations": self.operations,
            "tension_sensitivities": self.tension_sensitivities,
            "graph": self.graph.to_dict(),
            "associative_field": asdict(self.associative_field),
            "models": {key: asdict(value) for key, value in self.models.items()},
            "language": asdict(self.language),
            "history": self.history,
            "parent_ids": self.parent_ids,
            "viability": self.viability,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, object]) -> "DevelopmentalInstance":
        models_raw = raw.get("models", {})
        language_raw = raw.get("language", {})
        field_raw = raw.get("associative_field", {})
        assert isinstance(models_raw, dict) and isinstance(language_raw, dict) and isinstance(field_raw, dict)
        operations = cast(Iterable[str], raw["operations"])
        sensitivities = cast(Mapping[str, float], raw["tension_sensitivities"])
        graph_raw = cast(Mapping[str, object], raw["graph"])
        history = cast(Iterable[str], raw.get("history", []))
        parent_ids = cast(Iterable[str], raw.get("parent_ids", ()))
        viability = cast(Mapping[str, float], raw.get("viability", {}))
        symbols = {
            key: GroundedSymbol(**value) for key, value in language_raw.get("symbols", {}).items()
        }
        return cls(
            instance_id=str(raw["instance_id"]),
            operations=tuple(operations),
            tension_sensitivities=dict(sensitivities),
            graph=RelationalHypergraph.from_dict(graph_raw),
            associative_field=AssociativeField(
                vectors={key: dict(value) for key, value in field_raw.get("vectors", {}).items()},
                activations=dict(field_raw.get("activations", {})),
            ),
            models={key: CompetingWorldModel(**value) for key, value in models_raw.items()},
            language=InternalLanguage(symbols, dict(language_raw.get("compositions", {}))),
            history=list(history),
            parent_ids=tuple(parent_ids),
            viability=dict(viability),
            status=str(raw.get("status", "active")),
        )


@dataclass
class Ecology:
    instances: dict[str, DevelopmentalInstance] = field(default_factory=dict)
    ledger: EventLedger = field(default_factory=EventLedger)
    archive: dict[str, dict[str, object]] = field(default_factory=dict)
    resource_pool: float = 100.0

    def add(self, instance: DevelopmentalInstance) -> None:
        if instance.instance_id in self.instances:
            raise ValueError("instance already exists")
        self.instances[instance.instance_id] = instance

    def allocate(self, requested: Mapping[str, float]) -> dict[str, float]:
        """Quality-diversity allocation protects unique niches before utility."""
        active = {key: self.instances[key] for key in requested if self.instances[key].status == "active"}
        if not active:
            return {}
        floor = min(self.resource_pool * 0.05, self.resource_pool / len(active))
        allocation = {key: min(requested[key], floor) for key in active}
        remaining = self.resource_pool - sum(allocation.values())
        scores = {
            key: max(0.01, item.viability.get("uniqueness", 0.0))
            * (1.0 + item.viability.get("grounding", 0.0) + item.viability.get("revision", 0.0))
            / max(0.01, item.viability.get("cost", 1.0))
            for key, item in active.items()
        }
        while remaining > 1e-9:
            eligible = [key for key in active if allocation[key] + 1e-9 < requested[key]]
            if not eligible:
                break
            total = sum(scores[key] for key in eligible)
            spent = 0.0
            for key in eligible:
                addition = min(requested[key] - allocation[key], remaining * scores[key] / total)
                allocation[key] += addition
                spent += addition
            remaining -= spent
            if spent <= 1e-12:
                break
        return allocation

    def spawn(self, child: DevelopmentalInstance, tension_ids: Iterable[str]) -> None:
        self.add(child)
        self.ledger.append(
            EventType.INSTANCE_SPAWNED,
            actors=child.parent_ids,
            targets=(child.instance_id,),
            delta={"operations": child.operations, "status": "active"},
            evidence=tuple(tension_ids),
        )

    def split(self, instance_id: str, left_ops: Iterable[str], right_ops: Iterable[str]) -> tuple[str, str]:
        parent = self.instances[instance_id]
        left_id, right_id = f"{instance_id}:a", f"{instance_id}:b"
        left = DevelopmentalInstance(left_id, tuple(left_ops), dict(parent.tension_sensitivities), parent_ids=(instance_id,))
        right = DevelopmentalInstance(right_id, tuple(right_ops), dict(parent.tension_sensitivities), parent_ids=(instance_id,))
        for child in (left, right):
            child.history = list(parent.history)
            child.viability = dict(parent.viability)
            self.add(child)
        parent.status = "dormant"
        self.ledger.append(
            EventType.INSTANCE_SPLIT,
            actors=(instance_id,),
            targets=(left_id, right_id),
            delta={"parent_status": "dormant"},
            evidence=("persistent_operation_incompatibility",),
        )
        return left_id, right_id

    def merge(self, left_id: str, right_id: str, merged_id: str) -> str:
        left, right = self.instances[left_id], self.instances[right_id]
        merged = DevelopmentalInstance(
            merged_id,
            tuple(dict.fromkeys(left.operations + right.operations)),
            {key: max(left.tension_sensitivities.get(key, 0), right.tension_sensitivities.get(key, 0)) for key in left.tension_sensitivities.keys() | right.tension_sensitivities.keys()},
            parent_ids=(left_id, right_id),
        )
        merged.history = list(dict.fromkeys(left.history + right.history))
        self.add(merged)
        left.status = right.status = "dormant"
        self.ledger.append(
            EventType.INSTANCES_MERGED,
            actors=(left_id, right_id),
            targets=(merged_id,),
            delta={"source_status": "dormant", "merged_operations": merged.operations},
            evidence=("low_translation_loss", "positive_synergy"),
        )
        return merged_id

    def make_dormant(self, instance_id: str) -> None:
        self.instances[instance_id].status = "dormant"
        self.ledger.append(
            EventType.INSTANCE_DORMANT,
            actors=(instance_id,),
            targets=(instance_id,),
            delta={"status": "dormant"},
            evidence=("low_activity_high_uniqueness",),
        )

    def decay(self, instance_id: str) -> None:
        instance = self.instances.pop(instance_id)
        instance.status = "decayed"
        self.archive[instance_id] = instance.to_dict()
        self.ledger.append(
            EventType.INSTANCE_DECAYED,
            actors=(instance_id,),
            targets=(instance_id,),
            delta={"status": "decayed", "recoverable": True},
            evidence=("redundant_high_cost_low_revision",),
        )

    def revive(self, instance_id: str) -> DevelopmentalInstance:
        instance = DevelopmentalInstance.from_dict(self.archive[instance_id])
        instance.status = "dormant"
        self.instances[instance_id] = instance
        return instance

    def checkpoint(self) -> str:
        payload = {
            "instances": {key: value.to_dict() for key, value in self.instances.items()},
            "archive": self.archive,
            "resource_pool": self.resource_pool,
        }
        return json.dumps(payload, sort_keys=True)

    @classmethod
    def restore(cls, checkpoint: str) -> "Ecology":
        raw = json.loads(checkpoint)
        return cls(
            instances={key: DevelopmentalInstance.from_dict(value) for key, value in raw["instances"].items()},
            archive=raw["archive"],
            resource_pool=raw["resource_pool"],
        )
