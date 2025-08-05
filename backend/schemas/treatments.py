from pydantic import BaseModel, Field

class TreatmentResponse(BaseModel):
    treatment_date: str = Field(..., description="Fecha del tratamiento (YYYY-MM-DD)")
    start_time: int = Field(..., description="Hora de inicio del tratamiento (HH)")
    end_time: int = Field(..., description="Hora de fin del tratamiento (HH)")
    setpoint: float = Field(..., description="Setpoint del tratamiento (°C)")