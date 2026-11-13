"""Run a fictional end-to-end inspection with one explicit, empty output folder."""
import sys
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

from src.ledger import Blocked
from src.synthetic import FIXED_NOW, actor, evidence, requirement, returned, seed, source


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True,
                        help="new or empty output folder; existing work is never overwritten")
    args = parser.parse_args(argv)
    out = args.out.expanduser().resolve()
    if out == Path(out.anchor):
        parser.error("choose a dedicated output folder, not a filesystem root")
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        parser.error("output folder must be empty; preserve prior results and choose another folder")
    out.mkdir(parents=True, exist_ok=True)
    db_path, json_path, readout_path = out / "pilot.sqlite", out / "RESULT.json", out / "READOUT.md"
    if any(p.resolve().parent != out for p in (db_path, json_path, readout_path)):
        parser.error("output escaped its explicit folder")
    ledger = seed(db_path)
    builder, reviewer = actor("builder"), actor("reviewer")
    result = {"scope": "fictional local pilot; no live procurement operations",
              "clock": FIXED_NOW.isoformat(), "clock_is_fixed_synthetic": True}
    try:
        for case, qty in (("river", "10"), ("hill", "20")):
            ledger.link_demand(f"demand-{case}", builder,
                               {"link_id": f"demand-{case}", "requirement_key": [case, "line-1", "1"],
                                "need_type": "prebid_sourcing", "quantity": qty})
        result["shared_worklist_before"] = ledger.active_worklist()
        mismatch = returned(ledger, "inspect-40-vs-30", quote_id="q40")
        result["mismatch_diagnostic"] = ledger.consume_diagnostic(
            "consumer-hold", reviewer, mismatch, mismatch, "synthetic://consumer/decision-HOLD")
        try:
            ledger.review_candidate("must-not-approve", reviewer, mismatch, mismatch,
                                    "approve", "synthetic://review")
            raise AssertionError("mismatched variant was approved")
        except Blocked as error:
            result["mismatch_approval_blocked"] = str(error)
        a = returned(ledger, "river-inspection")
        b = returned(ledger, "hill-inspection", ["hill", "line-1", "1"])
        ledger.review_candidate("review-river", reviewer, a, a, "approve", "synthetic://reviewer/decision")
        ledger.apply_candidate("apply-river", reviewer, a, a, "synthetic://local-candidate-projection")
        result["metrics_after_apply_before_use"] = ledger.metric_snapshot()
        ledger.use_candidate("use-river", reviewer, a, a, "synthetic://consumer/used-output")
        result["metrics_after_explicit_use"] = ledger.metric_snapshot()
        result["shared_quote_ids"] = [ledger.candidate(c)["candidate"]["quote"]["quote_id"] for c in (a, b)]
        ledger.intake_requirement("unmapped-row", builder,
                                  requirement(requirement_id="unmapped", destination=None))
        gap = returned(ledger, "mapping-gap", ["river", "unmapped", "1"])
        result["mapping_gap_preserved"] = ledger.candidate(gap)["candidate"]["blockers"]
        ledger.intake_source("new-quote-version", builder,
                             source("quote-src", "2", "d", "2026-10-31T13:00:00Z"))
        result["after_source_revision"] = {"river_current": ledger.candidate(a)["current"],
                                            "hill_current": ledger.candidate(b)["current"],
                                            "history_still_used": ledger.candidate(a)["state"]["status"]}
        try:
            ledger.consume_diagnostic("stale-HOLD", reviewer, mismatch, mismatch, "synthetic://consumer/stale")
            raise AssertionError("stale diagnostic was silently reused")
        except Blocked as error:
            result["stale_diagnostic_blocked"] = str(error)
        ledger.transition_case("close-river", builder, "river", "close", "explicit synthetic close")
        result["after_only_river_closed"] = ledger.active_worklist()
        ledger.transition_case("hill-won", builder, "hill", "win", "synthetic award receipt")
        ledger.link_demand("hill-fulfillment", builder,
                           {"link_id": "hill-fulfillment", "requirement_key": ["hill", "line-1", "1"],
                            "need_type": "fulfillment", "quantity": "4"})
        result["won_keeps_fulfillment"] = ledger.active_worklist()
        ledger.transition_case("reopen-river", builder, "river", "reopen", "explicit synthetic reopen")
        result["after_reopen"] = ledger.active_worklist()
        result["persisted_counts"] = ledger.counts()
        result["metrics"] = ledger.metric_snapshot()
        result["not_implemented"] = ["live identity/authentication or staff channel bindings",
            "quote-discovery missions without a predeclared quote scope", "leases/retries across real hosts",
            "production bus/offline queue/backpressure", "real master promotion or tender submission",
            "legal/equivalence/price/stock/capital acceptance"]
        result["separate_readonly_catalog_import"] = "src/catalog_intake.py; actual business intake is not run by this fictional demo"
        json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        readout_path.write_text(
            "# Synthetic BidOps B demo\n\n"
            "Fictional data only; fixed synthetic clock. This is not staff onboarding or procurement acceptance.\n\n"
            "- One shared quote q30 feeds two independently versioned package candidates.\n"
            "- The 40mm quote against a 30mm need returns a mismatch, consumed as HOLD; approval remains blocked.\n"
            "- A missing destination stays visible as an exception.\n"
            "- Review, application, explicit commercial-use receipt and diagnostic-use receipt stay separate.\n"
            "- A quote source revision makes both affected candidates stale without deleting their history.\n"
            "- Closing one case keeps the other case's demand. WON retains fulfillment; reopening restores prebid demand.\n\n"
            "Inspect RESULT.json and pilot.sqlite in this same directory. No real master, messages, network, upload or submission was touched.\n",
            encoding="utf-8")
        print(json.dumps({"output": str(out), "counts": result["persisted_counts"],
                          "metrics": result["metrics"]}, ensure_ascii=True))
    finally:
        ledger.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
