"""
Phase 5 Implementation & Production QA Unit Tests.
Verifies Phase 5 production Sikkim historical landslide mapping endpoints,
507 primary source feature conservation, 23 derived Cartosat association exclusion,
Phase 2D cell coverage counts (7,355 total: 2,820 OBSERVED, 98 PARTIALLY_COVERED, 4,437 DATA_NOT_HELD),
strict temporal semantics (observation_year set, event_date = NULL), DATA_NOT_HELD preservation,
15-year timeline status categories, inventory feature density field semantics, zero ML/recurrence,
and layer provenance completeness.
"""

import unittest
import json
from pathlib import Path
from fastapi.testclient import TestClient

from backend.api.main import app

BASE_DIR = Path(r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis")
DERIVED_DIR = BASE_DIR / "data" / "derived"
EXPORTS_DIR = BASE_DIR / "exports"


class TestPhase5ImplementationQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        with open(DERIVED_DIR / "density" / "sikkim_inventory_density_grid_4326.geojson", "r", encoding="utf-8") as f:
            cls.grid_fc = json.load(f)

    def test_fastapi_healthcheck(self):
        """Phase 5 QA: Verify FastAPI health check returns ok, Phase 5 version, and zero eligible years."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["recurrence_eligible_years_count"], 0)
        self.assertIn("Phase 5", data["phase"])

    def test_baseline_507_features_conserved_across_api(self):
        """Phase 5 QA: Prove /api/local/inventory/features conserves 507 primary source features."""
        res = self.client.get("/api/local/inventory/features")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        ge_poly_count = len(data["ge_polygons"]["features"])
        ge_pt_count = len(data["ge_points"]["features"])
        cart_poly_count = len(data["cartosat_polygons"]["features"])

        self.assertEqual(ge_poly_count, 255)
        self.assertEqual(ge_pt_count, 185)
        self.assertEqual(cart_poly_count, 67)
        self.assertEqual(ge_poly_count + ge_pt_count + cart_poly_count, 507)

    def test_derived_23_cartosat_unions_excluded_from_counts(self):
        """Phase 5 QA: Prove 23 derived Cartosat scarp/deposit unions are isolated from primary feature counts."""
        res = self.client.get("/api/local/inventory/features")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        derived_unions_count = len(data["cartosat_derived_unions"]["features"])
        self.assertEqual(derived_unions_count, 23)
        self.assertEqual(data["baseline_summary"]["primary_source_features"], 507)
        self.assertEqual(data["baseline_summary"]["derived_cartosat_unions"], 23)

    def test_phase2d_outputs_preserved(self):
        """Phase 5 QA: Prove Phase 2D grid cell coverage metrics remain strictly intact."""
        features = self.grid_fc.get("features", [])
        self.assertEqual(len(features), 7355)

        observed = sum(1 for f in features if f["properties"]["observation_status"] == "OBSERVED")
        partially_covered = sum(1 for f in features if f["properties"]["observation_status"] == "PARTIALLY_COVERED")
        data_not_held = sum(1 for f in features if f["properties"]["observation_status"] == "DATA_NOT_HELD")

        self.assertEqual(observed, 2820)
        self.assertEqual(partially_covered, 98)
        self.assertEqual(data_not_held, 4437)

    def test_temporal_semantics_intact(self):
        """Phase 5 QA: Prove observation year represents imagery observation record, event_date remains NULL."""
        res = self.client.get("/api/local/inventory/temporal/2011")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        for feat in data["features"]:
            self.assertIn("observation_year", feat["properties"])
            self.assertEqual(feat["properties"]["observation_year"], 2011)
            self.assertIsNone(feat["properties"].get("event_date"))

    def test_data_not_held_never_converted_to_zero(self):
        """Phase 5 QA: Prove missing observation years return 404 with DATA_NOT_HELD notice (no 0 counts created)."""
        res = self.client.get("/api/local/inventory/temporal/2004")
        self.assertEqual(res.status_code, 404)
        self.assertIn("DATA_NOT_HELD", res.json()["detail"])

    def test_timeline_3_category_status(self):
        """Phase 5 QA: Prove /api/local/inventory/temporal returns 15-year timeline with valid status categories."""
        res = self.client.get("/api/local/inventory/temporal")
        self.assertEqual(res.status_code, 200)
        timeline = res.json()
        self.assertTrue(len(timeline) >= 15)

        held_years = {2002, 2005, 2006, 2009, 2010, 2011, 2012, 2015, 2017, 2018, 2019}
        meta_years = {2014, 2023}

        for item in timeline:
            yr = item["year"]
            if yr in held_years:
                self.assertEqual(item["status_class"], "VALIDATED_OBSERVATIONS_HELD")
                self.assertIsNotNone(item["feature_count"])
            elif yr in meta_years:
                self.assertEqual(item["status_class"], "AUTHORITATIVE_METADATA_ONLY")
                self.assertIsNone(item["feature_count"])
            elif yr < 2026:
                self.assertEqual(item["status_class"], "DATA_NOT_HELD")
                self.assertIsNone(item["feature_count"])

    def test_density_grid_field_name(self):
        """Phase 5 QA: Prove density field name is strictly centroid_assigned_inventory_feature_density_per_km2."""
        res = self.client.get("/api/local/inventory/density/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["density_field_name"], "centroid_assigned_inventory_feature_density_per_km2")
        self.assertIn("does NOT represent risk", data["disclaimer"])

    def test_provenance_metadata_completeness(self):
        """Phase 5 QA: Prove /api/local/inventory/provenance returns tracking metadata for all catalogued layers."""
        res = self.client.get("/api/local/inventory/provenance")
        self.assertEqual(res.status_code, 200)
        prov = res.json()
        self.assertEqual(len(prov), 5)

        layer_names = [p["layer_name"] for p in prov]
        self.assertIn("Google Earth Landslide Polygons", layer_names)
        self.assertIn("Cartosat Derived Scarp/Deposit Unions", layer_names)


if __name__ == "__main__":
    unittest.main()
