"""Ledger side of the catalog bridge: one case authority, provenance, assessments."""
from datetime import timedelta
from pathlib import Path
import tempfile
import unittest

from src.catalog_bridge import bridge_variant, read_case_snapshot
from src.catalog_lifecycle import resolve_line, transition_case as catalog_transition
from src.ledger import Blocked, Conflict, Ledger, digest
from src.synthetic import FIXED_NOW, NODES, actor, evidence, issue, returned, seed, source
from tests import test_catalog_lifecycle as catalog_tests

ASSESSMENTS = {"dossier_compliance", "supply_capability", "economics_working_capital",
               "competitive_basis", "actual_outcome"}


def snap(case_id="river", status="active", planning_date="2026-11-26", official=None, events=()):
    body = {"schema": "bidops-case-snapshot/1", "case_id": case_id, "status": status,
            "planning_date": planning_date, "official_closing_at": official,
            "source_status": "fictional", "active_source_version": "fictional-v1",
            "closure_policy": "explicit_only", "lifecycle_events": list(events)}
    return {**body, "snapshot_sha256": digest(body)}


def bridged(variant_id, length, status="BRIDGED"):
    return {"status": status, "line_id": "line-" + variant_id, "case_id": "river",
            "variant": {"variant_id": variant_id, "item_code": "SAME-CODE",
                        "specification": {"catalog_specification": f"fictional{length}mm"}, "unit": "EA",
                        "registration_id": None, "identity_valid_from": "2026-01-01",
                        "identity_valid_until": "2027-12-31"},
            "provenance": {"mapping": "explicit_reviewed_line_resolution", "catalog_variant_id": variant_id,
                           "catalog_identity_sha256": "e" * 64, "resolution_evidence_ref": "synthetic://review",
                           "reviewed_by": "fictional-independent-owner", "line_id": "line-" + variant_id,
                           "case_id": "river", "source_version": "f" * 64, "source_anchor": "synthetic:1",
                           "name_raw": "fictional needle", "uom_raw": "EA"},
            "flags": []}


PRODUCT = {"trade_name": "Fixture-A", "manufacturer": "Factory-A", "strength": "1", "form": "tab", "pack": "box"}


