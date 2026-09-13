# Phase 1 — Sikkim Landslide Data Research Report

**Module:** Multi-Temporal Sikkim Landslide Historical Hotspot & Recurrence Intelligence
**Problem statement:** SIH26001
**Scope of this phase:** Sections 32.1–32.10 of the specification (research, catalogue, coverage, gaps). No UI, no ingestion code executed yet.

---

## 1. Headline finding

**Sikkim has four usable observation years between 2011 and 2025, not fifteen.**

Systematic, geometry-bearing landslide inventories covering Sikkim exist for **2011, 2014, 2017 and 2023**. Everything else is either partial (one research inventory over ~3,000 km² of southern Sikkim), report-level without geometry, or absent.

This is not a gap to be papered over. It is the single most important design constraint in the module, and the specification already anticipated it in Section 16: the recurrence denominator must reflect data availability. What the research shows is that the denominator is *four*, not fifteen, and that even those four years cover different areas under different triggers.

| Year | Status | Source |
|---|---|---|
| 2011 | AVAILABLE (partial extent) | NRSC event-based, 18 Sep 2011 earthquake — 1,196 landslides |
| 2012, 2013 | PARTIAL COVERAGE | Southern Sikkim research inventory only |
| 2014 | AVAILABLE (statewide) | NRSC seasonal monsoon inventory |
| 2015 | PARTIAL COVERAGE | Southern Sikkim research inventory only |
| 2016 | PARTIAL COVERAGE | NRSC report — PDF only, no geometry |
| 2017 | AVAILABLE (statewide) | NRSC seasonal monsoon inventory |
| 2018, 2019 | PARTIAL COVERAGE | Southern Sikkim research inventory only |
| 2020, 2021, 2022 | **DATA NOT AVAILABLE** | — |
| 2023 | AVAILABLE (statewide) | NRSC seasonal inventory + Oct 2023 GLOF cascade |
| 2024, 2025 | **DATA NOT AVAILABLE** | Site-specific GSI reports only |

Machine-readable version: `data/metadata/SIKKIM_YEAR_COVERAGE.csv`.

---

## 2. What this does to the recurrence engine

The naive formula in Section 16 — `active_years / years_with_usable_observations` — needs one correction before it is defensible.

The four available years do not observe the same ground. The 2011 earthquake inventory covers roughly 4,105 km² of a 7,096 km² state. The southern Sikkim research inventory covers ~3,000 km² and ships an explicit mapped-extent polygon and a cloud-mask polygon. Cloud cover truncates every optical inventory differently each year.

So the denominator has to be **per cell, not per state**:

```
recurrence_index(cell) = active_years(cell) / |{ y : cell ∈ observed_extent(y) }|
```

Concretely:

- Store a `mapped_extent` geometry and, where published, a `cloud_mask` geometry for **every** year-source pair. The southern Sikkim dataset gives you both for free; for the NRSC layers the extent has to be reconstructed from the published analysis footprint.
- A cell that was never inside any 2011 image footprint has a 2011 denominator contribution of zero — it is not a "no landslide in 2011" observation.
- Report `n_observed_years` alongside every recurrence value in the API and on the map. A cell with 2/2 and a cell with 2/4 are not the same finding, and the dashboard must not render them identically.
- With a maximum denominator of 4, publish recurrence as an **ordinal evidence class** (Observed once / Observed repeatedly / Insufficient observation) rather than a continuous 0–1 score. A "0.75 recurrence index" from three observations invites exactly the false precision Section 15 warns against.

The mixed trigger regime compounds this. 2011 is earthquake-triggered; 2014 and 2017 are monsoon; 2023 is monsoon plus a GLOF cascade down the Teesta. A cell active in 2011 and 2023 is not demonstrating rainfall recurrence — it is demonstrating susceptibility to two different processes. Store `trigger` per event (the schema already has the field) and let the dashboard filter recurrence by trigger regime.

---

## 3. Access reality — what the importer can and cannot fetch

The specification is firm that the importer must not bypass authentication, and that cuts off a lot:

