"""
FastAPI Main Application
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from pathlib import Path
import json

from backend.core.config import (
    PROJECT_NAME, VERSION, DESCRIPTION, REGISTERED_DATABASE_ENGINE, REGISTERED_DEM_SOURCE, REGISTERED_RAINFALL_PRIMARY
)
from backend.core.research_constraints import get_dem_source_status
from backend.api.models import (
    HealthCheckResponse, SourceResponse, YearCoverageResponse, HotspotResponse, RecurrenceCellResponse,
    TemporalYearStatusResponse, DensityGridSummaryResponse, CoverageSummaryResponse, ProvenanceMetadataResponse
)
from scripts.init_db import CATALOGUED_SOURCES, parse_year_coverage_matrix

BASE_DIR = Path(r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis")
DERIVED_DIR = BASE_DIR / "data" / "derived"
TEMPORAL_DIR = DERIVED_DIR / "temporal"
DENSITY_DIR = DERIVED_DIR / "density"

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION
)

# CORS middleware for local frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Healthcheck endpoint returning system configuration and zero-eligible-year state."""
    matrix = parse_year_coverage_matrix()
    eligible_count = sum(1 for m in matrix if m["usable_for_denominator"])
    return HealthCheckResponse(
        status="ok",
        version=VERSION,
        database_engine=REGISTERED_DATABASE_ENGINE,
        registered_dem_source=REGISTERED_DEM_SOURCE or get_dem_source_status(),
        registered_rainfall_primary=REGISTERED_RAINFALL_PRIMARY,
        recurrence_eligible_years_count=eligible_count,
        phase="Phase 5 — Production Mapping & Data Layer"
    )


@app.get("/api/local/sources", response_model=List[SourceResponse])
def list_sources():
    """List all registered and catalogued data sources with provenance and license information."""
    return [
        SourceResponse(
            source_id=s["source_id"],
            name=s["name"],
            organization=s["organization"],
            provenance=s["provenance"],
            license=s.get("license"),
            download_method=s["download_method"],
            requires_auth=s["requires_auth"],
            status=s["status"],
            coverage_note=s.get("coverage_note")
        )
        for s in CATALOGUED_SOURCES
    ]


@app.get("/api/local/coverage", response_model=List[YearCoverageResponse])
def get_year_coverage():
    """Returns 15-year coverage matrix preserving all four status booleans."""
    matrix = parse_year_coverage_matrix()
    return [YearCoverageResponse(**row) for row in matrix]


@app.get("/api/local/hotspots", response_model=HotspotResponse)
def get_hotspots():
    """Returns Project-derived Historical Hotspot Index metadata with per-source counts (NEVER cross-source total)."""
    return HotspotResponse(
        title="Project-derived Historical Hotspot Index",
        kpi_label="TOTAL MAPPED RECORDS IN LOCAL DATABASE (not de-duplicated across sources)",
        per_source_counts={
            "NRSC_2011": 1196,
            "ZENODO_8169506_CARTOSAT": 44,
            "GHOSH_2012": 421
        },
        weakest_extent_basis="unknown",
        disclaimer="These figures describe separate surveys and must not be added together into a single total."
    )


@app.get("/api/local/recurrence", response_model=List[RecurrenceCellResponse])
def get_recurrence():
    """Returns cell recurrence. In current Phase 5 state with zero eligible years, returns NOT_OBSERVED everywhere."""
    return [
        RecurrenceCellResponse(
            cell_id=1,
            cell_code="SK_CELL_0001",
            observation_status="NOT_OBSERVED",
            denominator_eligible=False,
            active_years=0,
            observed_years=0,
            recurrence_index=None,
            recurrence_class="NOT_OBSERVED",
            weakest_extent_basis="unknown",
            trigger_regimes=[]
        )
    ]


# === PHASE 5 MAPPING & INVENTORY ENDPOINTS ===

@app.get("/api/local/inventory/features")
def get_inventory_features():
    """
    Returns GeoJSON FeatureCollections for all baseline historical inventory layers:
    GE Polygons (255), GE Points (185), Cartosat Polygons (67), Derived Cartosat Unions (23), Mapped Extent (1), State Boundary (1).
    Conserves 507 primary source features and marks derived associations explicitly.
    """
    def read_json_file(path: Path):
        if not path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {path.name}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "sikkim_boundary": read_json_file(DERIVED_DIR / "sikkim_state_boundary_4326.geojson"),
        "mapped_extent": read_json_file(DERIVED_DIR / "zenodo_mapped_extent_4326.geojson"),
        "ge_polygons": read_json_file(DERIVED_DIR / "zenodo_ge_polygons_4326.geojson"),
        "ge_points": read_json_file(DERIVED_DIR / "zenodo_ge_points_4326.geojson"),
        "cartosat_polygons": read_json_file(DERIVED_DIR / "zenodo_cartosat_polygons_4326.geojson"),
        "cartosat_derived_unions": read_json_file(DERIVED_DIR / "zenodo_cartosat_scarp_deposit_unions_4326.geojson"),
        "baseline_summary": {
            "primary_source_features": 507,
            "ge_polygons": 255,
            "ge_points": 185,
            "cartosat_polygons": 67,
            "derived_cartosat_unions": 23,
            "derived_association_note": "Cartosat scarp/deposit unions (23) are derived spatial associations and MUST NOT be added to inventory feature counts or density numerators."
        }
    }


@app.get("/api/local/inventory/temporal", response_model=List[TemporalYearStatusResponse])
def list_temporal_years():
    """
    Returns 15-year timeline status array distinguishing:
    1. VALIDATED_OBSERVATIONS_HELD (2002, 2005, 2006, 2009, 2010, 2011, 2012, 2015, 2017, 2018, 2019)
    2. AUTHORITATIVE_METADATA_ONLY (2011, 2014, 2017, 2023 - NRSC/GSI metadata pending vector acquisition)
    3. DATA_NOT_HELD (Missing observation years; no zero counts created)
    """
    held_years = {
        2002: 12, 2005: 14, 2006: 121, 2009: 67, 2010: 95,
        2011: 279, 2012: 153, 2015: 35, 2017: 98, 2018: 20, 2019: 13
    }
    authoritative_metadata_years = {2014, 2023}  # 2011 & 2017 also have held Zenodo features

    timeline = []
    for y in range(2002, 2026):
        if y in held_years:
            status_class = "VALIDATED_OBSERVATIONS_HELD"
            count = held_years[y]
            notes = "Imagery observation records held from Zenodo 8169506 dataset."
        elif y in authoritative_metadata_years:
            status_class = "AUTHORITATIVE_METADATA_ONLY"
            count = None
            notes = "Authoritative NRSC/NDEM seasonal report exists; vector GIS acquisition pending."
        else:
            status_class = "DATA_NOT_HELD"
            count = None
            notes = "No validated observation data currently held in database. Does NOT imply zero landslides."

        timeline.append(TemporalYearStatusResponse(
            year=y,
            status_class=status_class,
            feature_count=count,
            usable_for_recurrence_denominator=False,
            temporal_semantics="Imagery/Observation Year (event_date = NULL)",
            notes=notes
        ))

    return timeline


@app.get("/api/local/inventory/temporal/{year}")
def get_temporal_layer(year: int):
    """
    Returns GeoJSON feature layer for a specific imagery observation year.
    Returns HTTP 404 for missing/unsupported years with DATA_NOT_HELD status.
    """
    path = TEMPORAL_DIR / f"zenodo_observations_{year}_4326.geojson"
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"DATA_NOT_HELD: No validated observation layer currently held for year {year}. Missing data MUST NOT be interpreted as zero landslides."
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@app.get("/api/local/inventory/density")
def get_inventory_density_grid():
    """
    Returns 1 km inventory density grid GeoJSON (centroid_assigned_inventory_feature_density_per_km2).
    Density represents source feature density only, NOT risk, hazard, susceptibility, or recurrence.
    """
    path = DENSITY_DIR / "sikkim_inventory_density_grid_4326.geojson"
    if not path.exists():
        path = DERIVED_DIR / "sikkim_inventory_density_grid_4326.geojson"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Density grid file not found.")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


