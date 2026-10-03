from datetime import date, time

from sqlmodel import Field, SQLModel

from .tipos import (
    configSchemaEstado,
    configSchemaNombreServicio,
    configSchemasID,
)


class TurnoBase(SQLModel):
    servicio_nombre: configSchemaNombreServicio
    fecha: date
    hora: time
    usuario_id: int = Field(foreign_key="usuario.id")
    estado: configSchemaEstado


class TurnoCreate(TurnoBase):
    pass


class TurnoUpdate(TurnoBase):
    pass


class TurnoResponse(TurnoBase):
    id: configSchemasID
