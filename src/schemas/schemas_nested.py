from src.schemas.turnos import TurnoResponse
from src.schemas.usuario import UsuarioResponse


class UsuarioResponseNested(UsuarioResponse):
    turnos: list[TurnoResponse] = []


class TurnoResponseNested(TurnoResponse):
    usuario: UsuarioResponse
