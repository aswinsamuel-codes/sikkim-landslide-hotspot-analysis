# Sikkim Landslide Hotspot Analysis

> **Module:** SIH26001 — Sikkim Historical Landslide Intelligence & Hotspot Mapping System  
> **Baseline Version Tag:** `v0.1-sikkim-inventory` | **Verified Baseline Commit:** `d3e94cf`  
> **Status:** **PHASE 2D COMPLETED & LOCKED** (Data/GIS Inventory Foundation)

---

## 1. Project Overview

This repository provides the spatial, temporal, and database foundation for the **Sikkim Landslide Hotspot Analysis** project. It establishes an audited, reproducible geospatial pipeline for historical landslide inventory cataloguing, geometry ingestion, spatial grid density calculation, and observation coverage accounting across the state of Sikkim, India.

> [!IMPORTANT]
> **SYSTEM SCOPE STATEMENT:**  
> This repository represents the **data and GIS inventory foundation** for historical landslide observations in Sikkim. It is **NOT** a operational disaster early-warning system, real-time forecasting tool, or active landslide hazard prediction platform.

### Quick-Start Summary

```bash
# 1. Clone repository & setup environment
git clone https://github.com/aswinsamuel-codes/sikkim-landslide-hotspot-analysis.git
cd "sikkim-landslide-hotspot-analysis"
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install shapely fastapi uvicorn pillow

# 2. Run complete test suite (43 verified unit tests)
python -m unittest discover -s backend/tests -p "test_*.py" -v

# 3. Download raw Zenodo inventory & execute Phase 2D GIS QA grid generator
python scripts/download_zenodo_8169506.py
python scripts/generate_inventory_density_grid.py
```

### What This Repository Does NOT Currently Do

> [!WARNING]
> **SCOPE BOUNDARIES & UNIMPLEMENTED CAPABILITIES:**  
> * **No Real-Time Forecasting:** Does NOT predict future landslide events or issue real-time disaster alerts.
> * **No Susceptibility Modeling:** Does NOT generate landslide susceptibility maps or probability surfaces.
> * **No Machine Learning Predictions:** Contains zero trained ML models, neural networks, or hazard forecasting models.
> * **No Recurrence Scoring:** Does NOT calculate temporal recurrence rates, failure frequencies, or return periods.
> * **No Statewide Inventory Coverage:** Does NOT hold complete, statewide landslide geometries for all districts of Sikkim.

---

## 2. Current Status

The project follows a multi-phase implementation roadmap governed by strict scientific research contracts. **Phases 0 through 2D have been completed and verified.**

| Phase | Description | Status | Verification Summary |
| :--- | :--- | :---: | :--- |
| **Phase 0** | Research Constraints & Field Semantics Contract | **COMPLETED** | Established 10 non-negotiable research rules and field semantics |
| **Phase 1** | PostgreSQL / PostGIS Database Foundation | **COMPLETED** | DDL schema (`db/schema.sql`), source cataloguing & FastAPI endpoints |
| **Phase 2A** | Dataset Acquisition & Forensic Inspection | **COMPLETED** | Verified Zenodo 8169506 structure, projection, and metadata integrity |
| **Phase 2B** | Boundary & Inventory Layer Preparation | **COMPLETED** | Standardized 507 source features into WGS84 (`EPSG:4326`) |
| **Phase 2C-A** | Spatial Geometry QA & Inventory Ingest | **COMPLETED** | 100% geometry validity & Sikkim boundary containment verified |
| **Phase 2C-B** | Temporal Observation Analysis | **COMPLETED** | Extracted 11 distinct imagery observation years without event-date mapping |
| **Phase 2D** | Inventory Feature Density & Final GIS QA | **COMPLETED** | 1 km² projected UTM grid (`EPSG:32645`), true centroids, area conservation QA |

**Current Baseline Release Tag:** `v0.1-sikkim-inventory`  
**Current Verified Commit:** `d3e94cf`

---

## 3. Important Scientific & Data Limitations

