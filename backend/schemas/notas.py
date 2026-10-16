from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

# Creación de nota
class NotaCreate(BaseModel):
    inscripcion_id: int = Field(gt=0)
    calificacion: Decimal = Field(ge=0, le=20, max_digits=4, decimal_places=2)
    lapso: int = Field(ge=1, le=3, description="El lapso solo puede ser 1, 2 o 3")

# Actualización de nota
class NotaUpdate(BaseModel):
    calificacion: Decimal | None = Field(
        default=None, ge=0, le=20, max_digits=4, decimal_places=2
    )
    lapso: int | None = Field(
        default=None, ge=1, le=3, description="El lapso solo puede ser 1, 2 o 3"
    )

# Lectura de nota
class NotaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nota_id: int
    inscripcion_id: int
    calificacion: Decimal
    lapso: int
    fecha_registro: datetime | None = None

    @field_serializer("calificacion")
    def _nota_como_numero(self, valor: Decimal) -> float:
        return float(valor)
