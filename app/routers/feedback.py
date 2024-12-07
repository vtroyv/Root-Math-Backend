from fastapi import APIRouter

router= APIRouter(prefix='/feedback')

@router.get("/")
async def feedback():
    return {"feedback": "Good Job"}

