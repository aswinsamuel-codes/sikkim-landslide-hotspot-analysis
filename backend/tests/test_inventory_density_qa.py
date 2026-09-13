"""
Phase 2D Final GIS QA Unit Tests.
Verifies true geometric-centroid assignment, mapped-extent area conservation,
density denominator semantics, 507-feature conservation, derived-union exclusion,
and Sikkim area discrepancy reporting.
"""

import unittest
import os
import json

DERIVED_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\derived"
DENSITY_DIR = os.path.join(DERIVED_DIR, "density")
EXPORTS_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\exports"


class TestInventoryDensityQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        main_grid_path = os.path.join(DENSITY_DIR, "sikkim_inventory_density_grid_4326.geojson")
        qa_json_path = os.path.join(EXPORTS_DIR, "inventory_density_qa.json")
        qa_md_path = os.path.join(EXPORTS_DIR, "INVENTORY_DENSITY_QA.md")

        with open(main_grid_path, "r", encoding="utf-8") as f:
            cls.grid_fc = json.load(f)
        with open(qa_json_path, "r", encoding="utf-8") as f:
            cls.qa_data = json.load(f)
        with open(qa_md_path, "r", encoding="utf-8") as f:
            cls.qa_md = f.read()

    def test_true_geometric_centroid_assignment(self):
        """Final GIS QA: Prove true 2D geometric centroid in EPSG:32645 is used for 1-to-1 feature grid assignment."""
        centroid_audit = self.qa_data.get("true_geometric_centroid_assignment_audit", {})
        self.assertIn("GE_POLYGON", centroid_audit)
        self.assertIn("GE_POINT", centroid_audit)
        self.assertIn("CARTOSAT_POLYGON", centroid_audit)

        self.assertEqual(centroid_audit["GE_POLYGON"]["features_assigned_by_true_geometric_centroid"], 255)
        self.assertEqual(centroid_audit["GE_POINT"]["features_assigned_by_true_geometric_centroid"], 185)
        self.assertEqual(centroid_audit["CARTOSAT_POLYGON"]["features_assigned_by_true_geometric_centroid"], 67)

    def test_extent_area_conservation_and_tolerance(self):
        """Final GIS QA: Prove Zenodo 8169506 mapped extent polygon area conservation relative error is within tolerance (<0.50%)."""
        area_qa = self.qa_data.get("mapped_extent_area_conservation_qa", {})
        true_area = area_qa.get("zenodo_8169506_mapped_extent_polygon_area_km2", 0)
        grid_sum = area_qa.get("sum_grid_cell_extent_intersection_area_km2", 0)
        rel_err = area_qa.get("relative_error_percent", 99.0)
        tolerance = area_qa.get("tolerance_threshold_percent", 0.50)

        self.assertGreater(true_area, 2900.0, "Mapped extent polygon area must be ~2962 km²")
        self.assertGreater(grid_sum, 2900.0, "Grid sum extent area must be ~2956 km²")
        self.assertLess(rel_err, tolerance, f"Relative error {rel_err}% must be less than tolerance threshold {tolerance}%")
        self.assertEqual(area_qa.get("qa_result"), "PASSED_WITHIN_TOLERANCE")

    def test_boundary_area_conservation_and_tolerance(self):
        """Final GIS QA: Prove Sikkim state boundary area conservation relative error is within tolerance (<0.50%)."""
        boundary_qa = self.qa_data.get("boundary_area_conservation_qa", {})
        poly_area = boundary_qa.get("gadm_sikkim_boundary_polygon_area_km2", 0)
        grid_sum = boundary_qa.get("sum_grid_cell_in_state_area_km2", 0)
        rel_err = boundary_qa.get("relative_error_percent", 99.0)
        tolerance = boundary_qa.get("tolerance_percent", 0.50)

        self.assertGreater(poly_area, 7070.0, "GADM polygon area must be ~7081.54 km²")
        self.assertGreater(grid_sum, 7070.0, "Sum of grid cell in-state area must be ~7079.48 km²")
        self.assertLess(rel_err, tolerance, f"Relative error {rel_err}% must be less than tolerance threshold {tolerance}%")
        self.assertEqual(boundary_qa.get("qa_result"), "PASSED_WITHIN_TOLERANCE")

    def test_density_denominator_semantics(self):
        """Final GIS QA: Prove density field strictly uses nominal_cell_area_km2 (1.0) as denominator."""
        denom_qa = self.qa_data.get("density_denominator_semantics", {})
        self.assertEqual(denom_qa.get("denominator_used"), "nominal_cell_area_km2 (1.0 km²)")
        self.assertEqual(denom_qa.get("in_state_area_substitutions"), 0)

        features = self.grid_fc.get("features", [])
        for f in features:
            props = f["properties"]
            if props["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"):
                tot_cnt = props["total_source_layer_feature_count"]
                density = props["centroid_assigned_inventory_feature_density_per_km2"]
                nominal_area = props["nominal_cell_area_km2"]

                self.assertEqual(nominal_area, 1.0, "Nominal cell area must be 1.0 km²")
                self.assertEqual(density, round(tot_cnt / nominal_area, 4), "Density must strictly equal total count / nominal_cell_area_km2")

    def test_source_507_feature_conservation(self):
        """Final GIS QA: Prove exactly 507 source features are assigned across grid."""
        features = self.grid_fc.get("features", [])
        total_ge_poly = sum(f["properties"]["ge_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_ge_pt = sum(f["properties"]["ge_point_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_cart_poly = sum(f["properties"]["cartosat_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_assigned = total_ge_poly + total_ge_pt + total_cart_poly

        self.assertEqual(total_ge_poly, 255, "GE Polygons count must equal 255")
        self.assertEqual(total_ge_pt, 185, "GE Points count must equal 185")
        self.assertEqual(total_cart_poly, 67, "Cartosat Polygons count must equal 67")
        self.assertEqual(total_assigned, 507, "Total assigned source features MUST equal exactly 507")

    def test_derived_union_exclusion(self):
        """Final GIS QA: Prove 23 derived Cartosat unions remain strictly excluded."""
        features = self.grid_fc.get("features", [])
        total_assigned = sum(f["properties"]["total_source_layer_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        self.assertEqual(total_assigned, 507, "Derived unions MUST NOT increase 507 total source count")

    def test_observation_year_semantics(self):
        """Final GIS QA: Prove distinct observation years contain imagery observation records, not failure dates."""
        features = self.grid_fc.get("features", [])
        for f in features:
            props = f["properties"]
            self.assertNotIn("date_start", props)
            self.assertNotIn("failure_date", props)
            self.assertNotIn("recurrence_class", props)
            self.assertIn("distinct_observation_years_list", props)

    def test_sikkim_area_discrepancy_reported(self):
        """Final GIS QA: Prove GADM polygon area (~7,081.54 km²) and grid sum (~7,079.48 km²) are reported separately from reference ~7,096 km²."""
        grid_spec = self.qa_data.get("grid_specification", {})
        poly_area = grid_spec.get("gadm_sikkim_boundary_polygon_area_km2", 0)
        grid_sum = grid_spec.get("sum_grid_cell_in_state_area_km2", 0)
        ref_area = grid_spec.get("reference_sikkim_administrative_area_km2", 0)

        self.assertGreater(poly_area, 7080.0, "GADM polygon area must be ~7,081.54 km²")
        self.assertGreater(grid_sum, 7070.0, "Grid sum in-state area must be ~7,079.48 km²")
        self.assertEqual(ref_area, 7096.0, "Reference area must equal 7,096.0 km²")
        self.assertIn("differ", self.qa_md.lower())

    def test_output_cell_properties_complete(self):
        """Final GIS QA: Prove every feature in the output grid retains all required properties."""
        features = self.grid_fc.get("features", [])
        required_keys = [
            "cell_id", "nominal_cell_area_km2", "in_state_area_km2",
            "coverage_fraction", "observation_status", "ge_polygon_feature_count",
            "ge_point_feature_count", "cartosat_polygon_feature_count",
            "total_source_layer_feature_count",
            "centroid_assigned_inventory_feature_density_per_km2",
            "distinct_observation_years_list", "distinct_observation_years_count"
        ]
        for f in features:
            props = f["properties"]
            for k in required_keys:
                self.assertIn(k, props, f"Missing required property {k} in cell {props.get('cell_id')}")


if __name__ == "__main__":
    unittest.main()
