"""
Database Initialization & Seeding Script
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)

This script parses SIKKIM_COVERAGE_MATRIX_2011_2025.csv and seeds the `sources`
and `year_coverage` tables with verified research metadata.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

from backend.core.config import METADATA_DIR
from backend.core.research_constraints import COVERAGE_MATRIX_FILE, FIELD_SEMANTICS_FILE

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Sources Seeding Data
CATALOGUED_SOURCES = [
    {
        "source_id": "NRSC_2011",
        "name": "NRSC Post-Earthquake Landslide Inventory (18 Sep 2011)",
        "organization": "National Remote Sensing Centre (NRSC) / ISRO",
        "provenance": "A",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Martha et al. (2014) paper of record count (1,196 points). Geometry NOT HELD locally.",
        "status": "metadata_registered_geometry_not_held"
    },
    {
        "source_id": "NRSC_2014",
        "name": "NRSC Seasonal Monsoon Landslide Inventory (2014)",
        "organization": "NRSC / ISRO",
        "provenance": "A",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Bhuvan seasonal layer exists. Geometry NOT HELD locally.",
        "status": "metadata_registered_geometry_not_held"
    },
    {
        "source_id": "NRSC_2017",
        "name": "NRSC Seasonal Monsoon Landslide Inventory (2017)",
        "organization": "NRSC / ISRO",
        "provenance": "A",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Bhuvan seasonal layer exists. Geometry NOT HELD locally.",
        "status": "metadata_registered_geometry_not_held"
    },
    {
        "source_id": "NRSC_2023",
        "name": "NRSC Seasonal & GLOF Cascade Inventory (2023)",
        "organization": "NRSC / ISRO",
        "provenance": "A",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Bhuvan seasonal layer exists. Trigger INFERRED. Geometry NOT HELD locally.",
        "status": "metadata_registered_geometry_not_held"
    },
    {
        "source_id": "ZENODO_8169506",
        "name": "Sikkim Multi-Temporal Remote Sensing Landslide Inventory (2011-2019)",
        "organization": "Heijenk et al. / Zenodo",
        "provenance": "C",
        "license": "CC-BY-4.0",
        "license_allows_redistribution": True,
        "download_method": "http_get",
        "requires_auth": False,
        "coverage_note": "Google Earth & Cartosat mapped features over southern Sikkim. Excluded from recurrence.",
        "status": "acquired_pending_ingest"
    },
    {
        "source_id": "ZENODO_19421112",
        "name": "IIT Dhanbad Sikkim Inventory Package (282 MB RAR)",
        "organization": "IIT Dhanbad / Zenodo",
        "provenance": "B",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Quarantined 282 MB RAR package. Inspection required before use.",
        "status": "quarantined"
    },
    {
        "source_id": "COPERNICUS_DEM_GLO_30",
        "name": "Copernicus DEM GLO-30 Digital Elevation Model",
        "organization": "European Space Agency (ESA) / Copernicus",
        "provenance": "A",
        "license": "Open Data / Public Domain",
        "license_allows_redistribution": True,
        "download_method": "http_get",
        "requires_auth": False,
        "coverage_note": "Selected owner DEM decision (30m spatial resolution).",
        "status": "decision_registered_pending_phase8"
    },
    {
        "source_id": "ERA5_LAND",
        "name": "ERA5-Land Hourly Land Surface Reanalysis Precipitation",
        "organization": "ECMWF / Copernicus Climate Change Service",
        "provenance": "A",
        "license": "Copernicus License",
        "license_allows_redistribution": True,
        "download_method": "api",
        "requires_auth": False,
        "coverage_note": "Primary historical rainfall source (0.1° resolution, precipitation + soil moisture consistency).",
        "status": "decision_registered_pending_phase8"
    },
    {
        "source_id": "CHIRPS_V3",
        "name": "CHIRPS v3 Daily Rainfall (0.05°)",
        "organization": "UCSB CHC",
        "provenance": "B",
        "license": "Public Domain",
        "license_allows_redistribution": True,
        "download_method": "http_get",
        "requires_auth": False,
        "coverage_note": "Rainfall cross-check dataset (0.05° resolution).",
        "status": "decision_registered_pending_phase8"
    },
    {
        "source_id": "GPM_IMERG",
        "name": "GPM IMERG Half-Hourly Near-Real-Time Precipitation",
        "organization": "NASA / PPS",
        "provenance": "A",
        "download_method": "api",
        "requires_auth": False,
        "coverage_note": "Reserved for future operational trigger engine; not substituted for historical primary.",
        "status": "reserved_operational"
    },
    {
        "source_id": "IMD_025DEG",
        "name": "IMD 0.25° Daily Gridded Rainfall",
        "organization": "India Meteorological Department (IMD)",
        "provenance": "A",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Validation and district/state reference only; not cell-level historical rainfall source.",
        "status": "validation_reference_only"
    },
    {
        "source_id": "OSM_SIKKIM",
        "name": "OpenStreetMap Sikkim Road Network Extract",
        "organization": "OpenStreetMap Contributors / Geofabrik",
        "provenance": "D",
        "license": "ODbL 1.0",
        "license_allows_redistribution": True,
        "download_method": "http_get",
        "requires_auth": False,
        "coverage_note": "Sikkim road network. ODbL share-alike applies to derived road exposure datasets.",
        "status": "acquired"
    },
    {
        "source_id": "GHS_POP",
        "name": "Global Human Settlement Layer Population (GHS-POP)",
        "organization": "European Commission JRC",
        "provenance": "A",
        "license": "CC-BY-4.0",
        "license_allows_redistribution": True,
        "download_method": "http_get",
        "requires_auth": False,
        "coverage_note": "Primary population exposure dataset. Population figures labelled DERIVED/ESTIMATED.",
        "status": "catalogued"
    },
    {
        "source_id": "NASA_COOLR",
        "name": "NASA Cooperative Open Online Landslide Repository (COOLR)",
        "organization": "NASA GSFC",
        "provenance": "C",
        "license": "Public Domain",
        "license_allows_redistribution": True,
        "download_method": "api",
        "requires_auth": False,
        "coverage_note": "Global point repository. Sparse coverage in Sikkim (2020-2022).",
        "status": "catalogued"
    },
    {
        "source_id": "GHOSH_2012",
        "name": "Ghosh et al. (2012) 2011 Earthquake Landslide Benchmark",
        "organization": "Research Literature",
        "provenance": "B",
        "download_method": "manual_admin",
        "requires_auth": False,
        "coverage_note": "Literature benchmark count (~421 landslides). No geometry published.",
        "status": "literature_benchmark_no_geometry"
    }
]


def parse_year_coverage_matrix() -> List[Dict[str, Any]]:
    """Parse SIKKIM_COVERAGE_MATRIX_2011_2025.csv into dictionaries."""
    rows = []
    if not COVERAGE_MATRIX_FILE.exists():
        raise FileNotFoundError(f"Missing matrix file at {COVERAGE_MATRIX_FILE}")

    with open(COVERAGE_MATRIX_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "year": int(r["year"]),
                "handoff_class": r["handoff_class"],
                "inventory_exists": r["inventory_exists"].upper() == "TRUE",
                "geometry_held": r["geometry_held"].upper() == "TRUE",
                "extent_held": r["extent_held"].upper() == "TRUE",
                "usable_for_denominator": r["usable_for_denominator"].upper() == "TRUE",
                "trigger_regime": r.get("trigger_regime", "monsoon"),
                "trigger_confidence": r.get("trigger_confidence", "UNVERIFIED"),
                "notes": r.get("notes", "")
            })
    return rows


def print_seeding_summary() -> None:
    """Print summary of Phase 1 catalogued metadata."""
    sources = CATALOGUED_SOURCES
    matrix = parse_year_coverage_matrix()

    logging.info(f"=== PHASE 1 SOURCE CATALOGUE SUMMARY ===")
    logging.info(f"Total Sources Registered: {len(sources)}")
    for s in sources:
        logging.info(f"  - [{s['source_id']}] {s['name']} (Status: {s['status']})")

    logging.info(f"\n=== PHASE 1 YEAR COVERAGE MATRIX SUMMARY ===")
    eligible_count = sum(1 for m in matrix if m["usable_for_denominator"])
    logging.info(f"Total Observation Years: {len(matrix)}")
    logging.info(f"Recurrence-Eligible Observation Years: {eligible_count} of {len(matrix)}")
    for m in matrix:
        logging.info(
            f"  - Year {m['year']} [{m['handoff_class']}]: "
            f"inventory_exists={m['inventory_exists']}, "
            f"geometry_held={m['geometry_held']}, "
            f"extent_held={m['extent_held']}, "
            f"usable_for_denominator={m['usable_for_denominator']}"
        )


if __name__ == "__main__":
    print_seeding_summary()
