# DATA REQUEST & INSTITUTIONAL REQUISITION

**To:**  
Group Head / Director  
National Remote Sensing Centre (NRSC) / ISRO  
Balanagar, Hyderabad, Telangana — 500037  

**From:**  
Disaster Risk Intelligence & Early Warning Research Group  
Module SIH26001: AI-Based Early Warning & Landslide Risk Monitoring System for North-Eastern Region of India  

**Date:** 2026-09-13  
**Subject:** Formal Request for GIS Vector Geometries of Historical Sikkim Landslide Inventories (2011, 2014, 2017, 2023)  

---

### 1. Executive Summary & Purpose

Our project is developing a local-first, multi-temporal landslide intelligence, recurrence, and hotspot monitoring framework for the State of Sikkim under Problem Statement **SIH26001**.

To calculate honest temporal recurrence and spatial hotspot indices without circular spatial assumptions, our architecture requires official GIS vector geometries (polygons or points) and corresponding satellite observation extent footprints for the following historical NRSC/ISRO inventory mapping campaigns:

1. **2011 Post-Earthquake Inventory:** Vector point/polygon geometries mapped following the 18 September 2011 Mw 6.9 Sikkim earthquake (~1,196 mapped landslides as documented in *Martha, Govindharaj & Vinod Kumar, 2014*).
2. **2014 Seasonal Monsoon Inventory:** Vector polygon geometries for the 2014 monsoon landslide inventory over Sikkim.
3. **2017 Seasonal Monsoon Inventory:** Vector polygon geometries for the 2017 monsoon landslide inventory over Sikkim.
4. **2023 Seasonal & Extreme Cascade Inventory:** Vector polygon geometries for the 2023 landslide inventory over Sikkim (including extreme rainfall and South Lhonak GLOF cascade events).

---

### 2. Critical Architectural Requirement

Our recurrence engine enforces strict observation coverage rules: a terrain cell is only evaluated for recurrence when a verified, non-event-derived observation footprint is available locally. Currently, because vector geometries and published footprints are not available in public bulk export repositories, our system operates in a verified **correct-and-empty** state (`usable_for_denominator = FALSE`, returning `NOT_OBSERVED` across recurrence calculations).

Obtaining these official NRSC vector layers is on our project's critical path.

---

### 3. Requested Deliverables & Specifications

- **Format:** ESRI Shapefile, GeoJSON, or GeoPackage (EPSG:4326 or UTM Zone 45N EPSG:32645).
- **Attributes Requested:** Event Date / Acquisition Date, Landslide Area ($m^2$), Landslide Type (Scarp/Deposit/Polygon), Trigger Classification.
- **Coverage Extents:** Sensor footprints, image acquisition boundaries, and cloud/shadow mask geometries associated with each inventory campaign.

---

### 4. Institutional Undertaking & Data Protection

- Data will be used strictly for research, early warning model validation, and disaster risk reduction for the Sikkim region.
- All attribution to NRSC/ISRO will be prominently preserved in all software interfaces, maps, and reports.
- Data will be stored securely on local-first infrastructure in compliance with National Geospatial Policy guidelines.

**Requested By:**  
*Lead Geospatial & Software Architect, SIH26001 Research Team*  
*Contact Email / Phone:* [Institutional Credentials Attached]
