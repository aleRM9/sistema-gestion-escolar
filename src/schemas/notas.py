from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class NotaCreate(BaseModel):
    # CAMBIO: se recibe inscripcion_id, nombre de la FK obligatoria en notas,
    # para asociar cada calificación con su inscripción.
    inscripcion_id: int = Field(gt=0)
    # CAMBIO: precisión y escala coinciden con DECIMAL(4,2) del SQL.
    calificacion: Decimal = Field(ge=0, le=20, max_digits=4, decimal_places=2)
    # CAMBIO (BUG): antes era gt=1, lo que RECHAZABA el lapso 1 (solo dejaba
    # 2 y 3). Ahora ge=1: lapsos permitidos 1, 2 y 3.
    lapso: int = Field(ge=1, le=3, description="El lapso solo puede ser 1, 2 o 3")


class NotaUpdate(BaseModel):
    calificacion: Decimal | None = Field(
        default=None, ge=0, le=20, max_digits=4, decimal_places=2
    )
    # CAMBIO (BUG): el tipo era "int" con default=None (inconsistente) y
    # también tenía gt=1. Ahora es "int | None" con ge=1.
    lapso: int | None = Field(
        default=None, ge=1, le=3, description="El lapso solo puede ser 1, 2 o 3"
    )


class NotaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # CAMBIO: nombres alineados a la BD; se agregó fecha_registro a la respuesta.
    nota_id: int
    inscripcion_id: int
    calificacion: Decimal
    lapso: int
    fecha_registro: datetime | None = None

    # CAMBIO: sin esto, pydantic v2 entrega el Decimal como texto ("15.50")
    # en el JSON; así sale como número (15.5).
    @field_serializer("calificacion")
    def _nota_como_numero(self, valor: Decimal) -> float:
        return float(valor)
