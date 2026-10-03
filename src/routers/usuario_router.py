from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, col, select

from src.core import exceptions
from src.database.database import get_db
from src.models.usuario_model import Usuario
from src.schemas.schemas_nested import UsuarioResponseNested
from src.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def validar_dni(dni: str, db: Session):
    consulta = select(Usuario).where(Usuario.dni == dni)
    resultado = db.exec(consulta)
    if resultado.first():
        raise HTTPException(status_code=409, detail=exceptions.DNI_DUPLICADO)


@router.get("/", response_model=list[UsuarioResponse])
async def obtener_usuarios(
    nombre: str | None = None,
    dni: str | None = None,
    db: Session = Depends(get_db),  # noqa: B008
):
    consulta = select(Usuario)
    if nombre:
        consulta = consulta.where(col(Usuario.nombre).like(f"%{nombre}%"))
    if dni:
        consulta = consulta.where(Usuario.dni == dni)
    resultado = db.exec(consulta)
    return resultado.all()


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponseNested,
    responses=exceptions.not_found,
)
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):  # noqa: B008
    consulta = select(Usuario).where(Usuario.id == usuario_id)
    resultado = db.exec(consulta)
    usuario = resultado.first()
    if not usuario:
        raise HTTPException(status_code=404, detail=exceptions.USUARIO_NO_ENCONTRADO)
    return usuario


@router.post("/", response_model=UsuarioResponse, responses=exceptions.conflict_usuario)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):  # noqa: B008
    validar_dni(usuario.dni, db)
    nuevo_usuario = Usuario.model_validate(usuario)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    responses={**exceptions.not_found, **exceptions.conflict_usuario},
)
async def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    usuario_actualizado = db.get(Usuario, usuario_id)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail=exceptions.USUARIO_NO_ENCONTRADO)

    validar_dni(usuario.dni, db)

    usuario_actualizado.sqlmodel_update(usuario.model_dump())

    db.add(usuario_actualizado)
    db.commit()
    db.refresh(usuario_actualizado)
    return usuario_actualizado


@router.delete("/{usuario_id}", responses=exceptions.not_found)
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):  # noqa: B008
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail=exceptions.USUARIO_NO_ENCONTRADO)
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado"}
