"""Read-only adapter from the local catalog SQLite to Ledger-shaped values.

The catalog stays the only master of case state. Nothing here opens a writable
connection or mutates the catalog. A variant is bridged only through an explicit,
reviewed line_resolution row; never by MPSC, name or unit similarity.
"""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3

from .ledger import digest

_LIFECYCLE_KINDS = ("common_case_transition", "common_deadline_extension", "common_closure_plan")


def _open_readonly(catalog_path):
    path = Path(catalog_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    return sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)


def read_case_snapshot(catalog_path, case_id):
    db = _open_readonly(catalog_path)
    try:
        row = db.execute(
            "SELECT status,source_status,active_source_version,deadline_observed,"
            "official_closing_time,closure_policy FROM tender_case WHERE case_id=?",
            (case_id,)).fetchone()
        if row is None:
            raise ValueError("unknown case")
        status, source_status, source_version, planning, official, policy = row
        marks = ",".join("?" for _ in _LIFECYCLE_KINDS)
        events = []
        for event_id, kind, payload_sha, receipt in db.execute(
                f"SELECT event_id,type,payload_sha256,receipt FROM events WHERE type IN ({marks}) "
                "ORDER BY rowid", _LIFECYCLE_KINDS):
            body = json.loads(receipt)
            result = body.get("result") if isinstance(body, dict) else None
            if not isinstance(result, dict) or result.get("case_id") != case_id:
                continue
            # The catalog keeps only the payload checksum, not the evidence text,
            # so evidence_ref is None unless a receipt ever carries it.
            events.append({"event_id": event_id, "kind": kind,
                           "evidence_ref": result.get("evidence_ref", body.get("evidence_ref")),
                           "payload_sha256": payload_sha})
    finally:
        db.close()
    snapshot = {"schema": "bidops-case-snapshot/1", "case_id": case_id, "status": status,
                "planning_date": planning, "official_closing_at": official,
                "source_status": source_status, "active_source_version": source_version,
                "closure_policy": policy, "lifecycle_events": events}
    return {**snapshot, "snapshot_sha256": digest(snapshot)}


def bridge_variant(catalog_path, line_id):
    db = _open_readonly(catalog_path)
    try:
        line = db.execute(
            "SELECT case_id,source_version,source_anchor,name_raw,uom_raw FROM case_line WHERE line_id=?",
            (line_id,)).fetchone()
        if line is None:
            raise ValueError("unknown case line")
        case_id, source_version, source_anchor, name_raw, uom_raw = line
        try:
            resolution = db.execute(
                "SELECT r.variant_id,r.evidence_ref,r.reviewed_by,n.identity_sha256,i.identity_json "
                "FROM line_resolution r JOIN normalized_variant n ON n.variant_id=r.variant_id "
                "LEFT JOIN resolved_variant_identity i ON i.variant_id=r.variant_id WHERE r.line_id=?",
                (line_id,)).fetchone()
        except sqlite3.OperationalError as error:
            if "no such table" not in str(error):
                raise
            resolution = None  # lifecycle tables never initialised: nothing is resolved
    finally:
        db.close()
    if resolution is None:
        return {"status": "HOLD", "line_id": line_id, "case_id": case_id,
                "reason": "line_unresolved", "variant": None, "provenance": None}
    variant_id, evidence_ref, reviewed_by, identity_sha, identity_json = resolution
    if identity_json is None:
        raise ValueError("resolved line has no stored explicit identity")
    identity = json.loads(identity_json)
    variant = {"variant_id": variant_id, "item_code": identity["mpsc"],
               "specification": {"catalog_specification": identity["specification"]},
               "unit": identity["uom"], "registration_id": identity["registration_id"],
               "identity_valid_from": identity["valid_from"],
               "identity_valid_until": identity["valid_until"]}
    provenance = {"mapping": "explicit_reviewed_line_resolution", "catalog_variant_id": variant_id,
                  "catalog_identity_sha256": identity_sha, "resolution_evidence_ref": evidence_ref,
                  "reviewed_by": reviewed_by, "line_id": line_id, "case_id": case_id,
                  "source_version": source_version, "source_anchor": source_anchor,
                  "name_raw": name_raw, "uom_raw": uom_raw}
    flags = ["unit_conversion_not_attested"] if uom_raw != identity["uom"] else []
    return {"status": "BRIDGED", "line_id": line_id, "case_id": case_id,
            "variant": variant, "provenance": provenance, "flags": flags}
