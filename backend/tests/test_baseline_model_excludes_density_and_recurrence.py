"""
Test B-1: Baseline Susceptibility Model Decoupling & Anti-Leakage.
"""

import unittest
from backend.core.research_constraints import validate_ml_baseline_features


class TestBaselineModelDecoupling(unittest.TestCase):

    def test_baseline_model_excludes_density_and_recurrence(self):
        """Baseline feature list MUST contain no historical density or recurrence feature."""
        valid_baseline_features = [
            "slope_deg",
            "aspect_deg",
            "elevation_m",
            "curvature",
            "relief_m",
            "dist_to_drainage_m",
            "dist_to_road_m",
            "land_cover_class",
            "rain_3d_mm"
        ]
        # Should pass without exception
        validate_ml_baseline_features(valid_baseline_features)

        # Feature list with density must fail
        with self.assertRaises(ValueError) as cm1:
            validate_ml_baseline_features(["slope_deg", "hist_landslide_density"])
        self.assertIn("ML ANTI-LEAKAGE VIOLATION [B-1]", str(cm1.exception))

        # Feature list with recurrence must fail
        with self.assertRaises(ValueError) as cm2:
            validate_ml_baseline_features(["slope_deg", "hist_recurrence_index"])
        self.assertIn("ML ANTI-LEAKAGE VIOLATION [B-1]", str(cm2.exception))


if __name__ == "__main__":
    unittest.main()
