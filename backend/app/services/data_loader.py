"""
Data loader service for reading neighborhood data
"""
import json
from pathlib import Path
from typing import Dict, List, Optional

# In-memory cache
_NEIGHBORHOODS_CACHE: List[Dict] = []

DATA_FILE = Path(__file__).parent.parent / "data" / "processed" / "neighborhoods.json"

def load_neighborhoods_data() -> List[dict]:
    """
    Load neighborhoods data from JSON file.
    
    Returns:
        List of neighborhood dictionaries
    """
    try:
        global _NEIGHBORHOODS_CACHE

        if _NEIGHBORHOODS_CACHE:
            return _NEIGHBORHOODS_CACHE

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _NEIGHBORHOODS_CACHE = data

        return data
    except FileNotFoundError:
        # Return sample data if file doesn't exist
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {DATA_FILE}")
        return []

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