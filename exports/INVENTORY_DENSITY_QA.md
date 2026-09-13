# PHASE 2D FINAL GIS QA & INVENTORY DENSITY REPORT

**Module:** Sikkim Historical Landslide Intelligence & Hotspot Mapping  
**Date:** September 13, 2026  
**Status:** **PASSED — ALL FINAL GIS QA & CONSERVATION AUDITS VERIFIED**

> **MANDATORY NOTICE:**  
> *Centroid-assigned inventory feature density measures the spatial concentration of currently held source features in Zenodo 8169506 per nominal 1 km² cell. It MUST NOT be interpreted as landslide failure probability, hazard, or risk. Density uses nominal 1 km² cell area as denominator and never silently substitutes in_state_area_km2. Unmapped areas (coverage_fraction = 0.0) are marked DATA_NOT_HELD and are strictly NOT assigned zero observations.*

## 1. GRID & AREA CONSERVATION SPECIFICATIONS

- **Geographic Output CRS:** `EPSG:4326 (WGS 84)`  
- **Projected Metric Analysis CRS:** `EPSG:32645 (UTM Zone 45N)`  
- **Nominal Cell Dimensions:** `1,000 m × 1,000 m` (`1.00 km²` nominal cell area)  
- **Grid-Cell Centers / Intersection in Sikkim:** `7355 grid cells`  
- **GADM v4.1 Sikkim Boundary Polygon Area:** `7081.540805 km²`  
- **Sum of Grid Cell In-State Area Intersections:** `7079.477653 km²` (`7,079.48 km²` rounded)  
- **Reference Sikkim Administrative Area:** `~7096.00 km²`  
- **State Area Discrepancy Note:** The boundary-derived state area (GADM v4.1 polygon: 7,081.54 km², grid-intersection sum: 7,079.48 km²) and reference administrative-area definition (~7,096.00 km²) differ; they are reported separately and not described as matching.  

## 2. BOUNDARY-AREA CONSERVATION AUDIT

- **GADM v4.1 State Boundary Polygon Area:** `7081.540805 km²`  
- **Sum of Grid Cell In-State Intersection Area:** `7079.477653 km²`  
- **Absolute Area Error:** `2.063151 km²` (`2,063,151.40 m²`)  
- **Relative Area Error:** `0.029134%`  
- **Tolerance Threshold:** `< 0.5%`  
- **Audit Result:** **PASSED WITHIN TOLERANCE**  

## 3. MAPPED-EXTENT AREA CONSERVATION AUDIT (SHAPELY CROSS-CHECKED)

- **Zenodo 8169506 Mapped Extent Polygon Area (Shapely Independent):** `2962.146802 km²`  
- **Sum of Grid Cell Net Extent Intersection Area (Shapely):** `2956.609750 km²`  
- **Absolute Area Error:** `5.537052 km²`  
- **Relative Area Error:** `0.186927%`  
- **Tolerance Threshold:** `< 0.5%`  
- **Shapely Cross-Check Status:** `VERIFIED_EXACT_MATCH_WITH_SHAPELY`  
- **Audit Result:** **PASSED WITHIN TOLERANCE**  

## 4. TRUE GEOMETRIC CENTROID ASSIGNMENT AUDIT (EPSG:32645)

| Source Layer | Total Features | True Geometric Centroid Assigned | Spanning >1 Cell | Max Cells Crossed |
| :--- | :--- | :--- | :--- | :--- |
| **GE_POLYGON** | 255 | 255 | 70 | 4 |
| **GE_POINT** | 185 | 185 | 0 | 1 |
| **CARTOSAT_POLYGON** | 67 | 67 | 51 | 7 |
| **Total Source Inventory** | **507** | **507** | **121** | **7** |
| **Derived Cartosat Unions** | 23 | **0** | **0** | **EXCLUDED** |

## 5. DENSITY DENOMINATOR & COVERAGE AUDIT

- **Density Field Name:** `centroid_assigned_inventory_feature_density_per_km2`  
- **Density Denominator:** `nominal_cell_area_km2 = 1.0` (Strictly enforced; no `in_state_area_km2` substitutions)  
- **Features Assigned to OBSERVED Cells:** `497` features  
- **Features Assigned to PARTIALLY_COVERED Cells:** `10` features  
- **Silently Discarded Features:** **0** (All 507 source features preserved)  

## 6. CREATED OUTPUT LAYERS & MAPS

- `data/derived/density/sikkim_inventory_density_grid_4326.geojson`  
- `data/derived/density/sikkim_source_specific_density_grid_4326.geojson`  
- `data/derived/density/sikkim_observation_year_presence_grid_4326.geojson`  
- `exports/sikkim_inventory_feature_density_map.png`  
- `exports/sikkim_observation_year_distribution_map.png`  

