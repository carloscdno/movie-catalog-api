"""
Persistencia con JSON (fase 1):
- Prepara y resuelve la ruta del archivo de datos (movies.json).
- Crea el archivo si no existe.
- Implementa carga (load_data) y guardado (save_data) del catálogo.
- Mantiene la estructura en memoria como dicts simples (aún no Pydantic Models).

"""
from pathlib import Path
import json
from typing import List, Dict, Optional

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

def ensure_db_file_exists(path: Optional[Path] = None) -> Path:
    """
    Crea el archivo movies.json si no existe.
    Si no se pasa path, usa la ruta por defecto.
    """
    if path is None:
        path = get_db_path()
    

    if not path.exists():
        # Aseguramos que exista la carpeta donde estará el archivo
        path.parent.mkdir(parents=True, exist_ok=True)
        # Creamos el archivo vacío
        path.touch(exist_ok=True)
        # Inicializamos con una estructura minima valida
        path.write_text(json.dumps({"movies": [], "next_id": 1}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

class MovieDatabase:
    """
    Clase que actúa como base de datos en memoria para el catálogo de películas.
    Por ahora, solo mantiene los datos temporalmente mientras la app está activa.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        # Diccionario interno para almacenar las películas
        self.movies: Dict[int, dict] = {}
        self.next_id: int = 1  # ID incremental para nuevas películas
        
        # Ruta del archivo; si no te pasan una, usamos la por defecto
        self.file_path = Path(file_path) if file_path else get_db_path()
        ensure_db_file_exists(self.file_path) # Garantiza que el archivo exista con estructura básica o le pasamos la ruta
        self.load_data()        # Hidrata la memoria con lo que haya en disco
        
    # ---------------------------------------------------------------------
    # Persistencia
    # ---------------------------------------------------------------------
    
    def load_data(self) -> None:
        """
        Lee el archivo JSON y carga las películas en memoria.
        Espera un JSON con llaves: "movies" (lista) y "next_id" (int).
        Si el archivo está vacío o corrupto, re-inicializa estructura.
        """
        try:
            text = self.file_path.read_text(encoding="utf-8").strip()
            if not text:
                # Si está vacío, inicializamos estructura básica
                self.movies = {}
                self.next_id = 1
                self.save_data()
                return
            
            data = json.loads(text)
            
            # Validación mínima de estructura
            movies_list: List[Dict] = data.get("movies", [])
            next_id_val: int = data.get("next_id", 1)
            
            # Cargar en memoria como dict {id: dict_movie}
            self.movies = {}
            for item in movies_list:
                # Validación básica de que tenga id
                movie_id = item.get("id")
                if isinstance(movie_id, int):
                    self.movies[movie_id] = item
            
            # Si no viene next_id, lo calculamos como max_id + 1
            if isinstance(next_id_val, int) and next_id_val > 0:
                self.next_id = next_id_val
            else:
                self.next_id = (max(self.movies.keys()) + 1) if self.movies else 1
            
        except Exception as e:
            # Si algo falla (JSON malformado, etc.), re-inicializamos seguro
            print(f"[MovieDatabase.load_data] Error al cargar datos: {e}")
            self.movies = {}
            self.next_id = 1
            self.save_data()
    
    def save_data(self) -> None:
        """
        Vuelca el estado actual a disco en formato JSON.
        Estructura:
        {
          "movies": [ {...}, {...} ],
          "next_id": <int>
        }
        """

        try:
            data = {
                "movies": list(self.movies.values()),
                "next_id": self.next_id
            }

            self.file_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )

        except Exception as e:
            print(f"[MovieDatabase.save_data] Error al guardar datos: {e}")

            # Re-lanzar en escenarios reales si se quiere manejar afuera
            # raise

    # ---------------------------------------------------------------------
    # Operaciones en memoria (con persistencia mínima en add)
    # ---------------------------------------------------------------------
        
    def add_movie(self, movie_data: dict) -> dict:
        """
        Agrega una nueva película al catálogo.
        Persistencia: guarda inmediatamente tras agregar.
        """
        movie_id = self.next_id
        record = {"id": movie_id, **movie_data}
        self.movies[movie_id] = record
        self.next_id += 1
        
        # Guardamos tras cada cambio
        self.save_data()
        return record
    
    def list_movies(self) -> list[dict]:
        """Devuelve la lista de todas las películas en memoria."""
        return list(self.movies.values())
    
    def get_movie(self, movie_id: int) -> dict | None:  
        """Devuelve una película específica por ID (o None si no existe)."""
        return self.movies.get(movie_id)