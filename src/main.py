from fastapi import FastAPI

from src.database.database import SQLModel, engine
from src.routers.turno_router import router
from src.routers.usuario_router import router as usuario_router

app = FastAPI(title="turnosApi")


app.include_router(router, prefix="")
app.include_router(usuario_router, prefix="")
