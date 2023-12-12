def menu():
    '''Funcion para ver el menú donde interactuara el usuario'''
    while True:
        print()
        print('1- Cargar reserva habitacion',
              '\n2- Mostrar habitaciones reservadas',
              '\n3- Total de ingreso',
              '\n4- Guardar datos en un CSV',
              '\n0- Salir')
        
        opcion = input('Ingrese una opcion del menu: ')
        if opcion == '0':
            print('Saliendo...')
            break
        elif opcion == '1':
            cargar_reserva()
        elif opcion == '2':
            if reservas:
                mostrar_reservas()
            else:
                print('No hay ninguna reserva hecha')
        elif opcion == '3':
            if ganancias:
                ganancia_total()
            else:
                print('No hay ninguna ganancia')
        elif opcion == '4':
            if reservas:
                exportar_archivo()
            else:
                print('No hay datos para exportar')
        else:
            print('Ingrese una opcion del menu valida')
def contar_dias(d, m, a):
    treintadias = [4, 6, 9, 11]
    if m in treintadias:
        dialim = 30
    elif m == 2:
        if a % 4 == 0 and (a % 100 != 0 or a % 400 == 0):
            dialim = 29
        else:
            dialim = 28
    else:
        dialim = 31
    if d == dialim:
        d = 1
        if m == 12:
            m = 1
            a += 1
        else:
            m += 1
    else:
        d += 1
    return d, m, a

def contador_dias(inicio,fin):
    '''Funcion que permite saber cuantos dias hay entre 2 fechas'''
    dia, mes, anio = inicio
    contador = 0
    while True:
        dia, mes, anio = contar_dias(dia, mes, anio)
        ahora = dia, mes, anio
        contador += 1
        if fin == ahora:
            break
    return contador
def calcular_costo_alquiler(dias,ropa_blanca=False):
    '''
    Precondiciones: recibe 2 numeros enteros el cual 1 son los dias y otro si tendra acceso a la ropa_blanca
    Postcondiciones: devuelve 1 numero entero que es el costo de la estadia
    Funcion para calcular los costos de la reserva'''
    costo_diario=3000
    costo_ropa_blanca=500
    
    costo_total = dias * costo_diario

    if ropa_blanca:
        costo_total += costo_ropa_blanca

    return costo_total
def cargar_reserva():
    '''Funcion para cargar reserva, con sus diferentes blucles para no reciba errores'''
    while True:
        try:
            dni = int(input('Ingrese su numero dni: '))
            if dni in reservas.keys():
                print('Ya tiene una reserva con su nombre no puede agregar otra')
            elif dni > 5_000_000 and dni < 99_999_999:
                break
            else:
                print('El dni es incorrecto ingrese uno valido')
        except:
            print('Error con el dni , ingreselo nuevamente')
    while True:
        apellido = input('Ingrese su apellido: ')
        if apellido.isalpha():
            break
        else:
            print('Ingrese uno valido')
    while True:
        cant = (1,2)
        try:
            cant_personas = int(input('Ingrese cantidad de personas, Maximo 2: '))
            if cant_personas in cant:
                break
            else:
                print('Ingrese entre 1 o 2')
        except:
            print('Error, Ingrese un numero valido')
    while True:
        print()
        print('las habitaciones son',' '.join(habitaciones.keys()))
        num_habitacion = input('Ingrese un numero de habitacion disponible: ').upper()
        
        if num_habitacion in habitaciones and habitaciones[num_habitacion] is None:
            break
        else:
            print('La habitación se encuentra reservada.')
    while True:
        try:
            desde = input('Ingrese una fecha de inicio(DD/MM/YYYY): ')
            desde = tuple(map(int, desde.split('/')))
            if 3 == len(desde) and desde[2] >= 2023:
                break
            else:
                print('Ingrese una fecha valida con el formato (DD/MM/YYYY)')
        except:
            print('Error ingrese una fecha valida')
    while True:
        try:
            hasta = input('Ingrese una fecha de fin (DD/MM/YYYY): ')
            if 3 == len((hasta.split('/'))):
                hasta = tuple(map(int, hasta.split('/')))
                if hasta and desde[2] < hasta[2]:
                    break
                elif hasta and desde[2] == hasta[2] and desde[1] <= hasta[1]:
                    break
                    
                else:
                    print('Ingrese una fecha valida superior a la de inicio con formato (DD/MM/YYYY)')
            else:
                print('Ingrese una fecha valida con el formato (DD/MM/YYYY)')
        except:
            print('Error ingrese una fecha valida')

    while True:
        ropa = ('0','1')
        ropa_blanca = input('Desea adicionar ropa blanca?, para si (1) o no (0): ')
        if ropa_blanca in ropa:
            break
        else:
            print('Ingrese entre 1 y 0')
            
    dias_alquiler = contador_dias(desde,hasta)
    costo_total = calcular_costo_alquiler(dias_alquiler,ropa_blanca)
    print(f'Su precio de alquiler de {dias_alquiler} dias es de {costo_total}')
    
    while True:
        usuario = input('Le gustaria hacer esa reserva? (S) para si y (N) para no: ').upper()
        if usuario == 'S' or usuario == 'N':
            break
        else:
            print('Ingrese S o N')
    if usuario == 'S':
        habitaciones[num_habitacion] = dni
        reservas[dni] = {'Apellido': apellido.capitalize(), 'Cantidad personas': cant_personas, 'Inicio': desde,'Fin': hasta,  'Ropa_blanca': ropa_blanca}
        
        ganancias.append(costo_total)
        print('Reserva realizada con éxito.')
    else:
        print('Reserva rechazada.')
    
def ganancia_total():
    '''Funcion para calcular el total de las ganancias'''
    print(f'la ganancia es de {sum(ganancias)}')
    
def mostrar_reservas():
    '''Funcion que permite ver las reservas y la persona que reservo la Habitacion'''
    print('Lista de habitaciones reservadas')
    for habitacion, dni in habitaciones.items():
        if dni is not None:
            print(f'Habitación {habitacion}: DNI {dni}')
            
    
def exportar_archivo():
    '''Funcion para exportar todo los datos a un archivo CSV'''
    encabezado = ('DNI','Apellido','Cantidad personas','Inicio','Fin','Ropa blanca')
    separador = ';'
    try:
        with open('Informe_reservas.csv','wt',encoding = 'utf-8') as f:
            f.write(separador.join(encabezado) + '\n')
            for dni, datos in reservas.items():
                fila = [str(dni), datos['Apellido'], str(datos['Cantidad personas']), str(datos['Inicio']),str(datos['Fin']), datos['Ropa_blanca']]
                f.write(separador.join(fila) + "\n")
    except:
        print(f"Error al exportar archivo")
    else:
        print("Se creo correctamente")
        
habitaciones = {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None,
                'F': None}
reservas = {}
ganancias = []

if __name__ == '__main__':
    menu()