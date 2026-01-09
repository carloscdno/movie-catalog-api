from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import date

class MovieBase(BaseModel):
    """Modelo base para una película."""
    # Titulo de la pelicula (obligatorio)
    title: str = Field(..., min_length=1, max_length=200, description="Título de la película")
    
    # Director de la pelicula (obligatorio)
    director: str = Field(..., min_length=1, max_length=100, description="Director o Directora")
    
    # Año de estreno (dentro de un rango realista)
    year: int = Field(None, ge=1880, le=2030, description="Año de estreno")
    
    # Genero principal. Ejemplos: Acción, Comedia, Drama, Ciencia Ficción, etc.
    genre: str = Field(..., min_length=1, max_length=50, description="Género principal")
    
    # Duración en minutos (opcional)
    duration: Optional[int] = Field(None, ge=1, le=600, description="Duración en minutos")
    
    # Calificación (opcional, escala 0-10)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0, description="Calificación promedio")
    
    # Breve descripcion o sinopsis (opcional)
    description: Optional[str] = Field(None, max_length=1000, description="Breve sinopsis de la película")
    
    # Precio de alquiler o compra (opcional). Si existe debe ser mayor o igual a 0.
    price: Optional[float] = Field(None, ge=0.0, description="Precio de venta o renta")
    
    # Indica si la pelicula ya fue vista
    is_watched: bool = Field(default=False, description="Indica si la película ya fue vista")
    
    # --- Validaciones personalizadas ---
    @field_validator('year')
    @classmethod
    def validate_year(cls, value: int) -> int:
        """Valida que el año sea realista."""
        if value < 1880:
            raise ValueError("El año debe ser mayor o igual a 1880 (inicio del cine moderno).")
        if value > date.today().year + 5:
            raise ValueError("El año no puede ser más de 5 años en el futuro.")
        return value
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        """El título no puede estar vacío ni solo contener espacios."""
        if not value.strip():
            raise ValueError("El título no puede estar vacío o solo con espacios.")
        return value.strip()

    
class MovieCreate(MovieBase):
    """Modelo para crear una nueva película."""
    pass

# Todos los valores son opcionales para actualizaciones parciales
class MovieUpdate(BaseModel):
    """Modelo usado para actualizar parcialmente una película existente."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    director: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1880, le=2030)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    duration: Optional[int] = Field(None, ge=1, le=600)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, ge=0.0)
    is_watched: Optional[bool] = None

class MovieResponse(MovieBase):
    """Modelo para la respuesta de una película, incluye el ID."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje breve para el cliente")
    data: Optional[dict] = Field(None, description="Película devuelta [dict] o None si no aplica") 

class MovieListResponse(BaseModel):
    """Modelo para la respuesta al listar películas."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje breve para el cliente")
    data: List[dict] = Field(..., default_factory=list, description="Listado de peliculas en este paso")
    total: int = Field(..., description="Número total de películas en el catálogo")
    