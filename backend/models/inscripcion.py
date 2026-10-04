from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Inscripcion(Base):
    __tablename__ = "inscripciones"
    __table_args__ = (
        UniqueConstraint("alumno_id", "materia_id", "curso_id", name="inscripcion_unica"),
    )

    inscripcion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    materia_id: Mapped[int] = mapped_column(
        ForeignKey("materias.materia_id", ondelete="RESTRICT"), nullable=False
    )
    alumno_id: Mapped[int] = mapped_column(
        ForeignKey("alumnos.alumno_id", ondelete="RESTRICT"), nullable=False
    )
    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.curso_id", ondelete="RESTRICT"), nullable=False
    )
