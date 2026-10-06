from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.aula import (
    crear_aula,
    obtener_aula,
    listar_aulas,
    actualizar_aula,
    eliminar_aula,
)
from database import get_db
from schemas.aula import AulaCreate, AulaUpdate, AulaRead


router = APIRouter(prefix="/aulas", tags=["Aulas"])


@router.post("/", response_model=AulaRead, status_code=201)
def crear(datos: AulaCreate, db: Session = Depends(get_db)):
    """Registra una nueva aula en el sistema."""
    aula = crear_aula(db, datos)
    if aula is None:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un aula con el código [{datos.codigo}]",
        )
    return aula


@router.get("/", response_model=list[AulaRead])
def listar(db: Session = Depends(get_db)):
    """Devuelve todas las aulas registradas."""
    return listar_aulas(db)


@router.get("/{aula_id}", response_model=AulaRead)
def obtener(aula_id: int, db: Session = Depends(get_db)):
    """Devuelve los datos de un aula específica por su ID."""
    aula = obtener_aula(db, aula_id)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.put("/{aula_id}", response_model=AulaRead)
def actualizar(
    aula_id: int,
    datos: AulaUpdate,
    db: Session = Depends(get_db),
):
    """Actualiza los datos de un aula existente."""
    aula = actualizar_aula(db, aula_id, datos)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.delete("/{aula_id}")
def eliminar(aula_id: int, db: Session = Depends(get_db)):
    """Elimina un aula del sistema por su ID."""
    aula = eliminar_aula(db, aula_id)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return {"mensaje": f"El aula con ID {aula_id} ha sido eliminada"}
