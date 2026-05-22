from fastapi import FastAPI,Query,Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

peliculas = [
    {"id": 1, "titulo": "Inception", "año": 2010, "genero": "ciencia ficcion","activo":True},
    {"id": 2, "titulo": "The Dark Knight", "año": 2008, "genero": "accion", "activo":True},
    {"id": 3, "titulo": "Titanic", "año": 1997, "genero": "romance","activo":True},
]


configSchemasID=Annotated[int , Field(gt=0,description="id del articulo")]

configSchemaTitulos=Annotated[str,Field(max_length=40)]

configSchemaAño = Annotated[int,Field(gt=1900)]

configSchemaGeneros = Annotated[str,Field(min_length=4)]

configSchemasEstados = Annotated[bool,Field( description= "disponibilidad")]



path_id=Annotated[int,Path(gt=0, description="id mayor a 0")]



class PeliculasSchemas(BaseModel):

    id : configSchemasID
    titulo:configSchemaTitulos
    año : configSchemaAño
    genero : configSchemaGeneros
    activo : configSchemasEstados


class PeliculaCreateUpdateSchemas(BaseModel):
    titulo:configSchemaTitulos
    año : configSchemaAño
    genero : configSchemaGeneros
    activo : configSchemasEstados




not_found = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "pelicula no encontrada",
                }
            }
        },
    },
}


app = FastAPI()



@app.get("/pelicula", response_model=list[PeliculasSchemas])
async def mostrar_pelicula(
        genero: str = Query(description="porque genero desea filtrar?",default=None),
        ordenar: str =Query(description="porq desea ordenar por año o titulo",default=None)
):
    peliculas_filtradas=peliculas

    if genero:
        peliculas_filtradas=[
        pelicula for pelicula in peliculas
        if pelicula["genero"].lower()==genero.lower()]
    
    if ordenar:
        if ordenar == "titulo":
            peliculas_filtradas=sorted(peliculas_filtradas,key=lambda x:x["titulo"])
        elif ordenar == "año":
            peliculas_filtradas=sorted(peliculas_filtradas,key=lambda x:x["año"])

    return peliculas_filtradas



@app.get("/pelicula/{id}", response_model=PeliculasSchemas,responses= not_found)
async def pelicula_by_id( id:path_id):
    for pelicula in peliculas:
        if pelicula["id"]==id:
            return pelicula
    raise HTTPException(status_code=404,detail="id no encontrado")



@app.post("/pelicula",response_model=PeliculasSchemas)
async def agregar_pelicula(pelicula:PeliculaCreateUpdateSchemas):

    id=max(peliculas,key=lambda x:x["id"])["id"]+1

    nueva_pelicula=(pelicula.model_dump())

    nueva_pelicula["id"]=id

    peliculas.append(nueva_pelicula)
    
    return nueva_pelicula      



@app.put("/pelicula/{id}",response_model=PeliculasSchemas,responses=not_found)
async def modificar_pelicula(
    id:path_id,
    pelicula_editar:PeliculaCreateUpdateSchemas
    ):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            pelicula["titulo"]=pelicula_editar.titulo
            pelicula["año"]=pelicula_editar.año
            pelicula["genero"]=pelicula_editar.genero
            pelicula["activo"]=pelicula_editar.activo
            

            return pelicula
        
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")



@app.delete("/pelicula/{id}", responses=not_found)
async def borrar_pelicula(
    id: path_id,
    logico:Annotated[bool,Query(description="mantener registro?")]=True
    ):

    for pelicula in peliculas:
        if pelicula["id"]==id:
            if logico:
                pelicula["activo"]=False            
            else:
                peliculas.remove(pelicula)
            return {"detail":"borrado correctamente","peliculas":peliculas}
                    
    raise HTTPException(status_code=404,detail="no encontrado")
