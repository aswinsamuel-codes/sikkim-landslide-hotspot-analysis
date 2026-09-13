import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

DERIVED_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\derived"
EXPORTS_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\exports"
os.makedirs(EXPORTS_DIR, exist_ok=True)

out_map_path = os.path.join(EXPORTS_DIR, "sikkim_landslide_inventory_map.png")

# Load derived GeoJSON files
def load_geojson(fname):
    path = os.path.join(DERIVED_DIR, fname)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

boundary_fc = load_geojson("sikkim_state_boundary_4326.geojson")
ge_poly_fc = load_geojson("zenodo_ge_polygons_4326.geojson")
ge_pt_fc = load_geojson("zenodo_ge_points_4326.geojson")
cart_poly_fc = load_geojson("zenodo_cartosat_polygons_4326.geojson")
cart_union_fc = load_geojson("zenodo_cartosat_scarp_deposit_unions_4326.geojson")
extent_fc = load_geojson("zenodo_mapped_extent_4326.geojson")

# Image dimensions and map extent
WIDTH, HEIGHT = 2000, 2200
MARGIN_LEFT, MARGIN_RIGHT = 120, 80
MARGIN_TOP, MARGIN_BOTTOM = 220, 240

MAP_W = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
MAP_H = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

# Coordinates bounds
MIN_LON, MAX_LON = 87.95, 89.05
MIN_LAT, MAX_LAT = 27.00, 28.20

def geo_to_pixel(lon, lat):
    px = MARGIN_LEFT + int((lon - MIN_LON) / (MAX_LON - MIN_LON) * MAP_W)
    py = MARGIN_TOP + int((MAX_LAT - lat) / (MAX_LAT - MIN_LAT) * MAP_H)
    return px, py

# Create canvas
img = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 255)) # Dark slate background (#0f172a)
draw = ImageDraw.Draw(img)

# Try loading font or default
try:
    title_font = ImageFont.truetype("arial.ttf", 36)
    subtitle_font = ImageFont.truetype("arial.ttf", 22)
    label_font = ImageFont.truetype("arial.ttf", 18)
    small_font = ImageFont.truetype("arial.ttf", 15)
except:
    title_font = subtitle_font = label_font = small_font = ImageFont.load_default()

# 1. Draw Lat/Lon Gridlines
for lon_deg in [88.0, 88.2, 88.4, 88.6, 88.8, 89.0]:
    x1, y1 = geo_to_pixel(lon_deg, MIN_LAT)
    x2, y2 = geo_to_pixel(lon_deg, MAX_LAT)
    draw.line([(x1, y1), (x2, y2)], fill=(51, 65, 85, 180), width=1) # Slate 700
    draw.text((x1 - 20, HEIGHT - MARGIN_BOTTOM + 15), f"{lon_deg:.1f}°E", fill=(148, 163, 184, 255), font=small_font)

for lat_deg in [27.0, 27.2, 27.4, 27.6, 27.8, 28.0, 28.2]:
    x1, y1 = geo_to_pixel(MIN_LON, lat_deg)
    x2, y2 = geo_to_pixel(MAX_LON, lat_deg)
    draw.line([(x1, y1), (x2, y2)], fill=(51, 65, 85, 180), width=1)
    draw.text((MARGIN_LEFT - 75, y1 - 8), f"{lat_deg:.1f}°N", fill=(148, 163, 184, 255), font=small_font)

# Map bounding box border
draw.rectangle([(MARGIN_LEFT, MARGIN_TOP), (WIDTH - MARGIN_RIGHT, HEIGHT - MARGIN_BOTTOM)], outline=(71, 85, 105, 255), width=2)

# Helper to draw polygons
def draw_poly_feature(geom, fill_color, outline_color, outline_width=2):
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    gtype = geom["type"]
    coords = geom["coordinates"]
    polys = [coords] if gtype == "Polygon" else coords
    
    for poly in polys:
        for ring in poly:
            pts = [geo_to_pixel(pt[0], pt[1]) for pt in ring]
            if len(pts) >= 3:
                if fill_color:
                    ov_draw.polygon(pts, fill=fill_color)
                if outline_color:
                    ov_draw.line(pts + [pts[0]], fill=outline_color, width=outline_width)
                    
    img.alpha_composite(overlay)

# 2. Draw Sikkim State Boundary
if boundary_fc:
    for feat in boundary_fc["features"]:
        draw_poly_feature(feat["geometry"], fill_color=(30, 41, 59, 120), outline_color=(226, 232, 240, 255), outline_width=3)

# 3. Draw Mapped Observation Extent
if extent_fc:
    for feat in extent_fc["features"]:
        draw_poly_feature(feat["geometry"], fill_color=(16, 185, 129, 35), outline_color=(16, 185, 129, 220), outline_width=2)

# 4. Draw Google Earth Polygons
if ge_poly_fc:
    for feat in ge_poly_fc["features"]:
        draw_poly_feature(feat["geometry"], fill_color=(239, 68, 68, 140), outline_color=(248, 113, 113, 255), outline_width=1)

# 5. Draw Cartosat Polygons
if cart_poly_fc:
    for feat in cart_poly_fc["features"]:
        # Blue for scarps/deposits
        draw_poly_feature(feat["geometry"], fill_color=(6, 182, 212, 160), outline_color=(34, 211, 238, 255), outline_width=1)

