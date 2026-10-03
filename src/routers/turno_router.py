from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.core import exceptions
from src.database.database import get_db
from src.models.turno_model import Turno
from src.models.usuario_model import Usuario
from src.schemas.schemas_nested import TurnoResponseNested
from src.schemas.turnos import TurnoCreate, TurnoResponse

router = APIRouter(prefix="/turnos", tags=["Turnos"])


def validar_turno(datos: TurnoCreate, db: Session, turno_id: int | None = None):
    if not db.get(Usuario, datos.usuario_id):
        raise HTTPException(status_code=404, detail=exceptions.USUARIO_NO_ENCONTRADO)

    consulta = select(Turno).where(
        Turno.fecha == datos.fecha,
        Turno.hora == datos.hora,
    )
    if turno_id is not None:
        consulta = consulta.where(Turno.id != turno_id)

    if db.exec(consulta).first():
        raise HTTPException(status_code=409, detail=exceptions.TURNO_OCUPADO)


@router.get("/", response_model=list[TurnoResponseNested])
def obtener_turnos(
    desde: date | None = None,
    hasta: date | None = None,
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
    if desde:
        consulta = consulta.where(Turno.fecha >= desde)
    if hasta:
        consulta = consulta.where(Turno.fecha <= hasta)

    consulta = consulta.order_by(Turno.fecha, Turno.hora)  # pyright: ignore[reportArgumentType]

    return db.exec(consulta).all()


@router.get(
    "/{turno_id}", response_model=TurnoResponseNested, responses=exceptions.not_found
)
def obtener_turno(turno_id: int, db: Session = Depends(get_db)):  # noqa: B008
    turno = db.get(Turno, turno_id)
    if not turno:
        raise HTTPException(status_code=404, detail=exceptions.TURNO_NO_ENCONTRADO)
    return turno


@router.post(
    "/",
    response_model=TurnoResponse,
    status_code=201,
    responses={**exceptions.not_found, **exceptions.conflict},
)
def crear_turno(turno_nuevo: TurnoCreate, db: Session = Depends(get_db)):  # noqa: B008
    validar_turno(turno_nuevo, db)

    nuevo_turno = Turno.model_validate(turno_nuevo)
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


@router.put(
    "/{turno_id}",
    response_model=TurnoResponse,
    responses={**exceptions.not_found, **exceptions.conflict},
)
def actualizar_turno(
    turno_id: int,
    turno_nuevo: TurnoCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    turno = db.get(Turno, turno_id)
    if not turno:
        raise HTTPException(status_code=404, detail=exceptions.TURNO_NO_ENCONTRADO)

    validar_turno(turno_nuevo, db, turno_id=turno_id)

    turno.sqlmodel_update(turno_nuevo.model_dump())
    db.add(turno)
    db.commit()
    db.refresh(turno)
    return turno


@router.delete("/{turno_id}", responses=exceptions.not_found)
def borrar_turno(turno_id: int, db: Session = Depends(get_db)):  # noqa: B008
    turno = db.get(Turno, turno_id)
    if not turno:
        raise HTTPException(status_code=404, detail=exceptions.TURNO_NO_ENCONTRADO)

    db.delete(turno)
    db.commit()
    return {"mensaje": "Turno borrado correctamente"}
