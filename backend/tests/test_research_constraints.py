"""
Test suite for research constraint enforcement rules.
"""

import unittest
from backend.core.research_constraints import (
    load_field_semantics,
    validate_field_mapping,
    classify_observation_status,
    validate_ml_baseline_features,
    register_dem_source,
    get_dem_source_status,
    evaluate_ml_semantic_gate,
    MIN_OBSERVED_FRACTION,
)


class TestResearchConstraints(unittest.TestCase):

    def test_field_semantics_contract_loadable(self):
        """Verify field_semantics.json loads and contains forbidden mappings."""
        contract = load_field_semantics()
        self.assertIn("forbidden_mappings", contract)
        self.assertGreaterEqual(len(contract["forbidden_mappings"]), 7)

    def test_zenodo_year_to_date_start_mapping_forbidden(self):
        """FM-01: Mapping Zenodo Year to date_start MUST raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_field_mapping("Year", "date_start", source_name="Zenodo_8169506")
        self.assertIn("FORBIDDEN FIELD MAPPING", str(cm.exception))
        self.assertIn("FM-01", str(cm.exception))

    def test_district_string_rename_forbidden(self):
        """FM-02: String-based district rename MUST raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_field_mapping("district", "district_assignment")
        self.assertIn("FM-02", str(cm.exception))

    def test_road_distance_to_blockage_forbidden(self):
        """FM-03: Distance to road mapped to blockage MUST raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_field_mapping("distance_to_road_m", "road_blockage")
        self.assertIn("FM-03", str(cm.exception))

    def test_dem_source_owner_decision(self):
        """DEM source requires explicit owner decision and registers properly."""
        self.assertIsNone(get_dem_source_status())
        registered = register_dem_source("copernicus_dem_30m")
        self.assertEqual(registered, "copernicus_dem_30m")
        self.assertEqual(get_dem_source_status(), "copernicus_dem_30m")

        with self.assertRaises(ValueError):
            register_dem_source("invalid_dem_xyz")

    def test_ml_semantic_gate_failure_clauses(self):
        """ML semantic gate fails when observation coverage is insufficient."""
        passed, failing = evaluate_ml_semantic_gate(
            label_years=[2014, 2017],
            held_extents={2014: None, 2017: None},
            cell_observations_materialized=False,
            positive_labels_in_observed_cells=False,
            negatives_from_eligible_observed_cells=False,
            eligible_cell_years_count=0,
            positive_count=0,
            includes_zenodo_year=False,
            all_extents_unknown=True,
            spatial_cv_configured=False
        )
        self.assertFalse(passed)
        self.assertGreaterEqual(len(failing), 5)


if __name__ == "__main__":
    unittest.main()
