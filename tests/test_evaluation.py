import unittest

from interpretive_ecology.evaluation import evaluate_behavior


class BehavioralEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = evaluate_behavior()

    def test_ablation_is_executed_and_removes_prediction_gain(self):
        self.assertGreater(self.result.treatment_gain, 0.2)
        self.assertEqual(self.result.ablated_gain, 0.0)
        self.assertAlmostEqual(self.result.ablation_effect, self.result.treatment_gain)

    def test_restart_and_reinterpretation_have_behavioral_effects(self):
        self.assertAlmostEqual(self.result.restart_gain, self.result.treatment_gain)
        self.assertEqual(self.result.reinterpretation_effect, 3)

    def test_multiple_seeds_transfer_and_synergy_is_reported_honestly(self):
        self.assertEqual(len(self.result.seed_transfer_gains), 5)
        self.assertGreater(self.result.robustness_minimum, 0.2)
        # This controlled task does not require an ecology; record that failure.
        self.assertLessEqual(self.result.ecological_synergy, 0.0)


if __name__ == "__main__":
    unittest.main()
