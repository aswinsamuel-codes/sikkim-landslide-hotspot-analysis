"""
Test B-2: Zenodo observation_year exclusion from failure/event dates.
"""

import unittest
from backend.core.research_constraints import validate_field_mapping


class TestZenodoObservationYearGuard(unittest.TestCase):

    def test_zenodo_observation_year_not_used_as_event_year(self):
        """Zenodo Year MUST NOT map to date_start or event failure date."""
        with self.assertRaises(ValueError) as cm:
            validate_field_mapping("Year", "date_start", source_name="Zenodo_8169506")
        self.assertIn("FM-01", str(cm.exception))
        self.assertIn("Zenodo Year represents imagery observation/acquisition year", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
