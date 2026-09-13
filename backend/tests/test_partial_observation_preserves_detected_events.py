"""
Test B-3: Partial observation status preserves detected event numerators.
"""

import unittest
from backend.core.research_constraints import classify_observation_status


class TestPartialObservationNumerators(unittest.TestCase):

    def test_partial_observation_preserves_detected_events(self):
        """PARTIALLY_OBSERVED cells (0 < fraction < 0.5) preserve detected events but are denominator ineligible."""
        status, eligible = classify_observation_status(0.25)
        self.assertEqual(status, "PARTIALLY_OBSERVED")
        self.assertFalse(eligible)

        sample_cell_obs = {
            "observation_status": status,
            "denominator_eligible": eligible,
            "landslide_count": 3,
            "landslide_area_m2": 4500.0
        }
        self.assertEqual(sample_cell_obs["landslide_count"], 3)
        self.assertFalse(sample_cell_obs["denominator_eligible"])


if __name__ == "__main__":
    unittest.main()
