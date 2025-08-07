from services.supabase import supabase
from schemas.users import UserCreate, UserUpdate

def create_user_service(data: UserCreate):
    if data.rol.lower() not in ['administrador', 'medico']:
        return [False, {'status_code': 400, 'detail': "Rol inválido. Debe ser 'administrador' o 'medico'."}]

    # 1. Crear el usuario en Auth
    try:
        auth_result = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error creando usuario en Auth: {str(e)}"}]

    if not auth_result or not auth_result.user:
        return [False, {'status_code': 500, 'detail': "No se pudo crear el usuario en Auth"}]

    user_id = auth_result.user.id

    # 2. Insertar en la tabla usuarios
    try:
        supabase.table("usuarios").insert({
            "usuario_id": user_id,
            "nombre_usuario": data.nombre_usuario,
            "rol": data.rol.lower(),
            "email": data.email  # Guardar el email también
        }).execute()
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error insertando en tabla usuarios: {str(e)}"}]

    return [True, {
        "message": "Usuario creado exitosamente",
        "usuario_id": user_id,
        "nombre_usuario": data.nombre_usuario,
        "rol": data.rol
    }]

def user_list_service():
    try:
        result = supabase.table("usuarios").select("*").execute()
        if not result.data:
            return [True, {"users": []}]
        return [True, {"users": result.data}]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error al obtener usuarios: {str(e)}"}]


def update_user_service(user_id: str, data: UserUpdate):
    if data.rol and data.rol not in ['administrador', 'medico']:
        return [False,  {'status_code': 400, 'detail': "Rol inválido. Debe ser 'administrador' o 'medico'."}]
    try:
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        update_result = supabase.table("usuarios").update(update_data).eq("usuario_id", user_id).execute()
        if update_result.count == 0:
            return [False,  {'status_code': 404, 'detail': "Usuario no encontrado"}]
        return [True, {"message": "Usuario actualizado exitosamente"}]
    except Exception as e:
        return [False,  {'status_code': 500, 'detail': f"Error actualizando usuario: {str(e)}"}]

def delete_user_service(user_id: str):
    try:
        # Eliminar de Auth (esto requiere service_role key)
        supabase.auth.admin.delete_user(user_id)
        # No es necesario eliminar de la tabla "usuarios" si tienes cascade delete
        return [True, {"message": "Usuario eliminado exitosamente"}]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error eliminando usuario: {str(e)}"}]


def get_user_service(nombre_usuario: str):
    try:
        user = supabase.table("usuarios").select("*").eq("nombre_usuario", nombre_usuario).execute()
        if not user.data:
            return [False,  {'status_code': 404, 'detail': "Usuario no encontrado"}]
        return [True, user.data[0]]
    except Exception as e:
        return [False,  {'status_code': 500, 'detail': f"Error obteniendo usuario: {str(e)}"}]