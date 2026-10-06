from sqlalchemy.orm import query
from sqlalchemy.orm import Session
from backend.models.notas import Nota
from backend.schemas.notas import NotaCreate, NotaUpdate


def registrar_nota(db: Session, datos: NotaCreate) -> Nota:
    nota = Nota(**datos.model_dump())
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return nota


def obtener_nota(db: Session, nota_id: int) -> Nota | None:
    return db.get(Nota, nota_id)


def listar_notas(db: Session, inscripcion_id: int | None = None) -> list[Nota]:
    consulta = db.query(Nota)
    if inscripcion_id is not None:
        consulta = consulta.filter(Nota.inscripcion_id == inscripcion_id)
    return consulta.all()


def actualizar_nota(
    db: Session,
    nota_id: int,
    datos: NotaUpdate,
) -> Nota | None:
    nota = obtener_nota(db, nota_id)
    if nota is None:
        return None

    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    for campo, valor in cambios.items():
        setattr(nota, campo, valor)

    db.commit()
    db.refresh(nota)
    return nota


def eliminar_nota(db: Session, nota_id: int) -> Nota | None:
    nota = obtener_nota(db, nota_id)
    if nota is None:
        return None

    db.delete(nota)
    db.commit()
    return nota