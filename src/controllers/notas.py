from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from src.controllers.utils import confirmar
from src.exceptions import Conflicto, NoEncontrado
from src.models.inscripcion import Inscripcion
from src.models.notas import Nota
from src.schemas.notas import NotaCreate, NotaUpdate

MENSAJE_LAPSO = "Ya existe una nota para esa inscripción en ese lapso"


# CAMBIO: función nueva. Una inscripción solo puede tener UNA nota por lapso
# (regla uq_inscripcion_lapso del SQL). Antes no se validaba y cargar dos
# veces el mismo lapso reventaba con un error 500 de la base de datos.
def _lapso_ocupado(
    db: Session, id_inscripcion: int, lapso: int, excluir_id: int | None = None
) -> bool:
    consulta = db.query(Nota).filter(
        Nota.inscripcion_id == id_inscripcion, Nota.lapso == lapso
    )
    if excluir_id is not None:
        consulta = consulta.filter(Nota.nota_id != excluir_id)
    return consulta.first() is not None


def registrar_nota(db: Session, datos: NotaCreate) -> Nota:
    # CAMBIO: el esquema y la columna SQL usan inscripcion_id; se comprueba
    # esa misma referencia antes de consultar o insertar la nota.
    if db.get(Inscripcion, datos.inscripcion_id) is None:
        raise NoEncontrado(f"La inscripción {datos.inscripcion_id} no existe")
    if _lapso_ocupado(db, datos.inscripcion_id, datos.lapso):
        raise Conflicto(MENSAJE_LAPSO)

    nota = Nota(**datos.model_dump())
    db.add(nota)
    confirmar(db, MENSAJE_LAPSO)
    db.refresh(nota)
    return nota


def obtener_nota(db: Session, id_notas: int) -> Nota:
    nota = db.get(Nota, id_notas)
    if nota is None:
        raise NoEncontrado("Nota no encontrada")
    return nota


def listar_notas(db: Session) -> list[Nota]:
    # CAMBIO: se ordena por la clave primaria nota_id definida en el SQL.
    return db.query(Nota).order_by(Nota.nota_id).all()


def actualizar_nota(
    db: Session, id_notas: int, datos: NotaUpdate, usuario_id: int
) -> Nota:
    nota = obtener_nota(db, id_notas)
    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)

    # CAMBIO: si se cambia el lapso, se valida que no choque con otra nota.
    nuevo_lapso = cambios.get("lapso")
    if nuevo_lapso is not None and _lapso_ocupado(
        db, nota.inscripcion_id, nuevo_lapso, excluir_id=id_notas
    ):
        raise Conflicto(MENSAJE_LAPSO)

    # CAMBIO: el trigger audita los cambios de calificación usando este valor
    # de transacción; sin establecerlo PostgreSQL rechaza la actualización.
    if cambios.get("calificacion") is not None and cambios["calificacion"] != nota.calificacion:
        usuario_existe = db.execute(
            text("SELECT 1 FROM usuarios WHERE usuario_id = :usuario_id"),
            {"usuario_id": usuario_id},
        ).scalar_one_or_none()
        if usuario_existe is None:
            raise NoEncontrado(f"El usuario {usuario_id} no existe")
        db.execute(
            select(func.set_config("app.current_user_id", str(usuario_id), True))
        )

    for campo, valor in cambios.items():
        setattr(nota, campo, valor)

    confirmar(db, MENSAJE_LAPSO)
    db.refresh(nota)
    return nota


def eliminar_nota(db: Session, id_notas: int) -> None:
    nota = obtener_nota(db, id_notas)
    db.delete(nota)
    confirmar(db, "No se pudo eliminar la nota")
