from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Auditoria(Base):
    __tablename__ = "Auditoria"

    auditoria_notas_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nota_id: Mapped[int] = mapped_column(
        ForeignKey("notas.nota_id")
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.usuario_id")
    )
    fecha_cambio: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    calificacion_anterior: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    calificacion_modificada: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
