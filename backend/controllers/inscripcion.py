from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.models.inscripcion import Inscripcion
from backend.models.materia import Materia
from backend.schemas.inscripcion import InscripcionCreate, InscripcionUpdate


def registrar_inscripcion(db: Session, datos: InscripcionCreate) -> Inscripcion:
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.alumno_id == datos.alumno_id,
        Inscripcion.materia_id == datos.materia_id
    ).first

    if inscripcion:
        return None

    try:
        inscripcion = Inscripcion(**datos.model_dump())
        db.add(inscripcion)
        db.commit()
        db.refresh(inscripcion)
        return inscripcion
    except IntegrityError:
        db.rollback()
        return None


def obtener_inscripcion(db: Session, inscripcion_id: int) -> Inscripcion | None:
    return db.get(Inscripcion, inscripcion_id)


def listar_inscripciones(db: Session) -> list[Inscripcion]:
    return db.query(Inscripcion).all()


def actualizar_inscripcion(
    db: Session,
    inscripcion_id: int,
    datos: InscripcionUpdate,
) -> Inscripcion | None:
    inscripcion = obtener_inscripcion(db, inscripcion_id)
    if inscripcion is None:
        return None

    cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
    for campo, valor in cambios.items():
        setattr(inscripcion, campo, valor)

    db.commit()
    db.refresh(inscripcion)
    return inscripcion


def eliminar_inscripcion(db: Session, inscripcion_id: int) -> Inscripcion | None:
    inscripcion = obtener_inscripcion(db, inscripcion_id)
    if inscripcion is None:
        return None

    db.delete(inscripcion)
    db.commit()
    return inscripcion