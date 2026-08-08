import json
import unittest
from dataclasses import replace

from interpretive_ecology.phase7 import (
    EpisodeKernel,
    compose_boolean_language,
    _kernel_smoke_episode,
    run_phase_seven,
    run_phase_seven_zero,
)


class PhaseSevenEpisodeKernelTests(unittest.TestCase):
    def test_phase_seven_zero_closes_replays_and_hides_private_truth(self):
        report = run_phase_seven_zero()
        self.assertTrue(all(report.predicates.values()), report)
        self.assertTrue(report.exact_replay)
        self.assertTrue(report.private_truth_hidden)
        self.assertTrue(report.ownership_enforced)
        self.assertTrue(report.owned_evidence_persisted)

    def test_compositional_language_constructs_absent_nand(self):
        language = compose_boolean_language(2)
        nand = (1, 1, 1, 0)
        self.assertIn(nand, language)
        self.assertGreater(language[nand].cost, 3)
        self.assertEqual(language[nand].predict(((0, 0), (1, 1))), (1, 0))

    def test_protocol_digest_is_content_addressed(self):
        self.assertEqual(len(EpisodeKernel.protocol_digest), 64)
        int(EpisodeKernel.protocol_digest, 16)

    def test_checkpoint_tampering_is_rejected(self):
        record = _kernel_smoke_episode("neutral", {"kind": "delay", "lag": 1}, "private")
        tampered = replace(record, prior_digest="0" * 64)
        with self.assertRaises(ValueError):
            EpisodeKernel.replay(tampered)


class PhaseSevenSyntheticCurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_phase_seven()

    def test_all_confirmatory_predicates_pass(self):
        self.assertTrue(all(self.report.phase_7_0.predicates.values()), self.report)
        self.assertTrue(all(self.report.phase_7_1.predicates.values()), self.report)
        self.assertTrue(self.report.ready_for_phase_7_2)

    def test_ecology_is_necessary_but_not_better_than_pooling(self):
        phase = self.report.phase_7_1
        self.assertGreaterEqual(phase.ecological_synergy, 0.25)
        self.assertEqual(phase.mean_coalition_accuracy, phase.mean_pooled_accuracy)
        self.assertGreater(phase.mean_coalition_accuracy, phase.mean_linkage_ablation_accuracy)

    def test_intervention_operator_and_representation_controls(self):
        phase = self.report.phase_7_1
        self.assertGreater(phase.minimum_passive_version_space, 1)
        self.assertTrue(phase.all_macros_new_to_initial_grammar)
        self.assertGreater(phase.mean_coalition_accuracy, phase.mean_operator_ablation_accuracy)
        self.assertTrue(all(item.interventions > 0 for item in phase.families))
        self.assertTrue(all(item.replay_exact for item in phase.families))

    def test_result_is_json_serializable(self):
        from dataclasses import asdict

        encoded = json.dumps(asdict(self.report), sort_keys=True)
        self.assertIn('"ready_for_phase_7_2": true', encoded)


if __name__ == "__main__":
    unittest.main()
