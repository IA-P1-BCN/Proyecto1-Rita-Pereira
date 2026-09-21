class Tarifa:
    def __init__(self, precio_parado, precio_movimiento):
        self.precio_parado = precio_parado
        self.precio_movimiento = precio_movimiento

    def calcular_coste(self, segundos_parado, segundos_movimiento):
        coste_parado = segundos_parado * self.precio_parado
        coste_movimiento = segundos_movimiento * self.precio_movimiento
        return coste_parado + coste_movimiento