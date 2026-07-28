import unittest

from interpretive_ecology.cognition import (
    AssociativeField,
    CompetingWorldModel,
    GroundedSymbol,
    HyperEdge,
    HyperNode,
    InternalLanguage,
    RelationalHypergraph,
    negotiate_translation,
)


class StructuralCognitionTests(unittest.TestCase):
    def test_hypergraph_reifies_and_expands_motif_lineage(self):
        graph = RelationalHypergraph()
        for identifier in ("input", "state", "capacity"):
            graph.add_node(HyperNode(identifier, "role"))
        graph.add_edge(HyperEdge("lag", "precedes", ("input", "state")))
        graph.add_edge(HyperEdge("bound", "constrains", ("capacity", "state")))
        concept = graph.collapse(("lag", "bound"), "concept", "bounded-memory")
        self.assertEqual(concept.lineage, ("lag", "bound"))
        self.assertEqual(graph.neighbors("concept"), frozenset({"input", "state", "capacity"}))

    def test_associative_fields_diverge_with_history(self):
        first, second = AssociativeField(), AssociativeField()
        first.learn(("delay", "rhythm", "boundary"))
        second.learn(("delay", "archive", "memory"))
        self.assertIn("rhythm", first.perturb(("delay",)))
        self.assertNotIn("rhythm", second.perturb(("delay",)))

    def test_competing_models_are_retained_and_revised(self):
        immediate = CompetingWorldModel("immediate", ("lag=0",), {"lag": 0})
        delayed = CompetingWorldModel("delayed", ("lag>0",), {"lag": 3})
        immediate.update(error=0.5, tolerance=0.1)
        delayed.update(error=0.02, tolerance=0.1)
        delayed.revise(lag=4)
        self.assertGreater(delayed.plausibility, immediate.plausibility)
        self.assertEqual(delayed.revision, 1)

    def test_symbols_require_grounding_and_preserve_translation_residue(self):
        language = InternalLanguage()
        weak = GroundedSymbol("x", "op", ("one",), (), 0.5, ())
        source = GroundedSymbol("memory", "op-a", ("a", "b", "c"), (), 0.5, ())
        target = GroundedSymbol("lag", "op-b", ("b", "c", "d"), (), 0.4, ())
        self.assertFalse(language.propose(weak))
        self.assertTrue(language.propose(source))
        translation = negotiate_translation(source, target, ("a", "b", "c", "d"))
        self.assertEqual(translation.shared_cases, ("b", "c"))
        self.assertEqual(translation.residue, ("a", "d"))


if __name__ == "__main__":
    unittest.main()
