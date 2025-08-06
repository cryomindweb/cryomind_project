from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre_usuario: str
    rol: str  # debe ser 'administrador' o 'medico'

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    nombre_usuario: Optional[str] = None
    rol: Optional[str] = None  # debe ser 'administrador' o 'medico'

class UserResponse(BaseModel):
    nombre_usuario: str
    rol: str  # debe ser 'administrador' o 'medico'
    email: EmailStr

class UserListResponse(BaseModel):
    users: list[UserResponse]

class UserDelete(BaseModel):
    user_id: int