> [!CAUTION]
> **MANDATORY SCIENTIFIC LIMITATIONS & DATA DISCLAIMERS:**
>
> 1. **Inventory Completeness:** The currently held landslide inventory (Zenodo 8169506) is **localized to Southern and Central Sikkim** (~2,962 km² study area). It is **NOT** a statewide-complete inventory of Sikkim.
> 2. **Unmapped Area Semantics (`DATA_NOT_HELD`):** Grid cells outside the mapped study footprint are classified as `DATA_NOT_HELD` (`coverage_fraction = 0.0`). Unmapped areas indicate that imagery observations were **not conducted**, **NOT** that zero landslides occurred or that landslide risk is zero.
> 3. **Zero Recurrence-Eligible Years:** Currently held datasets contain **zero (0) recurrence-eligible observation years** under research contract rules. Temporal observations cannot be used to model recurrence rates or return intervals.
> 4. **Observation Year vs. Failure Date:** `observation_year` in the Zenodo dataset represents the **satellite imagery acquisition year**, **NOT** the physical landslide failure date.
> 5. **Localized Dataset Bounds:** The Zenodo dataset covers specific Google Earth and Cartosat satellite footprints. It must **never** be presented as a statewide annual inventory for Sikkim.
> 6. **Cartosat Derived Unions:** The 23 derived Cartosat scarp/deposit unions represent **spatially inferred associations**, **NOT** confirmed separate unique landslide events. They are strictly excluded from source feature tallies.
> 7. **Grid Density Semantics:** `centroid_assigned_inventory_feature_density_per_km2` is a **descriptive count of mapped features** assigned per nominal 1 km² grid cell. It is **NOT** a landslide failure probability, hazard score, or risk index.
> 8. **Unimplemented Models:** No susceptibility models, ML hazard predictions, recurrence scores, or forecasting algorithms are implemented in this version.

---

## 4. Data Sources & Provenance

The repository catalogues 15 external data sources classified under strict provenance and readiness tiers:

| Source ID | Dataset Name | Organization | Provenance Tier | Status | Local Geometry Held? |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **`ZENODO_8169506`** | Sikkim Multi-Temporal Remote Sensing Inventory (2011–2019) | Heijenk et al. / Zenodo | Tier C | **Acquired & Processed** | **YES** (507 source features) |
| **`OSM_SIKKIM`** | OpenStreetMap Sikkim Road Network Extract | OSM / Geofabrik | Tier D | Catalogued for Road Ingest | NO (Road Vector File Not Stored in Git) |
| **`NRSC_2011`** | NRSC Post-Earthquake Landslide Inventory (18 Sep 2011) | NRSC / ISRO | Tier A | Metadata Registered | NO (NRSC Request Pending) |
| **`NRSC_2014`** | NRSC Seasonal Monsoon Landslide Inventory (2014) | NRSC / ISRO | Tier A | Metadata Registered | NO (NRSC Request Pending) |
| **`NRSC_2017`** | NRSC Seasonal Monsoon Landslide Inventory (2017) | NRSC / ISRO | Tier A | Metadata Registered | NO (NRSC Request Pending) |
| **`NRSC_2023`** | NRSC Seasonal & GLOF Cascade Inventory (2023) | NRSC / ISRO | Tier A | Metadata Registered | NO (NRSC Request Pending) |
| **`ZENODO_19421112`** | IIT Dhanbad Sikkim Inventory Package (282 MB) | IIT Dhanbad / Zenodo | Tier B | **Quarantined** | NO (Archive Pending Ingest) |
| **`COPERNICUS_DEM_GLO_30`** | Copernicus DEM GLO-30 Digital Elevation Model | ESA / Copernicus | Tier A | Decision Registered | NO (Pending Phase 8) |
| **`ERA5_LAND`** | ERA5-Land Hourly Land Surface Reanalysis Rainfall | ECMWF / Copernicus | Tier A | Decision Registered | NO (Pending Phase 8) |
| **`CHIRPS_V3`** | CHIRPS v3 Daily Rainfall (0.05°) | UCSB CHC | Tier B | Decision Registered | NO (Pending Phase 8) |
| **`GPM_IMERG`** | GPM IMERG Half-Hourly Near-Real-Time Precipitation | NASA / PPS | Tier A | Reserved Operational | NO (Reserved Operational) |
| **`IMD_025DEG`** | IMD 0.25° Daily Gridded Rainfall | IMD | Tier A | Validation Reference | NO (Reference Only) |
| **`GHS_POP`** | Global Human Settlement Layer Population (GHS-POP) | European Commission JRC | Tier A | Catalogued | NO (Pending Exposure Phase) |
| **`NASA_COOLR`** | NASA Global Landslide Repository (COOLR) | NASA GSFC | Tier C | Catalogued | NO (Sparse Points) |
| **`GHOSH_2012`** | 2011 Sikkim Earthquake Landslide Benchmark | Research Literature | Tier B | Literature Benchmark | NO (No Published Geometries) |

