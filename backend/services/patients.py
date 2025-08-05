from services.supabase import supabase
from schemas.patients import PatientCreate
from fastapi import HTTPException

def create_patient_response(data: PatientCreate):
    try:
        insert_result = supabase.table("pacientes").insert({
            "patient_clinic_id": data.patient_clinic_id,
            "patient_name": data.patient_name,
            "patient_progenitor": data.patient_progenitor,
            "patient_birth_date": data.patient_birth_date,
            "patient_birth_hour": data.patient_birth_hour,
            "patient_birth_minute": data.patient_birth_minute,
            "patient_weight": data.patient_weight,
            "patient_gestation_weeks": data.patient_gestation_weeks,
            "patient_gestation_days": data.patient_gestation_days
        }).execute()
        if not insert_result.data:
            raise HTTPException(status_code=500, detail="No se pudo crear el paciente")
        patient_id = supabase.table("pacientes").select("paciente_id").eq("paciente_clinica_id", data.patient_clinic_id).execute().data[0]["paciente_id"]
        insert_result_tratment = supabase.table("tratamientos").insert({
            "paciente_id": patient_id,
            "treatment_date": data.treatment_date,
            "start_time": data.start_time,
            "end_time": data.end_time
        }).execute()
        return {
            "message": "Paciente creado exitosamente",
            "patient_id": insert_result.data[0]["id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando paciente: {str(e)}")

def create_patients_batch_response(data: list[PatientCreate]):
    responses = []
    for patient in data:
        response = create_patient_response(patient)
        responses.append(response)
    return responses

def patient_list_response():
    try:
        patients = supabase.table("pacientes").select("patient_clinic_id, patient_name").execute()
        return {"patients": patients.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pacientes: {str(e)}")

def get_patient_response(patient_clinic_id: str):
    try:
        patient = supabase.table("pacientes").select("*").eq("patient_clinic_id", patient_clinic_id).execute()
        if not patient.data:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return patient.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo paciente: {str(e)}")