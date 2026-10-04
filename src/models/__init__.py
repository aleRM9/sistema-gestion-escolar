# CAMBIO: se registran los modelos de tablas que son destino de FKs del
# módulo académico para que SQLAlchemy pueda resolver toda la metadata.
from .alumno import Alumno
from .curso import Curso
from .inscripcion import Inscripcion
from .materia import Materia
from .notas import Nota
from .representante import Representante

__all__ = ["Alumno", "Curso", "Inscripcion", "Materia", "Nota", "Representante"]
