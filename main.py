from fastapi import FastAPI

from db.database import Base, engine
from routes import questions

app = FastAPI()

app.include_router(questions.router)

Base.metadata.create_all(bind=engine)