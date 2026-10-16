from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column
from datetime import time

from .base import Base


class Bloque(Base):
    __tablename__ = "bloques"
    __table_args__ = (
        CheckConstraint(
            "dia IN ('lunes','martes','miercoles','jueves','viernes')",
            name="ck_bloques_dia"
        ),
        CheckConstraint("hora_fin > hora_inicio", name="hora_valida"),
    )

    bloque_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aula_id: Mapped[int] = mapped_column(
        ForeignKey("aulas.aula_id"), nullable=False
    )
    materia_id: Mapped[int] = mapped_column(
        ForeignKey("materias.materia_id"), nullable=False
    )
    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.curso_id"), nullable=False
    )
    profesor_id: Mapped[int] = mapped_column(
        ForeignKey("profesores.profesor_id"), nullable=False
    )
    dia: Mapped[str] = mapped_column(String(10), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
