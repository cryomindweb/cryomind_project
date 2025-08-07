import requests
import random

# Configuración
API_URL = "http://localhost:8000/temperatures/temperatures/batch"  # Cambia por tu endpoint real
ID_CLINICO = "3190"  # ID clínico del paciente

TOTAL_MEDIDAS = 561

TEMP_INICIAL = 38.5
TEMP_OBJETIVO = 36.5

def generar_temperaturas():
    temperaturas = []

    # Fase 1: Descenso suave (primeras 8 horas aprox.)
    medidas_descenso = 62  # 8 horas ≈ 62 mediciones (8h*3600 / 462s)
    for i in range(medidas_descenso):
        temp = TEMP_INICIAL - (i / medidas_descenso) * (TEMP_INICIAL - TEMP_OBJETIVO)
        temp += random.uniform(-0.05, 0.05)  # variación leve
        temperaturas.append(round(temp, 2))

    # Fase 2: Estabilización
    medidas_estables = TOTAL_MEDIDAS - medidas_descenso
    for _ in range(medidas_estables):
        temp = TEMP_OBJETIVO + random.uniform(-0.2, 0.2)
        temperaturas.append(round(temp, 2))

    return temperaturas

def generar_batch():
    temperaturas = generar_temperaturas()
    batch_data = []

    for i, temp in enumerate(temperaturas):
        batch_data.append({
            "marca_temporal": i,
            "temperatura": temp
        })

    payload = {
        "id_clinico": ID_CLINICO,
        "temperaturas": batch_data
    }
    return payload

def enviar_batch():
    payload = generar_batch()
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 201:
        print("✅ Batch enviado correctamente")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    enviar_batch()
