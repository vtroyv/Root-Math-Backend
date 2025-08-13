from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List,Dict,Any
from ..utils.others.llm import llm_sketch_feedback
from ..utils.lesson_task_utils.sketch.sketch_task_feedback import feedback_sketch_task

app =FastAPI()
# NOW GO THROUGH THIS FILE AND THE SKETCH QUESTION FEEDBACK -> SEE HOW IT"S MARKED AND IMPLEMENT SOMETHING SIMILAR HERE BUT ALSO USE LLM TO PROVIDE HELP!

# ---------------------------------------
# How sketch task questions are currently marked in lessontasks:
# First a response is sent which has the following form: 
# ------------------------------
# class SketchTask(BaseModel):
#     status: str
#     task: SketchTaskDetails
    
#  class SketchTaskDetails(BaseModel):
#     type: str
#     title: str
#     instructions: str
#     hint: str
#     gpt: str
#     renderType: str
#     marking: dict
    
# class Sketch(BaseModel):
#     task: SketchTask
#     reducedCoordinates: List[Dict[str, float]]
#     taskType: str
# -------------------------------
# Next we do the following: 
# -
# -> take the response and pass it on to the feedback_sketch_task.py file 
# -> Note that the most important thing is the marking dictionariy therefore when reusing this lesson sketch marking code to 
#    handle sketch questions i will need a similar marking object 
# so go through the marking object and essentially make sure it's a field in the question
# ---------------------------------------
class SketchResponse(BaseModel):
    reducedCoordinates: List[dict]
    questionData: Dict[str, Any]
    
router = APIRouter(prefix='/sketch/feedback')
# 
@router.post("/")
async def feedback(response: SketchResponse):
    # print(f" the reponse being sent is ", response )
    feedback = feedback_sketch_task(response)
    print('the feedback when marking the sketch questionTask is ', feedback)
  
#  
    
    
 
  
    
    return {"feedback": feedback}
# Now note that the coordinates are recieved, from left -> right with respect to the x axis, therefore first we should, 
#arrange our answer coordinates from left to right
#so we have: 

app.include_router(router)