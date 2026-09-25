import hashlib
import json

def cargar_hash_guardado():
    with open("config/security.json", "r") as f:
        datos = json.load(f)
    return datos["password_hash"]

def verificar_password(password_introducida):
    hash_introducido = hashlib.sha256(password_introducida.encode()).hexdigest()
    hash_guardado = cargar_hash_guardado()
    return hash_introducido == hash_guardado