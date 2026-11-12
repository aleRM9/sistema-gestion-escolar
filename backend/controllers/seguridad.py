import os
from datetime import datetime, timedelta, UTC
from typing import Annotated
from jose import jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_


from backend.database import get_db_session
from backend.models.usuario import Usuario  
#from backend.models.rol import Rol

# 1. LEER LA CLAVE SECRETA DE LAS VARIABLES DE ENTORNO (Solución A1)
# Si no existe en el archivo .env, levantará un error inmediatamente al arrancar la app.
password = os.getenv("DB_JWT_SECRET", "Clave")


def _obtener_clave_secreta() -> str:
    if not password:
        raise RuntimeError("La variable de entorno 'DB_JWT_SECRET' no está configurada.")
    return password

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuración del esquema Bearer para interceptar el header 'Authorization'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# --- 2. ENCRIPTACIÓN DE CONTRASEÑAS (BCRYPT) ---

def hash_password(contrasenia_plana: str) -> str:
    """Convierte una contraseña de texto plano en un hash seguro e ilegible."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contrasenia_plana.encode('utf-8'), salt).decode('utf-8')


def verify_password(contrasenia_plana: str, contrasenia_hasheada: str) -> bool:
    """Compara una contraseña ingresada contra el hash seguro de la base de datos."""
    if not contrasenia_hasheada or not isinstance(contrasenia_hasheada, str):
        return False
        
    if not contrasenia_plana or not isinstance(contrasenia_plana, str):
        return False
    try:
        return bcrypt.checkpw(
           contrasenia_plana.encode('utf-8'), 
           contrasenia_hasheada.encode('utf-8')
        )
    except ValueError:
        return False

#GESTIÓN DE TOKENS JWT

def codificar_token(payload: dict) -> str:
    """Genera un token JWT firmado criptográficamente con vencimiento."""
    copia_payload = payload.copy()
    expiracion = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copia_payload.update({"exp": expiracion})
    
    return jwt.encode(copia_payload, _obtener_clave_secreta(), algorithm=ALGORITHM)

def verificar_roles(roles_permitidos: list[int]):
    """Dependencia de fábrica para validar si el rol del usuario está autorizado."""
    async def dependencia_rol(usuario: Usuario = Depends(decodificar_y_verificar_usuario)):
        print(f"Rol del usuario ID: {usuario.rol_id}")
        if usuario.rol_id not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para acceder a este recurso"
            )
        return usuario
    return dependencia_rol         

async def decodificar_y_verificar_usuario(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db_session)]
) -> Usuario:
    
    exception_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o sesión vencida. Inicie sesión de nuevo.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    #Decodificar el Token
    try:
        payload = jwt.decode(token, _obtener_clave_secreta(), algorithms=[ALGORITHM])
    
        identificador_web = payload.get("sub") or payload.get("username") or payload.get("email")
        
        if not identificador_web:
            raise exception_credenciales
    except jwt.PyJWTError as jwt_err:
        raise exception_credenciales

    #Consultar Base de Datos con OR seguro
    try:
        id_numerico = None
        if str(identificador_web).isdigit():
            id_numerico = int(identificador_web)

        condiciones = [
            Usuario.correo == str(identificador_web),
            Usuario.nombre_usuario == str(identificador_web)
        ]
        if id_numerico is not None:
            condiciones.append(Usuario.usuario_id == id_numerico)

        # Hacemos la consulta asíncrona
        query = select(Usuario).where(or_(*condiciones))
        resultado = await db.execute(query)
        usuario = resultado.scalars().first()
        
    except Exception as db_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la consulta de base de datos: {str(db_err)}"
        )

    if usuario is None:
        raise exception_credenciales    
        
    return usuario
