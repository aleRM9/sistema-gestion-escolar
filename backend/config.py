from pydantic_settings import BaseSettings, SettingsConfigDict

# Clase Settings para centralizar, validar y cargar variables de entorno
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str # obligatorio: si falta, la app no arranca
    debug: bool = False