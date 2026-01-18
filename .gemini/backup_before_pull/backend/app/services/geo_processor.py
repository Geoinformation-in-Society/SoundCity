import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from shapely.geometry import shape, Point, Polygon, MultiPolygon
from shapely.ops import unary_union

logger = logging.getLogger(__name__)

DATA_DIR = Path("app/data/raw")

def load_geojson(filename: str) -> Dict[str, Any]:
    file_path = DATA_DIR / filename
    if not file_path.exists():
        logger.warning(f"{filename} not found.")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {filename}: {e}")
        return None

def calculate_green_score(district_geom: Polygon, green_shapes: List[Polygon]) -> float:
    """Calculate percentage of district area covered by green spaces."""
    if not green_shapes:
        return 0.0
    
    district_area = district_geom.area
    if district_area == 0:
        return 0.0
        
    # Find intersecting green spaces
    intersecting_green = []
    for green in green_shapes:
        if district_geom.intersects(green):
            intersection = district_geom.intersection(green)
            intersecting_green.append(intersection)
            
    if not intersecting_green:
        return 0.0
        
    # Union to handle overlapping green spaces (though uncommon for cadastral data)
    # Using unary_union might be slow if many geometries, but correct.
    # Optimization: simple sum of areas if we assume no overlap.
    # Let's trust the source data doesn't overlap excessively.
    total_green_area = sum(p.area for p in intersecting_green)
    
    # Cap at 1.0
    return min(1.0, total_green_area / district_area)

def calculate_tree_density(district_geom: Polygon, tree_points: List[Point]) -> int:
    """Calculate number of trees in district."""
    if not tree_points:
        return 0
    # Optimize: check bounds first or use spatial index if available
    count = 0
    for tree in tree_points:
        if district_geom.contains(tree):
            count += 1
    return count

def calculate_air_quality(district_geom: Polygon, sensors: List[Dict]) -> float:
    """Calculate average PM10 value from sensors in district."""
    # sensors is list of dict {lat, lon, P1, P2}
    if not sensors:
        return None
        
    values = []
    for s in sensors:
        pt = Point(s['lon'], s['lat'])
        if district_geom.contains(pt):
            # Prefer P1 (PM10) or P2 (PM2.5). Let's average valid readings.
            val = s.get('P1') or s.get('P2')
            if val is not None:
                values.append(val)
                
    if not values:
        return None
        
    avg_pm = sum(values) / len(values)
    # Map PM10 (approx) to 1-5 scale. 
    # < 20 = 5 (Excellent), 20-40 = 4, 40-50 = 3, 50-75 = 2, > 75 = 1
    if avg_pm < 20: return 5.0
    if avg_pm < 35: return 4.0
    if avg_pm < 50: return 3.0
    if avg_pm < 75: return 2.0
    return 1.0

