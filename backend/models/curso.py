from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base

class Curso(Base):
    __tablename__ = "cursos"
    __table_args__ = (
        CheckConstraint("grado >= 1 AND grado <= 5",
            name="ck_cursos_grado"
        ), 
        CheckConstraint("seccion IN ('A', 'B','C','D')",
            name="ck_cursos_seccion"
        ),
        CheckConstraint(
            r"periodo_escolar ^\d{4}-\d{4}$'",
            name="ck_cursos_periodo"
        )
    )

    curso_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grado:Mapped[int] = mapped_column(Integer, nullable=False)
    seccion:Mapped[int] = mapped_column(String(1), nullable=False)
    periodo_escolar: Mapped[str] = mapped_column(String(10), nullable=False)