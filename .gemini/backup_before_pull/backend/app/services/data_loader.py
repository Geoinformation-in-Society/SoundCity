"""
Data loader service for reading neighborhood data
"""
import json
from pathlib import Path
from typing import List, Optional, Dict
from app.services.geo_processor import process_neighborhoods

# In-memory cache
_NEIGHBORHOODS_CACHE: List[Dict] = []

def load_neighborhoods_data() -> List[dict]:
    """
    Load neighborhoods data from processed GeoJSONs.
    Uses in-memory cache to avoid re-processing on every request.
    
    Returns:
        List of neighborhood dictionaries
    """
    global _NEIGHBORHOODS_CACHE
    
    if _NEIGHBORHOODS_CACHE:
        return _NEIGHBORHOODS_CACHE
        
    try:
        print("Processing neighborhood data from raw sources...")
        data = process_neighborhoods()
        
        if not data:
            print("Warning: No data processed. Falling back to sample data.")
            return get_sample_data()
            
        _NEIGHBORHOODS_CACHE = data
        return data
        
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