"""
Configuration Settings
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)
"""

import os
from pathlib import Path
from typing import List

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
METADATA_DIR = DATA_DIR / "metadata"
SOURCES_DIR = DATA_DIR / "sources"
VALIDATION_DIR = DATA_DIR / "validation"
EXPORTS_DIR = BASE_DIR / "exports"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, METADATA_DIR, SOURCES_DIR, VALIDATION_DIR, EXPORTS_DIR, MODELS_DIR, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Application Information
PROJECT_NAME = "SIH26001 — Sikkim Historical Landslide Intelligence"
VERSION = "1.0.0-phase1"
DESCRIPTION = "Local-First Sikkim Landslide Intelligence & Hotspot Mapping System"

# Database Configuration (PostgreSQL + PostGIS)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sikkim_landslides")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Registered Owner Decisions (Phase 1)
REGISTERED_DATABASE_ENGINE = "postgresql_postgis"
REGISTERED_DEM_SOURCE = "copernicus_dem_glo_30"
REGISTERED_RAINFALL_PRIMARY = "era5_land"
REGISTERED_RAINFALL_CROSSCHECK = "chirps_v3"
REGISTERED_RAINFALL_OPERATIONAL = "gpm_imerg"
REGISTERED_RAINFALL_VALIDATION = "imd_0.25deg"

# SSRF Blocklist for URL Fetcher / Web Importer
SSRF_BLOCKED_HOSTS: List[str] = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "169.254.169.254", # AWS metadata service
    "metadata.google.internal", # GCP metadata service
]

SSRF_BLOCKED_SCHEMES: List[str] = [
    "file",
    "gopher",
    "dict",
    "ftp",
    "tftp",
    "ldap"
]
