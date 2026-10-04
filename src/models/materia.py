from sqlalchemy import CheckConstraint, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Materia(Base):
    __tablename__ = "materias"
    __table_args__ = (
        CheckConstraint("grado BETWEEN 1 AND 5", name="chk_grado"),
        # CAMBIO: se refleja la unicidad de nombre y grado definida en SQL.
        UniqueConstraint("nombre", "grado", name="grado_nombre_unico"),
    )

    materia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # CAMBIO: se limita a 50 caracteres, como materias.nombre en SQL.
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    codigo: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)  # 'MAT-1', 'FIS-4'
    grado: Mapped[int] = mapped_column(Integer, nullable=False)
