from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from .tipos import (
    configSchemaDia,
    configSchemaHorario,
    configSchemaDocumento,
    configSchemaEstado,
    configSchemaNombre,
    configSchemasID,
)

class TurnoBase(BaseModel):
    documento: configSchemaDocumento
    cliente: configSchemaNombre
    dia: configSchemaDia
    horario: configSchemaHorario
    servicio: List[str] = Field(min_length=1)


class TurnoCreate(TurnoBase):
    pass 


class TurnoUpdate(BaseModel):
    documento: Optional[configSchemaDocumento] = None
    cliente: Optional[configSchemaNombre] = None
    dia: Optional[configSchemaDia] = None
    horario: Optional[configSchemaHorario] = None
    servicio: Optional[List[str]] = None


class TurnoResponse(TurnoBase):
    id: configSchemasID
    estado: configSchemaEstado

    model_config = ConfigDict(from_attributes=True)
    