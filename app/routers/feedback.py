from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
from ..utils.preprocess_sympy import preprocess_sympy
from ..utils.llm import grade_feedback
from sympy import sympify

app = FastAPI()

class StudentResponse(BaseModel):
    sympy: List[str]
    questionData: dict[str,str]

router = APIRouter(prefix='/feedback')

@router.post("/")
async def feedback(response: StudentResponse):
    print(f'the initial response is {response}')
    data = preprocess_sympy(response.sympy)
    
    print(f'The original data is {data}')
    print(f"The data is given by the following{data['meta_data']['response']}")
    
    feedbackData = {
        "usersSympyResponse": data['meta_data']['response'],
        "questionData": response.questionData
    }
    
   
    print(f"The data i want to send to llm is {feedbackData}")
    feedback = grade_feedback(feedbackData)
   
    return {"feedback": feedback}

app.include_router(router)
