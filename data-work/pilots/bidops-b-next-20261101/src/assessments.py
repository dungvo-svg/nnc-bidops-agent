"""Pure fixture checks; no registry, accounting or procurement authority."""
from datetime import date
from decimal import Decimal, InvalidOperation


def _decimal(value):
    if not isinstance(value, str):
        return None
    try:
        number = Decimal(value)
        return number if number.is_finite() and number >= 0 else None
    except InvalidOperation:
        return None


def certificate_check(required, certificate, *, as_of):
    """Keep identity and expiry axes separate. This does not establish legality."""
    if not isinstance(required, dict) or not isinstance(certificate, dict):
        raise ValueError("explicit product and certificate objects required")
    today = date.fromisoformat(as_of)
    fields = ("trade_name", "manufacturer", "strength", "form", "pack")
    conflicts, unknown = [], []
    product = certificate.get("product")
    product = product if isinstance(product, dict) else {}
    for key in fields:
        expected, observed = required.get(key), product.get(key)
        expected = expected.strip() if isinstance(expected, str) else None
        observed = observed.strip() if isinstance(observed, str) else None
        if not expected or not observed:
            unknown.append(key)
        elif expected != observed:
            conflicts.append(key)
    dates = {}
    for key in ("registration_valid_until", "lot_expiry", "quote_valid_until", "delegation_valid_until"):
        value = certificate.get(key)
        try:
            dates[key] = "current_in_fixture" if date.fromisoformat(value) >= today else "expired_in_fixture"
        except (ValueError, TypeError):
            dates[key] = "unknown"
    registry_as_of = certificate.get("registry_as_of")
    try:
        registry_snapshot = date.fromisoformat(registry_as_of)
        snapshot_state = "future_invalid" if registry_snapshot > today else "historical_snapshot_only"
    except (ValueError, TypeError):
        snapshot_state = "unknown"
    return {"identity_state": "identity_conflict" if conflicts else "identity_unknown" if unknown else "matched_identity_only",
            "conflicting_fields": conflicts, "unknown_fields": unknown,
            "expiry_axes": dates, "registry_as_of": registry_as_of,
            "registry_snapshot_state": snapshot_state, "business_approval": "not_attested",
            "meaning": "fixture data checks only; generic or registration number alone cannot establish product identity"}


def portfolio_check(resources, allocations, costs):
    """Count each commitment/cost once; no currency or EU conversion is inferred."""
    issues, unique_allocations, unique_costs = [], {}, {}
    for row in allocations:
        key = row["allocation_id"]
        if key in unique_allocations and unique_allocations[key] != row:
            raise ValueError("allocation_id reused with different payload")
        unique_allocations[key] = row
    by_resource, unresolved_by_resource = {}, {}
    for row in unique_allocations.values():
        key = row["resource_id"]
        available = resources.get(key)
        quantity = _decimal(row.get("quantity"))
        if available is None:
            issues.append({"resource_id": key, "reason": "resource_unknown"})
            continue
        if not row.get("unit") or row["unit"] != available.get("unit"):
            issues.append({"resource_id": key, "reason": "unit_unknown_or_mismatch"})
            unresolved_by_resource[key] = unresolved_by_resource.get(key, 0) + 1
            continue
        if quantity is None:
            issues.append({"resource_id": key, "reason": "quantity_unknown_or_invalid"})
            unresolved_by_resource[key] = unresolved_by_resource.get(key, 0) + 1
            continue
        by_resource[key] = by_resource.get(key, Decimal(0)) + quantity
    resource_view = []
    for key in sorted(set(by_resource) | set(unresolved_by_resource)):
        allocated = by_resource.get(key, Decimal(0))
        capacity = _decimal(resources[key].get("available"))
        unresolved = unresolved_by_resource.get(key, 0)
        state = ("overcommitted" if capacity is not None and allocated > capacity else
                 "allocation_unknown" if unresolved else "capacity_unknown" if capacity is None else "within_fixture_capacity")
        if state != "within_fixture_capacity":
            issues.append({"resource_id": key, "reason": state})
        resource_view.append({"resource_id": key, "allocated": None if unresolved else str(allocated),
                              "known_allocated": str(allocated), "unresolved_allocation_count": unresolved,
                              "available": None if capacity is None else str(capacity),
                              "unit": resources[key]["unit"], "state": state})
    for row in costs:
        key = row["cost_id"]
        if key in unique_costs and unique_costs[key] != row:
            raise ValueError("cost_id reused with different payload")
        unique_costs[key] = row
    totals = {}
    for row in unique_costs.values():
        amount, currency = _decimal(row.get("amount")), row.get("currency")
        basis = row.get("basis")
        try:
            date.fromisoformat(row.get("date"))
            date_known = True
        except (TypeError, ValueError):
            date_known = False
        if amount is None or currency not in {"LAK", "USD", "VND", "CNY", "THB"} or not date_known or basis not in {"capitalized_in_cogs", "incremental"}:
            issues.append({"cost_id": row["cost_id"], "reason": "amount_currency_date_or_basis_unknown"})
            continue
        bucket = totals.setdefault(currency, {"incremental": Decimal(0), "already_in_cogs": Decimal(0)})
        bucket["already_in_cogs" if basis == "capitalized_in_cogs" else "incremental"] += amount
    return {"resources": resource_view, "issues": issues,
            "costs_by_currency": {currency: {key: str(value) for key, value in bucket.items()}
                                  for currency, bucket in sorted(totals.items())},
            "allocation_count": len(unique_allocations), "cost_count": len(unique_costs),
            "business_approval": "not_attested", "cash_received": "unknown",
            "meaning": "scenario checks only; no FX, profit, cash receipt or live capacity inferred"}
