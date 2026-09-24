from datetime import date, time

from sqlmodel import Field, SQLModel


class TurnoBase(SQLModel):
    cliente_nombre: str
    cliente_dni: str
    servicio_nombre: str
    fecha: date
    hora: time
    estado: str = "Pendiente"


class Turno(TurnoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TurnoCreate(TurnoBase):
    pass


class TurnoResponse(TurnoBase):
    id: int
