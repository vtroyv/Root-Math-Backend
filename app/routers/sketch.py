from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List,Dict,Any
from ..utils.llm import sketch_feedback

app =FastAPI()

class SketchResponse(BaseModel):
    coordinates: List[dict]
    questionData: Dict[str, Any]
    
router = APIRouter(prefix='/sketch/feedback')

@router.post("/")
async def feedback(response: SketchResponse):
    test = response.coordinates
    answer = response.questionData['intercepts']
    print(f'The coordinates are from the user are {test}')
    print(f'The answer from the questiondata is {answer}')
    
    return {"feedback": 'This router is working'}, 
# Now note that the coordinates are recieved, from left -> right with respect to the x axis, therefore first we should, 
#arrange our answer coordinates from left to right
#so we have: 

app.include_router(router)