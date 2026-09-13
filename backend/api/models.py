"""
Pydantic Schemas for API Endpoints
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    status: str = "ok"
    version: str
    database_engine: str
    registered_dem_source: Optional[str]
    registered_rainfall_primary: Optional[str]
    recurrence_eligible_years_count: int = 0
    phase: str = "Phase 1 — Data Foundation"


class SourceResponse(BaseModel):
    source_id: str
    name: str
    organization: str
    provenance: str
    license: Optional[str] = None
    download_method: str
    requires_auth: bool = False
    status: str
    coverage_note: Optional[str] = None


class YearCoverageResponse(BaseModel):
    year: int
    handoff_class: str
    inventory_exists: bool
    geometry_held: bool
    extent_held: bool
    usable_for_denominator: bool
    trigger_regime: Optional[str] = None
    trigger_confidence: Optional[str] = None
    notes: Optional[str] = None


class RecurrenceCellResponse(BaseModel):
    cell_id: int
    cell_code: str
    observation_status: str # 'NOT_OBSERVED' | 'PARTIALLY_OBSERVED' | 'OBSERVED'
    denominator_eligible: bool
    active_years: int = 0
    observed_years: int = 0
    recurrence_index: Optional[float] = None
    recurrence_class: str = "NOT_OBSERVED"
    weakest_extent_basis: str = "unknown"
    trigger_regimes: List[str] = []


class HotspotResponse(BaseModel):
    title: str = "Project-derived Historical Hotspot Index"
    kpi_label: str = "TOTAL MAPPED RECORDS IN LOCAL DATABASE (not de-duplicated across sources)"
    per_source_counts: Dict[str, int]
    weakest_extent_basis: str = "unknown"
    disclaimer: str
