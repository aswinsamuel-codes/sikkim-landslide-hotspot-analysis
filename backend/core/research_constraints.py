"""
Research Constraints Enforcement Engine
SIH26001 — Sikkim Historical Landslide Intelligence (Rev 2)

This module provides compile-time and runtime validation of research rules,
forbidden field mappings, observation status classification, ML semantic gates,
and anti-leakage constraints.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Minimum area fraction of a cell inside a mapped observation extent required for denominator eligibility
MIN_OBSERVED_FRACTION: float = 0.5

# Standard Sikkim District reorganization boundary date (Official notification 26/L&PAD/2021)
DISTRICT_REORG_DATE: str = "2021-12-13"

# Registered DEM source (Owner decision required; initially unassigned)
REGISTERED_DEM_SOURCE: Optional[str] = None

# Path to semantics contract
METADATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "metadata"
FIELD_SEMANTICS_FILE = METADATA_DIR / "field_semantics.json"
COVERAGE_MATRIX_FILE = METADATA_DIR / "SIKKIM_COVERAGE_MATRIX_2011_2025.csv"


def load_field_semantics() -> Dict[str, Any]:
    """Load field semantics JSON contract."""
    if not FIELD_SEMANTICS_FILE.exists():
        raise FileNotFoundError(f"Semantics contract missing at {FIELD_SEMANTICS_FILE}")
    with open(FIELD_SEMANTICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_field_mapping(source_field: str, target_field: str, source_name: str = "") -> None:
    """
    Validate that a proposed field mapping does not violate forbidden mappings (A-11).
    Raises ValueError if a forbidden mapping is attempted.
    """
    semantics = load_field_semantics()
    for rule in semantics.get("forbidden_mappings", []):
        if rule.get("source_field") == source_field and rule.get("target_field") == target_field:
            if not rule.get("source") or rule.get("source").lower() in source_name.lower():
                raise ValueError(
                    f"FORBIDDEN FIELD MAPPING [{rule['rule_id']}]: "
                    f"Cannot map '{source_field}' to '{target_field}'. "
                    f"Reason: {rule['reason']}"
                )


def classify_observation_status(observed_fraction: float) -> Tuple[str, bool]:
    """
    Classify a cell-year observation into (observation_status, denominator_eligible).

    - NOT_OBSERVED (observed_fraction == 0): denominator_eligible = False, counts = NULL
    - PARTIALLY_OBSERVED (0 < observed_fraction < 0.5): denominator_eligible = False, preserves detected events
    - OBSERVED (observed_fraction >= 0.5): denominator_eligible = True, preserves detected events
    """
    if observed_fraction <= 0.0:
        return ("NOT_OBSERVED", False)
    elif observed_fraction < MIN_OBSERVED_FRACTION:
        return ("PARTIALLY_OBSERVED", False)
    else:
        return ("OBSERVED", True)


def validate_ml_baseline_features(feature_list: List[str]) -> None:
    """
    Anti-leakage rule B-1:
    Baseline susceptibility feature list MUST contain no historical density or recurrence feature.
    """
    forbidden_substrings = ["hist_landslide_density", "hist_recurrence_index", "density", "recurrence"]
    for feat in feature_list:
        feat_lower = feat.lower()
        for forbidden in forbidden_substrings:
            if forbidden in feat_lower:
                raise ValueError(
                    f"ML ANTI-LEAKAGE VIOLATION [B-1]: Baseline feature '{feat}' contains "
                    f"forbidden term '{forbidden}'. Baseline susceptibility model MUST be decoupled "
                    f"from historical density and recurrence."
                )


def register_dem_source(dem_name: str) -> str:
    """
    Register explicit owner DEM decision.
    Phase 0 registers decision; download permitted only in Phase 8.
    """
    global REGISTERED_DEM_SOURCE
    valid_options = ["copernicus_dem_glo_30", "copernicus_dem_30m", "nasadem_30m", "aster_gdem_v3"]
    norm_name = dem_name.lower().strip()
    if norm_name not in valid_options:
        raise ValueError(f"Invalid DEM selection '{dem_name}'. Valid options: {valid_options}")
    REGISTERED_DEM_SOURCE = norm_name
    return REGISTERED_DEM_SOURCE


def get_dem_source_status() -> Optional[str]:
    """Returns currently registered DEM source or None if owner decision pending."""
    return REGISTERED_DEM_SOURCE


def evaluate_ml_semantic_gate(
    label_years: List[int],
    held_extents: Dict[int, Optional[str]],
    cell_observations_materialized: bool,
    positive_labels_in_observed_cells: bool,
    negatives_from_eligible_observed_cells: bool,
    eligible_cell_years_count: int,
    positive_count: int,
    includes_zenodo_year: bool,
    all_extents_unknown: bool,
    spatial_cv_configured: bool,
    min_cell_years: int = 100,
    min_positives: int = 10
) -> Tuple[bool, List[str]]:
    """
    Evaluates the 8-clause ML Semantic Gate (QA-23 / A-12).
    Returns (passed: bool, failing_clause_ids: List[str]).
    """
    failing_clauses: List[str] = []

    # Clause 1: observation_extents row exists with non-null extent_basis for every label year
    for yr in label_years:
        basis = held_extents.get(yr)
        if basis is None:
            failing_clauses.append(f"CLAUSE_1_MISSING_EXTENT_BASIS_YEAR_{yr}")

    # Clause 2: cell_year_observations fully materialized
    if not cell_observations_materialized:
        failing_clauses.append("CLAUSE_2_UNMATERIALIZED_OBSERVATIONS")

    # Clause 3: Every positive label in observed = True cell for its year
    if not positive_labels_in_observed_cells:
        failing_clauses.append("CLAUSE_3_POSITIVES_IN_UNOBSERVED_CELLS")

    # Clause 4: Every negative drawn from denominator_eligible = True cell
    if not negatives_from_eligible_observed_cells:
        failing_clauses.append("CLAUSE_4_NEGATIVES_FROM_INELIGIBLE_CELLS")

    # Clause 5: Minimum cell-years & positive count met
    if eligible_cell_years_count < min_cell_years or positive_count < min_positives:
        failing_clauses.append("CLAUSE_5_INSUFFICIENT_DATA_VOLUME")

    # Clause 6: No label derives from Zenodo observation_year
    if includes_zenodo_year:
        failing_clauses.append("CLAUSE_6_ZENODO_YEAR_EXCLUSION_VIOLATED")

    # Clause 7: Extent basis check (refuse if all unknown)
    if all_extents_unknown:
        failing_clauses.append("CLAUSE_7_ALL_EXTENT_BASES_UNKNOWN")

    # Clause 8: Spatial CV config present with empirical block size justification
    if not spatial_cv_configured:
        failing_clauses.append("CLAUSE_8_SPATIAL_CV_NOT_CONFIGURED")

    passed = len(failing_clauses) == 0
    return passed, failing_clauses


def parse_safe_observation_year(val: Optional[Any]) -> Optional[int]:
    """
    Safely parse observation year from raw string fields (e.g. Zenodo 'descriptio').

    Rules:
    - If the source value is a strictly valid 4-digit year (1900-2026), return observation_year (int).
    - If it is 'Active', a full date ('1/9/2015'), multi-line text ('2009\\nActive'), or empty/null, return None.
    - Never interpret 'Active' or non-year values as an observation year or event date.
    """
    if val is None:
        return None
    s_val = str(val).strip()
    if not s_val:
        return None
    
    # Strictly check if s_val is a 4-digit year string
    if s_val.isdigit() and len(s_val) == 4:
        yr = int(s_val)
        if 1900 <= yr <= 2026:
            return yr
    
    return None

