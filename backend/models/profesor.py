from sqlalchemy import String, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base



class Profesor(Base):
    __tablename__ = "profesores"

    profesor_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cedula: Mapped[str] = mapped_column(String(10), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    especialidad: Mapped[str] = mapped_column(String(20))
    
    salario_base: Mapped[float] = mapped_column(
        Numeric(8, 2),
        CheckConstraint("salario_base > 0", name="check_salario_base")
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), unique=True)