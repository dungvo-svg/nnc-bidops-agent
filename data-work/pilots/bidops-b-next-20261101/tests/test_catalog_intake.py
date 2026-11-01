import csv
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from src.catalog_intake import REQUIRED, IntakeConflict, import_csv, query_counts, record_candidate_edges


def fictional_row(row=18, **changes):
    data = {field: "" for field in REQUIRED}
    data.update({"case_id": "FICTIONAL2027", "case_status": "current_2027_package",
                 "deadline_observed": "2026-11-13", "source_file_name": "fictional-source.xlsx",
                 "source_file_sha256": "a" * 64, "requirement_sheet": "List fictional ",
                 "requirement_row": str(row), "requirement_anchor": f"'List fictional '!A{row}:D{row}",
                 "requirement_name_raw": "Fictional same name", "requirement_uom_raw": "EA",
                 "quantity_status": "unknown_in_source", "intake_state": "sourcing_required",
                 "historical_price_basis": "historical_only", "historical_price_available": "False",
                 "destination_missing": "False", "identity_complete": "False",
                 "identity_missing_components": "mpsc|explicit_spec|validity",
                 "unresolved_identity_key": f"fictional:row:{row}",
                 "normalized_variant_descriptor": json.dumps({"name": "same", "mpsc": None}),
                 "candidate_group_key": f"candidate-only:{row}", "candidate_group_size": "1"})
    return {**data, **changes}


class CatalogIntakeBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="catalog-test-", dir=Path(__file__).resolve().parent)
        self.root = Path(self.temp.name)
        self.db = self.root / "catalog.sqlite"

    def tearDown(self):
        self.temp.cleanup()

    def csv(self, rows, name="source.csv"):
        path = self.root / name
        fields = sorted(set().union(*(row.keys() for row in rows)))
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def counts(self):
        db = sqlite3.connect(self.db)
        try:
            return query_counts(db)
        finally:
            db.close()

    def test_all_rows_retained_unknown_quantity_uom_and_same_name_not_merged(self):
        path = self.csv([fictional_row(18), fictional_row(19, requirement_uom_raw="")])
        receipt = import_csv(path, self.db, expected_rows=2)
        counts = self.counts()
        self.assertEqual(2, counts["case_line"])
        self.assertEqual(2, counts["unresolved_variant"])
        self.assertEqual(0, counts["normalized_variant"])
        self.assertEqual(2, counts["active_workitems"])
        self.assertEqual(2, counts["unknown_quantity"])
        self.assertEqual(1, counts["missing_requirement_uom"])
        self.assertEqual(2, counts["candidate_matching"])
        self.assertFalse(receipt["current_price_or_bid_approval"])

    def test_exact_batch_retry_is_same_receipt_and_no_new_rows_or_events(self):
        path = self.csv([fictional_row()])
        first = import_csv(path, self.db)
        before = self.counts()
        second = import_csv(path, self.db)
        self.assertEqual(first, second)
        self.assertEqual(before, self.counts())
        self.assertEqual(1, before["events"])

    def test_conflicting_row_version_rolls_back_whole_batch(self):
        original = fictional_row()
        import_csv(self.csv([original]), self.db)
        before = self.counts()
        changed = self.csv([fictional_row(19), {**original, "requirement_name_raw": "changed same row/version"}], "changed.csv")
        with self.assertRaises(IntakeConflict):
            import_csv(changed, self.db)
        self.assertEqual(before, self.counts())

    def test_candidate_group_stays_pending_and_prices_are_historical_only(self):
        common = {"candidate_group_key": "unapproved-same-label", "candidate_group_size": "2"}
        path = self.csv([fictional_row(18, **common, intake_state="historical_price_revalidation", historical_price_available="True"),
                         fictional_row(19, **common, intake_state="equivalence_review_required")])
        import_csv(path, self.db)
        counts = self.counts()
        self.assertEqual(1, counts["candidate_match_group"])
        self.assertEqual(2, counts["candidate_group_rows"])
        self.assertEqual(1, counts["source_quote_version"])
        self.assertEqual(0, counts["accepted_current_quotes"])
        self.assertEqual({"equivalence_review": 1, "historical_price_revalidation": 1}, counts["active_needs"])

    def test_unknown_official_hour_and_late_import_do_not_reopen_case(self):
        path = self.csv([fictional_row()])
        import_csv(path, self.db)
        db = sqlite3.connect(self.db)
        try:
            deadline, closing = db.execute("SELECT deadline_observed,official_closing_time FROM tender_case").fetchone()
            self.assertEqual("2026-11-13", deadline)
            self.assertIsNone(closing)
            db.execute("UPDATE tender_case SET status='closed'")
            db.commit()
        finally:
            db.close()
        import_csv(path, self.db)
        self.assertEqual(0, self.counts()["active_workitems"])
        self.assertEqual(1, self.counts()["case_line"])

    def test_duplicate_source_row_and_false_group_coverage_are_rejected(self):
        row = fictional_row()
        with self.assertRaises(IntakeConflict):
            import_csv(self.csv([row, row]), self.db)
        with self.assertRaises(IntakeConflict):
            import_csv(self.csv([fictional_row(18, candidate_group_key="g", candidate_group_size="1"),
                                 fictional_row(19, candidate_group_key="g", candidate_group_size="1")]), self.db)
        self.assertFalse(self.db.exists())

    def test_cross_batch_group_overflow_rejects_entire_second_transaction(self):
        group = {"candidate_group_key": "g", "candidate_group_size": "2"}
        first = self.csv([fictional_row(18, **group), fictional_row(19, **group)], "first.csv")
        import_csv(first, self.db)
        before = self.counts()
        second = self.csv([fictional_row(20, **group), fictional_row(21, **group)], "second.csv")
        with self.assertRaises(IntakeConflict):
            import_csv(second, self.db)
        self.assertEqual(before, self.counts())
        db = sqlite3.connect(self.db)
        try:
            self.assertEqual([(2, 2)], db.execute(
                "SELECT g.declared_size,count(m.line_id) FROM candidate_match_group g "
                "JOIN candidate_group_membership m ON m.case_id=g.case_id AND m.source_version=g.source_version "
                "AND m.group_key=g.group_key GROUP BY g.group_key").fetchall())
        finally:
            db.close()

    def test_existing_group_cannot_silently_change_its_declared_size(self):
        initial = {"candidate_group_key": "g", "candidate_group_size": "2"}
        import_csv(self.csv([fictional_row(18, **initial), fictional_row(19, **initial)], "first.csv"), self.db)
        before = self.counts()
        changed = {"candidate_group_key": "g", "candidate_group_size": "3"}
        with self.assertRaises(IntakeConflict):
            import_csv(self.csv([fictional_row(i, **changed) for i in (20, 21, 22)], "changed.csv"), self.db)
        self.assertEqual(before, self.counts())

    def test_partial_group_keeps_pending_coverage_then_fills_without_duplicate_rows(self):
        group = {"candidate_group_key": "g", "candidate_group_size": "2"}
        first_path = self.csv([fictional_row(18, **group)], "partial.csv")
        first = import_csv(first_path, self.db)
        self.assertEqual("coverage_pending", first["candidate_group_coverage"][0]["coverage_state"])
        self.assertEqual(1, first["candidate_group_coverage"][0]["observed_members"])
        self.assertFalse(first["candidate_group_coverage"][0]["identity_accepted"])
        second_path = self.csv([fictional_row(19, **group)], "remainder.csv")
        second = import_csv(second_path, self.db)
        self.assertEqual("membership_complete_pending_review", second["candidate_group_coverage"][0]["coverage_state"])
        self.assertEqual(2, second["candidate_group_coverage"][0]["observed_members"])
        self.assertEqual(0, self.counts()["normalized_variant"])
        before = self.counts()
        self.assertEqual(second, import_csv(second_path, self.db))
        self.assertEqual(before, self.counts())

    def test_singleton_group_declaration_cannot_be_reused_as_a_larger_group(self):
        import_csv(self.csv([fictional_row(18, candidate_group_key="g")], "singleton.csv"), self.db)
        before = self.counts()
        group = {"candidate_group_key": "g", "candidate_group_size": "2"}
        with self.assertRaises(IntakeConflict):
            import_csv(self.csv([fictional_row(19, **group), fictional_row(20, **group)], "larger.csv"), self.db)
        self.assertEqual(before, self.counts())

    def test_exact_legacy_retry_does_not_migrate_or_change_database_bytes(self):
        path = self.csv([fictional_row()])
        first = import_csv(path, self.db)
        db = sqlite3.connect(self.db)
        db.execute("DROP TABLE candidate_group_membership")
        db.commit()
        db.close()
        before = hashlib.sha256(self.db.read_bytes()).hexdigest()
        self.assertEqual(first, import_csv(path, self.db))
        self.assertEqual(before, hashlib.sha256(self.db.read_bytes()).hexdigest())
        db = sqlite3.connect(self.db)
        try:
            self.assertEqual([], db.execute("SELECT name FROM sqlite_master WHERE name='candidate_group_membership'").fetchall())
        finally:
            db.close()

    def test_legacy_new_batch_requires_unchanged_prior_rows_for_validated_metadata_backfill(self):
        original = fictional_row()
        import_csv(self.csv([original], "first.csv"), self.db)
        db = sqlite3.connect(self.db)
        db.execute("DROP TABLE candidate_group_membership")
        db.commit()
        db.close()
        before = self.counts()
        with self.assertRaises(IntakeConflict):
            import_csv(self.csv([fictional_row(19)], "partial-new.csv"), self.db)
        self.assertEqual(before, self.counts())
        receipt = import_csv(self.csv([original, fictional_row(19)], "full-new.csv"), self.db)
        self.assertEqual(1, receipt["inserted_rows"])
        self.assertEqual(1, receipt["unchanged_existing_rows"])
        self.assertEqual(2, self.counts()["case_line"])

    def test_candidate_inquiry_never_creates_resolved_or_accepted_link(self):
        import_csv(self.csv([fictional_row()]), self.db)
        edge = {"edge_id": "synthetic-inquiry", "case_id": "FICTIONAL2027", "source_row": 18,
                "source_workbook_sha256": "a" * 64, "target_ref": "fictional-common-item",
                "target_source_anchor": "unverified://source/row1", "target_source_sha256": None,
                "evidence_state": "parent_reported_source_pin_pending", "relation": "candidate_only",
                "reason": "needs human and source checks", "accepted": False}
        first = record_candidate_edges(self.db, [edge])
        self.assertEqual(first, record_candidate_edges(self.db, [edge]))
        self.assertEqual(1, self.counts()["catalog_candidate_edge"])
        self.assertEqual(0, self.counts()["normalized_variant"])
        self.assertEqual(0, first["accepted_merge"])
        with self.assertRaises(ValueError):
            record_candidate_edges(self.db, [{**edge, "accepted": True}])
        self.assertEqual(1, self.counts()["catalog_candidate_edge"])

    def test_wrong_database_is_not_contaminated(self):
        db = sqlite3.connect(self.db)
        db.execute("CREATE TABLE user_work(value TEXT)")
        db.execute("INSERT INTO user_work VALUES('preserve')")
        db.commit()
        db.close()
        with self.assertRaises(IntakeConflict):
            import_csv(self.csv([fictional_row()]), self.db)
        db = sqlite3.connect(self.db)
        try:
            self.assertEqual([("user_work",)], db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
            self.assertEqual("preserve", db.execute("SELECT value FROM user_work").fetchone()[0])
        finally:
            db.close()
