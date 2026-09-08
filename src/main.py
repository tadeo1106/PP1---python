
from fastapi import FastAPI

from src.database.database import Base, engine
from src.routers.turno_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="turnosApi")


app.include_router(router, tags=["turnos"], prefix="")



