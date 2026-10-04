from pydantic import BaseModel, ConfigDict, Field


class MateriaCreate(BaseModel):
    # CAMBIO: str_strip_whitespace quita espacios al inicio/fin, para que
    # " MAT-1 " y "MAT-1" no cuenten como códigos distintos.
    model_config = ConfigDict(str_strip_whitespace=True)

    # CAMBIO: el máximo coincide con varchar(50) de la tabla materias.
    nombre: str = Field(min_length=1, max_length=50)
    codigo: str = Field(min_length=1, max_length=10)  # Ej: 'MAT-1', 'FIS-4'
    grado: int = Field(ge=1, le=5)


class MateriaUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    # CAMBIO: las actualizaciones respetan el mismo varchar(50) que las altas.
    nombre: str | None = Field(default=None, min_length=1, max_length=50)
    codigo: str | None = Field(default=None, min_length=1, max_length=10)
    grado: int | None = Field(default=None, ge=1, le=5)


class MateriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    materia_id: int
    nombre: str
    codigo: str
    grado: int
