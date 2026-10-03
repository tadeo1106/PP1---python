from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.schemas.usuario import UsuarioBase

if TYPE_CHECKING:
    from src.models.turno_model import Turno


class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    turnos: list["Turno"] = Relationship(back_populates="usuario")
