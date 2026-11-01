"""Local catalog intake: retain every source demand before identity resolution.

This module imports explicit CSV bytes into one operator-chosen SQLite database.
It performs no external lookup, pharmacological matching, price calculation,
commercial approval, source mutation or identity merge. Fixture principals from
the mission pilot are deliberately not used to pretend a real employee ran this.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date, datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3


class IntakeConflict(ValueError):
    pass


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _nullable(value):
    return value if value is not None and value.strip() else None


def _boolean(value, name):
    if value.casefold() not in {"true", "false"}:
        raise ValueError(f"{name} must be explicitly true/false")
    return value.casefold() == "true"


SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS catalog_schema(version INTEGER PRIMARY KEY CHECK(version=1));
CREATE TABLE IF NOT EXISTS source_artifact(
 artifact_sha256 TEXT PRIMARY KEY, kind TEXT NOT NULL, file_name TEXT NOT NULL,
 locator TEXT NOT NULL, size_bytes INTEGER, metadata_only INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS tender_case(
 case_id TEXT PRIMARY KEY, status TEXT NOT NULL, source_status TEXT NOT NULL,
 active_source_version TEXT NOT NULL, deadline_observed TEXT,
 official_closing_time TEXT, closure_policy TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS intake_batch(
 batch_id TEXT PRIMARY KEY, csv_sha256 TEXT UNIQUE NOT NULL,
 case_id TEXT NOT NULL REFERENCES tender_case(case_id), receipt TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS case_line(
 line_id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES tender_case(case_id),
 source_version TEXT NOT NULL REFERENCES source_artifact(artifact_sha256),
 source_sheet TEXT NOT NULL, source_row INTEGER NOT NULL, source_anchor TEXT NOT NULL,
 source_message_id TEXT, stt_raw TEXT, group_raw TEXT, category TEXT,
 item_code_raw TEXT, mpsc_raw TEXT, name_raw TEXT NOT NULL, name_normalized_candidate TEXT,
 specification_raw TEXT, specification_status TEXT, uom_raw TEXT, uom_normalized_candidate TEXT,
 quantity_raw TEXT, quantity_status TEXT, intake_state TEXT NOT NULL,
 destination_anchor_candidate TEXT, destination_mapping_approved INTEGER NOT NULL CHECK(destination_mapping_approved=0),
 destination_missing INTEGER NOT NULL, row_payload_sha256 TEXT NOT NULL,
 UNIQUE(case_id,source_version,source_sheet,source_row));
CREATE TABLE IF NOT EXISTS unresolved_variant(
 unresolved_id TEXT PRIMARY KEY, line_id TEXT UNIQUE NOT NULL REFERENCES case_line(line_id),
 source_unresolved_key TEXT, candidate_descriptor TEXT NOT NULL,
 identity_missing_components TEXT NOT NULL, identity_complete INTEGER NOT NULL CHECK(identity_complete=0));
CREATE TABLE IF NOT EXISTS normalized_variant(
 variant_id TEXT PRIMARY KEY, identity_sha256 TEXT UNIQUE NOT NULL,
 approved_evidence_ref TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS candidate_match_group(
 case_id TEXT NOT NULL, source_version TEXT NOT NULL, group_key TEXT NOT NULL,
 declared_size INTEGER NOT NULL, state TEXT NOT NULL CHECK(state='pending_review'),
 PRIMARY KEY(case_id,source_version,group_key));
CREATE TABLE IF NOT EXISTS candidate_group_membership(
 line_id TEXT PRIMARY KEY REFERENCES case_line(line_id), case_id TEXT NOT NULL,
 source_version TEXT NOT NULL, group_key TEXT NOT NULL, declared_size INTEGER NOT NULL CHECK(declared_size>0));
CREATE TABLE IF NOT EXISTS candidate_matching(
 workitem_id TEXT PRIMARY KEY, line_id TEXT UNIQUE NOT NULL REFERENCES case_line(line_id),
 unresolved_id TEXT NOT NULL REFERENCES unresolved_variant(unresolved_id),
 state TEXT NOT NULL CHECK(state='pending'), need_type TEXT NOT NULL,
 candidate_group_key TEXT, flags TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS demand_link(
 link_id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES tender_case(case_id),
 line_id TEXT UNIQUE NOT NULL REFERENCES case_line(line_id),
 unresolved_id TEXT NOT NULL REFERENCES unresolved_variant(unresolved_id),
 need_type TEXT NOT NULL, quantity_raw TEXT, status TEXT NOT NULL CHECK(status IN ('open','fulfilled','cancelled')));
CREATE TABLE IF NOT EXISTS source_quote_version(
 quote_reference_id TEXT PRIMARY KEY, line_id TEXT UNIQUE NOT NULL REFERENCES case_line(line_id),
 source_version TEXT NOT NULL, price_anchor TEXT, historical_basis TEXT NOT NULL,
 evidence_kind TEXT NOT NULL CHECK(evidence_kind='historical_price_reference'),
 current_quote_accepted INTEGER NOT NULL CHECK(current_quote_accepted=0));
CREATE TABLE IF NOT EXISTS catalog_candidate_edge(
 edge_id TEXT PRIMARY KEY, line_id TEXT NOT NULL REFERENCES case_line(line_id),
 target_ref TEXT NOT NULL, target_source_anchor TEXT, target_source_sha256 TEXT,
 evidence_state TEXT NOT NULL, relation TEXT NOT NULL, reason TEXT NOT NULL,
 accepted INTEGER NOT NULL CHECK(accepted=0), payload_sha256 TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(
 event_id TEXT PRIMARY KEY, type TEXT NOT NULL, payload_sha256 TEXT NOT NULL,
 occurred_at TEXT NOT NULL, receipt TEXT NOT NULL);
CREATE VIEW IF NOT EXISTS active_sourcing_worklist AS
 SELECT c.case_id,c.deadline_observed,c.official_closing_time,l.line_id,l.source_version,
 l.source_sheet,l.source_row,l.source_anchor,l.name_raw,l.specification_raw,l.uom_raw,
 d.quantity_raw,d.need_type,d.unresolved_id,q.workitem_id,q.state AS queue_state,q.flags
 FROM demand_link d JOIN case_line l ON l.line_id=d.line_id
 JOIN tender_case c ON c.case_id=d.case_id
 JOIN candidate_matching q ON q.line_id=l.line_id
 WHERE c.status='active' AND d.status='open' AND l.source_version=c.active_source_version;
"""