def process_neighborhoods() -> List[Dict[str, Any]]:
    """Process raw data and return enriched neighborhood objects."""
    
    districts_data = load_geojson("districts.geojson")
    if not districts_data: return []

    green_data = load_geojson("green_spaces.geojson")
    noise_data = load_geojson("noise.geojson")
    trees_data = load_geojson("trees.geojson") # WFS GeoJSON
    air_data = load_geojson("air_sensors_global.json")

    # Pre-process Green Spaces
    green_shapes = []
    if green_data:
        for feature in green_data.get("features", []):
            try:
                geom = shape(feature["geometry"])
                if geom.is_valid: green_shapes.append(geom)
            except: pass

    # Pre-process Noise
    noise_shapes = []
    if noise_data:
         for feature in noise_data.get("features", []):
            try:
                geom = shape(feature["geometry"])
                level = feature["properties"].get("Pegel", 50) 
                if geom.is_valid: noise_shapes.append((geom, level))
            except: pass
            
    # Pre-process Trees (Points)
    tree_points = []
    if trees_data:
        for feature in trees_data.get("features", []):
            try:
                geom = shape(feature["geometry"])
                if isinstance(geom, Point):
                    tree_points.append(geom)
            except: pass

    # Pre-process Air Sensors (Filter for Münster Box approx: Lat 51.8-52.1, Lon 7.4-7.8)
    # This optimization is CRITICAL before spatial check loop
    relevant_sensors = []
    if air_data: # air_data is list of sensor objects? or one wrapper? Sensor.community 'data.json' is a list of sensor objects directly.
        # Check structure: usually list of dicts
        sensors_list = air_data if isinstance(air_data, list) else []
        for s in sensors_list:
            try:
                lat = float(s['location']['latitude'])
                lon = float(s['location']['longitude'])
                # Coarse box check
                if 51.8 <= lat <= 52.1 and 7.4 <= lon <= 7.8:
                    # Extract PM values
                    p1 = None # PM10
                    p2 = None # PM2.5
                    for data_val in s.get('sensordatavalues', []):
                        if data_val['value_type'] == 'P1': p1 = float(data_val['value'])
                        if data_val['value_type'] == 'P2': p2 = float(data_val['value'])
                    relevant_sensors.append({'lat': lat, 'lon': lon, 'P1': p1, 'P2': p2})
            except: continue

    # print(f"DEBUG: Loaded {len(districts_data.get('features', []))} districts.")
    # print(f"DEBUG: Loaded {len(green_shapes)} green shapes.")
    # print(f"DEBUG: Loaded {len(tree_points)} tree points.")
    
    results = []
    
    for feature in districts_data.get("features", []):
        props = feature.get("properties", {})
        # Name might be "Name", "NAME", or "NAME_STATI" (from Muenster Open Data)
        name = props.get("Name", props.get("NAME", props.get("NAME_STATI", "Unknown District")))
        id_ = str(props.get("Nr", props.get("NR", props.get("NR_STATIST", results.__len__() + 1))))
        
        try:
            district_geom = shape(feature["geometry"])
        except: continue
            
        # 1. Green Score
        green_score_val = calculate_green_score(district_geom, green_shapes)
        green_score_display = round(green_score_val * 5.0, 1)

        # 2. Noise Score
        raw_noise = 0.3
        if noise_shapes:
            hit_count = sum(1 for n_geom, _ in noise_shapes if district_geom.intersects(n_geom))
            raw_noise = min(1.0, hit_count * 0.1)
        noise_level = round(1.0 + (1.0 - raw_noise) * 4.0, 1)

        # 3. Tree Count
        tree_cnt = calculate_tree_density(district_geom, tree_points)
        
        # 4. Air Quality
        air_val = calculate_air_quality(district_geom, relevant_sensors)
        if air_val is not None:
             air_quality = round(air_val, 1)
        else:
             # Fallback if no sensors in district: 
             # Heuristic based on green score + distance from center
             center = Point(7.62, 51.96)
             dist = district_geom.centroid.distance(center)
             raw_air = min(1.0, 0.5 + (dist * 2.0) + (green_score_val * 0.5))
             air_quality = round(1.0 + (raw_air * 4.0), 1)

        # 5. Heat Stress (Heuristic)
        # Low Green + High Density (proxy: 1 - green_score) -> High Heat
        # Map: High Green = Low Heat (Score 1), Low Green = High Heat (Score 5)
        # So Heat Score ~ 5.0 - (green_score * 4.0)
        # But Trees provide cooling more than grass.
        # Let's say: Heat = 5 - (GreenScore * 2 + TreeScore * 2)?
        # A simpler robust proxy: Heat Risk is high (5) if green is low (0).
        heat_score = round(max(1.0, 5.0 - (green_score_val * 4.0)), 1)
        

        results.append({
            "id": id_,
            "name": name,
            "latitude": district_geom.centroid.y,
            "longitude": district_geom.centroid.x,
            "air_quality": air_quality,
            "noise_level": noise_level,
            "green_score": green_score_display,
            "tree_cnt": tree_cnt,
            "heat_score": heat_score,
            "geojson": feature
        })
        
    if results:
        logger.info(f"Processed {len(results)} neighborhoods. First item: {results[0]}")
        
    return results
