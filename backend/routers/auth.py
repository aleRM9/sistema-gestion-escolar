from typing import Annotated
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from backend.controllers.seguridad import verificar_roles
from backend.controllers.seguridad import codificar_token, verify_password, decodificar_y_verificar_usuario, oauth2_scheme
from backend.database import get_db_session
from backend.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/token")
async def inicio_sesion(
    forma: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db_session)]
) -> dict:
    
    """Endpoint único de login para todo el sistema."""
    # 1. Buscar al usuario en la BD de forma asíncrona por su correo/username
    resultado = await db.execute(select(Usuario).where(or_(Usuario.correo == forma.username ,Usuario.nombre_usuario == forma.username) ))
    usuario = resultado.scalar_one_or_none()
    
    # 2. Verificar existencia y contrastar contraseña con bcrypt
    if not usuario or not verify_password(forma.password, usuario.contrasenia):
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="El correo electrónico o la contraseña son incorrectos"
                )
        
    # 3. Codificar el token seguro con tu función del controlador
    token_generado = codificar_token({"sub": str(usuario.usuario_id)})
    
    # Format exigido por el estándar OAuth2 de FastAPI
    return {"access_token": token_generado}


@router.get("/datos")
async def obtener_datos_usuario(
    usuario: Usuario = Depends(verificar_roles([1,2]))
) -> dict:
    return {
        "Correo": usuario.correo,
        "Usuario": usuario.nombre_usuario,
        "Fecha de Registro": usuario.fecha_creacion
    }