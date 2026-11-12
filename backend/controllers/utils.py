from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.exceptions import Conflicto

async def confirmar(db: AsyncSession, mensaje_conflicto: str) -> None:
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        
        
        constraint = getattr(exc.orig, 'constraint_name', None)
        sqlstate = getattr(exc.orig, 'sqlstate', None)
        
        # Mapeamos cada restricción a su mensaje específico
        if constraint == 'uq_materia_codigo':
            mensaje_final = "El código de la materia ya está registrado."
        elif constraint == 'uq_materia_nombre_grado': 
            mensaje_final = "Ya existe una materia con ese nombre en ese grado."
        elif constraint == 'uq_inscripcion_lapso':
            mensaje_final = "El estudiante ya tiene una nota registrada para este lapso."
        elif constraint == 'chk_valor_nota':
            mensaje_final = "La calificación debe estar entre 0 y 20."
        elif constraint == 'chk_lapso':
            mensaje_final = "El lapso académico debe ser 1, 2 o 3."
        
        #  Fallback usando el SQLState estándar de PostgreSQL
        elif sqlstate == '23503':  # Violación de Foreign Key (Clave foránea)
            mensaje_final = "No se puede procesar: el alumno, materia o curso asociado no existe."
        elif sqlstate == '23505':  # Violación general de Unicidad (Unique)
            mensaje_final = "Error de duplicidad: Ya existe un registro con esos datos."
        else:
            
            mensaje_final = mensaje_conflicto
            
        raise Conflicto(mensaje_final)
