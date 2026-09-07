from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.bd import get_db
from src.models.turno_model import Turno
from src.schemas import turnos as schemas_turnos


router = APIRouter(prefix="/turnos", tags=["Turnos"])


@router.get("/", response_model=List[schemas_turnos.TurnoResponse])
def obtener_turnos(db: Session = Depends(get_db)):


    turnos = db.query(Turno).all()
    return turnos


@router.post("/", response_model=schemas_turnos.TurnoResponse)
def crear_turno(turno: schemas_turnos.TurnoCreate, db: Session = Depends(get_db)):
    turno_ocupado = db.query(Turno).filter(
        Turno.fecha == turno.fecha,
        Turno.hora == turno.hora
    ).first()
    

    if turno_ocupado:
        raise HTTPException(
            status_code=400, 
            detail="Ese horario ya está ocupado. Por favor, elige otro."
        )

    nuevo_turno = Turno(**turno.model_dump())
    
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    
    return nuevo_turno


@router.delete("/{turno_id}")
def borrar_turno(turno_id: int, db: Session = Depends(get_db)):
    turno_guardado = db.query(Turno).filter(Turno.id == turno_id).first()
    
    if not turno_guardado:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
        
    db.delete(turno_guardado)
    db.commit()
    
    return {"mensaje": f"Turno {turno_id} cancelado correctamente"}




@router.put("/{turno_id}", response_model=schemas_turnos.TurnoResponse)
def actualizar_turno_completo(turno_id: int, datos_actualizar: schemas_turnos.TurnoUpdate, db: Session = Depends(get_db)):

    turno_guardado = db.query(Turno).filter(Turno.id == turno_id).first()
    
    if not turno_guardado:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
        
    turno_ocupado = db.query(Turno).filter(
        Turno.fecha == datos_actualizar.fecha,
        Turno.hora == datos_actualizar.hora,
        Turno.id != turno_id  
    ).first()
    
    if turno_ocupado:
        raise HTTPException(status_code=400, detail="El horario solicitado ya está ocupado.")


    for clave, valor in datos_actualizar.model_dump().items():
    
        if valor is not None: 
            setattr(turno_guardado, clave, valor)
            

    db.commit()
    db.refresh(turno_guardado)
    
    return turno_guardado