**Open, no login, importer-ready:**
- Zenodo record 8169506 — CC-BY-4.0, direct file URLs, REST API, ships CSV alongside shapefiles
- Zenodo record 19421112 — CC-BY-4.0, single 282 MB `.rar`
- NRSC Bhuvan PDF reports, including `Sikkim_Landslide_2016.pdf` — direct HTTPS
- GSI Bhusanket incidence report PDFs under `/Output/LS_Incidence_Report/{year}/`
- NASA COOLR / GLC — open download plus REST API
- IMD gridded rainfall — public HTTP POST, one NetCDF per year
- OpenStreetMap (Geofabrik), WorldPop, ESA WorldCover — open direct download

**Viewable but not bulk-downloadable:**
- Bhuvan landslide inventory layers. They render through Bhuvan's WMS (`bhuvan-vec2.nrsc.gov.in/bhuvan/wms`) with an Identify Features tool, which implies feature-level attributes are queryable, but there is no public shapefile export. Treat WMS `GetFeatureInfo` as the technical route and verify the terms of use before automating it. For the hackathon, the honest path is a written data request to NRSC.

**Login-gated — out of scope for the importer by policy:**
- GSI Bhukosh / NGDR (registration required for download)
- NDEM (`ndem.nrsc.gov.in`) is an authorised-government-user platform

Recommended handling for the gated sources: the administrator downloads manually, drops the file in `/data/raw/<source>/`, and registers it through the same preview → mapping → approve flow as a URL import. The provenance record stores `download_method = manual_admin` rather than a fetch URL. This keeps one ingestion path and one provenance model, and it keeps the system inside the rules in Sections 6 and 27.

---

## 4. Dataset-specific traps found during inspection

**Southern Sikkim inventory (Zenodo 8169506)** — the highest-value open dataset, and the one most likely to be misused.

- The `Year` attribute is *the year of the first satellite image in which the landslide appears*, not the failure date. Loading it as `date_start` would silently fabricate a 15-year event timeline out of an image-availability artefact. Map it to a separate `observation_year` field and leave `date_start` null.
- The description says WGS 84 while the `.prj` files declare EPSG:3857. These are not the same thing. Verify against the actual `.prj` bytes on load and record the detected CRS in the provenance row; do not trust either the prose or a default assumption.
- Debris flows and rockfalls are **points** (source area); translational slides are **polygons** (source + deposit). `area_m2` is therefore present for one class and absent for another, by design. Do not impute.
- The Cartosat sub-inventory has 67 polygons describing 44 landslide features, because scarp and deposit are mapped separately. A naive row count over-counts by 52%. This is precisely what `duplicate_group_id` is for.
- The authors state the inventory was built to characterise landslide *domains* and gives a general picture rather than a complete one. It is not a complete inventory and must not be used as one.

**The 2011 earthquake, two ways.** NRSC mapped 1,196 landslides; Ghosh et al. (2012) mapped ~421 for the same event. Both are credible; they used different imagery, extents and minimum mapping units. Keep both, group them, and use the pair as the acceptance test for the duplicate-detection engine — if it collapses them to a single harmonised set with sensible group sizes, it works.

**The undocumented Zenodo archive (19421112).** Published April 2026 by IIT (ISM) Dhanbad with a completely empty description — no abstract, no coverage, no schema, no file listing. 282 MB in a single `.rar`. Unpack it in a sandbox, run the Section 27 archive checks (path traversal, compression ratio, member count), inventory what is actually inside, then re-catalogue the contents as distinct datasets. Do not catalogue it as one dataset — you do not yet know what it is.

**District names are a moving target.** On 21 December 2021 Sikkim went from four districts to six: East → Gangtok, with Pakyong carved out; West → Gyalshing, with Soreng carved out; North → Mangan; South → Namchi. Pre-2022 records say "East Sikkim". Post-2022 records say "Gangtok" or "Pakyong" and mean different areas. **Never assign district by string matching.** Assign it by spatial join against the boundary that was valid on the event date, keep the source's original district string in `notes`, and store both a `district_current` and a `district_as_reported`.

