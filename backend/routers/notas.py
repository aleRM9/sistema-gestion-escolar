from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.notas import (
    actualizar_nota,
    eliminar_nota,
    listar_notas,
    obtener_nota,
    registrar_nota,
)
from backend.controllers.reportes import calcular_promedio, generar_boletin
from backend.database import get_db
from backend.schemas.inscripcion import PATRON_PERIODO
from backend.schemas.notas import NotaCreate, NotaRead, NotaUpdate

router = APIRouter(prefix="/notas", tags=["Notas"])


@router.post("/", response_model=NotaRead, status_code=status.HTTP_201_CREATED)
async def crear(datos: NotaCreate, db: AsyncSession = Depends(get_db)):
    return await registrar_nota(db, datos)


@router.get("/", response_model=list[NotaRead])
async def listar(db: AsyncSession = Depends(get_db)):
    return await listar_notas(db)


@router.get("/promedio/{id_alumno}/{id_materia}")
async def promedio(
    id_alumno: int,
    id_materia: int,
    periodo: str | None = Query(default=None, pattern=PATRON_PERIODO),
    db: AsyncSession = Depends(get_db),
):
    return await calcular_promedio(db, id_alumno, id_materia, periodo)


@router.get("/boletin/{id_alumno}")
async def boletin(
    id_alumno: int,
    periodo: str | None = Query(default=None, pattern=PATRON_PERIODO),
    db: AsyncSession = Depends(get_db),
):
    return await generar_boletin(db, id_alumno, periodo)


@router.get("/{id_notas}", response_model=NotaRead)
async def obtener(id_notas: int, db: AsyncSession = Depends(get_db)):
    return await obtener_nota(db, id_notas)


@router.put("/{id_notas}", response_model=NotaRead)
async def actualizar(
    id_notas: int,
    datos: NotaUpdate,
    usuario_id: int = Header(gt=0, alias="X-Usuario-Id"),
    db: AsyncSession = Depends(get_db),
):
    return await actualizar_nota(db, id_notas, datos, usuario_id)


@router.delete("/{id_notas}")
async def eliminar(id_notas: int, db: AsyncSession = Depends(get_db)):
    await eliminar_nota(db, id_notas)
    return {"mensaje": "Nota eliminada correctamente"}
