from pydantic import BaseModel, ConfigDict  # noqa: I001
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

class TurnoUpdate(TurnoBase):
    pass
 
class TurnoResponse(TurnoBase):
    id: configSchemasID
    estado: configSchemaEstado

    model_config = ConfigDict(from_attributes=True)