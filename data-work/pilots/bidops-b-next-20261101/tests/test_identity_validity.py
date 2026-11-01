import tempfile
from pathlib import Path
import unittest
from src.ledger import Blocked
from src.synthetic import FIXED_NOW, actor, evidence, quote, requirement, returned, seed, variant


class IdentityValidityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent, prefix="validity-")
        self.ledger = seed(Path(self.temp.name) / "pilot.sqlite")
        self.builder, self.reviewer = actor("builder"), actor("reviewer")

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def create_candidate(self, name, **changes):
        self.ledger.intake_variant("v-" + name, self.builder, variant(name, **changes))
        self.ledger.intake_requirement("r-" + name, self.builder, requirement(requirement_id=name, variant_id=name))
        self.ledger.intake_quote("q-" + name, self.builder, quote("q-" + name, variant_id=name))
        return returned(self.ledger, "m-" + name, ["river", name, "1"], "q-" + name)

    def test_expired_identity_returns_hold_but_cannot_be_commercially_approved(self):
        cid = self.create_candidate("expired", identity_valid_from="2019-01-01", identity_valid_until="2020-01-01")
        self.assertIn("identity_validity_not_current", self.ledger.candidate(cid)["candidate"]["blockers"])
        with self.assertRaises(Blocked):
            self.ledger.review_candidate("approve", self.reviewer, cid, cid, "approve", "synthetic://approve")
        self.ledger.consume_diagnostic("hold", self.reviewer, cid, cid, "synthetic://hold")
        self.assertEqual(0, self.ledger.metric_snapshot()["commercial_used"])

    def test_missing_identity_validity_is_unknown_not_current(self):
        cid = self.create_candidate("unknown", identity_valid_until=None)
        self.assertIn("identity_validity_unknown", self.ledger.candidate(cid)["candidate"]["blockers"])
        with self.assertRaises(Blocked):
            self.ledger.review_candidate("approve", self.reviewer, cid, cid, "approve", "synthetic://approve")

    def test_malformed_and_reversed_dates_reject_intake_without_receipt(self):
        for name, changes in [("bad", {"identity_valid_from": "banana"}),
                              ("reverse", {"identity_valid_from": "2027-01-01", "identity_valid_until": "2026-01-01"})]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.ledger.intake_variant(name, self.builder, variant(name, **changes))
            self.assertIsNone(self.ledger.event_receipt(name))

    def test_identity_expiring_after_review_blocks_later_application(self):
        cid = self.create_candidate("today", identity_valid_until="2026-10-31")
        self.ledger.review_candidate("approve", self.reviewer, cid, cid, "approve", "synthetic://approve")
        self.ledger.clock = lambda: FIXED_NOW.replace(day=1, month=11)
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("late-apply", self.reviewer, cid, cid, "synthetic://apply")
        self.assertIsNone(self.ledger.event_receipt("late-apply"))


if __name__ == "__main__":
    unittest.main()
