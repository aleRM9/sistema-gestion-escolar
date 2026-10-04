from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.utils import confirmar
from backend.exceptions import Conflicto, NoEncontrado
from backend.models.alumno import Alumno
from backend.models.curso import Curso
from backend.models.inscripcion import Inscripcion
from backend.models.materia import Materia
from backend.schemas.inscripcion import InscripcionCreate, InscripcionUpdate


async def _verificar_referencias(
    db: AsyncSession,
    materia_id: int | None,
    alumno_id: int | None,
    curso_id: int | None,
) -> None:
    materia = await db.get(Materia, materia_id) if materia_id is not None else None
    curso = await db.get(Curso, curso_id) if curso_id is not None else None
    if materia_id is not None and materia is None:
        raise NoEncontrado(f"La materia {materia_id} no existe")
    if alumno_id is not None and await db.get(Alumno, alumno_id) is None:
        raise NoEncontrado(f"El alumno {alumno_id} no existe")
    if curso_id is not None and curso is None:
        raise NoEncontrado(f"El curso {curso_id} no existe")
    if materia is not None and curso is not None and materia.grado != curso.grado:
        raise Conflicto("El grado de la materia no coincide con el grado del curso")


async def _ya_inscrito(
    db: AsyncSession,
    alumno_id: int,
    materia_id: int,
    curso_id: int,
    excluir_id: int | None = None,
) -> bool:
    consulta = select(Inscripcion.inscripcion_id).where(
        Inscripcion.alumno_id == alumno_id,
        Inscripcion.materia_id == materia_id,
        Inscripcion.curso_id == curso_id,
    )
    if excluir_id is not None:
        consulta = consulta.where(Inscripcion.inscripcion_id != excluir_id)
    return await db.scalar(consulta.limit(1)) is not None


async def registrar_inscripcion(db: AsyncSession, datos: InscripcionCreate) -> Inscripcion:
    await _verificar_referencias(db, datos.materia_id, datos.alumno_id, datos.curso_id)

    mensaje = "El alumno ya está inscrito en esa materia y curso"
    if await _ya_inscrito(db, datos.alumno_id, datos.materia_id, datos.curso_id):
        raise Conflicto(mensaje)

    inscripcion = Inscripcion(**datos.model_dump())
    db.add(inscripcion)
    await confirmar(db, mensaje)
    await db.refresh(inscripcion)
    return inscripcion


async def obtener_inscripcion(db: AsyncSession, id_inscripcion: int) -> Inscripcion:
    inscripcion = await db.get(Inscripcion, id_inscripcion)
    if inscripcion is None:
        raise NoEncontrado("Inscripción no encontrada")
    return inscripcion


async def listar_inscripciones(db: AsyncSession) -> list[Inscripcion]:
    resultado = await db.scalars(select(Inscripcion).order_by(Inscripcion.inscripcion_id))
    return list(resultado.all())


async def actualizar_inscripcion(
    db: AsyncSession, id_inscripcion: int, datos: InscripcionUpdate
) -> Inscripcion:
    inscripcion = await obtener_inscripcion(db, id_inscripcion)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    materia_id = cambios.get("materia_id", inscripcion.materia_id)
    alumno_id = cambios.get("alumno_id", inscripcion.alumno_id)
    curso_id = cambios.get("curso_id", inscripcion.curso_id)
    await _verificar_referencias(db, materia_id, alumno_id, curso_id)

    mensaje = "El alumno ya está inscrito en esa materia y curso"
    if await _ya_inscrito(
        db,
        alumno_id,
        materia_id,
        curso_id,
        excluir_id=id_inscripcion,
    ):
        raise Conflicto(mensaje)

    for campo, valor in cambios.items():
        setattr(inscripcion, campo, valor)

    await confirmar(db, mensaje)
    await db.refresh(inscripcion)
    return inscripcion


async def eliminar_inscripcion(db: AsyncSession, id_inscripcion: int) -> None:
    inscripcion = await obtener_inscripcion(db, id_inscripcion)
    await db.delete(inscripcion)
    await confirmar(db, "No se pudo eliminar la inscripción")
