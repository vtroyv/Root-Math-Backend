from fastapi import FastAPI
from .routers import feedback

app = FastAPI()
app.include_router(feedback.router)

@app.get("/")
async def root():
    return {"Message": "Hello World"}


