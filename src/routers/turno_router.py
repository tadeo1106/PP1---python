from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, col, select

from src.core import exceptions
from src.database.database import get_db
from src.models.turno_model import Turno, TurnoCreate, TurnoResponse

router = APIRouter(prefix="/turnos", tags=["Turnos"])


from datetime import date


@router.get("/", response_model=list[TurnoResponse])
async def obtener_turnos(
    desde: date | None = None,
    hasta: date | None = None,
    nombre: str | None = None,
    dni: str | None = None,
    servicio: str | None = None,
    db: Session = Depends(get_db),  # noqa: B008
):
    if desde and hasta and desde > hasta:
        raise HTTPException(
            status_code=400, detail="'desde' no puede ser posterior a 'hasta'"
        )

    consulta = select(Turno)
    if servicio:
        consulta = consulta.where(Turno.servicio_nombre == servicio)
    if dni:
        consulta = consulta.where(Turno.cliente_dni == dni)
    if nombre:
        consulta = consulta.where(col(Turno.cliente_nombre).ilike(f"%{nombre}%"))
    if desde:
        consulta = consulta.where(Turno.fecha >= desde)
    if hasta:
        consulta = consulta.where(Turno.fecha <= hasta)

    consulta = consulta.order_by(Turno.fecha, Turno.hora)  # pyright: ignore[reportArgumentType]

    return db.exec(consulta).all()


@router.get("/{turno_id}", response_model=TurnoResponse, responses=exceptions.not_found)
async def obtener_turno(turno_id: int, db: Session = Depends(get_db)):  # noqa: B008
    turno = db.get(Turno, turno_id)

    if not turno:
        raise HTTPException(status_code=404, detail=exceptions.not_found)

    return turno


@router.post("/", response_model=TurnoResponse, responses=exceptions.conflict)
async def crear_turno(turno_nuevo: TurnoCreate, db: Session = Depends(get_db)):  # noqa: B008
    consulta = select(Turno).where(
        Turno.fecha == turno_nuevo.fecha, Turno.hora == turno_nuevo.hora
    )

    turno_ocupado = db.exec(consulta).first()

    if turno_ocupado:
        raise HTTPException(status_code=409, detail=exceptions.conflict)

    nuevo_turno = Turno.model_validate(turno_nuevo)
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)

    return nuevo_turno


@router.delete("/{turno_id}", responses=exceptions.not_found)
async def borrar_turno(turno_id: int, db: Session = Depends(get_db)):  # noqa: B008
    turno = db.get(Turno, turno_id)

    if not turno:
        raise HTTPException(status_code=404, detail=exceptions.not_found)

    db.delete(turno)
    db.commit()

    return {"mensaje": "turno borrado correctamente "}


@router.put(
    "/{turno_id}",
    response_model=TurnoResponse,
    responses=exceptions.not_found,
)
async def actualizar_turno_completo(
    turno_id: int,
    datos_actualizar: TurnoCreate,
    db: Session = Depends(get_db),  # noqa: B008
):

    turno_guardado = db.get(Turno, turno_id)
    if not turno_guardado:
        raise HTTPException(status_code=404, detail=exceptions.not_found)

    consulta = select(Turno).where(
        Turno.fecha == datos_actualizar.fecha,
        Turno.hora == datos_actualizar.hora,
        Turno.id != turno_id,
    )

    turno_ocupado = db.exec(consulta).first()

    if turno_ocupado:
        raise HTTPException(status_code=400, detail=exceptions.conflict)

    for clave, valor in datos_actualizar.model_dump().items():
        if valor is not None:
            setattr(turno_guardado, clave, valor)

    db.commit()
    db.refresh(turno_guardado)

    return turno_guardado
