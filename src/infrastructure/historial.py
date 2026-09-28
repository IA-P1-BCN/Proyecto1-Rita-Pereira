import sqlite3
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
DB_FILE = os.path.join(DATA_DIR, "historial.db")


def _conectar():
    os.makedirs(DATA_DIR, exist_ok=True)
    conexion = sqlite3.connect(DB_FILE)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carreras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            hora_inicio TEXT,
            hora_fin TEXT,
            total REAL
        )
    """)
    conexion.commit()
    return conexion


def guardar_carrera(carrera, tarifa):
    """Guarda una carrera finalizada en el historial persistente (SQLite)."""
    conexion = _conectar()
    cursor = conexion.cursor()

    fecha = datetime.fromtimestamp(carrera.hora_inicio).strftime("%Y-%m-%d")
    hora_inicio = datetime.fromtimestamp(carrera.hora_inicio).strftime("%H:%M:%S")
    hora_fin = datetime.fromtimestamp(carrera.hora_fin).strftime("%H:%M:%S") if carrera.hora_fin else ""
    total = round(carrera.calcular_total(tarifa), 2)


    cursor.execute(
        "INSERT INTO carreras (fecha, hora_inicio, hora_fin, total) VALUES (?, ?, ?, ?)",
        (fecha, hora_inicio, hora_fin, total)
    )
    conexion.commit()
    conexion.close()


def obtener_historial_dia(fecha: str = None) -> list:
    """Devuelve las carreras registradas en la fecha indicada (por defecto, hoy)."""
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")

    conexion = _conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT fecha, hora_inicio, hora_fin, total FROM carreras WHERE fecha = ?",
        (fecha,)
    )
    filas = cursor.fetchall()
    conexion.close()

    return [
        {"fecha": fila[0], "hora_inicio": fila[1], "hora_fin": fila[2], "total": fila[3]}
        for fila in filas
    ]