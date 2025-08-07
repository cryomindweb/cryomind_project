from pydantic import BaseModel, Field
from typing import List

class PatientCreate(BaseModel):
    id_clinico: str = Field(..., description="ID clinico del paciente")
    nombre_completo: str = Field(..., description="Nombre del paciente")
    nombre_progenitor: str = Field(..., description="Progenitor del paciente")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento del paciente (YYYY-MM-DD)")
    hora_nacimiento: int = Field(..., description="Hora de nacimiento del paciente (HH)")
    minuto_nacimiento: int = Field(..., description="Minuto de nacimiento del paciente (MM)")
    peso: float = Field(..., description="Peso del paciente al nacer (kg)")
    semanas_gestacion: int = Field(..., description="Semanas de gestación del paciente")
    dias_gestacion: int = Field(..., description="Días de gestación del paciente")

class PatientAllDataCreate(BaseModel):
    id_clinico: str = Field(..., description="ID clinico del paciente")
    nombre_completo: str = Field(..., description="Nombre del paciente")
    nombre_progenitor: str = Field(..., description="Progenitor del paciente")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento del paciente (YYYY-MM-DD)")
    hora_nacimiento: int = Field(..., description="Hora de nacimiento del paciente (HH)")
    minuto_nacimiento: int = Field(..., description="Minuto de nacimiento del paciente (MM)")
    peso: float = Field(..., description="Peso del paciente al nacer (kg)")
    semanas_gestacion: int = Field(..., description="Semanas de gestación del paciente")
    dias_gestacion: int = Field(..., description="Días de gestación del paciente")
    fecha_tratamiento: str = Field(..., description="Fecha del tratamiento (YYYY-MM-DD)")
    hora_inicio: str = Field(..., description="Hora de inicio del tratamiento (HH)")
    hora_finalizacion: str = Field(..., description="Hora de fin del tratamiento (HH)")
    observaciones: str = Field(..., description="Observaciones del tratamiento")
    setpoint: float = Field(..., description="Setpoint del tratamiento")

class PatientBatchCreate(BaseModel):
    pacientes: List[PatientAllDataCreate] = Field(..., description="Lista de pacientes a registrar en lote")

class PatientResponse(BaseModel):
    paciente_id: str = Field(..., description="ID del paciente")
    id_clinico: str = Field(..., description="ID clinico del paciente")
    nombre_completo: str = Field(..., description="Nombre del paciente")
    nombre_progenitor: str = Field(..., description="Progenitor del paciente")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento del paciente (YYYY-MM-DD)")
    hora_nacimiento: int = Field(..., description="Hora de nacimiento del paciente (HH)")
    minuto_nacimiento: int = Field(..., description="Minuto de nacimiento del paciente (MM)")
    peso: float = Field(..., description="Peso del paciente al nacer (kg)")
    semanas_gestacion: int = Field(..., description="Semanas de gestación del paciente")
    dias_gestacion: int = Field(..., description="Días de gestación del paciente")

class PatientShortResponse(BaseModel):
    id_clinico: str = Field(..., description="ID clinico del paciente")
    nombre_completo: str = Field(..., description="Nombre del paciente")

class PatientListResponse(BaseModel):
    pacientes: List[PatientShortResponse] = Field(..., description="Lista de pacientes")