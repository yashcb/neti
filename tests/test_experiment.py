import unittest

from interpretive_ecology.experiment import ExperimentConfig, run_experiment


class DecisiveExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_experiment()

    def test_all_pre_registered_criteria_pass(self):
        self.assertTrue(self.report.success, self.report.criteria)
        self.assertTrue(all(self.report.criteria.values()))

    def test_operator_is_discovered_and_transfers(self):
        self.assertEqual(self.report.discovered_lag, 3)
        self.assertGreater(self.report.training_gain, 0.2)
        self.assertGreater(self.report.held_out_gain, 0.2)

    def test_cue_and_ablation_controls(self):
        self.assertTrue(self.report.relevant_cue_concept)
        self.assertFalse(self.report.irrelevant_cue_concept)
        self.assertEqual(self.report.ablated_gain, 0.0)

    def test_genealogy_is_deep_and_persistent(self):
        self.assertGreaterEqual(len(self.report.concept_lineage), 5)
        self.assertGreater(self.report.persisted_later_gain, 0.2)

    def test_reproducible(self):
        repeated = run_experiment(ExperimentConfig())
        self.assertEqual(self.report.as_dict(), repeated.as_dict())


if __name__ == "__main__":
    unittest.main()
