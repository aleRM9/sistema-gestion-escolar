from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import datetime

from .base import Base


# Equivalente a tabla 'auditorias_notas'

class AuditoriaNota(Base):
    __tablename__ = "auditorias_notas"

    auditoria_nota_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nota_id: Mapped[int] = mapped_column(
        ForeignKey("notas.nota_id", ondelete="RESTRICT"), nullable=False
    )
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.usuario_id", ondelete="RESTRICT"), nullable=False
    )
    fecha_cambio: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    calificacion_anterior: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    calificacion_modificada: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