REQUIRED = {"case_id", "case_status", "deadline_observed", "official_closing_time",
            "source_file_name", "source_file_sha256", "source_message_id", "requirement_sheet",
            "requirement_row", "requirement_anchor", "requirement_name_raw", "requirement_spec_raw",
            "requirement_uom_raw", "quantity_raw", "quantity_status", "intake_state",
            "historical_price_basis", "historical_price_available", "destination_missing",
            "candidate_anchor", "identity_complete", "identity_missing_components",
            "unresolved_identity_key", "normalized_variant_descriptor", "candidate_group_key",
            "candidate_group_size"}


def _prepare(raw_bytes):
    reader = csv.DictReader(io.StringIO(raw_bytes.decode("utf-8-sig"), newline=""))
    if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
        raise ValueError("CSV header is missing or duplicates fields")
    if not REQUIRED.issubset(reader.fieldnames):
        raise ValueError("CSV is missing required intake fields")
    records, case_ids, source_versions, case_metadata, anchors = [], set(), set(), set(), set()
    group_counts = {}
    for csv_row, raw in enumerate(reader, 2):
        if None in raw or any(value is None for value in raw.values()):
            raise ValueError(f"malformed CSV row {csv_row}")
        for key in ("case_id", "case_status", "source_file_name", "requirement_sheet",
                    "requirement_anchor", "requirement_name_raw"):
            if not raw[key].strip():
                raise ValueError(f"missing {key} at CSV row {csv_row}")
        source_sha = raw["source_file_sha256"]
        if not re.fullmatch("[0-9a-f]{64}", source_sha):
            raise ValueError("source workbook SHA256 required")
        source_row = int(raw["requirement_row"])
        if source_row <= 0:
            raise ValueError("positive source row required")
        identity = [raw["case_id"], source_sha, raw["requirement_sheet"], source_row]
        identity_key = _json(identity)
        if identity_key in anchors:
            raise IntakeConflict("duplicate source row/version inside this CSV; no row silently dropped")
        anchors.add(identity_key)
        if raw["deadline_observed"]:
            date.fromisoformat(raw["deadline_observed"])
        need = {"sourcing_required": "sourcing", "equivalence_review_required": "equivalence_review",
                "historical_price_revalidation": "historical_price_revalidation"}.get(raw["intake_state"])
        if need is None:
            raise ValueError("unknown intake state; cannot guess sourcing workflow")
        historical = _boolean(raw["historical_price_available"], "historical_price_available")
        _boolean(raw["identity_complete"], "identity_complete")  # A source flag never approves an identity.
        missing_destination = _boolean(raw["destination_missing"], "destination_missing")
        descriptor = json.loads(raw["normalized_variant_descriptor"])
        if not isinstance(descriptor, dict):
            raise ValueError("candidate descriptor must be a JSON object")
        declared_size = int(raw["candidate_group_size"])
        if declared_size < 1:
            raise ValueError("candidate group size must be positive")
        group_key = raw["candidate_group_key"]
        if not group_key.strip():
            raise ValueError("explicit candidate group key required, including singleton rows")
        group_identity = (raw["case_id"], source_sha, group_key)
        group_counts.setdefault(group_identity, {"actual": 0, "declared": declared_size})
        group_counts[group_identity]["actual"] += 1
        if group_counts[group_identity]["declared"] != declared_size:
            raise IntakeConflict("inconsistent candidate group size")
        flags = ["identity_unresolved", "quantity_unknown"] if not raw["quantity_raw"] else ["identity_unresolved"]
        if not raw.get("requirement_mpsc_raw", "").strip():
            flags.append("mpsc_unknown")
        if not raw["requirement_uom_raw"].strip():
            flags.append("requirement_uom_unknown")
        if missing_destination:
            flags.append("destination_mapping_missing")
        if declared_size > 1:
            flags.append("candidate_group_pending_review")
        if historical:
            flags.append("historical_price_not_current_quote")
        if need == "equivalence_review":
            flags.append("equivalence_not_accepted")
        records.append({"raw": raw, "row": source_row, "line_id": "line:" + _hash(identity),
                        "payload_sha256": _hash(raw), "need_type": need,
                        "historical": historical, "destination_missing": missing_destination,
                        "descriptor": descriptor, "group_size": declared_size, "flags": flags})
        case_ids.add(raw["case_id"])
        source_versions.add(source_sha)
        case_metadata.add((raw["case_status"], raw["deadline_observed"], raw["official_closing_time"],
                           raw["source_file_name"]))
    if not records or len(case_ids) != 1 or len(source_versions) != 1 or len(case_metadata) != 1:
        raise ValueError("one explicit case/source version with consistent metadata is required")
    if any(g["actual"] > g["declared"] for g in group_counts.values()):
        raise IntakeConflict("candidate group source members exceed declared size")
    return records


