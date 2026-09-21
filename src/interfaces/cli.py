from src.domain.carrera import Carrera
from src.domain.tarifa import Tarifa

def cargar_tarifa():
    tarifa = Tarifa(0.02, 0.05)
    return tarifa

def mostrar_menu():
    print("\n--- TAXÍMETRO DIGITAL ---")
    print("1. Iniciar carrera")
    print("2. Cambiar estado (parado/movimiento)")
    print("3. Finalizar carrera y cobrar")
    print("4. Salir")

def main():
    tarifa = cargar_tarifa()
    carrera_activa = None

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            if carrera_activa is not None:
                print("Ya hay una carrera en curso.")
            else:
                carrera_activa = Carrera()
                print("Carrera iniciada. Estado: parado")

        elif opcion == "2":
            if carrera_activa is None:
                print("No hay ninguna carrera activa.")
            else:
                nuevo_estado = "movimiento" if carrera_activa.estado_actual == "parado" else "parado"
                carrera_activa.cambiar_estado(nuevo_estado)
                print(f"Nuevo estado: {nuevo_estado}")

        elif opcion == "3":
            if carrera_activa is None:
                print("No hay ninguna carrera activa.")
            else:
                carrera_activa.finalizar_carrera()
                total = carrera_activa.calcular_total(tarifa)
                print(f"Carrera finalizada. Total a cobrar: {total:.2f} €")
                carrera_activa = None

        elif opcion == "4":
            print("Cerrando aplicación. Hasta luego.")
            break

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()