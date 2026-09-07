from pydantic import BaseModel, ConfigDict
from typing import Optional

from schemas.tipos import (
    configSchemaDia,
    configSchemaEstado,
    configSchemasID,
    configSchemaHorario,
)

class TurnoBase(BaseModel):
    cliente_id: configSchemasID
    servicio_id: configSchemasID 
    dia: configSchemaDia
    horario: configSchemaHorario


class TurnoCreate(TurnoBase):
    pass 


class TurnoUpdate(BaseModel):
    cliente_id: Optional[configSchemasID] = None
    servicio_id: Optional[configSchemasID] = None
    dia: Optional[configSchemaDia] = None
    horario: Optional[configSchemaHorario] = None
    estado: Optional[configSchemaEstado] = None


class TurnoResponse(TurnoBase):
    id: configSchemasID
    estado: configSchemaEstado

    model_config = ConfigDict(from_attributes=True)
    