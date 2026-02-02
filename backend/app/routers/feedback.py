"""
Feedback router for collecting user feedback
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import FeedbackSubmission, FeedbackResponse, FeedbackStats
from app.services.feedback_service import feedback_service
import logging

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackSubmission):
    """
    Submit user feedback
    
    Stores feedback in a JSON file with timestamp and metadata
    """
    try:
        feedback_id = feedback_service.submit_feedback(
            useful_features=feedback.useful_features,
            most_important_indicators=feedback.most_important_indicators,
            housing_decision=feedback.housing_decision,
            data_clarity=feedback.data_clarity,
            improvement=feedback.improvement,
            session_data=feedback.session_data
        )
        
        return FeedbackResponse(
            status="success",
            message="Thank you for your feedback! Your input helps us improve SoundCity.",
            feedback_id=feedback_id
        )
        
    except Exception as e:
        logger.error(f"Error saving feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save feedback")


@router.get("/stats", response_model=FeedbackStats)
async def get_feedback_stats():
    """
    Get basic feedback statistics
    
    Returns summary statistics of collected feedback
    """
    try:
        stats = feedback_service.get_statistics()
        return FeedbackStats(**stats)
        
    except Exception as e:
        logger.error(f"Error retrieving feedback stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve feedback statistics")
