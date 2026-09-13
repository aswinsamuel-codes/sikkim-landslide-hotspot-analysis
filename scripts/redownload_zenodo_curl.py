import os
import json
import subprocess

TARGET_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\raw\zenodo_8169506"
RECORD_ID = "8169506"
API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Fetch record metadata via curl
meta_file = os.path.join(TARGET_DIR, "zenodo_meta.json")
os.makedirs(TARGET_DIR, exist_ok=True)

cmd_meta = [
    "curl.exe", "-s", "-L",
    "-A", USER_AGENT,
    API_URL,
    "-o", meta_file
]
subprocess.run(cmd_meta, check=True)

with open(meta_file, "r", encoding="utf-8") as f:
    record = json.load(f)

files = record.get('files', [])
print(f"Title: {record.get('metadata', {}).get('title')}")
print(f"Total files in record: {len(files)}")

manifest = {}
for f in files:
    filename = f['key']
    download_url = f['links']['self']
    size = f['size']
    checksum = f['checksum']
    dest_path = os.path.join(TARGET_DIR, filename)
    
    print(f"Downloading {filename} ({size:,} bytes)...")
    cmd = [
        "curl.exe", "-s", "-L",
        "-A", USER_AGENT,
        download_url,
        "-o", dest_path
    ]
    subprocess.run(cmd, check=True)
    
    actual_size = os.path.getsize(dest_path)
    status = "OK" if actual_size == size else f"MISMATCH ({actual_size:,} vs {size:,})"
    print(f" -> {filename}: {status}")
    manifest[filename] = {
        "expected_size": size,
        "actual_size": actual_size,
        "checksum": checksum,
        "download_url": download_url,
        "status": status
    }

manifest_path = os.path.join(TARGET_DIR, "manifest.json")
with open(manifest_path, "w") as mf:
    json.dump(manifest, mf, indent=2)

print(f"\nSuccessfully processed {len(manifest)} files in {TARGET_DIR}")
