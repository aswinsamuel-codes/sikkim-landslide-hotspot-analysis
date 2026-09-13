import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

DERIVED_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\data\derived"
TEMPORAL_DIR = os.path.join(DERIVED_DIR, "temporal")
EXPORTS_DIR = r"d:\karunya\hackathon\SIH\Sikkim landslide hotspot analysis\exports"

out_map_path = os.path.join(EXPORTS_DIR, "sikkim_temporal_observation_map.png")

with open(os.path.join(DERIVED_DIR, "sikkim_state_boundary_4326.geojson"), "r", encoding="utf-8") as f:
    boundary_fc = json.load(f)

with open(os.path.join(DERIVED_DIR, "zenodo_mapped_extent_4326.geojson"), "r", encoding="utf-8") as f:
    extent_fc = json.load(f)

WIDTH, HEIGHT = 2000, 2200
MARGIN_LEFT, MARGIN_RIGHT = 120, 80
MARGIN_TOP, MARGIN_BOTTOM = 220, 260

MAP_W = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
MAP_H = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

MIN_LON, MAX_LON = 87.95, 89.05
MIN_LAT, MAX_LAT = 27.00, 28.20

def geo_to_pixel(lon, lat):
    px = MARGIN_LEFT + int((lon - MIN_LON) / (MAX_LON - MIN_LON) * MAP_W)
    py = MARGIN_TOP + int((MAX_LAT - lat) / (MAX_LAT - MIN_LAT) * MAP_H)
    return px, py

img = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 255))
draw = ImageDraw.Draw(img)

try:
    title_font = ImageFont.truetype("arial.ttf", 36)
    subtitle_font = ImageFont.truetype("arial.ttf", 22)
    label_font = ImageFont.truetype("arial.ttf", 18)
    small_font = ImageFont.truetype("arial.ttf", 15)
except:
    title_font = subtitle_font = label_font = small_font = ImageFont.load_default()

for lon_deg in [88.0, 88.2, 88.4, 88.6, 88.8, 89.0]:
    x1, y1 = geo_to_pixel(lon_deg, MIN_LAT)
    x2, y2 = geo_to_pixel(lon_deg, MAX_LAT)
    draw.line([(x1, y1), (x2, y2)], fill=(51, 65, 85, 180), width=1)
    draw.text((x1 - 20, HEIGHT - MARGIN_BOTTOM + 15), f"{lon_deg:.1f}°E", fill=(148, 163, 184, 255), font=small_font)

for lat_deg in [27.0, 27.2, 27.4, 27.6, 27.8, 28.0, 28.2]:
    x1, y1 = geo_to_pixel(MIN_LON, lat_deg)
    x2_map, _ = geo_to_pixel(MAX_LON, lat_deg)
    draw.line([(x1, y1), (x2_map, y1)], fill=(51, 65, 85, 180), width=1)
    draw.text((MARGIN_LEFT - 75, y1 - 8), f"{lat_deg:.1f}°N", fill=(148, 163, 184, 255), font=small_font)

draw.rectangle([(MARGIN_LEFT, MARGIN_TOP), (WIDTH - MARGIN_RIGHT, HEIGHT - MARGIN_BOTTOM)], outline=(71, 85, 105, 255), width=2)

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

for feat in boundary_fc["features"]:
    draw_poly_feature(feat["geometry"], fill_color=(30, 41, 59, 120), outline_color=(226, 232, 240, 255), outline_width=3)

for feat in extent_fc["features"]:
    draw_poly_feature(feat["geometry"], fill_color=(16, 185, 129, 35), outline_color=(16, 185, 129, 220), outline_width=2)

YEAR_COLORS = {
    2002: (244, 63, 94),
    2005: (249, 115, 22),
    2006: (245, 158, 11),
    2009: (234, 179, 8),
    2010: (132, 204, 22),
    2011: (16, 185, 129),
    2012: (6, 182, 212),
    2015: (59, 130, 246),
    2017: (139, 92, 246),
    2018: (217, 70, 239),
    2019: (244, 114, 182),
}

year_files = [f for f in os.listdir(TEMPORAL_DIR) if f.startswith("zenodo_observations_") and f.endswith(".geojson")]

