import os
import time
import subprocess

TARGET_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\raw\zenodo_8169506"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

FILES = [
    "Cartosat_197823411_extents.cpg",
    "Cartosat_197823411_extents.dbf",
    "Cartosat_197823411_extents.prj",
    "Cartosat_197823411_extents.shp",
    "Cartosat_197823411_extents.shx",
    "Cartosat_197823411clouds.cpg",
    "Cartosat_197823411clouds.dbf",
    "Cartosat_197823411clouds.prj",
    "Cartosat_197823411clouds.shp",
    "Cartosat_197823411clouds.shx",
    "Cartosat_landslides_21Dec2021.cpg",
    "Cartosat_landslides_21Dec2021.dbf",
    "Cartosat_landslides_21Dec2021.prj",
    "Cartosat_landslides_21Dec2021.shp",
    "Cartosat_landslides_21Dec2021.shx",
    "Google_Earth_landslides_point_21Dec2021.cpg",
    "Google_Earth_landslides_point_21Dec2021.csv",
    "Google_Earth_landslides_point_21Dec2021.dbf",
    "Google_Earth_landslides_point_21Dec2021.prj",
    "Google_Earth_landslides_point_21Dec2021.shp",
    "Google_Earth_landslides_point_21Dec2021.shx",
    "Google_Earth_landslides_polygon_21Dec2021.cpg",
    "Google_Earth_landslides_polygon_21Dec2021.csv",
    "Google_Earth_landslides_polygon_21Dec2021.dbf",
    "Google_Earth_landslides_polygon_21Dec2021.prj",
    "Google_Earth_landslides_polygon_21Dec2021.shp",
    "Google_Earth_landslides_polygon_21Dec2021.shx",
    "Google_Earth_mapped_extent_21Dec2021.cpg",
    "Google_Earth_mapped_extent_21Dec2021.dbf",
    "Google_Earth_mapped_extent_21Dec2021.prj",
    "Google_Earth_mapped_extent_21Dec2021.qmd",
    "Google_Earth_mapped_extent_21Dec2021.shp",
    "Google_Earth_mapped_extent_21Dec2021.shx"
]

os.makedirs(TARGET_DIR, exist_ok=True)

manifest = {}
for fname in FILES:
    dest_path = os.path.join(TARGET_DIR, fname)
    url = f"https://zenodo.org/records/8169506/files/{fname}?download=1"
    print(f"Downloading {fname}...")
    cmd = [
        "curl.exe", "-s", "-L",
        "-A", USER_AGENT,
        url,
        "-o", dest_path
    ]
    subprocess.run(cmd, check=True)
    size = os.path.getsize(dest_path)
    print(f"  Saved {fname}: {size:,} bytes")
    manifest[fname] = {
        "size": size,
        "url": url,
        "is_valid": size != 763
    }
    time.sleep(1.5)

manifest_path = os.path.join(TARGET_DIR, "manifest.json")
with open(manifest_path, "w") as mf:
    import json
    json.dump(manifest, mf, indent=2)

print("Finished rate-limited download pass.")
