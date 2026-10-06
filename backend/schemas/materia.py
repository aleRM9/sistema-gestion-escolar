from pydantic import BaseModel, ConfigDict, Field


class MateriaCreate(BaseModel):
    nombre: str = Field(max_length=100)
    grado: int = Field(ge=1, le=5)
    codigo: str = Field(max_length=10)


class MateriaUpdate(BaseModel):
    nombre: str | None = Field(default=None, max_length=100)
    grado: int | None = Field(default=None, ge=1, le=5)
    codigo: str | None = Field(default=None, max_length=10)


class MateriaRead(BaseModel):
    materia_id: int
    nombre: str
    grado: int
    codigo: str

    model_config = ConfigDict(from_attributes=True)