---

## 5. Repository Structure

```
sikkim-landslide-hotspot-analysis/
├── backend/                        # FastAPI REST API & core domain logic
│   ├── api/                        # API route handlers (coverage status, catalogued sources, baseline system endpoints)
│   ├── core/                       # Core configuration, database connection, and research constraints
│   ├── domain/                     # Domain models, enums, and coverage matrix definitions
│   └── tests/                      # Suite of 43 automated unit tests
├── data/
│   ├── metadata/                   # Field semantics contract & coverage matrix CSVs
│   ├── raw/                        # Local raw downloads (git-ignored except base boundary)
│   │   └── boundaries/             # WGS84 Sikkim state boundary GeoJSON
│   └── derived/                    # Reproducible GIS build artifacts (git-ignored)
│       └── density/                # Derived 1 km x 1 km density grid GeoJSON layers
├── db/
│   └── schema.sql                  # Canonical PostGIS DDL schema definition
├── exports/                        # Committed QA markdown reports, JSON summaries, and rendered maps
│   ├── INVENTORY_DENSITY_QA.md     # Phase 2D final GIS QA report
│   ├── SPATIAL_QA_REPORT.md        # Phase 2C-A spatial geometry QA report
│   ├── TEMPORAL_OBSERVATION_QA.md  # Phase 2C-B temporal analysis report
│   └── sikkim_*.png                # Rendered GIS maps (density & temporal distribution)
├── scripts/                        # Standalone GIS processing, QA, and visualization scripts
│   ├── generate_inventory_density_grid.py  # Phase 2D grid generation & Shapely area conservation
│   ├── analyze_temporal_observations.py    # Temporal observation breakdown script
│   ├── download_zenodo_8169506.py          # Automated raw dataset acquisition script
│   └── init_db.py                          # Database seeding & metadata registration script
├── .gitignore                      # Minimal repository hygiene exclusion rules
├── PHASE1_DATA_RESEARCH_REPORT.md  # Detailed Phase 1 data architecture research report
├── schema.sql                      # Root schema reference copy (untracked in Git)
├── SIKKIM_LANDSLIDE_DATA_COVERAGE_MATRIX.csv # Master source coverage matrix
└── SIKKIM_YEAR_COVERAGE.csv        # Master observation year eligibility matrix
```

### Version Control Exclusion Policy (`.gitignore`)
* **`data/raw/`**: Excluded to avoid re-committing external third-party raw datasets. Reproducible via `scripts/download_zenodo_8169506.py`.
* **`data/derived/`**: Excluded because all derived GeoJSON grids (~46 MB) are 100% deterministically reproducible using `scripts/generate_inventory_density_grid.py`.
* **`scratch/`**: Excluded to isolate local temporary scripts, zip archives, and raw boundary downloads.
* **`exports/`**: Light-weight QA reports (`.md`, `.json`) and rendered maps (`.png`) are committed to track documentation history.

---

## 6. Technical Stack

