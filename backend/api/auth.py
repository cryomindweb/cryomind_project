from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.supabase import supabase

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class LoginData(BaseModel):
    username: str  # email
    password: str

@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
def login(data: LoginData):
    """
    Autenticación de usuarios mediante Supabase.
    Retorna el JWT generado por Supabase junto con el rol desde la tabla 'usuarios'.
    """

    # 1. Autenticación con Supabase Auth
    auth_result = supabase.auth.sign_in_with_password({
        "email": data.username,
        "password": data.password
    })

    if not auth_result or not auth_result.session or not auth_result.user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    user = auth_result.user
    access_token = auth_result.session.access_token

    # 2. Obtener rol desde tabla personalizada 'usuarios'
    try:
        rol_resp = supabase.table("usuarios") \
            .select("rol") \
            .eq("usuario_id", user.id) \
            .single() \
            .execute()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al consultar el rol del usuario")

    if not rol_resp.data or "rol" not in rol_resp.data:
        raise HTTPException(status_code=403, detail="Usuario sin rol asignado")

    role = rol_resp.data["rol"]

    # 3. Devolver token + rol
    return TokenResponse(
        access_token=access_token,
        role=role
    )
