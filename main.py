#API REST: representational state transfer / Interfaz de programación de aplicaciones para compartir recursos
# FastAPI: Framework para crear APIs con Python

from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable donde tendrá todas las caracteristicas de una API REST
app = FastAPI()

# Acá definimos el modelo
class Curso(BaseModel):

    id: Optional[str] = None  # ID opcional, se generará automáticamente
    nombre: str
    duracion: Optional[str] = None  # Duración en horas
    nivel: str
    duración: int


# Simularemos una base de datos

cursos_db = []

# CRUD_ READ (lectura) GET ALL: Leeremos todos los cursos que haya en la db

@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: CREATE (escribir) POST: Agregaremos un nuevo recurso a la base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4())  # Generamos un ID único con uuid para el curso
    cursos_db.append(curso)
    return curso

# CRUD: Read (lectura) GET (individual): Leeremos el curso que coincida con el ID que pedimos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto por el generador
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD: Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    # Actualizamos los campos del curso
    curso_actualizado.id = curso.id  # Mantenemos el ID original
    index = cursos_db.index(curso) # Buscamos el indice exacto donde está el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete (borrado/baja) DELETE: Eliominaremos un recurso que coincida con el ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso


# Para correr la API, ejecutamos el siguiente comando en la terminal:
# uvicorn main:app --reload