from fastapi import FastAPI

# Creamos la instancia de la aplicación FastAPI
app = FastAPI(
    title="Movie Catalog API",
    version="0.1.0",
    description="API básica para gestionar un catálogo de películas."
)

# Definimos el endpoint raíz
@app.get("/")
def read_root():
    """Endpoint principal de la API."""
    return {"message": "Bienvenido al Catálogo de Películas 🎬"}