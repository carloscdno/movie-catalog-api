from fastapi import FastAPI
from config import settings

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