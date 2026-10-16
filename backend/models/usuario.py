from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base


class Rol(Base):
    __tablename__ = "roles"

    rol_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_usuario: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    correo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    contrasenia: Mapped[str] = mapped_column(String(255), nullable=False)

    rol_id: Mapped[int] = mapped_column(
        ForeignKey("roles.rol_id"), nullable=False
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)