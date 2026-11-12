from typing import Annotated

from backend.controllers.seguridad import verificar_roles
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.usuario import Usuario
from backend.controllers.inscripcion import (
    actualizar_inscripcion,
    eliminar_inscripcion,
    listar_inscripciones,
    obtener_inscripcion,
    registrar_inscripcion,
)
from backend.database import get_db_session
from backend.schemas.inscripcion import (
    InscripcionCreate,
    InscripcionRead,
    InscripcionUpdate,
)

dependencia_db = Annotated[AsyncSession, Depends(get_db_session)]
router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"]) 


@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
async def crear(
    datos: InscripcionCreate,
    db:dependencia_db,
    usuario: Usuario = Depends(verificar_roles([3]))
    ):
    return await registrar_inscripcion(db, datos)


@router.get("/", response_model=list[InscripcionRead])
async def listar(
    db:dependencia_db,
    usuario: Usuario = Depends(verificar_roles([1,2]))
    ):
    return await listar_inscripciones(db)


@router.get("/{id_inscripcion}", response_model=InscripcionRead)
async def obtener(
    id_inscripcion: int,
    db:dependencia_db, 
    usuario: Usuario = Depends(verificar_roles([3]))
    ):
    return await obtener_inscripcion(db, id_inscripcion)


@router.put("/{id_inscripcion}", response_model=InscripcionRead)
async def actualizar(
    id_inscripcion: int,
    datos: InscripcionUpdate,
    db:dependencia_db,
    usuario: Usuario = Depends(verificar_roles([3]))
):
    return await actualizar_inscripcion(db, id_inscripcion, datos)


@router.delete("/{id_inscripcion}")
async def eliminar(
    id_inscripcion: int,
    db:dependencia_db,
    usuario: Usuario = Depends(verificar_roles([1,2]))
    ):
    await eliminar_inscripcion(db, id_inscripcion)
    return {"mensaje": "Inscripción eliminada correctamente"}