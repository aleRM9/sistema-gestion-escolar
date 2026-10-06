from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class NotaCreate(BaseModel):
    calificacion: Decimal = Field(ge=0, le=20)
    lapso: int = Field(gt=1, le=3)
    

class NotaUpdate(BaseModel):
    calificacion: Decimal | None = Field(default=None, ge=0, le=20)
    lapso: int = Field(default=None, gt=1, le=3, description="El lapso solo puede ser 1, 2 o 3")



class NotaRead(BaseModel):
    nota_id: int
    inscripcion_id: int
    calificacion: Decimal
    lapso: int

    model_config = ConfigDict(from_attributes=True)