class LedgerCatalogBridge(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bridge-test-", dir=Path(__file__).resolve().parent)
        self.when = FIXED_NOW
        self.ledger = seed(Path(self.temp.name) / "pilot.sqlite", lambda: self.when)
        self.builder, self.staff, self.reviewer = actor("builder"), actor("staff-a"), actor("reviewer")

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def adopt(self, event_id, snapshot, previous=None):
        return self.ledger.adopt_case_snapshot(event_id, self.builder, snapshot, previous)

    def approve(self, candidate_id):
        return self.ledger.review_candidate("review-" + candidate_id, self.reviewer,
                                            candidate_id, candidate_id, "approve", "synthetic://review")

    # --- one case authority ---
    def test_bound_case_refuses_ledger_side_transitions_and_deadline_writes(self):
        first = self.adopt("bind", snap())
        self.assertEqual(first, self.adopt("bind", snap()))
        self.assertEqual("catalog_snapshot", self.ledger.case_status("river")["authority"])
        for call in (lambda: self.ledger.transition_case("t", self.builder, "river", "close", "x"),
                     lambda: self.ledger.set_case_deadline("d", self.builder, "river", "2026-11-09T00:00:00Z", "x"),
                     lambda: self.ledger.extend_case_deadline("e", self.builder, "river",
                                                              "2026-12-09T00:00:00Z", "synthetic://x")):
            with self.assertRaises(Blocked):
                call()
        self.assertEqual("ledger", self.ledger.case_status("hill")["authority"])
        self.ledger.transition_case("hill-close", self.builder, "hill", "close", "unbound case keeps ledger control")

    def test_snapshot_cas_and_tamper_are_rejected_atomically(self):
        one = snap()
        self.adopt("bind", one)
        closed = snap(status="closed", events=[{"event_id": "c", "kind": "common_case_transition",
                                                 "evidence_ref": "synthetic://close"}])
        with self.assertRaises(Conflict):
            self.adopt("stale", closed, None)
        tampered = {**closed, "status": "won"}
        with self.assertRaises(ValueError):
            self.adopt("tamper", tampered, one["snapshot_sha256"])
        self.assertIsNone(self.ledger.event_receipt("stale"))
        self.assertIsNone(self.ledger.event_receipt("tamper"))
        self.assertEqual("active", self.ledger.case_status("river")["status"])
        self.adopt("close", closed, one["snapshot_sha256"])
        self.assertEqual("closed", self.ledger.case_status("river")["status"])

    def test_planning_date_is_not_a_legal_hour_but_passing_it_is_overdue_unknown(self):
        self.adopt("bind", snap(planning_date="2026-11-01"))
        state = self.ledger.case_status("river")
        self.assertIsNone(state["deadline"])
        self.assertEqual("active", state["timeline_status"])
        self.when += timedelta(days=2)
        state = self.ledger.case_status("river")
        self.assertEqual(("active", "overdue_unknown"), (state["status"], state["timeline_status"]))

    def test_snapshot_reopen_starts_new_scope_and_snapshot_change_stales_candidate(self):
        cid = returned(self.ledger)
        one = snap()
        self.adopt("bind", one)
        with self.assertRaises(Blocked):  # authority changed after the candidate
            self.approve(cid)
        self.ledger.cancel_mission("m1-cancel", self.builder, "m1", "synthetic://rebind")
        fresh = returned(self.ledger, "m2")
        self.approve(fresh)
        close_event = {"event_id": "c", "kind": "common_case_transition", "evidence_ref": "synthetic://c"}
        closed = snap(status="closed", events=[close_event])
        self.adopt("close", closed, one["snapshot_sha256"])
        reopened = snap(events=[close_event, {"event_id": "r", "kind": "common_case_transition",
                                              "evidence_ref": "synthetic://r"}])
        with self.assertRaises(Conflict):  # correct head hash, but an older snapshot cannot roll back
            self.adopt("rollback", one, closed["snapshot_sha256"])
        self.assertIsNone(self.ledger.event_receipt("rollback"))
        receipt = self.adopt("reopen", reopened, closed["snapshot_sha256"])
        self.assertTrue(receipt["result"]["case_reopened"])
        with self.assertRaises(Blocked):
            self.ledger.apply_candidate("old-apply", self.reviewer, fresh, fresh, "synthetic://apply")

    def test_fulfillment_follows_catalog_won_snapshot(self):
        one = snap()
        self.adopt("bind", one)
        link = {"link_id": "purchase", "requirement_key": ["river", "line-1", "1"],
                "need_type": "fulfillment", "quantity": None}
        with self.assertRaises(Blocked):
            self.ledger.link_demand("purchase", self.builder, link)
        self.adopt("won", snap(status="won"), one["snapshot_sha256"])
        self.assertEqual("open", self.ledger.link_demand("purchase", self.builder, link)["result"]["status"])

    # --- identity bridge ---
    def test_bridged_variants_keep_spec_and_provenance_and_hold_is_refused(self):
        self.ledger.intake_bridged_variant("b30", self.builder, bridged("cat-30", "30"))
        self.ledger.intake_bridged_variant("b40", self.builder, bridged("cat-40", "40"))
        self.assertNotEqual(self.ledger._get("variant", "cat-30")["identity_hash"],
                            self.ledger._get("variant", "cat-40")["identity_hash"])
        self.assertEqual("e" * 64, self.ledger._get("variant_provenance", "line-cat-30")["catalog_identity_sha256"])
        hold = {**bridged("cat-hold", "30", "HOLD"), "variant": None, "provenance": None}
        with self.assertRaises(ValueError):
            self.ledger.intake_bridged_variant("hold", self.builder, hold)
        missing = bridged("cat-x", "50")
        missing["provenance"] = None
        with self.assertRaises(ValueError):
            self.ledger.intake_bridged_variant("noprov", self.builder, missing)
        self.assertIsNone(self.ledger.event_receipt("hold"))

    # --- assessments wired into qualification ---
    def test_without_checks_five_assessments_are_unknown_with_reason_and_no_score(self):
        got = self.ledger.qualify(["river", "line-1", "1"], "q30", evidence())
        self.assertEqual(ASSESSMENTS, set(got["business_assessments"]))
        for item in got["business_assessments"].values():
            self.assertEqual("unknown", item["status"])
            self.assertTrue(item["reason"])
            self.assertNotIn("score", item)
        self.assertEqual("needs_review", got["status"])

    def certificate(self, product=PRODUCT, **dates):
        return {"certificate": {"required": PRODUCT, "certificate": {"product": product, **dates},
                                "source_ref": {"source_id": "quote-src", "version": "1"}}}

    def test_certificate_conflict_or_expiry_blocks_and_match_is_not_approval(self):
        bad = self.ledger.qualify(["river", "line-1", "1"], "q30", evidence(),
                                  self.certificate({**PRODUCT, "strength": "2"}))
        self.assertIn("certificate_identity_conflict", bad["blockers"])
        expired = self.ledger.qualify(["river", "line-1", "1"], "q30", evidence(),
                                      self.certificate(registration_valid_until="2026-01-01"))
        self.assertIn("certificate_registration_valid_until_expired", expired["blockers"])
        good = self.ledger.qualify(["river", "line-1", "1"], "q30", evidence(),
                                   self.certificate(registration_valid_until="2027-01-01"))
        dossier = good["business_assessments"]["dossier_compliance"]
        self.assertEqual("checked_fixture_only", dossier["status"])
        self.assertEqual("not_attested", good["assessment_checks"]["certificate"]["business_approval"])
        self.assertEqual("needs_review", good["status"])

    def test_portfolio_overcommit_blocks_and_costs_stay_per_currency(self):
        checks = {"portfolio": {"resources": {"stock": {"available": "10", "unit": "box"}},
                                "allocations": [{"allocation_id": "a", "case_id": "river", "resource_id": "stock",
                                                 "quantity": "7", "unit": "box"},
                                                {"allocation_id": "b", "case_id": "hill", "resource_id": "stock",
                                                 "quantity": "6", "unit": "box"}],
                                "costs": [{"cost_id": "f", "amount": "5", "currency": "USD",
                                           "date": "2026-10-31", "basis": "incremental"}],
                                "source_ref": {"source_id": "demand-src", "version": "1"}}}
        got = self.ledger.qualify(["river", "line-1", "1"], "q30", evidence(), checks)
        self.assertIn("portfolio_overcommitted", got["blockers"])
        self.assertEqual({"USD"}, set(got["assessment_checks"]["portfolio"]["costs_by_currency"]))
        self.assertEqual("unknown", got["business_assessments"]["competitive_basis"]["status"])

    def test_check_source_drift_stales_candidate_and_payload_without_checks_is_unchanged(self):
        issue(self.ledger, "m")
        self.ledger.receive_mission("m-r", self.staff, "m")
        self.ledger.respond_mission("m-a", self.staff, "m", "accepted", "synthetic://scope")
        receipt = self.ledger.return_mission("m-ret", self.staff, "m", "q30", evidence(),
                                             self.certificate(registration_valid_until="2027-01-01"))
        cid = receipt["result"]["candidate"]["candidate_hash"]
        self.ledger.intake_source("rev", self.builder, source("quote-src", "2", "d", "2026-10-31T13:00:00Z"))
        with self.assertRaises(Blocked):
            self.approve(cid)
        envelope = self.ledger.db.execute("SELECT envelope FROM events WHERE event_id='m-ret'").fetchone()[0]
        self.assertIn('"checks"', envelope)

    def test_return_without_checks_keeps_original_event_payload_shape(self):
        returned(self.ledger)
        envelope = self.ledger.db.execute("SELECT envelope FROM events WHERE event_id='m1-return'").fetchone()[0]
        import json
        self.assertEqual({"mission_id", "quote_id", "evidence"}, set(json.loads(envelope)["payload"]))


class CatalogToLedgerIntegration(unittest.TestCase):
    """Real catalog fixture -> read-only bridge -> separate ledger DB (never one shared DB)."""
    setUp_catalog = catalog_tests.CatalogLifecycleBehavior.setUp
    query = catalog_tests.CatalogLifecycleBehavior.query
    shared_lines = catalog_tests.CatalogLifecycleBehavior.shared_lines

    def setUp(self):
        self.setUp_catalog()
        self.ledger = Ledger(self.root / "ledger.sqlite", NODES, lambda: FIXED_NOW)
        self.builder = actor("builder")

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def test_catalog_lifecycle_flows_into_ledger_as_single_case_authority(self):
        first = read_case_snapshot(self.db, "SETTHA2027")
        self.ledger.adopt_case_snapshot("bind", self.builder, first, None)
        state = self.ledger.case_status("SETTHA2027")
        self.assertEqual(("active", "catalog_snapshot", "2026-11-26", None),
                         (state["status"], state["authority"], state["planning_date"], state["deadline"]))
        catalog_transition(self.db, "close", "SETTHA2027", "close", "synthetic://close")
        closed = read_case_snapshot(self.db, "SETTHA2027")
        self.ledger.adopt_case_snapshot("close", self.builder, closed, first["snapshot_sha256"])
        self.assertEqual("closed", self.ledger.case_status("SETTHA2027")["status"])
        with self.assertRaises(Blocked):
            self.ledger.transition_case("ledger-reopen", self.builder, "SETTHA2027", "reopen", "bypass")
        catalog_transition(self.db, "reopen", "SETTHA2027", "reopen", "synthetic://reopen")
        reopened = read_case_snapshot(self.db, "SETTHA2027")
        receipt = self.ledger.adopt_case_snapshot("reopen", self.builder, reopened, closed["snapshot_sha256"])
        self.assertTrue(receipt["result"]["case_reopened"])
        self.assertEqual(1, self.ledger._case_epoch("SETTHA2027"))
        with self.assertRaises(Conflict):
            self.ledger.adopt_case_snapshot("rollback", self.builder, closed, reopened["snapshot_sha256"])
        self.assertTrue(self.db.is_file())
        self.assertFalse((self.root / "ledger.sqlite").samefile(self.db))

    def test_only_explicitly_resolved_lines_bridge_and_spec_stays_separate(self):
        lines = dict((case, line) for line, case in self.shared_lines())
        self.assertEqual("HOLD", bridge_variant(self.db, lines["SETTHA2027"])["status"])
        resolve_line(self.db, "r30", lines["SETTHA2027"], "variant-30", self.identity,
                     "synthetic://review/30", "fictional-independent-owner")
        resolve_line(self.db, "r40", lines["MAHOSOT2027"], "variant-40",
                     {**self.identity, "specification": "fictional40mm"},
                     "synthetic://review/40", "fictional-independent-owner")
        for event, case in (("b30", "SETTHA2027"), ("b40", "MAHOSOT2027")):
            self.ledger.intake_bridged_variant(event, self.builder, bridge_variant(self.db, lines[case]))
        v30, v40 = self.ledger._get("variant", "variant-30"), self.ledger._get("variant", "variant-40")
        self.assertEqual(v30["item_code"], v40["item_code"])
        self.assertNotEqual(v30["identity_hash"], v40["identity_hash"])
        provenance = self.ledger._get("variant_provenance", lines["SETTHA2027"])
        self.assertEqual("synthetic://review/30", provenance["resolution_evidence_ref"])


if __name__ == "__main__":
    unittest.main()
