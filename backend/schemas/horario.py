from pydantic import BaseModel
from datetime import date

class HorarioRespuesta(BaseModel):
    id: int
    curso: str
    dia: str
    hora_inicio: str
    hora_fin: str

    class Config:
        from_attributes = True