* **Database & Spatial Engine:** PostgreSQL 15+ with PostGIS 3.3+ extension
* **Programming Language & GIS Libraries:** Python 3.11+, Shapely 2.1.2 (Exact projected 2D polygon intersection & area integration)
* **Web Framework & API Engine:** FastAPI 0.100+, Uvicorn (ASGI web application)
* **Cartographic Rendering:** Python Imaging Library (Pillow) for high-resolution PNG map generation
* **Testing Framework:** Python standard `unittest` library (43 passing unit tests)

---

## 7. Data Model & Semantics

The project strictly enforces the field semantics defined in `data/metadata/field_semantics.json`:

1. **Observation Year vs. Failure Year:** `observation_year` is defined as the satellite imagery observation date. Mapping `observation_year` to an event failure date (`date_start`) is strictly forbidden.
2. **Observation Coverage Statuses:**
   * `OBSERVED` ($\text{coverage\_fraction} \ge 0.50$): Grid cell has at least 50% mapped extent coverage.
   * `PARTIALLY_COVERED` ($0.0 < \text{coverage\_fraction} < 0.50$): Cell intersects boundary or study area edge; numerator preserved, denominator ineligible.
   * `DATA_NOT_HELD` ($\text{coverage\_fraction} = 0.00$): Cell is unmapped. Attributes evaluate to `NULL` (never assigned zero observations).
3. **Recurrence Eligibility:** Requires verified multi-year baseline imagery covering the same cell. Under current held datasets, 0 observation years are recurrence-eligible.
4. **Derived vs. Source Features:** Source features (507) represent raw mapped geometry outputs. Spatially inferred associations (23 Cartosat unions) are tagged `DERIVED_SPATIAL_ASSOCIATION` and excluded from source feature counts.

---

## 8. Current Landslide Inventory Breakdown

The verified inventory (Zenodo 8169506) contains **507 source inventory features** standardized into `EPSG:4326`:

| Source Feature Layer | Feature Count | Geometry Type | Spatial Coverage | Notes |
| :--- | :---: | :---: | :--- | :--- |
| **Google Earth Polygons** | **255** | Polygon / MultiPolygon | Southern / Central Sikkim | Visualized mapped scarps/deposits |
| **Google Earth Points** | **185** | Point | Southern / Central Sikkim | Centroid points of mapped landslides |
| **Cartosat Polygons** | **67** | Polygon | Southern Sikkim Footprint | Cartosat mapped features |
| **Total Source Inventory** | **507** | — | — | **Conserved exactly in all grid processing** |
| *Cartosat Derived Unions* | *23* | MultiPolygon | Southern Sikkim | *Spatially inferred unions (EXCLUDED from source count)* |
| *Google Earth Mapped Extent* | *1* | Polygon | Southern / Central Sikkim | *Study area footprint polygon (2,962.15 km²)* |

---

## 9. Spatial Density Analysis (Phase 2D)

Spatial density analysis is conducted on a uniform **1 km × 1 km grid** in projected metric coordinates (**`EPSG:32645`** / UTM Zone 45N):

* **Grid Dimensions:** 89 columns × 118 rows (7,355 grid cells intersecting the Sikkim state boundary).
* **Feature Assignment:** Each source feature is assigned to **exactly one grid cell** using its true geometric centroid calculated in projected `EPSG:32645`.
* **Density Metric:** `centroid_assigned_inventory_feature_density_per_km2` $= \frac{N_{\text{source}}}{1.0\text{ km}^2}$. Uses the nominal 1 km² grid-cell area as denominator; `in_state_area_km2` is reported separately for boundary cells and never substituted.

### Phase 2D Verified Area Conservation QA Results

* **GADM v4.1 Sikkim State Boundary Area (EPSG:32645):** `7,081.540805 km²`
* **Sum of Grid-Cell In-State Area Intersections:** `7,079.477653 km²` (`7,079.48 km²` rounded)
* **Boundary Area Conservation Error:** Absolute = `2.063151 km²` | Relative = **`0.029134%`** (Tolerance `< 0.50%` $\implies$ **PASSED**)
* **Reference Administrative Area:** `~7,096.00 km²` (*GADM polygon area and reference administrative area differ by ~14.46 km² / 0.20% and are reported separately as non-matching*).
* **Zenodo 8169506 Mapped Extent Polygon Area (Shapely):** `2,962.146802 km²`
* **Sum of Grid-Cell Mapped Extent Intersections (Shapely):** `2,956.609750 km²`
* **Mapped-Extent Area Conservation Error:** Absolute = `5.537052 km²` | Relative = **`0.186927%`** (Tolerance `< 0.50%` $\implies$ **PASSED WITH SHAPELY CROSS-CHECK**).

