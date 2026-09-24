from typing import Any

not_found: dict[int | str, dict[str, Any]] = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "id del cliente no encontrada",
                }
            }
        },
    },
}


conflict: dict[int | str, dict[str, Any]] = {
    409: {
        "description": "Conflicto turnos",
        "content": {
            "application/json": {
                "example": {"detail": "Ya hay un turno para ese día y esa hora"}
            }
        },
    }
}
