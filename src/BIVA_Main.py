# ----------------------------------------------------------------------------------------
#                                  WebScraping BIVA Comunicados
# 
# Programa que extraerá información contable de la Bolsa de BIVA Mexico
# Autor: SteveCarpio
# Versión: V2 2025
# ----------------------------------------------------------------------------------------

from   cfg.BMV_librerias import *
from   biva.BIVA_paso0     import sTv_paso0
from   biva.BIVA_paso1     import sTv_paso1
from   biva.BIVA_paso2     import sTv_paso2

tiempo_inicio = dt.now()
var_NombreSalida= 'BIVA'
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
    print(Fore.YELLOW + "\nPaso 1 completado! \n")

def paso2():
    print(Fore.GREEN + f"\nEjecutando PASO_2........ {dt.now()} 👌\n")
    sTv_paso2(var_NombreSalida, var_FechasSalida)
    print(Fore.GREEN + "\nPaso 2 completado! \n")

def todos():
    print(Fore.LIGHTBLUE_EX + "\nEjecutando TODOS los pasos.......................... 💪")
    paso1()
    paso2()
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
