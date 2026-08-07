import unittest

from interpretive_ecology.advanced_phases import (
    run_phase_1_4_falsifiers,
    run_phase_five,
    run_phase_six,
)
from interpretive_ecology.system import DevelopmentalInstance, Ecology


class PhaseOneToFourFalsifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_phase_1_4_falsifiers()

    def test_noisy_scale_missing_cases_and_mechanism_family(self):
        self.assertTrue(all(self.report.predicates.values()), self.report)
        self.assertLess(self.report.noisy_scale_relative_error, 0.08)
        self.assertGreater(self.report.noisy_transfer_interval[0], 0.95)
        self.assertEqual(self.report.missing_case_transfer, 1.0)
        self.assertEqual(self.report.mechanism_family_accuracy, 1.0)

    def test_operator_is_checkpointed_inside_instance(self):
        self.assertEqual(self.report.checkpoint_operator_accuracy, 1.0)


class ActiveInquiryTests(unittest.TestCase):
    def test_observational_equivalence_requires_intervention(self):
        report = run_phase_five()
        self.assertTrue(all(report.predicates.values()), report)
        self.assertEqual(report.passive_direct_accuracy, report.passive_proxy_accuracy)
        self.assertEqual(report.selected_action, "randomize-driver")
        self.assertEqual(report.no_intervention_state, "preserve_plurality")
        self.assertTrue(report.operator_persisted)


class NonstationaryRevisionTests(unittest.TestCase):
    def test_scope_split_preserves_old_and_new_capability(self):
        report = run_phase_six()
        self.assertTrue(all(report.predicates.values()), report)
        self.assertLess(report.parent_regime_b_accuracy, 0.70)
        self.assertEqual(report.split_regime_a_accuracy, 1.0)
        self.assertEqual(report.split_regime_b_accuracy, 1.0)
        self.assertEqual(report.parent_status, "dormant")
        self.assertTrue(report.checkpoint_preserved_split)

    def test_instance_split_inherits_developmental_state(self):
        ecology = Ecology()
        parent = DevelopmentalInstance("parent", ("a", "b"), {"strain": 1.0})
        parent.encode_experience("case", {"feature": 1.0})
        parent.install_operator("op", {"kind": "delay", "lag": 1})
        ecology.add(parent)
        left, right = ecology.split("parent", ("a",), ("b",))
        for child_id in (left, right):
            child = ecology.instances[child_id]
            self.assertIn("case", child.graph.nodes)
            self.assertIn("op", child.operator_artifacts)


if __name__ == "__main__":
    unittest.main()