def query_counts(db):
    tables = ("tender_case", "case_line", "unresolved_variant", "normalized_variant",
              "candidate_matching", "demand_link", "source_quote_version", "candidate_match_group",
              "catalog_candidate_edge", "source_artifact", "intake_batch", "events")
    counts = {t: db.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in tables}
    counts["active_workitems"] = db.execute("SELECT count(*) FROM active_sourcing_worklist").fetchone()[0]
    counts["active_needs"] = dict(db.execute("SELECT need_type,count(*) FROM active_sourcing_worklist GROUP BY need_type"))
    counts["unknown_quantity"] = db.execute("SELECT count(*) FROM case_line WHERE quantity_raw IS NULL").fetchone()[0]
    counts["missing_requirement_uom"] = db.execute("SELECT count(*) FROM case_line WHERE uom_raw IS NULL").fetchone()[0]
    counts["candidate_group_rows"] = db.execute("SELECT count(*) FROM candidate_matching WHERE candidate_group_key IS NOT NULL").fetchone()[0]
    counts["accepted_current_quotes"] = db.execute("SELECT count(*) FROM source_quote_version WHERE current_quote_accepted<>0").fetchone()[0]
    return counts


def _schema(db):
    names = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if names and "catalog_schema" not in names:
        raise IntakeConflict("target is not an intake catalog database; existing DB left unchanged")
    if "catalog_schema" in names and db.execute("SELECT version FROM catalog_schema").fetchall() != [(1,)]:
        raise IntakeConflict("unsupported catalog schema version")
    db.executescript(SCHEMA)
    db.execute("INSERT OR IGNORE INTO catalog_schema VALUES(1)")


