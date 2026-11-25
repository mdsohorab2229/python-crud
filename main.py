from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from db import engine
from model import student , subject
from sqlalchemy import inspect
from routers import student_controller

student.base.metadata.create_all(bind = engine)
subject.base.metadata.create_all(bind = engine)



app = FastAPI(title="student management")
app.include_router(student_controller.router)

FRONTEND_FOLDER=Path(__file__).parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_FOLDER, html=True), name="frontend")

