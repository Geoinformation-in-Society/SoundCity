"""
Feedback service for managing user feedback
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service for handling feedback operations"""
    
    def __init__(self):
        """Initialize feedback service"""
        self.data_dir = Path(__file__).parent.parent / "data" / "feedback"
        self.feedback_file = self.data_dir / "feedback.json"
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_feedback(self) -> List[Dict]:
        """
        Load feedback from JSON file
        
        Returns:
            List of feedback entries
        """
        if not self.feedback_file.exists():
            return []
        
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Feedback file corrupted, returning empty list")
            return []
        except Exception as e:
            logger.error(f"Error loading feedback: {str(e)}")
            return []
    
    def _save_feedback(self, data: List[Dict]):
        """
        Save feedback to JSON file
        
        Args:
            data: List of feedback entries to save
        """
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving feedback: {str(e)}")
            raise
    
    def submit_feedback(
        self,
        satisfaction: int,
        useful_feature: str,
        most_important_indicator: str,
        housing_decision: str,
        improvement: Optional[str],
        would_recommend: bool,
        session_data: Optional[Dict] = None
    ) -> int:
        """
        Submit new feedback entry
        
        Args:
            satisfaction: Satisfaction rating (1-5)
            useful_feature: Most useful feature
            most_important_indicator: Most important indicator (air/noise/green/heat)
            housing_decision: Would use for housing decisions (definitely/maybe/no)
            improvement: Suggested improvements (optional)
            would_recommend: Would recommend to others
            session_data: Additional session metadata (optional)
        
        Returns:
            Feedback ID of the newly created entry
        """
        # Load existing feedback
        data = self._load_feedback()
        
        # Create new entry
        feedback_id = len(data) + 1
        entry = {
            "id": feedback_id,
            "satisfaction": satisfaction,
            "useful_feature": useful_feature,
            "most_important_indicator": most_important_indicator,
            "housing_decision": housing_decision,
            "improvement": improvement,
            "would_recommend": would_recommend,
            "session_data": session_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add and save
        data.append(entry)
        self._save_feedback(data)
        
        logger.info(f"Feedback submitted: ID={feedback_id}, Satisfaction={satisfaction}")
        
        return feedback_id
    
    def get_statistics(self) -> Dict:
        """
        Calculate feedback statistics
        
        Returns:
            Dictionary containing feedback statistics
        """
        data = self._load_feedback()
        
        if not data:
            return {
                "total_responses": 0,
                "average_satisfaction": 0.0,
                "recommendation_rate": 0.0,
                "most_useful_feature": None,
                "feature_breakdown": {}
            }
        
        # Calculate basic stats
        total = len(data)
        avg_satisfaction = sum(item['satisfaction'] for item in data) / total
        recommendations = sum(1 for item in data if item['would_recommend'])
        recommendation_rate = (recommendations / total) * 100
        
        # Feature popularity
        feature_counts = {}
        for item in data:
            feature = item.get('useful_feature', 'Unknown')
            feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        most_useful = max(feature_counts, key=feature_counts.get) if feature_counts else None
        
        return {
            "total_responses": total,
            "average_satisfaction": round(avg_satisfaction, 2),
            "recommendation_rate": round(recommendation_rate, 1),
            "most_useful_feature": most_useful,
            "feature_breakdown": feature_counts
        }
    
    def get_all_feedback(self) -> List[Dict]:
        """
        Get all feedback entries
        
        Returns:
            List of all feedback entries
        """
        return self._load_feedback()
    
    def export_to_csv(self, output_path: Path) -> bool:
        """
        Export feedback to CSV file
        
        Args:
            output_path: Path to save CSV file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            import csv
            
            data = self._load_feedback()
            if not data:
                return False
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            return True
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return False


# Create singleton instance
feedback_service = FeedbackService()
