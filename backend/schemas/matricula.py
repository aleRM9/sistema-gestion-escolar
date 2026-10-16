from pydantic import BaseModel
from datetime import date

class MatriculaCrear(BaseModel):
    estudiante_id: int
    curso_id: int


class MatriculaRespuesta(BaseModel):
    id: int
    estudiante_id: int
    curso_id: int
    fecha_matricula: date

    class Config:
        from_attributes = True
