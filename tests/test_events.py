import json
import unittest

from interpretive_ecology.events import EventLedger, EventType


class EventLedgerTests(unittest.TestCase):
    def test_lineage_and_serialization(self):
        ledger = EventLedger()
        root = ledger.append(EventType.SIGNAL_RECEIVED, delta={"items": frozenset({"b", "a"})})
        child = ledger.append(EventType.ANCHOR_FOUND, parents=(root.event_id,))
        ledger.validate()
        self.assertEqual(ledger.lineage(child.event_id), (root.event_id,))
        self.assertEqual(json.loads(ledger.to_json())[0]["state_delta"]["items"], ["a", "b"])

    def test_unknown_parent_is_rejected(self):
        with self.assertRaises(ValueError):
            EventLedger().append(EventType.ANCHOR_FOUND, parents=("missing",))


if __name__ == "__main__":
    unittest.main()
