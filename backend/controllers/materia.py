from backend.models.materia import Materia
from backend.schemas.materia import MateriaCreate, MateriaUpdate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def registrar_materia(db: Session, datos:MateriaCreate):
    materia_existente = (
        db.query(Materia).filter(Materia.codigo == datos.codigo).first()
    )

    if materia_existente:
        return None
    try:
        materia = Materia(**datos.model_dump())
        db.add(materia)
        db.commit()
        db.refresh(materia)
        return materia
    except IntegrityError:
        db.rollback
        return None


def obtener_materia(db: Session, materia_id: int):
    return db.get(Materia, materia_id)


def listar_materias(db: Session):
    return db.query(Materia).all()


def actualizar_materia(db: Session, materia_id: int, datos: MateriaUpdate):
    materia = obtener_materia(db, materia_id)
    if materia is None:
        return None

    datos_dict = datos.model_dump(exclude_unset=True)

    for campo, valor in datos_dict.items():
        setattr(materia, campo, valor)

    db.commit()
    db.refresh(materia)
    return materia


def eliminar_materia(db: Session, materia_id: int):
    materia = obtener_materia(db, materia_id)
    if materia is None:
        return None

    db.delete(materia)
    db.commit()
    return materia