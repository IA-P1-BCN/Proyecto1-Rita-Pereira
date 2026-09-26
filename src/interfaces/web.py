from flask import Flask, jsonify, request, redirect, url_for, render_template, session
import os
from src.domain.carrera import Carrera
from src.interfaces.cli import cargar_tarifa
from src.infrastructure.historial import guardar_carrera, obtener_historial_dia
from src.infrastructure.auth import verificar_password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "redhead"

tarifa = cargar_tarifa()
carrera_activa = None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        nombre = request.form.get("nombre")
        if verificar_password(password):
            session["autenticado"] = True
            session["nombre"] = nombre
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Contraseña incorrecta")
    return render_template("login.html")

@app.route("/")
def home():
    if not session.get("autenticado"):
        return redirect(url_for("login"))
    return render_template("index.html", nombre=session.get("nombre"))

@app.route("/api/carrera/iniciar", methods=["POST"])
def iniciar_carrera():
    if not session.get("autenticado"): return jsonify({"error": "No autenticado"}), 401
    global carrera_activa
    if carrera_activa is not None:
        return jsonify({"error": "Ya hay una carrera en curso."}), 400
    else:
        carrera_activa = Carrera()
        return jsonify({"mensaje": "Carrera iniciada", "estado": carrera_activa.estado_actual})

@app.route("/api/carrera/estado", methods=["POST"])
def cambiar_estado():
    if not session.get("autenticado"): return jsonify({"error": "No autenticado"}), 401
    global carrera_activa
    if carrera_activa is None:
        return jsonify({"error": "No hay ninguna carrera activa."}), 400
    else:
        nuevo_estado = "movimiento" if carrera_activa.estado_actual == "parado" else "parado"
        carrera_activa.cambiar_estado(nuevo_estado)
        return jsonify({"mensaje": "Estado cambiado", "estado": nuevo_estado})

@app.route("/api/carrera/finalizar", methods=["POST"])
def finalizar_carrera():
    if not session.get("autenticado"): return jsonify({"error": "No autenticado"}), 401
    global carrera_activa
    if carrera_activa is None:
        return jsonify({"error": "No hay ninguna carrera activa."}), 400
    else:
        carrera_activa.finalizar_carrera()
        total = carrera_activa.calcular_total(tarifa)
        guardar_carrera(carrera_activa, tarifa)
        carrera_activa = None
        return jsonify({"mensaje": "Carrera finalizada", "total": round(total, 2)})

@app.route("/api/carrera/actual", methods=["GET"])
def carrera_actual():
    if not session.get("autenticado"): return jsonify({"error": "No autenticado"}), 401
    if carrera_activa is None:
        return jsonify({"activa": False})
    else:
        return jsonify({"activa": True, "estado": carrera_activa.estado_actual, "total": round(carrera_activa.total_actual(tarifa), 2)})

@app.route("/api/historial", methods=["GET"])
def ver_historial():
    if not session.get("autenticado"): return jsonify({"error": "No autenticado"}), 401
    historial = obtener_historial_dia()
    return jsonify(historial)

@app.route("/logout")
def logout():
    session.pop("autenticado", None)
    session.pop("nombre", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)