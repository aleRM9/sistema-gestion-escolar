from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.notas import (
    registrar_nota, obtener_nota, listar_notas,
    actualizar_nota, eliminar_nota,
)
from backend.database import get_db_session
from backend.schemas.notas import NotaCreate, NotaUpdate, NotaRead

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])

@router.post("/", response_model=NotaRead, status_code=201)
async def crear(datos: NotaCreate, db: AsyncSession = Depends(get_db_session)):
    # Registra una nueva calificación para una inscripción
    return registrar_nota(db, datos)

@router.get("/", response_model=list[NotaRead])
async def listar(db: AsyncSession = Depends(get_db_session)):
    # Devuelve todas las calificaciones registradas
    return listar_notas(db)

@router.get("/{nota_id}", response_model=NotaRead)
async def obtener(nota_id: int, db: AsyncSession = Depends(get_db_session)):
    nota = obtener_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    return nota

@router.get("/inscripcion/{inscripcion_id}", response_model=list[NotaRead])
async def listar_por_inscripcion(inscripcion_id: int, db: AsyncSession = Depends(get_db_session)):
    # Devuelve todas las calificaciones de una inscripción específica.
    return listar_notas(db, inscripcion_id=inscripcion_id)

@router.put("/{nota_id}", response_model=NotaRead)
async def actualizar(nota_id: int, datos: NotaUpdate, db: AsyncSession = Depends(get_db_session)):
    nota = actualizar_nota(db, nota_id, datos)
    if nota is None:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    return nota

@router.delete("/{nota_id}")
async def eliminar(nota_id: int, db: AsyncSession = Depends(get_db_session)):
    nota = eliminar_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    return {"mensaje": "Calificación eliminada correctamente"}
