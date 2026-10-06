from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.controllers.inscripcion import (
    actualizar_inscripcion,
    eliminar_inscripcion,
    listar_inscripciones,
    obtener_inscripcion,
    registrar_inscripcion,
)
from src.database import get_db
from src.schemas.inscripcion import (
    InscripcionCreate,
    InscripcionRead,
    InscripcionUpdate,
)


router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.post("/", response_model=InscripcionRead, status_code=201)
def crear(datos: InscripcionCreate, db: Session = Depends(get_db)):
    inscripcion = registrar_inscripcion(db, datos)
    if inscripcion is None:
        raise HTTPException(status_code=404, detail=f"Inscripcion ya registrada")
        
    return inscripcion


@router.get("/", response_model=list[InscripcionRead])
def listar(db: Session = Depends(get_db)):
    return listar_inscripciones(db)


@router.get("/{inscripcion_id}", response_model=InscripcionRead)
def obtener(inscripcion_id: int, db: Session = Depends(get_db)):
    inscripcion = obtener_inscripcion(db, inscripcion_id)
    if inscripcion is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return inscripcion


@router.put("/{inscripcion_id}", response_model=InscripcionRead)
def actualizar(
    inscripcion_id: int,
    datos: InscripcionUpdate,
    db: Session = Depends(get_db),
):
    inscripcion = actualizar_inscripcion(db, inscripcion_id, datos)
    if inscripcion is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return inscripcion


@router.delete("/{inscripcion_id}")
def eliminar(inscripcion_id: int, db: Session = Depends(get_db)):
    inscripcion = eliminar_inscripcion(db, inscripcion_id)
    if inscripcion is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"mensaje": "Inscripción eliminada correctamente"}