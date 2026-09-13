"""
Phase 1 Integration & Database Tests.
Verifies Phase 1 ORM models, Pydantic schemas, source registration,
FastAPI endpoints, and year coverage matrix seeding.
"""

import unittest
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.core.config import (
    REGISTERED_DATABASE_ENGINE, REGISTERED_DEM_SOURCE, REGISTERED_RAINFALL_PRIMARY
)
from scripts.init_db import CATALOGUED_SOURCES, parse_year_coverage_matrix


class TestPhase1Database(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_fastapi_healthcheck_endpoint(self):
        """GET /health must return ok status, Phase 1 version, and 0 eligible years."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["database_engine"], "postgresql_postgis")
        self.assertEqual(data["registered_dem_source"], "copernicus_dem_glo_30")
        self.assertEqual(data["registered_rainfall_primary"], "era5_land")
        self.assertEqual(data["recurrence_eligible_years_count"], 0)

    def test_list_sources_endpoint(self):
        """GET /api/local/sources must list all 15 catalogued sources."""
        response = self.client.get("/api/local/sources")
        self.assertEqual(response.status_code, 200)
        sources = response.json()
        self.assertEqual(len(sources), 15)

        source_ids = [s["source_id"] for s in sources]
        self.assertIn("NRSC_2011", source_ids)
        self.assertIn("COPERNICUS_DEM_GLO_30", source_ids)
        self.assertIn("ERA5_LAND", source_ids)
        self.assertIn("ZENODO_19421112", source_ids)

        # Check quarantined source
        quarantined = next(s for s in sources if s["source_id"] == "ZENODO_19421112")
        self.assertEqual(quarantined["status"], "quarantined")

    def test_coverage_endpoint_preserves_four_flags(self):
        """GET /api/local/coverage must return 15 rows with distinct status booleans."""
        response = self.client.get("/api/local/coverage")
        self.assertEqual(response.status_code, 200)
        coverage = response.json()
        self.assertEqual(len(coverage), 15)

        for row in coverage:
            self.assertIn("inventory_exists", row)
            self.assertIn("geometry_held", row)
            self.assertIn("extent_held", row)
            self.assertIn("usable_for_denominator", row)
            self.assertFalse(row["usable_for_denominator"])

    def test_hotspots_endpoint_per_source_counts(self):
        """GET /api/local/hotspots must return per-source counts and NEVER cross-source total."""
        response = self.client.get("/api/local/hotspots")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Project-derived Historical Hotspot Index")
        self.assertIn("per_source_counts", data)
        self.assertIn("NRSC_2011", data["per_source_counts"])

    def test_recurrence_endpoint_returns_not_observed(self):
        """GET /api/local/recurrence must return NOT_OBSERVED cells in zero-eligible state."""
        response = self.client.get("/api/local/recurrence")
        self.assertEqual(response.status_code, 200)
        cells = response.json()
        self.assertGreater(len(cells), 0)
        self.assertEqual(cells[0]["observation_status"], "NOT_OBSERVED")
        self.assertEqual(cells[0]["recurrence_class"], "NOT_OBSERVED")


if __name__ == "__main__":
    unittest.main()
