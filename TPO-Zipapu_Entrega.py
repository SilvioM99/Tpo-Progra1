from datetime import datetime, timedelta
from typing import List

def menu() -> None:
    """
    Función para ver el menú donde interactuara el usuario
    """
    while True:
        print()
        print(
            "1- Cargar reserva habitación",
            "\n2- Mostrar habitaciones reservadas",
            "\n3- Total de ingreso",
            "\n4- Guardar datos en un CSV",
            "\n0- Salir",
        )

        opcion = input("Ingrese una opción del menu: ")
        if opcion == "0":
            print("Saliendo...")
            break
        elif opcion == "1":
            cargar_reserva()
        elif opcion == "2":
            if reservas:
                mostrar_reservas(habitaciones)
            else:
                print("No hay ninguna reserva hecha")
        elif opcion == "3":
            if ganancias:
                total = ganancia_total(ganancias)
                print(f"la ganancia es de {total}")
            else:
                print("No hay ninguna ganancia")
        elif opcion == "4":
            if reservas:
                exportar_archivo()
            else:
                print("No hay datos para exportar")
        else:
            print("Ingrese una opcion del menu valida")

def contador_dias(inicio: tuple, fin: tuple, formato="%d/%m/%Y") -> int:
    """
    Función que permite saber cuantos días hay entre 2 fechas
    Precondiciones: Recibe como parámetros 2 fechas con formato d/m/a tipo string
    Postcondiciones: Devuelve la diferencia entre las 2 fechas como un numero entero
    """
    inicio_str = "/".join(map(str, inicio))
    fin_str = "/".join(map(str, fin))

    inicio_fecha = datetime.strptime(inicio_str, formato)
    fin_fecha = datetime.strptime(fin_str, formato)
    diferencia = fin_fecha - inicio_fecha

    return diferencia.days


def calcular_costo_alquiler(dias: int, ropa_blanca=False) -> int:
    """
    Función para calcular los costos de la reserva
    Precondiciones: recibe 2 números enteros el cual 1 son los días y otro si tendrá acceso a la ropa_blanca
    Postcondiciones: devuelve 1 numero entero que es el costo de la estadía
    """ ## primero va el contrato y luego pre y pos
    costo_diario = 3000
    costo_ropa_blanca = 500

    costo_total = dias * costo_diario

    if ropa_blanca:
        costo_total += costo_ropa_blanca

    return costo_total


