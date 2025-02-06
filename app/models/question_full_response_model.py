#This is where i will define my model to create structured output for my grade_feedback function 

from pydantic import BaseModel
from typing import Dict

class MarkFeedback(BaseModel):
    """Represents the feedback for a specific mark"""
    feedback: str
    
class GPTStructuredResponse(BaseModel):
    """
    The overall structured response from GPT.
    -'marks' is a dictionary of dynamic mark keys -> MarkFeedback objects
    -'totalMarks'  is a string summarizing total achieved vs. total possible
    -'finalFeedback' is a string summarizing overall performance    
    """
    
    marks: Dict[str, MarkFeedback]
    totalMarks: str
    finalFeedback: str
    
    