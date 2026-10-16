from sqlalchemy import CheckConstraint, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

# Equivalente a tabla 'cursos'
class Curso(Base):
    __tablename__ = "cursos"
    __table_args__ = (
        CheckConstraint("grado BETWEEN 1 AND 5", name="cursos_grado_check"),
        CheckConstraint("seccion IN ('A', 'B', 'C', 'D')", name="cursos_seccion_check"),
        CheckConstraint(
            "periodo_escolar ~ '^[0-9]{4}-[0-9]{4}$'",
            name="cursos_periodo_escolar_check",
        ),
        UniqueConstraint("grado", "seccion", "periodo_escolar", name="curso_unico"), # Constraint que indica: El grado, sección y periodo de cada curso debe ser unico 
    )

    curso_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grado: Mapped[int] = mapped_column(Integer, nullable=False)
    seccion: Mapped[str] = mapped_column(String(1), nullable=False)
    periodo_escolar: Mapped[str] = mapped_column(String(10), nullable=False)
      