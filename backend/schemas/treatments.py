from pydantic import BaseModel, Field
from typing import Optional

class TreatmentResponse(BaseModel):
    id_clinico: str = Field(..., description="ID clinico del paciente")
    fecha_tratamiento: str = Field(..., description="Fecha del tratamiento (YYYY-MM-DD)")
    hora_inicio: str = Field(..., description="Hora de inicio del tratamiento (HH)")
    hora_finalizacion: str = Field(..., description="Hora de fin del tratamiento (HH)")
    observaciones: Optional[str] = Field(..., description="Observaciones del tratamiento")
    setpoint: float = Field(..., description="Setpoint del tratamiento")