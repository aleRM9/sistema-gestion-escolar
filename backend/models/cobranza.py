from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from .base import Base


class Cobranza(Base):
    __tablename__ = "cobranzas"
    __table_args__ = (
        CheckConstraint("monto > 0", name="ck_cobranzas_monto"),
        CheckConstraint(
            "estado IN ('pagado', 'por cobrar')",
            name="ck_cobranzas_estado"
        ),
    )

    cobranza_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    concepto: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_vencimiento: Mapped[date] = mapped_column(Date, nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(15), nullable=False)
    alumno_id: Mapped[int] = mapped_column(
        ForeignKey("alumnos.alumno_id"), nullable=False
    )
    representante_id: Mapped[int] = mapped_column(
        ForeignKey("representantes.representante_id"), nullable=False
    )
