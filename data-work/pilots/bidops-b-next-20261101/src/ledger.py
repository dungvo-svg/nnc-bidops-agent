"""Small durable event boundary; no network, source parsing or procurement writes.

Actor identifiers and capabilities are fixture configuration, not authentication.
The caller owns the explicit SQLite file. Every state change and its receipt share
one transaction. Returned candidates are proposals, never procurement acceptance.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Callable

from .assessments import certificate_check, portfolio_check


class Conflict(ValueError):
    pass


class Forbidden(ValueError):
    pass


class Blocked(ValueError):
    pass


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp must include UTC offset")
    return parsed


def _ref(value):
    if not isinstance(value, dict) or set(value) != {"source_id", "version"}:
        raise ValueError("source_ref requires source_id and version")
    return {k: _text(value[k], k) for k in ("source_id", "version")}


def _key(value):
    return canonical(value)


def _business_assessments(checks):
    """Five separate business assessments; fixture checks inform, never score or approve."""
    def unknown(reason):
        return {"status": "unknown", "reason": reason}
    certificate, portfolio = checks["certificate"], checks["portfolio"]
    fixture = "fixture check only; business owner has not attested"
    return {
        "dossier_compliance": ({"status": "checked_fixture_only", "reason": fixture,
                                "identity_state": certificate["identity_state"]}
                               if certificate else unknown("no certificate/dossier check supplied")),
        "supply_capability": ({"status": "checked_fixture_only", "reason": fixture,
                               "resource_states": [r["state"] for r in portfolio["resources"]]}
                              if portfolio else unknown("no capacity/allocation check supplied")),
        "economics_working_capital": ({"status": "checked_fixture_only", "reason": fixture + "; no FX, profit or cash",
                                       "currencies": sorted(portfolio["costs_by_currency"])}
                                      if portfolio else unknown("no cost/working-capital check supplied")),
        "competitive_basis": unknown("no competitor or award-basis evidence in pilot"),
        "actual_outcome": unknown("outcome is only known after an award receipt"),
    }


def _nodes(nodes):
    normalized = []
    for node in nodes:
        n = {k: _text(node.get(k), k) for k in ("node_id", "owner_id", "agent_id")}
        caps = node.get("capabilities")
        if not isinstance(caps, list) or any(not isinstance(c, str) for c in caps):
            raise ValueError("capabilities must be a list of strings")
        n["capabilities"] = sorted(set(caps))
        normalized.append(n)
    if len({n["node_id"] for n in normalized}) != len(normalized):
        raise ValueError("duplicate node_id")
    return sorted(normalized, key=lambda n: n["node_id"])


class Ledger:
    def __init__(self, db_path: str | Path, nodes: list[dict],
                 clock: Callable[[], datetime] | None = None):
        normalized = _nodes(nodes)
        self.path = Path(db_path)
        if str(db_path) == ":memory:":
            raise ValueError("choose an explicit persistent pilot DB path")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.db = sqlite3.connect(self.path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS objects(
              kind TEXT NOT NULL, key TEXT NOT NULL, payload TEXT NOT NULL,
              PRIMARY KEY(kind,key));
            CREATE TABLE IF NOT EXISTS source_heads(
              source_id TEXT PRIMARY KEY, version TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS requirement_heads(
              package_id TEXT, requirement_id TEXT, version TEXT NOT NULL,
              PRIMARY KEY(package_id,requirement_id));
            CREATE TABLE IF NOT EXISTS events(
              event_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL,
              envelope TEXT NOT NULL, receipt TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS mission_state(
              mission_id TEXT PRIMARY KEY, status TEXT NOT NULL,
              candidate_id TEXT);
            CREATE TABLE IF NOT EXISTS candidate_state(
              candidate_id TEXT PRIMARY KEY, status TEXT NOT NULL,
              review_event TEXT, apply_event TEXT, use_event TEXT);
            CREATE TABLE IF NOT EXISTS variant_identity(
              identity_hash TEXT PRIMARY KEY, variant_id TEXT UNIQUE NOT NULL);
            CREATE TABLE IF NOT EXISTS case_state(
              case_id TEXT PRIMARY KEY, status TEXT NOT NULL,
              deadline TEXT, planned_closure TEXT);
            CREATE TABLE IF NOT EXISTS demand_state(
              link_id TEXT PRIMARY KEY, status TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS case_authority(
              case_id TEXT PRIMARY KEY, snapshot_sha256 TEXT NOT NULL,
              planning_date TEXT, snapshot TEXT NOT NULL);
        """)
        try:
            with self.db:
                self._immutable("config", "nodes", normalized)
        except BaseException:
            self.db.close()
            raise
        self.nodes = {n["node_id"]: n for n in normalized}

    def close(self):
        self.db.close()

    def now(self):
        now = self.clock()
        if now.tzinfo is None:
            raise ValueError("clock must be timezone aware")
        return now.astimezone(timezone.utc)

    def _get(self, kind, key):
        row = self.db.execute("SELECT payload FROM objects WHERE kind=? AND key=?",
                              (kind, key)).fetchone()
        if row is None:
            raise ValueError(f"unknown {kind}: {key}")
        return json.loads(row[0])

    def _immutable(self, kind, key, payload):
        text = canonical(payload)
        old = self.db.execute("SELECT payload FROM objects WHERE kind=? AND key=?",
                              (kind, key)).fetchone()
        if old:
            if old[0] != text:
                raise Conflict(f"immutable {kind} key reused with different content")
            return False
        self.db.execute("INSERT INTO objects VALUES(?,?,?)", (kind, key, text))
        return True

    def _authorize(self, actor, capability):
        if not isinstance(actor, dict):
            raise Forbidden("explicit node/owner/agent actor required")
        node = self.nodes.get(actor.get("node_id"))
        if node is None or any(actor.get(k) != node[k] for k in
                               ("node_id", "owner_id", "agent_id")):
            raise Forbidden("actor does not match configured owned node")
        if set(actor) != {"node_id", "owner_id", "agent_id"}:
            raise Forbidden("unexpected actor fields")
        if capability not in node["capabilities"]:
            raise Forbidden(f"missing pilot capability: {capability}")
        return node

    def _event(self, event_id, actor, kind, payload, capability, change):
        _text(event_id, "event_id")
        envelope = {"type": kind, "actor": actor, "payload": payload}
        checksum = digest(envelope)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            prior = self.db.execute("SELECT payload_digest,receipt FROM events WHERE event_id=?",
                                    (event_id,)).fetchone()
            if prior:
                if prior[0] != checksum:
                    raise Conflict("event_id collision: actor/type/payload changed")
                self.db.execute("COMMIT")
                return json.loads(prior[1])
            self._authorize(actor, capability)
            result = change()
            receipt = {"event_id": event_id, "type": kind, "payload_digest": checksum,
                       "occurred_at": self.now().isoformat(), "actor": actor,
                       "result": result, "scope": "local-synthetic-only"}
            self.db.execute("INSERT INTO events VALUES(?,?,?,?)",
                            (event_id, checksum, canonical(envelope), canonical(receipt)))
            self.db.execute("COMMIT")
            return receipt
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def intake_source(self, event_id, actor, source):
        source = json.loads(canonical(source))
        def change():
            for field in ("source_id", "version", "locator", "observed_at"):
                _text(source.get(field), field)
            if set(source) != {"source_id", "version", "sha256", "observed_at", "locator"}:
                raise ValueError("unexpected or missing source fields")
            if not re.fullmatch(r"[a-f0-9]{64}", source.get("sha256", "")):
                raise ValueError("source SHA256 must be lowercase hexadecimal")
            when = _instant(source["observed_at"])
            added = self._immutable("source", _key(_ref({k: source[k] for k in
                                        ("source_id", "version")})), source)
            if added:
                head = self.db.execute("SELECT version FROM source_heads WHERE source_id=?",
                                       (source["source_id"],)).fetchone()
                if head:
                    old = self._source({"source_id": source["source_id"], "version": head[0]})
                    previous = _instant(old["observed_at"])
                    if when == previous:
                        raise Conflict("same observation time with another source version")
                    advance = when > previous
                else:
                    advance = True
                if advance:
                    self.db.execute("INSERT INTO source_heads VALUES(?,?) ON CONFLICT(source_id) "
                                    "DO UPDATE SET version=excluded.version",
                                    (source["source_id"], source["version"]))
            return {"source_ref": {k: source[k] for k in ("source_id", "version")},
                    "inserted": added}
        return self._event(event_id, actor, "source_intake", source, "source_intake", change)

    def _source(self, ref):
        return self._get("source", _key(_ref(ref)))

    def _manifest(self, refs):
        unique = {_key(_ref(r)): _ref(r) for r in refs}
        return [{**unique[k], "sha256": self._source(unique[k])["sha256"]}
                for k in sorted(unique)]

    def _assert_sources_current(self, manifest):
        for ref in manifest:
            source_ref = {k: ref[k] for k in ("source_id", "version")}
            source = self._source(source_ref)
            head = self.db.execute("SELECT version FROM source_heads WHERE source_id=?",
                                   (ref["source_id"],)).fetchone()
            if not head or head[0] != ref["version"] or source["sha256"] != ref["sha256"]:
                raise Blocked(f"source revision drift: {ref['source_id']}")

    def intake_quote(self, event_id, actor, quote):
        quote = json.loads(canonical(quote))
        def change():
            expected = {"quote_id", "supplier_id", "item_code", "variant_id", "unit",
                        "currency", "basis", "price", "valid_from", "valid_until", "source_ref"}
            if set(quote) != expected:
                raise ValueError("unexpected or missing quote fields; unknown values must be null")
            for k in ("quote_id", "supplier_id", "variant_id"):
                _text(quote[k], k)
            if quote["item_code"] is not None:
                _text(quote["item_code"], "item_code")
            self._variant_for(quote)
            self._source(quote["source_ref"])
            added = self._immutable("quote", quote["quote_id"], quote)
            return {"quote_id": quote["quote_id"], "inserted": added}
        return self._event(event_id, actor, "quote_intake", quote, "quote_intake", change)

    def intake_requirement(self, event_id, actor, requirement, expected_previous_version=None):
        requirement = json.loads(canonical(requirement))
        def change():
            fields = {"package_id", "requirement_id", "version", "item_code", "variant_id",
                      "unit", "source_ref", "destination"}
            if set(requirement) != fields:
                raise ValueError("unexpected or missing requirement fields")
            for k in ("package_id", "requirement_id", "version", "variant_id"):
                _text(requirement[k], k)
            if requirement["item_code"] is not None:
                _text(requirement["item_code"], "item_code")
            self.case_status(requirement["package_id"])
            self._variant_for(requirement)
            self._source(requirement["source_ref"])
            key = [requirement[k] for k in ("package_id", "requirement_id", "version")]
            added = self._immutable("requirement", _key(key), requirement)
            if added:
                head = self.db.execute("SELECT version FROM requirement_heads WHERE package_id=? AND requirement_id=?",
                                       tuple(key[:2])).fetchone()
                previous = head[0] if head else None
                if previous != expected_previous_version:
                    raise Conflict("requirement head changed; explicit expected_previous_version required")
                self.db.execute("INSERT INTO requirement_heads VALUES(?,?,?) ON CONFLICT(package_id,requirement_id) "
                                "DO UPDATE SET version=excluded.version", tuple(key))
            return {"requirement_key": key, "inserted": added}
        return self._event(event_id, actor, "requirement_intake",
                           {"requirement": requirement, "expected_previous_version": expected_previous_version},
                           "requirement_intake", change)

    def _assert_requirement_current(self, key):
        row = self.db.execute("SELECT version FROM requirement_heads WHERE package_id=? AND requirement_id=?",
                              tuple(key[:2])).fetchone()
        if not row or row[0] != key[2]:
            raise Blocked("requirement revision drift")

    def qualify(self, requirement_key, quote_id, evidence, checks=None):
        """Read-only inspection; missing or negative evidence remains a blocker.

        Optional fixture checks (certificate/portfolio) are pinned with their source refs.
        """
        req = self._get("requirement", _key(requirement_key))
        quote = self._get("quote", quote_id)
        if not isinstance(evidence, dict) or set(evidence) != {"goods", "documents", "money"}:
            raise ValueError("evidence must specify exactly goods/documents/money")
        evidence = json.loads(canonical(evidence))
        blockers = []
        case = self.case_status(req["package_id"])
        if case["status"] != "active":
            blockers.append("case_prebid_inactive")
        if case["timeline_status"] == "overdue_unknown":
            blockers.append("case_deadline_overdue_unknown")
        variant = self._get("variant", req["variant_id"])
        if not variant["identity_complete"]:
            blockers.append("normalized_identity_incomplete")
        refs = [req["source_ref"], quote["source_ref"]]
        axes = {}
        for axis in ("goods", "documents", "money"):
            obj = evidence[axis]
            if obj is None:
                axes[axis] = False
                blockers.append(f"{axis}_evidence_missing")
                continue
            if not isinstance(obj, dict) or set(obj) != {"ref", "source_ref"}:
                raise ValueError("evidence object requires ref and source_ref")
            _text(obj["ref"], "evidence.ref")
            refs.append(_ref(obj["source_ref"]))
            axes[axis] = True
        check_results, check_blockers, check_refs = self._run_checks(checks)
        blockers.extend(check_blockers)
        manifest = self._manifest(refs + check_refs)
        try:
            self._assert_sources_current(manifest)
            self._assert_requirement_current(requirement_key)
        except Blocked as error:
            blockers.append(str(error))
        if req["item_code"] is None or quote["item_code"] is None:
            blockers.append("item_code_unknown")
        elif req["item_code"] != quote["item_code"]:
            blockers.append("item_code_mismatch")
        if req["variant_id"] != quote["variant_id"]:
            blockers.append("variant_mismatch")
        if not req["unit"] or not quote["unit"]:
            blockers.append("unit_unknown")
        elif req["unit"] != quote["unit"]:
            blockers.append("unit_mismatch")
        quote_variant = self._get("variant", quote["variant_id"])
        for identity_variant in (variant, quote_variant):
            blockers.extend(self._identity_date_blockers(identity_variant))
        if (req["unit"] and variant["unit"] and req["unit"] != variant["unit"]
                or quote["unit"] and quote_variant["unit"] and quote["unit"] != quote_variant["unit"]):
            blockers.append("normalized_unit_conflict")
        if not req["destination"]:
            blockers.append("destination_mapping_missing")
        if quote["currency"] not in {"USD", "VND", "THB", "CNY", "LAK"}:
            blockers.append("currency_unknown_or_unsupported")
        if not isinstance(quote["basis"], str) or not quote["basis"].strip():
            blockers.append("price_basis_unknown")
        try:
            price = Decimal(quote["price"]) if isinstance(quote["price"], str) else None
            if price is None or not price.is_finite() or price < 0:
                raise InvalidOperation()
        except (InvalidOperation, ValueError):
            blockers.append("price_unknown_or_invalid")
        blockers.extend(self._quote_date_blockers(quote))
        body = {"schema": "bidops-candidate/1", "requirement_key": requirement_key,
                "requirement": req, "quote": quote, "evidence": evidence,
                "axes": axes, "source_manifest": manifest,
                "case_snapshot_sha256": case["snapshot_sha256"],
                "assessment_checks": check_results,
                "business_assessments": _business_assessments(check_results),
                "case_epoch": self._case_epoch(req["package_id"]),
                "as_of": self.now().date().isoformat(), "blockers": sorted(set(blockers)),
                "status": "blocked" if blockers else "needs_review",
                "business_authorization": "not_attested"}
        return {**body, "candidate_hash": digest(body)}

    def _run_checks(self, checks):
        """Fixture certificate/portfolio checks; results are evidence, never approval."""
        results, blockers, refs = {"certificate": None, "portfolio": None}, [], []
        if checks is None:
            return results, blockers, refs
        if not isinstance(checks, dict) or not set(checks) <= {"certificate", "portfolio"}:
            raise ValueError("checks may only contain certificate and/or portfolio")
        today = self.now().date().isoformat()
        if checks.get("certificate") is not None:
            item = checks["certificate"]
            if not isinstance(item, dict) or set(item) != {"required", "certificate", "source_ref"}:
                raise ValueError("certificate check requires required, certificate and source_ref")
            refs.append(_ref(item["source_ref"]))
            result = certificate_check(item["required"], item["certificate"], as_of=today)
            if result["identity_state"] != "matched_identity_only":
                blockers.append("certificate_" + result["identity_state"])
            blockers.extend(f"certificate_{axis}_expired" for axis, state in result["expiry_axes"].items()
                            if state == "expired_in_fixture")
            if result["registry_snapshot_state"] == "future_invalid":
                blockers.append("certificate_registry_snapshot_future_invalid")
            results["certificate"] = result
        if checks.get("portfolio") is not None:
            item = checks["portfolio"]
            if not isinstance(item, dict) or set(item) != {"resources", "allocations", "costs", "source_ref"}:
                raise ValueError("portfolio check requires resources, allocations, costs and source_ref")
            refs.append(_ref(item["source_ref"]))
            result = portfolio_check(item["resources"], item["allocations"], item["costs"])
            blockers.extend(sorted({"portfolio_" + issue["reason"] for issue in result["issues"]}))
            results["portfolio"] = result
        return results, blockers, refs

    def _quote_date_blockers(self, quote):
        if not quote["valid_from"] or not quote["valid_until"]:
            return ["quote_validity_unknown"]
        try:
            start, end = date.fromisoformat(quote["valid_from"]), date.fromisoformat(quote["valid_until"])
        except (ValueError, TypeError):
            return ["quote_validity_invalid"]
        if start > end:
            return ["quote_validity_invalid"]
        today = self.now().date()
        return ["quote_not_current"] if not start <= today <= end else []

    def _identity_date_blockers(self, variant):
        start, end = variant["identity_valid_from"], variant["identity_valid_until"]
        if start is None or end is None:
            return ["identity_validity_unknown"]
        try:
            start, end = date.fromisoformat(start), date.fromisoformat(end)
        except (ValueError, TypeError):
            return ["identity_validity_invalid"]
        if start > end:
            return ["identity_validity_invalid"]
        return [] if start <= self.now().date() <= end else ["identity_validity_not_current"]

    def issue_mission(self, event_id, actor, mission):
        mission = json.loads(canonical(mission))
        def change():
            fields = {"mission_id", "node_id", "requirement_key", "quote_ids",
                      "source_manifest", "deadline", "expected_output"}
            if set(mission) != fields:
                raise ValueError("mission requires exact scoped contract fields")
            for k in ("mission_id", "node_id", "deadline", "expected_output"):
                _text(mission[k], k)
            if mission["node_id"] not in self.nodes:
                raise ValueError("unknown target owned node")
            if _instant(mission["deadline"]) <= self.now():
                raise Blocked("mission deadline already reached")
            key = mission["requirement_key"]
            req = self._get("requirement", _key(key))
            self._assert_requirement_current(key)
            if self.case_status(req["package_id"])["status"] != "active":
                raise Blocked("case is not active for prebid mission")
            if not self.prebid_demand_active(key):
                raise Blocked("no active prebid demand for scoped requirement")
            if not isinstance(mission["quote_ids"], list) or not mission["quote_ids"]:
                raise ValueError("explicit nonempty quote scope required")
            refs = [req["source_ref"]] + [self._get("quote", q)["source_ref"] for q in mission["quote_ids"]]
            expected = self._manifest(refs)
            supplied = self._manifest(mission["source_manifest"])
            if not all(ref in supplied for ref in expected):
                raise Blocked("mission manifest omits scoped source")
            self._assert_sources_current(supplied)
            stored = {**mission, "source_manifest": supplied, "issued_by": actor,
                      "case_epoch": self._case_epoch(req["package_id"])}
            if not self._immutable("mission", mission["mission_id"], stored):
                raise Conflict("mission already issued; retry the original event_id")
            self.db.execute("INSERT INTO mission_state VALUES(?,?,NULL)", (mission["mission_id"], "issued"))
            return {"mission_id": mission["mission_id"], "status": "issued"}
        return self._event(event_id, actor, "mission_issue", mission, "mission_issue", change)

    def _owned_mission(self, actor, mission_id, require_current=True):
        mission = self._get("mission", mission_id)
        if actor["node_id"] != mission["node_id"]:
            raise Forbidden("mission belongs to another owned node")
        if require_current:
            self._assert_sources_current(mission["source_manifest"])
            self._assert_requirement_current(mission["requirement_key"])
            if self.case_status(mission["requirement_key"][0])["status"] != "active":
                raise Blocked("case is not active for prebid mission")
            if not self.prebid_demand_active(mission["requirement_key"]):
                raise Blocked("no active prebid demand for scoped requirement")
            if self.now() >= _instant(mission["deadline"]):
                raise Blocked("mission deadline reached; explicit reissue required")
            if mission.get("case_epoch", 0) != self._case_epoch(mission["requirement_key"][0]):
                raise Blocked("case reopened after mission issue; explicit reissue required")
        state = self.db.execute("SELECT * FROM mission_state WHERE mission_id=?", (mission_id,)).fetchone()
        return mission, state

    def receive_mission(self, event_id, actor, mission_id):
        def change():
            _, state = self._owned_mission(actor, mission_id)
            if state["status"] != "issued":
                raise Blocked("mission is not awaiting receipt")
            self.db.execute("UPDATE mission_state SET status='received' WHERE mission_id=?", (mission_id,))
            return {"mission_id": mission_id, "status": "received"}
        return self._event(event_id, actor, "mission_receive", {"mission_id": mission_id},
                           "mission_receive", change)

    def respond_mission(self, event_id, actor, mission_id, response, evidence_ref):
        """Transport receipt is separate from accepting responsibility for work."""
        payload = {"mission_id": mission_id, "response": response, "evidence_ref": evidence_ref}
        def change():
            if response not in {"accepted", "needs_input", "rejected"}:
                raise ValueError("explicit accepted/needs_input/rejected response required")
            _text(evidence_ref, "mission response evidence_ref")
            mission, state = self._owned_mission(actor, mission_id, response == "accepted")
            if state["status"] not in {"received", "needs_input"}:
                raise Blocked("mission response requires a received, unresolved mission")
            if response == "accepted":
                for row in self.db.execute("SELECT m.mission_id,o.payload FROM mission_state m "
                                           "JOIN objects o ON o.key=m.mission_id AND o.kind='mission' "
                                           "WHERE m.status='accepted'"):
                    if json.loads(row["payload"])["node_id"] == mission["node_id"]:
                        raise Blocked("pilot WIP=1: return or cancel existing accepted mission first")
            self.db.execute("UPDATE mission_state SET status=? WHERE mission_id=?", (response, mission_id))
            return {"mission_id": mission_id, "status": response}
        return self._event(event_id, actor, "mission_response", payload, "mission_accept", change)

    def cancel_mission(self, event_id, actor, mission_id, evidence_ref):
        payload = {"mission_id": mission_id, "evidence_ref": evidence_ref}
        def change():
            _text(evidence_ref, "mission cancellation evidence_ref")
            mission = self._get("mission", mission_id)
            if actor["owner_id"] != mission["issued_by"]["owner_id"]:
                raise Forbidden("only issuing owner may cancel this pilot mission")
            state = self.db.execute("SELECT * FROM mission_state WHERE mission_id=?", (mission_id,)).fetchone()
            if state["status"] == "cancelled":
                raise Blocked("mission already cancelled; retry original event_id")
            self.db.execute("UPDATE mission_state SET status='cancelled' WHERE mission_id=?", (mission_id,))
            return {"mission_id": mission_id, "status": "cancelled", "previous_status": state["status"],
                    "candidate_id_preserved": state["candidate_id"], "automatic_undo": False}
        return self._event(event_id, actor, "mission_cancel", payload, "mission_cancel", change)

    def return_mission(self, event_id, actor, mission_id, quote_id, evidence, checks=None):
        payload = {"mission_id": mission_id, "quote_id": quote_id, "evidence": evidence}
        if checks is not None:
            # Present only when used, so earlier events keep their exact retry digest.
            payload["checks"] = checks
        def change():
            mission, state = self._owned_mission(actor, mission_id)
            if state["status"] != "accepted":
                raise Blocked("mission must be explicitly accepted before return")
            if quote_id not in mission["quote_ids"]:
                raise Forbidden("quote outside immutable mission scope")
            candidate = self.qualify(mission["requirement_key"], quote_id, evidence, checks)
            if not all(ref in mission["source_manifest"] for ref in candidate["source_manifest"]):
                raise Forbidden("evidence source outside immutable mission manifest")
            candidate.pop("candidate_hash")
            candidate.update({"proposer": actor, "mission_id": mission_id})
            candidate_id = digest(candidate)
            candidate["candidate_hash"] = candidate_id
            added = self._immutable("candidate", candidate_id, candidate)
            if added:
                self.db.execute("INSERT INTO candidate_state(candidate_id,status) VALUES(?,?)",
                                (candidate_id, "returned"))
            self.db.execute("UPDATE mission_state SET status='returned',candidate_id=? WHERE mission_id=?",
                            (candidate_id, mission_id))
            return {"mission_id": mission_id, "status": "returned", "candidate": candidate}
        return self._event(event_id, actor, "mission_return", payload, "mission_return", change)

    def _candidate_current(self, candidate_id, expected_hash, require_valid_quote=True):
        candidate = self._get("candidate", candidate_id)
        body = {k: v for k, v in candidate.items() if k != "candidate_hash"}
        if expected_hash != candidate_id or digest(body) != expected_hash:
            raise Conflict("candidate digest mismatch")
        self._assert_sources_current(candidate["source_manifest"])
        self._assert_requirement_current(candidate["requirement_key"])
        mission_state = self.db.execute("SELECT status FROM mission_state WHERE mission_id=?",
                                        (candidate["mission_id"],)).fetchone()
        if mission_state is None or mission_state[0] == "cancelled":
            raise Blocked("candidate mission cancelled; preserved history cannot be newly promoted")
        case = self.case_status(candidate["requirement_key"][0])
        if case["status"] != "active":
            raise Blocked("case is not active for prebid candidate")
        if case["timeline_status"] == "overdue_unknown":
            raise Blocked("case deadline passed without a confirmed disposition or extension")
        if not self.prebid_demand_active(candidate["requirement_key"]):
            raise Blocked("no active prebid demand for candidate")
        if candidate.get("case_snapshot_sha256") != case["snapshot_sha256"]:
            raise Blocked("case snapshot changed after candidate; requalify required")
        if candidate.get("case_epoch", 0) != self._case_epoch(candidate["requirement_key"][0]):
            raise Blocked("case reopened after candidate; review is not inherited")
        if require_valid_quote and self._quote_date_blockers(candidate["quote"]):
            raise Blocked("candidate quote is not currently valid")
        if require_valid_quote:
            for item in (candidate["requirement"], candidate["quote"]):
                variant = self._get("variant", item["variant_id"])
                if self._identity_date_blockers(variant):
                    raise Blocked("candidate identity validity is unknown or not currently valid")
        state = self.db.execute("SELECT * FROM candidate_state WHERE candidate_id=?", (candidate_id,)).fetchone()
        return candidate, state

    def review_candidate(self, event_id, actor, candidate_id, expected_hash, decision, evidence_ref):
        payload = {"candidate_id": candidate_id, "expected_hash": expected_hash,
                   "decision": decision, "evidence_ref": evidence_ref}
        def change():
            _text(evidence_ref, "review evidence_ref")
            if decision not in {"approve", "reject"}:
                raise ValueError("explicit approve/reject decision required")
            candidate, state = self._candidate_current(candidate_id, expected_hash,
                                                       require_valid_quote=decision == "approve")
            if actor["owner_id"] == candidate["proposer"]["owner_id"]:
                raise Forbidden("pilot requires a different reviewing owner")
            if state["status"] != "returned":
                raise Blocked("candidate already reviewed; create a new candidate for a changed proposal")
            if decision == "approve" and candidate["blockers"]:
                raise Blocked("unresolved candidate cannot be approved")
            status = "reviewed" if decision == "approve" else "rejected"
            self.db.execute("UPDATE candidate_state SET status=?,review_event=? WHERE candidate_id=?",
                            (status, event_id, candidate_id))
            return {"candidate_id": candidate_id, "status": status, "decision": decision}
        return self._event(event_id, actor, "candidate_review", payload, "candidate_review", change)

    def _promote(self, event_id, actor, candidate_id, expected_hash, evidence_ref, use):
        kind, previous, status = ("candidate_use", "applied", "used") if use else ("candidate_apply", "reviewed", "applied")
        payload = {"candidate_id": candidate_id, "expected_hash": expected_hash, "evidence_ref": evidence_ref}
        def change():
            _text(evidence_ref, "promotion evidence_ref")
            _, state = self._candidate_current(candidate_id, expected_hash)
            if state["status"] != previous:
                raise Blocked(f"candidate must be {previous} before {status}")
            column = "use_event" if use else "apply_event"
            self.db.execute(f"UPDATE candidate_state SET status=?,{column}=? WHERE candidate_id=?",
                            (status, event_id, candidate_id))
            return {"candidate_id": candidate_id, "status": status,
                    "meaning": "explicit local receipt; no real master write or tender submission"}
        return self._event(event_id, actor, kind, payload, kind, change)

    def apply_candidate(self, event_id, actor, candidate_id, expected_hash, evidence_ref):
        return self._promote(event_id, actor, candidate_id, expected_hash, evidence_ref, False)

    def use_candidate(self, event_id, actor, candidate_id, expected_hash, evidence_ref):
        return self._promote(event_id, actor, candidate_id, expected_hash, evidence_ref, True)

    def consume_diagnostic(self, event_id, actor, candidate_id, expected_hash, evidence_ref):
        """Record useful HOLD consumption, never approval/application/commercial use."""
        payload = {"candidate_id": candidate_id, "expected_hash": expected_hash,
                   "evidence_ref": evidence_ref, "output_status": "HOLD"}
        def change():
            _text(evidence_ref, "diagnostic consumer evidence_ref")
            candidate, state = self._candidate_current(candidate_id, expected_hash, False)
            if not candidate["blockers"] or state["status"] != "returned":
                raise Blocked("diagnostic HOLD requires an unresolved returned candidate")
            if actor["owner_id"] == candidate["proposer"]["owner_id"]:
                raise Forbidden("diagnostic consumption needs a different downstream owner")
            return {"candidate_id": candidate_id, "output_status": "HOLD",
                    "used_in_candidate": evidence_ref, "commercial_use": False,
                    "candidate_status_unchanged": "returned"}
        return self._event(event_id, actor, "candidate_diagnostic_use", payload,
                           "candidate_diagnostic_use", change)

    def candidate(self, candidate_id):
        candidate = self._get("candidate", candidate_id)
        state = dict(self.db.execute("SELECT * FROM candidate_state WHERE candidate_id=?", (candidate_id,)).fetchone())
        try:
            self._candidate_current(candidate_id, candidate_id)
            current, reason = True, None
        except Blocked as error:
            current, reason = False, str(error)
        return {"candidate": candidate, "state": state,
                "current": current, "current_blocker": reason}

    def package_view(self, package_id):
        rows = self.db.execute("SELECT requirement_id,version FROM requirement_heads WHERE package_id=? ORDER BY requirement_id",
                               (package_id,)).fetchall()
        return [self._get("requirement", _key([package_id, r[0], r[1]])) for r in rows]

    def event_receipt(self, event_id):
        row = self.db.execute("SELECT receipt FROM events WHERE event_id=?", (event_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def counts(self):
        kinds = {r[0]: r[1] for r in self.db.execute("SELECT kind,count(*) FROM objects GROUP BY kind")}
        return {**kinds, "events": self.db.execute("SELECT count(*) FROM events").fetchone()[0]}

    def metric_snapshot(self):
        states = self.db.execute("SELECT * FROM candidate_state").fetchall()
        diagnostics = set()
        for row in self.db.execute("SELECT envelope FROM events"):
            event = json.loads(row[0])
            if event["type"] == "candidate_diagnostic_use":
                diagnostics.add(event["payload"]["candidate_id"])
        return {"window": "all persisted pilot events", "grain": "unique candidate_id",
                "reviewed": sum(bool(r["review_event"]) for r in states),
                "applied": sum(bool(r["apply_event"]) for r in states),
                "commercial_used": sum(bool(r["use_event"]) for r in states),
                "diagnostic_hold_used": len(diagnostics),
                "meaning": "synthetic local receipts, not valid quotes/day or live procurement adoption"}

    def intake_variant(self, event_id, actor, variant):
        """Canonical synthetic identity; incomplete variants are never auto-merged."""
        variant = json.loads(canonical(variant))
        return self._event(event_id, actor, "variant_intake", variant, "catalog_intake",
                           lambda: self._store_variant(variant))

    def intake_bridged_variant(self, event_id, actor, bridged):
        """Variant from an explicit reviewed catalog line resolution, with its provenance.

        Only a BRIDGED record is accepted; HOLD/unresolved lines never become variants.
        """
        bridged = json.loads(canonical(bridged))
        def change():
            if not isinstance(bridged, dict) or bridged.get("status") != "BRIDGED":
                raise ValueError("only a BRIDGED catalog resolution can become a ledger variant")
            variant, provenance = bridged.get("variant"), bridged.get("provenance")
            if not isinstance(variant, dict) or not isinstance(provenance, dict):
                raise ValueError("bridged variant and provenance are required")
            if provenance.get("mapping") != "explicit_reviewed_line_resolution":
                raise ValueError("only explicit reviewed line resolution is accepted")
            for key in ("catalog_variant_id", "catalog_identity_sha256", "resolution_evidence_ref",
                        "reviewed_by", "line_id", "source_version"):
                _text(provenance.get(key), "provenance." + key)
            if provenance["catalog_variant_id"] != variant.get("variant_id"):
                raise Conflict("provenance does not describe this variant")
            result = self._store_variant(variant)
            record = {**provenance, "flags": bridged.get("flags") or []}
            # One variant may be resolved from several case lines; provenance is per line.
            if not self._immutable("variant_provenance", provenance["line_id"], record):
                raise Conflict("variant already bridged with this provenance; retry original event_id")
            return {**result, "provenance_mapping": provenance["mapping"]}
        return self._event(event_id, actor, "variant_bridge", bridged, "catalog_intake", change)

    def _store_variant(self, variant):
        fields = {"variant_id", "item_code", "specification", "unit",
                  "registration_id", "identity_valid_from", "identity_valid_until"}
        if not isinstance(variant, dict) or set(variant) != fields:
            raise ValueError("normalized variant fields required; unknown is null")
        _text(variant["variant_id"], "variant_id")
        if variant["item_code"] is not None:
            _text(variant["item_code"], "item_code")
        spec = variant["specification"]
        if spec is not None and (not isinstance(spec, dict) or any(
                not isinstance(k, str) or not isinstance(v, str) or not v.strip()
                for k, v in spec.items())):
            raise ValueError("specification is null or a string-to-string object")
        for field in fields - {"variant_id", "item_code", "specification"}:
            if variant[field] is not None:
                _text(variant[field], field)
        for field in ("identity_valid_from", "identity_valid_until"):
            if variant[field] is not None:
                try:
                    date.fromisoformat(variant[field])
                except (ValueError, TypeError) as error:
                    raise ValueError(f"{field} must be an ISO date or null") from error
        if (variant["identity_valid_from"] and variant["identity_valid_until"]
                and variant["identity_valid_from"] > variant["identity_valid_until"]):
            raise ValueError("identity validity range is reversed")
        complete = bool(variant["item_code"] and spec and variant["unit"])
        identity = {k: v for k, v in variant.items() if k != "variant_id"}
        identity_hash = digest(identity if complete else variant)
        stored = {**variant, "identity_hash": identity_hash, "identity_complete": complete}
        added = self._immutable("variant", variant["variant_id"], stored)
        if added:
            old = self.db.execute("SELECT variant_id FROM variant_identity WHERE identity_hash=?",
                                  (identity_hash,)).fetchone()
            if old:
                raise Conflict(f"identity already has canonical variant_id: {old[0]}")
            self.db.execute("INSERT INTO variant_identity VALUES(?,?)", (identity_hash, variant["variant_id"]))
        return {"variant_id": variant["variant_id"], "identity_complete": complete, "inserted": added}

    def _variant_for(self, item):
        variant = self._get("variant", item["variant_id"])
        if item["item_code"] != variant["item_code"]:
            raise Conflict("item code differs from registered variant")
        if item["unit"] is not None and not isinstance(item["unit"], str):
            raise ValueError("unit must be a string or null")
        # A wrong supplier UOM is retained for qualification to reject explicitly.
        return variant

    def create_case(self, event_id, actor, case_id, title, deadline=None):
        payload = {"case_id": case_id, "title": title, "deadline": deadline}
        def change():
            _text(case_id, "case_id")
            _text(title, "title")
            if deadline is not None:
                _instant(deadline)
            if not self._immutable("tender_case", case_id, payload):
                raise Conflict("case already exists; retry its original event_id")
            self.db.execute("INSERT INTO case_state VALUES(?,?,?,NULL)", (case_id, "active", deadline))
            return {"case_id": case_id, "status": "active"}
        return self._event(event_id, actor, "case_create", payload, "case_manage", change)

    def _case_epoch(self, case_id):
        """Each explicit reopen starts a new scope; earlier reviews/missions are history."""
        return self.db.execute(
            "SELECT count(*) FROM events WHERE json_extract(envelope,'$.type')='case_transition' "
            "AND json_extract(envelope,'$.payload.case_id')=? "
            "AND json_extract(envelope,'$.payload.action')='reopen'", (case_id,)).fetchone()[0] + self.db.execute(
            "SELECT count(*) FROM events WHERE json_extract(envelope,'$.type')='case_snapshot_adopt' "
            "AND json_extract(receipt,'$.result.case_id')=? "
            "AND json_extract(receipt,'$.result.case_reopened')=1", (case_id,)).fetchone()[0]

    def case_status(self, case_id):
        self._get("tender_case", case_id)
        state = dict(self.db.execute("SELECT * FROM case_state WHERE case_id=?", (case_id,)).fetchone())
        bound = self.db.execute("SELECT snapshot_sha256,planning_date FROM case_authority WHERE case_id=?",
                                (case_id,)).fetchone()
        state["authority"] = "catalog_snapshot" if bound else "ledger"
        state["snapshot_sha256"] = bound[0] if bound else None
        state["planning_date"] = bound[1] if bound else None
        # Neither a legal closing instant nor a planning date closes a case by itself.
        passed = (state["deadline"] and self.now() > _instant(state["deadline"])
                  or state["planning_date"] and self.now().date() > date.fromisoformat(state["planning_date"]))
        state["timeline_status"] = "overdue_unknown" if state["status"] == "active" and passed else state["status"]
        return state

    def _ledger_owned_case(self, case_id):
        state = self.case_status(case_id)
        if state["authority"] != "ledger":
            raise Blocked("case authority is the catalog snapshot; adopt a newer snapshot instead")
        return state

    def adopt_case_snapshot(self, event_id, actor, snapshot, expected_previous_sha256):
        """Project one catalog CaseSnapshot into the ledger; the catalog stays the case authority."""
        snapshot = json.loads(canonical(snapshot))
        payload = {"snapshot": snapshot, "expected_previous_sha256": expected_previous_sha256}
        def change():
            keys = {"schema", "case_id", "status", "planning_date", "official_closing_at", "source_status",
                    "active_source_version", "closure_policy", "lifecycle_events", "snapshot_sha256"}
            if not isinstance(snapshot, dict) or set(snapshot) != keys or snapshot["schema"] != "bidops-case-snapshot/1":
                raise ValueError("bidops-case-snapshot/1 fields required")
            body = {k: v for k, v in snapshot.items() if k != "snapshot_sha256"}
            if digest(body) != snapshot["snapshot_sha256"]:
                raise ValueError("case snapshot hash mismatch")
            case_id = _text(snapshot["case_id"], "case_id")
            if snapshot["status"] not in {"active", "closed", "cancelled", "won"}:
                raise ValueError("unknown catalog case status")
            if snapshot["planning_date"] is not None:
                date.fromisoformat(snapshot["planning_date"])
            if snapshot["official_closing_at"] is not None:
                _instant(snapshot["official_closing_at"])
            current = self.db.execute("SELECT snapshot_sha256,snapshot FROM case_authority WHERE case_id=?",
                                      (case_id,)).fetchone()
            if (current[0] if current else None) != expected_previous_sha256:
                raise Conflict("case snapshot head changed; explicit expected_previous_sha256 required")
            if current:
                # Catalog lifecycle history only grows; an older or diverged snapshot cannot roll back.
                seen = json.loads(current[1])["lifecycle_events"]
                if snapshot["lifecycle_events"][:len(seen)] != seen:
                    raise Conflict("case snapshot is older than or diverges from the adopted head")
            exists = self.db.execute("SELECT status FROM case_state WHERE case_id=?", (case_id,)).fetchone()
            if not exists:
                self._immutable("tender_case", case_id, {"case_id": case_id, "title": None, "deadline": None,
                                                         "authority": "catalog_snapshot"})
                self.db.execute("INSERT INTO case_state VALUES(?,?,?,NULL)", (case_id, "active", None))
            previous = exists[0] if exists else None
            reopened = previous is not None and previous != "active" and snapshot["status"] == "active"
            self.db.execute("UPDATE case_state SET status=?,deadline=? WHERE case_id=?",
                            (snapshot["status"], snapshot["official_closing_at"], case_id))
            self.db.execute("INSERT INTO case_authority VALUES(?,?,?,?) ON CONFLICT(case_id) DO UPDATE SET "
                            "snapshot_sha256=excluded.snapshot_sha256,planning_date=excluded.planning_date,"
                            "snapshot=excluded.snapshot",
                            (case_id, snapshot["snapshot_sha256"], snapshot["planning_date"], canonical(snapshot)))
            return {"case_id": case_id, "status": snapshot["status"], "previous_status": previous,
                    "snapshot_sha256": snapshot["snapshot_sha256"], "case_reopened": reopened,
                    "official_closing_at": snapshot["official_closing_at"], "authority": "catalog_snapshot"}
        return self._event(event_id, actor, "case_snapshot_adopt", payload, "case_manage", change)

    def transition_case(self, event_id, actor, case_id, action, reason):
        payload = {"case_id": case_id, "action": action, "reason": reason}
        def change():
            _text(reason, "case transition reason")
            state = self._ledger_owned_case(case_id)
            target = {"close": "closed", "cancel": "cancelled", "reopen": "active", "win": "won"}.get(action)
            if target is None:
                raise ValueError("explicit close/cancel/reopen/win required")
            if action == "reopen" and state["status"] == "active":
                raise Blocked("case already active")
            if action != "reopen" and state["status"] != "active":
                raise Blocked("explicitly reopen before another case disposition")
            self.db.execute("UPDATE case_state SET status=? WHERE case_id=?", (target, case_id))
            return {"case_id": case_id, "status": target}
        return self._event(event_id, actor, "case_transition", payload, "case_manage", change)

    def set_case_deadline(self, event_id, actor, case_id, deadline, reason):
        payload = {"case_id": case_id, "deadline": deadline, "reason": reason}
        def change():
            _instant(deadline)
            _text(reason, "deadline change reason")
            state = self._ledger_owned_case(case_id)
            self.db.execute("UPDATE case_state SET deadline=? WHERE case_id=?", (deadline, case_id))
            result = {"case_id": case_id, "deadline": deadline, "previous_deadline": state["deadline"],
                      "status": state["status"], "semantics": "correction"}
            if state["deadline"] and _instant(deadline) < _instant(state["deadline"]):
                # Recorded as fact; whether earlier corrections need extra approval is not decided.
                result["backward_correction_policy"] = "pending_business_decision"
            return result
        return self._event(event_id, actor, "case_deadline_changed", payload, "case_manage", change)

    def extend_case_deadline(self, event_id, actor, case_id, deadline, evidence_ref):
        """Extension (CL semantics): strictly later than the current deadline."""
        payload = {"case_id": case_id, "deadline": deadline, "evidence_ref": evidence_ref}
        def change():
            new = _instant(deadline)
            _text(evidence_ref, "extension evidence_ref")
            state = self._ledger_owned_case(case_id)
            if state["deadline"] and new <= _instant(state["deadline"]):
                raise ValueError("extension must be later than the current deadline")
            self.db.execute("UPDATE case_state SET deadline=? WHERE case_id=?", (deadline, case_id))
            return {"case_id": case_id, "deadline": deadline, "previous_deadline": state["deadline"],
                    "status": state["status"], "semantics": "extension"}
        return self._event(event_id, actor, "case_deadline_extended", payload, "case_manage", change)

    def plan_case_closure(self, event_id, actor, case_id, planned_at, reason):
        payload = {"case_id": case_id, "planned_at": planned_at, "reason": reason}
        def change():
            _instant(planned_at)
            _text(reason, "planned closure reason")
            state = self._ledger_owned_case(case_id)
            self.db.execute("UPDATE case_state SET planned_closure=? WHERE case_id=?", (planned_at, case_id))
            return {"case_id": case_id, "planned_closure": planned_at, "status": state["status"]}
        return self._event(event_id, actor, "case_closure_planned", payload, "case_manage", change)

    def link_demand(self, event_id, actor, link):
        link = json.loads(canonical(link))
        def change():
            if set(link) != {"link_id", "requirement_key", "need_type", "quantity"}:
                raise ValueError("demand link fields required")
            _text(link["link_id"], "link_id")
            req = self._get("requirement", _key(link["requirement_key"]))
            case = self.case_status(req["package_id"])
            if link["need_type"] not in {"prebid_sourcing", "fulfillment"}:
                raise ValueError("explicit need_type required")
            if link["need_type"] == "fulfillment" and case["status"] != "won":
                raise Blocked("fulfillment demand requires an explicitly won case")
            if link["quantity"] is not None:
                try:
                    quantity = Decimal(link["quantity"]) if isinstance(link["quantity"], str) else None
                    if quantity is None or not quantity.is_finite() or quantity <= 0:
                        raise InvalidOperation()
                except (InvalidOperation, ValueError):
                    raise ValueError("quantity must be null (unknown) or a positive decimal string")
            if not self._immutable("demand_link", link["link_id"], link):
                raise Conflict("demand link exists; retry original event_id")
            self.db.execute("INSERT INTO demand_state VALUES(?,?)", (link["link_id"], "open"))
            return {"link_id": link["link_id"], "status": "open",
                    "case_status": self.case_status(req["package_id"])["status"]}
        return self._event(event_id, actor, "demand_link", link, "case_manage", change)

    def finish_demand(self, event_id, actor, link_id, disposition, reason):
        payload = {"link_id": link_id, "disposition": disposition, "reason": reason}
        def change():
            self._get("demand_link", link_id)
            _text(reason, "demand disposition reason")
            if disposition not in {"fulfilled", "cancelled"}:
                raise ValueError("explicit fulfilled/cancelled required")
            state = self.db.execute("SELECT status FROM demand_state WHERE link_id=?", (link_id,)).fetchone()
            if state[0] != "open":
                raise Blocked("demand already disposed")
            self.db.execute("UPDATE demand_state SET status=? WHERE link_id=?", (disposition, link_id))
            return {"link_id": link_id, "status": disposition}
        return self._event(event_id, actor, "demand_disposition", payload, "case_manage", change)

    def active_worklist(self):
        """Derived view only. No source/quote/history deletion or case auto-close."""
        groups = {}
        rows = self.db.execute("SELECT o.payload FROM objects o JOIN demand_state d ON o.key=d.link_id "
                               "WHERE o.kind='demand_link' AND d.status='open' ORDER BY o.key").fetchall()
        for row in rows:
            link = json.loads(row[0])
            req = self._get("requirement", _key(link["requirement_key"]))
            case = self.case_status(req["package_id"])
            if link["need_type"] == "prebid_sourcing" and case["status"] != "active":
                continue
            variant = self._get("variant", req["variant_id"])
            key = (variant["variant_id"], link["need_type"])
            group = groups.setdefault(key, {"variant": variant, "need_type": link["need_type"],
                                            "known_quantity": Decimal(0), "unknown_quantity_count": 0,
                                            "stale_demand_count": 0, "demand_links": []})
            flags = []
            if not variant["identity_complete"]:
                flags.append("normalized_identity_incomplete")
            if not req["destination"]:
                flags.append("destination_mapping_missing")
            try:
                self._assert_requirement_current(link["requirement_key"])
                self._assert_sources_current(self._manifest([req["source_ref"]]))
            except Blocked as error:
                flags.append(str(error))
            stale = any("revision drift" in flag for flag in flags)
            if stale:
                group["stale_demand_count"] += 1
            elif link["quantity"] is None:
                group["unknown_quantity_count"] += 1
            else:
                group["known_quantity"] += Decimal(link["quantity"])
            group["demand_links"].append({**link, "case_status": case["status"],
                                         "timeline_status": case["timeline_status"], "current": not stale,
                                         "flags": flags})
        return [{**groups[k], "known_quantity": str(groups[k]["known_quantity"]),
                 "quantity": (None if groups[k]["unknown_quantity_count"] or groups[k]["stale_demand_count"]
                              or not groups[k]["variant"]["identity_complete"] else str(groups[k]["known_quantity"]))}
                for k in sorted(groups)]

    def prebid_demand_active(self, requirement_key):
        """An explicit open demand is required; quote arrival never creates one."""
        req = self._get("requirement", _key(requirement_key))
        if self.case_status(req["package_id"])["status"] != "active":
            return False
        try:
            self._assert_requirement_current(requirement_key)
        except Blocked:
            return False
        rows = self.db.execute("SELECT o.payload FROM objects o JOIN demand_state d ON o.key=d.link_id "
                               "WHERE o.kind='demand_link' AND d.status='open'").fetchall()
        return any((link := json.loads(r[0]))["requirement_key"] == requirement_key
                   and link["need_type"] == "prebid_sourcing" for r in rows)
