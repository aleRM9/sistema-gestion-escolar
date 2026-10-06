from sqlalchemy import Integer, Numeric, String, Date, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from .base import Base

class Pago(Base):
    __tablename__ = "pagos"

    __table_args__ = (
        CheckConstraint("monto > 0", name="ck_pagos_monto"),
    )
    pago_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_pago: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    concepto: Mapped[str] = mapped_column(String(100), nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    profesor_id: Mapped[int] = mapped_column(
        ForeignKey("profesores.profesor_id"), nullable=False
    )