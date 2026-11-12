from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.aula import Aula
from backend.schemas.aula import AulaCreate, AulaUpdate

async def crear_aula(db: AsyncSession, datos: AulaCreate) -> Aula | None:
    try:
        nueva_aula = Aula(**datos.model_dump())
        db.add(nueva_aula)
        db.commit()
        db.refresh(nueva_aula)
        return nueva_aula
    except IntegrityError:
        db.rollback()
        return None

async  def listar_aulas(db: AsyncSession) -> list[Aula]:
    return db.query(Aula).all()

async def obtener_aula(db: AsyncSession, aula_id: int) -> Aula | None:
    return db.query(Aula).filter(Aula.aula_id == aula_id).first()

async def actualizar_aula(db: AsyncSession, aula_id: int, datos: AulaUpdate) -> Aula | None:
    aula = obtener_aula(db, aula_id)
    if aula is None:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for key, value in cambios.items():
        setattr(aula, key, value)
        
    db.commit()
    db.refresh(aula)
    return aula

async def eliminar_aula(db: AsyncSession, aula_id: int) -> Aula | None:
    aula = obtener_aula(db, aula_id)
    if aula is None:
        return None
        
    db.delete(aula)
    db.commit()
    return aula
