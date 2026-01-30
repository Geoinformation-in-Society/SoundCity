import os
import requests
import json
from pathlib import Path

# Data directory
DATA_DIR = Path("app/data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# URLs
URLS = {
    "districts": "https://opendata.stadt-muenster.de/sites/default/files/stadtteile-statistische-bezirke-muenster.geojson",
    "green_spaces": "https://www.stadt-muenster.de/ows/mapserv706/odgruenserv?REQUEST=GetFeature&SERVICE=WFS&VERSION=2.0.0&TYPENAME=ms:Gruenflaechen&OUTPUTFORMAT=GEOJSON&EXCEPTIONS=XML&MAXFEATURES=1000&SRSNAME=EPSG:4326",
    "noise_traffic_day": "https://opendata.stadt-muenster.de/sites/default/files/laerm_stra%C3%9Fe_tag.json",
    "trees": "https://www.stadt-muenster.de/ows/mapserv706/odgruenserv?REQUEST=GetFeature&SERVICE=WFS&VERSION=2.0.0&TYPENAME=ms:Baeume&OUTPUTFORMAT=GEOJSON&EXCEPTIONS=XML&MAXFEATURES=100000&SRSNAME=EPSG:4326",
    # Global air quality data (will need filtering)
    "air_quality_api": "https://data.sensor.community/static/v1/data.json"
}

def download_file(url: str, filename: str, force: bool = False) -> Path:
    """Download a file from a URL to the data directory."""
    filepath = DATA_DIR / filename
    
    if filepath.exists() and not force:
        print(f"File {filename} already exists. Skipping download.")
        return filepath
        
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Verify it's valid JSON if expected
        if filename.endswith(('.json', '.geojson')):
            try:
                content = response.json()
            except json.JSONDecodeError:
                print(f"Warning: {filename} is not valid JSON. Saving anyway.")
                content = response.content
            
            with open(filepath, "w", encoding="utf-8") as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f)
                else:
                    f.write(content.decode('utf-8'))
        else:
            with open(filepath, "wb") as f:
                f.write(response.content)
                
        print(f"Successfully saved {filename}")
        return filepath
        
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return None

def fetch_all_data(force: bool = False):
    """Fetch all required datasets."""
    print("Starting data fetch...")
    
    # 1. Districts
    download_file(URLS["districts"], "districts.geojson", force)
    
    # 2. Green Spaces
    # Note: WFS might need pagination if > 1000 features, but start with this.
    download_file(URLS["green_spaces"], "green_spaces.geojson", force)
    
    # 3. Noise
    download_file(URLS["noise_traffic_day"], "noise.geojson", force)
    
    # 4. Trees
    download_file(URLS["trees"], "trees.geojson", force)

    # 5. Air Quality
    # This is a large file, might perform better if we just get it fresh every X minutes
    # For now, let's treat it like static data for the MVP
    download_file(URLS["air_quality_api"], "air_sensors_global.json", force)
    
    print("Data fetch completed.")

if __name__ == "__main__":
    fetch_all_data()