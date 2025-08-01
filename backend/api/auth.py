from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.supabase import supabase
from pydantic import BaseModel

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    
class LoginData(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=TokenResponse)
def login(data: LoginData):
    # 1. Iniciar sesión con Supabase
    print("Attempting to log in with Supabase...")
    auth_result = supabase.auth.sign_in_with_password({
        "email": data.username,
        "password": data.password
    })
    if not auth_result or not auth_result.session or not auth_result.user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user = auth_result.user
    access_token = auth_result.session.access_token

    # 2. Obtener rol desde tu tabla "usuarios"
    rol_resp = supabase.table("usuarios").select("rol").eq("usuario_id", user.id).single().execute()
    if rol_resp.data is None:
        raise HTTPException(status_code=403, detail="Usuario sin rol asignado")

    role = rol_resp.data["rol"]
    print(f"User role retrieved: {role}")
    # 3. Retornar el token de Supabase + rol
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role
    }