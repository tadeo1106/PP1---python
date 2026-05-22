from fastapi import FastAPI,Query,Path,Body
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

peliculas = [
    {"id": 1, "titulo": "Inception", "año": 2010, "genero": "ciencia ficcion","activo":True},
    {"id": 2, "titulo": "The Dark Knight", "año": 2008, "genero": "accion", "activo":True},
    {"id": 3, "titulo": "Titanic", "año": 1997, "genero": "romance","activo":True},
]


configSchemasID=Annotated[int , Field(gt=0,description='id del articulo')]

configSchemaTitulos=Annotated[str,Field(max_length=40)]

configSchemaAño = Annotated[int,Field(gt=1900)]

configSchemaGeneros = Annotated[str,Field(min_length=4)]

configSchemasEstados = Annotated[bool,Field( description= 'disponibilidad')]



pathID=Annotated[int,Path(gt=0, description="id mayor a 0")]

QueryEstado=Annotated[bool,Query(description="mantener registro",default=True)]



class PeliculasSchemas(BaseModel):

    id : configSchemasID
    titulo:configSchemaTitulos
    año : configSchemaAño
    genero : configSchemaGeneros
    activo : configSchemasEstados


class PeliculaUpdateSchemas(BaseModel):

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
async def filtrar_genero(
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

    return peliculas_filtradas if peliculas_filtradas else {"detail":"no encontrado"}



@app.get("/pelicula/{id}", response_model=PeliculasSchemas, responses= not_found)
async def pelicula_by_id( id:pathID):

    resultado=[pelicula for pelicula in peliculas
            if pelicula["id"]==id]
    if resultado:
        return resultado
    raise HTTPException(status_code=404,detail='id no encontraado')



@app.post("/pelicula")
async def agregar_pelicula(
    titulo: configSchemaTitulos,
    año: configSchemaAño,
    genero: configSchemaGeneros):   


    if not titulo.strip() or not genero.strip():
        return {"detail": "no puede estar vacio"}
    
    id=max(peliculas,key=lambda x:x["id"])["id"]+1


    pelicula={
        "id":id,
        "titulo":titulo,
        "año": año,
        "genero":genero}
    
    peliculas.append(pelicula)

    return {"detail":"todo correcto","pelicula añadida":pelicula}        



@app.put("/pelicula/{id}",response_model=PeliculasSchemas,responses=not_found)
async def modificar_pelicula(
    id:pathID,
    pelicula_editar=PeliculaUpdateSchemas
    ):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            pelicula["id"]=pelicula_editar.titulo
            pelicula["titulo"]=pelicula_editar.titulo
            pelicula["año"]=pelicula_editar.año
            pelicula["genero"]=pelicula_editar.genero
            

            return {"detail":"modificacion echas correctamente","pelicula modificada":pelicula}
        
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")



@app.delete("/pelicula/{id}")
async def borrar_pelicula(
    id: pathID,
    logico: QueryEstado
    ):

    for pelicula in peliculas:
        if pelicula["id"]==id:
            if logico:
                pelicula["activo"]=False            
            else:
                peliculas.remove(pelicula)
            return {"detail":"borrado correctamente","peliculas":peliculas}
                    
        return{"detail":"id no encontrado"}
