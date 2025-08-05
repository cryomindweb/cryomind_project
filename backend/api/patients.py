from fastapi import APIRouter
from schemas.patients import PatientCreate, PatientListResponse, PatientResponse, PatientBatchCreate
from services.patients import create_patient_response, patient_list_response, get_patient_response, create_patients_batch_response

router = APIRouter()

@router.post("/patients", status_code=201, summary="Registrar nuevo paciente")
def create_patient(data: PatientCreate):
    return create_patient_response(data)

#create many patients
@router.post("/patients/batch", status_code=201, summary="Registrar varios pacientes")
def create_patients_batch(data: PatientBatchCreate):
    return create_patients_batch_response(data.patients)

@router.get("/patients", response_model=PatientListResponse, summary="Listar pacientes")
def list_patients():
    return patient_list_response()

@router.get("/patients/{patient_clinic_id}", response_model=PatientResponse, summary="Obtener paciente por ID clinico")
def get_patient(patient_clinic_id: str):
    return get_patient_response(patient_clinic_id)

