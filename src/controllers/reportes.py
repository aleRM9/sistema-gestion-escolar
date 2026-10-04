"""CAMBIO: archivo nuevo.

La lógica del promedio y del boletín estaba metida dentro de routes/notas.py.
Se movió aquí para mantener las rutas simples y la lógica en los controllers,
como en el resto del proyecto (y como pide la rúbrica: separación de capas).
"""
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.exceptions import NoEncontrado
from src.models.curso import Curso
from src.models.inscripcion import Inscripcion
from src.models.materia import Materia
from src.models.notas import Nota


def _redondear(valor) -> float | None:
    # La BD devuelve Decimal (o None si no hay notas); se pasa a float con 2
    # decimales para que el JSON sea un número normal.
    return None if valor is None else round(float(valor), 2)


def calcular_promedio(
    db: Session, id_alumno: int, id_materia: int, periodo: str | None = None
) -> dict:
    """Promedio de un alumno en una materia."""
    # CAMBIO: el periodo pertenece a cursos; primero se determina el periodo
    # aplicable y luego se agregan las notas de todas sus inscripciones.
    consulta = (
        db.query(Curso.periodo_escolar)
        .select_from(Inscripcion)
        .join(Curso, Curso.curso_id == Inscripcion.curso_id)
        .filter(
            Inscripcion.alumno_id == id_alumno,
            Inscripcion.materia_id == id_materia,
        )
    )
    if periodo is not None:
        consulta = consulta.filter(Curso.periodo_escolar == periodo)
    fila = consulta.order_by(Curso.periodo_escolar.desc()).first()

    if fila is None:
        raise NoEncontrado("El alumno no está inscrito en esta materia")
    periodo_inscripcion = fila[0]

    # CAMBIO: se agregan las notas de todas las inscripciones del mismo curso
    # escolar, usando las columnas reales de notas.
    promedio, cantidad = (
        db.query(func.avg(Nota.calificacion), func.count(Nota.nota_id))
        .select_from(Inscripcion)
        .join(Curso, Curso.curso_id == Inscripcion.curso_id)
        .outerjoin(Nota, Nota.inscripcion_id == Inscripcion.inscripcion_id)
        .filter(
            Inscripcion.alumno_id == id_alumno,
            Inscripcion.materia_id == id_materia,
            Curso.periodo_escolar == periodo_inscripcion,
        )
        .one()
    )

    return {
        "id_alumno": id_alumno,
        "id_materia": id_materia,
        "periodo": periodo_inscripcion,
        # CAMBIO: sin notas devuelve null en vez de un 0 engañoso.
        "promedio_actual": _redondear(promedio),
        "lapsos_evaluados": cantidad,
    }


def generar_boletin(db: Session, id_alumno: int, periodo: str | None = None) -> dict:
    """Boletín de un alumno para un periodo (por defecto, el más reciente)."""
    # CAMBIO: el periodo se obtiene desde cursos, no desde inscripciones.
    if periodo is None:
        periodo = (
            db.query(func.max(Curso.periodo_escolar))
            .select_from(Inscripcion)
            .join(Curso, Curso.curso_id == Inscripcion.curso_id)
            .filter(Inscripcion.alumno_id == id_alumno)
            .scalar()
        )
    if periodo is None:
        raise NoEncontrado("El alumno no tiene materias inscritas")

    # CAMBIO: se consulta el periodo por Curso, se usan las PK/columnas reales
    # y se agrupan notas de la misma materia para ese periodo.
    filas = (
        db.query(
            Materia.nombre,
            func.count(Nota.nota_id),
            func.avg(Nota.calificacion),
        )
        .select_from(Inscripcion)
        .join(Curso, Curso.curso_id == Inscripcion.curso_id)
        .join(Materia, Materia.materia_id == Inscripcion.materia_id)
        .outerjoin(Nota, Nota.inscripcion_id == Inscripcion.inscripcion_id)
        .filter(Inscripcion.alumno_id == id_alumno, Curso.periodo_escolar == periodo)
        .group_by(Materia.materia_id, Materia.nombre)
        .order_by(Materia.nombre)
        .all()
    )

    if not filas:
        raise NoEncontrado("El alumno no tiene materias inscritas en ese periodo")

    materias = []
    promedios = []
    for nombre, cantidad, promedio in filas:
        promedio_materia = _redondear(promedio)
        materias.append(
            {
                "materia": nombre,
                "cantidad_notas": cantidad,
                "promedio_materia": promedio_materia,  # null si aún no hay notas
            }
        )
        if promedio_materia is not None:
            promedios.append(promedio_materia)

    return {
        "id_alumno": id_alumno,
        "periodo": periodo,
        "materias": materias,
        # CAMBIO DE COMPORTAMIENTO: antes las materias sin notas contaban como
        # 0 y bajaban el promedio general injustamente. Ahora solo se promedian
        # las materias que ya tienen notas. Si prefieren lo anterior, hay que
        # sumar 0 por cada materia sin notas.
        "promedio_general": (
            round(sum(promedios) / len(promedios), 2) if promedios else None
        ),
    }
