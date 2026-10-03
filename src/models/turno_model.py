from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from src.schemas.turnos import TurnoBase

if TYPE_CHECKING:
    from src.models.usuario_model import Usuario


class Turno(TurnoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario: Optional["Usuario"] = Relationship(back_populates="turnos")
