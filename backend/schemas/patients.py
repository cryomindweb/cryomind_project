from pydantic import BaseModel, Field
from typing import List

class PatientCreate(BaseModel):
    patient_clinic_id: str = Field(..., description="ID clinico del paciente")
    patient_name: str = Field(..., description="Nombre del paciente")
    patient_progenitor: str = Field(..., description="Progenitor del paciente")
    patient_birth_date: str = Field(..., description="Fecha de nacimiento del paciente (YYYY-MM-DD)")
    patient_birth_hour: int = Field(..., description="Hora de nacimiento del paciente (HH)")
    patient_birth_minute: int = Field(..., description="Minuto de nacimiento del paciente (MM)")
    patient_weight: float = Field(..., description="Peso del paciente al nacer (kg)")
    patient_gestation_weeks: int = Field(..., description="Semanas de gestación del paciente")
    patient_gestation_days: int = Field(..., description="Días de gestación del paciente")
    treatment_date: str = Field(..., description="Fecha del tratamiento (YYYY-MM-DD)")
    start_time: int = Field(..., description="Hora de inicio del tratamiento (HH)")
    end_time: int = Field(..., description="Hora de fin del tratamiento (HH)")

class PatientBatchCreate(BaseModel):
    patients: List[PatientCreate] = Field(..., description="Lista de pacientes a registrar en lote")

class PatientResponse(BaseModel):
    patient_id: str = Field(..., description="ID del paciente")
    patient_clinic_id: str = Field(..., description="ID clinico del paciente")
    patient_name: str = Field(..., description="Nombre del paciente")
    patient_progenitor: str = Field(..., description="Progenitor del paciente")
    patient_birth_date: str = Field(..., description="Fecha de nacimiento del paciente (YYYY-MM-DD)")
    patient_birth_hour: int = Field(..., description="Hora de nacimiento del paciente (HH)")
    patient_birth_minute: int = Field(..., description="Minuto de nacimiento del paciente (MM)")
    patient_weight: float = Field(..., description="Peso del paciente al nacer (kg)")
    patient_gestation_weeks: int = Field(..., description="Semanas de gestación del paciente")
    patient_gestation_days: int = Field(..., description="Días de gestación del paciente")

class PatientShortResponse(BaseModel):
    patient_clinic_id: str = Field(..., description="ID clinico del paciente")
    patient_name: str = Field(..., description="Nombre del paciente")

class PatientListResponse(BaseModel):
    patients: List[PatientShortResponse] = Field(..., description="Lista de pacientes")