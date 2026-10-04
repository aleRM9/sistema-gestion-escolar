from datetime import date

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    alumno_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    cedula: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    fecha_nacimiento: Mapped[date] = mapped_column(nullable=False)
    representante_id: Mapped[int] = mapped_column(
        ForeignKey("representantes.representante_id", ondelete="RESTRICT"),
        nullable=False,
    )
