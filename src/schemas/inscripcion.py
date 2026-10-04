from pydantic import BaseModel, ConfigDict, Field

# CAMBIO: la regex valida el periodo del curso en los endpoints de reportes.
PATRON_PERIODO = r"^\d{4}-\d{4}$"


class InscripcionCreate(BaseModel):
    # CAMBIO: curso_id es obligatorio en SQL; periodo y sección se obtienen
    # de cursos y no son columnas de inscripciones.
    materia_id: int = Field(gt=0)
    alumno_id: int = Field(gt=0)
    curso_id: int = Field(gt=0)


class InscripcionUpdate(BaseModel):
    materia_id: int | None = Field(default=None, gt=0)
    alumno_id: int | None = Field(default=None, gt=0)
    curso_id: int | None = Field(default=None, gt=0)


class InscripcionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # CAMBIO: la respuesta expone curso_id; periodo y sección se consultan en
    # cursos, pues no son columnas de inscripciones.
    inscripcion_id: int
    materia_id: int
    alumno_id: int
    curso_id: int
