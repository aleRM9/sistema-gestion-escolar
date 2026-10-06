from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.notas import (
    registrar_nota, obtener_nota, listar_notas,
    actualizar_nota, eliminar_nota,
)
from database import get_db
from schemas.notas import NotaCreate, NotaUpdate, NotaRead

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])

@router.post("/", response_model=NotaRead, status_code=201)
def crear(datos: NotaCreate, db: Session = Depends(get_db)):
    # Registra una nueva calificación para una inscripción
    return registrar_nota(db, datos)

@router.get("/", response_model=list[NotaRead])
def listar(db: Session = Depends(get_db)):
    # Devuelve todas las calificaciones registradas
    return listar_notas(db)

@router.get("/{nota_id}", response_model=NotaRead)
def obtener(nota_id: int, db: Session = Depends(get_db)):
    nota = obtener_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    return nota

@router.get("/inscripcion/{inscripcion_id}", response_model=list[NotaRead])
def listar_por_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    # Devuelve todas las calificaciones de una inscripción específica.
    return listar_notas(db, inscripcion_id=inscripcion_id)

@router.put("/{nota_id}", response_model=NotaRead)
def actualizar(nota_id: int, datos: NotaUpdate, db: Session = Depends(get_db)):
    nota = actualizar_nota(db, nota_id, datos)
    if nota is None:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    return nota

@router.delete("/{nota_id}")
def eliminar(nota_id: int, db: Session = Depends(get_db)):
    nota = eliminar_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    return {"mensaje": "Calificación eliminada correctamente"}
