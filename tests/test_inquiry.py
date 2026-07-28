import unittest

from interpretive_ecology.cognition import CompetingWorldModel
from interpretive_ecology.inquiry import (
    DevelopmentalTension,
    InquiryOrganism,
    InvestigationAction,
    TensionState,
    create_tool,
    select_discriminating_action,
)


class InquiryMechanicsTests(unittest.TestCase):
    def test_investigation_selects_model_discriminating_consequence(self):
        models = (
            CompetingWorldModel("immediate", (), {}),
            CompetingWorldModel("delayed", (), {}),
        )
        weak = InvestigationAction("observe", {"immediate": 0.5, "delayed": 0.55}, 1.0, 1.0)
        strong = InvestigationAction("intervene", {"immediate": 0.1, "delayed": 0.9}, 2.0, 1.0)
        self.assertEqual(select_discriminating_action(models, (weak, strong)).action_id, "intervene")

    def test_tool_creation_requires_sandboxed_consequence_validation(self):
        operations = {"double": lambda value: value * 2, "offset": lambda value: value + 1}
        tool = create_tool("two-x-plus-one", ("double", "offset"), {1.0: 3.0, 3.0: 7.0}, operations, ("tension",))
        self.assertEqual(tool.apply(5.0, operations), 11.0)
        with self.assertRaises(ValueError):
            create_tool("bad", ("offset",), {1.0: 9.0}, operations, ())

    def test_inquiry_continues_only_while_tensions_generate_products(self):
        tension = DevelopmentalTension("t", "strain", ("instance",), 0.5)
        inquiry = InquiryOrganism("q", {"t": tension}, 5.0)
        tension.metabolize("concept", 0.2)
        self.assertTrue(inquiry.step(1.0, ("concept",), ("does it transfer?",)))
        self.assertTrue(inquiry.should_continue())
        tension.resolve()
        self.assertTrue(inquiry.step(1.0, ()))
        self.assertEqual(inquiry.state, "completed")
        self.assertEqual(tension.state, TensionState.RESOLVED)


if __name__ == "__main__":
    unittest.main()
