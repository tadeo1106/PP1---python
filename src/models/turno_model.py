from sqlalchemy import Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from ..database.bd import  Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True)
    nombre = Column(String)


class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_servicio = Column(String) 


class Turno(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(String)
    fecha = Column(Date)
    horario = Column("hora", Time)
    estado = Column(String, default="pendiente")
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))


    cliente = relationship("Cliente")
    servicio = relationship("Servicio")