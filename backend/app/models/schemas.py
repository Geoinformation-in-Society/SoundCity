from pydantic import BaseModel, Field
from typing import Optional, Dict

class NeighborhoodBase(BaseModel):
    """Base neighborhood model"""
    name: str = Field(..., description="Neighborhood name")
    air_quality: float = Field(..., ge=1.0, le=5.0, description="Air quality score (1-5)")
    noise_level: float = Field(..., ge=1.0, le=5.0, description="Noise level score (1-5, higher is quieter)")
    green_space: float = Field(..., ge=1.0, le=5.0, description="Green space availability score (1-5)")
    tree_greenness: float = Field(..., ge=1.0, le=5.0, description="Tree greenness score (1-5)")
    urban_heat: float = Field(..., ge=1.0, le=5.0, description="Urban heat island effect score (1-5)")

class Neighborhood(NeighborhoodBase):
    """Neighborhood model with computed fields"""
    id: str = Field(..., description="Unique neighborhood identifier")
    livability_score: float = Field(..., description="Overall livability score (0-10)")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    geojson: Optional[Dict] = Field(None, description="GeoJSON boundary data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "kreuzviertel",
                "name": "Kreuzviertel",
                "air_quality": 4.0,
                "noise_level": 2.0,
                "green_space": 3.5,
                "tree_greenness": 4.0,
                "urban_heat": 3.0,
                "livability_score": 7.2,
                "latitude": 51.9607,
                "longitude": 7.6261,
                "geojson": {
                    "type": "Polygon",
                    "coordinates": [[[7.6200, 51.9580], [7.6300, 51.9580], [7.6300, 51.9630], [7.6200, 51.9630], [7.6200, 51.9580]]]
                }
            }
        }

class NeighborhoodDetail(Neighborhood):
    """Detailed neighborhood information"""
    insights: str = Field(..., description="AI-generated insights about the neighborhood")
    metadata: Optional[Dict] = Field(None, description="Additional metadata")
    geojson: Optional[Dict] = Field(None, description="GeoJSON boundary data")

class ScoreWeights(BaseModel):
    """Weight configuration for score calculation"""
    air_weight: float = Field(0.2, ge=0.0, le=1.0, description="Weight for air quality (0-1)")
    noise_weight: float = Field(0.2, ge=0.0, le=1.0, description="Weight for noise level (0-1)")
    green_space_weight: float = Field(0.2, ge=0.0, le=1.0, description="Weight for green space availability (0-1)")
    tree_greenness_weight: float = Field(0.2, ge=0.0, le=1.0, description="Weight for tree greenness (0-1)")
    urban_heat_weight: float = Field(0.2, ge=0.0, le=1.0, description="Weight for urban heat island effect (0-1)")
    class Config:
        json_schema_extra = {
            "example": {
                "air_weight": 0.2,
                "noise_weight": 0.2,
                "green_space_weight": 0.2,
                "tree_greenness_weight": 0.2,
                "urban_heat_weight": 0.2
            }
        }