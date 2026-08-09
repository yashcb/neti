import json
import unittest

from interpretive_ecology.phase72 import phase_seven_two_as_dict, run_phase_seven_two


class PhaseSevenTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_phase_seven_two()

    def test_all_confirmatory_predicates_pass(self):
        self.assertTrue(all(self.report.predicates.values()), self.report)

    def test_matched_multiset_order_changes_capability(self):
        for pair in self.report.order_pairs:
            self.assertTrue(pair.same_episode_multiset)
            self.assertTrue(pair.forward_target_acquired)
            self.assertFalse(pair.reverse_target_acquired)
            self.assertTrue(pair.capability_follows_checkpoint)
            self.assertTrue(pair.reset_removes_capability)

    def test_linkage_inference_abstention_and_owner_permutation(self):
        self.assertEqual(self.report.uncertain_linkage_accuracy, 1.0)
        self.assertLess(self.report.positional_linkage_accuracy, 0.25)
        self.assertTrue(self.report.ambiguous_linkage_abstained)
        self.assertEqual(self.report.owner_permutation_accuracy, 1.0)

    def test_merge_is_selective_and_persistent(self):
        self.assertTrue(self.report.compatible_merge_selected)
        self.assertTrue(self.report.incompatible_merge_rejected)
        self.assertTrue(self.report.merged_capabilities_persisted)

    def test_population_stress_has_family_level_interval(self):
        self.assertEqual(self.report.mechanism_stress_families, 64)
        self.assertEqual(self.report.mechanism_stress_accuracy, 1.0)
        self.assertGreater(self.report.mechanism_stress_wilson_interval[0], 0.94)

    def test_report_is_deterministic_json(self):
        first = json.dumps(phase_seven_two_as_dict(), sort_keys=True)
        second = json.dumps(phase_seven_two_as_dict(), sort_keys=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
