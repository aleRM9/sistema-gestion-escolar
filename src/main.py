from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# CAMBIO: se importan los modelos académicos y sus tablas referenciadas para
# que SQLAlchemy registre las FKs declaradas por PROYECTO LENGUAJES.sql.
import src.models  # noqa: F401
from src.exceptions import Conflicto, NoEncontrado
from src.routes.inscripcion import router as inscripciones_router
from src.routes.materias import router as materias_router
from src.routes.notas import router as notas_router

# CAMBIO: se quitó el "lifespan" con Base.metadata.create_all(). Tenía dos
# fallos: (1) estaba definido pero nunca se pasaba a FastAPI(), así que no
# corría; (2) si hubiera corrido, habría chocado con el script .sql.
# Ahora el esquema se administra con PROYECTO LENGUAJES.sql (ver README), para
# mantener la base existente como fuente de verdad.
app = FastAPI(title="Sistema de Gestión Escolar")

app.include_router(materias_router)
app.include_router(notas_router)
app.include_router(inscripciones_router)


# CAMBIO: estos dos manejadores convierten los errores de src/exceptions.py
# en respuestas HTTP (404 y 409) en un solo lugar.
@app.exception_handler(NoEncontrado)
async def manejar_no_encontrado(request: Request, exc: NoEncontrado):
    return JSONResponse(status_code=404, content={"detail": exc.detalle})


@app.exception_handler(Conflicto)
async def manejar_conflicto(request: Request, exc: Conflicto):
    return JSONResponse(status_code=409, content={"detail": exc.detalle})


@app.get("/", tags=["Inicio"])
async def saludo():
    # CAMBIO: mensaje cambiado de "Hola, mundo!" a uno descriptivo.
    return {"message": "Sistema de Gestión Escolar: API en línea"}
