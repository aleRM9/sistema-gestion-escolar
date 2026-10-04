from pydantic import BaseModel, ConfigDict, Field

PATRON_PERIODO = r"^\d{4}-\d{4}$"


class InscripcionCreate(BaseModel):
    materia_id: int = Field(gt=0)
    alumno_id: int = Field(gt=0)
    curso_id: int = Field(gt=0)


class InscripcionUpdate(BaseModel):
    materia_id: int | None = Field(default=None, gt=0)
    alumno_id: int | None = Field(default=None, gt=0)
    curso_id: int | None = Field(default=None, gt=0)


class InscripcionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inscripcion_id: int
    materia_id: int
    alumno_id: int
    curso_id: int
