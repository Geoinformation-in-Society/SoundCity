"""
Scoring service for calculating livability scores
"""

def calculate_livability_score(
    air_quality: float,
    noise_level: float,
    green_space: float,
    urban_heat: float,
    air_weight: float = 0.25,
    noise_weight: float = 0.25,
    green_space_weight: float = 0.25,
    urban_heat_weight: float = 0.25
) -> float:
    """
    Calculate livability score based on weighted factors.
    
    Args:
        air_quality: Air quality score (1-5, higher is better)
        noise_level: Noise level score (1-5, higher is quieter/better)
        green_space: Green environment score (1-5, higher is better)
        urban_heat: Urban heat island effect score (1-5, higher is better)
        air_weight: Weight for air quality (0-1)
        noise_weight: Weight for noise level (0-1)
        green_space_weight: Weight for green environment (0-1)
        urban_heat_weight: Weight for urban heat island effect (0-1)
    
    Returns:
        Livability score (0-10)
    
    Example:
        >>> calculate_livability_score(4.0, 3.0, 3.5, 3.0)
        6.8
    """
    # Normalize weights to ensure they sum to 1
    total_weight = air_weight + noise_weight + green_space_weight + urban_heat_weight

    if total_weight == 0:
        air_weight = noise_weight = green_space_weight = urban_heat_weight = 0.25
    else:
        air_weight = air_weight / total_weight
        noise_weight = noise_weight / total_weight
        green_space_weight = green_space_weight / total_weight
        urban_heat_weight = urban_heat_weight / total_weight
    
    # Calculate weighted score (convert 5-point scale to 10-point)
    score = (
        air_quality * air_weight + 
        noise_level * noise_weight + 
        green_space * green_space_weight + 
        urban_heat * urban_heat_weight
        ) * 2
    
    return round(score, 1)

def generate_insights(
    name: str,
    air_quality: float,
    noise_level: float,
    green_space: float,
    urban_heat: float,
    livability_score: float
) -> str:
    """
    Generate human-readable insights based on scores.
    
    Args:
        name: Neighborhood name
        air_quality: Air quality score (1-5)
        noise_level: Noise level score (1-5)
        green_space: Green environment score (1-5)
        urban_heat: Urban heat island effect score (1-5)
        livability_score: Overall score (0-10)
    
    Returns:
        Insight text describing the neighborhood
    """
    # Air quality description
    if air_quality >= 4.0:
        air_desc = "excellent air quality with minimal pollution"
    elif air_quality >= 3.0:
        air_desc = "moderate air quality, typical for urban areas"
    else:
        air_desc = "fair air quality, with noticeable pollution levels"
    
    # Noise level description
    if noise_level >= 4.0:
        noise_desc = "very quiet environment with minimal traffic noise"
    elif noise_level >= 3.0:
        noise_desc = "moderate noise levels during peak hours"
    else:
        noise_desc = "higher noise levels due to proximity to major roads"
    
    # Overall assessment
    if livability_score >= 8.0:
        overall = f"{name} is an excellent choice for residents seeking a high quality of life."
    elif livability_score >= 6.5:
        overall = f"{name} offers a good balance of urban amenities and livability."
    else:
        overall = f"{name} has some environmental challenges but may suit those prioritizing other factors."
    
    # Combine insights
    insight = f"{name} features {air_desc}. The area experiences {noise_desc}. {overall}"
    
    return insight