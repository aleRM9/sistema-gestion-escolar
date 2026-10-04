from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.utils import confirmar
from backend.exceptions import Conflicto, NoEncontrado
from backend.models.materia import Materia
from backend.schemas.materia import MateriaCreate, MateriaUpdate


async def _codigo_en_uso(
    db: AsyncSession, codigo: str, excluir_id: int | None = None
) -> bool:
    consulta = select(Materia.materia_id).where(Materia.codigo == codigo)
    if excluir_id is not None:
        consulta = consulta.where(Materia.materia_id != excluir_id)
    return await db.scalar(consulta.limit(1)) is not None


async def _nombre_grado_en_uso(
    db: AsyncSession, nombre: str, grado: int, excluir_id: int | None = None
) -> bool:
    consulta = select(Materia.materia_id).where(
        Materia.nombre == nombre,
        Materia.grado == grado,
    )
    if excluir_id is not None:
        consulta = consulta.where(Materia.materia_id != excluir_id)
    return await db.scalar(consulta.limit(1)) is not None


async def registrar_materia(db: AsyncSession, datos: MateriaCreate) -> Materia:
    if await _codigo_en_uso(db, datos.codigo):
        raise Conflicto(f"Código [{datos.codigo}] ya registrado")
    if await _nombre_grado_en_uso(db, datos.nombre, datos.grado):
        raise Conflicto("Ya existe una materia con ese nombre para ese grado")

    materia = Materia(**datos.model_dump())
    db.add(materia)
    await confirmar(db, f"Código [{datos.codigo}] ya registrado")
    await db.refresh(materia)
    return materia


async def obtener_materia(db: AsyncSession, id_materia: int) -> Materia:
    materia = await db.get(Materia, id_materia)
    if materia is None:
        raise NoEncontrado("Materia no encontrada")
    return materia


async def listar_materias(db: AsyncSession) -> list[Materia]:
    resultado = await db.scalars(select(Materia).order_by(Materia.materia_id))
    return list(resultado.all())


async def actualizar_materia(
    db: AsyncSession, id_materia: int, datos: MateriaUpdate
) -> Materia:
    materia = await obtener_materia(db, id_materia)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    nuevo_codigo = cambios.get("codigo")
    if nuevo_codigo is not None and await _codigo_en_uso(db, nuevo_codigo, id_materia):
        raise Conflicto(f"Código [{nuevo_codigo}] ya registrado")
    nombre = cambios.get("nombre", materia.nombre)
    grado = cambios.get("grado", materia.grado)
    if await _nombre_grado_en_uso(db, nombre, grado, id_materia):
        raise Conflicto("Ya existe una materia con ese nombre para ese grado")

    for campo, valor in cambios.items():
        setattr(materia, campo, valor)

    await confirmar(db, "No se pudo actualizar la materia")
    await db.refresh(materia)
    return materia


async def eliminar_materia(db: AsyncSession, id_materia: int) -> None:
    materia = await obtener_materia(db, id_materia)
    await db.delete(materia)
    await confirmar(
        db, "No se puede eliminar la materia porque tiene inscripciones asociadas"
    )
