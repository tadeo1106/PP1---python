from fastapi import FastAPI

import src.models
from src.database.database import SQLModel, engine
from src.routers.turno_router import router

SQLModel.metadata.create_all(bind=engine)


app = FastAPI(title="turnosApi")


app.include_router(router, tags=["turnos"], prefix="")
