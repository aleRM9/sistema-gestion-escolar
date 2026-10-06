from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base


class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (
        CheckConstraint(
            "calificacion >= 0 AND calificacion <= 20",
            name="ck_notas_calificacion",
        ),
    )

    nota_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    inscripcion_id: Mapped[int] = mapped_column(
        ForeignKey("inscripciones.inscripcion_id"),
        nullable=False,
        index=True,
    )
    calificacion: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    lapso: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default= datetime.now)