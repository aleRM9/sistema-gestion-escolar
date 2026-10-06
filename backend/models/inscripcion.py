from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class Inscripcion(Base):
    __tablename__ = "inscripciones"

    inscripcion_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    materia_id: Mapped[int] = mapped_column(
        ForeignKey("materias.materia_id"),
        nullable=False,
        index=True,
    )
    alumno_id: Mapped[int] = mapped_column(
        ForeignKey("alumnos.alumno_id"),
        nullable=False,
        index=True,
    )
    curso_id: Mapped[int] = mapped_column(
            ForeignKey("cursos.curso_id"),
            nullable=False,
            index=True,
        )