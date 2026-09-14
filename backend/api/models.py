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


class TemporalYearStatusResponse(BaseModel):
    year: int
    status_class: str  # 'VALIDATED_OBSERVATIONS_HELD' | 'AUTHORITATIVE_METADATA_ONLY' | 'DATA_NOT_HELD'
    feature_count: Optional[int] = None
    usable_for_recurrence_denominator: bool = False
    temporal_semantics: str
    notes: Optional[str] = None


class DensityGridSummaryResponse(BaseModel):
    total_cells: int = 7355
    observed_cells: int = 2820
    partially_covered_cells: int = 98
    data_not_held_cells: int = 4437
    density_field_name: str = "centroid_assigned_inventory_feature_density_per_km2"
    disclaimer: str = "Inventory Feature Density represents count of centroid-assigned features per 1 km2 cell. It does NOT represent risk, hazard, probability, or recurrence."


class CoverageSummaryResponse(BaseModel):
    total_cells: int = 7355
    observed_cells: int = 2820
    partially_covered_cells: int = 98
    data_not_held_cells: int = 4437
    sikkim_state_boundary_area_km2: float = 7081.54
    grid_intersection_area_km2: float = 7079.48
    discrepancy_percentage: float = 0.0291
    mapped_extent_area_km2: float = 2962.15


class ProvenanceMetadataResponse(BaseModel):
    layer_name: str
    source_id: str
    organization: str
    provenance_tier: str
    original_geometry_type: str
    original_crs: str
    temporal_semantics: str
    feature_count: int
    processing_method: str

