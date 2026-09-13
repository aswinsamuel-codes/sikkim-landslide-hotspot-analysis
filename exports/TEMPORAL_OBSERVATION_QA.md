# PHASE 2C-B TEMPORAL OBSERVATION QA REPORT

**Module:** Sikkim Historical Landslide Intelligence & Hotspot Mapping  
**Date:** September 13, 2026  
**Status:** **PASSED — SAFE TEMPORAL SEMANTICS VERIFIED**

> **MANDATORY LIMITATION NOTICE:**  
> *Observation year indicates the year associated with the source imagery/observation record. It is not a confirmed landslide failure date.*

## 1. TEMPORAL INVENTORY BREAKDOWN

- **Earliest Observation Year:** `2002`  
- **Latest Observation Year:** `2019`  
- **Valid Observation Years Present:** `[2002, 2005, 2006, 2009, 2010, 2011, 2012, 2015, 2017, 2018, 2019]`  

| Observation Year | GE Polygons (255) | GE Points (185) | Cartosat Polygons (67) | Total Source-Layer Features | Dataset Observation Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2002** | 9 | 1 | 0 | 10 | Source imagery observation record. |
| **2005** | 8 | 4 | 0 | 12 | Source imagery observation record. |
| **2006** | 10 | 1 | 0 | 11 | Source imagery observation record. |
| **2009** | 5 | 1 | 0 | 6 | Source imagery observation record. |
| **2010** | 12 | 9 | 0 | 21 | Source imagery observation record. |
| **2011** | 152 | 37 | 0 | 189 | Highest source-feature count in this dataset. |
| **2012** | 15 | 3 | 0 | 18 | Source imagery observation record. |
| **2015** | 8 | 4 | 0 | 12 | Source imagery observation record. |
| **2017** | 10 | 3 | 0 | 13 | Source imagery observation record. |
| **2018** | 2 | 0 | 0 | 2 | Source imagery observation record. |
| **2019** | 1 | 0 | 0 | 1 | Source imagery observation record. |
| **NULL / Active / Unspecified** | 23 | 122 | 67 | 212 | Non-year or unspecified temporal records. |

## 2. NULL / UNPARSED TEMPORAL VALUES AUDIT

- **GE Polygons NULL Count:** `19` (Strings: `'Active'`, `'Active \| 2005'`, `'2009\nActive\nPersistent'`, `'1/9/2015'`, `'Active \| In morainic deposit'`)
- **GE Points NULL Count:** `122` (Strings: `''` [92 blank], `'Active'`, `'Definite \| Active'`, `'Image 10/5/2011'`, `'Earliest image 11/24/2007'`)
- **Cartosat NULL Count:** `67` (No temporal field present in source DBF)
- **Semantic Rule:** Non-year strings like `'Active'` are safely retained in `source_attributes` JSONB with `observation_year = NULL`. They are **never** converted into event dates.

## 3. SPATIAL TEMPORAL LAYERS CREATED

- `data/derived/temporal/zenodo_observations_2002_4326.geojson`
- `data/derived/temporal/zenodo_observations_2005_4326.geojson`
- `data/derived/temporal/zenodo_observations_2006_4326.geojson`
- `data/derived/temporal/zenodo_observations_2009_4326.geojson`
- `data/derived/temporal/zenodo_observations_2010_4326.geojson`
- `data/derived/temporal/zenodo_observations_2011_4326.geojson`
- `data/derived/temporal/zenodo_observations_2012_4326.geojson`
- `data/derived/temporal/zenodo_observations_2015_4326.geojson`
- `data/derived/temporal/zenodo_observations_2017_4326.geojson`
- `data/derived/temporal/zenodo_observations_2018_4326.geojson`
- `data/derived/temporal/zenodo_observations_2019_4326.geojson`
- `data/derived/temporal/zenodo_observations_unspecified_active_4326.geojson`

## 4. CROSS-SOURCE SPATIAL CANDIDATE OVERLAP ANALYSIS (BBOX OVERLAPS ONLY)

1. **GE Points in GE Polygon BBOXes:** `4` of `185` points (2.16%).
2. **GE Polygons in Cartosat BBOXes:** `1` of `255` polygons (0.39%).
3. **GE Points in Cartosat BBOXes:** `0` of `185` points (0.0%).
4. **Cartosat Scarp-Deposit Unions:** `23` derived spatial association features (`DERIVED_SPATIAL_ASSOCIATION`).

> **IMPORTANT NOTICE:** BBOX candidate overlap reports bounding-box relationships ONLY. It is **NOT** proof of actual geometry intersection or common landslide identity, and features are **NEVER** merged into a fake unique feature tally.
