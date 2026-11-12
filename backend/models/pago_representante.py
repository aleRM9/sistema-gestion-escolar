from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from decimal import Decimal

from .base import Base
from .enums import MetodoPago, metodo_pago_enum


# Equivalente a tabla 'pagos_representantes'
class PagoRepresentante(Base):
    __tablename__ = "pagos_representantes"
    __table_args__ = (
        CheckConstraint("monto > 0", name="ck_pagos_representantes_monto"),
    )

    pago_representante_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monto: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    fecha_pago: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    metodo_pago: Mapped[MetodoPago] = mapped_column(metodo_pago_enum, nullable=False)
    referencia_pago: Mapped[str] = mapped_column(String(100), nullable=False)
    representante_id: Mapped[int] = mapped_column(
        ForeignKey("representantes.representante_id", ondelete="RESTRICT"),
        nullable=False,
    )
