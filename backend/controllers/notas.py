from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.utils import confirmar
from backend.exceptions import Conflicto, NoEncontrado
from backend.models.inscripcion import Inscripcion
from backend.models.notas import Nota
from backend.schemas.notas import NotaCreate, NotaUpdate

MENSAJE_LAPSO = "Ya existe una nota para esa inscripción en ese lapso"


async def _lapso_ocupado(
    db: AsyncSession,
    id_inscripcion: int,
    lapso: int,
    excluir_id: int | None = None,
) -> bool:
    consulta = select(Nota.nota_id).where(
        Nota.inscripcion_id == id_inscripcion, Nota.lapso == lapso
    )
    if excluir_id is not None:
        consulta = consulta.where(Nota.nota_id != excluir_id)
    return await db.scalar(consulta.limit(1)) is not None


async def registrar_nota(db: AsyncSession, datos: NotaCreate) -> Nota:
    if await db.get(Inscripcion, datos.inscripcion_id) is None:
        raise NoEncontrado(f"La inscripción {datos.inscripcion_id} no existe")
    if await _lapso_ocupado(db, datos.inscripcion_id, datos.lapso):
        raise Conflicto(MENSAJE_LAPSO)

    nota = Nota(**datos.model_dump())
    db.add(nota)
    await confirmar(db, MENSAJE_LAPSO)
    await db.refresh(nota)
    return nota


async def obtener_nota(db: AsyncSession, id_notas: int) -> Nota:
    nota = await db.get(Nota, id_notas)
    if nota is None:
        raise NoEncontrado("Nota no encontrada")
    return nota


async def listar_notas(db: AsyncSession) -> list[Nota]:
    resultado = await db.scalars(select(Nota).order_by(Nota.nota_id))
    return list(resultado.all())


async def actualizar_nota(
    db: AsyncSession, id_notas: int, datos: NotaUpdate, usuario_id: int
) -> Nota:
    nota = await obtener_nota(db, id_notas)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    nuevo_lapso = cambios.get("lapso")
    if nuevo_lapso is not None and await _lapso_ocupado(
        db, nota.inscripcion_id, nuevo_lapso, excluir_id=id_notas
    ):
        raise Conflicto(MENSAJE_LAPSO)

    if cambios.get("calificacion") is not None and cambios["calificacion"] != nota.calificacion:
        usuario_existe = await db.execute(
            text("SELECT 1 FROM usuarios WHERE usuario_id = :usuario_id"),
            {"usuario_id": usuario_id},
        ).scalar_one_or_none()
        if usuario_existe is None:
            raise NoEncontrado(f"El usuario {usuario_id} no existe")
        await db.execute(
            select(func.set_config("app.current_user_id", str(usuario_id), True))
        )

    for campo, valor in cambios.items():
        setattr(nota, campo, valor)

    await confirmar(db, MENSAJE_LAPSO)
    await db.refresh(nota)
    return nota


async def eliminar_nota(db: AsyncSession, id_notas: int) -> None:
    nota = await obtener_nota(db, id_notas)
    await db.delete(nota)
    await confirmar(db, "No se pudo eliminar la nota")
