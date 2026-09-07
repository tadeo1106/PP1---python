from pydantic import BaseModel, ConfigDict
from typing import Optional

from schemas.tipos import configSchemaNombreServicio, configSchemasID





class ServicioBase(BaseModel):
    nombre_servicio: configSchemaNombreServicio

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[configSchemaNombreServicio] = None

class ServicioResponse(ServicioBase):
    id: configSchemasID

    model_config = ConfigDict(from_attributes=True)