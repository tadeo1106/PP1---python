from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.tipos import configSchemaDocumento, configSchemaNombre, configSchemasID




class ClienteBase(BaseModel):
    dni: configSchemaDocumento
    nombre: configSchemaNombre


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    dni: Optional[configSchemaDocumento] = None
    nombre: Optional[configSchemaNombre] = None


class ClienteResponse(ClienteBase):
    id: configSchemasID

    model_config = ConfigDict(from_attributes=True)
 