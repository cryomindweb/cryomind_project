from fastapi import APIRouter, Depends, HTTPException
from services.users import create_user_service, user_list_service, update_user_service, delete_user_service, get_user_service
from schemas.users import UserCreate, UserListResponse, UserUpdate, UserUpdate, UserResponse
from core.dependencies import require_admin

router = APIRouter()

@router.post("/signup", status_code=201, summary="Registrar nuevo usuario")
def signup(data: UserCreate, user: dict = Depends(require_admin)):
    success, response = create_user_service(data)
    if not success:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

@router.get("/users", response_model=UserListResponse, summary="Listar usuarios")
def users_list(user: dict = Depends(require_admin)):
    success, response = user_list_service()
    if not success:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

@router.put("/users/{user_id}", response_model=UserUpdate, summary="Actualizar usuario")
def update_user(user_id: str, data: UserUpdate, user: dict = Depends(require_admin)):
    success, response = update_user_service(user_id, data)
    if not success:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

@router.delete("/users/{user_id}", status_code=200, summary="Eliminar usuario")
def delete_user(user_id: str, user: dict = Depends(require_admin)):
    success, response = delete_user_service(user_id)
    if not success:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

@router.get("/users/{nombre_usuario}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(nombre_usuario: str, user: dict = Depends(require_admin)):
    success, response = get_user_service(nombre_usuario)
    if not success:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response