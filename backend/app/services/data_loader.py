"""
Data loader service for reading neighborhood data
"""
import json
from pathlib import Path
from typing import List, Optional

DATA_FILE = Path(__file__).parent.parent / "data" / "processed" / "neighborhoods.json"

def load_neighborhoods_data() -> List[dict]:
    """
    Load neighborhoods data from JSON file.
    
    Returns:
        List of neighborhood dictionaries
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Return sample data if file doesn't exist
        return get_sample_data()
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {DATA_FILE}")
        return get_sample_data()

def get_sample_data() -> List[dict]:
    """
    Get sample neighborhood data for development/testing.
    
    Returns:
        List of sample neighborhoods
    """
    return [
        {
            "id": "kreuzviertel",
            "name": "Kreuzviertel",
            "air_quality": 4.0,
            "noise_level": 2.0,
            "latitude": 51.9607,
            "longitude": 7.6261,
            "metadata": {
                "population": 12500,
                "area_km2": 2.3,
                "description": "Historic district near the city center"
            }
        },
        {
            "id": "gievenbeck",
            "name": "Gievenbeck",
            "air_quality": 3.5,
            "noise_level": 4.0,
            "latitude": 51.9693,
            "longitude": 7.5651,
            "metadata": {
                "population": 18000,
                "area_km2": 8.7,
                "description": "Quiet suburban area with good green spaces"
            }
        },
        {
            "id": "altstadt",
            "name": "Altstadt",
            "air_quality": 3.0,
            "noise_level": 2.5,
            "latitude": 51.9625,
            "longitude": 7.6256,
            "metadata": {
                "population": 8500,
                "area_km2": 1.2,
                "description": "Historic old town with vibrant atmosphere"
            }
        },
        {
            "id": "mauritz",
            "name": "Mauritz",
            "air_quality": 4.0,
            "noise_level": 3.0,
            "latitude": 51.9551,
            "longitude": 7.6428,
            "metadata": {
                "population": 15000,
                "area_km2": 3.5,
                "description": "Mixed residential and commercial area"
            }
        },
        {
            "id": "handorf",
            "name": "Handorf",
            "air_quality": 4.5,
            "noise_level": 5.0,
            "latitude": 51.9889,
            "longitude": 7.7147,
            "metadata": {
                "population": 6500,
                "area_km2": 12.4,
                "description": "Rural area with excellent air quality"
            }
        }
    ]

def find_neighborhood_by_id(neighborhood_id: str) -> Optional[dict]:
    """
    Find a specific neighborhood by ID.
    
    Args:
        neighborhood_id: Unique neighborhood identifier
    
    Returns:
        Neighborhood dictionary or None if not found
    """
    neighborhoods = load_neighborhoods_data()
    return next((n for n in neighborhoods if n["id"] == neighborhood_id), None)