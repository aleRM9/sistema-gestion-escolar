from sqlalchemy import ForeignKey, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from representante import Representante
from .base import Base

# Equivalente a tabla 'alumnos'
class Alumno(Base):
    __tablename__ = "alumnos"

    alumno_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    cedula: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False) # Cambiado a Date
      
    # Instruccción equivalente a la referencia a la tabla representantes, mediante la FK representante_id
    representante_id: Mapped[int] = mapped_column(
        ForeignKey("representantes.representante_id", ondelete="RESTRICT"),
        nullable=False,
    )
    
    # Establece sincronización bidireccional entre alumnos y representantes
    representante: Mapped["Representante"] = relationship(back_populates="alumnos")
      
    # Clave foránea para establecer referencia a la tabla cursos  
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.curso_id"))
