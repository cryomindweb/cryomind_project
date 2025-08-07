from fastapi import APIRouter, HTTPException
from schemas.patients import PatientAllDataCreate, PatientListResponse, PatientResponse, PatientBatchCreate
from schemas.treatments import TreatmentResponse
from services.patients import create_patient_service, patient_list_service, get_patient_service, create_patients_batch_service, PatientCreate
from services.treatments import create_treatment_service

router = APIRouter()

@router.post("/", status_code=201, summary="Registrar nuevo paciente")
def create_patient(data: PatientAllDataCreate):
    patient_data = {
            "id_clinico": data.id_clinico,
            "nombre_completo": data.nombre_completo,
            "nombre_progenitor": data.nombre_progenitor,
            "fecha_nacimiento": data.fecha_nacimiento,
            "hora_nacimiento": data.hora_nacimiento,
            "minuto_nacimiento": data.minuto_nacimiento,
            "peso": data.peso,
            "semanas_gestacion": data.semanas_gestacion,
            "dias_gestacion": data.dias_gestacion
        }
    tratment_data = {
            "id_clinico": data.id_clinico,
            "fecha_tratamiento": data.fecha_tratamiento,
            "hora_inicio": data.hora_inicio,
            "hora_finalizacion": data.hora_finalizacion,
            "observaciones": data.observaciones,
            "setpoint": data.setpoint
        }
    patient_status, patient_response = create_patient_service(PatientCreate(**patient_data)) # type: ignore
    if not patient_status:
        raise HTTPException(status_code=patient_response['status_code'], detail=patient_response['detail'])
    treatment_status, treatment_response = create_treatment_service(TreatmentResponse(**tratment_data)) # type: ignore
    if not treatment_status:
        raise HTTPException(status_code=treatment_response['status_code'], detail=treatment_response['detail'])
    return {"message": "Paciente y tratamiento creados exitosamente"}

#create many patients
@router.post("/batch", status_code=201, summary="Registrar varios pacientes")
def create_patients_batch(data: PatientBatchCreate):
    if not data.patients: # type: ignore
        raise HTTPException(status_code=400, detail="No se proporcionaron pacientes para crear")
    
    responses = create_patients_batch_service(data.patients) # type: ignore
    if not all(response[0] for response in responses):
        raise HTTPException(status_code=500, detail="Error al crear algunos pacientes")
    
    return {"message": "Pacientes creados exitosamente", "responses": responses}

@router.get("/", response_model=PatientListResponse, summary="Listar pacientes")
def list_patients():
    status, response = patient_list_service()
    if not status:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

@router.get("/{patient_clinic_id}", response_model=PatientResponse, summary="Obtener paciente por ID clinico")
def get_patient(patient_clinic_id: str):
    status, response = get_patient_service(patient_clinic_id)
    if not status:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