# 6. Draw Cartosat Derived Unions (Dashed outline representation)
if cart_union_fc:
    for feat in cart_union_fc["features"]:
        draw_poly_feature(feat["geometry"], fill_color=None, outline_color=(250, 204, 21, 200), outline_width=2)

# 7. Draw Google Earth Points
if ge_pt_fc:
    for feat in ge_pt_fc["features"]:
        pt = feat["geometry"]["coordinates"]
        px, py = geo_to_pixel(pt[0], pt[1])
        draw.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=(234, 179, 8, 255), outline=(0, 0, 0, 255), width=1)

# 8. Render Header & Title Banner
draw.rectangle([(0, 0), (WIDTH, 200)], fill=(15, 23, 42, 255))
draw.text((MARGIN_LEFT, 25), "SIKKIM HISTORICAL LANDSLIDE GIS INVENTORY MAP", fill=(248, 250, 252, 255), font=title_font)
draw.text((MARGIN_LEFT, 75), "Local-First Spatial Inspection & Data Validation Layer (EPSG:4326)", fill=(56, 189, 248, 255), font=subtitle_font)

# Disclaimer Box
draw.rectangle([(MARGIN_LEFT, 115), (WIDTH - MARGIN_RIGHT, 180)], fill=(30, 41, 59, 255), outline=(245, 158, 11, 255), width=2)
draw.text((MARGIN_LEFT + 20, 125), "CRITICAL SEMANTIC NOTICE: ZENODO 8169506 IS A PARTIAL LOCALIZED SOUTHERN SIKKIM INVENTORY.", fill=(251, 191, 36, 255), font=label_font)
draw.text((MARGIN_LEFT + 20, 150), "Areas outside the green mapped extent footprint are UNINVENTORIED (Data Not Held) and MUST NOT be treated as zero landslides.", fill=(226, 232, 240, 255), font=small_font)

# 9. Render Legend & Layer Count Card (Bottom Footer)
footer_y = HEIGHT - MARGIN_BOTTOM + 55
draw.rectangle([(MARGIN_LEFT, footer_y), (WIDTH - MARGIN_RIGHT, HEIGHT - 30)], fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=2)

# Legend Column 1: Boundaries & Extent
draw.rectangle([(MARGIN_LEFT + 20, footer_y + 20), (MARGIN_LEFT + 45, footer_y + 35)], fill=(30, 41, 59, 255), outline=(226, 232, 240, 255), width=2)
draw.text((MARGIN_LEFT + 55, footer_y + 18), "Sikkim State Boundary (GADM v4.1)", fill=(241, 245, 249, 255), font=small_font)

draw.rectangle([(MARGIN_LEFT + 20, footer_y + 50), (MARGIN_LEFT + 45, footer_y + 65)], fill=(16, 185, 129, 80), outline=(16, 185, 129, 255), width=2)
draw.text((MARGIN_LEFT + 55, footer_y + 48), "GE Mapped Extent Footprint (1 Feature)", fill=(52, 211, 153, 255), font=small_font)

draw.rectangle([(MARGIN_LEFT + 20, footer_y + 80), (MARGIN_LEFT + 45, footer_y + 95)], fill=(15, 23, 42, 255), outline=(71, 85, 105, 255), width=1)
draw.text((MARGIN_LEFT + 55, footer_y + 78), "Unmapped Sikkim Area (UNINVENTORIED)", fill=(148, 163, 184, 255), font=small_font)

# Legend Column 2: Landslide Inventory Layers
col2_x = MARGIN_LEFT + 550
draw.rectangle([(col2_x, footer_y + 20), (col2_x + 25, footer_y + 35)], fill=(239, 68, 68, 180), outline=(248, 113, 113, 255), width=1)
draw.text((col2_x + 35, footer_y + 18), "GE Landslide Polygons (255 Source Features)", fill=(248, 113, 113, 255), font=small_font)

draw.ellipse([(col2_x + 5, footer_y + 50), (col2_x + 20, footer_y + 65)], fill=(234, 179, 8, 255), outline=(0, 0, 0, 255), width=1)
draw.text((col2_x + 35, footer_y + 48), "GE Landslide Points (185 Source Features)", fill=(250, 204, 21, 255), font=small_font)

draw.rectangle([(col2_x, footer_y + 80), (col2_x + 25, footer_y + 95)], fill=(6, 182, 212, 180), outline=(34, 211, 238, 255), width=1)
draw.text((col2_x + 35, footer_y + 78), "Cartosat Landslide Polygons (67 Source Features)", fill=(34, 211, 238, 255), font=small_font)

# Legend Column 3: Derived Layers & Total Summary
col3_x = MARGIN_LEFT + 1150
draw.rectangle([(col3_x, footer_y + 20), (col3_x + 25, footer_y + 35)], fill=(15, 23, 42, 255), outline=(250, 204, 21, 255), width=2)
draw.text((col3_x + 35, footer_y + 18), "Cartosat Derived Unions (23 Features - DERIVED)", fill=(253, 224, 71, 255), font=small_font)

draw.text((col3_x, footer_y + 50), "SOURCE INVENTORY SUMMARY:", fill=(241, 245, 249, 255), font=label_font)
draw.text((col3_x, footer_y + 78), "507 Source Inventory Features across 3 Layers (NOT Unique Landslides)", fill=(56, 189, 248, 255), font=small_font)

# Save final map image
img.save(out_map_path, "PNG")
print(f"Map image successfully generated and saved to {out_map_path} ({os.path.getsize(out_map_path):,} bytes)")
