from fastapi import APIRouter, HTTPException
from database import MovieDatabase
from models import MovieCreate, MovieUpdate, MovieResponse, MovieListResponse

# Creamos un router modular para las rutas de peliculas
router = APIRouter(tags=["movies"])

# Instancia de la base de datos de películas
db = MovieDatabase()

# Endpoint para crear una nueva película
@router.post("/movies/", status_code=201, response_model=MovieResponse)
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
@router.get("/movies/", response_model=MovieListResponse)
def list_movies():
    """ Endpoint para listar todas las películas.
    Retorna una lista de diccionarios con los datos actuales del catálogo.
    """
    items = db.list_movies()
    return {
        "success": True,
        "message": f"Se encontraron {len(items)} películas en el catálogo",
        "data": items,
        "total": len(items)
    }

# Endpoint para obtener una película por su ID
@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    """Devuelve una película por su ID.
    - Si existe, retorna el objeto (dict) con sus campos.
    - Si no existe, lanza un 404 con un mensaje claro.
    """
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Película con ID {movie_id} no encontrada")
    return {
        "success": True,
        "message": "Película encontrada correctamente",
        "data": movie
    }

# Endpoint para actualizar pelicula existente
@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, changes: MovieUpdate):
    """
    Actualiza los datos de una película existente.
    - Busca el ID.
    - Aplica solo los campos enviados.
    - Guarda los cambios en el JSON.
    """
    # 1) Buscamos la pelicula
    movie = db.get_movie(movie_id)
    if movie is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Película con ID {movie_id} no encontrada"
            )
    
    # 2) Tomar únicamente los campos provistos en el body
    update_data = changes.model_dump(exclude_unset=True)
    
    # 3) Aplicar los cambios en memoria
    movie.update(update_data)
    db.movies[movie_id] = movie
    
    # 4) Guardar los cambios en el archivo JSON
    db.save_data()
    
    return {
        "success": True,
        "message": f"Película con ID {movie_id} actualizada correctamente",
        "data": movie
    }

# Endpoint para eliminar una película por su ID
@router.delete("/movies/{movie_id}", response_model=MovieResponse)
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
        "message": f"Película con ID {movie_id} eliminada correctamente",
        "data": None
    }