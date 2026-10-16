"""CAMBIO: archivo nuevo.

La lógica del promedio y del boletín estaba metida dentro de routes/notas.py.
Se movió aquí para mantener las rutas simples y la lógica en los controllers,
como en el resto del proyecto (y como pide la rúbrica: separación de capas).
"""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.exceptions import NoEncontrado
from backend.models.curso import Curso
from backend.models.inscripcion import Inscripcion
from backend.models.materia import Materia
from backend.models.notas import Nota


def _redondear(valor) -> float | None:
    return None if valor is None else round(float(valor), 2)


async def calcular_promedio(
    db: AsyncSession, id_alumno: int, id_materia: int, periodo: str | None = None
) -> dict:
    """Promedio de un alumno en una materia."""
    consulta = (
        select(Curso.periodo_escolar)
        .select_from(Inscripcion)
        .join(Curso, Curso.curso_id == Inscripcion.curso_id)
        .where(
            Inscripcion.alumno_id == id_alumno,
            Inscripcion.materia_id == id_materia,
        )
    )
    if periodo is not None:
        consulta = consulta.where(Curso.periodo_escolar == periodo)
    fila = (await db.execute(consulta.order_by(Curso.periodo_escolar.desc()).limit(1))).first()

    if fila is None:
        raise NoEncontrado("El alumno no está inscrito en esta materia")
    periodo_inscripcion = fila[0]

    consulta_promedio = (
        select(func.avg(Nota.calificacion), func.count(Nota.nota_id))
        .select_from(Inscripcion)
        .join(Curso, Curso.curso_id == Inscripcion.curso_id)
        .outerjoin(Nota, Nota.inscripcion_id == Inscripcion.inscripcion_id)
        .where(
            Inscripcion.alumno_id == id_alumno,
            Inscripcion.materia_id == id_materia,
            Curso.periodo_escolar == periodo_inscripcion,
        )
    )
    resultado = await db.execute(consulta_promedio)
    promedio, cantidad = resultado.one()

    return {
        "id_alumno": id_alumno,
        "id_materia": id_materia,
        "periodo": periodo_inscripcion,
        "promedio_actual": _redondear(promedio),
        "lapsos_evaluados": cantidad,
    }


async def generar_boletin(
    db: AsyncSession, id_alumno: int, periodo: str | None = None
) -> dict:
    """Boletín de un alumno para un periodo (por defecto, el más reciente)."""
    if periodo is None:
        periodo = await db.scalar(
            select(func.max(Curso.periodo_escolar))
            .select_from(Inscripcion)
            .join(Curso, Curso.curso_id == Inscripcion.curso_id)
            .where(Inscripcion.alumno_id == id_alumno)
        )
    if periodo is None:
        raise NoEncontrado("El alumno no tiene materias inscritas")

    consulta = (
        select(
            Materia.nombre,
            func.count(Nota.nota_id),
            func.avg(Nota.calificacion),
        )
        .select_from(Inscripcion)
        .join(Curso, Curso.curso_id == Inscripcion.curso_id)
        .join(Materia, Materia.materia_id == Inscripcion.materia_id)
        .outerjoin(Nota, Nota.inscripcion_id == Inscripcion.inscripcion_id)
        .where(Inscripcion.alumno_id == id_alumno, Curso.periodo_escolar == periodo)
        .group_by(Materia.materia_id, Materia.nombre)
        .order_by(Materia.nombre)
    )
    filas = (await db.execute(consulta)).all()

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
                "promedio_materia": promedio_materia,
            }
        )
        if promedio_materia is not None:
            promedios.append(promedio_materia)

    return {
        "id_alumno": id_alumno,
        "periodo": periodo,
        "materias": materias,
        "promedio_general": (
            round(sum(promedios) / len(promedios), 2) if promedios else None
        ),
    }
