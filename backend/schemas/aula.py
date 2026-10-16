from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class AulaCreate(BaseModel):
    codigo: str = Field(..., max_length=10, description="Código único del aula (Ej. A-101)")
    ubicacion: str = Field(..., max_length=100, description="Ubicación física del aula")

class AulaUpdate(BaseModel):
    codigo: Optional[str] = Field(default=None, max_length=10)
    ubicacion: Optional[str] = Field(default=None, max_length=100)

class AulaRead(BaseModel):
    aula_id: int
    codigo: str
    ubicacion: str

    # Permite a Pydantic leer los datos directamente desde el modelo de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
