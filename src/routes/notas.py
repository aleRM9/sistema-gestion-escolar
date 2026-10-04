from fastapi import APIRouter, Depends, Header, Query, status
from sqlalchemy.orm import Session

from src.controllers.notas import (
    actualizar_nota,
    eliminar_nota,
    listar_notas,
    obtener_nota,
    registrar_nota,
)
from src.controllers.reportes import calcular_promedio, generar_boletin
from src.database import get_db
from src.schemas.inscripcion import PATRON_PERIODO
from src.schemas.notas import NotaCreate, NotaRead, NotaUpdate

router = APIRouter(prefix="/notas", tags=["Notas"])


# CAMBIO (en todo el archivo): las rutas quedaron delgadas. La lógica del
# promedio y del boletín, que estaba aquí dentro, se movió a
# controllers/reportes.py. Los errores salen como 404 / 409 desde los
# controllers. El parámetro de ruta ahora es {id_notas} (nombre de la BD).
@router.post("/", response_model=NotaRead, status_code=status.HTTP_201_CREATED)
def crear(datos: NotaCreate, db: Session = Depends(get_db)):
    return registrar_nota(db, datos)


@router.get("/", response_model=list[NotaRead])
def listar(db: Session = Depends(get_db)):
    return listar_notas(db)


# CAMBIO: las rutas de reportes van ANTES que "/{id_notas}" para evitar
# ambigüedades de ruteo, y aceptan ?periodo=2025-2026 (opcional, validado con
# la misma regex que la inscripción).
@router.get("/promedio/{id_alumno}/{id_materia}")
def promedio(
    id_alumno: int,
    id_materia: int,
    periodo: str | None = Query(default=None, pattern=PATRON_PERIODO),
    db: Session = Depends(get_db),
):
    return calcular_promedio(db, id_alumno, id_materia, periodo)


@router.get("/boletin/{id_alumno}")
def boletin(
    id_alumno: int,
    periodo: str | None = Query(default=None, pattern=PATRON_PERIODO),
    db: Session = Depends(get_db),
):
    return generar_boletin(db, id_alumno, periodo)


@router.get("/{id_notas}", response_model=NotaRead)
def obtener(id_notas: int, db: Session = Depends(get_db)):
    return obtener_nota(db, id_notas)


@router.put("/{id_notas}", response_model=NotaRead)
def actualizar(
    id_notas: int,
    datos: NotaUpdate,
    usuario_id: int = Header(gt=0, alias="X-Usuario-Id"),
    db: Session = Depends(get_db),
):
    # CAMBIO: el SQL exige el usuario actor para auditar calificaciones; este
    # encabezado es provisional y debe sustituirse por la identidad autenticada.
    return actualizar_nota(db, id_notas, datos, usuario_id)


@router.delete("/{id_notas}")
def eliminar(id_notas: int, db: Session = Depends(get_db)):
    eliminar_nota(db, id_notas)
    return {"mensaje": "Nota eliminada correctamente"}
