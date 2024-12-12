from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
from ..utils import preprocess_sympy
from sympy import sympify

app = FastAPI()

class StudentResponse(BaseModel):
    sympy: List[str]

router = APIRouter(prefix='/feedback')

@router.post("/")
async def feedback(response: StudentResponse):
    # print("Parsed response object:", response)
    funcs = [sympify(expr) for expr in response.sympy]
    print("The sympyified functions should look like",funcs )
    
    # This will print something like: response=StudentResponse(response=[1,2,3,4,5])
    print("List of numbers:", response.sympy)
    # This will print just the list: [1, 2, 3, 4, 5]

    return {"feedback": "Good Job"}

app.include_router(router)
