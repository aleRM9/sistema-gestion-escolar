from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.exceptions import Conflicto, NoEncontrado
from backend.database import Base, engine, get_db_session
from backend.routers import inscripcion, materias, notas, horarios, calificaciones, aulas, reportes_router, auth


from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Iniciar servidor fastAPI
app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db_session)):
    try:
        # Ejecuta una consulta extremadamente ligera para validar la conexión
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        # Si la BD está caída, fallará el execute y entrará aquí
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


# Evento de inicio para crear las tablas de forma asíncrona y segura
@app.on_event("startup")
async def startup_event():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tablas creadas o verificadas correctamente en la base de datos.")
    except Exception as e:
        print(f"Aviso: No se pudo conectar a la base de datos para crear tablas: {e}")

# Incluir los routers de la API
app.include_router(auth.router)
app.include_router(inscripcion.router)
app.include_router(materias.router)
app.include_router(notas.router)
app.include_router(horarios.router)
app.include_router(aulas.router)
app.include_router(calificaciones.router)
app.include_router(reportes_router.router)


origenes = [
    "http://localhost:3000", # Puerto del frontend
    "http://localhost:8000"  # Puerto del backend
]

# Handler de excepción "No encontrado"
@app.exception_handler(NoEncontrado)
async def _no_encontrado(_: Request, exc: NoEncontrado):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.detalle}
    )

# Handler de excepción "Conflicto"
@app.exception_handler(Conflicto)
async def _conflicto(_: Request, exc: Conflicto):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.detalle}
    )

# Agregar el middleware del sistema (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_methods=["*"],
    allow_headers=["*"],
)



