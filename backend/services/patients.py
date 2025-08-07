from services.supabase import supabase
from schemas.patients import PatientCreate

def create_patient_service(data: PatientCreate):
    try:
        insert_result = supabase.table("pacientes").insert({
            "id_clinico": data.id_clinico,
            "nombre_completo": data.nombre_completo,
            "nombre_progenitor": data.nombre_progenitor,
            "fecha_nacimiento": data.fecha_nacimiento,
            "hora_nacimiento": data.hora_nacimiento,
            "minuto_nacimiento": data.minuto_nacimiento,
            "peso": data.peso,
            "semanas_gestacion": data.semanas_gestacion,
            "dias_gestacion": data.dias_gestacion
        }).execute()
        if not insert_result.data:
            return [False,  {'status_code': 500, 'detail': "No se pudo crear el paciente"}]
        return [True, {"message": "Paciente creado exitosamente"}]
    except Exception as e:
        return [False,  {'status_code': 500, 'detail': f"Error creando paciente: {str(e)}"}]

def create_patients_batch_service(data: list[PatientCreate]):
    responses = []
    for patient in data:
        response = create_patient_service(patient)
        responses.append(response)
    return responses

def patient_list_service():
    try:
        patients = supabase.table("pacientes").select("id_clinico, nombre_completo").execute()
        return [True, {"pacientes": patients.data or []}]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error al obtener pacientes: {str(e)}"}]


def get_patient_service(id_clinico: str):
    try:
        patient = supabase.table("pacientes").select("*").eq("id_clinico", id_clinico).execute()
        if not patient.data:
            return [False,  {'status_code': 500, 'detail': "Paciente no encontrado"}]
        return [True, patient.data[0]]
    except Exception as e:
        return [False,  {'status_code': 500, 'detail': f"Error obteniendo paciente: {str(e)}"}]