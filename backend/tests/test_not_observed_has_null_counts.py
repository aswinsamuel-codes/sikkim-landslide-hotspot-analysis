"""
Test B-3: NOT_OBSERVED status forces landslide_count and landslide_area_m2 to NULL.
"""

import unittest
from backend.core.research_constraints import classify_observation_status


class TestNotObservedNullCounts(unittest.TestCase):

    def test_not_observed_has_null_counts(self):
        """NOT_OBSERVED cells (fraction = 0) MUST have NULL count/area, never 0."""
        status, eligible = classify_observation_status(0.0)
        self.assertEqual(status, "NOT_OBSERVED")
        self.assertFalse(eligible)

        sample_cell_obs = {
            "observation_status": status,
            "denominator_eligible": eligible,
            "landslide_count": None,
            "landslide_area_m2": None
        }
        self.assertIsNone(sample_cell_obs["landslide_count"])
        self.assertIsNone(sample_cell_obs["landslide_area_m2"])


if __name__ == "__main__":
    unittest.main()
