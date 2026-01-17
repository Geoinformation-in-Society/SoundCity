"""
Data collection script for Sound City
Collects air quality and noise data for Münster neighborhoods
Now uses real neighborhoods from OpenStreetMap
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from shapely.geometry import shape, Point, Polygon

class MunsterDataCollector:
    """Collector for Münster neighborhood environmental data"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "app" / "data"
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"
        self.geojson_path = self.base_path / "geojson"
        
        # Create directories if they don't exist
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.geojson_path.mkdir(parents=True, exist_ok=True)

        # Load neighborhoods from the fetched data
        self.neighborhoods = self.load_neighborhoods()
        self.boundaries = self.load_boundaries()

        # Load raw geospatial data for analysis
        self.green_shapes = self._load_green_spaces()
        self.tree_points = self._load_trees()
        self.air_sensors = self._load_air_sensors()
        self.noise_shapes = self._load_noise_shapes()

    def _load_geojson_raw(self, filename: str) -> Optional[Dict]:
        """Helper to load raw GeoJSON from raw_path"""

        path = self.raw_path / filename

        if not path.exists():
            print(f"⚠ Raw file not found: {filename}")
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"✗ Error loading {filename}: {e}")
            return None

    def _load_air_sensors(self) -> List[Dict]:
        """
        Load air quality data:
        1. Try official Münster Open Data first.
        2. Filter for Münster region.
        """
        print("  💨 Loading air quality data...")
        sensors = []
        
        # 1. Official Data
        # URL found via browser: https://www.muenster01.de/luftqualitaet/data/luftqualitaet_muenster.geojson
        try:
            url = "https://www.muenster01.de/luftqualitaet/data/luftqualitaet_muenster.geojson"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for feature in data.get('features', []):
                    props = feature.get('properties', {})
                    geom = feature.get('geometry', {})
                    if geom.get('type') == 'Point':
                        coords = geom.get('coordinates')
                        
                        # Extract official values
                        # Keys seen: "Feinstaub (PM₁₀)", "Stickstoffdioxid (NO₂)", "Luftqualitätsindex"
                        pm10 = props.get("Feinstaub (PM\u2081\u2080)")
                        no2 = props.get("Stickstoffdioxid (NO\u2082)")
                        
                        # Ensure values are float or None
                        if pm10 == '-' or pm10 is None: pm10 = None
                        else: pm10 = float(pm10)
                        
                        # Official stations don't always have PM2.5, but key is "Feinstaub (PM₂.₅)" if present
                        pm25 = props.get("Feinstaub (PM\u2082,\u2085)")
                        if pm25 == '-' or pm25 is None: pm25 = None
                        else: pm25 = float(pm25)

                        sensors.append({
                            'lat': coords[1],
                            'lon': coords[0],
                            'source': 'official',
                            'P1': pm10,  # Map to standard key for PM10
                            'P2': pm25,  # Map to standard key for PM2.5
                            'NO2': no2,  # Extra key
                            'props': props
                        })
                print(f"    ✓ Loaded {len(sensors)} official air quality stations")
        except Exception as e:
            print(f"    ⚠ Could not load official air data: {e}")

        # 2. Sensor.Community (Global Fallback/Augmentation)
        try:
            data = self._load_geojson_raw("air_sensors_global.json")
            if isinstance(data, list):
                for s in data:
                    try:
                        lat = float(s['location']['latitude'])
                        lon = float(s['location']['longitude'])
                        # Filter for Münster region
                        if 51.8 <= lat <= 52.1 and 7.4 <= lon <= 7.8:
                            p1 = None; p2 = None
                            for val in s.get('sensordatavalues', []):
                                if val['value_type'] == 'P1': p1 = float(val['value'])
                                if val['value_type'] == 'P2': p2 = float(val['value'])
                            sensors.append({'lat': lat, 'lon': lon, 'P1': p1, 'P2': p2, 'source': 'sensor_community'})
                    except: pass
        except Exception as e:
            print(f"    ⚠ Error processing sensor.community data: {e}")
            
        print(f"    ✓ Total air sensors/stations: {len(sensors)}")
        return sensors

    def calculate_noise_score_official(self, district_geom: Polygon) -> Dict:
        """
        Calculate noise score based on intersection with official Noise Map polygons.
        official maps have dB ranges.
        """
        if not self.noise_shapes or not any(self.noise_shapes.values()):
            return {'score': None, 'method': 'No official data'}
            
        # We process 'street_day' as the primary indicator for general noise
        # But 'street_night' is also critical for residential quality.
        # Let's average the impact of street_day and street_night.
        
        def get_db_impact(shapes_list, geom):
            total_area = geom.area
            if total_area == 0: return 0
            
            w_db_sum = 0.0
            touched_area = 0.0
            
            # Ensure district geom is valid
            if not geom.is_valid:
                geom = geom.buffer(0)

            for item in shapes_list:
                shape_geom = item['geom']
                if not shape_geom.is_valid:
                    shape_geom = shape_geom.buffer(0)
                    
                try:
                    if geom.intersects(shape_geom):
                        inter = geom.intersection(shape_geom)
                        area = inter.area
                        if area > 0:
                            # Extract dB level from props
                            # Typical props in NRW maps: "pegel" -> "LDEN" or range strings?
                            # Let's assume range or extract regex if needed.
                            # Based on standard: often "LDEN" or "L_Day" is an integer or range.
                            # Let's try to find a numeric value. 
                            # If we look at the file, it likely has valid properties.
                            # For now, let's treat existence as "High Noise" (e.g. >55dB is usually mapped)
                            # If props exist, assume >55dB.
                            
                            # Refined: Parse "pegel" or similar. 
                            # If unknown, assume 65dB (mid-range of noisy areas).
                            db = 65.0 
                            props = item['props']
                            # Try to find a level
                            for k, v in props.items():
                                if 'db' in k.lower() or 'level' in k.lower() or 'klasse' in k.lower():
                                    if isinstance(v, (int, float)):
                                        db = float(v)
                                        break
                                        
                            w_db_sum += area * db
                            touched_area += area
                except: pass
            
            # If no intersection, assume background noise ~40dB
            if touched_area < total_area:
                 w_db_sum += (total_area - touched_area) * 40.0
                 
            return w_db_sum / total_area

        # Calculate average dB for the district
        avg_db_day = get_db_impact(self.noise_shapes.get('street_day', []), district_geom)
        avg_db_night = get_db_impact(self.noise_shapes.get('street_night', []), district_geom)
        
        avg_db = (avg_db_day + avg_db_night) / 2.0
        
        # Map dB to score (1-5)
        # < 45: 5.0 (Quiet)
        # 45-50: 4.5
        # 50-55: 4.0
        # 55-60: 3.0
        # 60-65: 2.0
        # > 65: 1.0 (Loud)
        
        score = 1.0
        if avg_db < 45: score = 5.0
        elif avg_db < 50: score = 4.5
        elif avg_db < 55: score = 4.0
        elif avg_db < 60: score = 3.0
        elif avg_db < 65: score = 2.0
        
        return {
            'score': score,
            'estimated_db': round(avg_db, 1),
            'method': 'Official Noise Map (2022)'
        }

    # ... (existing methods) ...

    def collect_all_data(self) -> List[Dict]:
        """
        Collect data for all neighborhoods.
        """
        
        results = []
        
        for i, neighborhood in enumerate(self.neighborhoods, 1):
            print(f"[{i}/{len(self.neighborhoods)}] {neighborhood['name']}")
            
            lat = neighborhood['latitude']
            lon = neighborhood['longitude']
            n_id = neighborhood['id']
            
            # Get boundary geometry
            geom_dict = self.boundaries.get(n_id)
            shapely_geom = None
            
            if geom_dict:
                try:
                    shapely_geom = shape(geom_dict)
                except: pass

            # Calculate Green Score & Trees & Heat
            green_space_score = 0.0
            tree_greenness_score = 0.0
            urban_heat_score = 0.0
            
            if shapely_geom:
                print("\n🌳 GREEN & HEAT:")
                green_space_score = self.calculate_green_score(shapely_geom)
                tree_greenness_score = self.calculate_tree_density(shapely_geom)
                urban_heat_score = self.calculate_heat_score(green_space_score)
                print(f"    ✓ Green: {green_space_score*100:.1f}%, Trees: {tree_greenness_score}, Heat: {urban_heat_score}/5")

            
            # Collect air quality
            print("\n💨 AIR QUALITY:")
            air_quality_score = 3.5 
            air_data = {'score': None, 'estimated': True}
            
            if shapely_geom:
                 air_data = self.calculate_air_quality(shapely_geom)
                 if air_data['score'] is not None:
                     air_quality_score = air_data['score']
                     print(f"    ✓ Calculated from {air_data.get('sensor_count', 0)} sensors: Score {air_quality_score}/5")
                 else:
                     # Fallback heuristic
                     center_lat, center_lon = 51.9607, 7.6261
                     dist = ((lat - center_lat)**2 + (lon - center_lon)**2)**0.5 * 111 
                     raw_air = min(1.0, 0.4 + (dist/10.0) + (green_space_score * 0.5))
                     air_quality_score = round(1.0 + (raw_air * 4.0), 1)
                     print(f"    ⚠ No sensors, using spatial heuristic: {air_quality_score}/5")

            
            # Estimate noise
            print("\n🔊 NOISE POLLUTION:")
            
            if shapely_geom and self.noise_shapes and any(self.noise_shapes.values()):
                 # Use official data if available
                 noise_data = self.calculate_noise_score_official(shapely_geom)
                 print(f"    ✓ Official Noise Map: Score {noise_data['score']}/5 ({noise_data['estimated_db']} dB)")
            else:
                 # Fallback to Overpass/Distance
                 noise_data = self.estimate_noise_level(lat, lon, n_id)

            # Compile result
            result = {
                "id": n_id,
                "name": neighborhood['name'],
                "latitude": lat,
                "longitude": lon,
                "air_quality": round(air_quality_score, 1),
                "noise_level": round(noise_data['score'], 1),
                "green_space": round(green_space_score * 5.0, 1), 
                "tree_greenness": tree_greenness_score,
                "urban_heat": urban_heat_score,
                "geojson": geom_dict,  
                "metadata": {
                    "osm_id": neighborhood.get('osm_id'),
                    "pm25_raw": air_data.get('pm25'),
                    "pm10_raw": air_data.get('pm10'),
                    "estimated_db": noise_data.get('estimated_db'),
                    "green_coverage_pct": round(green_space_score * 100, 1),
                    "data_sources": {
                        "air_quality": "Sensor.Community + Official (LANUV)" if not air_data.get('estimated') else "Spatial Heuristic",
                        "noise": noise_data.get('method', 'Estimated'),
                        "boundaries": "OpenStreetMap",
                        "trees": "Baumkataster WFS",
                        "heat": "Heuristic (Inverse Green) - EU Data requires auth"
                    },
                    "last_updated": datetime.now().isoformat()
                }
            }
            
            results.append(result)
            print(f"\n  ✓ Complete: Air={air_quality_score}/5, Noise={noise_data['score']}/5")
            print("  " + "-"*66 + "\n")
            
            if noise_data.get('method') == 'OSM road analysis' and i < len(self.neighborhoods):
                time.sleep(1.0)
        
        return results

    def fetch_official_noise_data(self):
        """Fetch official noise GeoJSONs if not present"""
        files = {
            "noise_street_day.json": "https://opendata.stadt-muenster.de/sites/default/files/laerm_stra%C3%9Fe_tag.json",
            "noise_street_night.json": "https://opendata.stadt-muenster.de/sites/default/files/laerm_stra%C3%9Fe_nacht.json",
            "noise_industry_day.json": "https://opendata.stadt-muenster.de/sites/default/files/laerm_gewerbe_tag.json",
            "noise_industry_night.json": "https://opendata.stadt-muenster.de/sites/default/files/laerm_gewerbe_nacht.json"
        }
        
        print("  🔊 Checking official Noise Data...")
        for filename, url in files.items():
            path = self.raw_path / filename
            if not path.exists():
                print(f"    ⬇ Downloading {filename}...")
                try:
                    r = requests.get(url, stream=True)
                    r.raise_for_status()
                    with open(path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                except Exception as e:
                    print(f"    ✗ Failed to download {filename}: {e}")
            else:
                pass # print(f"    ✓ {filename} exists")

    def _load_noise_shapes(self) -> Dict[str, List[Dict]]:
        """Load noise polygons for spatial analysis"""
        self.fetch_official_noise_data()
        
        noise_data = {'street_day': [], 'street_night': [], 'industry_day': [], 'industry_night': []}
        
        files = {
            'street_day': "noise_street_day.json",
            'street_night': "noise_street_night.json",
            'industry_day': "noise_industry_day.json",
            'industry_night': "noise_industry_night.json"
        }
        
        print("  🔊 Loading Noise GeoJSONs...")
        for key, filename in files.items():
            data = self._load_geojson_raw(filename)
            if data:
                count = 0
                for feature in data.get('features', []):
                    try:
                        # Extract dB level. Usually in properties like "db_low", "db_high", "klasse"
                        # Or "Pegel", "LDEN" etc.
                        geom = shape(feature['geometry'])
                        props = feature.get('properties', {})
                        noise_data[key].append({'geom': geom, 'props': props})
                        count += 1
                    except: pass
                print(f"    ✓ {key}: {count} polygons")
        
        # Verify if any data was loaded
        total_shapes = sum(len(v) for v in noise_data.values())
        print(f"    ✓ DEBUG: Total noise polygons loaded: {total_shapes}")
        return noise_data

    def _load_green_spaces(self) -> List[Polygon]:
        """Load green spaces as Shapely polygons"""
        print("  🌳 Loading green spaces...")
        data = self._load_geojson_raw("green_spaces.geojson")
        shapes = []
        if data:
            for feature in data.get("features", []):
                try:
                    geom = shape(feature["geometry"])
                    if geom.is_valid: shapes.append(geom)
                except: pass
        print(f"    ✓ Loaded {len(shapes)} green space polygons")
        return shapes

    def _load_trees(self) -> List[Point]:
        """Load trees as Shapely points"""
        print("  🌲 Loading trees...")
        data = self._load_geojson_raw("trees.geojson")
        points = []
        if data:
            for feature in data.get("features", []):
                try:
                    geom = shape(feature["geometry"])
                    if isinstance(geom, Point):
                        points.append(geom)
                except: pass
        print(f"    ✓ Loaded {len(points)} tree points")
        return points
    
    def load_neighborhoods(self) -> List[Dict]:
        """
        Load neighborhoods directly from the geojson boundaries file.
        
        Returns:
            List of neighborhoods with center coordinates
        """
        geojson_file = self.geojson_path / "neighborhoods_boundaries.geojson"
        
        if not geojson_file.exists():
            print("⚠ Neighborhoods GeoJSON not found!")
            print("  Please run: python scripts/fetch_neighborhoods.py first")
            print("\n  Using default neighborhoods as fallback...")
            return self._get_default_neighborhoods()
        
        try:
            with open(geojson_file, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            
            neighborhoods = []
            for feature in geojson_data.get('features', []):
                props = feature.get('properties', {})
                geometry = feature.get('geometry', {})
                
                # Extract neighborhood name
                name = props.get('NAME_STATI') or feature.get('id', 'Unknown')
                neighborhood_id = name.lower().replace(' ', '-').replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')
                
                # Calculate centroid from geometry
                center = self._calculate_centroid(geometry)
                
                neighborhood = {
                    'id': neighborhood_id,
                    'name': name,
                    'latitude': center['lat'],
                    'longitude': center['lon'],
                    'osm_id': props.get('OBJECTID', 0)
                }
                
                neighborhoods.append(neighborhood)
            
            print(f"✓ Loaded {len(neighborhoods)} neighborhoods from GeoJSON boundaries")
            return neighborhoods
        except Exception as e:
            print(f"✗ Error loading neighborhoods from GeoJSON: {e}")
            return self._get_default_neighborhoods()
    
    def _calculate_centroid(self, geometry: Dict) -> Dict:
        """
        Calculate centroid of a polygon geometry.
        
        Args:
            geometry: GeoJSON geometry object
            
        Returns:
            Dictionary with lat and lon
        """
        if geometry.get('type') != 'Polygon':
            return {'lat': 51.9607, 'lon': 7.6261}  # Default to Münster center
        
        coords = geometry.get('coordinates', [[]])[0]
        if not coords:
            return {'lat': 51.9607, 'lon': 7.6261}
        
        # Simple centroid calculation
        total_lat = sum(c[1] for c in coords)
        total_lon = sum(c[0] for c in coords)
        count = len(coords)
        
        return {
            'lat': round(total_lat / count, 4),
            'lon': round(total_lon / count, 4)
        }
    
    def load_boundaries(self) -> Dict:
        """
        Load neighborhood boundaries from GeoJSON file.
        
        Returns:
            Dictionary mapping neighborhood ID to geometry
        """
        geojson_file = self.geojson_path / "neighborhoods_boundaries.geojson"
        
        if not geojson_file.exists():
            print("⚠ Boundaries GeoJSON not found")
            return {}
        
        try:
            with open(geojson_file, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            
            boundaries = {}
            for feature in geojson_data.get('features', []):
                props = feature.get('properties', {})
                geometry = feature.get('geometry')
                
                # Use NAME_STATI property to create neighborhood ID
                name = props.get('NAME_STATI', 'Unknown')
                neighborhood_id = name.lower().replace(' ', '-').replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')
                
                if neighborhood_id and geometry:
                    boundaries[neighborhood_id] = geometry
            
            print(f"✓ Loaded {len(boundaries)} neighborhood boundaries from GeoJSON")
            return boundaries
        except Exception as e:
            print(f"✗ Error loading boundaries: {e}")
            return {}
    
    def _get_default_neighborhoods(self) -> List[Dict]:
        """Fallback neighborhoods if fetch fails"""
        return [
            {"id": "kreuzviertel", "name": "Kreuzviertel", "latitude": 51.9607, "longitude": 7.6261},
            {"id": "sentrup", "name": "Sentrup", "latitude": 51.9618, "longitude": 7.5937},
            {"id": "gievenbeck", "name": "Gievenbeck", "latitude": 51.9724, "longitude": 7.5708},
            {"id": "handorf", "name": "Handorf", "latitude": 51.9889, "longitude": 7.7147},
            {"id": "mecklenbeck", "name": "Mecklenbeck", "latitude": 51.9306, "longitude": 7.5816},
            {"id": "sprakel", "name": "Sprakel", "latitude": 52.0373, "longitude": 7.6172},
            {"id": "albachten", "name": "Albachten", "latitude": 51.9219, "longitude": 7.5273},
            {"id": "berg_fidel", "name": "Berg Fidel", "latitude": 51.9249, "longitude": 7.6222},
            {"id": "nienberge", "name": "Nienberge", "latitude": 52.0284, "longitude": 7.5595},
            {"id": "roxel", "name": "Roxel", "latitude": 51.9549, "longitude": 7.5332},
            {"id": "wolbeck", "name": "Wolbeck", "latitude": 51.9206, "longitude": 7.7272},
            {"id": "coerde", "name": "Coerde", "latitude": 51.9942, "longitude": 7.6119},
            {"id": "hiltrup", "name": "Hiltrup", "latitude": 51.9026, "longitude": 7.6428},
            {"id": "altstadt", "name": "Altstadt", "latitude": 51.9625, "longitude": 7.6256},
            {"id": "amelsbüren", "name": "Amelsbüren", "latitude": 51.8834, "longitude": 7.6059},
            {"id": "gremmendorf", "name": "Gremmendorf", "latitude": 51.9266, "longitude": 7.6707},
            {"id": "angelmodde", "name": "Angelmodde", "latitude": 51.9400, "longitude": 7.7000},
            {"id": "mitte_süd", "name": "Mitte-Süd", "latitude": 51.9550, "longitude": 7.6200},
            {"id": "mitte_nord", "name": "Mitte-Nord", "latitude": 51.9650, "longitude": 7.6200},
            {"id": "mauritz", "name": "Mauritz", "latitude": 51.9551, "longitude": 7.6428},
        ]
    
    def calculate_air_quality(self, district_geom: Polygon) -> Dict:
        """
        Calculate air quality from local sensors within district.
        Returns dict with score and raw values.
        """
        if not self.air_sensors or not district_geom:
            return {'score': None, 'pm10': None, 'pm25': None, 'estimated': True}

        values_pm10 = []
        values_pm25 = []
        
        for s in self.air_sensors:
            pt = Point(s['lon'], s['lat'])
            if district_geom.contains(pt):
                if s['P1']: values_pm10.append(s['P1'])
                if s['P2']: values_pm25.append(s['P2'])
        
        if not values_pm10 and not values_pm25:
             return {'score': None, 'pm10': None, 'pm25': None, 'estimated': True}

        avg_pm10 = sum(values_pm10)/len(values_pm10) if values_pm10 else None
        avg_pm25 = sum(values_pm25)/len(values_pm25) if values_pm25 else None
        
        # Use PM10 for scoring primarily (or max of both converted to an index)
        # Using simplified PM10 scale from geo_processor
        # < 20 = 5.0, < 35 = 4.0, < 50 = 3.0, < 75 = 2.0, > 75 = 1.0
        val_for_score = avg_pm10 if avg_pm10 is not None else (avg_pm25 * 2) # Crude conversion check?
        
        score = 3.0
        if val_for_score is not None:
            if val_for_score < 20: score = 5.0
            elif val_for_score < 35: score = 4.0
            elif val_for_score < 50: score = 3.0
            elif val_for_score < 75: score = 2.0
            else: score = 1.0
            
        return {
            'score': score,
            'pm10': round(avg_pm10, 1) if avg_pm10 else None, 
            'pm25': round(avg_pm25, 1) if avg_pm25 else None,
            'estimated': False,
            'sensor_count': len(values_pm10) + len(values_pm25)
        }
    
    def _get_regional_air_estimate(self, lat: float, lon: float) -> Dict:
        """Get regional air quality estimate based on location"""
        # Münster city center
        center_lat, center_lon = 51.9607, 7.6261
        distance = ((lat - center_lat) ** 2 + (lon - center_lon) ** 2) ** 0.5
        distance_km = distance * 111
        
        # Germany typical values
        if distance_km < 2:
            pm25 = 13.5
            location_type = "urban center"
        elif distance_km < 5:
            pm25 = 11.0
            location_type = "suburban"
        else:
            pm25 = 8.5
            location_type = "rural"
        
        print(f"    ℹ Using {location_type} estimate: PM2.5 {pm25:.1f} µg/m³")
        
        return {
            'pm25': pm25,
            'pm10': pm25 * 1.5,
            'no2': pm25 * 2,
            'estimated': True,
            'location_type': location_type
        }
    
    def _safe_average(self, values: List[float]) -> Optional[float]:
        """Calculate average of values"""
        valid_values = [v for v in values if v is not None and v > 0]
        if not valid_values:
            return None
        return round(sum(valid_values) / len(valid_values), 1)
    
    def pm25_to_score(self, pm25_value: Optional[float]) -> float:
        """
        Convert PM2.5 µg/m³ to score (1-5).
        
        Based on WHO Air Quality Guidelines:
        - Excellent: 0-5 µg/m³ → 5.0
        - Good: 5-10 µg/m³ → 4.5
        - Moderate: 10-15 µg/m³ → 4.0
        - Fair: 15-25 µg/m³ → 3.0
        - Poor: 25-35 µg/m³ → 2.0
        - Very Poor: >35 µg/m³ → 1.0
        """
        if pm25_value is None:
            return 3.5
        
        if pm25_value <= 5:
            return 5.0
        elif pm25_value <= 10:
            return 4.5
        elif pm25_value <= 15:
            return 4.0
        elif pm25_value <= 25:
            return 3.0
        elif pm25_value <= 35:
            return 2.0
        else:
            return 1.0
    
    def estimate_noise_level(self, lat: float, lon: float, neighborhood_id: str) -> Dict:
        """
        Estimate noise level using OSM road data.
        
        Args:
            lat: Latitude
            lon: Longitude
            neighborhood_id: Neighborhood identifier
        
        Returns:
            Dictionary with noise score and details
        """
        print(f"  🔊 Estimating noise level...")
        
        try:
            # Query Overpass for nearby roads
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json][timeout:25];
            (
              way["highway"](around:1500,{lat},{lon});
            );
            out body;
            """
            
            response = requests.post(overpass_url, data={'data': overpass_query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Count road types
            road_counts = {
                'motorway': 0,
                'trunk': 0,
                'primary': 0,
                'secondary': 0,
                'residential': 0
            }
            
            for element in data.get('elements', []):
                if element.get('type') == 'way' and 'tags' in element:
                    highway = element['tags'].get('highway', '')
                    
                    if 'motorway' in highway:
                        road_counts['motorway'] += 1
                    elif 'trunk' in highway:
                        road_counts['trunk'] += 1
                    elif 'primary' in highway:
                        road_counts['primary'] += 1
                    elif 'secondary' in highway:
                        road_counts['secondary'] += 1
                    elif 'residential' in highway:
                        road_counts['residential'] += 1
            
            # Calculate noise impact
            noise_impact = (
                road_counts['motorway'] * 10 +
                road_counts['trunk'] * 7 +
                road_counts['primary'] * 5 +
                road_counts['secondary'] * 3 +
                road_counts['residential'] * 0.5
            )
            
            # Convert to score (1-5, higher is quieter)
            if noise_impact == 0:
                noise_score = 5.0
            elif noise_impact < 10:
                noise_score = 4.5
            elif noise_impact < 20:
                noise_score = 4.0
            elif noise_impact < 40:
                noise_score = 3.5
            elif noise_impact < 60:
                noise_score = 3.0
            elif noise_impact < 80:
                noise_score = 2.5
            else:
                noise_score = 2.0
            
            estimated_db = 40 + (5 - noise_score) * 10
            
            print(f"    ✓ Noise score: {noise_score}/5 (est. {estimated_db:.0f} dB)")
            print(f"    ℹ Roads found: {sum(road_counts.values())} (Major: {road_counts['motorway'] + road_counts['trunk'] + road_counts['primary']})")
            
            return {
                'score': noise_score,
                'estimated_db': estimated_db,
                'road_counts': road_counts,
                'method': 'OSM road analysis'
            }
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
            # Fallback to distance-based estimate
            return self._get_distance_based_noise(lat, lon)
    
    def _get_distance_based_noise(self, lat: float, lon: float) -> Dict:
        """Fallback noise estimation based on distance from center"""
        center_lat, center_lon = 51.9607, 7.6261
        distance = ((lat - center_lat) ** 2 + (lon - center_lon) ** 2) ** 0.5
        distance_km = distance * 111
        
        if distance_km < 1:
            noise_score = 2.5
        elif distance_km < 3:
            noise_score = 3.0
        elif distance_km < 5:
            noise_score = 3.5
        else:
            noise_score = 4.0
        
        estimated_db = 40 + (5 - noise_score) * 10
        
        print(f"    ℹ Using distance-based estimate: {noise_score}/5")
        
        return {
            'score': noise_score,
            'estimated_db': estimated_db,
            'method': 'distance-based estimation'
        }
    
    
    def calculate_green_score(self, district_geom: Polygon) -> float:
        """Calculate percentage of district area covered by green spaces."""
        if not self.green_shapes or not district_geom:
            return 0.0
        
        district_area = district_geom.area
        if district_area == 0:
            return 0.0
            
        # Optimize: simple overlap check first
        intersecting_green_area = 0.0
        for green in self.green_shapes:
            if district_geom.intersects(green):
                try:
                    intersection = district_geom.intersection(green)
                    intersecting_green_area += intersection.area
                except: pass
        
        # Cap at 1.0 (100%)
        return min(1.0, intersecting_green_area / district_area)

    def calculate_tree_density(self, district_geom: Polygon) -> int:
        """Calculate number of trees in district."""
        if not self.tree_points or not district_geom:
            return 0
        
        count = 0
        for tree in self.tree_points:
            if district_geom.contains(tree):
                count += 1
        return count

    def calculate_heat_score(self, green_score_val: float) -> float:
        """
        Calculate Heat Island score (1-5) based on heuristics.
        Logic: High Green Score = Low Heat Island Effect.
        Heat Score = 5 (High Heat) - (Green Score * 4) -> Scaled to 1-5.
        """
        # Linear mapping: 0.0 Green -> 5.0 Heat, 1.0 Green -> 1.0 Heat
        score = 5.0 - (green_score_val * 4.0)
        return round(max(1.0, min(5.0, score)), 1)


    
    def save_data(self, data: List[Dict]):
        """
        Save collected data to JSON files.
        
        Args:
            data: List of neighborhood data
        """
        # Save raw data with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_file = self.raw_path / f"neighborhoods_{timestamp}.json"
        
        with open(raw_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Raw data saved to: {raw_file}")
        
        # Save processed data (used by API)
        processed_file = self.processed_path / "neighborhoods.json"
        
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Processed data saved to: {processed_file}")



def main():
    """Main execution function"""
    collector = MunsterDataCollector()
    
    if not collector.neighborhoods:
        print("\n✗ No neighborhoods loaded. Exiting.")
        return
    
    # Collect data
    data = collector.collect_all_data()
    
    # Save to files
    collector.save_data(data)
    
    print("="*70)
    print("✓ DATA COLLECTION COMPLETE")
    print("="*70)
    print(f"\n📁 Total neighborhoods: {len(data)}")
    print(f"📊 Data ready for API use")
    print(f"🗺️  Boundaries included: {sum(1 for d in data if d.get('geojson'))}/{len(data)}")
    print("\n📝 Next steps:")
    print("  1. Restart your backend: uvicorn app.main:app --reload")
    print("  2. Check frontend: http://localhost:5173")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()