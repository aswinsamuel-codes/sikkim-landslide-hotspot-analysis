# Phase 4 — Authoritative Sikkim Landslide Inventory Acquisition Audit Report

**Project:** Sikkim Landslide Hotspot Analysis  
**Module:** SIH26001 — Historical Landslide Intelligence Pipeline  
**Date:** 2026-09-13 21:45:05  
**Status:** **ACQUISITION AUDIT COMPLETE — AUTHORITATIVE SOURCE ACQUISITION PENDING**  

---

## 1. Executive Summary & Core Principles

Phase 4 focuses on evaluating, acquiring, tracking provenance for, and integrating legitimately obtainable Sikkim landslide inventory geometries into the historical mapping pipeline.

### Core Scientific & Data Principles Enforced:
1. **Source Authority ≠ Spatial Completeness:** Legitimate institutional datasets (e.g. NRSC, GSI) are authoritative, but their absence from unauthenticated public endpoints does not mean data does not exist.
2. **Mapped Absence ≠ Landslide Absence (`DATA_NOT_HELD`):** Grid cells outside mapped footprints indicate **unobserved areas**, **NEVER** zero landslide hazard.
3. **Imagery Observation Year ≠ Landslide Failure Date:** Satellite imagery acquisition dates (`observation_year`) must **NEVER** be converted into physical event failure dates (`date_start = NULL`).
4. **Bounding-Box Overlap ≠ Confirmed Duplicate:** Candidate spatial overlaps are indexed via `group_id` without deleting or merging raw source rows.
5. **No Geometry Fabrication:** No GIS shapefiles are reconstructed or fabricated from PDF reports, summary counts, or WMS raster tiles.

---

## 2. Source-by-Source Forensic Acquisition Audit Matrix

| Source ID | Access Status | Data Avail? | Geom Avail? | Format | CRS | Sikkim Coverage | Temporal Semantics | License | Tier | Role | Acquisition Status |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **`ZENODO_8169506`** | Public Download | YES | YES | Shapefile (Poly/Pt) | EPSG:4326 | Partial South/Central (~2,962 km²) | Imagery Observation Year | CC-BY-4.0 | Tier C | Held Primary Baseline | **ACQUIRED_AND_PROCESSED** |
| **`NRSC_2011`** | Requisition Required | YES | NO (PDF/WMS) | Bhuvan Viewer / PDF | EPSG:4326 | Statewide (~4,105 km²) | Event Date (2011-09-18) | Restricted Govt | Tier A | Primary Event Inventory | **ACQUISITION_PENDING** |
| **`NRSC_2014`** | Requisition Required | YES | NO (WMS) | Bhuvan Viewer / WMS | EPSG:4326 | Statewide Monsoon | Seasonal Monsoon | Restricted Govt | Tier A | Recurrence Contributor | **ACQUISITION_PENDING** |
| **`NRSC_2017`** | Requisition Required | YES | NO (WMS) | Bhuvan Viewer / WMS | EPSG:4326 | Statewide Monsoon | Seasonal Monsoon | Restricted Govt | Tier A | Recurrence Contributor | **ACQUISITION_PENDING** |
| **`NRSC_2023`** | Requisition Required | YES | NO (WMS) | Bhuvan / NDEM | EPSG:4326 | Statewide Monsoon + GLOF | Multi-Trigger Regime | Restricted Govt | Tier A | Primary Event & Seasonal | **ACQUISITION_PENDING** |
| **`GSI_BHUSANKET`** | Public Web GIS Portal | NO (Vector) | NO (Vector) | WMS Tiles / PDF | Unknown | Site-Specific Incidents | Event Incidence Date | Govt View Only | Tier A | Research / High Priority | **ACQUISITION_PENDING** |
| **`ZENODO_19421112`** | Public Download | YES | NO (Inventory) | RAR Archive (282 MB) | EPSG:4326 | Statewide Susceptibility | Static Factors | NOT_DECLARED_ON_RECORD | Tier B | Quarantined Susceptibility | **QUARANTINED** |
| **`NASA_COOLR`** | Public Download | YES | YES | GeoJSON (Points) | EPSG:4326 | Sparse Points (2 points) | Reported Event Date | Public Domain | Tier C | Secondary Validation Only | **ACQUIRED_AND_PROCESSED** |
| **`OSM_SIKKIM`** | Public Download | YES | YES | Shapefile / PBF | EPSG:4326 | Statewide Infrastructure | Edit Timestamp | ODbL | Tier D | Exposure Reference | **CATALOGUED_FOR_INFRASTRUCTURE** |
| **`GADM_SIKKIM_BOUNDARY`** | Local GeoJSON | YES | YES | GeoJSON (MultiPoly) | EPSG:4326 | Statewide Boundary | Boundary Version 2021 | GADM Non-Comm | Tier A | Administrative Mask | **ACQUIRED_AND_PROCESSED** |

