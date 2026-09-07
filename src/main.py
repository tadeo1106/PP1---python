
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine, Base
from models import turno_model
from routers.turno_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="turnosApi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["turnos"], prefix="")



