from fastapi import APIRouter, HTTPException
from schemas.treatments import TreatmentResponse
from services.treatments import get_treatment_service

router = APIRouter()

@router.get("/{patient_id}", response_model=TreatmentResponse, summary="Obtener tratamiento por ID de paciente")
def get_treatment(patient_id: str):
    success, response = get_treatment_service(patient_id)
    if not success:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response