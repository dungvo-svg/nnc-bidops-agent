import hashlib
import inspect
import re
import unittest

import tests.test_catalog_lifecycle as base
from src import catalog_bridge
from src.catalog_bridge import bridge_variant, read_case_snapshot
from src.catalog_lifecycle import extend_deadline, resolve_line, transition_case


class CatalogBridgeBehavior(unittest.TestCase):
    # Reuse the lifecycle fixture by function, not by class, so discovery does not rerun its tests.
    setUp = base.CatalogLifecycleBehavior.setUp
    tearDown = base.CatalogLifecycleBehavior.tearDown
    query = base.CatalogLifecycleBehavior.query
    shared_lines = base.CatalogLifecycleBehavior.shared_lines

    def sha(self):
        return hashlib.sha256(self.db.read_bytes()).hexdigest()

    def test_snapshot_shape_and_stable_hash(self):
        first = read_case_snapshot(self.db, "SETTHA2027")
        second = read_case_snapshot(self.db, "SETTHA2027")
        self.assertEqual(first, second)
        self.assertEqual("bidops-case-snapshot/1", first["schema"])
        self.assertEqual("SETTHA2027", first["case_id"])
        self.assertEqual("active", first["status"])
        self.assertEqual("2026-11-26", first["planning_date"])
        self.assertIsNone(first["official_closing_at"])
        self.assertEqual([], first["lifecycle_events"])
        for key in ("source_status", "active_source_version", "closure_policy"):
            self.assertIn(key, first)
        self.assertRegex(first["snapshot_sha256"], r"^[0-9a-f]{64}$")
        from src.ledger import digest
        body = {k: v for k, v in first.items() if k != "snapshot_sha256"}
        self.assertEqual(digest(body), first["snapshot_sha256"])

    def test_hash_changes_after_close_reopen_and_extend(self):
        seen = [read_case_snapshot(self.db, "SETTHA2027")["snapshot_sha256"]]
        transition_case(self.db, "close", "SETTHA2027", "close", "synthetic://close")
        closed = read_case_snapshot(self.db, "SETTHA2027")
        self.assertEqual("closed", closed["status"])
        self.assertEqual(["close"], [e["event_id"] for e in closed["lifecycle_events"]])
        self.assertEqual("common_case_transition", closed["lifecycle_events"][0]["kind"])
        seen.append(closed["snapshot_sha256"])
        transition_case(self.db, "reopen", "SETTHA2027", "reopen", "synthetic://reopen")
        reopened = read_case_snapshot(self.db, "SETTHA2027")
        self.assertEqual("active", reopened["status"])
        seen.append(reopened["snapshot_sha256"])
        extend_deadline(self.db, "extend", "SETTHA2027", "2026-12-10", "synthetic://extension")
        extended = read_case_snapshot(self.db, "SETTHA2027")
        self.assertEqual("2026-12-10", extended["planning_date"])
        self.assertIsNone(extended["official_closing_at"])
        self.assertEqual(["close", "reopen", "extend"], [e["event_id"] for e in extended["lifecycle_events"]])
        seen.append(extended["snapshot_sha256"])
        self.assertEqual(4, len(set(seen)))
        # Same-status-and-date states reached via different history are still different snapshots.
        self.assertNotEqual(seen[0], seen[2])

    def test_other_case_events_do_not_leak_into_snapshot(self):
        transition_case(self.db, "close-mahosot", "MAHOSOT2027", "close", "synthetic://close")
        settha = read_case_snapshot(self.db, "SETTHA2027")
        self.assertEqual([], settha["lifecycle_events"])
        self.assertEqual("active", settha["status"])

    def test_planning_date_is_never_turned_into_closing_time(self):
        snapshot = read_case_snapshot(self.db, "SETTHA2027")
        self.assertIsNotNone(snapshot["planning_date"])
        self.assertIsNone(snapshot["official_closing_at"])

    def test_unknown_case_raises(self):
        with self.assertRaises(ValueError):
            read_case_snapshot(self.db, "NO-SUCH-CASE")

    def test_reads_do_not_change_catalog_bytes(self):
        before = self.sha()
        read_case_snapshot(self.db, "SETTHA2027")
        line = self.shared_lines()[0][0]
        bridge_variant(self.db, line)
        resolve_line(self.db, "r1", line, "v-30", self.identity, "synthetic://review/1", "fictional-owner")
        after_resolve = self.sha()
        bridge_variant(self.db, line)
        read_case_snapshot(self.db, "SETTHA2027")
        self.assertEqual(after_resolve, self.sha())
        self.assertNotEqual(before, after_resolve)

    def test_unresolved_line_holds_without_name_or_mpsc_match(self):
        line, case = self.shared_lines()[0]
        result = bridge_variant(self.db, line)
        self.assertEqual({"status": "HOLD", "line_id": line, "case_id": case,
                          "reason": "line_unresolved", "variant": None, "provenance": None}, result)

    def test_resolving_one_line_does_not_bridge_same_mpsc_sibling(self):
        (line_a, _), (line_b, _) = self.shared_lines()
        resolve_line(self.db, "r1", line_a, "v-30", self.identity, "synthetic://review/1", "fictional-owner")
        self.assertEqual("BRIDGED", bridge_variant(self.db, line_a)["status"])
        self.assertEqual("HOLD", bridge_variant(self.db, line_b)["status"])

    def test_unknown_line_raises(self):
        with self.assertRaises(ValueError):
            bridge_variant(self.db, "line:does-not-exist")

    def test_bridged_variant_matches_ledger_shape_and_provenance(self):
        line, case = self.shared_lines()[0]
        resolve_line(self.db, "r1", line, "v-30", self.identity, "synthetic://review/1", "fictional-owner")
        result = bridge_variant(self.db, line)
        self.assertEqual("BRIDGED", result["status"])
        self.assertEqual((line, case), (result["line_id"], result["case_id"]))
        self.assertEqual({"variant_id": "v-30", "item_code": "SYNTHETIC-CODE",
                          "specification": {"catalog_specification": "fictional30mm"}, "unit": "EA",
                          "registration_id": None, "identity_valid_from": None,
                          "identity_valid_until": None}, result["variant"])
        stored_sha = self.query("SELECT identity_sha256 FROM normalized_variant WHERE variant_id='v-30'")[0][0]
        p = result["provenance"]
        self.assertEqual("explicit_reviewed_line_resolution", p["mapping"])
        self.assertEqual("v-30", p["catalog_variant_id"])
        self.assertEqual(stored_sha, p["catalog_identity_sha256"])
        self.assertEqual("synthetic://review/1", p["resolution_evidence_ref"])
        self.assertEqual("fictional-owner", p["reviewed_by"])
        self.assertEqual((line, case), (p["line_id"], p["case_id"]))
        for key in ("source_version", "source_anchor", "name_raw", "uom_raw"):
            self.assertIn(key, p)
        self.assertTrue(p["source_anchor"])
        self.assertEqual("EA", p["uom_raw"])
        self.assertEqual([], result["flags"])

    def test_same_mpsc_different_specification_stay_two_variants(self):
        (line_a, _), (line_b, _) = self.shared_lines()
        resolve_line(self.db, "r1", line_a, "v-30", self.identity, "synthetic://review/30", "fictional-owner")
        resolve_line(self.db, "r2", line_b, "v-40", {**self.identity, "specification": "fictional40mm"},
                     "synthetic://review/40", "fictional-owner")
        a, b = bridge_variant(self.db, line_a), bridge_variant(self.db, line_b)
        self.assertEqual("BRIDGED", a["status"]);self.assertEqual("BRIDGED", b["status"])
        self.assertEqual(a["variant"]["item_code"], b["variant"]["item_code"])
        self.assertNotEqual(a["variant"]["variant_id"], b["variant"]["variant_id"])
        self.assertEqual({"catalog_specification": "fictional30mm"}, a["variant"]["specification"])
        self.assertEqual({"catalog_specification": "fictional40mm"}, b["variant"]["specification"])
        self.assertNotEqual(a["provenance"]["catalog_identity_sha256"], b["provenance"]["catalog_identity_sha256"])
        self.assertNotEqual(a["provenance"]["resolution_evidence_ref"], b["provenance"]["resolution_evidence_ref"])

    def test_two_lines_resolved_to_same_variant_share_variant_id_but_keep_own_provenance(self):
        for line, case in self.shared_lines():
            resolve_line(self.db, "r-" + case, line, "v-30", self.identity, "synthetic://review/" + case, "fictional-owner")
        results = [bridge_variant(self.db, line) for line, _ in self.shared_lines()]
        self.assertEqual({"v-30"}, {r["variant"]["variant_id"] for r in results})
        self.assertEqual(2, len({r["provenance"]["line_id"] for r in results}))
        self.assertEqual(2, len({r["provenance"]["resolution_evidence_ref"] for r in results}))

    def test_uom_mismatch_is_flagged_not_converted(self):
        line, _ = self.shared_lines()[0]
        resolve_line(self.db, "r1", line, "v-box", {**self.identity, "uom": "BOX"}, "synthetic://review/box", "fictional-owner")
        result = bridge_variant(self.db, line)
        self.assertEqual("BOX", result["variant"]["unit"])
        self.assertEqual("EA", result["provenance"]["uom_raw"])
        self.assertIn("unit_conversion_not_attested", result["flags"])

    def test_registration_and_validity_pass_through_from_identity(self):
        line, _ = self.shared_lines()[0]
        identity = {**self.identity, "registration_id": "FICT-REG-1", "valid_from": "2026-01-01", "valid_until": "2027-01-01"}
        resolve_line(self.db, "r1", line, "v-reg", identity, "synthetic://review/reg", "fictional-owner")
        variant = bridge_variant(self.db, line)["variant"]
        self.assertEqual("FICT-REG-1", variant["registration_id"])
        self.assertEqual("2026-01-01", variant["identity_valid_from"])
        self.assertEqual("2027-01-01", variant["identity_valid_until"])

    def test_module_contains_no_write_statements(self):
        source = inspect.getsource(catalog_bridge)
        self.assertIsNone(re.search(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|REPLACE)\s+(INTO|OR|FROM|TABLE|\w+\s+SET)",
                                    source, re.I))
        for needle in ("executescript", "commit(", "BEGIN", "isolation_level", "initialize_lifecycle", "PRAGMA"):
            self.assertNotIn(needle, source)
        self.assertIn("mode=ro", source)
        own = [n for n, f in inspect.getmembers(catalog_bridge, inspect.isfunction)
               if not n.startswith("_") and f.__module__ == catalog_bridge.__name__]
        self.assertEqual(["bridge_variant", "read_case_snapshot"], sorted(own))


if __name__ == "__main__":
    unittest.main()
