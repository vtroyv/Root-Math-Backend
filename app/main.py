from fastapi import FastAPI
from .routers import question_feedback
from .routers import question_sketch_feedback
from .routers import lesson_feedback
from .routers import ask_tutor

app = FastAPI()
app.include_router(question_feedback.router)
app.include_router(question_sketch_feedback.router)
app.include_router(lesson_feedback.router)
app.include_router(ask_tutor.router)




@app.get("/")
async def root():
    return {"Message": "Hello World"}