---

## 3. Detailed Forensic Findings by Target Dataset

### 3.1 NRSC / ISRO / NDEM Datasets (2011, 2014, 2017, 2023)
- **Status:** **ACQUISITION_PENDING**
- **Inspection Findings:** NRSC publishes landslide inventory maps and summary reports on Bhuvan and NDEM portals. However, **no direct unauthenticated bulk vector GIS shapefile download links exist**. Numerical landslide counts in PDF reports (e.g. 1,196 landslides in 2011) do **NOT** constitute spatial GIS geometry.
- **Formal Requisition:** A formal data requisition request (`exports/NRSC_DATA_REQUEST_LETTER.md`) has been prepared for institutional clearance. Zero geometry will be fabricated from PDF counts.

### 3.2 Geological Survey of India (GSI Bhusanket / Bhooskhalan)
- **Status:** **ACQUISITION_PENDING**
- **Inspection Findings:** Inspected portal endpoints (`https://bhukosh.gsi.gov.in`, `https://bhukosh.gsi.gov.in/bhusanket`, `https://landslides.gsi.gov.in/bhooskhalan`). **No bulk vector endpoint was identified during the inspected routes.**
- **Compliance Wording:** The project strictly avoids claiming that GSI vector endpoints do not exist globally, recording only that no bulk vector export was identified during inspected public routes.

### 3.3 Zenodo 19421112 Sandbox Inspection
- **Status:** **QUARANTINED**
- **Record Title:** *Data for Landslide Susceptibility Mapping in the Sikkim Himalaya* (IIT Dhanbad, 282 MB RAR archive `Sikkim_landslide_susceptibility_data.rar`).
- **License Status:** **`NOT_DECLARED_ON_RECORD`** (No license is declared on the record page; CC-BY-4.0 is not assumed).
- **Inspection Findings:** Archive contains raster/vector spatial factor layers (slope, aspect, elevation, geology, land cover, distance to roads/faults/streams) used as inputs for susceptibility zonation modeling. It does **NOT** contain raw historical landslide event inventory shapefiles.
- **Quarantine Verdict:** Remains quarantined in sandbox (`scratch/sandbox_zenodo_19421112`) and strictly excluded from primary landslide inventory density grids.

### 3.4 NASA COOLR Secondary Validation Layer
- **Status:** **ACQUIRED_AND_PROCESSED**
- **Ingest Details:** 2 point incidents within Sikkim state boundary stored in `data/derived/validation/nasa_coolr_secondary_validation_points_4326.geojson`.
- **Grid Rule:** Tagged `usable_for_density_grid = False`. Strictly excluded from nominal 1 km² polygon feature density grids.

---

## 4. Locked Baseline Conservation Verification

The Phase 2D/Phase 3 locked baseline metrics remain **100% conserved and unmodified**:
- **Total Source Inventory Features:** `507` (255 GE polygons, 185 GE points, 67 Cartosat polygons)
- **Derived Cartosat Unions Excluded:** `23`
- **Recurrence-Eligible Years:** `0`
- **Mapped Extent Area:** `2,962.146802 km²` (Grid sum: `2,956.609750 km²`)
- **Analysis CRS:** `EPSG:32645 (UTM Zone 45N)`
- **Nominal Density Denominator:** `1.0 km²`

---

## 5. Next Steps & Approval Gate

Phase 4 initial acquisition audit is complete. In accordance with Phase 4 rules, full ingestion of any newly acquired dataset will proceed only after this acquisition audit has been reviewed and approved.

---
*Report generated by Phase 4 Acquisition Audit Engine.*
