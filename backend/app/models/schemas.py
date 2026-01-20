from pydantic import BaseModel, Field
from typing import Optional, Dict

class NeighborhoodBase(BaseModel):
    """Base neighborhood model"""
    name: str = Field(..., description="Neighborhood name")
    air_quality: float = Field(..., ge=1.0, le=5.0, description="Air quality score (1-5)")
    noise_level: float = Field(..., ge=1.0, le=5.0, description="Noise level score (1-5, higher is quieter)")
    green_space: float = Field(..., ge=1.0, le=5.0, description="Green environment score (1-5)")
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
                "green_space": 3.7,
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
    air_weight: float = Field(0.25, ge=0.0, le=1.0, description="Weight for air quality (0-1)")
    noise_weight: float = Field(0.25, ge=0.0, le=1.0, description="Weight for noise level (0-1)")
    green_space_weight: float = Field(0.25, ge=0.0, le=1.0, description="Weight for green environment (0-1)")
    urban_heat_weight: float = Field(0.25, ge=0.0, le=1.0, description="Weight for urban heat island effect (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "air_weight": 0.25,
                "noise_weight": 0.25,
                "green_space_weight": 0.25,
                "urban_heat_weight": 0.25
            }
        }


class FeedbackSubmission(BaseModel):
    """User feedback submission"""
    satisfaction: int = Field(..., ge=1, le=5, description="Satisfaction rating (1-5)")
    useful_feature: str = Field(..., description="Most useful feature")
    most_important_indicator: str = Field(..., description="Most important indicator (air/noise/green/heat)")
    housing_decision: str = Field(..., description="Would use for housing decisions (definitely/maybe/no)")
    improvement: Optional[str] = Field(None, description="Suggested improvements")
    would_recommend: bool = Field(..., description="Would recommend to others")
    session_data: Optional[Dict] = Field(None, description="Session metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "satisfaction": 5,
                "useful_feature": "comparison",
                "most_important_indicator": "air",
                "housing_decision": "definitely",
                "improvement": "Add more neighborhoods",
                "would_recommend": True,
                "session_data": {"page": "comparison", "duration": 120}
            }
        }


class FeedbackResponse(BaseModel):
    """Feedback submission response"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    feedback_id: int = Field(..., description="Unique feedback identifier")


class FeedbackStats(BaseModel):
    """Feedback statistics"""
    total_responses: int = Field(..., description="Total number of responses")
    average_satisfaction: float = Field(..., description="Average satisfaction score")
    recommendation_rate: float = Field(..., description="Percentage of users who would recommend")
    most_useful_feature: Optional[str] = Field(None, description="Most popular feature")
    feature_breakdown: Dict[str, int] = Field(..., description="Feature popularity breakdown")