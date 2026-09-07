from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time

from .tipos import (
    configSchemaDni,
    configSchemaEstado,
    configSchemaNombre,
    configSchemaNombreServicio,
    configSchemasID,
)



class TurnoBase(BaseModel):
    cliente_nombre: configSchemaNombre
    cliente_dni: configSchemaDni
    servicio_nombre: configSchemaNombreServicio
    fecha: date
    hora: time

class TurnoCreate(TurnoBase):
    pass

class TurnoUpdate(BaseModel):
    cliente_nombre: Optional[configSchemaNombre] = None
    cliente_dni: Optional[configSchemaDni] = None
    servicio_nombre: Optional[configSchemaNombreServicio] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    estado: Optional[configSchemaEstado] = None

class TurnoResponse(TurnoBase):
    id: configSchemasID
    estado: configSchemaEstado

    model_config = ConfigDict(from_attributes=True)