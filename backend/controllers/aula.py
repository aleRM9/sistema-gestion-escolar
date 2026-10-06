from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.aula import Aula
from schemas.aula import AulaCreate, AulaUpdate

def crear_aula(db: Session, datos: AulaCreate) -> Aula | None:
    try:
        nueva_aula = Aula(**datos.model_dump())
        db.add(nueva_aula)
        db.commit()
        db.refresh(nueva_aula)
        return nueva_aula
    except IntegrityError:
        db.rollback()
        return None

def listar_aulas(db: Session) -> list[Aula]:
    return db.query(Aula).all()

def obtener_aula(db: Session, aula_id: int) -> Aula | None:
    return db.query(Aula).filter(Aula.aula_id == aula_id).first()

def actualizar_aula(db: Session, aula_id: int, datos: AulaUpdate) -> Aula | None:
    aula = obtener_aula(db, aula_id)
    if aula is None:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for key, value in cambios.items():
        setattr(aula, key, value)
        
    db.commit()
    db.refresh(aula)
    return aula

def eliminar_aula(db: Session, aula_id: int) -> Aula | None:
    aula = obtener_aula(db, aula_id)
    if aula is None:
        return None
        
    db.delete(aula)
    db.commit()
    return aula
