from fastapi import FastAPI
from .routers import question_feedback
from .routers import sketch
from .routers import lesson_feedback

app = FastAPI()
app.include_router(question_feedback.router)
app.include_router(sketch.router)
app.include_router(lesson_feedback.router)



@app.get("/")
async def root():
    return {"Message": "Hello World"}


