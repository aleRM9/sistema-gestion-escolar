from datetime import datetime
from decimal import Decimal

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

from .base import Base


class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (
        CheckConstraint("calificacion BETWEEN 0 AND 20", name="notas_calificacion_check"),
        CheckConstraint("lapso BETWEEN 1 AND 3", name="notas_lapso_check"),
        UniqueConstraint("inscripcion_id", "lapso", name="nota_unica"),
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
