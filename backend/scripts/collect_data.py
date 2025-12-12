"""
Data collection script for Sound City
Collects air quality and noise data for Münster neighborhoods
Now uses real neighborhoods from OpenStreetMap
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


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
        
        # Load neighborhoods from the fetched data
        self.neighborhoods = self.load_neighborhoods()
        self.boundaries = self.load_boundaries()
    
    def load_neighborhoods(self) -> List[Dict]:
        """
        Load neighborhoods from the list file created by fetch_neighborhoods.py
        
        Returns:
            List of neighborhoods
        """
        list_file = self.geojson_path / "neighborhoods_list.json"
        
        if not list_file.exists():
            print("⚠ Neighborhoods list not found!")
            print("  Please run: python scripts/fetch_neighborhoods.py first")
            print("\n  Using default neighborhoods as fallback...")
            return self._get_default_neighborhoods()
        
        try:
            with open(list_file, 'r', encoding='utf-8') as f:
                neighborhoods = json.load(f)
            print(f"✓ Loaded {len(neighborhoods)} neighborhoods from OpenStreetMap data")
            return neighborhoods
        except Exception as e:
            print(f"✗ Error loading neighborhoods: {e}")
            return self._get_default_neighborhoods()
    
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
                neighborhood_id = feature.get('id') or feature.get('properties', {}).get('id')
                if neighborhood_id:
                    boundaries[neighborhood_id] = feature['geometry']
            
            print(f"✓ Loaded {len(boundaries)} neighborhood boundaries")
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
    
    def collect_air_quality_openaq(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Collect air quality data from OpenAQ API V2.
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            Dictionary with PM2.5 and other pollutant values or None
        """
        try:
            # Use V2 API with measurements endpoint
            url = "https://api.openaq.org/v2/measurements"
            
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=7)
            
            params = {
                "coordinates": f"{lat},{lon}",
                "radius": 50000,  # 50km radius
                "date_from": start_date.isoformat(),
                "date_to": end_date.isoformat(),
                "limit": 1000,
                "parameter": ["pm25", "pm10", "no2"]
            }
            
            print(f"  📍 Fetching air quality for ({lat:.4f}, {lon:.4f})...")
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                print(f"    ⚠ No data found, using regional estimate")
                return self._get_regional_air_estimate(lat, lon)
            
            # Collect measurements
            pm25_values = []
            pm10_values = []
            no2_values = []
            
            for result in results:
                parameter = result.get('parameter')
                value = result.get('value')
                
                if value is not None and value > 0:
                    if parameter == 'pm25':
                        pm25_values.append(value)
                    elif parameter == 'pm10':
                        pm10_values.append(value)
                    elif parameter == 'no2':
                        no2_values.append(value)
            
            avg_pm25 = self._safe_average(pm25_values)
            avg_pm10 = self._safe_average(pm10_values)
            avg_no2 = self._safe_average(no2_values)
            
            if avg_pm25:
                print(f"    ✓ PM2.5: {avg_pm25:.1f} µg/m³ (from {len(pm25_values)} readings)")
            else:
                print(f"    ⚠ No PM2.5 data, using estimate")
                return self._get_regional_air_estimate(lat, lon)
            
            return {
                'pm25': avg_pm25,
                'pm10': avg_pm10,
                'no2': avg_no2,
                'measurements_count': len(results)
            }
            
        except Exception as e:
            print(f"    ✗ API Error: {e}")
            return self._get_regional_air_estimate(lat, lon)
    
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
    
    def collect_all_data(self) -> List[Dict]:
        """
        Collect data for all neighborhoods.
        
        Returns:
            List of neighborhood data dictionaries
        """
        print("\n" + "="*70)
        print("🌍 SOUND CITY - DATA COLLECTION")
        print("="*70 + "\n")
        print(f"Processing {len(self.neighborhoods)} neighborhoods...\n")
        
        results = []
        
        for i, neighborhood in enumerate(self.neighborhoods, 1):
            print(f"[{i}/{len(self.neighborhoods)}] {neighborhood['name']}")
            
            lat = neighborhood['latitude']
            lon = neighborhood['longitude']
            n_id = neighborhood['id']
            
            # Collect air quality
            print("\n💨 AIR QUALITY:")
            air_data = self.collect_air_quality_openaq(lat, lon)
            air_quality_score = self.pm25_to_score(air_data.get('pm25'))
            
            # Estimate noise
            print("\n🔊 NOISE POLLUTION:")
            noise_data = self.estimate_noise_level(lat, lon, n_id)
            
            # Get boundary geometry
            geometry = self.boundaries.get(n_id)
            
            # Compile result
            result = {
                "id": n_id,
                "name": neighborhood['name'],
                "latitude": lat,
                "longitude": lon,
                "air_quality": round(air_quality_score, 1),
                "noise_level": round(noise_data['score'], 1),
                "geojson": geometry,  # Include polygon geometry
                "metadata": {
                    "osm_id": neighborhood.get('osm_id'),
                    "pm25_raw": air_data.get('pm25'),
                    "pm10_raw": air_data.get('pm10'),
                    "no2_raw": air_data.get('no2'),
                    "estimated_db": noise_data.get('estimated_db'),
                    "data_sources": {
                        "air_quality": "OpenAQ API" if not air_data.get('estimated') else "Regional estimate",
                        "noise": noise_data.get('method', 'Estimated'),
                        "boundaries": "OpenStreetMap (Overpass API)"
                    },
                    "last_updated": datetime.now().isoformat()
                }
            }
            
            results.append(result)
            print(f"\n  ✓ Complete: Air={air_quality_score}/5, Noise={noise_data['score']}/5")
            print("  " + "-"*66 + "\n")
            
            # Rate limiting
            if i < len(self.neighborhoods):
                time.sleep(2)
        
        return results
    
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
    
    def print_summary(self, data: List[Dict]):
        """Print summary statistics"""
        print("\n" + "="*70)
        print("📊 COLLECTION SUMMARY")
        print("="*70)
        print(f"{'Neighborhood':<25} {'Air Quality':<15} {'Noise Level':<15}")
        print("-" * 70)
        
        for item in data:
            print(f"{item['name']:<25} {item['air_quality']:<15.1f} {item['noise_level']:<15.1f}")
        
        avg_air = sum(d['air_quality'] for d in data) / len(data)
        avg_noise = sum(d['noise_level'] for d in data) / len(data)
        
        print("-" * 70)
        print(f"{'AVERAGE':<25} {avg_air:<15.1f} {avg_noise:<15.1f}")
        print()


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
    
    # Print summary
    collector.print_summary(data)
    
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