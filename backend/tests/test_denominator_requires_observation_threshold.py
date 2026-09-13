"""
Test B-3: Denominator eligibility requires observed_fraction >= min_observed_fraction (0.5).
"""

import unittest
from backend.core.research_constraints import classify_observation_status, MIN_OBSERVED_FRACTION


class TestDenominatorObservationThreshold(unittest.TestCase):

    def test_denominator_requires_observation_threshold(self):
        """Denominator eligibility evaluates to TRUE only when observed_fraction >= 0.5."""
        self.assertEqual(MIN_OBSERVED_FRACTION, 0.5)

        # 0.499 is PARTIALLY_OBSERVED -> ineligible
        status_below, eligible_below = classify_observation_status(0.499)
        self.assertEqual(status_below, "PARTIALLY_OBSERVED")
        self.assertFalse(eligible_below)

        # 0.500 is OBSERVED -> eligible
        status_at, eligible_at = classify_observation_status(0.500)
        self.assertEqual(status_at, "OBSERVED")
        self.assertTrue(eligible_at)

        # 0.850 is OBSERVED -> eligible
        status_above, eligible_above = classify_observation_status(0.850)
        self.assertEqual(status_above, "OBSERVED")
        self.assertTrue(eligible_above)


if __name__ == "__main__":
    unittest.main()
