"""Explicit local lifecycle receipts and a derived worklist; no live authorization."""
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sqlite3
from .catalog_intake import IntakeConflict, _json, _hash

SCHEMA = """
CREATE TABLE IF NOT EXISTS resolved_variant_identity(
 variant_id TEXT PRIMARY KEY REFERENCES normalized_variant(variant_id), identity_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS line_resolution(
 line_id TEXT PRIMARY KEY REFERENCES case_line(line_id), variant_id TEXT NOT NULL REFERENCES normalized_variant(variant_id),
 evidence_ref TEXT NOT NULL, reviewed_by TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS fulfillment_need(
 need_id TEXT PRIMARY KEY, line_id TEXT NOT NULL REFERENCES case_line(line_id), remaining_quantity TEXT,
 status TEXT NOT NULL CHECK(status IN ('open','fulfilled','cancelled')), evidence_ref TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS case_lifecycle_control(
 case_id TEXT PRIMARY KEY REFERENCES tender_case(case_id), planned_closure_date TEXT);
"""


def initialize_lifecycle(db_path):
    path=Path(db_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    db=sqlite3.connect(path)
    try:
        if db.execute("SELECT version FROM catalog_schema").fetchall()!=[(1,)]:
            raise ValueError("existing catalog schema required")
        db.executescript(SCHEMA)
    finally:
        db.close()


def _event(db_path,event_id,kind,payload,change):
    if not event_id or not isinstance(event_id,str):
        raise ValueError("event_id required")
    initialize_lifecycle(db_path)
    db=sqlite3.connect(Path(db_path).resolve(),isolation_level=None)
    checksum=_hash({"kind":kind,"payload":payload})
    try:
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("BEGIN IMMEDIATE")
        old=db.execute("SELECT payload_sha256,receipt FROM events WHERE event_id=?",(event_id,)).fetchone()
        if old:
            if old[0]!=checksum:
                raise IntakeConflict("lifecycle event_id reused with changed payload")
            db.execute("COMMIT")
            return json.loads(old[1])
        result=change(db)
        receipt={"event_id":event_id,"kind":kind,"payload_sha256":checksum,"result":result,
                 "scope":"local operator evidence; not authenticated business authorization"}
        db.execute("INSERT INTO events VALUES(?,?,?,?,?)",(event_id,kind,checksum,datetime.now(timezone.utc).isoformat(),_json(receipt)))
        db.execute("COMMIT")
        return receipt
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()


def _case(db,case_id):
    row=db.execute("SELECT status,deadline_observed FROM tender_case WHERE case_id=?",(case_id,)).fetchone()
    if not row:
        raise ValueError("unknown case")
    return row


def _evidence(value):
    if not isinstance(value,str) or not value.strip():
        raise ValueError("explicit evidence reference required")


def transition_case(db_path,event_id,case_id,action,evidence_ref):
    payload={"case_id":case_id,"action":action,"evidence_ref":evidence_ref}
    def change(db):
        _evidence(evidence_ref)
        current,_=_case(db,case_id)
        target={"close":"closed","cancel":"cancelled","win":"won","reopen":"active"}.get(action)
        if not target or (action=="reopen" and current=="active") or (action!="reopen" and current!="active"):
            raise ValueError("explicit legal lifecycle transition required")
        db.execute("UPDATE tender_case SET status=? WHERE case_id=?",(target,case_id))
        return {"case_id":case_id,"previous":current,"status":target,"history_deleted":False}
    return _event(db_path,event_id,"common_case_transition",payload,change)


def extend_deadline(db_path,event_id,case_id,new_date,evidence_ref):
    payload={"case_id":case_id,"new_date":new_date,"evidence_ref":evidence_ref}
    def change(db):
        _evidence(evidence_ref)
        proposed=date.fromisoformat(new_date)
        current,old=_case(db,case_id)
        if old and proposed<=date.fromisoformat(old):
            raise ValueError("extension must be later than the observed date")
        db.execute("UPDATE tender_case SET deadline_observed=? WHERE case_id=?",(new_date,case_id))
        return {"case_id":case_id,"old_date":old,"new_date":new_date,"status_unchanged":current,
                "formal_closing_time":"not inferred"}
    return _event(db_path,event_id,"common_deadline_extension",payload,change)


def plan_closure(db_path,event_id,case_id,planned_date,evidence_ref):
    payload={"case_id":case_id,"planned_date":planned_date,"evidence_ref":evidence_ref}
    def change(db):
        _evidence(evidence_ref);date.fromisoformat(planned_date)
        status,_=_case(db,case_id)
        db.execute("INSERT INTO case_lifecycle_control VALUES(?,?) ON CONFLICT(case_id) DO UPDATE SET planned_closure_date=excluded.planned_closure_date",(case_id,planned_date))
        return {"case_id":case_id,"planned_date":planned_date,"status_unchanged":status}
    return _event(db_path,event_id,"common_closure_plan",payload,change)


def resolve_line(db_path,event_id,line_id,variant_id,identity,evidence_ref,reviewed_by):
    """Only an explicit reviewed binding; no name matching or inferred equivalence."""
    payload={"line_id":line_id,"variant_id":variant_id,"identity":identity,"evidence_ref":evidence_ref,"reviewed_by":reviewed_by}
    def change(db):
        _evidence(evidence_ref);_evidence(reviewed_by);_evidence(variant_id)
        required={"mpsc","specification","uom","registration_id","valid_from","valid_until"}
        if not isinstance(identity,dict) or set(identity)!=required:
            raise ValueError("complete explicit identity fields required; optional registration/validity may be null")
        for key in ("mpsc","specification","uom"):
            _evidence(identity[key])
        if not db.execute("SELECT 1 FROM case_line WHERE line_id=?",(line_id,)).fetchone():
            raise ValueError("unknown case line")
        checksum=_hash(identity)
        prior=db.execute("SELECT identity_sha256 FROM normalized_variant WHERE variant_id=?",(variant_id,)).fetchone()
        if prior and prior[0]!=checksum:
            raise IntakeConflict("resolved variant ID has different identity")
        same=db.execute("SELECT variant_id FROM normalized_variant WHERE identity_sha256=?",(checksum,)).fetchone()
        if same and same[0]!=variant_id:
            raise IntakeConflict("identity already has another canonical variant ID")
        binding=db.execute("SELECT variant_id FROM line_resolution WHERE line_id=?",(line_id,)).fetchone()
        if binding:
            raise IntakeConflict("existing resolution requires an explicit amendment, not overwrite")
        db.execute("INSERT OR IGNORE INTO normalized_variant VALUES(?,?,?)",(variant_id,checksum,evidence_ref))
        db.execute("INSERT OR IGNORE INTO resolved_variant_identity VALUES(?,?)",(variant_id,_json(identity)))
        db.execute("INSERT INTO line_resolution VALUES(?,?,?,?)",(line_id,variant_id,evidence_ref,reviewed_by))
        return {"line_id":line_id,"variant_id":variant_id,"binding":"explicit local reviewed receipt",
                "quote_or_bid_accepted":False}
    return _event(db_path,event_id,"common_line_resolution",payload,change)


def create_fulfillment(db_path,event_id,need_id,line_id,remaining_quantity,evidence_ref):
    payload={"need_id":need_id,"line_id":line_id,"remaining_quantity":remaining_quantity,"evidence_ref":evidence_ref}
    def change(db):
        _evidence(evidence_ref);_evidence(need_id)
        row=db.execute("SELECT case_id FROM case_line WHERE line_id=?",(line_id,)).fetchone()
        if not row or _case(db,row[0])[0]!="won":
            raise ValueError("explicit won case and known line required")
        if remaining_quantity is not None:
            try:
                amount=Decimal(remaining_quantity) if isinstance(remaining_quantity,str) else None
                if amount is None or not amount.is_finite() or amount<=0:
                    raise InvalidOperation()
            except InvalidOperation:
                raise ValueError("remaining quantity must be a positive decimal string or null")
        db.execute("INSERT INTO fulfillment_need VALUES(?,?,?,'open',?)",(need_id,line_id,remaining_quantity,evidence_ref))
        return {"need_id":need_id,"status":"open","source_demand_preserved":True}
    return _event(db_path,event_id,"common_fulfillment_create",payload,change)


def finish_fulfillment(db_path,event_id,need_id,disposition,evidence_ref):
    payload={"need_id":need_id,"disposition":disposition,"evidence_ref":evidence_ref}
    def change(db):
        _evidence(evidence_ref)
        row=db.execute("SELECT status FROM fulfillment_need WHERE need_id=?",(need_id,)).fetchone()
        if not row or row[0]!="open" or disposition not in {"fulfilled","cancelled"}:
            raise ValueError("explicit disposition of an open fulfillment need required")
        db.execute("UPDATE fulfillment_need SET status=?,evidence_ref=? WHERE need_id=?",(disposition,evidence_ref,need_id))
        return {"need_id":need_id,"status":disposition}
    return _event(db_path,event_id,"common_fulfillment_disposition",payload,change)


def active_worklist(db_path,as_of=None):
    """Read-only projection. Unresolved lines never collapse by name/code/UOM."""
    today=as_of or date.today()
    db=sqlite3.connect(Path(db_path).resolve().as_uri()+"?mode=ro",uri=True)
    db.row_factory=sqlite3.Row
    try:
        prefix="SELECT l.line_id,l.case_id,l.name_raw,l.uom_raw,c.status,c.deadline_observed,r.variant_id,v.identity_json,"
        joins=" FROM case_line l JOIN tender_case c ON c.case_id=l.case_id LEFT JOIN line_resolution r ON r.line_id=l.line_id LEFT JOIN resolved_variant_identity v ON v.variant_id=r.variant_id "
        pre=db.execute(prefix+"d.link_id AS need_id,d.need_type,p.quantity_normalized AS quantity,p.quantity_flag"+joins+
                       "JOIN demand_link d ON d.line_id=l.line_id LEFT JOIN line_source_record p ON p.line_id=l.line_id WHERE c.status='active' AND d.status='open' AND l.source_version=c.active_source_version").fetchall()
        post=db.execute(prefix+"f.need_id,'fulfillment' AS need_type,f.remaining_quantity AS quantity,NULL AS quantity_flag"+joins+
                        "JOIN fulfillment_need f ON f.line_id=l.line_id WHERE f.status='open'").fetchall()
        groups={}
        for row in [*pre,*post]:
            item=dict(row)
            family="fulfillment" if item["need_type"]=="fulfillment" else "prebid"
            key=(family,"resolved:"+item["variant_id"] if item["variant_id"] else "unresolved:"+item["line_id"])
            g=groups.setdefault(key,{"key":key[1],"need_family":family,"resolved_variant_id":item["variant_id"],
                                      "known_quantity":Decimal(0),"unknown_quantity_count":0,"demands":[]})
            flags=[]
            if item["deadline_observed"] and today>date.fromisoformat(item["deadline_observed"]) and item["status"]=="active":
                flags.append("overdue_unknown_not_auto_closed")
            if item["quantity_flag"]:
                flags.append(item["quantity_flag"])
            if item["variant_id"] and json.loads(item["identity_json"])["uom"]!=item["uom_raw"]:
                flags.append("unit_conversion_not_attested")
            if item["quantity"] is None or not item["uom_raw"] or "unit_conversion_not_attested" in flags:
                g["unknown_quantity_count"]+=1
            else:
                g["known_quantity"]+=Decimal(item["quantity"])
            item.pop("identity_json")
            item["flags"]=flags
            g["demands"].append(item)
        return [{**groups[k],"known_quantity":str(groups[k]["known_quantity"]),
                 "quantity_total":None if groups[k]["unknown_quantity_count"] else str(groups[k]["known_quantity"])}
                for k in sorted(groups)]
    finally:
        db.close()


def source_worklist(db_path,as_of=None):
    """One evidence inquiry per ORIGINAL source row; not a product identity merge.

    Consumers retain separate qualification obligations in active_worklist. This
    view reuses an inquiry for the same master record while forbidding an implicit
    cross-record or Kom/common name/UOM merge.
    """
    demand_groups=active_worklist(db_path,as_of)
    db=sqlite3.connect(Path(db_path).resolve().as_uri()+"?mode=ro",uri=True)
    try:
        links=dict(db.execute("SELECT line_id,record_id FROM line_source_record"))
        records={row[0]:row[1:] for row in db.execute("SELECT record_id,cohort,source_group,master_code,source_anchor FROM common_source_record")}
    finally:
        db.close()
    groups={}
    for group in demand_groups:
        for demand in group["demands"]:
            record_id=links[demand["line_id"]]
            key=(group["need_family"],record_id)
            cohort,source_group,code,anchor=records[record_id]
            item=groups.setdefault(key,{"record_id":record_id,"need_family":group["need_family"],
                  "cohort":cohort,"source_group":source_group,"master_code":code,"source_anchor":anchor,
                  "name_raw":demand["name_raw"],"reuse_scope":"same_original_master_row",
                  "case_demands":[]})
            item["case_demands"].append({**demand,"resolved_variant_id":group["resolved_variant_id"]})
    result=[]
    for key in sorted(groups):
        group=groups[key]
        variants={d["resolved_variant_id"] for d in group["case_demands"]}
        verified=None not in variants and len(variants)==1
        result.append({**group,"case_refs":sorted({d["case_id"] for d in group["case_demands"]}),
                       "need_types":sorted({d["need_type"] for d in group["case_demands"]}),
                       "demand_count":len(group["case_demands"]),"identity_verified":verified,
                       "cross_record_merge":False,"per_case_qualification_required":True})
    return result
