from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os

# Variables de entorno del contenedor de Docker
host = os.getenv("POSTGRES_HOST", "localhost")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "root_password")
db = os.getenv("POSTGRES_DB", "database")
port = os.getenv("POSTGRES_PORT", "5432")

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