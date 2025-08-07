from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from authlib.jose import jwt
from core.config import settings
from services.supabase import supabase

security = HTTPBearer()

def require_admin(credentials=Depends(security)):
    token = credentials.credentials

    # Validar el token usando el secret de Supabase (Legacy JWT Secret)
    try:
        claims = jwt.decode(token, settings.jwt_secret_key)  # HS256 por defecto
        claims.validate()
        user_id = claims.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}"
        )

    # Verificar rol en la base de datos
    rol_resp = supabase.table("usuarios").select("rol").eq("usuario_id", user_id).execute()
    if not rol_resp.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no encontrado")

    if rol_resp.data[0]["rol"].lower() != "administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso solo para administradores")

def require_medico(credentials=Depends(security)):
    token = credentials.credentials

    # Validar el token usando el secret de Supabase (Legacy JWT Secret)
    try:
        claims = jwt.decode(token, settings.jwt_secret_key)  # HS256 por defecto
        claims.validate()
        user_id = claims.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido o expirado: {str(e)}"
        )

    # Verificar rol en la base de datos
    rol_resp = supabase.table("usuarios").select("rol").eq("usuario_id", user_id).single().execute()
    if not rol_resp.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no encontrado")

    if rol_resp.data["rol"].lower() != "medico":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso solo para médicos")