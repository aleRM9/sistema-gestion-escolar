from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.exceptions import Conflicto


# CAMBIO: archivo/función nueva. Antes cada controller hacía su propio
# try/except con el commit, y en materia.py el rollback estaba mal escrito
# ("db.rollback" sin paréntesis, no se ejecutaba). Ahora hay un solo lugar:
# si la BD rechaza la operación (duplicado, llave foránea), deshace la
# transacción y lanza Conflicto (HTTP 409).
def confirmar(db: Session, mensaje_conflicto: str) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # con paréntesis: ahora sí se ejecuta
        raise Conflicto(mensaje_conflicto)
