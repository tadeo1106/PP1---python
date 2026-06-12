
from fastapi import FastAPI 
from src.routers.turno_router import router


app = FastAPI()

app.title = "turnosApi"  

app.include_router(router, tags=["turnos"], prefix="/turnos")