---

## 10. Temporal Observation Analysis

The Zenodo 8169506 dataset contains **11 distinct imagery observation years** (2002–2019):

* **Observation Years Present:** `2002, 2005, 2006, 2009, 2010, 2011, 2012, 2015, 2017, 2018, 2019`.
* **2011 Imagery Observation Count:** 189 features (152 GE polygons + 37 GE points). Represents the **highest imagery observation count** in this specific dataset (post-2011 Sikkim earthquake satellite imagery mapping context). It does **NOT** represent total landslide occurrences or failure event dates.
* **Unparsed / Active Records:** 212 features contain non-year temporal strings (e.g. `'Active'`, `'Definite | Active'`). These are safely stored in `source_attributes` JSONB with `observation_year = NULL`.

---

## 11. Reproducibility Guide

### Running Analysis & Reproducing Derived Artifacts

> [!NOTE]  
> Generating derived spatial outputs requires external raw data downloads. Third-party raw input files are intentionally not stored in Git.

### 1. Prerequisites & Environment Setup
```bash
git clone https://github.com/aswinsamuel-codes/sikkim-landslide-hotspot-analysis.git
cd "sikkim-landslide-hotspot-analysis"

python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install shapely fastapi uvicorn pillow
```

### 2. Download Raw Zenodo Dataset
```bash
python scripts/download_zenodo_8169506.py
```
*Downloads 35 shapefiles and metadata files from Zenodo Record 8169506 into `data/raw/zenodo_8169506/`.*

### 3. Database Initialization (Optional PostGIS Setup)
```bash
# Requires local PostgreSQL/PostGIS running on localhost:5432
python scripts/init_db.py
```

### 4. Execute GIS QA & Density Grid Generation
```bash
python scripts/generate_inventory_density_grid.py
python scripts/analyze_temporal_observations.py
```
*Calculates true geometric centroids, performs Shapely metric area conservation checks, regenerates GeoJSON density layers, and renders high-resolution PNG maps into `exports/`.*

---

## 12. Testing & Quality Assurance

The project enforces quality control through **43 automated unit tests**:

```bash
python -m unittest discover -s backend/tests -p "test_*.py" -v
```

```
Ran 43 tests in 0.523s
OK
```

### What the Test Suite Protects Against
* **`test_zenodo_observation_year_not_used_as_event_year`:** Prevents mapping imagery observation years to event failure dates (`date_start`).
* **`test_not_observed_has_null_counts`:** Ensures `DATA_NOT_HELD` cells evaluate to `NULL` (never assigned zero observations).
* **`test_boundary_area_conservation_and_tolerance`:** Asserts boundary area relative error is within `< 0.50%` tolerance.
* **`test_extent_area_conservation_and_tolerance`:** Asserts mapped extent area relative error is within `< 0.50%` tolerance.
* **`test_source_507_feature_conservation`:** Enforces exact conservation of all 507 source inventory features.
* **`test_derived_union_exclusion`:** Confirms 23 derived Cartosat unions do not inflate source feature tallies.
* **`test_baseline_model_excludes_density_and_recurrence`:** Guards against injecting density or unverified recurrence into baseline models.

---

## 13. Committed Outputs & Artifacts

Lightweight QA documentation and rendered GIS maps are committed in `exports/`:

