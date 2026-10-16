from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Enlace para la conexión con la base de datos. psycopg2 es un driver para PostgreSQL
db_url = "postgresql+psycopg2://postgres:root_password@localhost:5432/sistema-gestion-escolar"

# Actua como puerto de entrada y base de conexiones entre la base de datos y el backend en Python
engine = create_engine(db_url, echo=True)

# Creación de sesión, la cual gestiona operaciones de lectura y escritura, así como las transacciones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)