def cargar_reserva() -> None:
    """
    Función para cargar reserva, con sus diferentes bucles para no reciba errores
    Precondiciones: Tiene que haber un lugar donde guardar las reservas.
    Postcondiciones: devuelve una confirmación si se acepto la reserva o se rechazo.
    """
    while True:
        try:
            dni = int(input("Ingrese su numero dni: "))
            if dni in reservas.keys():
                print("Ya tiene una reserva con su nombre no puede agregar otra")
            elif dni > 5_000_000 and dni <= 99_999_999: ## tiene que incluir al 99_999-999
                break
            else:
                print("El dni es incorrecto ingrese uno valido")
        except:
            print("Error con el dni , ingrese nuevamente")
    while True:
        apellido = input("Ingrese su apellido: ")
        if apellido.isalpha():
            break
        else:
            print("Ingrese uno valido")
    while True:
        cant = (1, 2)
        try:
            cant_personas = int(input("Ingrese cantidad de personas, Máximo 2: "))
            if cant_personas in cant:
                break
            else:
                print("Ingrese entre 1 o 2")
        except:
            print("Error, Ingrese un numero valido")
    while True:
        print()
        print("las habitaciones son", " ".join(habitaciones.keys()))
        num_habitacion = input("Ingrese un numero de habitación disponible: ").upper()

        if num_habitacion in habitaciones and habitaciones[num_habitacion] == '':
            break
        else:
            print("La habitación se encuentra reservada.")
    while True:
        try:
            desde = input("Ingrese una fecha de inicio(DD/MM/YYYY): ")
            desde = tuple(map(int, desde.split("/")))
            if 3 == len(desde) and desde[2] >= 2023:
                break
            else:
                print("Ingrese una fecha valida con el formato (DD/MM/YYYY)")
        except:
            print("Error ingrese una fecha valida")
    while True:
        try:
            hasta = input("Ingrese una fecha de fin (DD/MM/YYYY): ")
            if 3 == len((hasta.split("/"))):
                hasta = tuple(map(int, hasta.split("/")))
                if hasta and desde[2] < hasta[2]:
                    break
                elif hasta and desde[2] == hasta[2] and desde[1] <= hasta[1]:
                    break

                else:
                    print(
                        "Ingrese una fecha valida superior a la de inicio con formato (DD/MM/YYYY)"
                    )
            else:
                print("Ingrese una fecha valida con el formato (DD/MM/YYYY)")
        except:
            print("Error ingrese una fecha valida")

    while True:
        ropa = ("0", "1")
        ropa_blanca = input("Desea adicionar ropa blanca?, para si (1) o no (0): ")
        if ropa_blanca in ropa:
            break
        else:
            print("Ingrese entre 1 y 0")

    dias_alquiler = contador_dias(desde, hasta)
    costo_total = calcular_costo_alquiler(dias_alquiler, ropa_blanca)
    print(f"Su precio de alquiler de {dias_alquiler} dias es de {costo_total}")

    while True:
        usuario = input(
            "Le gustaría hacer esa reserva? (S) para si y (N) para no: "
        ).upper()
        if usuario == "S" or usuario == "N":
            break
        else:
            print("Ingrese S o N")
    if usuario == "S":
        habitaciones[num_habitacion] = dni
        reservas[dni] = {
            "Apellido": apellido.capitalize(),
            "Cantidad personas": cant_personas,
            "Inicio": desde,
            "Fin": hasta,
            "Ropa_blanca": ropa_blanca,
        }

        ganancias.append(costo_total)
        print("Reserva realizada con éxito.")
    else:
        print("Reserva rechazada.")


def ganancia_total(beneficio: List) -> int:
    """
    Función para calcular el total de las ganancias
    Precondiciones: Tiene que haber mínimo una ganancia para ejecutar la función
    Postcondiciones: Devuelve un entero con la suma de toda las ganancias
    """
    return sum(beneficio)


def mostrar_reservas(hab: dict) -> None:
    """
    Función que permite ver las reservas y la persona que reservo la Habitación
    Precondiciones: Tiene que haber mínimo una habitación reservada para mostrar
    Postcondiciones: Muestra por pantalla las habitaciones reservadas
    """
    print("Lista de habitaciones reservadas")
    for hab, dni in hab.items():
        if dni:
            print(f"Habitación {hab}: DNI {dni}")


def exportar_archivo() -> None:
    """
    Función para exportar todo los datos a un archivo CSV
    Precondiciones: mínimo un dato en reservas
    Postcondiciones: exporta un archivo CSV con nombre Informe_reservas con los datos guardados en reservas
    """
    encabezado = (
        "DNI",
        "Apellido",
        "Cantidad personas",
        "Inicio",
        "Fin",
        "Ropa blanca",
    )
    separador = ";"
    try:
        with open("Informe_reservas.csv", "wt", encoding="utf-8") as f:
            f.write(separador.join(encabezado) + "\n")
            for dni, datos in reservas.items():
                fila = [
                    str(dni),
                    datos["Apellido"],
                    str(datos["Cantidad personas"]),
                    str(datos["Inicio"]),
                    str(datos["Fin"]),
                    datos["Ropa_blanca"],
                ]
                f.write(separador.join(fila) + "\n")
    except:
        print(f"Error al exportar archivo")
    else:
        print("Se creo correctamente")

## esto más que None deberían ser las estructuras vacías
habitaciones = {"A": '', "B": '', "C": '', "D": '', "E": '', "F": ''}
reservas = {}
ganancias = []

if __name__ == "__main__":
    menu()
