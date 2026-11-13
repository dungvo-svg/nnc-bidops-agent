"""Acceptance regressions for the B-next lifecycle slice (synthetic, local only)."""
from datetime import date, timedelta
from pathlib import Path
import tempfile
import unittest

from src.catalog_lifecycle import create_fulfillment, transition_case as catalog_transition
from src.ledger import Blocked, Conflict, Forbidden
from src.synthetic import FIXED_NOW, actor, evidence, issue, quote, returned, seed
from tests import test_catalog_lifecycle as catalog_tests


class LedgerLifecycleRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="next-test-", dir=Path(__file__).resolve().parent)
        self.when = FIXED_NOW
        self.ledger = seed(Path(self.temp.name) / "pilot.sqlite", lambda: self.when)
        self.builder, self.staff, self.reviewer = actor("builder"), actor("staff-a"), actor("reviewer")

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def link(self, link_id, case="river", need="prebid_sourcing", qty="10", who=None):
        return self.ledger.link_demand(link_id, who or self.builder,
                                       {"link_id": link_id, "requirement_key": [case, "line-1", "1"],
                                        "need_type": need, "quantity": qty})

    def approve(self, candidate_id):
        return self.ledger.review_candidate("review-" + candidate_id, self.reviewer,
                                            candidate_id, candidate_id, "approve", "synthetic://review")

    # fulfillment only after won
    def test_fulfillment_before_won_is_rejected_atomically(self):
        before = self.ledger.counts()
        with self.assertRaises(Blocked):
            self.link("early-purchase", need="fulfillment", qty="4")
        self.assertIsNone(self.ledger.event_receipt("early-purchase"))
        self.assertEqual(before, self.ledger.counts())
        self.ledger.transition_case("close", self.builder, "river", "close", "explicit")
        with self.assertRaises(Blocked):
            self.link("closed-purchase", need="fulfillment", qty="4")
        self.ledger.transition_case("reopen", self.builder, "river", "reopen", "explicit")
        self.ledger.transition_case("won", self.builder, "river", "win", "synthetic award receipt")
        self.assertEqual("open", self.link("purchase", need="fulfillment", qty="4")["result"]["status"])

    def test_fulfillment_retry_keeps_receipt_and_changed_payload_or_actor_conflicts(self):
        self.ledger.transition_case("won", self.builder, "river", "win", "synthetic award receipt")
        first = self.link("purchase", need="fulfillment", qty="4")
        self.assertEqual(first, self.link("purchase", need="fulfillment", qty="4"))
        with self.assertRaises(Conflict):
            self.link("purchase", need="fulfillment", qty="5")
        with self.assertRaises(Conflict):
            self.link("purchase", need="fulfillment", qty="4", who=self.staff)

    # deadlines: passage never closes, extension is not a correction
    def test_deadline_passage_does_not_auto_close_or_unlock_promotion(self):
        self.link("river-demand")
        cid = returned(self.ledger)
        self.approve(cid)
        self.when += timedelta(days=10)
        state = self.ledger.case_status("river")
        self.assertEqual(("active", "overdue_unknown"), (state["status"], state["timeline_status"]))
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("late-apply", self.reviewer, cid, cid, "synthetic://apply")
        self.assertEqual(["river-demand"], [d["link_id"] for d in self.ledger.active_worklist()[0]["demand_links"]])

    def test_extension_must_be_later_and_correction_is_flagged_not_decided(self):
        with self.assertRaises(ValueError):
            self.ledger.extend_case_deadline("bad-ext", self.builder, "river",
                                             "2026-11-01T10:00:00Z", "synthetic://extension")
        self.assertIsNone(self.ledger.event_receipt("bad-ext"))
        ext = self.ledger.extend_case_deadline("ext", self.builder, "river",
                                               "2026-11-10T10:00:00Z", "synthetic://extension")
        self.assertEqual("extension", ext["result"]["semantics"])
        back = self.ledger.set_case_deadline("fix", self.builder, "river",
                                             "2026-11-05T10:00:00Z", "synthetic typo correction")
        self.assertEqual("correction", back["result"]["semantics"])
        self.assertEqual("pending_business_decision", back["result"]["backward_correction_policy"])
        self.assertEqual("active", self.ledger.case_status("river")["status"])

    # close one case keeps shared demand
    def test_closing_one_case_keeps_other_case_demand_and_mission_scope(self):
        self.link("river-demand")
        self.link("hill-demand", "hill", qty="20")
        self.ledger.transition_case("close", self.builder, "river", "close", "explicit")
        self.assertFalse(self.ledger.prebid_demand_active(["river", "line-1", "1"]))
        self.assertTrue(self.ledger.prebid_demand_active(["hill", "line-1", "1"]))
        self.assertEqual("issued", issue(self.ledger, "hill-m", ["hill", "line-1", "1"])["result"]["status"])

    # reopen is a new scope
    def test_reopen_does_not_inherit_review_or_old_mission(self):
        cid = returned(self.ledger)
        self.approve(cid)
        issue(self.ledger, "pending")
        self.ledger.receive_mission("pending-received", self.staff, "pending")
        self.ledger.respond_mission("pending-accept", self.staff, "pending", "accepted", "synthetic://scope")
        self.ledger.transition_case("close", self.builder, "river", "close", "explicit")
        self.ledger.transition_case("reopen", self.builder, "river", "reopen", "approved synthetic reopening")
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("old-apply", self.reviewer, cid, cid, "synthetic://apply")
        self.assertFalse(self.ledger.candidate(cid)["current"])
        with self.assertRaises(Blocked):
            self.ledger.return_mission("late-return", self.staff, "pending", "q30", evidence())
        self.ledger.cancel_mission("pending-cancel", self.builder, "pending", "synthetic://reopen-scope")
        fresh = returned(self.ledger, "after-reopen")
        self.assertNotEqual(cid, fresh)
        self.approve(fresh)
        self.assertEqual("applied", self.ledger.apply_candidate(
            "fresh-apply", self.reviewer, fresh, fresh, "synthetic://apply")["result"]["status"])

    # identity and price
    def test_same_item_code_different_spec_is_never_merged(self):
        self.ledger.link_demand("d30", self.builder, {"link_id": "d30", "requirement_key": ["river", "line-1", "1"],
                                                      "need_type": "prebid_sourcing", "quantity": "10"})
        self.ledger.link_demand("d40", self.builder, {"link_id": "d40", "requirement_key": ["river", "line-2", "1"],
                                                      "need_type": "prebid_sourcing", "quantity": "5"})
        self.assertEqual({"v30", "v40"}, {g["variant"]["variant_id"] for g in self.ledger.active_worklist()})
        blockers = self.ledger.qualify(["river", "line-2", "1"], "q30", evidence())["blockers"]
        self.assertIn("variant_mismatch", blockers)

    def test_historical_price_is_not_current_and_cannot_be_approved(self):
        self.ledger.intake_quote("old-quote", self.builder,
                                 quote("q-2025", valid_from="2025-01-01", valid_until="2025-12-31"))
        cid = returned(self.ledger, "hist", quote_id="q-2025")
        self.assertIn("quote_not_current", self.ledger.candidate(cid)["candidate"]["blockers"])
        with self.assertRaises(Blocked):
            self.approve(cid)

    # evidence
    def test_missing_tampered_or_out_of_scope_evidence_cannot_promote(self):
        ev = evidence()
        ev["money"] = None
        cid = returned(self.ledger, "missing", ev=ev)
        self.assertIn("money_evidence_missing", self.ledger.candidate(cid)["candidate"]["blockers"])
        with self.assertRaises(Blocked):
            self.approve(cid)
        self.ledger.cancel_mission("missing-cancel", self.builder, "missing", "synthetic://wip-release")
        with self.assertRaises(Forbidden):
            returned(self.ledger, "outside", ev=evidence("other-src"))
        self.ledger.cancel_mission("outside-cancel", self.builder, "outside", "synthetic://wip-release")
        good = returned(self.ledger, "good")
        with self.assertRaises(Conflict):
            self.ledger.review_candidate("tampered", self.reviewer, good, "0" * 64, "approve", "synthetic://review")
        self.assertEqual("returned", self.ledger.candidate(good)["state"]["status"])

    # no skipped steps
    def test_received_accepted_returned_reviewed_applied_used_cannot_skip(self):
        issue(self.ledger, "m")
        with self.assertRaises(Blocked):
            self.ledger.respond_mission("early-accept", self.staff, "m", "accepted", "synthetic://scope")
        self.ledger.receive_mission("m-receive", self.staff, "m")
        with self.assertRaises(Blocked):
            self.ledger.return_mission("early-return", self.staff, "m", "q30", evidence())
        self.ledger.respond_mission("m-accept", self.staff, "m", "accepted", "synthetic://scope")
        cid = self.ledger.return_mission("m-return", self.staff, "m", "q30",
                                         evidence())["result"]["candidate"]["candidate_hash"]
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("early-apply", self.reviewer, cid, cid, "synthetic://apply")
        with self.assertRaises(Blocked):
            self.ledger.use_candidate("early-use", self.reviewer, cid, cid, "synthetic://use")
        self.approve(cid)
        with self.assertRaises(Blocked):
            self.ledger.use_candidate("still-early-use", self.reviewer, cid, cid, "synthetic://use")
        self.ledger.apply_candidate("apply", self.reviewer, cid, cid, "synthetic://apply")
        self.assertEqual("used", self.ledger.use_candidate("use", self.reviewer, cid, cid,
                                                           "synthetic://use")["result"]["status"])


