import unittest

from interpretive_ecology.inquiry import InvestigationAction, select_discriminating_action
from interpretive_ecology.cognition import CompetingWorldModel
from interpretive_ecology.readiness import run_pre_phase_seven_controls


class PrePhaseSevenReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_pre_phase_seven_controls()

    def test_all_preregistered_controls_pass(self):
        self.assertTrue(all(self.report.predicates.values()), self.report)

    def test_asynchrony_requires_identity_not_position(self):
        self.assertEqual(self.report.asynchronous_join_accuracy, 1.0)
        self.assertLess(self.report.asynchronous_positional_accuracy, 0.70)

    def test_continuous_recovery_is_not_binary_clustering(self):
        self.assertEqual(self.report.continuous_learned_lag, 3)
        self.assertLess(self.report.continuous_interaction_rmse, 0.04)
        self.assertGreater(self.report.continuous_additive_rmse, self.report.continuous_interaction_rmse * 2)

    def test_safety_is_a_constraint_not_a_utility_penalty(self):
        models = (CompetingWorldModel("a", (), {}), CompetingWorldModel("b", (), {}))
        prohibited = InvestigationAction("prohibited", {"a": -100, "b": 100}, 0.01, 0.0, 1.0)
        with self.assertRaises(ValueError):
            select_discriminating_action(models, (prohibited,), maximum_harm=0.1, minimum_reversibility=0.8)
        self.assertEqual(self.report.selected_safe_action, "reversible-probe")

    def test_noise_merge_and_grammar_negative_controls(self):
        self.assertLess(self.report.correlated_noise_robust_alarm_rate, 0.05)
        self.assertGreater(self.report.true_change_detection_rate, 0.90)
        self.assertTrue(self.report.merge_preserved_operators)
        self.assertTrue(self.report.merge_preserved_lineage_after_restart)
        self.assertLessEqual(self.report.closed_grammar_accuracy_on_nand, 0.75)
        self.assertEqual(self.report.expanded_grammar_accuracy_on_nand, 1.0)


if __name__ == "__main__":
    unittest.main()
