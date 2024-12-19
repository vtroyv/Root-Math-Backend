from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
from ..utils.preprocess_sympy import preprocess_sympy
from sympy import sympify

app = FastAPI()

class StudentResponse(BaseModel):
    sympy: List[str]

router = APIRouter(prefix='/feedback')

@router.post("/")
async def feedback(response: StudentResponse):
    data = preprocess_sympy(response)
    print(f"The data is given by the following{data['meta_data']['response']}")
   
    return {"feedback": "Good Job"}

app.include_router(router)