class CatalogLifecycleRegressions(unittest.TestCase):
    # Reuse the fictional four-BV fixture without re-running its test methods.
    setUp = catalog_tests.CatalogLifecycleBehavior.setUp
    tearDown = catalog_tests.CatalogLifecycleBehavior.tearDown
    query = catalog_tests.CatalogLifecycleBehavior.query
    shared_lines = catalog_tests.CatalogLifecycleBehavior.shared_lines

    def test_fulfillment_before_won_is_rejected_in_catalog_api(self):
        line = next(line for line, case in self.shared_lines() if case == "SETTHA2027")
        before = self.query("SELECT count(*) FROM fulfillment_need")
        with self.assertRaises(ValueError):
            create_fulfillment(self.db, "early", "need-early", line, "4", "synthetic://early")
        catalog_transition(self.db, "close", "SETTHA2027", "close", "synthetic://close")
        with self.assertRaises(ValueError):
            create_fulfillment(self.db, "closed", "need-closed", line, "4", "synthetic://closed")
        self.assertEqual(before, self.query("SELECT count(*) FROM fulfillment_need"))
        catalog_transition(self.db, "reopen", "SETTHA2027", "reopen", "synthetic://reopen")
        catalog_transition(self.db, "won", "SETTHA2027", "win", "synthetic://award")
        self.assertEqual("open", create_fulfillment(self.db, "after-win", "need", line, None,
                                                    "synthetic://remaining")["result"]["status"])


if __name__ == "__main__":
    unittest.main()
