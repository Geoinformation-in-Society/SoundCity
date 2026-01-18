from pydantic import BaseModel, Field
from typing import Optional, Dict

class NeighborhoodBase(BaseModel):
    """Base neighborhood model"""
    name: str = Field(..., description="Neighborhood name")
    air_quality: float = Field(..., ge=1.0, le=5.0, description="Air quality score (1-5)")
    noise_level: float = Field(..., ge=1.0, le=5.0, description="Noise level score (1-5, higher is quieter)")
    green_score: Optional[float] = Field(None, ge=0.0, le=5.0, description="Green space score (0-5)")
    tree_cnt: Optional[int] = Field(None, description="Number of trees")
    heat_score: Optional[float] = Field(None, ge=1.0, le=5.0, description="Heat stress score (1-5, higher is hotter)")

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
                "livability_score": 6.0,
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
    air_weight: float = Field(0.5, ge=0.0, le=1.0, description="Weight for air quality (0-1)")
    noise_weight: float = Field(0.5, ge=0.0, le=1.0, description="Weight for noise level (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "air_weight": 0.6,
                "noise_weight": 0.4
            }
        }