import unittest
from src.assessments import certificate_check, portfolio_check


class AssessmentTests(unittest.TestCase):
    def test_same_generic_or_registration_does_not_resolve_identity(self):
        expected = {"trade_name": "Fixture-A", "manufacturer": "Factory-A", "strength": "750mg/150ml", "form": "infusion", "pack": "bottle"}
        certificate = {"generic": "same-generic", "registration_id": "same-number",
                       "product": {**expected, "trade_name": "Fixture-B", "strength": "500mg/100ml"},
                       "registration_valid_until": "2026-12-31", "registry_as_of": "2025-12-26"}
        got = certificate_check(expected, certificate, as_of="2026-10-31")
        self.assertEqual(got["identity_state"], "identity_conflict")
        self.assertIn("strength", got["conflicting_fields"])
        self.assertEqual(got["registry_snapshot_state"], "historical_snapshot_only")
        self.assertEqual(got["business_approval"], "not_attested")

    def test_four_expiries_cannot_substitute_for_each_other(self):
        product = dict(trade_name="A", manufacturer="M", strength="1", form="tab", pack="box")
        got = certificate_check(product, {"product": product, "registration_valid_until": "2026-12-31",
            "lot_expiry": "2026-09-01", "quote_valid_until": "2026-10-31"}, as_of="2026-10-31")
        self.assertEqual(got["identity_state"], "matched_identity_only")
        self.assertEqual(got["expiry_axes"], {"registration_valid_until": "current_in_fixture", "lot_expiry": "expired_in_fixture",
            "quote_valid_until": "current_in_fixture", "delegation_valid_until": "unknown"})

    def test_missing_identity_is_unknown_not_a_match(self):
        self.assertEqual(certificate_check({}, {}, as_of="2026-10-31")["identity_state"], "identity_unknown")

    def test_whitespace_or_nonstring_product_fields_are_not_matching_identity(self):
        fields = ("trade_name", "manufacturer", "strength", "form", "pack")
        for invalid in ("   ", 42):
            with self.subTest(value=invalid):
                product = {key: invalid for key in fields}
                result = certificate_check(product, {"product": product}, as_of="2026-10-31")
                self.assertEqual(result["identity_state"], "identity_unknown")
                self.assertEqual(set(result["unknown_fields"]), set(fields))

    def test_two_packages_cannot_both_use_same_full_capacity(self):
        got = portfolio_check({"stock": {"available": "10", "unit": "box"}}, [
            {"allocation_id": "a", "case_id": "A", "resource_id": "stock", "quantity": "7", "unit": "box"},
            {"allocation_id": "b", "case_id": "B", "resource_id": "stock", "quantity": "6", "unit": "box"}], [])
        self.assertEqual(got["resources"][0]["allocated"], "13")
        self.assertEqual(got["resources"][0]["state"], "overcommitted")

    def test_same_allocation_retry_not_double_counted_and_collision_rejected(self):
        row = {"allocation_id": "a", "case_id": "A", "resource_id": "cash", "quantity": "7", "unit": "USD"}
        got = portfolio_check({"cash": {"available": "10", "unit": "USD"}}, [row, dict(row)], [])
        self.assertEqual(got["allocation_count"], 1)
        self.assertEqual(got["resources"][0]["allocated"], "7")
        with self.assertRaises(ValueError):
            portfolio_check({}, [row, {**row, "quantity": "8"}], [])

    def test_capitalized_freight_not_deducted_again_and_no_fx_total(self):
        rows = [{"cost_id": "freight", "amount": "100", "currency": "USD", "date": "2026-10-31", "basis": "capitalized_in_cogs"},
                {"cost_id": "local", "amount": "2000", "currency": "LAK", "date": "2026-10-31", "basis": "incremental"}]
        got = portfolio_check({}, [], rows + [dict(rows[0])])
        self.assertEqual(got["cost_count"], 2)
        self.assertEqual(got["costs_by_currency"]["USD"], {"incremental": "0", "already_in_cogs": "100"})
        self.assertEqual(got["costs_by_currency"]["LAK"]["incremental"], "2000")
        self.assertEqual(got["cash_received"], "unknown")

    def test_eu_is_not_money_and_unknown_quantity_stays_unknown(self):
        got = portfolio_check({"truck": {"available": "10", "unit": "EU"}}, [
            {"allocation_id": "a", "case_id": "A", "resource_id": "truck", "quantity": "1", "unit": "USD"},
            {"allocation_id": "b", "case_id": "B", "resource_id": "truck", "quantity": None, "unit": "EU"}], [])
        self.assertEqual(got["resources"][0]["state"], "allocation_unknown")
        self.assertIsNone(got["resources"][0]["allocated"])
        self.assertEqual(got["resources"][0]["unresolved_allocation_count"], 2)

    def test_known_subtotal_cannot_hide_unknown_other_case_allocation(self):
        got = portfolio_check({"stock": {"available": "10", "unit": "box"}}, [
            {"allocation_id": "a", "case_id": "A", "resource_id": "stock", "quantity": "7", "unit": "box"},
            {"allocation_id": "b", "case_id": "B", "resource_id": "stock", "quantity": None, "unit": "box"}], [])
        resource = got["resources"][0]
        self.assertEqual(resource["known_allocated"], "7")
        self.assertIsNone(resource["allocated"])
        self.assertEqual(resource["state"], "allocation_unknown")

    def test_unknown_cost_not_zero_or_default_kip(self):
        got = portfolio_check({}, [], [{"cost_id": "x", "amount": None, "currency": "CNJ", "date": None, "basis": "incremental"}])
        self.assertEqual(got["costs_by_currency"], {})
        self.assertEqual(got["issues"][0]["reason"], "amount_currency_date_or_basis_unknown")


if __name__ == "__main__":
    unittest.main()
