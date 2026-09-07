from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from models.turno_model import Turno
from schemas import turnos as schemas_turnos 


router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.post("/", response_model=schemas_turnos.TurnoResponse)
def crear_turno(turno: schemas_turnos.TurnoCreate, db: Session = Depends(get_db)):
    nuevo_turno = Turno(**turno.model_dump())
    
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    
    return nuevo_turno


@router.get("/", response_model=List[schemas_turnos.TurnoResponse])
def obtener_turnos(db: Session = Depends(get_db)):
    turnos = db.query(Turno).all()
    return turnos




@router.delete("/{turno_id}")
def borrar_turno(turno_id: int, db: Session = Depends(get_db)):
    turno_guardado = db.query(Turno).filter(Turno.id == turno_id).first()
    
    if not turno_guardado:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
        
    db.delete(turno_guardado)
    db.commit()
    
    return {"mensaje": f"Turno {turno_id} cancelado correctamente"}