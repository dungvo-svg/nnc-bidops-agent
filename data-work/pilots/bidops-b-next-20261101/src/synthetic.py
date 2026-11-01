"""Fictional records for the local demo/tests; never ingest business sources."""
from datetime import datetime, timezone
from .ledger import Ledger, canonical

FIXED_NOW = datetime(2026, 10, 31, 12, 0, tzinfo=timezone.utc)
NODES = [
    {"node_id": "builder", "owner_id": "fictional-ceo", "agent_id": "agent-ceo",
     "capabilities": ["source_intake", "quote_intake", "requirement_intake", "catalog_intake",
                      "case_manage", "mission_issue", "mission_cancel", "mission_receive", "mission_return"]},
    {"node_id": "staff-a", "owner_id": "fictional-staff-a", "agent_id": "agent-a",
     "capabilities": ["mission_receive", "mission_accept", "mission_return", "candidate_review"]},
    {"node_id": "staff-b", "owner_id": "fictional-staff-b", "agent_id": "agent-b",
     "capabilities": ["mission_receive", "mission_accept", "mission_return"]},
    {"node_id": "reviewer", "owner_id": "fictional-reviewer", "agent_id": "agent-reviewer",
     "capabilities": ["candidate_review", "candidate_apply", "candidate_use", "candidate_diagnostic_use"]},
]


def actor(node_id):
    n = next(n for n in NODES if n["node_id"] == node_id)
    return {k: n[k] for k in ("node_id", "owner_id", "agent_id")}


def source(source_id, version="1", sha="a", observed="2026-10-28T00:00:00Z"):
    return {"source_id": source_id, "version": version, "sha256": sha * 64,
            "observed_at": observed, "locator": f"synthetic://{source_id}/{version}"}


def variant(variant_id, length="30", **changes):
    return {"variant_id": variant_id, "item_code": "SAME-CODE",
            "specification": {"needle_length_mm": length}, "unit": "EA",
            "registration_id": "fictional-registration-A", "identity_valid_from": "2026-01-01",
            "identity_valid_until": "2027-12-31", **changes}


def quote(quote_id="q30", variant_id="v30", source_id="quote-src", **changes):
    return {"quote_id": quote_id, "supplier_id": "fictional-supplier",
            "item_code": "SAME-CODE", "variant_id": variant_id, "unit": "EA",
            "currency": "USD", "basis": "per EA, fictional EXW", "price": "12.50",
            "valid_from": "2026-10-01", "valid_until": "2026-11-30",
            "source_ref": {"source_id": source_id, "version": "1"}, **changes}


def requirement(package_id="river", requirement_id="line-1", variant_id="v30", **changes):
    return {"package_id": package_id, "requirement_id": requirement_id, "version": "1",
            "item_code": "SAME-CODE", "variant_id": variant_id, "unit": "EA",
            "source_ref": {"source_id": "demand-src", "version": "1"},
            "destination": f"fictional-sheet/{requirement_id}", **changes}


def evidence(source_id="quote-src"):
    return {axis: {"ref": f"synthetic://evidence/{axis}",
                   "source_ref": {"source_id": source_id, "version": "1"}}
            for axis in ("goods", "documents", "money")}


def seed(db_path, clock=None):
    ledger = Ledger(db_path, NODES, clock or (lambda: FIXED_NOW))
    who = actor("builder")
    ledger.intake_source("seed-src-demand", who, source("demand-src"))
    ledger.intake_source("seed-src-quote", who, source("quote-src", sha="b", observed="2026-10-29T00:00:00Z"))
    ledger.intake_source("seed-src-other", who, source("other-src", sha="c"))
    ledger.intake_variant("seed-v30", who, variant("v30"))
    ledger.intake_variant("seed-v40", who, variant("v40", "40"))
    for case_id in ("river", "hill"):
        ledger.create_case(f"seed-case-{case_id}", who, case_id,
                           f"Fictional {case_id} 2027", "2026-11-03T10:00:00Z")
    for req in (requirement(), requirement("hill"), requirement(requirement_id="line-2", variant_id="v40")):
        ledger.intake_requirement(f"seed-req-{req['package_id']}-{req['requirement_id']}", who, req)
    for q in (quote(), quote("q40", "v40"), quote("q-other", source_id="other-src")):
        ledger.intake_quote(f"seed-quote-{q['quote_id']}", who, q)
    return ledger


def issue(ledger, mission_id, key=None, quote_id="q30", node_id="staff-a"):
    key = key or ["river", "line-1", "1"]
    q = ledger._get("quote", quote_id)
    req = ledger._get("requirement", canonical(key))
    if not ledger.prebid_demand_active(key):
        link_id = "synthetic-mission-demand-" + "-".join(key)
        ledger.link_demand(link_id, actor("builder"),
                           {"link_id": link_id, "requirement_key": key,
                            "need_type": "prebid_sourcing", "quantity": None})
    mission = {"mission_id": mission_id, "node_id": node_id, "requirement_key": key,
               "quote_ids": [quote_id], "source_manifest": [req["source_ref"], q["source_ref"]],
               "deadline": "2026-11-02T12:00:00Z", "expected_output": "variant-aware decision packet"}
    return ledger.issue_mission(f"{mission_id}-issue", actor("builder"), mission)


def returned(ledger, mission_id="m1", key=None, quote_id="q30", ev=None):
    issue(ledger, mission_id, key, quote_id)
    ledger.receive_mission(f"{mission_id}-receive", actor("staff-a"), mission_id)
    ledger.respond_mission(f"{mission_id}-accept", actor("staff-a"), mission_id,
                           "accepted", "synthetic://owner/accepted-scope")
    if ev is None:
        q = ledger._get("quote", quote_id)
        ev = evidence(q["source_ref"]["source_id"])
    receipt = ledger.return_mission(f"{mission_id}-return", actor("staff-a"), mission_id, quote_id, ev)
    return receipt["result"]["candidate"]["candidate_hash"]
