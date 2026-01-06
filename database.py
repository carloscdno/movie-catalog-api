from pathlib import Path

# Nombre por defecto del archivo donde guardaremos las películas
DEFAULT_DB_FILE = "movies.json"

# Usamos pathlib para construir una ruta segura
# Este comando genera una ruta absoluta al archivo movies.json,
# colocándolo en el mismo nivel que este archivo database.py

DB_PATH = Path(__file__).with_name(DEFAULT_DB_FILE)

def get_db_path() -> Path:
    """Devuelve la ruta absoluta del archivo de base de datos.
    Con esto centralizamos la ubicación del JSON y evitamos errores de rutas relativas.
    """
    return DB_PATH

def ensure_db_file_exists() -> Path:
    """
    Crea el archivo movies.json si no existe.
    No escribe datos todavía, solo garantiza que el archivo esté presente.
    """
    path = get_db_path()

    if not path.exists():
        # Aseguramos que exista la carpeta donde estará el archivo
        path.parent.mkdir(parents=True, exist_ok=True)
        # Creamos el archivo vacío
        path.touch(exist_ok=True)

    return path

class MovieDatabase:
    """
    Clase que actúa como base de datos en memoria para el catálogo de películas.
    Por ahora, solo mantiene los datos temporalmente mientras la app está activa.
    """
    
    def __init__(self):
        # Diccionario interno para almacenar las películas
        self.movies: dict[int, dict] = {}
        self.next_id: int = 1  # ID incremental para nuevas películas
        
    def add_movie(self, movie_data: dict) -> dict:
        """
        Agrega una nueva película al catálogo.
        Aún no guarda en JSON (solo memoria).
        """
        movie_id = self.next_id
        self.movies[movie_id] = {"id": movie_id, **movie_data}
        self.next_id += 1
        return self.movies[movie_id]
    
    def list_movies(self) -> list[dict]:
        """Devuelve la lista de todas las películas en memoria."""
        return list(self.movies.values())
    
    def get_movie(self, movie_id: int) -> dict | None:  
        """Devuelve una película específica por ID (o None si no existe)."""
        return self.movies.get(movie_id)