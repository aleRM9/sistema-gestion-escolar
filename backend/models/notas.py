from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import datetime

from .base import Base

# Equivalente a tabla 'notas'
class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (
    CheckConstraint(
        "calificacion >= 0 AND calificacion <= 20", # Nota entre 0 y 20
        name="ck_notas_calificacion",
    ),
        CheckConstraint("lapso BETWEEN 1 AND 3", name="notas_lapso_check"), # Lapso entre 1 y 3
        UniqueConstraint("inscripcion_id", "lapso", name="nota_unica"), # Nota única por lapso
    )

    nota_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inscripcion_id: Mapped[int] = mapped_column(
        ForeignKey("inscripciones.inscripcion_id", ondelete="CASCADE"), nullable=False
    )
    calificacion: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    lapso: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

  


