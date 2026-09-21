import json
import os
from datetime import datetime

RUTA_HISTORIAL = "data/historial.json"

def guardar_carrera(carrera, tarifa):
    total = carrera.calcular_total(tarifa)

    nueva_entrada = {
        "hora_inicio": datetime.fromtimestamp(carrera.hora_inicio).isoformat(),
        "hora_fin": datetime.fromtimestamp(carrera.hora_fin).isoformat(),
        "segundos_parado": round(carrera.segundos_parado, 2),
        "segundos_movimiento": round(carrera.segundos_movimiento, 2),
        "total": round(total, 2)
    }

    historial = _leer_historial()
    historial.append(nueva_entrada)
    _escribir_historial(historial)

def obtener_historial_dia():
    historial = _leer_historial()
    hoy = datetime.now().date()

    carreras_hoy = []
    for entrada in historial:
        fecha_carrera = datetime.fromisoformat(entrada["hora_inicio"]).date()
        if fecha_carrera == hoy:
            carreras_hoy.append(entrada)

    return carreras_hoy

def _leer_historial():
    if not os.path.exists(RUTA_HISTORIAL):
        return []
    with open(RUTA_HISTORIAL, "r") as f:
        return json.load(f)

def _escribir_historial(historial):
    os.makedirs(os.path.dirname(RUTA_HISTORIAL), exist_ok=True)
    with open(RUTA_HISTORIAL, "w") as f:
        json.dump(historial, f, indent=4)