from sqlalchemy.orm import Session

from src.controllers.utils import confirmar
from src.exceptions import Conflicto, NoEncontrado
from src.models.alumno import Alumno
from src.models.curso import Curso
from src.models.inscripcion import Inscripcion
from src.models.materia import Materia
from src.schemas.inscripcion import InscripcionCreate, InscripcionUpdate


# CAMBIO: función nueva. Comprueba que la materia y el alumno existan antes
# de inscribir, para responder 404 con un mensaje claro en vez de un error
# de llave foránea de la base de datos.
def _verificar_referencias(
    db: Session,
    materia_id: int | None,
    alumno_id: int | None,
    curso_id: int | None,
) -> None:
    materia = db.get(Materia, materia_id) if materia_id is not None else None
    curso = db.get(Curso, curso_id) if curso_id is not None else None
    if materia_id is not None and materia is None:
        raise NoEncontrado(f"La materia {materia_id} no existe")
    if alumno_id is not None and db.get(Alumno, alumno_id) is None:
        raise NoEncontrado(f"El alumno {alumno_id} no existe")
    if curso_id is not None and curso is None:
        raise NoEncontrado(f"El curso {curso_id} no existe")
    # CAMBIO: replica antes del INSERT/UPDATE el trigger SQL que prohíbe
    # asignar una materia cuyo grado no coincida con el curso.
    if materia is not None and curso is not None and materia.grado != curso.grado:
        raise Conflicto("El grado de la materia no coincide con el grado del curso")


# CAMBIO: función nueva. Detecta si el alumno ya está inscrito en esa materia
# en ese periodo (regla uq_alumno_materia_periodo del SQL). Antes la regla
# ignoraba el periodo, lo que impedía re-inscribir en años distintos.
def _ya_inscrito(
    db: Session,
    alumno_id: int,
    materia_id: int,
    curso_id: int,
    excluir_id: int | None = None,
) -> bool:
    consulta = db.query(Inscripcion).filter(
        Inscripcion.alumno_id == alumno_id,
        Inscripcion.materia_id == materia_id,
        Inscripcion.curso_id == curso_id,
    )
    if excluir_id is not None:
        consulta = consulta.filter(Inscripcion.id_inscripcion != excluir_id)
    return consulta.first() is not None


def registrar_inscripcion(db: Session, datos: InscripcionCreate) -> Inscripcion:
    _verificar_referencias(db, datos.materia_id, datos.alumno_id, datos.curso_id)

    # CAMBIO: la unicidad SQL depende del curso, no de un periodo duplicado
    # directamente en la inscripción.
    mensaje = "El alumno ya está inscrito en esa materia y curso"
    if _ya_inscrito(db, datos.alumno_id, datos.materia_id, datos.curso_id):
        raise Conflicto(mensaje)

    inscripcion = Inscripcion(**datos.model_dump())
    db.add(inscripcion)
    confirmar(db, mensaje)
    db.refresh(inscripcion)
    return inscripcion


def obtener_inscripcion(db: Session, id_inscripcion: int) -> Inscripcion:
    # CAMBIO: lanza NoEncontrado en vez de devolver None (ver materia.py).
    inscripcion = db.get(Inscripcion, id_inscripcion)
    if inscripcion is None:
        raise NoEncontrado("Inscripción no encontrada")
    return inscripcion


def listar_inscripciones(db: Session) -> list[Inscripcion]:
    return db.query(Inscripcion).order_by(Inscripcion.inscripcion_id).all()


def actualizar_inscripcion(
    db: Session, id_inscripcion: int, datos: InscripcionUpdate
) -> Inscripcion:
    inscripcion = obtener_inscripcion(db, id_inscripcion)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    # CAMBIO: se validan las referencias y el grado del resultado final,
    # incluyendo los valores que no se modificaron en la petición.
    materia_id = cambios.get("materia_id", inscripcion.materia_id)
    alumno_id = cambios.get("alumno_id", inscripcion.alumno_id)
    curso_id = cambios.get("curso_id", inscripcion.curso_id)
    _verificar_referencias(db, materia_id, alumno_id, curso_id)

    mensaje = "El alumno ya está inscrito en esa materia y curso"
    if _ya_inscrito(
        db,
        alumno_id,
        materia_id,
        curso_id,
        excluir_id=id_inscripcion,
    ):
        raise Conflicto(mensaje)

    for campo, valor in cambios.items():
        setattr(inscripcion, campo, valor)

    confirmar(db, mensaje)
    db.refresh(inscripcion)
    return inscripcion


def eliminar_inscripcion(db: Session, id_inscripcion: int) -> None:
    # Las notas de la inscripción se borran solas (ON DELETE CASCADE en la BD)
    inscripcion = obtener_inscripcion(db, id_inscripcion)
    db.delete(inscripcion)
    confirmar(db, "No se pudo eliminar la inscripción")
