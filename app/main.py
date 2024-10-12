from typing import Dict

from fastapi import FastAPI

from app.routers import task, user

app = FastAPI()


@app.get("/")
async def welcome() -> Dict:
    return {"message": "Welcome to Taskmanager"}


app.include_router(task.router)
app.include_router(user.router)