for yf in year_files:
    ypath = os.path.join(TEMPORAL_DIR, yf)
    with open(ypath, "r", encoding="utf-8") as f:
        t_fc = json.load(f)
        
    for feat in t_fc["features"]:
        geom = feat["geometry"]
        yr = feat["properties"].get("observation_year")
        color = YEAR_COLORS.get(yr, (148, 163, 184)) if yr else (100, 116, 139)
        
        gtype = geom["type"]
        if gtype == "Point":
            pt = geom["coordinates"]
            px, py = geo_to_pixel(pt[0], pt[1])
            draw.ellipse([(px - 4, py - 4), (px + 4, py + 4)], fill=color + (255,), outline=(0, 0, 0, 255), width=1)
        else:
            draw_poly_feature(geom, fill_color=color + (140,), outline_color=color + (255,), outline_width=1)

# Header
draw.rectangle([(0, 0), (WIDTH, 200)], fill=(15, 23, 42, 255))
draw.text((MARGIN_LEFT, 25), "SIKKIM HISTORICAL LANDSLIDE OBSERVATION YEAR MAP", fill=(248, 250, 252, 255), font=title_font)
draw.text((MARGIN_LEFT, 75), "Year-Wise Imagery Observation Record Distribution (2002 - 2019)", fill=(56, 189, 248, 255), font=subtitle_font)

# Disclaimer Box
draw.rectangle([(MARGIN_LEFT, 115), (WIDTH - MARGIN_RIGHT, 180)], fill=(30, 41, 59, 255), outline=(245, 158, 11, 255), width=2)
draw.text((MARGIN_LEFT + 20, 125), "MANDATORY SEMANTIC LIMITATION:", fill=(251, 191, 36, 255), font=label_font)
draw.text((MARGIN_LEFT + 20, 150), "Observation year indicates the year associated with the source imagery/observation record. It is NOT a confirmed landslide failure date.", fill=(226, 232, 240, 255), font=small_font)

# Footer
footer_y = HEIGHT - MARGIN_BOTTOM + 55
draw.rectangle([(MARGIN_LEFT, footer_y), (WIDTH - MARGIN_RIGHT, HEIGHT - 30)], fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=2)

draw.text((MARGIN_LEFT + 20, footer_y + 15), "OBSERVATION YEARS PRESENT:", fill=(241, 245, 249, 255), font=label_font)

col_x = MARGIN_LEFT + 20
col_y = footer_y + 45

for yr in [2002, 2005, 2006, 2009, 2010, 2011]:
    color = YEAR_COLORS[yr]
    draw.rectangle([(col_x, col_y), (col_x + 20, col_y + 15)], fill=color + (255,), outline=(255, 255, 255, 255), width=1)
    draw.text((col_x + 28, col_y - 2), f"{yr}", fill=(241, 245, 249, 255), font=small_font)
    col_x += 110

col_x = MARGIN_LEFT + 20
col_y = footer_y + 75

for yr in [2012, 2015, 2017, 2018, 2019]:
    color = YEAR_COLORS[yr]
    draw.rectangle([(col_x, col_y), (col_x + 20, col_y + 15)], fill=color + (255,), outline=(255, 255, 255, 255), width=1)
    draw.text((col_x + 28, col_y - 2), f"{yr}", fill=(241, 245, 249, 255), font=small_font)
    col_x += 110

draw.rectangle([(col_x, col_y), (col_x + 20, col_y + 15)], fill=(100, 116, 139, 255), outline=(255, 255, 255, 255), width=1)
draw.text((col_x + 28, col_y - 2), "Active/NULL", fill=(148, 163, 184, 255), font=small_font)

draw.text((MARGIN_LEFT + 950, footer_y + 15), "NEUTRAL DISTRIBUTION NOTICE:", fill=(241, 245, 249, 255), font=label_font)
draw.text((MARGIN_LEFT + 950, footer_y + 45), "2011 represents the highest source-feature count in this dataset.", fill=(148, 163, 184, 255), font=small_font)
draw.text((MARGIN_LEFT + 950, footer_y + 70), "Variation reflects satellite imagery availability & mapping intensity, NOT failure counts.", fill=(56, 189, 248, 255), font=small_font)

img.save(out_map_path, "PNG")
print(f"Temporal map image successfully saved to {out_map_path} ({os.path.getsize(out_map_path):,} bytes)")
