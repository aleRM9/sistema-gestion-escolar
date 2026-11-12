from typing import Annotated
from backend.controllers.seguridad import verificar_roles
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.materia import (
    actualizar_materia,
    eliminar_materia,
    listar_materias,
    obtener_materia,
    registrar_materia,
)
from backend.database import get_db_session
from backend.schemas.materia import MateriaCreate, MateriaRead, MateriaUpdate
from backend.models.usuario import Usuario

dependecia_db = Annotated[AsyncSession, Depends(get_db_session)]
router = APIRouter(prefix="/materias", tags=["Materias"])


@router.post("/", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
async def crear(
    datos: MateriaCreate,
    db: dependecia_db,
    usuario: Usuario = Depends(verificar_roles([1]))
    ):
    return await registrar_materia(db, datos)


@router.get("/", response_model=list[MateriaRead])
async def listar(
    db: dependecia_db,
    usuario: Usuario = Depends(verificar_roles([3]))
    ):
    return await listar_materias(db)


@router.get("/{id_materia}", response_model=MateriaRead)
async def obtener(
    id_materia: int,
    db: dependecia_db,
    usuario: Usuario = Depends(verificar_roles([3]))
    ):
    return await obtener_materia(db, id_materia)


@router.put("/{id_materia}", response_model=MateriaRead)
async def actualizar(
    id_materia: int, datos: MateriaUpdate, 
    db: dependecia_db,
    usuario: Usuario = Depends(verificar_roles([1]))
    ):
    return await actualizar_materia(db, id_materia, datos)


@router.delete("/{id_materia}")
async def eliminar(
    id_materia: int,
    db: dependecia_db,
    usuario: Usuario = Depends(verificar_roles([1]))
    ):
    await eliminar_materia(db, id_materia)
    return {"mensaje": "Materia eliminada correctamente"}