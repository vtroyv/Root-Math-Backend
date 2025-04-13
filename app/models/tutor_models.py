from pydantic import BaseModel
from typing import List, Dict

class PromptResponse(BaseModel):
    id: str
    title: str
    currentUrl: str
    latestConversation: List[Dict]
    lessonContext: Dict
    
