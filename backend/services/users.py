from services.supabase import supabase
from schemas.users import UserCreate, UserUpdate
from fastapi import HTTPException

def create_user(data: UserCreate):
    if data.rol.lower() not in ['administrador', 'medico']:
        raise HTTPException(status_code=400, detail="Rol inválido. Debe ser 'administrador' o 'medico'.")
    try:
        auth_result = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando usuario en Auth: {str(e)}")
    if not auth_result or not auth_result.user:
        raise HTTPException(status_code=500, detail="No se pudo crear el usuario en Auth")
    user_id = auth_result.user.id
    try:
        insert_result = supabase.table("usuarios").insert({
            "usuario_id": user_id,
            "nombre_usuario": data.nombre_usuario,
            "rol": data.rol.lower()
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error insertando en tabla usuarios: {str(e)}")
    return {
        "message": "Usuario creado exitosamente",
        "usuario_id": user_id,
        "nombre_usuario": data.nombre_usuario,
        "rol": data.rol
    }

def user_list_response():
    try:
        users = supabase.table("usuarios").select("*").execute()
        return {"users": users.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

def update_user_response(user_id: str, data: UserUpdate):
    if data.rol and data.rol not in ['administrador', 'medico']:
        raise HTTPException(status_code=400, detail="Rol inválido. Debe ser 'administrador' o 'medico'.")
    try:
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        update_result = supabase.table("usuarios").update(update_data).eq("usuario_id", user_id).execute()
        if update_result.count == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando usuario: {str(e)}")

def delete_user_response(user_id: str):
    try:
        delete_result = supabase.table("usuarios").delete().eq("usuario_id", user_id).execute()
        if delete_result.count == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando usuario: {str(e)}")

def get_user_response(nombre_usuario: str):
    try:
        user = supabase.table("usuarios").select("*").eq("nombre_usuario", nombre_usuario).execute()
        if not user.data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo usuario: {str(e)}")