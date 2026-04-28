from fastapi import FastAPI



app=FastAPI()


mensaje={"titulo":"contenido"}

@app.get("/")
async def mostrar_mensaje():
    return mensaje


@app.post("/")
async def nuevo_mensaje(titulo,contenido):
    msj={titulo:contenido}

    return {"detail":"no errores","nuevo mensaje":msj}
@app.put("/")
async def modificar_mensaje(titulo,contenido):   
    mensaje["titulo"]=titulo
    mensaje["contenido"]=contenido

    return {"detail":"no errores", "resultado":mensaje}



@app.delete("/")
async def borrar_mensaje():
    d=mensaje.pop("titulo")

    return {"detail":"no errores","resultado":mensaje,"lo que borraste":d}