def _group_membership(db, rec):
    """Persist declarations for every source row, including singleton groups."""
    raw = rec["raw"]
    identity = (raw["case_id"], raw["source_file_sha256"], raw["candidate_group_key"])
    declaration = db.execute("SELECT declared_size FROM candidate_match_group "
                             "WHERE case_id=? AND source_version=? AND group_key=?", identity).fetchone()
    if declaration and declaration[0] != rec["group_size"]:
        raise IntakeConflict("existing candidate group declared size conflicts with incoming declaration")
    prior_sizes = db.execute("SELECT DISTINCT declared_size FROM candidate_group_membership "
                             "WHERE case_id=? AND source_version=? AND group_key=?", identity).fetchall()
    if any(size[0] != rec["group_size"] for size in prior_sizes):
        raise IntakeConflict("existing candidate group member declared size conflicts with incoming declaration")
    value = (rec["line_id"], *identity, rec["group_size"])
    old = db.execute("SELECT line_id,case_id,source_version,group_key,declared_size "
                     "FROM candidate_group_membership WHERE line_id=?", (rec["line_id"],)).fetchone()
    if old:
        if tuple(old) != value:
            raise IntakeConflict("source row group membership changed without a source version change")
    else:
        db.execute("INSERT INTO candidate_group_membership VALUES(?,?,?,?,?)", value)
    if rec["group_size"] > 1:
        db.execute("INSERT OR IGNORE INTO candidate_match_group VALUES(?,?,?,?,'pending_review')",
                   (*identity, rec["group_size"]))


def _validate_group_coverage(db, case_id, source_sha):
    """Check cumulative membership, never merely the current CSV's row count."""
    missing = db.execute("SELECT count(*) FROM case_line l LEFT JOIN candidate_group_membership g "
                         "ON g.line_id=l.line_id WHERE l.case_id=? AND l.source_version=? AND g.line_id IS NULL",
                         (case_id, source_sha)).fetchone()[0]
    if missing:
        raise IntakeConflict("legacy group metadata incomplete; include unchanged prior source rows for validated backfill")
    groups = db.execute("SELECT group_key,min(declared_size),max(declared_size),count(*) "
                        "FROM candidate_group_membership WHERE case_id=? AND source_version=? GROUP BY group_key",
                        (case_id, source_sha)).fetchall()
    coverage = []
    for key, low, high, observed in groups:
        if low != high or observed > high:
            raise IntakeConflict("cumulative candidate group members exceed or conflict with declared size")
        if high > 1:
            coverage.append({"group_key": key, "declared_size": high, "observed_members": observed,
                             "coverage_state": ("coverage_pending" if observed < high
                                                else "membership_complete_pending_review"),
                             "identity_accepted": False})
    return coverage


