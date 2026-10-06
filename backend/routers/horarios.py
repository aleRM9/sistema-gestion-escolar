from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.horario import (
    crear_horario, obtener_horario, listar_horarios,
    actualizar_horario, eliminar_horario,
)
from database import get_db
from schemas.horario import HorarioRespuesta

router = APIRouter(prefix="/horarios", tags=["Horarios"])

@router.post("/", response_model=HorarioRespuesta, status_code=201)
def crear(datos: dict, db: Session = Depends(get_db)):
    """Registra un nuevo bloque horario validando choques de horario."""
    return crear_horario(db, datos)

@router.get("/", response_model=list[HorarioRespuesta])
def listar(db: Session = Depends(get_db)):
    """Devuelve todos los bloques horarios registrados."""
    return listar_horarios(db)

@router.get("/{horario_id}", response_model=HorarioRespuesta)
def obtener(horario_id: int, db: Session = Depends(get_db)):
    horario = obtener_horario(db, horario_id)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.put("/{horario_id}", response_model=HorarioRespuesta)
def actualizar(horario_id: int, datos: dict, db: Session = Depends(get_db)):
    horario = actualizar_horario(db, horario_id, datos)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.delete("/{horario_id}")
def eliminar(horario_id: int, db: Session = Depends(get_db)):
    # Eliminar retorna un dict con mensaje, no un HorarioRespuesta
    resultado = eliminar_horario(db, horario_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return resultado
