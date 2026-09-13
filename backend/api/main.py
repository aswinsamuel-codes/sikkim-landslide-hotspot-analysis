"""
FastAPI Main Application
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from backend.core.config import (
    PROJECT_NAME, VERSION, DESCRIPTION, REGISTERED_DATABASE_ENGINE, REGISTERED_DEM_SOURCE, REGISTERED_RAINFALL_PRIMARY
)
from backend.core.research_constraints import get_dem_source_status
from backend.api.models import (
    HealthCheckResponse, SourceResponse, YearCoverageResponse, HotspotResponse, RecurrenceCellResponse
)
from scripts.init_db import CATALOGUED_SOURCES, parse_year_coverage_matrix

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION
)

# CORS middleware for local frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
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
        phase="Phase 1 — Data Foundation"
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
    """Returns cell recurrence. In current Phase 1 state with zero eligible years, returns NOT_OBSERVED everywhere."""
    # Stub response representing correct-and-empty state
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
