from pydantic import BaseModel, ConfigDict, Field


class InscripcionCreate(BaseModel):
    materia_id: int = Field(gt=0)
    alumno_id: int = Field(gt=0)
    curso_id: int = Field(gt=0)
    
    
class InscripcionUpdate(BaseModel):
    materia_id: int | None = Field(default=None, gt=0)
    alumno_id: int | None = Field(default=None, gt=0)
    curso_id: int | None = Field(default=None,gt=0)


class InscripcionRead(BaseModel):
    inscripcion_id: int
    materia_id: int
    alumno_id: int
    curso_id: int

    model_config = ConfigDict(from_attributes=True)