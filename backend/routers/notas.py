from fastapi import HTTPException , APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.notas import NotaCreate, NotaUpdate, NotaRead
from backend.controllers.notas import (
    actualizar_nota,
    eliminar_nota,
    listar_notas,
    obtener_nota,
    registrar_nota,
)
from backend.database import get_db  


router = APIRouter(prefix="/notas", tags=["Notas"])


@router.post("/", response_model=NotaRead, status_code=201)
def crear(datos: NotaCreate, db: Session = Depends(get_db)):
    return registrar_nota(db, datos)


@router.get("/", response_model=list[NotaRead])
def listar(db: Session = Depends(get_db)):
    return listar_notas(db)


@router.get("/{nota_id}", response_model=NotaRead)
def obtener(nota_id: int, db: Session = Depends(get_db)):
    nota = obtener_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota

@router.put("/{nota_id}", response_model=NotaRead)
def actualizar(
    nota_id: int,
    datos: NotaUpdate,
    db: Session = Depends(get_db),
):
    nota = actualizar_nota(db, nota_id, datos)
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota


@router.delete("/{nota_id}")
def eliminar(nota_id: int, db: Session = Depends(get_db)):
    nota = eliminar_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return {"mensaje": "Nota eliminada correctamente"}