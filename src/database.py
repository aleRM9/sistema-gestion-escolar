import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()


# CAMBIO: función nueva. Antes, si faltaba una variable del .env, la app
# fallaba con un error confuso de conexión. Ahora avisa cuál variable falta.
def _requerida(nombre: str) -> str:
    valor = os.getenv(nombre)
    if not valor:
        raise RuntimeError(
            f"Falta la variable de entorno {nombre}. "
            "Crea tu archivo .env a partir de .env.example."
        )
    return valor


# CAMBIO: antes la URL se armaba con un f-string y variables llamadas USERNAME,
# PASSWORD, DATABASE, HOST y PORT. Problemas que tenía:
#   1) En Windows, USERNAME ya es una variable del sistema (tu usuario de
#      Windows) y load_dotenv() NO la sobrescribe: se conectaba a Postgres
#      con el usuario equivocado. Por eso ahora todas llevan prefijo DB_.
#   2) Una contraseña con caracteres como @ / : rompía el f-string.
#      URL.create() los escapa correctamente.
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=_requerida("DB_USER"),
    password=_requerida("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=_requerida("DB_NAME"),
)

# CAMBIO: pool_pre_ping evita errores cuando Postgres cierra conexiones viejas.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CAMBIO: se eliminó el "Base = declarative_base()" que estaba aquí. Había dos
# Base distintos (este y el de models/base.py) y solo uno se usaba. Ahora la
# única Base es la de src/models/base.py.


# Dependencia para abrir/cerrar la sesión en cada petición HTTP
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
