from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.exceptions import Conflicto


async def confirmar(db: AsyncSession, mensaje_conflicto: str) -> None:
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise Conflicto(mensaje_conflicto)
