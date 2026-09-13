"""
SQLAlchemy ORM Models
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)
"""

import datetime
from sqlalchemy import (
    Column, Integer, BigInteger, SmallInteger, Float, Numeric, String, Boolean, Date, DateTime, Text, ARRAY, JSON, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from backend.core.database import Base


class Source(Base):
    __tablename__ = "sources"
    __table_args__ = {"schema": "sikkim"}

    source_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    coverage_start = Column(Date, nullable=True)
    coverage_end = Column(Date, nullable=True)
    coverage_note = Column(Text, nullable=True)
    provenance = Column(String, nullable=False) # 'A','B','C','D','E'
    license = Column(String, nullable=True)
    license_allows_redistribution = Column(Boolean, nullable=True)
    download_method = Column(String, nullable=False)
    requires_auth = Column(Boolean, nullable=False, default=False)
    robots_checked_at = Column(DateTime(timezone=True), nullable=True)
    robots_allows_fetch = Column(Boolean, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    last_imported_at = Column(DateTime(timezone=True), nullable=True)
    record_count = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)


class SourceFieldMapping(Base):
    __tablename__ = "source_field_mappings"
    __table_args__ = (
        UniqueConstraint("source_id", "version", "source_field"),
        {"schema": "sikkim"}
    )

    mapping_id = Column(BigInteger, primary_key=True, autoincrement=True)
    source_id = Column(String, ForeignKey("sikkim.sources.source_id", ondelete="CASCADE"), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    source_field = Column(String, nullable=False)
    target_field = Column(String, nullable=False)
    transform = Column(String, nullable=True)
    created_by = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)


class YearCoverage(Base):
    __tablename__ = "year_coverage"
    __table_args__ = {"schema": "sikkim"}

    year = Column(SmallInteger, primary_key=True)
    handoff_class = Column(String, nullable=False)
    inventory_exists = Column(Boolean, nullable=False)
    geometry_held = Column(Boolean, nullable=False)
    extent_held = Column(Boolean, nullable=False)
    usable_for_denominator = Column(Boolean, nullable=False)
    contributing_sources = Column(ARRAY(String), nullable=True)
    trigger_regime = Column(String, nullable=True)
    trigger_confidence = Column(String, nullable=True)
    notes = Column(Text, nullable=True)


class ObservationExtent(Base):
    __tablename__ = "observation_extents"
    __table_args__ = (
        UniqueConstraint("source_id", "year", "season"),
        {"schema": "sikkim"}
    )

    extent_id = Column(BigInteger, primary_key=True, autoincrement=True)
    source_id = Column(String, ForeignKey("sikkim.sources.source_id"), nullable=False)
    year = Column(SmallInteger, nullable=False)
    season = Column(String, nullable=True)
    trigger_regime = Column(String, nullable=True)
    sensor = Column(String, nullable=True)
    min_mapping_unit_m2 = Column(Numeric, nullable=True)
    extent_basis = Column(String, nullable=False, default="unknown")
    extent_is_approximate = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False)
    notes = Column(Text, nullable=True)


class LandslideEvent(Base):
    __tablename__ = "landslide_events"
    __table_args__ = {"schema": "sikkim"}

    event_id = Column(String, primary_key=True) # UUID string
    raw_id = Column(BigInteger, nullable=True)
    import_id = Column(String, nullable=False)
    source = Column(String, ForeignKey("sikkim.sources.source_id"), nullable=False)
    source_id = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    source_publication = Column(String, nullable=True)
    provenance = Column(String, nullable=False)

    date_start = Column(Date, nullable=True)
    date_end = Column(Date, nullable=True)
    date_precision = Column(String, nullable=True)
    observation_year = Column(SmallInteger, nullable=True)
    year = Column(SmallInteger, nullable=True)
    month = Column(SmallInteger, nullable=True)
    season = Column(String, nullable=True)

    district_current = Column(String, nullable=True)
    district_at_event_time = Column(String, nullable=True)
    district_as_reported = Column(String, nullable=True)
    location_name = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    geometry_type = Column(String, nullable=True)
    position_accuracy_m = Column(Numeric, nullable=True)

    landslide_type = Column(String, nullable=True)
    trigger = Column(String, nullable=True)
    area_m2 = Column(Numeric, nullable=True)
    area_basis = Column(String, nullable=True)

    road_name = Column(String, nullable=True)
    nearest_road = Column(String, nullable=True)
    distance_to_road_m = Column(Numeric, nullable=True)

    validation_status = Column(String, nullable=False, default="pending")
    confidence = Column(String, nullable=True)
    inventory_type = Column(String, nullable=True)
    original_dataset = Column(String, nullable=True)
    duplicate_group_id = Column(String, nullable=True)
    is_group_representative = Column(Boolean, nullable=False, default=False)
    representative_method = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)


