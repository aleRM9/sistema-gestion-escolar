from pydantic import BaseModel, ConfigDict, Field

# Creación de materias
class MateriaCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1, max_length=50)
    codigo: str = Field(min_length=1, max_length=10)
    grado: int = Field(ge=1, le=5)

# Actualización de materias
class MateriaUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str | None = Field(default=None, min_length=1, max_length=50)
    codigo: str | None = Field(default=None, min_length=1, max_length=10)
    grado: int | None = Field(default=None, ge=1, le=5)

# Lectura de materias
class MateriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    materia_id: int
    nombre: str
    codigo: str
    grado: int

