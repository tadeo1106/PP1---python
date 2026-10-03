from sqlmodel import SQLModel

from src.schemas.tipos import (
    configSchemaCorreoElectronico,
    configSchemaDocumento,
    configSchemaNombre,
    configSchemasID,
)


class UsuarioBase(SQLModel):
    dni: configSchemaDocumento
    nombre: configSchemaNombre
    correo_electronico: configSchemaCorreoElectronico


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: configSchemasID
