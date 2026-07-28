"""Executable structural substrates for developmental interpretation.

The representations are deliberately small enough to inspect, but every object
changes later computation: graph rewrites alter available relations, field
learning alters resonance, model evidence alters prediction choice, and symbols
must be grounded in executable operators before entering an internal language.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import math
from typing import Iterable, Mapping


@dataclass(frozen=True)
class HyperNode:
    node_id: str
    kind: str
    attributes: dict[str, object] = field(default_factory=dict)
    lineage: tuple[str, ...] = ()


@dataclass(frozen=True)
class HyperEdge:
    edge_id: str
    relation: str
    members: tuple[str, ...]
    attributes: dict[str, object] = field(default_factory=dict)
    lineage: tuple[str, ...] = ()


@dataclass
class RelationalHypergraph:
    nodes: dict[str, HyperNode] = field(default_factory=dict)
    edges: dict[str, HyperEdge] = field(default_factory=dict)

    def add_node(self, node: HyperNode) -> None:
        if node.node_id in self.nodes:
            raise ValueError(f"duplicate node: {node.node_id}")
        self.nodes[node.node_id] = node

    def add_edge(self, edge: HyperEdge) -> None:
        if edge.edge_id in self.edges:
            raise ValueError(f"duplicate edge: {edge.edge_id}")
        if len(edge.members) < 2 or not set(edge.members) <= self.nodes.keys():
            raise ValueError("hyperedge requires at least two existing members")
        self.edges[edge.edge_id] = edge

    def neighbors(self, node_id: str, relation: str | None = None) -> frozenset[str]:
        if node_id not in self.nodes:
            raise KeyError(node_id)
        result: set[str] = set()
        for edge in self.edges.values():
            if node_id in edge.members and (relation is None or edge.relation == relation):
                result.update(edge.members)
        result.discard(node_id)
        return frozenset(result)

    def collapse(self, motif_edges: Iterable[str], concept_id: str, handle: str) -> HyperNode:
        """Reify a recurring multi-edge structure without deleting its ancestry."""
        identifiers = tuple(dict.fromkeys(motif_edges))
        if not identifiers or not set(identifiers) <= self.edges.keys():
            raise ValueError("motif must contain existing edges")
        members = tuple(sorted({item for key in identifiers for item in self.edges[key].members}))
        concept = HyperNode(
            concept_id,
            "concept",
            {"handle": handle, "expanded_members": members},
            identifiers,
        )
        self.add_node(concept)
        for index, member in enumerate(members):
            self.add_edge(
                HyperEdge(
                    f"{concept_id}:grounding:{index}",
                    "compresses",
                    (concept_id, member),
                    lineage=identifiers,
                )
            )
        return concept

    def split(self, node_id: str, partitions: Mapping[str, Iterable[str]]) -> tuple[HyperNode, ...]:
        original = self.nodes[node_id]
        result = []
        for child_id, evidence in partitions.items():
            child = HyperNode(
                child_id,
                original.kind,
                {**original.attributes, "split_evidence": tuple(evidence)},
                original.lineage + (node_id,),
            )
            self.add_node(child)
            result.append(child)
        return tuple(result)

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": {key: asdict(value) for key, value in self.nodes.items()},
            "edges": {key: asdict(value) for key, value in self.edges.items()},
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "RelationalHypergraph":
        raw_nodes = data.get("nodes", {})
        raw_edges = data.get("edges", {})
        assert isinstance(raw_nodes, dict) and isinstance(raw_edges, dict)
        graph = cls()
        for raw in raw_nodes.values():
            assert isinstance(raw, dict)
            graph.add_node(HyperNode(**raw))
        for raw in raw_edges.values():
            assert isinstance(raw, dict)
            graph.add_edge(HyperEdge(**raw))
        return graph


@dataclass
class AssociativeField:
    """A learned sparse co-activation field, local to one developmental history."""

    vectors: dict[str, dict[str, float]] = field(default_factory=dict)
    activations: dict[str, int] = field(default_factory=dict)

    def learn(self, active_units: Iterable[str], weight: float = 1.0) -> None:
        units = tuple(dict.fromkeys(active_units))
        for unit in units:
            self.activations[unit] = self.activations.get(unit, 0) + 1
            vector = self.vectors.setdefault(unit, {})
            for peer in units:
                if peer != unit:
                    vector[peer] = vector.get(peer, 0.0) + weight

    def similarity(self, left: str, right: str) -> float:
        a, b = self.vectors.get(left, {}), self.vectors.get(right, {})
        keys = a.keys() | b.keys()
        numerator = sum(a.get(key, 0.0) * b.get(key, 0.0) for key in keys)
        denominator = math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))
        return numerator / denominator if denominator else 0.0

    def perturb(self, cues: Iterable[str], depth: int = 2, decay: float = 0.55) -> dict[str, float]:
        frontier = {cue: 1.0 for cue in cues if cue in self.vectors}
        result = dict(frontier)
        for _ in range(depth):
            following: dict[str, float] = {}
            for unit, activation in frontier.items():
                total = sum(self.vectors[unit].values()) or 1.0
                for peer, weight in self.vectors[unit].items():
                    value = activation * decay * weight / total
                    following[peer] = max(following.get(peer, 0.0), value)
                    result[peer] = max(result.get(peer, 0.0), value)
            frontier = following
        return result


@dataclass
class CompetingWorldModel:
    model_id: str
    assumptions: tuple[str, ...]
    parameters: dict[str, float]
    evidence_for: float = 1.0
    evidence_against: float = 1.0
    revision: int = 0

    @property
    def plausibility(self) -> float:
        return self.evidence_for / (self.evidence_for + self.evidence_against)

    def update(self, error: float, tolerance: float) -> None:
        if error <= tolerance:
            self.evidence_for += max(0.01, tolerance - error)
        else:
            self.evidence_against += error - tolerance

    def revise(self, **parameters: float) -> None:
        self.parameters.update(parameters)
        self.revision += 1


@dataclass(frozen=True)
class GroundedSymbol:
    symbol: str
    operator_id: str
    positive_cases: tuple[str, ...]
    counterexamples: tuple[str, ...]
    predictive_gain: float
    lineage: tuple[str, ...]


@dataclass
class InternalLanguage:
    symbols: dict[str, GroundedSymbol] = field(default_factory=dict)
    compositions: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def propose(self, symbol: GroundedSymbol, minimum_groundings: int = 2) -> bool:
        grounded = len(set(symbol.positive_cases)) >= minimum_groundings
        operational = bool(symbol.operator_id) and symbol.predictive_gain > 0.0
        if grounded and operational:
            self.symbols[symbol.symbol] = symbol
            return True
        return False

    def compose(self, handle: str, symbols: Iterable[str]) -> None:
        parts = tuple(symbols)
        if not parts or not set(parts) <= self.symbols.keys():
            raise ValueError("composition requires grounded symbols")
        self.compositions[handle] = parts


@dataclass(frozen=True)
class Translation:
    source_symbol: str
    target_symbol: str
    shared_cases: tuple[str, ...]
    agreement: float
    residue: tuple[str, ...]


def negotiate_translation(
    source: GroundedSymbol, target: GroundedSymbol, cases: Iterable[str]
) -> Translation:
    shared = tuple(case for case in cases if case in source.positive_cases and case in target.positive_cases)
    universe = set(source.positive_cases) | set(target.positive_cases)
    agreement = len(shared) / len(universe) if universe else 0.0
    residue = tuple(sorted(universe - set(shared)))
    return Translation(source.symbol, target.symbol, shared, agreement, residue)
