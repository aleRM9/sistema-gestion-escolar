from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from decimal import Decimal

from .base import Base
from .enums import EstadoRecibo, estado_recibo_enum


# Equivalente a tabla 'recibos_cobro' (antes 'cobranzas')
class ReciboCobro(Base):
    __tablename__ = "recibos_cobro"
    __table_args__ = (
        CheckConstraint("monto_total > 0", name="ck_recibos_cobro_monto_total"),
        CheckConstraint("monto_pagado >= 0", name="ck_recibos_cobro_monto_pagado"),
        CheckConstraint("monto_pagado <= monto_total", name="pago_no_excede"),
    )

    recibo_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concepto: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_generacion: Mapped[date] = mapped_column(
        Date, nullable=False, server_default=func.current_date()
    )
    monto_total: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    monto_pagado: Mapped[Decimal] = mapped_column(
        Numeric(8, 2), nullable=False, server_default="0"
    )

    estado: Mapped[EstadoRecibo] = mapped_column(
        estado_recibo_enum, nullable=False, server_default="pendiente"
    )
    alumno_id: Mapped[int] = mapped_column(
        ForeignKey("alumnos.alumno_id", ondelete="RESTRICT"), nullable=False
    )
