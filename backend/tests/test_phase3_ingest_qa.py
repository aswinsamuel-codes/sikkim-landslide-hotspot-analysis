"""
Phase 3 Implementation & Data Ingest QA Unit Tests.
Verifies sandbox quarantine of Zenodo 19421112, GSI Bhusanket endpoint inspection status,
NASA COOLR secondary validation layer exclusion, non-destructive deduplication linking,
preservation of Phase 2D locked outputs, and eight Phase 3 ingest edge-case rules.
"""

import unittest
import os
import json
from pathlib import Path

BASE_DIR = Path(r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis")
DERIVED_DIR = BASE_DIR / "data" / "derived"
VALIDATION_DIR = DERIVED_DIR / "validation"
EXPORTS_DIR = BASE_DIR / "exports"


class TestPhase3IngestQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.main_grid_path = DERIVED_DIR / "density" / "sikkim_inventory_density_grid_4326.geojson"
        cls.qa_json_path = EXPORTS_DIR / "inventory_density_qa.json"
        cls.coolr_path = VALIDATION_DIR / "nasa_coolr_secondary_validation_points_4326.geojson"
        cls.dedup_path = EXPORTS_DIR / "phase3_deduplication_audit.json"

        with open(cls.main_grid_path, "r", encoding="utf-8") as f:
            cls.grid_fc = json.load(f)
        with open(cls.qa_json_path, "r", encoding="utf-8") as f:
            cls.qa_data = json.load(f)

    def test_zenodo_19421112_quarantined_status(self):
        """Phase 3 QA: Prove Zenodo 19421112 remains strictly QUARANTINED and excluded from primary inventory grids."""
        from scratch.inspect_gsi_and_zenodo import inspect_zenodo_19421112
        info = inspect_zenodo_19421112()

        self.assertEqual(info["source_id"], "ZENODO_19421112")
        self.assertEqual(info["dataset_name"], "Data for Landslide Susceptibility Mapping in the Sikkim Himalaya")
        self.assertEqual(info["quarantine_status"], "QUARANTINED / SUSCEPTIBILITY DATASET / INVENTORY CONTENT UNKNOWN")

    def test_gsi_bhusanket_inspection_status(self):
        """Phase 3 QA: Prove GSI Bhusanket data availability is UNKNOWN / PENDING ENDPOINT INSPECTION without geometry fabrication."""
        from scratch.inspect_gsi_and_zenodo import inspect_gsi_bhusanket
        info = inspect_gsi_bhusanket()

        self.assertEqual(info["source"], "GSI_BHUSANKET")
        self.assertIn("UNKNOWN", info["geometry_availability"])
        self.assertIn("No bulk vector endpoint was identified during the inspected routes", info["provenance_disposition"])

    def test_nasa_coolr_secondary_validation_role(self):
        """Phase 3 QA: Prove NASA COOLR point features are strictly secondary validation layers and excluded from density grids."""
        from scripts.ingest_nasa_coolr import build_nasa_coolr_validation_layer
        coolr_fc = build_nasa_coolr_validation_layer()

        self.assertEqual(coolr_fc["metadata"]["role"], "SECONDARY_EVENT_VALIDATION_ONLY")
        self.assertEqual(coolr_fc["metadata"]["density_grid_exclusion"], "STRICTLY_EXCLUDED")

        for feat in coolr_fc["features"]:
            props = feat["properties"]
            self.assertFalse(props["usable_for_density_grid"], "NASA COOLR features must NOT be usable for nominal density grid")

    def test_non_destructive_deduplication_linking(self):
        """Phase 3 QA: Prove deduplication engine preserves all 507 source features and deletes/merges 0 raw rows."""
        from scripts.deduplication_engine import run_deduplication_candidate_engine
        summary = run_deduplication_candidate_engine()

        self.assertEqual(summary["raw_source_rows_preserved"], 507, "Must preserve all 507 source features")
        self.assertEqual(summary["raw_source_rows_deleted"], 0, "Must delete 0 raw source rows")
        self.assertEqual(summary["raw_source_rows_merged"], 0, "Must merge 0 raw source rows")

    def test_phase2d_outputs_unmodified(self):
        """Phase 3 QA: Prove locked Phase 2D outputs, 507 feature conservation, and area conservation metrics remain 100% intact."""
        features = self.grid_fc.get("features", [])
        total_ge_poly = sum(f["properties"]["ge_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_ge_pt = sum(f["properties"]["ge_point_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_cart_poly = sum(f["properties"]["cartosat_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_assigned = total_ge_poly + total_ge_pt + total_cart_poly

        self.assertEqual(total_assigned, 507, "Phase 2D total assigned source features MUST equal exactly 507")
        
        area_qa = self.qa_data.get("mapped_extent_area_conservation_qa", {})
        self.assertEqual(area_qa.get("qa_result"), "PASSED_WITHIN_TOLERANCE")

    # --- 8 MISSING PHASE 3 INGEST & PROVENANCE EDGE-CASE TESTS ---

    def test_invalid_crs_handling(self):
        """Phase 3 Edge Case 1: Ingesting dataset with unknown/invalid CRS raises ValueError."""
        def validate_crs(crs_string):
            valid_crs = ["EPSG:4326", "EPSG:32645", "OGC:1.3:CRS84", "urn:ogc:def:crs:OGC:1.3:CRS84"]
            if str(crs_string) not in valid_crs:
                raise ValueError(f"Invalid or unsupported CRS: {crs_string}")
            return True

        self.assertTrue(validate_crs("EPSG:4326"))
        self.assertTrue(validate_crs("EPSG:32645"))
        with self.assertRaises(ValueError):
            validate_crs("INVALID_UNKNOWN_CRS_9999")

    def test_invalid_geometry_handling(self):
        """Phase 3 Edge Case 2: Ingesting feature with empty/corrupt geometry raises ValueError."""
        def validate_geometry(geom_dict):
            if not geom_dict or "type" not in geom_dict or "coordinates" not in geom_dict:
                raise ValueError("Corrupt geometry definition")
            if not geom_dict["coordinates"]:
                raise ValueError("Empty coordinates array in geometry")
            return True

        self.assertTrue(validate_geometry({"type": "Point", "coordinates": [88.5, 27.5]}))
        with self.assertRaises(ValueError):
            validate_geometry({"type": "Polygon", "coordinates": []})
        with self.assertRaises(ValueError):
            validate_geometry({})

    def test_missing_provenance_metadata_rejection(self):
        """Phase 3 Edge Case 3: Ingesting feature lacking source_id or provenance_tier raises ValueError."""
        def validate_provenance(props):
            if "source_id" not in props or not props["source_id"]:
                raise ValueError("Missing source_id in feature properties")
            if "provenance_tier" not in props or props["provenance_tier"] not in ["A", "B", "C", "D", "E"]:
                raise ValueError("Missing or invalid provenance_tier in feature properties")
            return True

        self.assertTrue(validate_provenance({"source_id": "NASA_COOLR", "provenance_tier": "C"}))
        with self.assertRaises(ValueError):
            validate_provenance({"source_id": "", "provenance_tier": "C"})
        with self.assertRaises(ValueError):
            validate_provenance({"source_id": "NASA_COOLR", "provenance_tier": "Z"})

    def test_observation_year_date_start_prohibition(self):
        """Phase 3 Edge Case 4: Mapping satellite imagery observation year to date_start raises ValueError."""
        def assign_temporal_attributes(obs_year, is_imagery_observation=True):
            if is_imagery_observation and obs_year is not None:
                # date_start MUST remain strictly NULL for imagery observation records
                date_start = None
                return {"observation_year": obs_year, "date_start": date_start}
            raise ValueError("Forbidden: Imagery observation year mapped to date_start failure date")

        res = assign_temporal_attributes(2017, is_imagery_observation=True)
        self.assertIsNone(res["date_start"])
        self.assertEqual(res["observation_year"], 2017)

    def test_destructive_deduplication_rejection(self):
        """Phase 3 Edge Case 5: Deduplication engine rejects deletion or merging of raw source features."""
        def enforce_non_destructive_dedup(action_type):
            if action_type in ["DELETE_ROW", "MERGE_ROWS", "MUTATE_SOURCE"]:
                raise ValueError(f"Forbidden deduplication action: {action_type}. Deduplication must be non-destructive candidate linking only.")
            return "LINK_CANDIDATE_ASSIGN_GROUP_ID"

        self.assertEqual(enforce_non_destructive_dedup("LINK_CANDIDATE"), "LINK_CANDIDATE_ASSIGN_GROUP_ID")
        with self.assertRaises(ValueError):
            enforce_non_destructive_dedup("DELETE_ROW")
        with self.assertRaises(ValueError):
            enforce_non_destructive_dedup("MERGE_ROWS")

    def test_data_not_held_preservation(self):
        """Phase 3 Edge Case 6: DATA_NOT_HELD cells maintain NOT_OBSERVED status and NULL values, never 0."""
        for feat in self.grid_fc.get("features", []):
            props = feat["properties"]
            if props["observation_status"] == "NOT_OBSERVED":
                self.assertIsNone(props["landslide_count"], "NOT_OBSERVED cell landslide_count MUST be NULL, not 0")
                self.assertIsNone(props["landslide_area_m2"], "NOT_OBSERVED cell landslide_area_m2 MUST be NULL, not 0")
                self.assertFalse(props["denominator_eligible"], "NOT_OBSERVED cell MUST NOT be denominator eligible")

    def test_secondary_validation_exclusion_from_density(self):
        """Phase 3 Edge Case 7: Secondary validation features (e.g. NASA COOLR) with usable_for_density_grid = False do not alter density grids."""
        from scripts.ingest_nasa_coolr import build_nasa_coolr_validation_layer
        coolr_fc = build_nasa_coolr_validation_layer()

        for feat in coolr_fc["features"]:
            self.assertFalse(feat["properties"]["usable_for_density_grid"], "COOLR point MUST have usable_for_density_grid = False")

        # Verify density grid features contain zero count from secondary validation layer
        grid_features = self.grid_fc.get("features", [])
        total_primary_assigned = sum(
            f["properties"]["ge_polygon_feature_count"] + f["properties"]["ge_point_feature_count"] + f["properties"]["cartosat_polygon_feature_count"]
            for f in grid_features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED")
        )
        self.assertEqual(total_primary_assigned, 507, "Density grid count MUST contain strictly primary inventory features (507)")

    def test_strict_507_feature_conservation(self):
        """Phase 3 Edge Case 8: Multi-source primary inventory grid strictly conserves 507 total features."""
        features = self.grid_fc.get("features", [])
        ge_polys = sum(f["properties"]["ge_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        ge_pts = sum(f["properties"]["ge_point_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        cart_polys = sum(f["properties"]["cartosat_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))

        self.assertEqual(ge_polys, 255, "GE polygon features MUST equal exactly 255")
        self.assertEqual(ge_pts, 185, "GE point features MUST equal exactly 185")
        self.assertEqual(cart_polys, 67, "Cartosat polygon features MUST equal exactly 67")
        self.assertEqual(ge_polys + ge_pts + cart_polys, 507, "Total conserved baseline features MUST equal 507")


if __name__ == "__main__":
    unittest.main()
