from fastapi import APIRouter, HTTPException
from database import MovieDatabase

# Creamos un router modular para las rutas de peliculas
router = APIRouter(tags=["movies"])

# Instancia de la base de datos de películas
db = MovieDatabase()

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