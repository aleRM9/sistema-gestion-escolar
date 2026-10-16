from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
class ProfesorCurso(Base):
    __tablename__ = "profesores_cursos"
    __table_args__ = (
        UniqueConstraint("materia_id", "curso_id", name="materia_curso_unico"),
    )
    profesor_id: Mapped[int] = mapped_column(
        ForeignKey("profesores.profesor_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    materia_id: Mapped[int] = mapped_column(
        ForeignKey("materias.materia_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.curso_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )