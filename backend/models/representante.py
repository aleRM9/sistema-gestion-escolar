from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .alumno import Alumno

# Equivalente a tabla 'representantes'
class Representante(Base):
    __tablename__ = "representantes"

    representante_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    cedula: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    correo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    direccion: Mapped[str] = mapped_column(String(200), nullable=False)
    # Lo mantienen los triggers (recibos nuevos suman, pagos restan). Puede ser negativo (saldo a favor)
    monto_deuda: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, server_default="0"
    )

    alumnos: Mapped[list["Alumno"]] = relationship(back_populates="representante")
