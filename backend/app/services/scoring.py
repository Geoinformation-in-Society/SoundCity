"""
Scoring service for calculating livability scores
"""

def calculate_livability_score(
    air_quality: float,
    noise_level: float,
    air_weight: float = 0.5,
    noise_weight: float = 0.5
) -> float:
    """
    Calculate livability score based on weighted factors.
    
    Args:
        air_quality: Air quality score (1-5, higher is better)
        noise_level: Noise level score (1-5, higher is quieter/better)
        air_weight: Weight for air quality (0-1)
        noise_weight: Weight for noise level (0-1)
    
    Returns:
        Livability score (0-10)
    
    Example:
        >>> calculate_livability_score(4.0, 3.0, 0.5, 0.5)
        7.0
    """
    # Normalize weights to ensure they sum to 1
    total_weight = air_weight + noise_weight
    if total_weight == 0:
        air_weight = noise_weight = 0.5
    else:
        air_weight = air_weight / total_weight
        noise_weight = noise_weight / total_weight
    
    # Calculate weighted score (convert 5-point scale to 10-point)
    score = (air_quality * air_weight + noise_level * noise_weight) * 2
    
    return round(score, 1)

def generate_insights(
    name: str,
    air_quality: float,
    noise_level: float,
    livability_score: float
) -> str:
    """
    Generate human-readable insights based on scores.
    
    Args:
        name: Neighborhood name
        air_quality: Air quality score (1-5)
        noise_level: Noise level score (1-5)
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

def get_score_color(score: float) -> str:
    """
    Get color code for score visualization.
    
    Args:
        score: Livability score (0-10)
    
    Returns:
        Hex color code
    """
    if score >= 8.0:
        return "#4ade80"  # Green
    elif score >= 6.0:
        return "#fbbf24"  # Yellow
    else:
        return "#f87171"  # Red