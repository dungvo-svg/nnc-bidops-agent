"""Append a pinned four-hospital handoff to a LOCAL catalog; no live source calls.

One master record may have several case consumers. Neither a master code nor an
exact name/UOM collision establishes a resolved product variant or valid quote.
"""
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from decimal import Decimal
import unicodedata
from datetime import datetime, timezone

from .catalog_intake import IntakeConflict, _schema, _json, _hash

CASES = {"SL Settha": ("SETTHA2027", "Settha"), "SL SVNK": ("SVNK2027", "SVNK"),
         "SL Me and Dek": ("MEDEK2027", "Me and Dek"), "SL Mahosot": ("MAHOSOT2027", "Mahosot")}
STAGES = {"Tìm nguồn": "sourcing", "Xem lại hàng": "equivalence_review", "Tính giá": "cost_calculation",
          "Đã có giá": "price_validity_review", "Đã có báo giá – chốt NCC": "quote_supplier_review"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS common_source_record(
 record_id TEXT PRIMARY KEY, cohort TEXT NOT NULL, source_version TEXT NOT NULL,
 source_group TEXT NOT NULL, master_code TEXT, parser_index TEXT,
 source_anchor TEXT NOT NULL, raw_fields TEXT NOT NULL, payload_sha256 TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS line_source_record(
 line_id TEXT PRIMARY KEY REFERENCES case_line(line_id), record_id TEXT NOT NULL REFERENCES common_source_record(record_id),
 row_kind TEXT NOT NULL, physical_sheet TEXT, physical_excel_row INTEGER,
 parser_index TEXT, quantity_normalized TEXT, quantity_flag TEXT);
CREATE TABLE IF NOT EXISTS external_source_provenance(
 source_group TEXT PRIMARY KEY, drive_file_id TEXT NOT NULL, extracted_content_sha256 TEXT NOT NULL,
 revision_last_observed TEXT, revision_observed_at TEXT, content_read_at TEXT,
 raw_xlsx_sha256 TEXT, metadata TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS common_collision_group(
 collision_id TEXT PRIMARY KEY, source_group TEXT NOT NULL, name_key TEXT NOT NULL,
 uom_key TEXT NOT NULL, source_record_count INTEGER NOT NULL, accepted INTEGER NOT NULL CHECK(accepted=0));
CREATE TABLE IF NOT EXISTS common_collision_member(
 collision_id TEXT REFERENCES common_collision_group(collision_id), record_id TEXT REFERENCES common_source_record(record_id),
 PRIMARY KEY(collision_id,record_id));
CREATE TABLE IF NOT EXISTS four_intake_manifest_pin(
 source_json_sha256 TEXT PRIMARY KEY, manifest_semantic_sha256 TEXT NOT NULL,
 manifest_json TEXT NOT NULL, provenance_event_id TEXT NOT NULL);
"""


def normalized_quantity(raw):
    """Only plainly positive integers/short decimals; do not guess locale grouping."""
    value = raw.strip()
    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", value):
        return None, "quantity_locale_or_format_unknown"
    number = Decimal(value)
    if number <= 0:
        return None, "selected_raw_quantity_not_positive"
    return str(number.normalize()) if "." in value else str(number), None


def _name_key(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _immutable(db, table, key_col, key, value_cols, values):
    old = db.execute(f"SELECT {','.join(value_cols)} FROM {table} WHERE {key_col}=?", (key,)).fetchone()
    if old:
        if tuple(old) != tuple(values):
            raise IntakeConflict(f"immutable {table} identity content conflict")
        return False
    db.execute(f"INSERT INTO {table}({key_col},{','.join(value_cols)}) VALUES({','.join('?' for _ in range(len(values)+1))})",
               (key, *values))
    return True


def _seed_kom_records(db):
    """Index existing Kom physical rows, without copying or fabricating new demand."""
    db.row_factory = sqlite3.Row
    for row in db.execute("SELECT * FROM case_line WHERE case_id='KOM2027'").fetchall():
        line = dict(row)
        record_id = "source-record:kom:" + line["line_id"].split(":", 1)[1]
        fields = _json(line)
        _immutable(db, "common_source_record", "record_id", record_id,
                   ["cohort", "source_version", "source_group", "master_code", "parser_index", "source_anchor", "raw_fields", "payload_sha256"],
                   ["Kom", line["source_version"], "Kom", line["item_code_raw"], None, line["source_anchor"], fields, _hash(line)])
        db.execute("INSERT OR IGNORE INTO line_source_record VALUES(?,?,?,?,?,?,?,?)",
                   (line["line_id"], record_id, "physical_workbook_row", line["source_sheet"], line["source_row"],
                    None, None, "quantity_unknown_in_source" if line["quantity_raw"] is None else None))
    db.row_factory = None


def common_counts(db):
    return {
        "source_records": db.execute("SELECT count(*) FROM common_source_record").fetchone()[0],
        "source_records_by_cohort": dict(db.execute("SELECT cohort,count(*) FROM common_source_record GROUP BY cohort")),
        "case_lines": db.execute("SELECT count(*) FROM case_line").fetchone()[0],
        "case_lines_by_case": dict(db.execute("SELECT case_id,count(*) FROM case_line GROUP BY case_id")),
        "demand_links": db.execute("SELECT count(*) FROM demand_link").fetchone()[0],
        "unresolved_case_line_identities": db.execute("SELECT count(*) FROM unresolved_variant").fetchone()[0],
        "resolved_variants": db.execute("SELECT count(*) FROM normalized_variant").fetchone()[0],
        "four_source_statuses": dict(db.execute("SELECT json_extract(raw_fields,'$.\"Việc cần làm\"'),count(*) FROM common_source_record WHERE cohort='four-BV' GROUP BY 1")),
        "four_collision_groups": db.execute("SELECT count(*) FROM common_collision_group").fetchone()[0],
        "physical_excel_rows_unknown": db.execute("SELECT count(*) FROM line_source_record WHERE row_kind='extraction_parser_index' AND physical_excel_row IS NULL").fetchone()[0],
        "unknown_quantities": db.execute("SELECT count(*) FROM line_source_record WHERE quantity_normalized IS NULL").fetchone()[0],
        "current_quote_accepted": db.execute("SELECT count(*) FROM source_quote_version WHERE current_quote_accepted<>0").fetchone()[0],
    }


def import_four(json_path, manifest_path, db_path):
    path, manifest_file = Path(json_path).resolve(), Path(manifest_path).resolve()
    data = path.read_bytes()
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest_digest = _hash(manifest)
    sha = hashlib.sha256(data).hexdigest()
    if sha != manifest["sha256"] or len(data) != manifest["bytes"]:
        raise IntakeConflict("four-case handoff size/hash does not match manifest")
    rows = json.loads(data)
    if len(rows) != manifest["row_count"]:
        raise IntakeConflict("manifest row count mismatch")
    sources = {s["group"]: s for s in manifest["sources"]}
    prepared, identities, by_group, collisions = [], set(), {}, {}
    for raw in rows:
        if not isinstance(raw, dict) or any(not isinstance(v, str) for v in raw.values()):
            raise ValueError("all handoff source fields must remain raw strings")
        group, code, index = raw["group"], raw["Mã DM chung"], raw[""]
        if group not in sources or not code.strip() or not re.fullmatch(r"\d+", index):
            raise ValueError("source group/master code/parser index missing")
        identity = [sources[group]["drive_file_id"], sha, group, code, index]
        identity_key = _json(identity)
        if identity_key in identities:
            raise IntakeConflict("duplicate master record identity")
        identities.add(identity_key)
        if raw["Việc cần làm"] not in STAGES:
            raise ValueError("unknown catalog stage; cannot force it to sourcing")
        demands = [(field, raw[field]) for field in CASES if raw[field].strip() and raw[field].strip() != "0"]
        if not demands:
            raise ValueError("MTP-only/no-four-case-demand record is outside this manifest cohort")
        record_id = "source-record:four:" + _hash(identity)
        anchor = f"drive:{sources[group]['drive_file_id']};readable-master-section3;parser-index:{index};extract:{sources[group]['extracted_content_sha256']}"
        collision = (group, _name_key(raw["Tên tiếng Anh"]), _name_key(raw["Đơn vị"]))
        collisions.setdefault(collision, []).append(record_id)
        prepared.append((raw, record_id, anchor, demands, collision))
        by_group[group] = by_group.get(group, 0) + 1
    if by_group != {s["group"]: s["selected_rows"] for s in manifest["sources"]}:
        raise IntakeConflict("manifest source-group coverage mismatch")
    target = Path(db_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(target, isolation_level=None)
    try:
        _schema(db)
        db.executescript(SCHEMA)
        db.execute("BEGIN IMMEDIATE")
        event_id = "four-case-intake:" + sha
        old = db.execute("SELECT receipt FROM events WHERE event_id=?", (event_id,)).fetchone()
        if old:
            pin = db.execute("SELECT manifest_semantic_sha256 FROM four_intake_manifest_pin WHERE source_json_sha256=?", (sha,)).fetchone()
            if not pin:
                raise IntakeConflict("legacy intake lacks full manifest pin; explicit verified provenance backfill required")
            if pin[0] != manifest_digest:
                raise IntakeConflict("same JSON hash with changed manifest provenance or mapping rules")
            db.execute("COMMIT")
            return json.loads(old[0])
        _seed_kom_records(db)
        db.execute("INSERT OR IGNORE INTO source_artifact VALUES(?,?,?,?,?,0)", (sha, "four_case_json", path.name, str(path), len(data)))
        for source in manifest["sources"]:
            db.execute("INSERT OR IGNORE INTO source_artifact VALUES(?,?,?,?,NULL,1)",
                       (source["extracted_content_sha256"], "drive_readable_extraction_reference", source["group"], source["url"]))
            _immutable(db, "external_source_provenance", "source_group", source["group"],
                       ["drive_file_id", "extracted_content_sha256", "revision_last_observed", "revision_observed_at", "content_read_at", "raw_xlsx_sha256", "metadata"],
                       [source["drive_file_id"], source["extracted_content_sha256"], source.get("revision_last_observed_20261031_0949UTC"),
                        "2026-10-31 09:49 UTC (minute precision; manifest observation)", source.get("content_fresh_read_UTC"), source.get("raw_xlsx_sha256"), _json(source)])
        for case_id, label in CASES.values():
            prior = db.execute("SELECT active_source_version FROM tender_case WHERE case_id=?", (case_id,)).fetchone()
            if prior and prior[0] != sha:
                raise IntakeConflict("case snapshot replacement requires reviewed promotion")
            db.execute("INSERT OR IGNORE INTO tender_case VALUES(?,?,?,?,?,?,?)",
                       (case_id, "active", "planning_only_formal_conditions_not_verified", sha,
                        manifest["case_deadlines_planning_only"].get(label), None,
                        "no auto-close; dates are planning observations; official closing hour unknown"))
        for raw, record_id, anchor, demands, collision in prepared:
            _immutable(db, "common_source_record", "record_id", record_id,
                       ["cohort", "source_version", "source_group", "master_code", "parser_index", "source_anchor", "raw_fields", "payload_sha256"],
                       ["four-BV", sha, raw["group"], raw["Mã DM chung"], raw[""], anchor, _json(raw), _hash(raw)])
            for field, qty in demands:
                case_id = CASES[field][0]
                line_id = "line:four:" + _hash([record_id, case_id])
                unresolved_id = "unresolved:four:" + _hash([record_id, case_id])
                known_qty, qty_flag = normalized_quantity(qty)
                flags = ["identity_unresolved", "parser_index_not_physical_excel_row", "catalog_status_not_acceptance"]
                if qty_flag:
                    flags.append(qty_flag)
                if not raw["Đơn vị"].strip():
                    flags.append("requirement_uom_unknown")
                if len(collisions[collision]) > 1:
                    flags.append("exact_name_uom_collision_pending")
                name = raw["Tên tiếng Anh"] or raw["Tên tiếng Lào"] or f"[source label missing; master {raw['Mã DM chung']}]"
                db.execute("INSERT INTO case_line VALUES(" + ",".join("?" for _ in range(25)) + ")",
                           (line_id, case_id, sha, "readable-master-section3/" + raw["group"], int(raw[""]), anchor,
                            None, None, raw["Nhóm"], raw["group"], raw["Mã DM chung"], None, name,
                            None, None, "standalone_verified_requirement_spec_not_provided", raw["Đơn vị"] or None,
                            None, qty, "raw_source_quantity; see provenance normalized value/flag", raw["Việc cần làm"],
                            None, 0, 1, _hash([raw, case_id, field, qty])))
                descriptor = {"source_master_code": raw["Mã DM chung"], "source_group": raw["group"],
                              "name_candidate": raw["Tên tiếng Anh"], "uom_raw": raw["Đơn vị"],
                              "standalone_spec": None, "registration_validity": None, "quote_validity": None}
                db.execute("INSERT INTO unresolved_variant VALUES(?,?,?,?,?,0)",
                           (unresolved_id, line_id, record_id + ":" + case_id, _json(descriptor), "spec|pack|registration|validity|case_equivalence_not_reviewed"))
                work_id, need = "match:four:" + _hash([record_id, case_id]), STAGES[raw["Việc cần làm"]]
                db.execute("INSERT INTO candidate_matching VALUES(?,?,?,'pending',?,NULL,?)", (work_id, line_id, unresolved_id, need, _json(flags)))
                db.execute("INSERT INTO demand_link VALUES(?,?,?,?,?,?,'open')", ("demand:four:" + _hash([record_id, case_id]), case_id, line_id, unresolved_id, need, qty))
                db.execute("INSERT INTO line_source_record VALUES(?,?,?,?,?,?,?,?)", (line_id, record_id, "extraction_parser_index", None, None, raw[""], known_qty, qty_flag))
        for (group, name, unit), record_ids in collisions.items():
            if len(record_ids) > 1:
                cid = "collision:" + _hash([sha, group, name, unit])
                db.execute("INSERT INTO common_collision_group VALUES(?,?,?,?,?,0)", (cid, group, name, unit, len(record_ids)))
                db.executemany("INSERT INTO common_collision_member VALUES(?,?)", [(cid, rid) for rid in record_ids])
        receipt = {"event_id": event_id, "source_json_sha256": sha, "source_records_imported": len(rows),
                   "manifest_semantic_sha256": manifest_digest,
                   "manifest_bytes_sha256": hashlib.sha256(manifest_file.read_bytes()).hexdigest(),
                   "four_case_demand_links": sum(len(p[3]) for p in prepared), "counts": common_counts(db),
                   "grain": "source record != case consumer != accepted unique variant", "accepted_mapping_or_quote": False,
                   "parser_index_is_physical_excel_row": False, "mtphab_imported_as_case": False}
        now = datetime.now(timezone.utc).isoformat()
        db.execute("INSERT INTO four_intake_manifest_pin VALUES(?,?,?,?)", (sha, manifest_digest, _json(manifest), event_id))
        db.execute("INSERT INTO events VALUES(?,?,?,?,?)", (event_id, "four_case_intake", _hash([sha,manifest_digest]), now, _json(receipt)))
        db.execute("COMMIT")
        return receipt
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()


def backfill_verified_manifest_pin(json_path, manifest_path, db_path):
    """Explicit additive correction for the just-built legacy intake, never silent.

    The operator must supply the original handoff. Every raw record, stored source
    metadata and planning deadline must agree. Original import receipt is retained.
    """
    data = Path(json_path).read_bytes()
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    sha, md = hashlib.sha256(data).hexdigest(), _hash(manifest)
    rows = json.loads(data)
    if sha != manifest["sha256"] or len(data) != manifest["bytes"] or len(rows) != manifest["row_count"]:
        raise IntakeConflict("handoff hash/coverage does not match manifest")
    path = Path(db_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    db = sqlite3.connect(path,isolation_level=None)
    try:
        _schema(db)
        db.executescript(SCHEMA)
        db.execute("BEGIN IMMEDIATE")
        event_id = "verified-manifest-pin:" + _hash([sha,md])
        old = db.execute("SELECT receipt FROM events WHERE event_id=?",(event_id,)).fetchone()
        if old:
            db.execute("COMMIT")
            return json.loads(old[0])
        if not db.execute("SELECT 1 FROM events WHERE event_id=?",("four-case-intake:"+sha,)).fetchone():
            raise IntakeConflict("no matching historical intake event")
        for source in manifest["sources"]:
            stored = db.execute("SELECT metadata FROM external_source_provenance WHERE source_group=?",(source["group"],)).fetchone()
            if not stored or stored[0] != _json(source):
                raise IntakeConflict("legacy stored source provenance does not match supplied original manifest")
        wanted = {(r["group"],r["Mã DM chung"],r[""]):_hash(r) for r in rows}
        actual = {(g,c,i):p for g,c,i,p in db.execute("SELECT source_group,master_code,parser_index,payload_sha256 FROM common_source_record WHERE cohort='four-BV' AND source_version=?",(sha,))}
        if len(wanted)!=len(rows) or actual!=wanted:
            raise IntakeConflict("legacy raw source record payloads do not match supplied handoff")
        for case_id,label in CASES.values():
            deadline = db.execute("SELECT deadline_observed FROM tender_case WHERE case_id=?",(case_id,)).fetchone()
            if not deadline or deadline[0]!=manifest["case_deadlines_planning_only"].get(label):
                raise IntakeConflict("planning deadline metadata differs; review required")
        existing = db.execute("SELECT manifest_semantic_sha256 FROM four_intake_manifest_pin WHERE source_json_sha256=?",(sha,)).fetchone()
        if existing and existing[0]!=md:
            raise IntakeConflict("manifest pin already has another provenance")
        db.execute("INSERT OR IGNORE INTO four_intake_manifest_pin VALUES(?,?,?,?)",(sha,md,_json(manifest),event_id))
        receipt={"event_id":event_id,"source_json_sha256":sha,"manifest_semantic_sha256":md,
                 "verified_raw_records":len(rows),"correction":"additive manifest pin; historical import receipt retained",
                 "business_rows_changed":0,"commercial_approval":False}
        db.execute("INSERT INTO events VALUES(?,?,?,?,?)",(event_id,"verified_manifest_pin",_hash([sha,md]),datetime.now(timezone.utc).isoformat(),_json(receipt)))
        db.execute("COMMIT")
        return receipt
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()
