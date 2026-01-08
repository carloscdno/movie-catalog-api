from fastapi import APIRouter, HTTPException
from database import MovieDatabase
from models import MovieCreate # Nueva importación

# Creamos un router modular para las rutas de peliculas
router = APIRouter(tags=["movies"])

# Instancia de la base de datos de películas
db = MovieDatabase()

# Endpoint para crear una nueva película
@router.post("/movies/", status_code=201)
def create_movie(movie: MovieCreate):
    """ Crea una nueva película en el catálogo.
    - Valida campos mínimos requeridos.
    - Asigna un ID incremental automáticamente.
    - Guarda en memoria y persiste en el archivo JSON.
    """
    # ---------------------------------------------------------------------
    # Validacion Manual (antes de usar Pydantic)
    # ---------------------------------------------------------------------
    #required = ["title", "director", "year", "genre"]
    
    #missing_fields = [field for field in required if field not in payload]
    #if missing_fields:
    #    raise HTTPException(
    #        status_code=400,
    #        detail=f"Faltan campos requeridos: {', '.join(missing_fields)}"
    #    )
    # Crear la película en memoria
    #db.add_movie(payload)
    
    # Guardar en disco
    #db.save_data()
    
    # ---------------------------------------------------------------------
    # Usando Pydantic para validacion automática
    # ---------------------------------------------------------------------
    # Convertimos el modelo validado a dict
    data = movie.model_dump()
    
    # Guardado en memoria y persistencia
    created = db.add_movie(data)
   
    
    return {
        "success": True,
        "message": "Película creada correctamente",
        "data": created
    }

# Endpoint para listar todas las películas
@router.get("/movies/")
def list_movies():
    """ Endpoint para listar todas las películas.
    Retorna una lista de diccionarios con los datos actuales del catálogo.
    """
    return db.list_movies()

# Endpoint para obtener una película por su ID
@router.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    """Devuelve una película por su ID.
    - Si existe, retorna el objeto (dict) con sus campos.
    - Si no existe, lanza un 404 con un mensaje claro.
    """
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    return movie

# Endpoint para actualizar pelicula existente
@router.put("/movies/{movie_id}")
def update_movie(movie_id: int, payload: dict):
    """
    Actualiza los datos de una película existente.
    - Busca el ID.
    - Aplica solo los campos enviados.
    - Guarda los cambios en el JSON.
    """
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    
    # Actualizamos solo los campos presentes en el payload
    movie.update(payload)
    db.movies[movie_id] = movie
    db.save_data()
    
    return {
        "success": True,
        "message": f"Película con ID {movie_id} actualizada correctamente",
        "data": movie
    }

# Endpoint para eliminar una película por su ID
@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    """
    Elimina una película por ID.
    - Si existe: la borra del diccionario en memoria y persiste el cambio en JSON.
    - Si no existe: responde 404.
    """
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    
    # Borrado en memoria y persistencia
    del db.movies[movie_id]
    db.save_data()
    
    return {
        "success": True,
        "message": f"Película con ID {movie_id} eliminada correctamente"
    }