def import_csv(csv_path, db_path, expected_rows=None):
    path, target = Path(csv_path).resolve(), Path(db_path).resolve()
    raw_bytes = path.read_bytes()
    csv_sha = hashlib.sha256(raw_bytes).hexdigest()
    records = _prepare(raw_bytes)
    if expected_rows is not None and len(records) != expected_rows:
        raise ValueError(f"expected {expected_rows} source rows, got {len(records)}")
    first = records[0]["raw"]
    source_sha, case_id = first["source_file_sha256"], first["case_id"]
    batch_id = "catalog-intake:" + csv_sha
    target.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(target, isolation_level=None)
    try:
        # An exact historical retry is a read, even after this additive schema update.
        # Do not mutate an already imported catalog merely to add group metadata.
        names = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "catalog_schema" in names and "intake_batch" in names:
            if db.execute("SELECT version FROM catalog_schema").fetchall() != [(1,)]:
                raise IntakeConflict("unsupported catalog schema version")
            prior = db.execute("SELECT receipt FROM intake_batch WHERE batch_id=?", (batch_id,)).fetchone()
            if prior:
                return json.loads(prior[0])
        _schema(db)
        db.execute("BEGIN IMMEDIATE")
        prior = db.execute("SELECT receipt FROM intake_batch WHERE batch_id=?", (batch_id,)).fetchone()
        if prior:
            db.execute("COMMIT")
            return json.loads(prior[0])
        existing_case = db.execute("SELECT active_source_version FROM tender_case WHERE case_id=?", (case_id,)).fetchone()
        if existing_case and existing_case[0] != source_sha:
            raise IntakeConflict("new workbook source version needs explicit reviewed promotion; current case was not changed")
        # Never reactivate or change deadline/status of an existing case on late intake.
        db.execute("INSERT OR IGNORE INTO tender_case VALUES(?,?,?,?,?,?,?)",
                   (case_id, "active", first["case_status"], source_sha,
                    _nullable(first["deadline_observed"]), _nullable(first["official_closing_time"]),
                    "deadline_observation_is_not_auto_close; official hour unknown remains null"))
        db.execute("INSERT OR IGNORE INTO source_artifact VALUES(?,?,?,?,?,?)",
                   (csv_sha, "intake_csv", path.name, str(path), len(raw_bytes), 0))
        db.execute("INSERT OR IGNORE INTO source_artifact VALUES(?,?,?,?,?,?)",
                   (source_sha, "workbook_reference", first["source_file_name"],
                    first["source_file_name"], None, 1))
        inserted = 0
        for rec in records:
            raw, line_id = rec["raw"], rec["line_id"]
            old = db.execute("SELECT row_payload_sha256 FROM case_line WHERE line_id=?", (line_id,)).fetchone()
            if old:
                if old[0] != rec["payload_sha256"]:
                    raise IntakeConflict("same case/source row/version has conflicting CSV payload")
                _group_membership(db, rec)
                continue
            unresolved_id = "unresolved:" + line_id.split(":", 1)[1]
            db.execute("INSERT INTO case_line VALUES(" + ",".join("?" for _ in range(25)) + ")",
                       (line_id, case_id, source_sha, raw["requirement_sheet"], rec["row"], raw["requirement_anchor"],
                        _nullable(raw["source_message_id"]), _nullable(raw.get("stt_raw")), _nullable(raw.get("group_raw")),
                        _nullable(raw.get("category_normalized")), _nullable(raw.get("requirement_code_raw")),
                        _nullable(raw.get("requirement_mpsc_raw")), raw["requirement_name_raw"],
                        _nullable(raw.get("requirement_name_normalized")), _nullable(raw["requirement_spec_raw"]),
                        _nullable(raw.get("requirement_spec_status")), _nullable(raw["requirement_uom_raw"]),
                        _nullable(raw.get("requirement_uom_normalized")), _nullable(raw["quantity_raw"]),
                        raw["quantity_status"], raw["intake_state"], _nullable(raw["candidate_anchor"]),
                        0, int(rec["destination_missing"]), rec["payload_sha256"]))
            db.execute("INSERT INTO unresolved_variant VALUES(?,?,?,?,?,0)",
                       (unresolved_id, line_id, raw["unresolved_identity_key"], _json(rec["descriptor"]),
                        raw["identity_missing_components"]))
            _group_membership(db, rec)
            group_key = raw["candidate_group_key"] if rec["group_size"] > 1 else None
            db.execute("INSERT INTO candidate_matching VALUES(?,?,?,'pending',?,?,?)",
                       ("match:" + line_id.split(":", 1)[1], line_id, unresolved_id,
                        rec["need_type"], group_key, _json(rec["flags"])))
            db.execute("INSERT INTO demand_link VALUES(?,?,?,?,?,?,'open')",
                       ("demand:" + line_id.split(":", 1)[1], case_id, line_id, unresolved_id,
                        rec["need_type"], _nullable(raw["quantity_raw"])))
            if rec["historical"]:
                db.execute("INSERT INTO source_quote_version VALUES(?,?,?,?,?,'historical_price_reference',0)",
                           ("history:" + line_id.split(":", 1)[1], line_id, source_sha,
                            _nullable(raw.get("history_price_anchors")) or _nullable(raw["candidate_anchor"]),
                            raw["historical_price_basis"]))
            inserted += 1
        coverage = _validate_group_coverage(db, case_id, source_sha)
        now = datetime.now(timezone.utc).isoformat()
        counts = query_counts(db)
        # These two rows are committed below in the same transaction as all imported records.
        counts["intake_batch"] += 1
        counts["events"] += 1
        receipt = {"schema": "catalog-intake-receipt/1", "batch_id": batch_id, "csv_sha256": csv_sha,
                   "csv_path": str(path), "source_workbook_sha256": source_sha,
                   "source_workbook_name": first["source_file_name"], "case_id": case_id,
                   "occurred_at": now, "source_rows": len(records), "inserted_rows": inserted,
                   "unchanged_existing_rows": len(records) - inserted, "counts": counts,
                   "candidate_group_coverage": coverage,
                   "partial_group_policy": "retain all observed rows; incomplete membership stays coverage_pending and unaccepted",
                   "identity_resolution": "all retained unresolved; zero accepted merge",
                   "current_price_or_bid_approval": False, "scope": "Kom intake only; not combined four-hospital catalog"}
        encoded = _json(receipt)
        db.execute("INSERT INTO intake_batch VALUES(?,?,?,?)", (batch_id, csv_sha, case_id, encoded))
        db.execute("INSERT INTO events VALUES(?,?,?,?,?)",
                   (batch_id, "catalog_intake", csv_sha, now, encoded))
        db.execute("COMMIT")
        return receipt
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()


