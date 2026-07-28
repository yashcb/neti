import unittest

from interpretive_ecology.cognition import GroundedSymbol
from interpretive_ecology.system import DevelopmentalInstance, Ecology


def instance(identifier="instance", operations=("temporal",)):
    return DevelopmentalInstance(identifier, operations, {"strain": 0.8})


class EcologySystemTests(unittest.TestCase):
    def test_checkpoint_preserves_language_and_behavioral_reinterpretation(self):
        ecology = Ecology()
        item = instance()
        item.encode_experience("case-a", {"delay": 1.0})
        item.encode_experience("case-b", {"delay": 0.8})
        item.ground_symbol(GroundedSymbol("lag", "lag-op", ("case-a", "case-b"), (), 0.4, ()))
        self.assertEqual(item.reinterpret("concept-lag", ("case-a", "case-b")), 2)
        ecology.add(item)
        restored = Ecology.restore(ecology.checkpoint())
        carrier = restored.instances["instance"]
        self.assertIn("lag", carrier.language.symbols)
        self.assertTrue(carrier.concept_changes_retrieval("concept-lag"))

    def test_quality_diversity_allocation_protects_minority(self):
        ecology = Ecology(resource_pool=20.0)
        common, rare = instance("common"), instance("rare", ("geometric",))
        common.viability.update({"uniqueness": 0.1, "grounding": 4.0})
        rare.viability.update({"uniqueness": 1.0, "grounding": 0.0})
        ecology.add(common)
        ecology.add(rare)
        allocation = ecology.allocate({"common": 20.0, "rare": 20.0})
        self.assertGreater(allocation["rare"], 1.0)
        self.assertAlmostEqual(sum(allocation.values()), 20.0)

    def test_birth_split_merge_decay_and_revival_change_state(self):
        ecology = Ecology()
        parent = instance("parent", ("temporal", "causal"))
        ecology.spawn(parent, ("tension-a",))
        left, right = ecology.split("parent", ("temporal",), ("causal",))
        merged = ecology.merge(left, right, "descendant")
        ecology.decay(merged)
        self.assertNotIn(merged, ecology.instances)
        self.assertIn(merged, ecology.archive)
        revived = ecology.revive(merged)
        self.assertEqual(revived.status, "dormant")
        self.assertEqual(revived.parent_ids, (left, right))


if __name__ == "__main__":
    unittest.main()
