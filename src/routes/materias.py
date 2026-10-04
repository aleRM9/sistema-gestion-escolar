from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.controllers.materia import (
    actualizar_materia,
    eliminar_materia,
    listar_materias,
    obtener_materia,
    registrar_materia,
)
from src.database import get_db
from src.schemas.materia import MateriaCreate, MateriaRead, MateriaUpdate

router = APIRouter(prefix="/materias", tags=["Materias"])


# CAMBIO (en todas las rutas de este archivo): ya no hacen "if x is None:
# raise HTTPException(...)". Los controllers lanzan NoEncontrado / Conflicto
# y main.py los convierte en 404 / 409. Antes un código duplicado daba 404
# (incorrecto); ahora da 409. El parámetro de ruta pasó de {materia_id} a
# {id_materia} para coincidir con la BD.
@router.post("/", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: MateriaCreate, db: Session = Depends(get_db)):
    return registrar_materia(db, datos)


@router.get("/", response_model=list[MateriaRead])
def listar(db: Session = Depends(get_db)):
    return listar_materias(db)


@router.get("/{id_materia}", response_model=MateriaRead)
def obtener(id_materia: int, db: Session = Depends(get_db)):
    return obtener_materia(db, id_materia)


@router.put("/{id_materia}", response_model=MateriaRead)
def actualizar(id_materia: int, datos: MateriaUpdate, db: Session = Depends(get_db)):
    return actualizar_materia(db, id_materia, datos)


@router.delete("/{id_materia}")
def eliminar(id_materia: int, db: Session = Depends(get_db)):
    eliminar_materia(db, id_materia)
    return {"mensaje": "Materia eliminada correctamente"}
