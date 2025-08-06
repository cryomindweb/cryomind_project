from pydantic import BaseModel, Field
from typing import List

class TemperatureCreate(BaseModel):
    id_clinico: str = Field(..., description="ID clínico del paciente")
    marca_temporal: int = Field(..., description="Marca de tiempo de la temperatura (YYYY-MM-DD HH:MM:SS)")
    temperatura: float = Field(..., description="Temperatura del paciente en grados Celsius")

class TemperatureBatchStructure(BaseModel):
    marca_temporal: int = Field(..., description="Marca de tiempo de la temperatura (YYYY-MM-DD HH:MM:SS)")
    temperatura: float = Field(..., description="Temperatura del paciente en grados Celsius")

class TemperatureBatchCreate(BaseModel):
    id_clinico: str = Field(..., description="ID clínico del paciente")
    temperaturas: List[TemperatureBatchStructure] = Field(..., description="Lista de temperaturas a registrar")

class TemperatureResponse(BaseModel):
    marca_temporal: int = Field(..., description="Marca de tiempo de la temperatura (YYYY-MM-DD HH:MM:SS)")
    temperatura: float = Field(..., description="Temperatura del paciente en grados Celsius")
    marca_temporal_segundos: int = Field(..., description="Marca de tiempo en segundos")
    marca_temporal_horas: float = Field(..., description="Marca de tiempo en horas")

class TemperatureListResponse(BaseModel):
    id_clinico: str = Field(..., description="ID clínico del paciente")
    temperaturas: List[TemperatureResponse] = Field(..., description="Lista de temperaturas registradas")