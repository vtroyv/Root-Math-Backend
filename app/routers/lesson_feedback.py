from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..utils.preprocess_sympy import preprocess_sympy
from ..utils.llm import grade_lesson_feedback, multiple_choice_image_response
from ..models.lesson_response_model import StudentResponse, MultipleChoiceImage, Sketch
from ..utils.preprocess_sympy import preprocess_sympy

app = FastAPI()

# Define our BaseModels to represent the structure of data
# Arriving from the APIRoute



router = APIRouter(prefix='/lesson-feedback')

@router.post("/multiple-choice-images")
async def feedback_multiple_choice_images(response: MultipleChoiceImage):
    feedback_MCI = multiple_choice_image_response(response)
    return(feedback_MCI)

@router.post("/sketch")
async def feedback_sketch(response: Sketch):
    print(f"The sketch response is  {response}")
    return(response)

    

@router.post("/")
async def feedback(response: StudentResponse):
    
    try:
        test = preprocess_sympy
        print(test)
    except:
        print('could\'t clearn up the sympy ')
        pass
    
    
    structured_lesson_feedback = grade_lesson_feedback(response)

    
    
    return (structured_lesson_feedback)
    
    
    

app.include_router(router)



# This is where your router logic will go to enable you to process the result.
