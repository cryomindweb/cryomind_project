from pydantic import BaseModel, Field
from typing import List

class TemperatureCreate(BaseModel):
    timestamp: str = Field(..., description="Marca de tiempo de la temperatura (YYYY-MM-DD HH:MM:SS)")
    temperature: float = Field(..., description="Temperatura del paciente en grados Celsius")

class TemperatureBatchCreate(BaseModel):
    patient_clinic_id: str = Field(..., description="ID clínico del paciente")
    temperatures: List[TemperatureCreate] = Field(..., description="Lista de temperaturas a registrar")

class TemperatureResponse(BaseModel):
    timestamp: str = Field(..., description="Marca de tiempo de la temperatura (YYYY-MM-DD HH:MM:SS)")
    temperature: float = Field(..., description="Temperatura del paciente en grados Celsius")

class TemperatureListResponse(BaseModel):
    temperatures: List[TemperatureResponse] = Field(..., description="Lista de temperaturas registradas")