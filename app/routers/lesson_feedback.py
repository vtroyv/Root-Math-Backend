from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..utils.preprocess_sympy import preprocess_sympy
from ..utils.llm import grade_lesson_feedback
from ..models.lesson_response_model import StudentResponse

app = FastAPI()

# Define our BaseModels to represent the structure of data
# Arriving from the APIRoute


router = APIRouter(prefix='/lesson-feedback')

@router.post("/")
async def feedback(response: StudentResponse):
    # print(f"The original task sent to fastAPI is {response.task} ")
    # print(f"The original latex sent ot fastAPI is {response.latexInput}")
    # You will have to call grade_lesson_feedback to get the feedback for the lesson, 
    #It should return the feedback as well as a boolean correct :true or false 
    
    structured_lesson_feedback = grade_lesson_feedback(response)
    # print(f"The test is {test}")
    
    
    return (structured_lesson_feedback)
    
app.include_router(router)

# This is where your router logic will go to enable you to process the result.
