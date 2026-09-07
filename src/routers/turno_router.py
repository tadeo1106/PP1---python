from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from models.turno_model import Turno
from schemas import turnos as schemas_turnos 


router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.post("/", response_model=schemas_turnos.TurnoResponse)
def crear_turno(turno: schemas_turnos.TurnoCreate, db: Session = Depends(get_db)):
    # Pasamos los datos del esquema al modelo usando desempaquetado de Pydantic
    nuevo_turno = Turno(**turno.model_dump())
    
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    
    return nuevo_turno

# 2. READ (GET)
@router.get("/", response_model=List[schemas_turnos.TurnoResponse])
def obtener_turnos(db: Session = Depends(get_db)):
    turnos = db.query(Turno).all()
    return turnos

# 3. UPDATE (PUT)
@router.put("/{turno_id}", response_model=schemas_turnos.TurnoResponse)
def actualizar_turno(turno_id: int, datos_actualizar: schemas_turnos.TurnoUpdate, db: Session = Depends(get_db)):
    turno_guardado = db.query(Turno).filter(Turno.id == turno_id).first()
    
    if not turno_guardado:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    # Extraemos solo lo que el usuario envió (gracias al exclude_unset=True)
    datos_extraidos = datos_actualizar.model_dump(exclude_unset=True)
    
    for clave, valor in datos_extraidos.items():
        setattr(turno_guardado, clave, valor)
        
    db.commit()
    db.refresh(turno_guardado)
    
    return turno_guardado

# 4. DELETE (DELETE)
@router.delete("/{turno_id}")
def borrar_turno(turno_id: int, db: Session = Depends(get_db)):
    turno_guardado = db.query(Turno).filter(Turno.id == turno_id).first()
    
    if not turno_guardado:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
        
    db.delete(turno_guardado)
    db.commit()
    
    return {"mensaje": f"Turno {turno_id} cancelado correctamente"}