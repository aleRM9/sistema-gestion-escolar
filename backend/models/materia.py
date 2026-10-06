from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Materia(Base):
    __tablename__ = "materias"
    __table_args__ = (
        CheckConstraint("grado BETWEEN 1 AND 5", name="ck_materias_grado"),
    )

    materia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(
        String(10), nullable=False, unique=True, index=True
    )
    grado: Mapped[int] = mapped_column(Integer, nullable=False)