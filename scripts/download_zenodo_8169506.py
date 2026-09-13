"""
Zenodo 8169506 Acquisition & SHA-256 Verifier Script
SIH26001 — Sikkim Historical Landslide Intelligence (Phase 2A)

Downloads public open-access CC-BY-4.0 files from Zenodo record 8169506
to data/raw/zenodo_8169506/ and computes SHA-256 checksums.
"""

import os
import json
import hashlib
import urllib.request
from pathlib import Path
from typing import Dict, List, Any

RAW_ZENODO_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "zenodo_8169506"
RAW_ZENODO_DIR.mkdir(parents=True, exist_ok=True)

ZENODO_RECORD_API = "https://zenodo.org/api/records/8169506"


def compute_sha256(filepath: Path) -> str:
    """Computes SHA-256 hash of a file on disk."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_zenodo_files() -> List[Dict[str, Any]]:
    """Fetches record metadata and downloads files to RAW_ZENODO_DIR."""
    import subprocess
    print(f"Fetching record metadata from {ZENODO_RECORD_API}...")
    cmd = ["curl.exe", "-s", "-L", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", ZENODO_RECORD_API]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout:
        raise RuntimeError(f"Failed to fetch Zenodo metadata: {res.stderr}")

    record_data = json.loads(res.stdout)
    title = record_data.get("metadata", {}).get("title")
    license_type = record_data.get("metadata", {}).get("license")
    files_info = record_data.get("files", [])

    print(f"Title: {title}")
    print(f"License: {license_type}")
    print(f"Total files in Zenodo record: {len(files_info)}")

    manifest = []

    for f_item in files_info:
        file_key = f_item.get("key")
        download_url = f_item.get("links", {}).get("self")
        expected_size = f_item.get("size")
        target_path = RAW_ZENODO_DIR / file_key

        if not target_path.exists() or target_path.stat().st_size != expected_size:
            print(f"Downloading {file_key} ({expected_size} bytes)...")
            dl_cmd = ["curl.exe", "-s", "-L", "-A", "Mozilla/5.0", "-o", str(target_path), download_url]
            dl_res = subprocess.run(dl_cmd, capture_output=True)
            if dl_res.returncode != 0:
                print(f"Warning: Download failed for {file_key}")
        else:
            print(f"Already present: {file_key} ({expected_size} bytes)")

        sha256_hash = compute_sha256(target_path) if target_path.exists() else ""
        manifest.append({
            "filename": file_key,
            "path": str(target_path),
            "size_bytes": target_path.stat().st_size if target_path.exists() else 0,
            "sha256": sha256_hash,
            "download_url": download_url
        })

    # Save manifest
    manifest_path = RAW_ZENODO_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as mf:
        json.dump({
            "source_id": "ZENODO_8169506",
            "title": title,
            "license": license_type,
            "files": manifest
        }, mf, indent=2)

    print(f"Saved manifest to {manifest_path}")
    return manifest


if __name__ == "__main__":
    download_zenodo_files()
