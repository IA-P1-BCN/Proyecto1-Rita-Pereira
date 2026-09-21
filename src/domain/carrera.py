import time

class Carrera:
    def __init__(self):
        self.hora_inicio = time.time()
        self.estado_actual = "parado"
        self.hora_inicio_estado_actual = time.time()
        self.segundos_parado = 0
        self.segundos_movimiento = 0
        self.hora_fin = None

    def cambiar_estado(self, nuevo_estado):
        ahora = time.time()
        segundos_transcurridos = ahora - self.hora_inicio_estado_actual

        if self.estado_actual == "parado":
            self.segundos_parado += segundos_transcurridos
        else:
            self.segundos_movimiento += segundos_transcurridos

        self.estado_actual = nuevo_estado
        self.hora_inicio_estado_actual = ahora

    def finalizar_carrera(self):
        ahora = time.time()
        segundos_transcurridos = ahora - self.hora_inicio_estado_actual

        if self.estado_actual == "parado":
            self.segundos_parado += segundos_transcurridos
        else:
            self.segundos_movimiento += segundos_transcurridos

        self.hora_fin = ahora

    def calcular_total(self, tarifa):
        return tarifa.calcular_coste(self.segundos_parado, self.segundos_movimiento)