-- ============================================================
-- SIKKIM HISTORICAL LANDSLIDE INTELLIGENCE — Database Schema (Rev 2)
-- SIH26001 · Phase 0 Implementation
-- ============================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SCHEMA IF NOT EXISTS sikkim;
SET search_path TO sikkim, public;

-- Enums
CREATE TYPE provenance_class AS ENUM ('A','B','C','D','E');
CREATE TYPE coverage_status   AS ENUM ('AVAILABLE','PARTIAL','NOT_AVAILABLE');
CREATE TYPE observation_status_type AS ENUM ('NOT_OBSERVED','PARTIALLY_OBSERVED','OBSERVED');
CREATE TYPE validation_state  AS ENUM ('pending','valid','flagged','rejected','outside_sikkim');
CREATE TYPE import_state      AS ENUM ('fetched','parsed','previewed','approved','rejected','failed');
CREATE TYPE measurement_basis AS ENUM ('OBSERVED','DERIVED','ESTIMATED');
CREATE TYPE download_method   AS ENUM ('http_get','http_post','api','wms','manual_admin','file_upload');
CREATE TYPE extent_basis_type AS ENUM ('published_polygon','published_area_figure','assumed_statewide','unknown');
CREATE TYPE match_status_type AS ENUM ('not_assessed','candidate','confirmed','conflicting');

-- 1. SOURCES
CREATE TABLE sources (
    source_id            TEXT PRIMARY KEY,
    name                 TEXT NOT NULL,
    organization         TEXT NOT NULL,
    url                  TEXT,
    description          TEXT,
    coverage_start       DATE,
    coverage_end         DATE,
    coverage_note        TEXT,
    provenance           provenance_class NOT NULL,
    license              TEXT,
    license_allows_redistribution BOOLEAN,
    download_method      download_method NOT NULL,
    requires_auth        BOOLEAN NOT NULL DEFAULT FALSE,
    robots_checked_at    TIMESTAMPTZ,
    robots_allows_fetch  BOOLEAN,
    enabled              BOOLEAN NOT NULL DEFAULT TRUE,
    last_imported_at     TIMESTAMPTZ,
    record_count         INTEGER,
    status               TEXT,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT auth_sources_are_manual
        CHECK (NOT requires_auth OR download_method IN ('manual_admin','file_upload'))
);

CREATE TABLE source_field_mappings (
    mapping_id    BIGSERIAL PRIMARY KEY,
    source_id     TEXT NOT NULL REFERENCES sources(source_id) ON DELETE CASCADE,
    version       INTEGER NOT NULL DEFAULT 1,
    source_field  TEXT NOT NULL,
    target_field  TEXT NOT NULL,
    transform     TEXT,
    created_by    TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, version, source_field)
);

-- 2. IMPORT HISTORY
CREATE TABLE import_runs (
    import_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id          TEXT NOT NULL REFERENCES sources(source_id),
    requested_url      TEXT,
    final_url          TEXT,
    import_time        TIMESTAMPTZ NOT NULL DEFAULT now(),
    detected_format    TEXT,
    content_type       TEXT,
    bytes_downloaded   BIGINT,
    file_hash          TEXT,
    raw_path           TEXT,
    records_found      INTEGER,
    records_imported   INTEGER,
    records_rejected   INTEGER,
    duplicates_found   INTEGER,
    validation_errors  JSONB,
    state              import_state NOT NULL DEFAULT 'fetched',
    approved_by        TEXT,
    approved_at        TIMESTAMPTZ,
    notes              TEXT
);

