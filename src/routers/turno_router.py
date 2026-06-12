from typing import Annotated

from src.models.turno_model import TurnoSchemas,TurnoCreateUpdateSchemas

from fastapi import APIRouter, HTTPException ,Query,Path 

from src.database.db import turnos 

from src.core.exceptions import not_found

router=APIRouter()


path_id = Annotated[int, Path(gt=0, description="id mayor a 0")]


@router.get("/turnos", response_model=list[TurnoSchemas])
async def mostrar_turnos(
        servicio: str = Query(description="¿Por qué servicio desea filtrar?", default=None),
):
    turnos_filtrados = turnos

    if servicio:
        turnos_filtrados = [
            turno for turno in turnos
            if servicio in turno["servicio"]
        ]
    
    return turnos_filtrados


@router.get("/turnos/{id}", response_model=TurnoSchemas,responses= not_found)
async def turno_by_id( id:path_id):
    for turno in turnos:
        if turno["id"]==id:
            return turno
    raise HTTPException(status_code=404,detail="id no encontrado")



@router.post("/turnos",response_model=TurnoCreateUpdateSchemas)
async def agregar_turno(turno:TurnoCreateUpdateSchemas):

    id=max(turnos,key=lambda x:x["id"])["id"]+1

    nuevo_turno=(turno.model_dump())

    nuevo_turno["id"]=id

    turnos.append(nuevo_turno)
    
    return nuevo_turno      



@router.put("/turnos/{id}",response_model=TurnoSchemas,responses=not_found)
async def modificar_turno(
    id:path_id,
    turno_editar:TurnoCreateUpdateSchemas
    ):
    for turno in turnos:
        if turno["id"] == id:
            turno["cliente"]=turno_editar.cliente
            turno["dia"]=turno_editar.dia
            turno["horario"]=turno_editar.horario
            turno["servicio"]=turno_editar.servicio
            

            return turno
        
    raise HTTPException(status_code=404, detail="id del turno no encontrado")


@router.delete("/turnos/{id}", responses=not_found)
async def eliminar_turno(id: path_id):
    for turno in turnos:
        if turno["id"] == id:
            turnos.remove(turno) 
            return {"mensaje": "Turno eliminado"}
            
    raise HTTPException(status_code=404, detail="id no encontrado")