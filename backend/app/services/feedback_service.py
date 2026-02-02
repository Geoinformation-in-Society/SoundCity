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
        useful_features: list,
        most_important_indicators: list,
        housing_decision: str,
        data_clarity: str,
        improvement: Optional[str],
        session_data: Optional[Dict] = None
    ) -> int:
        """
        Submit new feedback entry

        Args:
            useful_features: List of features used (up to 2)
            most_important_indicators: List of indicators user focused on (up to 2)
            housing_decision: Support level for housing decisions (not_at_all/slightly/moderately/largely/fully)
            data_clarity: Data clarity rating (strongly_disagree/disagree/neutral/agree/strongly_agree)
            improvement: Suggested improvements (optional)
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
            "useful_features": useful_features,
            "most_important_indicators": most_important_indicators,
            "housing_decision": housing_decision,
            "data_clarity": data_clarity,
            "improvement": improvement,
            "session_data": session_data,
            "timestamp": datetime.now().isoformat()
        }

        # Add and save
        data.append(entry)
        self._save_feedback(data)

        logger.info(f"Feedback submitted: ID={feedback_id}, Features={useful_features}, Indicators={most_important_indicators}")

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
                "average_data_clarity": 0.0,
                "housing_decision_distribution": {},
                "feature_breakdown": {},
                "indicator_breakdown": {}
            }
        
        # Calculate basic stats
        total = len(data)
        
        # Data clarity: Convert Likert scale to numeric for averaging
        clarity_scale = {
            "strongly_disagree": 1,
            "disagree": 2,
            "neutral": 3,
            "agree": 4,
            "strongly_agree": 5
        }
        clarity_scores = [clarity_scale.get(item.get('data_clarity', 'neutral'), 3) for item in data]
        avg_clarity = sum(clarity_scores) / total if clarity_scores else 0
        
        # Housing decision distribution
        housing_counts = {}
        for item in data:
            decision = item.get('housing_decision', 'Unknown')
            housing_counts[decision] = housing_counts.get(decision, 0) + 1
        
        # Feature popularity (accounting for multi-select)
        feature_counts = {}
        for item in data:
            features = item.get('useful_features', [])
            for feature in features:
                feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        # Indicator popularity (accounting for multi-select)
        indicator_counts = {}
        for item in data:
            indicators = item.get('most_important_indicators', [])
            for indicator in indicators:
                indicator_counts[indicator] = indicator_counts.get(indicator, 0) + 1
        
        return {
            "total_responses": total,
            "average_data_clarity": round(avg_clarity, 2),
            "housing_decision_distribution": housing_counts,
            "feature_breakdown": feature_counts,
            "indicator_breakdown": indicator_counts
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
