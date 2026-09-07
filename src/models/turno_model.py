from sqlalchemy import Column, Date, Integer, String, Time
from src.database.bd import Base

class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)

    cliente_nombre = Column(String)

    cliente_dni = Column(String)

    servicio_nombre = Column(String)

    fecha = Column(Date)

    hora = Column(Time)
    
    estado = Column(String, default="Pendiente")