from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException
from backend.models.bloque import Bloque
async def hay_choque_horario( # Función asíncrona para validar choques de horarios
    db: AsyncSession,
    dia: str,
    hora_inicio: time,
    hora_fin: time,
    profesor_id: int,
    aula_id: int,
    curso_id: int,
    excluir_bloque_id: int | None = None,
) -> None:
    """
    Lanza HTTPException 409 si el nuevo bloque choca con alguno existente.
    Verifica 3 recursos independientes: profesor, aula y curso.
    """
    # Condición de solapamiento de horas en el mismo día
    solapamiento = and_(
        Bloque.dia == dia,
        Bloque.hora_inicio < hora_fin,
        Bloque.hora_fin > hora_inicio,
    )
    # Excluir el bloque actual en operaciones de edición
    filtro_exclusion = (
        Bloque.bloque_id != excluir_bloque_id
        if excluir_bloque_id is not None
        else True
    )
    # Tipos de conflictos (choques)
    conflictos = {
        "profesor": (
            Bloque.profesor_id == profesor_id,
            "El docente ya tiene una clase asignada en ese día y horario",
        ),
        "aula": (
            Bloque.aula_id == aula_id,
            "El aula ya está ocupada en ese día y horario",
        ),
        "curso": (
            Bloque.curso_id == curso_id,
            "El curso ya tiene otra materia asignada en ese día y horario",
        ),
    }
    for recurso, (condicion_recurso, mensaje) in conflictos.items():
        # Construir consulta
        stmt = (
            select(Bloque).filter(solapamiento, condicion_recurso, filtro_exclusion)
        )

        # Ejecución de consulta de forma asíncrona
        resultado = await db.execute(stmt)

        # Obtener primer registro de 'Bloque' mapeado bajo la condición de colisión
        choque = resultado.scalars().first()

        if choque: # Si hay colisión de bloques
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Conflicto de horario",
                    "recurso": recurso,
                    "mensaje": mensaje,
                    "bloque_en_conflicto": choque.bloque_id,
                },
            )
