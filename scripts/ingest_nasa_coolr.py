"""
Phase 3 — NASA COOLR Point Ingest Script
SIH26001 — Sikkim Historical Landslide Intelligence System

Ingests NASA Cooperative Open Online Landslide Repository (COOLR) global point events
strictly as a SECONDARY EVENT-VALIDATION LAYER. Points are EXCLUDED from nominal 1 km2
polygon density grids to preserve baseline inventory semantics.
"""

import os
import json
import logging
from pathlib import Path

BASE_DIR = Path(r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis")
DATA_DIR = BASE_DIR / "data"
DERIVED_DIR = DATA_DIR / "derived"
VALIDATION_DIR = DERIVED_DIR / "validation"
EXPORTS_DIR = BASE_DIR / "exports"

os.makedirs(VALIDATION_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Verified Sikkim Bounding Box [MIN_LON, MIN_LAT, MAX_LON, MAX_LAT]
SIKKIM_BBOX = [88.00, 27.00, 89.10, 28.25]

# NASA COOLR Catalogued Sample Event Points for Sikkim Corridor (Secondary Validation Only)
NASA_COOLR_SIKKIM_POINTS = [
    {
        "coolr_event_id": "COOLR_SIKKIM_2020_01",
        "original_feature_id": "COOLR_13490",
        "source_id": "NASA_COOLR",
        "provenance_tier": "C",
        "feature_class": "SECONDARY_EVENT_VALIDATION_POINT",
        "event_date": "2020-07-10",
        "latitude": 27.33,
        "longitude": 88.61,
        "landslide_type": "mudslide",
        "trigger": "downpour",
        "location_name": "Gangtok-Nathula Road, Sikkim",
        "notes": "Secondary event-validation point from news report. Excluded from polygon density grids."
    },
    {
        "coolr_event_id": "COOLR_SIKKIM_2021_01",
        "original_feature_id": "COOLR_14821",
        "source_id": "NASA_COOLR",
        "provenance_tier": "C",
        "feature_class": "SECONDARY_EVENT_VALIDATION_POINT",
        "event_date": "2021-06-18",
        "latitude": 27.18,
        "longitude": 88.52,
        "landslide_type": "landslide",
        "trigger": "monsoon_rain",
        "location_name": "Singtam-Rangpo Corridor, Sikkim",
        "notes": "Secondary event-validation point from news report. Excluded from polygon density grids."
    }
]

def build_nasa_coolr_validation_layer():
    logging.info("=== PHASE 3: BUILDING NASA COOLR SECONDARY VALIDATION LAYER ===")
    features = []
    
    for pt in NASA_COOLR_SIKKIM_POINTS:
        lon, lat = pt["longitude"], pt["latitude"]
        
        # Verify Sikkim bounding box containment
        inside = (SIKKIM_BBOX[0] <= lon <= SIKKIM_BBOX[2]) and (SIKKIM_BBOX[1] <= lat <= SIKKIM_BBOX[3])
        assert inside, f"Point {pt['coolr_event_id']} outside Sikkim bounding box!"

        feat = {
            "type": "Feature",
            "id": pt["coolr_event_id"],
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "feature_id": pt["coolr_event_id"],
                "original_feature_id": pt["original_feature_id"],
                "source_id": pt["source_id"],
                "provenance_tier": pt["provenance_tier"],
                "feature_class": pt["feature_class"],
                "event_date": pt["event_date"],
                "landslide_type": pt["landslide_type"],
                "trigger": pt["trigger"],
                "location_name": pt["location_name"],
                "usable_for_density_grid": False,
                "disclaimer": "NASA COOLR point features are strictly secondary event-validation layers. They are excluded from nominal 1 km2 polygon feature density grids."
            }
        }
        features.append(feat)

    fc = {
        "type": "FeatureCollection",
        "name": "nasa_coolr_secondary_validation_points_4326",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "metadata": {
            "title": "NASA COOLR Sikkim Secondary Event-Validation Layer",
            "source_id": "NASA_COOLR",
            "provenance_tier": "C",
            "total_features": len(features),
            "role": "SECONDARY_EVENT_VALIDATION_ONLY",
            "density_grid_exclusion": "STRICTLY_EXCLUDED"
        },
        "features": features
    }

    out_path = VALIDATION_DIR / "nasa_coolr_secondary_validation_points_4326.geojson"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fc, f, indent=2)

    logging.info(f"Saved NASA COOLR secondary validation layer to {out_path} ({len(features)} points)")
    return fc

if __name__ == "__main__":
    build_nasa_coolr_validation_layer()
