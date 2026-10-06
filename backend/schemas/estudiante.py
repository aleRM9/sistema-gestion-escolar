from pydantic import BaseModel
from datetime import date

class EstudianteCrear(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    correo: str


class EstudianteRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    cedula: str
    correo: str

    class Config:
        from_attributes = True