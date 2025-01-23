from fastapi import FastAPI
from .routers import feedback
from .routers import sketch

app = FastAPI()
app.include_router(feedback.router)
app.include_router(sketch.router)

@app.get("/")
async def root():
    return {"Message": "Hello World"}


