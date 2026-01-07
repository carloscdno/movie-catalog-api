from fastapi import FastAPI
from config import settings
from models import MovieCreate
import movies

# Creamos la instancia de la aplicación FastAPI
app = FastAPI(
    title = settings.app_name,
    version= settings.app_version,
    debug = settings.debug,
)

# Definimos el endpoint raíz
@app.get("/")
async def root():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}

# POST endpoint para crear una nueva película
@app.post("/movies/")
async def create_movie(payload: MovieCreate):
    """Crea una nueva película en el catálogo."""
    return {
        "success": True,
        "message": "Película recibida (aun sin guardar)",
        "data": payload.model_dump()
        }

# Montamos rutas del router en /api/v1
app.include_router(movies.router, prefix="/api/v1")