**IMD rainfall is too coarse to be a discriminating feature on its own.** At 0.25° the entire state occupies roughly ten grid cells, so a 1 km risk grid built on IMD rainfall will have near-identical rainfall values across hundreds of cells. Use IMERG at 0.1° as the primary, IMD as the gauge-anchored cross-check, and push for Sikkim's own AWS network for anything operational.

**Land cover and roads are single-epoch.** ESA WorldCover has 2020 and 2021 only; OSM gives you today's road network. Using either as a feature for a 2011 landslide is temporal leakage. Either accept it and document it prominently in the model card, or restrict those features to the years where they are contemporaneous.

---

## 5. Consequences for the ML pipeline (Section 22–24)

Section 22 correctly forbids training on latitude/longitude and historical counts alone. The research adds three further constraints:

1. **There is no usable negative class from absence.** A cell with no mapped landslide in 2014 might have had none, or might have been under cloud, or outside the analysed footprint. Negatives must be sampled only from cells inside a verified mapped extent for that year.

2. **Four observation years is a small-n problem.** Susceptibility modelling (where does terrain permit failure) is defensible with this data. Temporal hazard forecasting (will it fail this week) is not, from this data alone. Build the susceptibility model now; label the output honestly as susceptibility; let the dynamic rainfall layer come from the future forecasting engine, as the Section 31 architecture already envisages.

3. **Spatial cross-validation is mandatory, and the split must respect inventory extents.** Random splitting across a 1 km grid leaks neighbouring cells into both folds. Use spatially blocked folds (blocks of 5–10 km), and hold out one inventory source entirely as an external test set — for example, train without the southern Sikkim research inventory and test on it.

The output layer must carry three clearly separated things, per Section 24: `historical_hotspot` (observed), `modelled_susceptibility` (derived), and later `current_forecast` (dynamic). The dashboard should make it impossible to confuse them — different colour ramps, different legends, explicit labels.

---

## 6. Naming discipline

Per Section 15, the derived index is labelled **"Project-derived Historical Hotspot Index"** everywhere it appears — API field names, map legends, exports, and report headers. It is not a GSI or NRSC index, and GSI's NLSM susceptibility zonation (which *is* official) must be rendered as a separate layer with its own attribution so the two are never mistaken for each other.

---

## 7. Recommended next steps

1. Fetch the three fully-open datasets first (Zenodo 8169506, NASA COOLR Sikkim subset, GSI Bhusanket PDFs) and stand up the ingestion path end to end on real data.
2. Stand up PostGIS with `db/schema.sql` and load the six current district boundaries plus a historical four-district boundary set valid before 21 Dec 2021.
3. Build mapped-extent handling before building the hotspot engine. The extent polygons are the thing that makes the recurrence numbers honest, and retrofitting them later means recomputing everything.
4. Open a formal data request to NRSC for the Sikkim 2011/2014/2017/2023 inventory vectors, and to GSI for the Sikkim landslide inventory. Four datasets unlock the entire 2011–2023 spine of this module, and an email is far cheaper than a scraper.
5. Only then build the importer UI, the map and the ML pipeline.

---

## 8. Files produced in this phase

| File | Purpose |
|---|---|
| `SIKKIM_LANDSLIDE_DATA_COVERAGE_MATRIX.csv` | 22-row catalogue, exact columns per Section 32 |
| `data/metadata/SIKKIM_YEAR_COVERAGE.csv` | Year-by-year availability driving the recurrence denominator |
| `db/schema.sql` | PostgreSQL/PostGIS schema (Section 33.1) |
| `docs/PHASE1_DATA_RESEARCH_REPORT.md` | This report |

**Accuracy note:** record counts marked "NOT PUBLISHED" are exactly that — NRSC publishes the Sikkim seasonal layers without a state-level count in the public material reviewed. They are left blank rather than estimated. Per Section 2, no year, count or extent in these files has been invented.
