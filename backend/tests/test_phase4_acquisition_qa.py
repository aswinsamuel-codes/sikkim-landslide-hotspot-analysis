"""
Phase 4 Implementation & Acquisition Audit QA Unit Tests.
Verifies Phase 4 acquisition audit findings, conservative GSI wording, Zenodo 19421112 quarantine status,
NRSC acquisition pending status, NASA COOLR secondary validation exclusion, observation year semantics,
and 100% preservation of the locked 507-feature baseline.
"""

import unittest
import os
import json
from pathlib import Path

BASE_DIR = Path(r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis")
DERIVED_DIR = BASE_DIR / "data" / "derived"
VALIDATION_DIR = DERIVED_DIR / "validation"
EXPORTS_DIR = BASE_DIR / "exports"


class TestPhase4AcquisitionQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.main_grid_path = DERIVED_DIR / "density" / "sikkim_inventory_density_grid_4326.geojson"
        cls.qa_json_path = EXPORTS_DIR / "inventory_density_qa.json"
        cls.audit_json_path = EXPORTS_DIR / "phase4_acquisition_audit.json"
        cls.audit_md_path = EXPORTS_DIR / "PHASE4_ACQUISITION_AUDIT.md"

        with open(cls.main_grid_path, "r", encoding="utf-8") as f:
            cls.grid_fc = json.load(f)
        with open(cls.qa_json_path, "r", encoding="utf-8") as f:
            cls.qa_data = json.load(f)
        with open(cls.audit_json_path, "r", encoding="utf-8") as f:
            cls.audit_data = json.load(f)

    def test_phase4_acquisition_audit_reports_exist(self):
        """Phase 4 QA: Prove phase4_acquisition_audit.json and PHASE4_ACQUISITION_AUDIT.md exist and are valid."""
        self.assertTrue(self.audit_json_path.exists(), "phase4_acquisition_audit.json MUST exist")
        self.assertTrue(self.audit_md_path.exists(), "PHASE4_ACQUISITION_AUDIT.md MUST exist")
        self.assertEqual(self.audit_data.get("phase4_status"), "ACQUISITION AUDIT COMPLETE")

    def test_gsi_bhusanket_conservative_wording(self):
        """Phase 4 QA: Prove GSI Bhusanket disposition uses exact conservative wording."""
        sources = {s["source_id"]: s for s in self.audit_data.get("sources", [])}
        self.assertIn("GSI_BHUSANKET", sources)
        gsi = sources["GSI_BHUSANKET"]

        self.assertEqual(gsi["acquisition_status"], "ACQUISITION_PENDING")
        self.assertIn("No bulk vector endpoint was identified during the inspected routes", gsi["notes"])

    def test_zenodo_19421112_quarantined_status(self):
        """Phase 4 QA: Prove Zenodo 19421112 remains strictly QUARANTINED as a susceptibility dataset."""
        sources = {s["source_id"]: s for s in self.audit_data.get("sources", [])}
        self.assertIn("ZENODO_19421112", sources)
        z = sources["ZENODO_19421112"]

        self.assertEqual(z["acquisition_status"], "QUARANTINED")
        self.assertEqual(z["inventory_role"], "QUARANTINED_SUSCEPTIBILITY_DATASET")
        self.assertEqual(z["license_status"], "NOT_DECLARED_ON_RECORD")

    def test_nrsc_acquisition_pending_status(self):
        """Phase 4 QA: Prove NRSC 2011, 2014, 2017, and 2023 datasets are tagged ACQUISITION_PENDING without geometry fabrication."""
        sources = {s["source_id"]: s for s in self.audit_data.get("sources", [])}
        for nrsc_id in ["NRSC_2011", "NRSC_2014", "NRSC_2017", "NRSC_2023"]:
            self.assertIn(nrsc_id, sources)
            self.assertEqual(sources[nrsc_id]["acquisition_status"], "ACQUISITION_PENDING")
            self.assertFalse(sources[nrsc_id]["geometry_available"], f"{nrsc_id} geometry must not be fabricated from counts/PDFs")

    def test_nasa_coolr_secondary_validation_role(self):
        """Phase 4 QA: Prove NASA COOLR features are strictly secondary validation and excluded from density grids."""
        coolr_path = VALIDATION_DIR / "nasa_coolr_secondary_validation_points_4326.geojson"
        with open(coolr_path, "r", encoding="utf-8") as f:
            coolr_fc = json.load(f)

        for feat in coolr_fc["features"]:
            self.assertFalse(feat["properties"]["usable_for_density_grid"])

    def test_locked_baseline_507_features_conserved(self):
        """Phase 4 QA: Prove 507 locked source inventory features are 100% conserved."""
        features = self.grid_fc.get("features", [])
        total_ge_poly = sum(f["properties"]["ge_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_ge_pt = sum(f["properties"]["ge_point_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))
        total_cart_poly = sum(f["properties"]["cartosat_polygon_feature_count"] for f in features if f["properties"]["observation_status"] in ("OBSERVED", "PARTIALLY_COVERED"))

        self.assertEqual(total_ge_poly, 255)
        self.assertEqual(total_ge_pt, 185)
        self.assertEqual(total_cart_poly, 67)
        self.assertEqual(total_ge_poly + total_ge_pt + total_cart_poly, 507)

    def test_nrsc_2011_inspection_report_valid(self):
        """Phase 4 QA: Prove NRSC 2011 inspection report correctly records ACQUISITION_PENDING / METADATA_ONLY status."""
        report_path = EXPORTS_DIR / "phase4_nrsc_2011_inspection.json"
        self.assertTrue(report_path.exists(), "phase4_nrsc_2011_inspection.json MUST exist")

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["source_id"], "NRSC_2011")
        self.assertFalse(data["legitimate_vector_geometry_found"])
        self.assertEqual(data["acquisition_disposition"], "ACQUISITION_PENDING / METADATA_ONLY")
        self.assertEqual(data["reported_count_in_pdf"], 1196)

    def test_nrsc_2014_inspection_report_valid(self):
        """Phase 4 QA: Prove NRSC 2014 inspection report correctly records ACQUISITION_PENDING / METADATA_ONLY status."""
        report_path = EXPORTS_DIR / "phase4_nrsc_2014_inspection.json"
        self.assertTrue(report_path.exists(), "phase4_nrsc_2014_inspection.json MUST exist")

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["source_id"], "NRSC_2014")
        self.assertFalse(data["legitimate_vector_geometry_found"])
        self.assertEqual(data["acquisition_disposition"], "ACQUISITION_PENDING / METADATA_ONLY")
        self.assertEqual(data["observation_year"], 2014)
        self.assertIsNone(data["event_date"])

    def test_nrsc_2017_inspection_report_valid(self):
        """Phase 4 QA: Prove NRSC 2017 inspection report correctly records ACQUISITION_PENDING / METADATA_ONLY status."""
        report_path = EXPORTS_DIR / "phase4_nrsc_2017_inspection.json"
        self.assertTrue(report_path.exists(), "phase4_nrsc_2017_inspection.json MUST exist")

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["source_id"], "NRSC_2017")
        self.assertFalse(data["legitimate_vector_geometry_found"])
        self.assertEqual(data["acquisition_disposition"], "ACQUISITION_PENDING / METADATA_ONLY")
        self.assertEqual(data["observation_year"], 2017)
        self.assertIsNone(data["event_date"])

    def test_nrsc_2023_inspection_report_valid(self):
        """Phase 4 QA: Prove NRSC 2023 inspection report correctly records ACQUISITION_PENDING / METADATA_ONLY status."""
        report_path = EXPORTS_DIR / "phase4_nrsc_2023_inspection.json"
        self.assertTrue(report_path.exists(), "phase4_nrsc_2023_inspection.json MUST exist")

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["source_id"], "NRSC_2023")
        self.assertFalse(data["legitimate_vector_geometry_found"])
        self.assertEqual(data["acquisition_disposition"], "ACQUISITION_PENDING / METADATA_ONLY")
        self.assertEqual(data["observation_year"], 2023)
        self.assertIsNone(data["event_date"])
        self.assertEqual(data["trigger_classification"], "SEASONAL_AND_EVENT_MIXED_TRIGGER")
        self.assertEqual(data["license_status"], "NOT_DECLARED_ON_RECORD")

    def test_gsi_inspection_report_valid(self):
        """Phase 4 QA: Prove GSI inspection report correctly records required structure, conservative disposition, and susceptibility separation."""
        report_path = EXPORTS_DIR / "phase4_gsi_inspection.json"
        self.assertTrue(report_path.exists(), "phase4_gsi_inspection.json MUST exist")

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["source_id"], "GSI_BHUSANKET")
        self.assertFalse(data["legitimate_vector_geometry_found"])
        self.assertEqual(data["acquisition_disposition"], "ACQUISITION_PENDING / METADATA_ONLY")
        self.assertEqual(data["license_status"], "NOT_DECLARED_ON_RECORD")
        self.assertIn("No bulk vector endpoint was identified during the inspected routes", data["compliance_rule_enforced"])
        self.assertIn("SUSCEPTIBILITY_SEPARATED_FROM_INVENTORY", data["inventory_vs_susceptibility_classification"])

        breakdown = data.get("gsi_source_breakdown", {})
        self.assertIn("A_bulk_sikkim_vector_inventory", breakdown)
        self.assertIn("B_individual_public_landslide_records", breakdown)
        self.assertIn("C_downloadable_inventory_data", breakdown)
        self.assertIn("D_web_viewable_records", breakdown)
        self.assertIn("E_susceptibility_products", breakdown)
        self.assertIn("F_combination_summary", breakdown)
        self.assertEqual(breakdown["E_susceptibility_products"]["status"], "SUSCEPTIBILITY_ONLY")

    def test_phase4_final_acquisition_matrix_valid(self):
        """Phase 4 QA: Prove consolidated PHASE4_FINAL_ACQUISITION_MATRIX.json and report exist and validate all 5 sources."""
        matrix_path = EXPORTS_DIR / "PHASE4_FINAL_ACQUISITION_MATRIX.json"
        report_path = EXPORTS_DIR / "PHASE4_FINAL_ACQUISITION_REPORT.md"
        self.assertTrue(matrix_path.exists(), "PHASE4_FINAL_ACQUISITION_MATRIX.json MUST exist")
        self.assertTrue(report_path.exists(), "PHASE4_FINAL_ACQUISITION_REPORT.md MUST exist")

        with open(matrix_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("ACQUISITION AUDIT & INSPECTION COMPLETE", data["phase4_status"])
        self.assertEqual(data["conservative_disposition_statement"], "No bulk vector endpoint was identified during the inspected routes.")

        # Baseline protection assertions
        baseline = data.get("baseline_protection", {})
        self.assertEqual(baseline.get("primary_inventory_features_conserved"), 507)
        self.assertEqual(baseline.get("derived_cartosat_associations"), 23)
        self.assertEqual(baseline.get("recurrence_eligible_years"), 0)

        # Source records assertion (NRSC 2011, 2014, 2017, 2023, and GSI Bhusanket)
        sources = {s["source_id"]: s for s in data.get("sources_matrix", [])}
        for sid in ["NRSC_2011", "NRSC_2014", "NRSC_2017", "NRSC_2023", "GSI_BHUSANKET"]:
            self.assertIn(sid, sources)
            self.assertFalse(sources[sid]["vector_gis_available"])
            self.assertEqual(sources[sid]["acquisition_status"], "ACQUISITION_PENDING")
            self.assertEqual(sources[sid]["license_status"], "NOT_DECLARED_ON_RECORD")


if __name__ == "__main__":
    unittest.main()





