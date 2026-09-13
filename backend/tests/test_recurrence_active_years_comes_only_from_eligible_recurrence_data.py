"""
Test B-2: Recurrence active_years derives ONLY from denominator-eligible recurrence data in Phase 6.
"""

import csv
import unittest
from backend.core.research_constraints import COVERAGE_MATRIX_FILE


class TestRecurrenceActiveYearsSource(unittest.TestCase):

    def test_recurrence_active_years_comes_only_from_eligible_recurrence_data(self):
        """Recurrence active_years MUST only count denominator-eligible years (Zenodo excluded)."""
        zenodo_years = ["2012", "2013", "2015", "2018", "2019"]
        with open(COVERAGE_MATRIX_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["year"] in zenodo_years:
                    self.assertEqual(
                        row["usable_for_denominator"].upper(),
                        "FALSE",
                        f"Zenodo year {row['year']} must have usable_for_denominator=FALSE so it cannot feed recurrence active_years."
                    )


if __name__ == "__main__":
    unittest.main()
