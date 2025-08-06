from pydantic import BaseModel, Field

class TreatmentResponse(BaseModel):
    id_clinico: str = Field(..., description="ID clinico del paciente")
    fecha_tratamiento: str = Field(..., description="Fecha del tratamiento (YYYY-MM-DD)")
    hora_inicio: int = Field(..., description="Hora de inicio del tratamiento (HH)")
    hora_finalizacion: int = Field(..., description="Hora de fin del tratamiento (HH)")
    setpoint: float = Field(..., description="Setpoint del tratamiento")