@app.get("/api/local/inventory/density/summary", response_model=DensityGridSummaryResponse)
def get_inventory_density_summary():
    """Returns summary metadata for the 1 km inventory feature density grid."""
    return DensityGridSummaryResponse()


@app.get("/api/local/inventory/coverage/summary", response_model=CoverageSummaryResponse)
def get_coverage_summary():
    """Returns summary metadata for observation coverage status across Sikkim's 7,355 grid cells."""
    return CoverageSummaryResponse()


@app.get("/api/local/inventory/provenance", response_model=List[ProvenanceMetadataResponse])
def get_layer_provenance():
    """Returns layer-by-layer provenance and tracking information for all catalogued layers."""
    return [
        ProvenanceMetadataResponse(
            layer_name="Google Earth Landslide Polygons",
            source_id="ZENODO_8169506_GE_POLY",
            organization="Zenodo / Research Community",
            provenance_tier="AUTHORITATIVE_COMMUNITY_PUBLIC",
            original_geometry_type="Polygon",
            original_crs="EPSG:4326",
            temporal_semantics="Imagery Observation Year (2002-2019, event_date = NULL)",
            feature_count=255,
            processing_method="Geometric centroid grid assignment to 1 km UTM45N cells"
        ),
        ProvenanceMetadataResponse(
            layer_name="Google Earth Landslide Points",
            source_id="ZENODO_8169506_GE_POINT",
            organization="Zenodo / Research Community",
            provenance_tier="AUTHORITATIVE_COMMUNITY_PUBLIC",
            original_geometry_type="Point",
            original_crs="EPSG:4326",
            temporal_semantics="Imagery Observation Year (2002-2019, event_date = NULL)",
            feature_count=185,
            processing_method="Point-in-polygon grid assignment to 1 km UTM45N cells"
        ),
        ProvenanceMetadataResponse(
            layer_name="Cartosat Landslide Polygons",
            source_id="ZENODO_8169506_CARTOSAT_POLY",
            organization="Zenodo / Research Community",
            provenance_tier="AUTHORITATIVE_COMMUNITY_PUBLIC",
            original_geometry_type="Polygon",
            original_crs="EPSG:4326",
            temporal_semantics="Post-Earthquake Observation (2011-09-30, event_date = NULL)",
            feature_count=67,
            processing_method="Geometric centroid grid assignment to 1 km UTM45N cells"
        ),
        ProvenanceMetadataResponse(
            layer_name="Cartosat Derived Scarp/Deposit Unions",
            source_id="ZENODO_8169506_CARTOSAT_DERIVED_UNION",
            organization="Project Derived Spatial Association",
            provenance_tier="PROJECT_DERIVED_ASSOCIATION",
            original_geometry_type="MultiPolygon",
            original_crs="EPSG:4326",
            temporal_semantics="Derived Spatial Union (2011-09-30)",
            feature_count=23,
            processing_method="Derived scarp+deposit union; EXCLUDED from inventory numerators & density"
        ),
        ProvenanceMetadataResponse(
            layer_name="Mapped Extent Footprint",
            source_id="ZENODO_8169506_EXTENT",
            organization="Zenodo / Research Community",
            provenance_tier="AUTHORITATIVE_COMMUNITY_PUBLIC",
            original_geometry_type="Polygon",
            original_crs="EPSG:4326",
            temporal_semantics="Survey Extent Boundary (~2,962 km2)",
            feature_count=1,
            processing_method="Spatial denominator boundary for OBSERVED vs DATA_NOT_HELD grid cells"
        )
    ]

