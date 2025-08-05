from fastapi import APIRouter
from services.users import create_user, user_list_response, update_user_response, delete_user_response, get_user_response
from schemas.users import UserCreate, UserListResponse, UserUpdate, UserUpdate, UserResponse

router = APIRouter()

@router.post("/signup", status_code=201, summary="Registrar nuevo usuario")
def signup(data: UserCreate):
    return create_user(data)

@router.get("/users", response_model=UserListResponse, summary="Listar usuarios")
def users_list():
    return user_list_response()

@router.put("/users/{user_id}", response_model=UserUpdate, summary="Actualizar usuario")
def update_user(user_id: str, data: UserUpdate):
    return update_user_response(user_id, data)

@router.delete("/users/{user_id}", status_code=200, summary="Eliminar usuario")
def delete_user(user_id: str):
    return delete_user_response(user_id)

@router.get("/users/{nombre_usuario}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(nombre_usuario: str):
    return get_user_response(nombre_usuario)