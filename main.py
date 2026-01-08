from fastapi import FastAPI
from config import settings

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


# Montamos rutas del router en /api/v1
app.include_router(movies.router, prefix="/api/v1")