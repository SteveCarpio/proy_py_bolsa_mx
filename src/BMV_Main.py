# ----------------------------------------------------------------------------------------
#                                  WebScraping BMV "DEUDAS"
#
# Programa que extraerá información contable de la Web BMV 
# Autor: SteveCarpio
# Versión: V2 2025
# ----------------------------------------------------------------------------------------

from   cfg.BMV_librerias import *
from   bmv.BMV_paso0     import sTv_paso0
from   bmv.BMV_paso1     import sTv_paso1
from   bmv.BMV_paso2     import sTv_paso2
from   bmv.BMV_paso3     import sTv_paso3
from   bmv.BMV_paso4     import sTv_paso4
from   bmv.BMV_paso5     import sTv_paso5
from   bmv.BMV_paso6     import sTv_paso6
from   bmv.BMV_paso7     import sTv_paso7
from   bmv.BMV_paso8     import sTv_paso8


tiempo_inicio = dt.now()
var_NombreSalida= 'BMV'
var_FechasSalida= ""  # tiempo_inicio.strftime("%Y%m%d_%H%M%S")

os.system("cls")

# Inicializar colorama
init(autoreset=True)

# Inicializar carpetas y borrado de files
sTv_paso0(var_NombreSalida, var_FechasSalida)


# ------------------------------- MENU -----------------------------------

# Funciones para los pasos
def paso1():
    print(Fore.YELLOW + f"\nEjecutando PASO_1........ {dt.now()} 👌\n")
    sTv_paso1(var_NombreSalida, var_FechasSalida)
    print(Fore.YELLOW + "Paso 1 completado! \n")

def paso2():
    print(Fore.GREEN + f"\nEjecutando PASO_2........ {dt.now()} 👌\n")
    sTv_paso2(var_NombreSalida, var_FechasSalida)
    print(Fore.GREEN + "Paso 2 completado! \n")

def paso3():
    print(Fore.GREEN + f"\nEjecutando PASO_3........ {dt.now()} 👌\n")
    sTv_paso3(var_NombreSalida, var_FechasSalida ) 
    print(Fore.GREEN + "Paso 3 completado! \n")

def paso4():
    print(Fore.GREEN + f"\nEjecutando PASO_4........ {dt.now()} 👌\n")
    sTv_paso4(var_NombreSalida, var_FechasSalida ) 
    print(Fore.GREEN + "Paso 4 completado! \n")

def paso5():
    print(Fore.YELLOW + f"\nEjecutando PASO_5........ {dt.now()} 👌\n")
    sTv_paso5(var_NombreSalida, var_FechasSalida)
    print(Fore.YELLOW + "Paso 5 completado! \n")

def paso6():
    print(Fore.GREEN + f"\nEjecutando PASO_6........ {dt.now()} 👌\n")
    sTv_paso6(var_NombreSalida, var_FechasSalida ) 
    print(Fore.GREEN + "\nPaso 6 completado! \n")

def paso7():
    print(Fore.GREEN + f"\nEjecutando PASO_7........ {dt.now()} 👌\n")
    sTv_paso7(var_NombreSalida, var_FechasSalida)
    print(Fore.GREEN + "\nPaso 7 completado! \n")

def paso8():
    print(Fore.CYAN + f"\nEjecutando PASO_8........ {dt.now()} 👌\n")
    sTv_paso8(var_NombreSalida, var_FechasSalida)
    print(Fore.CYAN + "\nPaso 8 completado! \n")

def todos():
    print(Fore.LIGHTBLUE_EX + "\nEjecutando TODOS los pasos.......................... 💪")
    paso1()
    paso2()
    paso3()
    paso4()
    paso5()
    paso6()
    paso7()
    paso8()
    print(Fore.LIGHTBLUE_EX + "¡Todos los pasos completados exitosamentex! 🎉 \n")
    print(Fore.CYAN + f"---------------------------------------------------------------------------------------")
    print(Fore.CYAN + f" Tiempo Transcurrido INI: {tiempo_inicio} - FIN: {dt.now()}")
    print(Fore.CYAN + f"---------------------------------------------------------------------------------------")


# Función para limpiar la pantalla (en sistemas basados en UNIX)
def limpiar_pantalla():
    os.system("cls")  

# Menú interactivo
def mostrar_menu(par_FechasSalida):
    limpiar_pantalla()
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "  Fecha Ejecución:  " + dt.now().strftime("%Y%m%d_%H%M%S"))  # par_FechasSalida
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "        🖥️   MENÚ PRINCIPAL 🖥️")
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.LIGHTBLUE_EX + "0) 🔵 Ejecutar TODOS los pasos   ")
    print(Fore.YELLOW       + "1) 🟡 Ejecutar el PASO_1         ")
    print(Fore.GREEN        + "2) 🟢 Ejecutar el PASO_2         ")
    print(Fore.GREEN        + "3) 🟢 Ejecutar el PASO_3         ")
    print(Fore.GREEN        + "4) 🟢 Ejecutar el PASO_4         ")
    print(Fore.YELLOW       + "5) 🟡 Ejecutar el PASO_5         ")
    print(Fore.GREEN        + "6) 🟢 Ejecutar el PASO_6         ")
    print(Fore.GREEN        + "7) 🟢 Ejecutar el PASO_7         ")
    print(Fore.CYAN         + "8) 🔵 Ejecutar el PASO_8         ")
    print(Fore.RED          + "x) ❌ Salir del programa   " + Fore.WHITE + "    (.v2)")
    print(Fore.MAGENTA + "=" * 37)


# Función principal para gestionar el menú
def ejecutar_menu(par_FechasSalida):
    while True:
        mostrar_menu(par_FechasSalida)
        opcion = input(Fore.WHITE + "Selecciona una opción: ")

        if opcion   == '0':
            todos()
        elif opcion == '1':
            paso1()
        elif opcion == '2':
            paso2()
        elif opcion == '3':
            paso3()
        elif opcion == '4':
            paso4()
        elif opcion == '5':
            paso5()
        elif opcion == '6':
            paso6()
        elif opcion == '7':
            paso7()
        elif opcion == '8':
            paso8()    
        elif opcion.upper() == 'X':
            print(Fore.RED + "\n¡Saliendo del programa! 👋\n")
            break
        else:
            print(Fore.RED + "\n ❌ Opción no válida, por favor elige una opción válida ❌\n")
        
        # Pausa para que el usuario vea los resultados
        input(Fore.WHITE + "Presiona Enter para continuar...")


if len(sys.argv) > 1 and sys.argv[1] == "RUN":
    todos()
else:
    input(Fore.WHITE + "Presiona Enter para continuar...")
    # Ejecutar el menú
    ejecutar_menu(var_FechasSalida)

# FIN: By Steve Carpio - 2025    
