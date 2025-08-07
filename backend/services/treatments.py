from services.supabase import supabase
from schemas.treatments import TreatmentResponse

def create_treatment_service(data: TreatmentResponse):
    try:
        insert_result = supabase.table("tratamientos").insert({
            "id_clinico": data.id_clinico,
            "fecha_tratamiento": data.fecha_tratamiento,
            "hora_inicio": data.hora_inicio,
            "hora_finalizacion": data.hora_finalizacion,
            "observaciones": data.observaciones,
            "setpoint": data.setpoint
        }).execute()
        if not insert_result.data:
            return [False,  {'status_code': 500, 'detail': "No se pudo crear el tratamiento"}]
        return [True, {"message": "Tratamiento creado exitosamente"}]
    except Exception as e:
        return [False,  {'status_code': 500, 'detail': f"Error creando tratamiento: {str(e)}"}]

def get_treatment_service(id_clinico: str):
    try:
        treatment = supabase.table("tratamientos").select("id_clinico, fecha_tratamiento, hora_inicio, hora_finalizacion, observaciones, setpoint").eq("id_clinico", id_clinico).execute()
        print(treatment.data)
        if not treatment.data:
            print("Tratamiento no encontrado")
            return [False,  {'status_code': 500, 'detail': "Tratamiento no encontrado"}]
        return [True, TreatmentResponse(**treatment.data[0])]
    except Exception as e:
        print(f"Error obteniendo tratamiento: {str(e)}")
        return [False,  {'status_code': 500, 'detail': f"Error obteniendo tratamiento: {str(e)}"}]