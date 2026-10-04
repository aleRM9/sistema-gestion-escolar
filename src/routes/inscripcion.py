from fastapi import APIRouter, Depends, status
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


# CAMBIO (en todas las rutas de este archivo): mismo criterio que en
# routes/materias.py: los errores salen de los controllers (404 / 409) y el
# parámetro de ruta ahora es {id_inscripcion}. Antes, una inscripción
# duplicada respondía 404 "Inscripcion ya registrada", que era incorrecto.
@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
def crear(datos: InscripcionCreate, db: Session = Depends(get_db)):
    return registrar_inscripcion(db, datos)


@router.get("/", response_model=list[InscripcionRead])
def listar(db: Session = Depends(get_db)):
    return listar_inscripciones(db)


@router.get("/{id_inscripcion}", response_model=InscripcionRead)
def obtener(id_inscripcion: int, db: Session = Depends(get_db)):
    return obtener_inscripcion(db, id_inscripcion)


@router.put("/{id_inscripcion}", response_model=InscripcionRead)
def actualizar(
    id_inscripcion: int,
    datos: InscripcionUpdate,
    db: Session = Depends(get_db),
):
    return actualizar_inscripcion(db, id_inscripcion, datos)


@router.delete("/{id_inscripcion}")
def eliminar(id_inscripcion: int, db: Session = Depends(get_db)):
    eliminar_inscripcion(db, id_inscripcion)
    return {"mensaje": "Inscripción eliminada correctamente"}
