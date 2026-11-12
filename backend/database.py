from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os
from backend.models.base import Base

load_dotenv()

# Variables de entorno del contenedor de Docker
host = os.getenv("DB_HOST") or os.getenv("POSTGRES_HOST", "database")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")

# Enlace para la conexión con la base de datos. asyncpg es un driver asíncrono para PostgreSQL
DB_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
)

# Actua como puerto de entrada y base de conexiones entre la base de datos y el backend en Python
engine = create_async_engine(DB_URL, echo=True)
# Creación de sesión asíncrona, la cual gestiona operaciones de lectura y escritura, así como las transacciones
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Función generadora de sesión en la base de datos
async def get_db_session():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()