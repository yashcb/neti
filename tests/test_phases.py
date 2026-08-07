import unittest

from interpretive_ecology.phases import (
    PHASE_ONE_PROTOCOL,
    generate_distributed_world,
    run_phase_four,
    run_phase_one,
    run_phase_three,
    run_phase_two,
)


class FrozenProtocolTests(unittest.TestCase):
    def test_phase_one_replicates_success_and_preserves_negative_synergy(self):
        report = run_phase_one()
        self.assertTrue(all(report.predicates.values()))
        self.assertLessEqual(report.ecological_synergy, 0.0)
        self.assertEqual(PHASE_ONE_PROTOCOL["protocol_version"], "eie-phase-1-v1")


class DistributedIdentifiabilityTests(unittest.TestCase):
    def test_local_histories_are_disjoint_and_joint_operator_transfers(self):
        world = generate_distributed_world(0)
        self.assertEqual(len({fragment.owner for fragment in world.fragments}), 3)
        self.assertTrue(all(len(fragment.values) == 256 for fragment in world.fragments))
        report = run_phase_two()
        self.assertTrue(all(report.predicates.values()), report)
        self.assertEqual(report.learned_lag, 3)
        self.assertEqual(report.learned_table, (0, 1, 1, 0))
        self.assertGreater(report.ecological_synergy, 0.30)
        self.assertAlmostEqual(report.pooled_gap, 0.0)

    def test_phase_two_is_deterministic(self):
        self.assertEqual(run_phase_two(), run_phase_two())


class LearnedAlignmentTests(unittest.TestCase):
    def test_roles_and_capacities_are_learned_and_residue_survives(self):
        report = run_phase_three()
        self.assertTrue(all(report.predicates.values()), report)
        self.assertEqual(report.supplied_role_labels, 0)
        self.assertEqual(report.supplied_capacities, 0)
        self.assertEqual(len(report.translation_residue), 3)
        self.assertGreater(report.transfer_accuracy - report.wrong_alignment_accuracy, 0.25)


class TypedProgramTests(unittest.TestCase):
    def test_program_synthesis_and_semantic_ablations(self):
        report = run_phase_four()
        self.assertTrue(all(report.predicates.values()), report)
        self.assertEqual(report.expression, "xor(delay(driver,3),context)")
        self.assertEqual(report.deleted_name_accuracy, report.held_out_accuracy)
        self.assertLess(report.deleted_semantics_accuracy, 0.60)
        self.assertEqual(report.inlined_accuracy, report.held_out_accuracy)


if __name__ == "__main__":
    unittest.main()
