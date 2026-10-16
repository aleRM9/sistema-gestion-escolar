from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.inscripcion import (
    actualizar_inscripcion,
    eliminar_inscripcion,
    listar_inscripciones,
    obtener_inscripcion,
    registrar_inscripcion,
)
from database import get_db_session
from schemas.inscripcion import (
    InscripcionCreate,
    InscripcionRead,
    InscripcionUpdate,
)

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
async def crear(datos: InscripcionCreate, db: AsyncSession = Depends(get_db_session)):
    return await registrar_inscripcion(db, datos)


@router.get("/", response_model=list[InscripcionRead])
async def listar(db: AsyncSession = Depends(get_db_session)):
    return await listar_inscripciones(db)


@router.get("/{id_inscripcion}", response_model=InscripcionRead)
async def obtener(id_inscripcion: int, db: AsyncSession = Depends(get_db_session)):
    return await obtener_inscripcion(db, id_inscripcion)


@router.put("/{id_inscripcion}", response_model=InscripcionRead)
async def actualizar(
    id_inscripcion: int,
    datos: InscripcionUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    return await actualizar_inscripcion(db, id_inscripcion, datos)


@router.delete("/{id_inscripcion}")
async def eliminar(id_inscripcion: int, db: AsyncSession = Depends(get_db_session)):
    await eliminar_inscripcion(db, id_inscripcion)
    return {"mensaje": "Inscripción eliminada correctamente"}