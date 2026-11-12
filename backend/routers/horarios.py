from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.horario import (
    crear_horario, obtener_horario, listar_horarios,
    actualizar_horario, eliminar_horario,
)
from backend.database import get_db_session
from backend.schemas.horario import HorarioRespuesta

router = APIRouter(prefix="/horarios", tags=["Horarios"])

@router.post("/", response_model=HorarioRespuesta, status_code=201)
async def crear(datos: dict, db: AsyncSession = Depends(get_db_session)):
    """Registra un nuevo bloque horario validando choques de horario."""
    return crear_horario(db, datos)

@router.get("/", response_model=list[HorarioRespuesta])
async def listar(db: AsyncSession = Depends(get_db_session)):
    """Devuelve todos los bloques horarios registrados."""
    return listar_horarios(db)

@router.get("/{horario_id}", response_model=HorarioRespuesta)
async def obtener(horario_id: int, db: AsyncSession = Depends(get_db_session)):
    horario = obtener_horario(db, horario_id)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.put("/{horario_id}", response_model=HorarioRespuesta)
async def actualizar(horario_id: int, datos: dict, db: AsyncSession = Depends(get_db_session)):
    horario = actualizar_horario(db, horario_id, datos)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.delete("/{horario_id}")
async def eliminar(horario_id: int, db: AsyncSession = Depends(get_db_session)):
    # Eliminar retorna un dict con mensaje, no un HorarioRespuesta
    resultado = eliminar_horario(db, horario_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return resultado
