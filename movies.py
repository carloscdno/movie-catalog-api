from fastapi import APIRouter
from database import MovieDatabase

# Creamos un router modular para las rutas de peliculas
router = APIRouter(tags=["movies"])

# Instancia de la base de datos de películas
db = MovieDatabase()

@router.get("/movies/")
def list_movies():
    """ Endpoint para listar todas las películas.
    Retorna una lista de diccionarios con los datos actuales del catálogo.
    """
    return db.list_movies()

