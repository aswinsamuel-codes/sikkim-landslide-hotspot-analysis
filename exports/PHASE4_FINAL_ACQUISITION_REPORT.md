# Phase 4 Final Acquisition Report & Consolidation Matrix

**Project:** Sikkim Landslide Hotspot Analysis  
**Status:** `ACQUISITION AUDIT & INSPECTION COMPLETE — CONSOLIDATED BASELINE LOCKED`  
**Baseline Freeze Tag:** `v0.2-phase3-provenance-validation` (Commit `907287c`)  

> [!IMPORTANT]
> **Core Compliance Ruling:** No bulk vector endpoint was identified during the inspected routes. WMS raster visualization, web map viewers, PDF summary reports, and susceptibility zoning maps do NOT constitute downloadable spatial GIS vector inventory geometry. Zero geometry has been fabricated.

## 1. Key Principles & Semantic Protections

1. **Observation Year vs. Event Failure Date:** Satellite imagery observation year $\neq$ failure/occurrence date. `event_date` remains strictly `NULL` unless explicitly established by source records.
2. **Missing Geometry vs. Zero Landslides:** Absence of downloadable vector GIS geometry or observation footprint $\neq$ zero landslides. Cells without coverage maintain `DATA_NOT_HELD` or `NOT_OBSERVED` status with `NULL` counts.
3. **Strict Source Distinctions:** Historical event inventory labels are strictly separated from susceptibility factor maps (e.g. Zenodo 19421112, NLSM 1:50,000), web viewer tiles, and summary counts.
4. **Baseline Feature Conservation:** Primary historical inventory remains strictly **507 features** (255 GE polygons, 185 GE points, 67 Cartosat polygons).
5. **Derived Union Exclusion:** The **23 derived Cartosat scarp/deposit spatial associations** remain strictly excluded from density numerators.
6. **Zero Recurrence Eligibility:** Recurrence-eligible observation years remain strictly **0**.

## 2. Consolidated Authoritative Source Matrix

| Source ID | Authority | Dataset Name | Inspected Routes | Vector Geometry Status | Acquisition Disposition | Provenance Tier | Requisition Pathway |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `NRSC_2011` | National Remote Sensing Centre (NRSC) / ISRO | NRSC Sikkim Earthquake Landslide Inventory (2011) | Bhuvan Disaster Portal, ISRO WMS capabilities, NDEM, and official NRSC 2011 event report PDF | `UNAVAILABLE` | `ACQUISITION_PENDING / METADATA_ONLY` | `AUTHORITATIVE_PUBLIC_METADATA` | Formal institutional requisition letter to NRSC/ISRO (exports/NRSC_DATA_REQUEST_LETTER.md) |
| `NRSC_2014` | National Remote Sensing Centre (NRSC) / ISRO | NRSC Seasonal Monsoon Landslide Inventory (2014) | Bhuvan Disaster Management Portal, ISRO Bhuvan WMS Portal, NDEM Monsoon Portal 2014 | `UNAVAILABLE` | `ACQUISITION_PENDING / METADATA_ONLY` | `AUTHORITATIVE_PUBLIC_METADATA` | Formal institutional requisition letter to NRSC/ISRO (exports/NRSC_DATA_REQUEST_LETTER.md) |
| `NRSC_2017` | National Remote Sensing Centre (NRSC) / ISRO | NRSC Seasonal Monsoon Landslide Inventory (2017) | Bhuvan Disaster Management Portal, ISRO Bhuvan WMS Portal, NDEM Monsoon Portal 2017 | `UNAVAILABLE` | `ACQUISITION_PENDING / METADATA_ONLY` | `AUTHORITATIVE_PUBLIC_METADATA` | Formal institutional requisition letter to NRSC/ISRO (exports/NRSC_DATA_REQUEST_LETTER.md) |
| `NRSC_2023` | National Remote Sensing Centre (NRSC) / ISRO | NRSC Seasonal & Mixed-Trigger Landslide Inventory (2023) | Bhuvan Disaster Management Portal, ISRO Bhuvan WMS Portal, NDEM Portal 2023 | `UNAVAILABLE` | `ACQUISITION_PENDING / METADATA_ONLY` | `AUTHORITATIVE_PUBLIC_METADATA` | Formal institutional requisition letter to NRSC/ISRO (exports/NRSC_DATA_REQUEST_LETTER.md) |
| `GSI_BHUSANKET` | Geological Survey of India (GSI) / Ministry of Mines | GSI Bhusanket & Bhooskhalan Landslide Ecosystem | GSI Bhukosh Portal, GSI Bhusanket Interface, GSI Bhooskhalan Portal, GSI NLSM 1:50,000 Interface | `UNAVAILABLE` | `ACQUISITION_PENDING / METADATA_ONLY` | `AUTHORITATIVE_PUBLIC_METADATA` | Formal institutional requisition to Geological Survey of India (GSI) |

## 3. Source-by-Source Summary Notes

### NRSC 2011 (`NRSC_2011`)
- **Scope:** Post-2011 Sikkim Earthquake inventory campaign (1,196 landslides reported in PDF report).
- **Temporal Semantics:** Event occurrence date 2011-09-18 supported by earthquake event.
- **Disposition:** `ACQUISITION_PENDING / METADATA_ONLY` (PDF map & count available; vector GIS shapefile unavailable publicly).

### NRSC 2014 (`NRSC_2014`)
- **Scope:** Seasonal monsoon landslide inventory 2014.
- **Temporal Semantics:** Imagery observation year 2014, `event_date = NULL`.
- **Disposition:** `ACQUISITION_PENDING / METADATA_ONLY` (WMS raster viewer accessible; vector GIS file unavailable publicly).

### NRSC 2017 (`NRSC_2017`)
- **Scope:** Seasonal monsoon landslide inventory 2017.
- **Temporal Semantics:** Imagery observation year 2017, `event_date = NULL`.
- **Disposition:** `ACQUISITION_PENDING / METADATA_ONLY` (WMS raster viewer accessible; vector GIS file unavailable publicly).

### NRSC 2023 (`NRSC_2023`)
- **Scope:** Seasonal monsoon and October 2023 South Lhonak GLOF event mixed-trigger inventory.
- **Temporal Semantics:** Mixed-trigger imagery observation year 2023, `event_date = NULL`.
- **Disposition:** `ACQUISITION_PENDING / METADATA_ONLY` (Bhuvan/NDEM web map layers accessible; vector GIS file unavailable publicly).

### GSI Bhusanket (`GSI_BHUSANKET`)
- **Scope:** GSI Bhusanket, Bhooskhalan, and NLSM 1:50,000 ecosystem.
- **Temporal Semantics:** Occurrence dates preserved for field incident reports when provided; survey/publication dates not mapped to `event_date`.
- **Disposition:** `ACQUISITION_PENDING / METADATA_ONLY` (Web map interactive points & NLSM susceptibility layers viewable; bulk vector inventory unavailable unauthenticated).

---

## 4. Quarantined Susceptibility Datasets

- **Zenodo 19421112:** Classified as `QUARANTINED`. Contains susceptibility factor raster/vector inputs (slope, aspect, elevation), NOT raw historical landslide event inventory labels. License: `NOT_DECLARED_ON_RECORD`.

---

## 5. Verification & Baseline Status

- **Primary Features Conserved:** 507
- **Derived Cartosat Unions Excluded:** 23
- **Recurrence-Eligible Observation Years:** 0
- **Tracked Files Modified:** 0 (`git diff --stat` empty)
- **Final Disposition:** `PHASE 4 CONSOLIDATION COMPLETE — CONSOLIDATED MATRIX LOCKED`