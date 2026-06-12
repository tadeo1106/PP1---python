
not_found = {
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
