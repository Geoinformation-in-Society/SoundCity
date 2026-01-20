"""
API endpoints for neighborhood data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.schemas import Neighborhood, NeighborhoodDetail, ScoreWeights
from app.services.data_loader import load_neighborhoods_data, find_neighborhood_by_id
from app.services.scoring import calculate_livability_score, generate_insights

router = APIRouter(prefix="/api/v1/neighborhoods", tags=["neighborhoods"])

@router.get("/", response_model=List[Neighborhood])
def get_neighborhoods(
    air_weight: float = Query(0.25, ge=0.0, le=1.0, description="Weight for air quality"),
    noise_weight: float = Query(0.25, ge=0.0, le=1.0, description="Weight for noise level"),
    green_space_weight: float = Query(0.25, ge=0.0, le=1.0, description="Weight for green environment"),
    urban_heat_weight: float = Query(0.25, ge=0.0, le=1.0, description="Weight for urban heat island effect")
):
    """
    Get all neighborhoods with calculated livability scores.
    
    Query Parameters:
        - air_weight: Weight for air quality (0-1, default: 0.25)
        - noise_weight: Weight for noise level (0-1, default: 0.25)
        - green_space_weight: Weight for green environment (0-1, default: 0.25)
        - urban_heat_weight: Weight for urban heat island effect (0-1, default: 0.25)
    
    Returns:
        List of neighborhoods with livability scores
    """

    neighborhoods_data = load_neighborhoods_data()
    neighborhoods = []

    for data in neighborhoods_data:
        score = calculate_livability_score(
            data["air_quality"],
            data["noise_level"],
            data["green_space"],
            data["urban_heat"],
            air_weight,
            noise_weight,
            green_space_weight,
            urban_heat_weight
        )

        neighborhood = Neighborhood(
            id=data["id"],
            name=data["name"],
            air_quality=data["air_quality"],
            noise_level=data["noise_level"],
            green_space=data["green_space"],
            urban_heat=data["urban_heat"],
            livability_score=score,
            latitude=data["latitude"],
            longitude=data["longitude"],
            geojson=data.get("geojson")
        )

        neighborhoods.append(neighborhood)
    
    # Sort by livability score (descending)
    neighborhoods.sort(key=lambda x: x.livability_score, reverse=True)

    return neighborhoods

@router.get("/{neighborhood_id}", response_model=NeighborhoodDetail)
def get_neighborhood_detail(
    neighborhood_id: str,
    air_weight: float = Query(0.25, ge=0.0, le=1.0),
    noise_weight: float = Query(0.25, ge=0.0, le=1.0),
    green_space_weight: float = Query(0.25, ge=0.0, le=1.0),
    urban_heat_weight: float = Query(0.25, ge=0.0, le=1.0)
):
    """
    Get detailed information for a specific neighborhood.
    
    Path Parameters:
        - neighborhood_id: Unique neighborhood identifier
    
    Query Parameters:
        - air_weight: Weight for air quality (0-1, default: 0.25)
        - noise_weight: Weight for noise level (0-1, default: 0.25)
        - green_space_weight: Weight for green environment (0-1, default: 0.25)
        - urban_heat_weight: Weight for urban heat island effect (0-1, default: 0.25)
    
    Returns:
        Detailed neighborhood information with insights
    """
    data = find_neighborhood_by_id(neighborhood_id)
    
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Neighborhood '{neighborhood_id}' not found"
        )
    
    score = calculate_livability_score(
        data["air_quality"],
        data["noise_level"],
        data["green_space"],
        data["urban_heat"],
        air_weight,
        noise_weight,
        green_space_weight,
        urban_heat_weight
    )
    
    insights = generate_insights(
        data["name"],
        data["air_quality"],
        data["noise_level"],
        data["green_space"],
        data["urban_heat"],
        score
    )
    
    return NeighborhoodDetail(
        id=data["id"],
        name=data["name"],
        air_quality=data["air_quality"],
        noise_level=data["noise_level"],
        green_space=data["green_space"],
        urban_heat=data["urban_heat"],
        livability_score=score,
        latitude=data["latitude"],
        longitude=data["longitude"],
        insights=insights,
        metadata=data.get("metadata")
    )

@router.get("/{neighborhood_id}/compare/{other_id}")
def compare_neighborhoods(
    neighborhood_id: str,
    other_id: str,
    air_weight: float = Query(0.25, ge=0.0, le=1.0),
    noise_weight: float = Query(0.25, ge=0.0, le=1.0),
    green_space_weight: float = Query(0.25, ge=0.0, le=1.0),
    urban_heat_weight: float = Query(0.25, ge=0.0, le=1.0)
):
    """
    Compare two neighborhoods side by side.
    
    Path Parameters:
        - neighborhood_id: First neighborhood ID
        - other_id: Second neighborhood ID
    
    Returns:
        Comparison data for both neighborhoods
    """
    n1_data = find_neighborhood_by_id(neighborhood_id)
    n2_data = find_neighborhood_by_id(other_id)
    
    if not n1_data:
        raise HTTPException(status_code=404, detail=f"Neighborhood '{neighborhood_id}' not found")
    if not n2_data:
        raise HTTPException(status_code=404, detail=f"Neighborhood '{other_id}' not found")
    
    n1_score = calculate_livability_score(
        n1_data["air_quality"],
        n1_data["noise_level"], 
        n1_data["green_space"], 
        n1_data["urban_heat"], 
        air_weight, 
        noise_weight, 
        green_space_weight,
        urban_heat_weight
    )

    n2_score = calculate_livability_score(
        n2_data["air_quality"], 
        n2_data["noise_level"], 
        n2_data["green_space"], 
        n2_data["urban_heat"], 
        air_weight, 
        noise_weight, 
        green_space_weight,
        urban_heat_weight
    )
    
    return {
        "neighborhood1": {
            "id": n1_data["id"],
            "name": n1_data["name"],
            "air_quality": n1_data["air_quality"],
            "noise_level": n1_data["noise_level"],
            "green_space": n1_data["green_space"],
            "urban_heat": n1_data["urban_heat"],
            "livability_score": n1_score
        },
        "neighborhood2": {
            "id": n2_data["id"],
            "name": n2_data["name"],
            "air_quality": n2_data["air_quality"],
            "noise_level": n2_data["noise_level"],
            "green_space": n2_data["green_space"],
            "urban_heat": n2_data["urban_heat"],
            "livability_score": n2_score
        },

        "winner": n1_data["name"] if n1_score > n2_score else n2_data["name"] if n2_score > n1_score else "Tie"
    }