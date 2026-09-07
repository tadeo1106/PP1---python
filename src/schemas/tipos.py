from pydantic import BaseModel, Field
from typing import Annotated
from datetime import date, time


configSchemasID = Annotated[int, Field(gt=0, description="ID numérico en la base de datos")]
configSchemaDocumento = Annotated[str, Field(min_length=7, description="DNI del cliente")]
configSchemaNombre = Annotated[str, Field(min_length=3, max_length=50, description="Nombre del cliente")]
configSchemaNombreServicio = Annotated[str, Field(min_length=3, max_length=100, description="Nombre del servicio")]


configSchemaDia = Annotated[date, Field(description="Fecha del turno, formato AAAA-MM-DD")]
configSchemaHorario = Annotated[time, Field(description="Horario del turno, formato HH:MM")]

configSchemaEstado = Annotated[str, Field(description="Estado actual del turno")]