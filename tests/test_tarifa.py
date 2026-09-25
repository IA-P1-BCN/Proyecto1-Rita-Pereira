from src.domain.tarifa import Tarifa

def test_calcular_coste():
    tarifa = Tarifa(0.02, 0.05)
    resultado = tarifa.calcular_coste(10, 10)
    assert resultado == 0.7, f"Se esperaba 0.7, pero se obtuvo {resultado}"

def test_todo_parado():
    tarifa = Tarifa(0.02, 0.05)
    resultado = tarifa.calcular_coste(10, 0)
    assert resultado == 0.2, f"Se esperaba 0.2, pero se obtuvo {resultado}"

def test_coste_0():
    tarifa = Tarifa(0.02, 0.05)
    resultado = tarifa.calcular_coste(0, 0)
    assert resultado == 0.0, f"Se esperaba 0.0, pero se obtuvo {resultado}"

def test_siempre_movimiento():
    tarifa = Tarifa(0.02, 0.05)
    resultado = tarifa.calcular_coste(0, 10)
    assert resultado == 0.5, f"Se esperaba 0.5, pero se obtuvo {resultado}"

def test_tarifa_gratuita():
    tarifa = Tarifa(0.0, 0.0)
    resultado = tarifa.calcular_coste(10, 10)
    assert resultado == 0.0, f"Se esperaba 0.0, pero se obtuvo {resultado}"