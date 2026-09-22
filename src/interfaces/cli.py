from src.domain.carrera import Carrera
from src.domain.tarifa import Tarifa
from src.infrastructure.historial import guardar_carrera, obtener_historial_dia
from src.infrastructure.logger import configurar_logger

def cargar_tarifa():
    tarifa = Tarifa(0.02, 0.05)
    return tarifa

def mostrar_menu():
    print("\n--- TAXÍMETRO DIGITAL ---")
    print("1. Iniciar carrera")
    print("2. Cambiar estado (parado/movimiento)")
    print("3. Finalizar carrera y cobrar")
    print("4. Ver histórico del día")
    print("5. Salir")

def main():
    tarifa = cargar_tarifa()
    carrera_activa = None
    logger = configurar_logger()
    logger.info("Aplicación iniciada por el usuario.")

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            if carrera_activa is not None:
                print("Ya hay una carrera en curso.")
                logger.warning("Ya hay una carrera en curso.")
            else:
                carrera_activa = Carrera()
                print("Carrera iniciada. Estado: parado")
                logger.info("Carrera iniciada. Estado: parado")

        elif opcion == "2":
            if carrera_activa is None:
                print("No hay ninguna carrera activa.")
                logger.warning("No hay ninguna carrera activa.")
            else:
                nuevo_estado = "movimiento" if carrera_activa.estado_actual == "parado" else "parado"
                carrera_activa.cambiar_estado(nuevo_estado)
                print(f"Nuevo estado: {nuevo_estado}")
                logger.info(f"Cambio de estado a: {nuevo_estado}")


        elif opcion == "3":
            if carrera_activa is None:
                print("No hay ninguna carrera activa.")
                logger.warning("No hay ninguna carrera activa.")
            else:
                carrera_activa.finalizar_carrera()
                total = carrera_activa.calcular_total(tarifa)
                print(f"Carrera finalizada. Total a cobrar: {total:.2f} €")
                logger.info(f"Carrera finalizada. Total a cobrar: {total:.2f} €")
                guardar_carrera(carrera_activa, tarifa)
                carrera_activa = None

        elif opcion == "4":
            historial = obtener_historial_dia()
            if not historial:
                print("No hay carreras registradas hoy.")
            else:
                print(f"\n--- HISTÓRICO DE HOY ({len(historial)} carreras) ---")
                for carrera in historial:
                    print(f"{carrera['hora_inicio']} → {carrera['hora_fin']}: {carrera['total']} €")

        elif opcion == "5":
            print("Cerrando aplicación. Hasta luego.")
            logger.info("Aplicación cerrada por el usuario.")
            break

        else:
            print("Opción no válida, intenta de nuevo.")
            logger.warning("Opción no válida seleccionada.")

if __name__ == "__main__":
    main()