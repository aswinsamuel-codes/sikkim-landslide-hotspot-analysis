const API_BASE = '/api/local';

export async function fetchHealth() {
  const res = await fetch('/health');
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchInventoryFeatures() {
  const res = await fetch(`${API_BASE}/inventory/features`);
  if (!res.ok) throw new Error('Failed to fetch inventory features');
  return res.json();
}

export async function fetchTemporalYears() {
  const res = await fetch(`${API_BASE}/inventory/temporal`);
  if (!res.ok) throw new Error('Failed to fetch temporal timeline');
  return res.json();
}

export async function fetchTemporalLayer(year) {
  const res = await fetch(`${API_BASE}/inventory/temporal/${year}`);
  if (res.status === 404) {
    const errorData = await res.json();
    throw new Error(errorData.detail || `DATA_NOT_HELD: No data for year ${year}`);
  }
  if (!res.ok) throw new Error(`Failed to fetch temporal layer for year ${year}`);
  return res.json();
}

export async function fetchDensityGrid() {
  const res = await fetch(`${API_BASE}/inventory/density`);
  if (!res.ok) throw new Error('Failed to fetch density grid');
  return res.json();
}

export async function fetchDensitySummary() {
  const res = await fetch(`${API_BASE}/inventory/density/summary`);
  if (!res.ok) throw new Error('Failed to fetch density summary');
  return res.json();
}

export async function fetchCoverageSummary() {
  const res = await fetch(`${API_BASE}/inventory/coverage/summary`);
  if (!res.ok) throw new Error('Failed to fetch coverage summary');
  return res.json();
}

export async function fetchLayerProvenance() {
  const res = await fetch(`${API_BASE}/inventory/provenance`);
  if (!res.ok) throw new Error('Failed to fetch layer provenance');
  return res.json();
}
