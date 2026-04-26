from fastapi import FastAPI,Query,Path,Body

peliculas = [
    {"id": 1, "titulo": "Inception", "año": 2010, "genero": "ciencia ficcion","activo":True},
    {"id": 2, "titulo": "The Dark Knight", "año": 2008, "genero": "accion", "activo":True},
    {"id": 3, "titulo": "Titanic", "año": 1997, "genero": "romance","activo":True},
]





app = FastAPI()



@app.get("/pelicula")
async def filtrar_genero(
        genero: str = Query(description="porque genero desea filtrar?",default=None),
        ordenar: str =Query(description="porq desea ordenar por anio o titulo",default=None)
):
    peliculas_filtradas=peliculas

    if genero:
        peliculas_filtradas=[
        pelicula for pelicula in peliculas
        if pelicula["genero"].lower()==genero.lower()]
    
    if ordenar:
        if ordenar == "titulo":
            peliculas_filtradas=sorted(peliculas_filtradas,key=lambda x:x["titulo"])
        elif ordenar == "anio":
            peliculas_filtradas=sorted(peliculas_filtradas,key=lambda x:x["año"])

    return peliculas_filtradas if peliculas_filtradas else {"error":"no encontrado"}



@app.get("/pelicula/{id}")
async def pelicula_id(
    id:int = Path(gt=0,description="ID mayor a 0")
    ):

    resultado=[pelicula for pelicula in peliculas
            if pelicula["id"]==id]
    return resultado if resultado else {"error": "id no encontrado"}



@app.post("/pelicula")
async def agregar_pelicula(
    titulo: str =Body(min_length=3),
    año: int = Body(ge=1900, le=2100),
    genero: str = Body(min_length=3)):


    if not titulo.strip() or not genero.strip():
        return {"error": "no puede estar vacio"}
    
    id=max(peliculas,key=lambda x:x["id"])["id"]+1




    pelicula={
        "id":id,
        "titulo":titulo,
        "año": año,
        "genero":genero}
    
    peliculas.append(pelicula)

    return {"correcto":pelicula}        



@app.put("/pelicula/{id}")
async def modificar_pelicula(
    id:int=Path(gt=0, description="id mayor a 0"),
    titulo: str =Body(min_length=3),
    año: int = Body(ge=1900, le=2100),
    genero: str = Body(min_length=3)
    ):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            pelicula["id"]=id
            pelicula["titulo"]=titulo
            pelicula["año"]=año
            pelicula["genero"]=genero

            return {"detail":"modificacion echas correctamente","pelicula":pelicula}
        
    return{"detail":"id no encontrado"}



@app.delete("/pelicula/{id}")
async def borrar_pelicula(
    id: int=Path(gt=0, description="id mayor a 0"),
    logico: bool=Query(description="mantener registro",default=True)
    ):

    for pelicula in peliculas:
        if pelicula["id"]==id:
            if logico:
                pelicula["activo"]=False            
            else:
                peliculas.remove(pelicula)
            return {"detail":"borrado correctamente","peliculas":peliculas}
                    
    return{"detail":"id no encontrado","peliculas":peliculas}
