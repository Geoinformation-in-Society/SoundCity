"""
Data loader service for reading neighborhood data
"""
import json
from pathlib import Path
from typing import List, Optional, Dict


# In-memory cache
_NEIGHBORHOODS_CACHE: List[Dict] = []

# Constants
DATA_PATH = Path(__file__).parent.parent / "data" / "processed" / "neighborhoods.json"

def load_neighborhoods_data() -> List[dict]:
    """
    Load neighborhoods data from processed JSON file.
    Uses in-memory cache.
    """
    global _NEIGHBORHOODS_CACHE
    
    if _NEIGHBORHOODS_CACHE:
        return _NEIGHBORHOODS_CACHE
        
    try:
        if DATA_PATH.exists():
            print(f"Loading data from {DATA_PATH}...")
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                _NEIGHBORHOODS_CACHE = data
                print(f"✓ Loaded {len(data)} neighborhoods.")
                return data
        else:
            print(f"⚠ Data file not found at {DATA_PATH}")
            return get_sample_data()
            
    except Exception as e:
        print(f"Error loading neighborhoods: {e}")
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
            "name": "Kreuzviertel (Sample)",
            "air_quality": 60,
            "noise_level": 40,
            "green_score": 30,
            "latitude": 51.9607,
            "longitude": 7.6261,
            "metadata": {
                "description": "Sample data (Real data failed to load)"
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
    # Handle string vs int IDs
    return next((n for n in neighborhoods if str(n["id"]) == str(neighborhood_id)), None)