-- 3. RAW STAGING (Immutable)
CREATE TABLE raw_records (
    raw_id             BIGSERIAL PRIMARY KEY,
    import_id          UUID NOT NULL REFERENCES import_runs(import_id),
    source_id          TEXT NOT NULL REFERENCES sources(source_id),
    original_record_id TEXT,
    payload            JSONB NOT NULL,
    raw_geometry       geometry(Geometry, 4326),
    source_crs         TEXT,
    ingested_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE RULE raw_records_no_update AS ON UPDATE TO raw_records DO INSTEAD NOTHING;
CREATE RULE raw_records_no_delete AS ON DELETE TO raw_records DO INSTEAD NOTHING;

-- 4. GEOGRAPHY
CREATE TABLE districts (
    district_id   BIGSERIAL PRIMARY KEY,
    name          TEXT NOT NULL,
    legacy_name   TEXT,
    valid_from    DATE NOT NULL,
    valid_to      DATE,
    geom          geometry(MultiPolygon, 4326) NOT NULL,
    notes         TEXT,
    UNIQUE (name, valid_from)
);

CREATE TABLE state_boundary (
    id    SMALLINT PRIMARY KEY DEFAULT 1,
    geom  geometry(MultiPolygon, 4326) NOT NULL,
    CHECK (id = 1)
);

-- 5. YEAR COVERAGE MATRIX (Preserves 4 distinct status booleans)
CREATE TABLE year_coverage (
    year                      SMALLINT PRIMARY KEY,
    handoff_class             TEXT NOT NULL,
    inventory_exists          BOOLEAN NOT NULL,
    geometry_held             BOOLEAN NOT NULL,
    extent_held               BOOLEAN NOT NULL,
    usable_for_denominator    BOOLEAN NOT NULL,
    contributing_sources      TEXT[],
    trigger_regime            TEXT,
    trigger_confidence        TEXT,
    notes                     TEXT
);

-- 6. OBSERVATION EXTENTS
CREATE TABLE observation_extents (
    extent_id             BIGSERIAL PRIMARY KEY,
    source_id             TEXT NOT NULL REFERENCES sources(source_id),
    year                  SMALLINT NOT NULL,
    season                TEXT,
    trigger_regime        TEXT,
    mapped_extent         geometry(MultiPolygon, 4326) NOT NULL,
    cloud_mask            geometry(MultiPolygon, 4326),
    sensor                TEXT,
    min_mapping_unit_m2   NUMERIC,
    extent_basis          extent_basis_type NOT NULL DEFAULT 'unknown',
    extent_is_approximate BOOLEAN NOT NULL DEFAULT FALSE,
    status                coverage_status NOT NULL,
    notes                 TEXT,
    UNIQUE (source_id, year, season)
);

-- 7. LANDSLIDE EVENTS
CREATE TABLE duplicate_groups (
    duplicate_group_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    method              TEXT NOT NULL,
    spatial_tolerance_m NUMERIC,
    temporal_tolerance_days INTEGER,
    min_iou             NUMERIC,
    member_count        INTEGER,
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    confidence          TEXT,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE landslide_events (
    event_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_id              BIGINT REFERENCES raw_records(raw_id),
    import_id           UUID NOT NULL REFERENCES import_runs(import_id),
    source              TEXT NOT NULL REFERENCES sources(source_id),
    source_id           TEXT,
    source_url          TEXT,
    source_publication  TEXT,
    provenance          provenance_class NOT NULL,

    date_start          DATE,
    date_end            DATE,
    date_precision      TEXT,
    observation_year    SMALLINT,
    year                SMALLINT,
    month               SMALLINT CHECK (month BETWEEN 1 AND 12),
    season              TEXT,

    district_current     TEXT,
    district_at_event_time TEXT,
    district_as_reported TEXT,
    location_name        TEXT,

    latitude            DOUBLE PRECISION CHECK (latitude BETWEEN -90 AND 90),
    longitude           DOUBLE PRECISION CHECK (longitude BETWEEN -180 AND 180),
    geometry            geometry(Geometry, 4326),
    geometry_type       TEXT,
    position_accuracy_m NUMERIC,

    landslide_type      TEXT,
    trigger             TEXT,
    area_m2             NUMERIC CHECK (area_m2 IS NULL OR area_m2 > 0),
    area_basis          measurement_basis,

    road_name           TEXT,
    nearest_road        TEXT,
    distance_to_road_m  NUMERIC,

    validation_status   validation_state NOT NULL DEFAULT 'pending',
    confidence          TEXT,
    inventory_type      TEXT,
    original_dataset    TEXT,
    duplicate_group_id  UUID REFERENCES duplicate_groups(duplicate_group_id),
    is_group_representative BOOLEAN NOT NULL DEFAULT FALSE,
    representative_method   TEXT,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ROAD IMPACT REPORTS (Source-documented road impacts only)
CREATE TABLE road_impact_reports (
    report_id        BIGSERIAL PRIMARY KEY,
    event_id         UUID REFERENCES landslide_events(event_id),
    source_id        TEXT NOT NULL REFERENCES sources(source_id),
    road_name        TEXT NOT NULL,
    chainage_km      NUMERIC,
    impact_type      TEXT NOT NULL,  -- 'blocked', 'damaged', 'washed_out'
    reported_at      TIMESTAMPTZ,
    notes            TEXT
);

-- 8. HOTSPOT GRID & CELL-YEAR OBSERVATIONS
CREATE TABLE grid_cells (
    cell_id          BIGSERIAL PRIMARY KEY,
    cell_code        TEXT UNIQUE NOT NULL,
    geom             geometry(Polygon, 4326) NOT NULL,
    centroid         geometry(Point, 4326) NOT NULL,
    area_m2          NUMERIC NOT NULL,
    district_current TEXT
);

CREATE TABLE cell_year_observations (
    cell_id           BIGINT NOT NULL REFERENCES grid_cells(cell_id),
    year              SMALLINT NOT NULL,
    observation_status observation_status_type NOT NULL,
    observed_fraction NUMERIC NOT NULL DEFAULT 0.0 CHECK (observed_fraction BETWEEN 0.0 AND 1.0),
    denominator_eligible BOOLEAN NOT NULL DEFAULT FALSE,
    trigger_regime    TEXT,
    landslide_count   INTEGER,
    landslide_area_m2 NUMERIC,
    source_ids        TEXT[],
    PRIMARY KEY (cell_id, year),

    -- Semantic integrity rules:
    -- NOT_OBSERVED => count & area MUST BE NULL, denominator_eligible MUST BE FALSE
    CONSTRAINT check_not_observed_semantics
        CHECK (observation_status != 'NOT_OBSERVED' OR (landslide_count IS NULL AND landslide_area_m2 IS NULL AND denominator_eligible = FALSE)),

    -- PARTIALLY_OBSERVED => denominator_eligible MUST BE FALSE
    CONSTRAINT check_partially_observed_semantics
        CHECK (observation_status != 'PARTIALLY_OBSERVED' OR denominator_eligible = FALSE),

    -- OBSERVED => denominator_eligible MUST BE TRUE
    CONSTRAINT check_observed_semantics
        CHECK (observation_status != 'OBSERVED' OR denominator_eligible = TRUE)
);

CREATE TABLE hotspot_metrics (
    cell_id                      BIGINT PRIMARY KEY REFERENCES grid_cells(cell_id),
    computed_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    window_start_year            SMALLINT NOT NULL,
    window_end_year              SMALLINT NOT NULL,
    landslide_count              INTEGER NOT NULL,
    landslide_density            NUMERIC,
    mapped_area_m2               NUMERIC,
    observation_years_with_records SMALLINT NOT NULL DEFAULT 0,
    active_years                 SMALLINT NOT NULL DEFAULT 0,
    observed_years               SMALLINT NOT NULL DEFAULT 0,
    recurrence_index             NUMERIC,
    recurrence_class             TEXT NOT NULL DEFAULT 'NOT_OBSERVED',
    weakest_extent_basis         extent_basis_type NOT NULL DEFAULT 'unknown',
    hotspot_index                NUMERIC,
    hotspot_class                TEXT,
    trigger_regimes              TEXT[],
    CONSTRAINT recurrence_needs_observation
        CHECK ((observed_years < 2 AND recurrence_index IS NULL)
            OR (observed_years >= 2 AND recurrence_index IS NOT NULL)),
    CONSTRAINT active_within_observed CHECK (active_years <= observed_years)
);

-- 9. ML FEATURES & MODELS
CREATE TABLE cell_features (
    cell_id              BIGINT NOT NULL REFERENCES grid_cells(cell_id),
    feature_epoch        SMALLINT NOT NULL,
    slope_deg            NUMERIC,
    aspect_deg           NUMERIC,
    elevation_m          NUMERIC,
    curvature            NUMERIC,
    relief_m             NUMERIC,
    land_cover_class     TEXT,
    land_cover_epoch     SMALLINT,
    geology_unit         TEXT,
    soil_moisture        NUMERIC,
    dist_to_drainage_m   NUMERIC,
    dist_to_road_m       NUMERIC,
    dist_to_fault_m      NUMERIC,
    rain_1d_mm           NUMERIC,
    rain_3d_mm           NUMERIC,
    rain_7d_mm           NUMERIC,
    rain_15d_mm          NUMERIC,
    rain_30d_mm          NUMERIC,
    rainfall_source      TEXT,
    dem_source           TEXT NOT NULL,
    PRIMARY KEY (cell_id, feature_epoch)
);

CREATE TABLE model_runs (
    model_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              TEXT NOT NULL,
    algorithm         TEXT NOT NULL,
    model_category    TEXT NOT NULL DEFAULT 'baseline', -- 'baseline' | 'experimental'
    trained_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    feature_list      TEXT[] NOT NULL,
    cv_strategy       TEXT NOT NULL,
    holdout_source    TEXT,
    train_years       SMALLINT[],
    metrics           JSONB,
    artifact_path     TEXT NOT NULL,
    output_type       TEXT NOT NULL,
    dem_source        TEXT,
    rainfall_source   TEXT,
    extent_basis_note TEXT,
    notes             TEXT
);

CREATE TABLE model_predictions (
    model_id       UUID NOT NULL REFERENCES model_runs(model_id) ON DELETE CASCADE,
    cell_id        BIGINT NOT NULL REFERENCES grid_cells(cell_id),
    probability    NUMERIC CHECK (probability BETWEEN 0 AND 1),
    risk_class     TEXT,
    contributions  JSONB,
    predicted_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (model_id, cell_id)
);
