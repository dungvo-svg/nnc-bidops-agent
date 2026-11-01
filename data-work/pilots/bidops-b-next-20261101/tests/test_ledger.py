from copy import deepcopy
from datetime import timedelta
from pathlib import Path
import tempfile
import unittest

from src.ledger import Ledger, Conflict, Forbidden, Blocked
from src.synthetic import (FIXED_NOW, NODES, actor, evidence, issue, quote,
                           requirement, returned, seed, source, variant)


class LedgerBehavior(unittest.TestCase):
    def setUp(self):
        # Explicit owned workspace avoids Windows sandbox's inaccessible default Temp.
        self.temp = tempfile.TemporaryDirectory(prefix="pilot-test-", dir=Path(__file__).resolve().parent)
        self.db_path = Path(self.temp.name) / "pilot.sqlite"
        self.when = FIXED_NOW
        self.ledger = seed(self.db_path, lambda: self.when)
        self.builder, self.staff, self.reviewer = actor("builder"), actor("staff-a"), actor("reviewer")

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def revise_quote_source(self):
        self.ledger.intake_source("quote-revision", self.builder,
                                 source("quote-src", "2", "d", "2026-10-31T13:00:00Z"))

    def approve(self, candidate_id):
        return self.ledger.review_candidate("review-" + candidate_id, self.reviewer,
                                            candidate_id, candidate_id, "approve", "synthetic://review")

    def test_retry_survives_reopen_without_second_effect(self):
        issue(self.ledger, "m")
        first = self.ledger.receive_mission("received", self.staff, "m")
        before = self.ledger.counts()
        self.ledger.close()
        self.ledger = Ledger(self.db_path, NODES, lambda: self.when)
        self.assertEqual(first, self.ledger.receive_mission("received", self.staff, "m"))
        self.assertEqual(before, self.ledger.counts())

    def test_same_event_changed_payload_or_actor_is_conflict(self):
        issue(self.ledger, "m")
        self.ledger.receive_mission("same-id", self.staff, "m")
        with self.assertRaises(Conflict):
            self.ledger.receive_mission("same-id", actor("staff-b"), "m")
        with self.assertRaises(Conflict):
            self.ledger.receive_mission("same-id", self.staff, "different-mission")

    def test_same_source_version_changed_hash_rolls_back(self):
        before = self.ledger.counts()
        with self.assertRaises(Conflict):
            self.ledger.intake_source("bad-source", self.builder, source("demand-src", sha="f"))
        self.assertIsNone(self.ledger.event_receipt("bad-source"))
        self.assertEqual(before, self.ledger.counts())

    def test_ceo_capability_does_not_allow_staff_impersonation(self):
        issue(self.ledger, "m")
        with self.assertRaises(Forbidden):
            self.ledger.receive_mission("ceo-takeover", self.builder, "m")
        forged = {**self.staff, "owner_id": "fictional-ceo"}
        with self.assertRaises(Forbidden):
            self.ledger.receive_mission("forged", forged, "m")

    def test_return_requires_receipt_and_cannot_choose_unscoped_quote(self):
        issue(self.ledger, "m")
        with self.assertRaises(Blocked):
            self.ledger.return_mission("early", self.staff, "m", "q30", evidence())
        self.ledger.receive_mission("recv", self.staff, "m")
        self.ledger.respond_mission("accept", self.staff, "m", "accepted", "synthetic://accept")
        with self.assertRaises(Forbidden):
            self.ledger.return_mission("outside", self.staff, "m", "q40", evidence())

    def test_shared_offer_stored_once_used_in_two_package_candidates(self):
        a = returned(self.ledger, "a")
        b = returned(self.ledger, "b", ["hill", "line-1", "1"])
        self.assertNotEqual(a, b)
        self.assertEqual("q30", self.ledger.candidate(a)["candidate"]["quote"]["quote_id"])
        self.assertEqual("q30", self.ledger.candidate(b)["candidate"]["quote"]["quote_id"])
        self.assertEqual(3, self.ledger.counts()["quote"])
        self.assertEqual(2, len(self.ledger.package_view("river")))

    def test_same_item_code_two_lengths_cannot_cross_match(self):
        good = self.ledger.qualify(["river", "line-1", "1"], "q30", evidence())
        bad = self.ledger.qualify(["river", "line-1", "1"], "q40", evidence())
        self.assertEqual("needs_review", good["status"])
        self.assertIn("variant_mismatch", bad["blockers"])
        self.assertEqual(2, self.ledger.counts()["variant"])

    def test_mismatch_diagnostic_is_consumed_as_hold_not_commercial_use(self):
        cid = returned(self.ledger, "mismatch", quote_id="q40")
        first = self.ledger.consume_diagnostic("hold", self.reviewer, cid, cid, "synthetic://consumer/hold")
        self.assertEqual(first, self.ledger.consume_diagnostic("hold", self.reviewer, cid, cid, "synthetic://consumer/hold"))
        self.assertEqual("HOLD", first["result"]["output_status"])
        self.assertEqual("returned", self.ledger.candidate(cid)["state"]["status"])
        with self.assertRaises(Blocked):
            self.approve(cid)
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("apply-invalid", self.reviewer, cid, cid, "synthetic://apply")
        metrics = self.ledger.metric_snapshot()
        self.assertEqual(1, metrics["diagnostic_hold_used"])
        self.assertEqual(0, metrics["commercial_used"])

    def test_stale_diagnostic_consumption_is_blocked(self):
        cid = returned(self.ledger, "mismatch", quote_id="q40")
        self.revise_quote_source()
        with self.assertRaises(Blocked):
            self.ledger.consume_diagnostic("hold-stale", self.reviewer, cid, cid, "synthetic://hold")

    def test_goods_docs_money_true_do_not_approve_or_apply(self):
        cid = returned(self.ledger)
        view = self.ledger.candidate(cid)
        self.assertTrue(all(view["candidate"]["axes"].values()))
        self.assertEqual("returned", view["state"]["status"])
        self.assertEqual("not_attested", view["candidate"]["business_authorization"])
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("skip-review", self.reviewer, cid, cid, "synthetic://apply")

    def test_missing_axes_and_destination_are_preserved_as_exceptions(self):
        req = requirement(requirement_id="gap", destination=None)
        self.ledger.intake_requirement("gap-requirement", self.builder, req)
        ev = {"goods": evidence()["goods"], "documents": None, "money": None}
        cid = returned(self.ledger, "gap", ["river", "gap", "1"], ev=ev)
        blockers = self.ledger.candidate(cid)["candidate"]["blockers"]
        self.assertIn("destination_mapping_missing", blockers)
        self.assertIn("documents_evidence_missing", blockers)
        self.assertIn("money_evidence_missing", blockers)
        self.assertEqual(3, len(self.ledger.package_view("river")))

    def test_expired_missing_validity_unit_currency_and_basis_are_not_ready(self):
        variations = [({"valid_until": "2026-10-01"}, "quote_not_current"),
                      ({"valid_until": None}, "quote_validity_unknown"),
                      ({"unit": None}, "unit_unknown"),
                      ({"currency": "CNJ"}, "currency_unknown_or_unsupported"),
                      ({"basis": None}, "price_basis_unknown")]
        for i, (change, blocker) in enumerate(variations):
            q = quote(f"bad-{i}", **change)
            self.ledger.intake_quote(f"quote-{i}", self.builder, q)
            result = self.ledger.qualify(["river", "line-1", "1"], q["quote_id"], evidence())
            self.assertIn(blocker, result["blockers"])
            self.assertEqual("blocked", result["status"])

    def test_zero_price_is_known_but_blank_and_unknown_are_not_zero(self):
        for i, value in enumerate(("0", "", None)):
            q = quote(f"price-{i}", price=value)
            self.ledger.intake_quote(f"price-intake-{i}", self.builder, q)
            result = self.ledger.qualify(["river", "line-1", "1"], q["quote_id"], evidence())
            self.assertEqual(value != "0", "price_unknown_or_invalid" in result["blockers"])
        self.assertEqual("0", self.ledger._get("quote", "price-0")["price"])

    def test_equal_raw_units_cannot_override_canonical_variant_uom(self):
        self.ledger.intake_requirement("box-req", self.builder, requirement(requirement_id="box", unit="BOX"))
        self.ledger.intake_quote("box-quote", self.builder, quote("q-box", unit="BOX"))
        result = self.ledger.qualify(["river", "box", "1"], "q-box", evidence())
        self.assertIn("normalized_unit_conflict", result["blockers"])

    def test_return_and_apply_block_on_source_revision_but_history_remains(self):
        cid = returned(self.ledger, "ready")
        self.approve(cid)
        issue(self.ledger, "pending", ["hill", "line-1", "1"])
        self.ledger.receive_mission("pending-recv", self.staff, "pending")
        self.ledger.respond_mission("pending-accept", self.staff, "pending", "accepted", "synthetic://accept")
        count_before = self.ledger.counts()["events"]
        self.revise_quote_source()
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("stale-apply", self.reviewer, cid, cid, "synthetic://apply")
        with self.assertRaises(Blocked):
            self.ledger.return_mission("stale-return", self.staff, "pending", "q30", evidence())
        self.assertEqual("reviewed", self.ledger.candidate(cid)["state"]["status"])
        self.assertFalse(self.ledger.candidate(cid)["current"])
        self.assertEqual(count_before + 1, self.ledger.counts()["events"])

    def test_source_update_fanout_only_affected_candidates(self):
        a = returned(self.ledger, "a")
        b = returned(self.ledger, "b", ["hill", "line-1", "1"])
        unaffected = returned(self.ledger, "other", ["river", "line-1", "1"], "q-other")
        self.revise_quote_source()
        self.assertFalse(self.ledger.candidate(a)["current"])
        self.assertFalse(self.ledger.candidate(b)["current"])
        self.assertTrue(self.ledger.candidate(unaffected)["current"])

    def test_applied_is_not_used_and_expiry_blocks_later_use(self):
        cid = returned(self.ledger)
        self.approve(cid)
        self.ledger.apply_candidate("apply", self.reviewer, cid, cid, "synthetic://application")
        self.assertEqual("applied", self.ledger.candidate(cid)["state"]["status"])
        self.assertEqual(0, self.ledger.metric_snapshot()["commercial_used"])
        self.when += timedelta(days=31)
        with self.assertRaises(Blocked):
            self.ledger.use_candidate("late-use", self.reviewer, cid, cid, "synthetic://use")

    def test_explicit_use_and_wrong_capability_and_hash_are_separate(self):
        cid = returned(self.ledger)
        self.approve(cid)
        with self.assertRaises(Forbidden):
            self.ledger.apply_candidate("staff-apply", self.staff, cid, cid, "synthetic://apply")
        with self.assertRaises(Conflict):
            self.ledger.apply_candidate("wrong-hash", self.reviewer, cid, "0" * 64, "synthetic://apply")
        with self.assertRaises(Blocked):
            self.ledger.use_candidate("too-early", self.reviewer, cid, cid, "synthetic://use")
        self.ledger.apply_candidate("apply", self.reviewer, cid, cid, "synthetic://apply")
        self.ledger.use_candidate("use", self.reviewer, cid, cid, "synthetic://actual-consumer")
        self.assertEqual(1, self.ledger.metric_snapshot()["commercial_used"])

    def test_same_owner_cannot_self_review_even_with_review_capability(self):
        cid = returned(self.ledger)
        with self.assertRaises(Forbidden):
            self.ledger.review_candidate("self-review", self.staff, cid, cid, "approve", "synthetic://self")

    def test_new_requirement_version_blocks_old_review(self):
        cid = returned(self.ledger)
        self.approve(cid)
        req = requirement(version="2", destination="fictional-sheet/new-line")
        self.ledger.intake_requirement("req-revised", self.builder, req, expected_previous_version="1")
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("old-apply", self.reviewer, cid, cid, "synthetic://apply")
        self.assertEqual("2", self.ledger.package_view("river")[0]["version"])

    def test_old_source_backfill_does_not_restore_stale_candidate(self):
        cid = returned(self.ledger)
        self.revise_quote_source()
        self.ledger.intake_source("old-backfill", self.builder,
                                 source("quote-src", "0", "e", "2026-10-20T00:00:00Z"))
        self.assertFalse(self.ledger.candidate(cid)["current"])

    def test_late_unseen_requirement_version_cannot_roll_back_head(self):
        self.ledger.intake_requirement("v2", self.builder, requirement(version="2"), expected_previous_version="1")
        with self.assertRaises(Conflict):
            self.ledger.intake_requirement("late-v0", self.builder, requirement(version="0"))
        self.assertEqual("2", self.ledger.package_view("river")[0]["version"])
        self.assertIsNone(self.ledger.event_receipt("late-v0"))

    def test_node_config_cannot_silently_gain_capabilities_on_reopen(self):
        changed = deepcopy(NODES)
        changed[1]["capabilities"].append("candidate_apply")
        with self.assertRaises(Conflict):
            Ledger(self.db_path, changed, lambda: self.when)

    def test_lao_unicode_roundtrips_in_durable_receipt(self):
        title = "ຕົວຢ່າງ ຂໍ້ມູນຈຳລອງ"
        receipt = self.ledger.create_case("lao", self.builder, "lao-case", title)
        self.ledger.close()
        self.ledger = Ledger(self.db_path, NODES, lambda: self.when)
        self.assertEqual(receipt, self.ledger.event_receipt("lao"))
        self.assertEqual(title, self.ledger._get("tender_case", "lao-case")["title"])

    def link(self, link_id, case="river", need="prebid_sourcing", qty="10", line="line-1"):
        return self.ledger.link_demand(link_id, self.builder,
                                      {"link_id": link_id, "requirement_key": [case, line, "1"],
                                       "need_type": need, "quantity": qty})

    def test_closing_only_one_case_keeps_shared_variant_and_all_sources(self):
        self.link("river-demand")
        self.link("hill-demand", "hill", qty="20")
        before = self.ledger.counts()
        self.assertEqual("30", self.ledger.active_worklist()[0]["quantity"])
        self.ledger.transition_case("close-river", self.builder, "river", "close", "explicit fictional closure")
        work = self.ledger.active_worklist()
        self.assertEqual(1, len(work))
        self.assertEqual("20", work[0]["quantity"])
        self.assertEqual("hill", work[0]["demand_links"][0]["requirement_key"][0])
        for kind in ("source", "quote", "variant", "requirement", "demand_link"):
            self.assertEqual(before[kind], self.ledger.counts()[kind])

    def test_reopen_restores_demand_but_late_quote_does_not(self):
        self.link("river-demand")
        self.ledger.transition_case("close", self.builder, "river", "close", "explicit")
        self.ledger.intake_quote("late-quote", self.builder, quote("late-quote"))
        self.link("late-demand", qty="2")
        self.assertEqual([], self.ledger.active_worklist())
        self.assertEqual("closed", self.ledger.case_status("river")["status"])
        self.ledger.transition_case("reopen", self.builder, "river", "reopen", "approved synthetic reopening")
        self.assertEqual("12", self.ledger.active_worklist()[0]["quantity"])

    def test_deadline_passage_planned_close_and_extension_keep_unknown_visible(self):
        self.link("river-demand")
        self.ledger.plan_case_closure("planned", self.builder, "river", "2026-10-31T13:00:00Z", "plan only")
        self.when += timedelta(days=4)
        self.assertEqual("active", self.ledger.case_status("river")["status"])
        self.assertEqual("overdue_unknown", self.ledger.case_status("river")["timeline_status"])
        self.assertEqual(1, len(self.ledger.active_worklist()))
        self.ledger.set_case_deadline("extended", self.builder, "river", "2026-11-10T10:00:00Z", "documented synthetic extension")
        self.assertEqual("active", self.ledger.case_status("river")["timeline_status"])
        self.assertIsNotNone(self.ledger.event_receipt("planned"))
        self.assertIsNotNone(self.ledger.event_receipt("extended"))

    def test_overdue_unknown_blocks_promotion_without_hiding_demand(self):
        self.link("river-demand")
        cid = returned(self.ledger)
        self.approve(cid)
        self.when += timedelta(days=4)
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("past-deadline", self.reviewer, cid, cid, "synthetic://apply")
        self.assertEqual("active", self.ledger.case_status("river")["status"])
        self.assertEqual(1, len(self.ledger.active_worklist()))

    def test_won_package_retains_fulfillment_until_explicitly_finished(self):
        self.link("prebid")
        self.link("purchase-after-win", need="fulfillment", qty="4")
        self.ledger.transition_case("won", self.builder, "river", "win", "synthetic award receipt")
        work = self.ledger.active_worklist()
        self.assertEqual(["fulfillment"], [w["need_type"] for w in work])
        self.ledger.finish_demand("delivered", self.builder, "purchase-after-win", "fulfilled", "synthetic receipt")
        self.assertEqual([], self.ledger.active_worklist())

    def test_closed_case_blocks_late_mission_return_and_promotion(self):
        cid = returned(self.ledger)
        self.approve(cid)
        issue(self.ledger, "pending")
        self.ledger.receive_mission("pending-received", self.staff, "pending")
        self.ledger.transition_case("closed", self.builder, "river", "close", "explicit")
        with self.assertRaises(Blocked):
            self.ledger.return_mission("late-return", self.staff, "pending", "q30", evidence())
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("late-apply", self.reviewer, cid, cid, "synthetic://apply")

    def test_identity_retains_registration_and_unresolved_rows_do_not_merge(self):
        second = variant("v30-registration-B", registration_id="fictional-registration-B")
        self.ledger.intake_variant("other-reg", self.builder, second)
        self.assertEqual(3, self.ledger.counts()["variant"])
        for name in ("unresolved-row-A", "unresolved-row-B"):
            self.ledger.intake_variant(name, self.builder, variant(name, specification=None, unit=None))
        with self.assertRaises(Conflict):
            self.ledger.intake_variant("alias", self.builder, variant("different-id-same-complete-identity"))
        self.assertEqual(5, self.ledger.counts()["variant"])

    def test_ambiguous_identity_demand_remains_visible_and_blocked(self):
        self.ledger.intake_variant("unknown", self.builder, variant("unknown-row", specification=None))
        req = requirement(requirement_id="unknown-row", variant_id="unknown-row", destination=None)
        self.ledger.intake_requirement("unknown-req", self.builder, req)
        self.link("unknown-link", line="unknown-row")
        work = self.ledger.active_worklist()
        self.assertIn("normalized_identity_incomplete", work[0]["demand_links"][0]["flags"])
        self.assertIn("destination_mapping_missing", work[0]["demand_links"][0]["flags"])

    def test_unknown_quantity_is_active_and_never_assumed_zero(self):
        self.link("known", qty="10")
        self.link("unknown", "hill", qty=None)
        work = self.ledger.active_worklist()[0]
        self.assertEqual("10", work["known_quantity"])
        self.assertEqual(1, work["unknown_quantity_count"])
        self.assertIsNone(work["quantity"])
        self.assertEqual(2, len(work["demand_links"]))
        self.assertTrue(self.ledger.prebid_demand_active(["hill", "line-1", "1"]))

    def test_stale_requirement_quantity_is_not_added_to_current_quantity(self):
        self.link("v1-demand", qty="10")
        self.ledger.intake_requirement("req-v2", self.builder, requirement(version="2"), expected_previous_version="1")
        self.ledger.link_demand("v2-demand", self.builder,
                               {"link_id": "v2-demand", "requirement_key": ["river", "line-1", "2"],
                                "need_type": "prebid_sourcing", "quantity": "15"})
        work = self.ledger.active_worklist()[0]
        self.assertEqual("15", work["known_quantity"])
        self.assertEqual(1, work["stale_demand_count"])
        self.assertIsNone(work["quantity"])

    def test_cancelled_demand_blocks_pending_mission_and_promotion(self):
        self.link("prebid")
        cid = returned(self.ledger)
        self.approve(cid)
        issue(self.ledger, "pending")
        self.ledger.finish_demand("cancel-demand", self.builder, "prebid", "cancelled", "explicit")
        with self.assertRaises(Blocked):
            self.ledger.receive_mission("late-receive", self.staff, "pending")
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("late-apply", self.reviewer, cid, cid, "synthetic://apply")
        self.assertEqual("active", self.ledger.case_status("river")["status"])

    def test_price_arrival_does_not_create_or_restart_demand(self):
        self.ledger.intake_quote("late-price", self.builder, quote("fresh-arrival"))
        mission = {"mission_id": "no-demand", "node_id": "staff-a", "requirement_key": ["river", "line-1", "1"],
                   "quote_ids": ["q30"], "source_manifest": [{"source_id": "demand-src", "version": "1"},
                   {"source_id": "quote-src", "version": "1"}], "deadline": "2026-11-02T00:00:00Z",
                   "expected_output": "inspect"}
        with self.assertRaises(Blocked):
            self.ledger.issue_mission("no-demand", self.builder, mission)
        self.assertEqual([], self.ledger.active_worklist())

    def test_received_needs_input_and_rejected_are_not_acceptance(self):
        issue(self.ledger, "m")
        self.ledger.receive_mission("recv", self.staff, "m")
        with self.assertRaises(Blocked):
            self.ledger.return_mission("received-only", self.staff, "m", "q30", evidence())
        self.ledger.respond_mission("needs-input", self.staff, "m", "needs_input", "synthetic://need-more-context")
        with self.assertRaises(Blocked):
            self.ledger.return_mission("needs-input-return", self.staff, "m", "q30", evidence())
        self.ledger.respond_mission("reject", self.staff, "m", "rejected", "synthetic://not-in-scope")
        with self.assertRaises(Blocked):
            self.ledger.respond_mission("accept-rejected", self.staff, "m", "accepted", "synthetic://cannot-revive")

    def test_wip_one_releases_on_cancel_with_history_preserved(self):
        for mission_id in ("m1", "m2"):
            issue(self.ledger, mission_id)
            self.ledger.receive_mission(mission_id + "-recv", self.staff, mission_id)
        self.ledger.respond_mission("accept-first", self.staff, "m1", "accepted", "synthetic://accept")
        with self.assertRaises(Blocked):
            self.ledger.respond_mission("over-capacity", self.staff, "m2", "accepted", "synthetic://accept")
        self.ledger.cancel_mission("cancel-first", self.builder, "m1", "synthetic://cancel")
        self.ledger.respond_mission("accept-second", self.staff, "m2", "accepted", "synthetic://accept")
        self.assertIsNotNone(self.ledger.event_receipt("accept-first"))
        with self.assertRaises(Blocked):
            self.ledger.return_mission("cancelled-return", self.staff, "m1", "q30", evidence())

    def test_cancel_after_produced_does_not_undo_existing_application(self):
        cid = returned(self.ledger)
        self.approve(cid)
        self.ledger.apply_candidate("apply", self.reviewer, cid, cid, "synthetic://apply")
        receipt = self.ledger.cancel_mission("cancel-produced", self.builder, "m1", "synthetic://cancel")
        self.assertFalse(receipt["result"]["automatic_undo"])
        self.assertEqual("applied", self.ledger.candidate(cid)["state"]["status"])
        with self.assertRaises(Blocked):
            self.ledger.use_candidate("new-use", self.reviewer, cid, cid, "synthetic://use")

    def test_source_row_without_mpsc_unit_or_quantity_never_invents_identity(self):
        for row_id in ("source-row-1", "source-row-2"):
            self.ledger.intake_variant(row_id + "-variant", self.builder,
                                       variant(row_id, item_code=None, specification=None, unit=None,
                                               registration_id=None, identity_valid_from=None, identity_valid_until=None))
            self.ledger.intake_requirement(row_id + "-requirement", self.builder,
                                           requirement(requirement_id=row_id, variant_id=row_id,
                                                       item_code=None, unit=None, destination=None))
            self.ledger.link_demand(row_id + "-demand", self.builder,
                                   {"link_id": row_id + "-demand", "requirement_key": ["river", row_id, "1"],
                                    "need_type": "prebid_sourcing", "quantity": None})
        work = self.ledger.active_worklist()
        self.assertEqual(2, len(work))
        self.assertTrue(all(w["quantity"] is None and w["variant"]["item_code"] is None for w in work))
        self.assertTrue(all(not w["variant"]["identity_complete"] for w in work))


if __name__ == "__main__":
    unittest.main()
