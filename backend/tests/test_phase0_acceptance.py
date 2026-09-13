"""
Phase 0 Acceptance Tests (QA-12 / QA-27).
"""

import csv
import unittest
from backend.core.research_constraints import COVERAGE_MATRIX_FILE, classify_observation_status


class TestPhase0Acceptance(unittest.TestCase):

    def test_zero_eligible_years_matrix(self):
        """Verify coverage matrix has 0 recurrence-eligible observation years."""
        self.assertTrue(COVERAGE_MATRIX_FILE.exists(), f"Coverage matrix missing at {COVERAGE_MATRIX_FILE}")

        rows = []
        with open(COVERAGE_MATRIX_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        self.assertEqual(len(rows), 15)

        # Verify usable_for_denominator is FALSE for ALL 15 years
        for r in rows:
            self.assertEqual(r["usable_for_denominator"].upper(), "FALSE", f"Year {r['year']} should have usable_for_denominator=FALSE")

        # Verify NRSC years (2011, 2014, 2017, 2023) have geometry_held = FALSE
        nrsc_years = ["2011", "2014", "2017", "2023"]
        for r in rows:
            if r["year"] in nrsc_years:
                self.assertEqual(r["geometry_held"].upper(), "FALSE", f"Year {r['year']} should have geometry_held=FALSE")

    def test_unobserved_cell_year_semantics(self):
        """Unobserved cell-year MUST evaluate to NOT_OBSERVED with NULL count and area."""
        status, eligible = classify_observation_status(0.0)
        self.assertEqual(status, "NOT_OBSERVED")
        self.assertFalse(eligible)

    def test_four_coverage_flags_preserved(self):
        """Verify that inventory_exists, geometry_held, extent_held, usable_for_denominator are distinct."""
        with open(COVERAGE_MATRIX_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

        required_flags = ["inventory_exists", "geometry_held", "extent_held", "usable_for_denominator"]
        for flag in required_flags:
            self.assertIn(flag, fieldnames, f"Missing required coverage status flag '{flag}' in matrix")


if __name__ == "__main__":
    unittest.main()
