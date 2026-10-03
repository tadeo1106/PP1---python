from typing import Any

TURNO_NO_ENCONTRADO = "Turno no encontrado"
USUARIO_NO_ENCONTRADO = "Usuario no encontrado"
TURNO_OCUPADO = "Ya hay un turno para ese día y esa hora"
DNI_DUPLICADO = "Ya existe un usuario con ese DNI"


not_found: dict[int | str, dict[str, Any]] = {
    404: {
        "description": "No se encontró el recurso con ese id",
        "content": {"application/json": {"example": {"detail": TURNO_NO_ENCONTRADO}}},
    },
}

conflict: dict[int | str, dict[str, Any]] = {
    409: {
        "description": "Conflicto: el horario ya está ocupado",
        "content": {"application/json": {"example": {"detail": TURNO_OCUPADO}}},
    }
}

conflict_usuario: dict[int | str, dict[str, Any]] = {
    409: {
        "description": "Conflicto: DNI duplicado o usuario con turnos",
        "content": {"application/json": {"example": {"detail": DNI_DUPLICADO}}},
    }
}
