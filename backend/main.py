from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models.base import Base
from routers import inscripcion, materias, notas, horarios, calificaciones, reportes, aulas

# Aplicar manejo de excepciones para la conexión con base de datos
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Aviso: No se pudo conectar a la base de datos para crear tablas: {e}")


# Inicializar servidor fastAPI
app = FastAPI()
app.include_router(inscripcion.router)
app.include_router(materias.router)
app.include_router(notas.router)
app.include_router(horarios.router)
app.include_router(aulas.router)
app.include_router(calificaciones.router)
app.include_router(reportes.router)


origenes = [
    "http://localhost:3000", # Puerto del frontend
    "http://localhost:8000" # Puerto del backend
]

# Agregar el middleware del sistema
app.add_middleware(
    CORSMiddleware, # Habilita el Intercambio de Recursos de Origen Cruzado(CORS)
    allow_origins=origenes, # Especifica la ruta los puertos
    allow_methods= ["*"] # Permite todos los métodos del backend
)
