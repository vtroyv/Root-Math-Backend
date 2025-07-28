from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..utils.others.preprocess_sympy import preprocess_sympy
from ..utils.others.llm import grade_feedback, grade_feedback_blocks
from ..utils.others.grade_sympy_response import evaluate_correctness

app = FastAPI()

class StudentResponse(BaseModel):
    sympy: List[str]
    questionData: Dict[str,Any]

router = APIRouter(prefix='/feedback')

@router.post("/")
async def feedback(response: StudentResponse):
    # print(f'the initial response is {response}')
    data = preprocess_sympy(response.sympy)
    
    
    print(f'The original data is {data}')
    # print(f"The data is given by the following{data['meta_data']['response']}")
    
    mathematicallyCorrect = evaluate_correctness(data)
    # print(f"is the response mathematically correct? {mathematicallyCorrect}")
    
    feedbackData = {
        "usersSympyResponse": data['meta_data']['response'],
        "questionData": response.questionData
    }
    #grade_feedback should return the dictionary from GPTStructuredResponse
    
    
    
   
    # # print(f"The data i want to send to llm is {feedbackData}")
    # structured_result = grade_feedback(feedbackData)
    
    structured_result = grade_feedback_blocks(feedbackData)
    
    print(f"The data returned to nextjs is {structured_result}")
   
    return structured_result

app.include_router(router)