* **`exports/INVENTORY_DENSITY_QA.md`:** Phase 2D final GIS QA report with Shapely area conservation metrics.
* **`exports/SPATIAL_QA_REPORT.md`:** Phase 2C-A spatial geometry validity and boundary containment audit.
* **`exports/TEMPORAL_OBSERVATION_QA.md`:** Phase 2C-B temporal observation breakdown and overlap analysis.
* **`exports/NRSC_DATA_REQUEST_LETTER.md`:** Formal research data request letter for NRSC/ISRO geometry datasets.
* **`exports/sikkim_inventory_feature_density_map.png`:** High-resolution map of centroid-assigned feature density per 1 km² grid.
* **`exports/sikkim_observation_year_distribution_map.png`:** High-resolution map of distinct observation years per 1 km² grid.

---

## 14. Git & Versioning Policy

* **Main Branch:** `main`
* **Baseline Commit:** `d3e94cf`
* **Baseline Tag:** `v0.1-sikkim-inventory`
* **Data Exclusion Policy:** Large raw shapefiles (`data/raw/`), temporary scratch files (`scratch/`), and reproducible build outputs (`data/derived/`) are strictly ignored by `.gitignore`.

---

## 15. Project Roadmap

### Completed Work (Phases 0 — 2D)
- [x] Phase 0: Research semantic contracts & non-negotiable rules.
- [x] Phase 1: PostgreSQL/PostGIS database schema DDL & FastAPI foundation.
- [x] Phase 2A/2B: Zenodo 8169506 geometry standardization (507 features into EPSG:4326).
- [x] Phase 2C-A: Spatial geometry validity & Sikkim boundary containment audit (100% inside).
- [x] Phase 2C-B: Temporal imagery observation breakdown (11 distinct years).
- [x] Phase 2D: Inventory feature density grid (1 km² EPSG:32645 UTM grid) & Shapely area conservation QA.

### Future Work (Phases 3 — 8) — *NOT YET IMPLEMENTED*
- [ ] **Phase 3:** Authoritative inventory acquisition (NRSC/ISRO vector geometry ingest).
- [ ] **Phase 4:** Observation coverage expansion & multi-source alignment.
- [ ] **Phase 5:** Recurrence analysis (once denominator-eligible multi-year Baselines exist).
- [ ] **Phase 6:** Spatial hotspot analysis.
- [ ] **Phase 7:** Landslide susceptibility & environmental factor modeling (DEM, slope, rainfall).
- [ ] **Phase 8:** Machine learning hazard models & predictive forecasting.

---

## 16. Responsible Interpretation

> [!CAUTION]
> **RESPONSIBLE DATA USE GUIDELINES:**  
> * **Absence of Evidence vs. Evidence of Absence:** The absence of a mapped landslide in this inventory does **NOT** prove that no landslide occurred. Unmapped areas simply lack held observation data.
> * **Density vs. Hazard:** Inventory feature density reflects spatial mapping concentration in the study area. It must **never** be interpreted as landslide failure probability, hazard susceptibility, or risk.

---

## 17. Licensing, Data Usage & Attribution

* **Repository Code & Documentation:** No separate repository-wide open-source license has been declared yet for this repository codebase. Third-party datasets retain their respective original licenses and usage restrictions.
* **Zenodo 8169506 Dataset:** Creative Commons Attribution (**CC BY 4.0**). *Attribution: Heijenk et al. (2024).*
* **OpenStreetMap Road Data:** Open Database License (**ODbL 1.0**). *Attribution: © OpenStreetMap contributors.*
* **GADM Administrative Boundaries:** Restricted to **academic and non-commercial research use only**. Redistribution of raw GADM archives is prohibited.

---

## 18. Acknowledgements & References

1. **Heijenk et al. (2024):** *Multi-temporal remote sensing landslide inventory for Sikkim, India.* Zenodo. DOI: [10.5281/zenodo.8169506](https://doi.org/10.5281/zenodo.8169506).
2. **Martha et al. (2014):** *Landslides triggered by the Wenchuan and Sikkim earthquakes.* NRSC / ISRO Technical Report.
3. **GADM:** *Global Administrative Areas, Version 4.1.* [gadm.org](https://gadm.org).
4. **Copernicus DEM:** European Space Agency (ESA) Copernicus Digital Elevation Model (GLO-30).
