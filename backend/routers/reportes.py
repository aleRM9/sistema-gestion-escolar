from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.notas import Nota
from models.inscripcion import Inscripcion
from models.alumno import Alumno
from models.bloque import Bloque
from models.aula import Aula
from models.profesor import Profesor
from schemas.reportes_schema import ReporteEstudiantes, ReportePromedio, ReporteGeneral


router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/estudiantes", response_model=ReporteEstudiantes)
def reporte_estudiantes(db: Session = Depends(get_db)):
    # Devuelve el total de estudiantes registrados en el sistema.
    total = db.query(func.count(Alumno.alumno_id)).scalar()
    return ReporteEstudiantes(total_estudiantes=total)


@router.get("/promedio/{inscripcion_id}", response_model=ReportePromedio)
def reporte_promedio_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    # Calcula el promedio de notas de una inscripción específica.
    promedio = (
        db.query(func.avg(Nota.calificacion))
        .filter(Nota.inscripcion_id == inscripcion_id)
        .scalar()
    )
    if promedio is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron notas para esta inscripción",
        )
    return ReportePromedio(estudiante_id=inscripcion_id, promedio=float(promedio))


@router.get("/general", response_model=ReporteGeneral)
def reporte_general(db: Session = Depends(get_db)):
    # Genera un reporte general: total de estudiantes, aprobados y reprobados (nota mínima de aprobación: 10).
    NOTA_APROBACION = 10.0

    total_estudiantes = db.query(func.count(Alumno.alumno_id)).scalar()

    # Subconsulta: promedio por inscripción
    promedios = (
        db.query(
            Nota.inscripcion_id,
            func.avg(Nota.calificacion).label("promedio"),
        )
        .group_by(Nota.inscripcion_id)
        .subquery()
    )

    total_aprobados = (
        db.query(func.count())
        .filter(promedios.c.promedio >= NOTA_APROBACION)
        .scalar()
    )
    total_reprobados = (
        db.query(func.count())
        .filter(promedios.c.promedio < NOTA_APROBACION)
        .scalar()
    )

    return ReporteGeneral(
        total_estudiantes=total_estudiantes or 0,
        total_aprobados=total_aprobados or 0,
        total_reprobados=total_reprobados or 0,
    )


@router.get("/horarios")
def reporte_horarios(db: Session = Depends(get_db)):
    # Devuelve el listado completo de bloques horarios registrados.
    return db.query(Bloque).all()


@router.get("/aulas")
def reporte_aulas(db: Session = Depends(get_db)):
    # Devuelve el listado completo de aulas con su disponibilidad.
    return db.query(Aula).all()


@router.get("/docentes")
def reporte_docentes(db: Session = Depends(get_db)):
    # Devuelve el listado completo de profesores registrados.
    return db.query(Profesor).all()
