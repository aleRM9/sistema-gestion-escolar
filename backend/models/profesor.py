from sqlalchemy import String, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


# Equivalente a tabla 'Profesores'
class Profesor(Base):
    __tablename__ = "profesores"

    profesor_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    cedula: Mapped[str] = mapped_column(String(10), unique=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    especialidad: Mapped[str] = mapped_column(String(20), nullable=False)
    
    salario_base: Mapped[float] = mapped_column(
        Numeric(8, 2),
        CheckConstraint("salario_base > 0", name="check_salario_base")
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), unique=True)