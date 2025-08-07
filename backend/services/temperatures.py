from services.supabase import supabase
from schemas.temperatures import TemperatureCreate, TemperatureBatchCreate, TemperatureBatchStructure
from typing import List

def create_temperature_service(temperature_data: TemperatureCreate):
    marca_temporal_segundos = temperature_data.marca_temporal * 462
    marca_temporal_horas = marca_temporal_segundos / 3600
    try:
        data = {
            "id_clinico": temperature_data.id_clinico,
            "marca_temporal": temperature_data.marca_temporal,
            "temperatura": temperature_data.temperatura,
            "marca_temporal_segundos": marca_temporal_segundos,
            "marca_temporal_horas": marca_temporal_horas
        }
        response = supabase.table("temperaturas").insert(data).execute()
        if not response.data:
            return [False, {'status_code': 500, 'detail': "No se pudo crear la temperatura"}]
        return [True, {"message": "Temperatura creada exitosamente", "data": response.data[0]}]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error creando temperatura: {str(e)}"}]

def create_temperature_from_batch_service(temperature_data: TemperatureBatchStructure, id_clinico: str):
    marca_temporal_segundos = temperature_data.marca_temporal * 462
    marca_temporal_horas = marca_temporal_segundos / 3600
    try:
        data = {
            "id_clinico": id_clinico,
            "marca_temporal": temperature_data.marca_temporal,
            "temperatura": temperature_data.temperatura,
            "marca_temporal_segundos": marca_temporal_segundos,
            "marca_temporal_horas": marca_temporal_horas
        }
        response = supabase.table("temperaturas").insert(data).execute()
        if not response.data:
            return [False, {'status_code': 500, 'detail': "No se pudo crear la temperatura"}]
        return [True, {"message": "Temperatura creada exitosamente", "data": response.data[0]}]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error creando temperatura: {str(e)}"}]
    
def create_temperature_batch_service(temperatures_data: TemperatureBatchCreate):
    responses = []
    for temperature in temperatures_data.temperaturas:
        response = create_temperature_from_batch_service(temperature, temperatures_data.id_clinico)
        responses.append(response)
    return responses

def temperature_list_service(id_clinico: str):
    try:
        temperatures = supabase.table("temperaturas").select("temperatura, marca_temporal_horas").eq("id_clinico", id_clinico).order("marca_temporal_horas", desc=False).execute()
        if not temperatures.data:
            return [False, {'status_code': 404, 'detail': "No se encontraron temperaturas"}]
        return [True, {"temperaturas": temperatures.data}]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error al obtener temperaturas: {str(e)}"}]

def get_temperature_service(id_clinico: str, marca_temporal: int):
    try:
        temperature = supabase.table("temperaturas").select("*").eq("id_clinico", id_clinico).eq("marca_temporal", marca_temporal).execute()
        if not temperature.data:
            return [False, {'status_code': 404, 'detail': "Temperatura no encontrada"}]
        return [True, temperature.data[0]]
    except Exception as e:
        return [False, {'status_code': 500, 'detail': f"Error obteniendo temperatura: {str(e)}"}]
