from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date
from representante import Representante

class Alumno(Base):
    __tablename__ = "alumnos"

    alumno_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cedula: Mapped[str] = mapped_column(String(10), unique=True)
    fecha_nacimiento: Mapped[date] = mapped_column(Date) # Cambiado a Date
    
    representante_id: Mapped[int] = mapped_column(ForeignKey("representantes.representante_id"))
    representante: Mapped["Representante"] = relationship(back_populates="alumnos")
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.curso_id"))