class RoadImpactReport(Base):
    __tablename__ = "road_impact_reports"
    __table_args__ = {"schema": "sikkim"}

    report_id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(String, ForeignKey("sikkim.landslide_events.event_id"), nullable=True)
    source_id = Column(String, ForeignKey("sikkim.sources.source_id"), nullable=False)
    road_name = Column(String, nullable=False)
    chainage_km = Column(Numeric, nullable=True)
    impact_type = Column(String, nullable=False) # 'blocked', 'damaged', 'washed_out'
    reported_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)


class GridCell(Base):
    __tablename__ = "grid_cells"
    __table_args__ = {"schema": "sikkim"}

    cell_id = Column(BigInteger, primary_key=True, autoincrement=True)
    cell_code = Column(String, unique=True, nullable=False)
    area_m2 = Column(Numeric, nullable=False)
    district_current = Column(String, nullable=True)


class CellYearObservation(Base):
    __tablename__ = "cell_year_observations"
    __table_args__ = (
        CheckConstraint(
            "observation_status != 'NOT_OBSERVED' OR (landslide_count IS NULL AND landslide_area_m2 IS NULL AND denominator_eligible = FALSE)",
            name="check_not_observed_semantics"
        ),
        CheckConstraint(
            "observation_status != 'PARTIALLY_OBSERVED' OR denominator_eligible = FALSE",
            name="check_partially_observed_semantics"
        ),
        CheckConstraint(
            "observation_status != 'OBSERVED' OR denominator_eligible = TRUE",
            name="check_observed_semantics"
        ),
        {"schema": "sikkim"}
    )

    cell_id = Column(BigInteger, ForeignKey("sikkim.grid_cells.cell_id"), primary_key=True)
    year = Column(SmallInteger, primary_key=True)
    observation_status = Column(String, nullable=False) # 'NOT_OBSERVED','PARTIALLY_OBSERVED','OBSERVED'
    observed_fraction = Column(Numeric, nullable=False, default=0.0)
    denominator_eligible = Column(Boolean, nullable=False, default=False)
    trigger_regime = Column(String, nullable=True)
    landslide_count = Column(Integer, nullable=True)
    landslide_area_m2 = Column(Numeric, nullable=True)
    source_ids = Column(ARRAY(String), nullable=True)


class HotspotMetric(Base):
    __tablename__ = "hotspot_metrics"
    __table_args__ = (
        CheckConstraint(
            "(observed_years < 2 AND recurrence_index IS NULL) OR (observed_years >= 2 AND recurrence_index IS NOT NULL)",
            name="recurrence_needs_observation"
        ),
        {"schema": "sikkim"}
    )

    cell_id = Column(BigInteger, ForeignKey("sikkim.grid_cells.cell_id"), primary_key=True)
    computed_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    window_start_year = Column(SmallInteger, nullable=False)
    window_end_year = Column(SmallInteger, nullable=False)
    landslide_count = Column(Integer, nullable=False)
    landslide_density = Column(Numeric, nullable=True)
    mapped_area_m2 = Column(Numeric, nullable=True)
    observation_years_with_records = Column(SmallInteger, nullable=False, default=0)
    active_years = Column(SmallInteger, nullable=False, default=0)
    observed_years = Column(SmallInteger, nullable=False, default=0)
    recurrence_index = Column(Numeric, nullable=True)
    recurrence_class = Column(String, nullable=False, default="NOT_OBSERVED")
    weakest_extent_basis = Column(String, nullable=False, default="unknown")
    hotspot_index = Column(Numeric, nullable=True)
    hotspot_class = Column(String, nullable=True)
    trigger_regimes = Column(ARRAY(String), nullable=True)
