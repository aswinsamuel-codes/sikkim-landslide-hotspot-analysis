import unittest
import os
import json

TEMPORAL_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\derived\temporal"
EXPORTS_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\exports"

class TestTemporalObservationQA(unittest.TestCase):
    def test_temporal_geojson_layers_exist_and_valid(self):
        expected_years = [2002, 2005, 2006, 2009, 2010, 2011, 2012, 2015, 2017, 2018, 2019]
        for yr in expected_years:
            fname = f"zenodo_observations_{yr}_4326.geojson"
            fpath = os.path.join(TEMPORAL_DIR, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing temporal layer: {fname}")
            with open(fpath, "r", encoding="utf-8") as f:
                fc = json.load(f)
                self.assertEqual(fc.get("type"), "FeatureCollection")
                self.assertGreater(len(fc.get("features", [])), 0)

    def test_unspecified_active_layer_exists_and_valid(self):
        unspec_fname = "zenodo_observations_unspecified_active_4326.geojson"
        unspec_path = os.path.join(TEMPORAL_DIR, unspec_fname)
        self.assertTrue(os.path.exists(unspec_path), f"Missing unspecified layer: {unspec_fname}")
        with open(unspec_path, "r", encoding="utf-8") as f:
            fc = json.load(f)
            self.assertEqual(fc.get("type"), "FeatureCollection")
            self.assertEqual(len(fc.get("features", [])), 212)

    def test_date_start_is_strictly_null(self):
        for fname in os.listdir(TEMPORAL_DIR):
            if fname.endswith(".geojson"):
                with open(os.path.join(TEMPORAL_DIR, fname), "r", encoding="utf-8") as f:
                    fc = json.load(f)
                    for feat in fc.get("features", []):
                        props = feat.get("properties", {})
                        self.assertIsNone(props.get("date_start"), "date_start MUST be strictly NULL for observation year records.")

    def test_mandatory_disclaimer_present_in_all_temporal_features(self):
        expected_disclaimer = "Observation year indicates the year associated with the source imagery/observation record. It is not a confirmed landslide failure date."
        for fname in os.listdir(TEMPORAL_DIR):
            if fname.endswith(".geojson"):
                with open(os.path.join(TEMPORAL_DIR, fname), "r", encoding="utf-8") as f:
                    fc = json.load(f)
                    for feat in fc.get("features", []):
                        props = feat.get("properties", {})
                        self.assertEqual(props.get("disclaimer"), expected_disclaimer)

    def test_temporal_qa_report_files_exist(self):
        json_report = os.path.join(EXPORTS_DIR, "temporal_observation_qa.json")
        md_report = os.path.join(EXPORTS_DIR, "TEMPORAL_OBSERVATION_QA.md")
        self.assertTrue(os.path.exists(json_report), "Missing temporal_observation_qa.json")
        self.assertTrue(os.path.exists(md_report), "Missing TEMPORAL_OBSERVATION_QA.md")

    def test_no_unsupported_temporal_interpretations(self):
        """Correction 1: Verify absence of unsupported temporal interpretations and presence of neutral language."""
        md_path = os.path.join(EXPORTS_DIR, "TEMPORAL_OBSERVATION_QA.md")
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn("Pre-earthquake", content, "Report must not contain 'Pre-earthquake'")
        self.assertNotIn("Post-2011 Sikkim Earthquake imagery", content, "Report must not contain 'Post-2011 Sikkim Earthquake imagery'")
        self.assertIn("Highest source-feature count in this dataset.", content, "2011 must be described neutrally as highest source-feature count")

    def test_bbox_terminology_and_disclaimer(self):
        """Correction 2: Verify BBOX spatial candidate overlap terminology and disclaimer."""
        md_path = os.path.join(EXPORTS_DIR, "TEMPORAL_OBSERVATION_QA.md")
        json_path = os.path.join(EXPORTS_DIR, "temporal_observation_qa.json")

        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertNotIn("topological overlaps", md_content.lower(), "Must not use 'topological overlaps'")
        self.assertIn("BBOX", md_content, "Must use BBOX spatial candidate overlap terminology")
        self.assertIn("proof of actual geometry intersection", md_content, "Must state BBOX is NOT proof of geometry intersection")
        self.assertIn("disclaimer", data.get("cross_source_spatial_candidate_overlaps", {}))

    def test_feature_count_language_compliance(self):
        """Correction 3: Verify feature count language compliance."""
        md_path = os.path.join(EXPORTS_DIR, "TEMPORAL_OBSERVATION_QA.md")
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Ensure values are not called 'landslide count' or 'event count'
        self.assertNotIn("landslide count", content.lower())
        self.assertNotIn("event count", content.lower())
        self.assertIn("Total Source-Layer Features", content)

if __name__ == "__main__":
    unittest.main()

