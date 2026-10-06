from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.materia import MateriaCreate, MateriaUpdate, MateriaRead
from backend.controllers.materia import (
    actualizar_materia,
    eliminar_materia,
    listar_materias,
    obtener_materia,
    registrar_materia,
)
from backend.database import get_db  


router = APIRouter(prefix="/materias", tags=["Materias"])


@router.post("/", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: MateriaCreate, db: Session = Depends(get_db)):
    materia = registrar_materia(db, datos)
    if materia is None:
            raise HTTPException(status_code=404, detail=f"Codigo:[{datos.codigo}] ya registrado")
    
    return materia


@router.get("/", response_model=List[MateriaRead])
def listar(db: Session = Depends(get_db)):
    return listar_materias(db)


@router.get("/{materia_id}", response_model=MateriaRead)
def obtener(materia_id: int, db: Session = Depends(get_db)):
    materia = obtener_materia(db, materia_id)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.put("/{materia_id}", response_model=MateriaRead)
def actualizar(
    materia_id: int,
    datos: MateriaUpdate,
    db: Session = Depends(get_db),
):
    materia = actualizar_materia(db, materia_id, datos)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.delete("/{materia_id}")
def eliminar(materia_id: int, db: Session = Depends(get_db)):
    materia = eliminar_materia(db, materia_id)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return {"mensaje": "Materia eliminada correctamente"}