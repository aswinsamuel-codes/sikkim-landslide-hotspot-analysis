import unittest
import os
import json

DERIVED_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\derived"

class TestSpatialQALogic(unittest.TestCase):
    def test_derived_geojson_files_exist_and_valid(self):
        expected_files = [
            "sikkim_state_boundary_4326.geojson",
            "zenodo_ge_polygons_4326.geojson",
            "zenodo_ge_points_4326.geojson",
            "zenodo_cartosat_polygons_4326.geojson",
            "zenodo_cartosat_scarp_deposit_unions_4326.geojson",
            "zenodo_mapped_extent_4326.geojson"
        ]
        for fname in expected_files:
            fpath = os.path.join(DERIVED_DIR, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing derived file: {fname}")
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertEqual(data.get("type"), "FeatureCollection")
                self.assertGreater(len(data.get("features", [])), 0)

    def test_source_inventory_feature_counts_strictly_separated(self):
        with open(os.path.join(DERIVED_DIR, "zenodo_ge_polygons_4326.geojson"), "r", encoding="utf-8") as f:
            ge_poly = json.load(f)
        with open(os.path.join(DERIVED_DIR, "zenodo_ge_points_4326.geojson"), "r", encoding="utf-8") as f:
            ge_pt = json.load(f)
        with open(os.path.join(DERIVED_DIR, "zenodo_cartosat_polygons_4326.geojson"), "r", encoding="utf-8") as f:
            cart_poly = json.load(f)
        
        count_poly = len(ge_poly["features"])
        count_pt = len(ge_pt["features"])
        count_cart = len(cart_poly["features"])
        
        self.assertEqual(count_poly, 255)
        self.assertEqual(count_pt, 185)
        self.assertEqual(count_cart, 67)
        self.assertEqual(count_poly + count_pt + count_cart, 507)

    def test_cartosat_unions_marked_derived_spatial_association(self):
        with open(os.path.join(DERIVED_DIR, "zenodo_cartosat_scarp_deposit_unions_4326.geojson"), "r", encoding="utf-8") as f:
            cart_unions = json.load(f)
        self.assertEqual(len(cart_unions["features"]), 23)
        for feat in cart_unions["features"]:
            props = feat["properties"]
            self.assertEqual(props.get("derivation_status"), "DERIVED_SPATIAL_ASSOCIATION")
            self.assertEqual(props.get("association_basis"), "PURELY_SPATIALLY_INFERRED")
            self.assertIn("scarp_feature_id", props)
            self.assertIn("paired_deposit_feature_ids", props)

    def test_mapped_extent_disclaimer_semantics(self):
        with open(os.path.join(DERIVED_DIR, "zenodo_mapped_extent_4326.geojson"), "r", encoding="utf-8") as f:
            extent = json.load(f)
        meta = extent.get("metadata", {})
        self.assertIn("disclaimer", meta)
        self.assertIn("MUST NOT be assumed to have zero landslides", meta["disclaimer"])

if __name__ == "__main__":
    unittest.main()
