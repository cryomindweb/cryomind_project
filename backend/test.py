#!/usr/bin/env python3
"""
Prueba RPC Supabase - insertar_temperatura (FUNCTION RETURNS void)

Ajusta SUPABASE_URL y API_KEY con los valores de tu proyecto.
Ejecutar: python3 prueba_insertar_temperatura.py
"""

import requests
import json
import sys

# --- CONFIGURAR ---
SUPABASE_URL = "https://svwkhvfysjkobyjzlfqe.supabase.co"   # p.ej. https://abcd1234.supabase.co
RPC_NAME = "insertar_temperatura"                    # nombre de la función
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2d2todmZ5c2prb2J5anpsZnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4ODkwODAsImV4cCI6MjA2OTQ2NTA4MH0.zpWaKG1Gs9rpOrKvahQhAGhyO74Pzhv6lZ1wg_QruKI"
TIMEOUT = 30  # segundos
# -------------------

ENDPOINT = f"{SUPABASE_URL}/rest/v1/rpc/{RPC_NAME}"

# JSON de ejemplo provisto (p_id_clinico contiene un array de objetos)
payload = {
  "p_id_clinico": [
    { "p_id_clinico": "4999", "p_marca_temporal": 0, "p_temperatura": 38 },
    { "p_id_clinico": "4999", "p_marca_temporal": 1, "p_temperatura": 38 },
    { "p_id_clinico": "4999", "p_marca_temporal": 2, "p_temperatura": 37.9 },
    { "p_id_clinico": "4999", "p_marca_temporal": 3, "p_temperatura": 37.9 },
    { "p_id_clinico": "4999", "p_marca_temporal": 4, "p_temperatura": 37.8 },
    { "p_id_clinico": "4999", "p_marca_temporal": 5, "p_temperatura": 37.8 },
    { "p_id_clinico": "4999", "p_marca_temporal": 6, "p_temperatura": 37.8 },
    { "p_id_clinico": "4999", "p_marca_temporal": 7, "p_temperatura": 37.7 },
    { "p_id_clinico": "4999", "p_marca_temporal": 8, "p_temperatura": 37.7 },
    { "p_id_clinico": "4999", "p_marca_temporal": 9, "p_temperatura": 37.6 }
  ]
}

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def main():
    print("Endpoint:", ENDPOINT)
    print("Enviando payload ({} registros)...".format(len(payload["p_id_clinico"])))
    try:
        r = requests.post(ENDPOINT, headers=headers, json=payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        print("Error al conectar:", e)
        sys.exit(1)

    print("Código HTTP:", r.status_code)

    # Función RETURNS void típicamente retorna 204 No Content o 200 con cuerpo vacío.
    if r.status_code == 204:
        print("OK: 204 No Content (la función se ejecutó correctamente).")
        return
    if 200 <= r.status_code < 300:
        # Si hay contenido en la respuesta, mostrarlo
        if r.text and r.text.strip():
            try:
                print("Respuesta JSON:", r.json())
            except ValueError:
                print("Respuesta (texto):", r.text)
        else:
            print("OK: respuesta 2xx sin contenido.")
        return

    # Si llegamos aquí, hubo un error (4xx/5xx)
    print("ERROR: la función devolvió código de error.")
    # Supabase suele devolver JSON con detalles del error; intentar parsearlo
    try:
        err = r.json()
        print(json.dumps(err, indent=2, ensure_ascii=False))
    except ValueError:
        print("Cuerpo de respuesta:", r.text)

    sys.exit(2)

if __name__ == "__main__":
    if "<TU_API_KEY_AQUI>" in API_KEY or "<tu-proyecto>" in SUPABASE_URL:
        print("✖ Por favor edita SUPABASE_URL y API_KEY en el script antes de ejecutar.")
        sys.exit(1)
    main()
