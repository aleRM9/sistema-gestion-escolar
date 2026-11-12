from pydantic import BaseModel, ConfigDict, Field

PATRON_PERIODO = r"^\d{4}-\d{4}$"

# Crear inscripción
class InscripcionCreate(BaseModel):
    materia_id: int = Field(gt=0)
    alumno_id: int = Field(gt=0)
    curso_id: int = Field(gt=0)

# Actualizar inscripción
class InscripcionUpdate(BaseModel):
    materia_id: int | None = Field(default=None, gt=0)
    alumno_id: int | None = Field(default=None, gt=0)
    curso_id: int | None = Field(default=None, gt=0)

# Lectura de inscripción
class InscripcionRead(BaseModel):
    inscripcion_id: int
    alumno_id: int
    materia_id: int
    curso_id: int
    
    # Permite que Pydantic lea directamente objetos de SQLAlchemy/ORM
    model_config = ConfigDict(from_attributes=True)