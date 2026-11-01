import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from src.four_bv_intake import import_four, common_counts, backfill_verified_manifest_pin
from src.catalog_intake import IntakeConflict


def row(code="X-1", index="0", group="vt", **changes):
    return {"": index, "group": group, "Mã DM chung": code, "Nhóm": "source group",
            "Tên tiếng Anh": "Same source name", "Tên tiếng Lào": "ຕົວຢ່າງ", "Đơn vị": "EA",
            "SL Mittaphab": "999", "SL Settha": "10", "SL SVNK": "", "SL Me and Dek": "",
            "SL Mahosot": "20", "Tổng SL": "1029", "Việc cần làm": "Tìm nguồn", **changes}


class FourBvIntakeBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="four-intake-", dir=Path(__file__).resolve().parent)
        self.root = Path(self.temp.name)
        self.db = self.root / "common.sqlite"

    def tearDown(self):
        self.temp.cleanup()

    def files(self, rows):
        path = self.root / "source.json"
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        data = path.read_bytes()
        sources = []
        for group in sorted({r["group"] for r in rows}):
            sources.append({"group": group, "drive_file_id": "fictional-" + group, "url": "https://example.invalid/" + group,
                            "extracted_content_sha256": hashlib.sha256(group.encode()).hexdigest(),
                            "revision_last_observed_20261031_0949UTC": "observed-revision-not-raw-binary-proof",
                            "content_fresh_read_UTC": "fixture observation", "raw_xlsx_sha256": None,
                            "selected_rows": sum(r["group"] == group for r in rows)})
        manifest = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "row_count": len(rows),
                    "sources": sources, "case_deadlines_planning_only": {"Settha": "2026-11-26", "Mahosot": "2026-11-25", "Me and Dek": "2026-11-27", "SVNK": None}}
        mp = self.root / "manifest.json"
        mp.write_text(json.dumps(manifest), encoding="utf-8")
        return path, mp

    def query(self, sql):
        db = sqlite3.connect(self.db)
        try:
            return db.execute(sql).fetchall()
        finally:
            db.close()

    def test_records_and_case_consumers_have_different_grains_and_ignore_mtp_total(self):
        source, manifest = self.files([row(), row("X-2", "1", **{"SL Settha": "0", "SL Mahosot": "", "SL SVNK": "5"})])
        receipt = import_four(source, manifest, self.db)
        self.assertEqual(2, receipt["source_records_imported"])
        self.assertEqual(3, receipt["four_case_demand_links"])
        self.assertEqual(2, self.query("SELECT count(*) FROM common_source_record")[0][0])
        self.assertEqual(3, self.query("SELECT count(*) FROM case_line")[0][0])
        self.assertEqual(0, self.query("SELECT count(*) FROM tender_case WHERE case_id LIKE '%MTP%'")[0][0])
        self.assertEqual([("0", "999")], self.query("SELECT json_extract(raw_fields,'$.\"SL Settha\"'),json_extract(raw_fields,'$.\"SL Mittaphab\"') FROM common_source_record WHERE master_code='X-2'"))

    def test_exact_retry_does_not_duplicate_sources_demand_or_events(self):
        source, manifest = self.files([row()])
        first = import_four(source, manifest, self.db)
        before = self.query("SELECT (SELECT count(*) FROM common_source_record),(SELECT count(*) FROM case_line),(SELECT count(*) FROM events)")
        self.assertEqual(first, import_four(source, manifest, self.db))
        self.assertEqual(before, self.query("SELECT (SELECT count(*) FROM common_source_record),(SELECT count(*) FROM case_line),(SELECT count(*) FROM events)"))

    def test_parser_index_never_claims_physical_sheet_row_or_binary_hash(self):
        source, manifest = self.files([row()])
        import_four(source, manifest, self.db)
        self.assertEqual([("extraction_parser_index", None, None, "0")] * 2,
                         self.query("SELECT row_kind,physical_sheet,physical_excel_row,parser_index FROM line_source_record"))
        self.assertIsNone(self.query("SELECT raw_xlsx_sha256 FROM external_source_provenance")[0][0])
        self.assertIn("parser-index:0", self.query("SELECT source_anchor FROM case_line LIMIT 1")[0][0])

    def test_status_and_unknown_locale_quantity_do_not_become_price_ready_or_zero(self):
        source, manifest = self.files([row(**{"Việc cần làm": "Đã có giá", "SL Settha": "1,000", "SL Mahosot": ""})])
        import_four(source, manifest, self.db)
        self.assertEqual([("price_validity_review",)], self.query("SELECT need_type FROM demand_link"))
        self.assertEqual([(None, "quantity_locale_or_format_unknown")], self.query("SELECT quantity_normalized,quantity_flag FROM line_source_record"))
        self.assertEqual(0, self.query("SELECT count(*) FROM normalized_variant")[0][0])
        self.assertEqual(0, self.query("SELECT count(*) FROM source_quote_version WHERE current_quote_accepted<>0")[0][0])

    def test_same_parser_index_and_code_from_different_source_groups_do_not_collide(self):
        source, manifest = self.files([row(group="vt"), row(group="thuoc")])
        receipt = import_four(source, manifest, self.db)
        self.assertEqual(2, receipt["source_records_imported"])
        self.assertEqual(4, receipt["four_case_demand_links"])

    def test_name_uom_collisions_are_quarantined_not_merged(self):
        source, manifest = self.files([row(), row("X-2", "1")])
        import_four(source, manifest, self.db)
        self.assertEqual(1, self.query("SELECT count(*) FROM common_collision_group")[0][0])
        self.assertEqual(2, self.query("SELECT count(*) FROM common_collision_member")[0][0])
        self.assertEqual(0, self.query("SELECT count(*) FROM normalized_variant")[0][0])

    def test_manifest_mismatch_and_mtp_only_are_rejected_before_database_creation(self):
        source, manifest = self.files([row()])
        source.write_text("[]", encoding="utf-8")
        with self.assertRaises(IntakeConflict):
            import_four(source, manifest, self.db)
        self.assertFalse(self.db.exists())
        source, manifest = self.files([row(**{"SL Settha": "0", "SL Mahosot": ""})])
        with self.assertRaises(ValueError):
            import_four(source, manifest, self.db)
        self.assertFalse(self.db.exists())

    def test_same_json_changed_provenance_or_mapping_rules_is_not_an_exact_retry(self):
        source, manifest = self.files([row()])
        first = import_four(source, manifest, self.db)
        original = json.loads(manifest.read_text(encoding="utf-8"))
        changed = json.loads(json.dumps(original))
        changed["sources"][0]["drive_file_id"] = "different-origin"
        manifest.write_text(json.dumps(changed),encoding="utf-8")
        before = self.query("SELECT count(*) FROM events")
        with self.assertRaises(IntakeConflict):
            import_four(source,manifest,self.db)
        self.assertEqual(before,self.query("SELECT count(*) FROM events"))
        changed=original
        changed["mapping_rules"]="different semantic selection"
        manifest.write_text(json.dumps(changed),encoding="utf-8")
        with self.assertRaises(IntakeConflict):
            import_four(source,manifest,self.db)
        self.assertIn("manifest_semantic_sha256",first)

    def test_legacy_manifest_pin_requires_verified_explicit_additive_backfill(self):
        source,manifest=self.files([row()])
        first=import_four(source,manifest,self.db)
        db=sqlite3.connect(self.db)
        db.execute("DELETE FROM four_intake_manifest_pin")
        db.commit();db.close()
        with self.assertRaises(IntakeConflict):
            import_four(source,manifest,self.db)
        correction=backfill_verified_manifest_pin(source,manifest,self.db)
        self.assertEqual(0,correction["business_rows_changed"])
        self.assertEqual(first,import_four(source,manifest,self.db))