def record_candidate_edges(db_path, edges):
    """Optional inquiry-only bridge, never a resolved link or accepted quotation."""
    payload = json.loads(_json(edges))
    event_id = "candidate-inquiry:" + _hash(payload)
    path = Path(db_path).resolve()
    if not path.is_file():
        raise FileNotFoundError("existing imported catalog DB required")
    db = sqlite3.connect(path, isolation_level=None)
    try:
        _schema(db)
        db.execute("BEGIN IMMEDIATE")
        old = db.execute("SELECT receipt FROM events WHERE event_id=?", (event_id,)).fetchone()
        if old:
            db.execute("COMMIT")
            return json.loads(old[0])
        inserted = 0
        for edge in payload:
            if edge.get("accepted") is not False:
                raise ValueError("inquiry edge must explicitly be unaccepted")
            if edge["evidence_state"] not in {"parent_reported_source_pin_pending", "local_pinned_pending_review"}:
                raise ValueError("unreviewed provenance state required")
            line = db.execute("SELECT line_id FROM case_line WHERE case_id=? AND source_row=? AND source_version=?",
                              (edge["case_id"], edge["source_row"], edge["source_workbook_sha256"])).fetchall()
            if len(line) != 1:
                raise ValueError("candidate source anchor must resolve to exactly one retained line")
            checksum = _hash(edge)
            prior = db.execute("SELECT payload_sha256 FROM catalog_candidate_edge WHERE edge_id=?", (edge["edge_id"],)).fetchone()
            if prior:
                if prior[0] != checksum:
                    raise IntakeConflict("candidate edge_id conflict")
                continue
            db.execute("INSERT INTO catalog_candidate_edge VALUES(?,?,?,?,?,?,?,?,0,?)",
                       (edge["edge_id"], line[0][0], edge["target_ref"], edge.get("target_source_anchor"),
                        edge.get("target_source_sha256"), edge["evidence_state"], edge["relation"], edge["reason"], checksum))
            inserted += 1
        receipt = {"event_id": event_id, "inserted_inquiry_edges": inserted,
                   "accepted_merge": 0, "resolved_variant_links_created": 0}
        now = datetime.now(timezone.utc).isoformat()
        db.execute("INSERT INTO events VALUES(?,?,?,?,?)", (event_id, "candidate_inquiry", _hash(payload), now, _json(receipt)))
        db.execute("COMMIT")
        return receipt
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--expected-rows", type=int)
    args = parser.parse_args(argv)
    receipt = import_csv(args.csv, args.db, args.expected_rows)
    print(json.dumps(receipt, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
