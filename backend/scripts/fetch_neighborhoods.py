"""
Fetch real Münster neighborhoods with boundaries from OpenStreetMap
"""
import requests
import json
from pathlib import Path
from typing import List, Dict


def fetch_muenster_neighborhoods():
    """
    Fetch all neighborhoods (admin_level=10) in Münster with their boundaries.
    
    Returns:
        List of neighborhoods with GeoJSON geometries
    """
    print("\n" + "="*70)
    print("🗺️  FETCHING MÜNSTER NEIGHBORHOODS FROM OPENSTREETMAP")
    print("="*70 + "\n")
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Your Overpass query
    overpass_query = """
    [out:json][timeout:60];
    area["name"="Münster"]["admin_level"="6"]->.a;
    (
      relation["boundary"="administrative"]["admin_level"="10"](area.a);
    );
    out geom;
    """
    
    print("📡 Querying Overpass API...")
    print("   (This may take 30-60 seconds)")
    
    try:
        response = requests.post(
            overpass_url, 
            data={'data': overpass_query}, 
            timeout=90
        )
        response.raise_for_status()
        data = response.json()
        
        elements = data.get('elements', [])
        print(f"\n✓ Found {len(elements)} neighborhoods\n")
        
        neighborhoods = []
        
        for element in elements:
            if element.get('type') == 'relation':
                tags = element.get('tags', {})
                name = tags.get('name', 'Unknown')
                
                # Skip if no name
                if name == 'Unknown' or not name:
                    continue
                
                print(f"  Processing: {name}")
                
                # Extract geometry
                members = element.get('members', [])
                geometry = convert_osm_to_geojson(members, element)
                
                if geometry:
                    # Calculate center point (centroid)
                    center = calculate_centroid(geometry)
                    
                    # Create neighborhood ID (lowercase, replace spaces with dashes)
                    neighborhood_id = name.lower().replace(' ', '-').replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')
                    
                    neighborhood = {
                        'id': neighborhood_id,
                        'name': name,
                        'osm_id': element.get('id'),
                        'latitude': center['lat'],
                        'longitude': center['lon'],
                        'geometry': geometry,
                        'tags': tags
                    }
                    
                    neighborhoods.append(neighborhood)
                    print(f"    ✓ Center: ({center['lat']:.4f}, {center['lon']:.4f})")
        
        print(f"\n✓ Successfully processed {len(neighborhoods)} neighborhoods")
        return neighborhoods
        
    except requests.exceptions.Timeout:
        print("✗ Request timeout - Overpass API is slow")
        print("  Try again in a few minutes")
        return []
    except Exception as e:
        print(f"✗ Error: {e}")
        return []


def convert_osm_to_geojson(members: List[Dict], element: Dict) -> Dict:
    """
    Convert OSM relation members to GeoJSON geometry.
    
    Args:
        members: List of relation members
        element: OSM element
        
    Returns:
        GeoJSON geometry dictionary
    """
    # Find outer ways
    outer_ways = [m for m in members if m.get('role') == 'outer' and m.get('type') == 'way']
    
    if not outer_ways:
        return None
    
    # Collect all coordinates from outer ways
    all_coordinates = []
    
    for way in outer_ways:
        way_coords = []
        geometry = way.get('geometry', [])
        
        for node in geometry:
            lon = node.get('lon')
            lat = node.get('lat')
            if lon is not None and lat is not None:
                way_coords.append([lon, lat])
        
        if way_coords:
            all_coordinates.extend(way_coords)
    
    if not all_coordinates:
        return None
    
    # Close the polygon if not already closed
    if all_coordinates[0] != all_coordinates[-1]:
        all_coordinates.append(all_coordinates[0])
    
    # Return as GeoJSON Polygon
    return {
        "type": "Polygon",
        "coordinates": [all_coordinates]
    }


def calculate_centroid(geometry: Dict) -> Dict:
    """
    Calculate the centroid (center point) of a polygon.
    
    Args:
        geometry: GeoJSON geometry
        
    Returns:
        Dictionary with lat and lon
    """
    if geometry['type'] != 'Polygon':
        return {'lat': 0, 'lon': 0}
    
    coordinates = geometry['coordinates'][0]
    
    # Simple average of all points
    total_lat = sum(coord[1] for coord in coordinates)
    total_lon = sum(coord[0] for coord in coordinates)
    count = len(coordinates)
    
    return {
        'lat': round(total_lat / count, 4),
        'lon': round(total_lon / count, 4)
    }


def save_neighborhoods(neighborhoods: List[Dict]):
    """
    Save neighborhoods data to files.
    
    Args:
        neighborhoods: List of neighborhood dictionaries
    """
    base_path = Path(__file__).parent.parent / "app" / "data"
    
    # Save complete data (with geometries)
    geojson_path = base_path / "geojson"
    geojson_path.mkdir(parents=True, exist_ok=True)
    
    # Create GeoJSON FeatureCollection
    geojson_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": n['id'],
                "properties": {
                    "id": n['id'],
                    "name": n['name'],
                    "osm_id": n['osm_id'],
                    "center_lat": n['latitude'],
                    "center_lon": n['longitude']
                },
                "geometry": n['geometry']
            }
            for n in neighborhoods
        ]
    }
    
    geojson_file = geojson_path / "neighborhoods_boundaries.geojson"
    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_collection, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ GeoJSON saved to: {geojson_file}")
    
    # Save simple list (without geometries) for reference
    simple_list = [
        {
            'id': n['id'],
            'name': n['name'],
            'latitude': n['latitude'],
            'longitude': n['longitude'],
            'osm_id': n['osm_id']
        }
        for n in neighborhoods
    ]
    
    list_file = geojson_path / "neighborhoods_list.json"
    with open(list_file, 'w', encoding='utf-8') as f:
        json.dump(simple_list, f, indent=2, ensure_ascii=False)
    
    print(f"✓ List saved to: {list_file}")


def main():
    """Main execution"""
    neighborhoods = fetch_muenster_neighborhoods()
    
    if not neighborhoods:
        print("\n✗ No neighborhoods fetched")
        return
    
    save_neighborhoods(neighborhoods)
    
    print("\n" + "="*70)
    print("✓ FETCH COMPLETE")
    print("="*70)
    print(f"\nTotal neighborhoods: {len(neighborhoods)}")
    print("\nSample neighborhoods:")
    for n in neighborhoods[:5]:
        print(f"  - {n['name']} ({n['id']})")
    
    if len(neighborhoods) > 5:
        print(f"  ... and {len(neighborhoods) - 5} more")
    
    print("\n📝 Next steps:")
    print("  1. Review the neighborhoods_list.json file")
    print("  2. Run the updated collect_data.py script")
    print("  3. Restart your backend server")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()