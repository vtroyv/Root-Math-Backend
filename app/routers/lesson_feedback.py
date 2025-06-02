from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..utils.others.preprocess_sympy import preprocess_sympy
from ..utils.others.llm import grade_lesson_feedback, multiple_choice_image_response
from ..models.lesson_response_model import StudentResponse, MultipleChoiceImage, Sketch, MultipleChoice, QuestionImage, CurveAndMFE
from ..utils.others.preprocess_sympy import preprocess_sympy
from ..utils.lesson_task_utils.sketch.lagrange_interpolation import lagrange_implementation
from ..utils.lesson_task_utils.sketch.sketch_task_feedback import feedback_sketch_task
from ..utils.lesson_task_utils.multiple_choice.multiple_choice_task_feedback import multiple_choice_response
from ..utils.lesson_task_utils.question_image.question_image_task_feedback import feedback_question_image
from ..utils.lesson_task_utils.curve_and_mfe.curve_and_mfe_feedback import feedback_curve_and_mfe

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
    print(f"The reponse is {response}")
    feedback = feedback_sketch_task(response)
    print(f"The feedback is {feedback}")
    
    return(feedback)

@router.post("/multiple-choice")
async def feedback_multiple_choice(response: MultipleChoice):
    feedback = multiple_choice_response(response)
    return feedback


@router.post("/image")
async def feedback_image(response: QuestionImage):
    feedback = feedback_question_image(response)
    return feedback

@router.post("/curve-and-mfe")
async def feedback_curveMFE(response: CurveAndMFE):
    print(f"The response is {response}")
    feedback = feedback_curve_and_mfe(response)
    #Successfully recieving lesson data now add implementation logic
    #Remember to make your code as reusable as possible particularly for checking equivalence of expected expressions and given expressions
    pass

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
