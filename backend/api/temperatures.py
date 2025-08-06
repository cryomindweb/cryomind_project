from fastapi import APIRouter, HTTPException
from schemas.temperatures import TemperatureCreate, TemperatureListResponse
from services.temperatures import create_temperature_service, create_temperature_batch_service, temperature_list_service, get_temperature_service
from typing import List

router = APIRouter()

@router.post("/temperatures", status_code=201, summary="Registrar nueva temperatura")
def create_temperature(data: TemperatureCreate):
    status, response = create_temperature_service(data)
    if not status:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return {"message": "Temperatura creada exitosamente", "data": response['data']}

@router.post("/temperatures/batch", status_code=201, summary="Registrar varias temperaturas")
def create_temperature_batch(data: List[TemperatureCreate]):
    responses = create_temperature_batch_service(data)
    if not all(response[0] for response in responses):
        raise HTTPException(status_code=500, detail="Error al crear algunas temperaturas")
    return {"message": "Temperaturas creadas exitosamente", "data": [response[1]['data'] for response in responses if response[0]]}

@router.get("/temperatures/{id_clinico}", response_model=TemperatureListResponse, summary="Listar temperaturas por ID clínico")
def list_temperatures(id_clinico: str):
    status, response = temperature_list_service(id_clinico)
    if not status:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

@router.get("/temperatures/{id_clinico}/{marca_temporal}", summary="Obtener temperatura por ID clínico y marca temporal")
def get_temperature(id_clinico: str, marca_temporal: int):
    status, response = get_temperature_service(id_clinico, marca_temporal)
    if not status:
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    return response

