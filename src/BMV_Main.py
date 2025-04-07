# ----------------------------------------------------------------------------------------
#                                  WebScraping BMV Comunicados
#
# Programa que extraerá información contable de la Web BMV 
# Autor: SteveCarpio
# Versión: V3 2025
# ----------------------------------------------------------------------------------------

from   cfg.BMV_librerias import *
import cfg.BMV_variables as sTv
from   bmv.BMV_paso0     import sTv_paso0
from   bmv.BMV_paso1     import sTv_paso1
from   bmv.BMV_paso2     import sTv_paso2
from   bmv.BMV_paso3     import sTv_paso3
from   bmv.BMV_paso4     import sTv_paso4
from   bmv.BMV_paso5     import sTv_paso5
from   bmv.BMV_paso6     import sTv_paso6
from   bmv.BMV_paso7     import sTv_paso7
from   bmv.BMV_paso8     import sTv_paso8

var_NombreSalida= 'BMV'
var_SendEmail= 'S'

if len(sys.argv) > 1 :
    var_param1 = sys.argv[1]
 
tiempo_inicio = dt.now()          #   2025-03-04 00:00:00.000000
tiempo_inicio = dt(2025, 4, 5)    #   dt(2025, 3, 31)

# Restar 1 día a la fecha actual
fecha_reducida = tiempo_inicio - timedelta(days=1)
# Crear variables con los formatos que necesitamos
var_Fechas1 = fecha_reducida.strftime('%Y-%m-%d')  # Formato "2025-03-04"
var_Fechas2 = fecha_reducida.strftime('%d-%m-%Y')  # Formato "04-03-2025"
var_Fechas3 = fecha_reducida.strftime('%Y%m%d')    # Formato "20250304"
# ----
var_FechasSalida= ""  # tiempo_inicio.strftime("%Y%m%d_%H%M%S")

os.system("cls")

# Inicializar colorama
init(autoreset=True)

# Inicializar carpetas y borrado de files
sTv_paso0(var_NombreSalida, var_FechasSalida, var_Fechas3)

# ------------------------------- MENU -----------------------------------

# Funciones para los pasos
def paso1():
    print(Fore.YELLOW + f"\nEjecutando PASO_1........ {dt.now()} \n")
    sTv_paso1(var_NombreSalida, var_FechasSalida)
    print(Fore.YELLOW + "Paso 1 completado! \n")

def paso2():
    print(Fore.GREEN + f"\nEjecutando PASO_2........ {dt.now()} \n")
    sTv_paso2(var_NombreSalida, var_FechasSalida)
    print(Fore.GREEN + "Paso 2 completado! \n")

def paso3():
    print(Fore.GREEN + f"\nEjecutando PASO_3........ {dt.now()} \n")
    sTv_paso3(var_NombreSalida, var_FechasSalida ) 
    print(Fore.GREEN + "Paso 3 completado! \n")

def paso4():
    print(Fore.GREEN + f"\nEjecutando PASO_4........ {dt.now()} \n")
    sTv_paso4(var_NombreSalida, var_FechasSalida ) 
    print(Fore.GREEN + "Paso 4 completado! \n")

def paso5():
    print(Fore.YELLOW + f"\nEjecutando PASO_5........ {dt.now()} \n")
    sTv_paso5(var_NombreSalida, var_FechasSalida)
    print(Fore.YELLOW + "Paso 5 completado! \n")

def paso6():
    print(Fore.GREEN + f"\nEjecutando PASO_6........ {dt.now()} \n")
    sTv_paso6(var_NombreSalida, var_FechasSalida ) 
    print(Fore.GREEN + "\nPaso 6 completado! \n")

def paso7():
    print(Fore.GREEN + f"\nEjecutando PASO_7........ {dt.now()} \n")
    sTv_paso7(var_NombreSalida, var_FechasSalida, tiempo_inicio)
    print(Fore.GREEN + "\nPaso 7 completado! \n")

def paso8():
    print(Fore.YELLOW + f"\nEjecutando PASO_8........ {dt.now()} \n")
    sTv_paso8(var_NombreSalida, var_FechasSalida, var_Fechas3, var_SendEmail)
    print(Fore.YELLOW + "\nPaso 8 completado! \n")

def pasoHelp():
    os.system("cls")
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.MAGENTA + "                         Proceso WebScraping Bolsa BMV")
    print(Fore.MAGENTA + "=" * 94)
    print("")
    print(Fore.WHITE + "Servidor:")
    print(Fore.WHITE + "    IP: 10.10.30.55 (Python)")
    print(Fore.WHITE + "    Usuario: Fiduciario")
    print(Fore.WHITE + "    Contraseña: Gestionada por Cerberus")
    print("")
    print(Fore.WHITE + "Ruta raíz:")
    print(Fore.WHITE + "    C:\\MisCompilados\\PROY_BOLSA_MX\\BMV\\")
    print("")
    print(Fore.WHITE + "Ejecución:")
    print(Fore.WHITE + "    BMV_Main_v3.exe RUN-NO-EMAIL")
    print("")
    print(Fore.WHITE + "Parámetros:")
    print(Fore.WHITE + "    [vació]: Muestra el menú actual")
    print(Fore.WHITE + "    RUN: Ejecuta el proceso enviando el correo de la Bolsa correspondiente")
    print(Fore.WHITE + "    RUN-NO-EMAIL: Ejecuta el proceso sin enviar el correo")
    print("")
    print(Fore.WHITE + "Planificación:")
    print(Fore.WHITE + "    Lun, Mar, Mié, Jue y Vie: 08:50h")
    print(Fore.WHITE + "    Sáb, Dom: 13:00h")
    print("")
    print(Fore.WHITE + "Pasos de ejecución:")
    print("")

    print(Fore.YELLOW + "    1) Selenium-WebScraping 'bmv.mx': Métodos empleados.. XPath, Html.PageSource.")
    print(Fore.WHITE + "       Navega en modo oculto por los apartados de Capital, Deudas y descarga en contenido de la Url")
    print(Fore.WHITE + "       Tener en cuenta el explorador y el driver de google, tener acceso fluido de internet para no tener")
    print(Fore.WHITE + "       problemas de red, no es recomendable usar el explorador Google mientras este en funcionamiento.")
    print("")
    print(Fore.GREEN + "    2) Pandas: Extraer URL de Capital y Deudas")
    print(Fore.WHITE + "       Se creará archivos excel con la información de apoyo para el siguiente paso.")
    print("")
    print(Fore.GREEN + "    3) Pandas: Tratamiento de URL de Capital y Deudas")
    print(Fore.WHITE + "       Creará 1 archivo excel unificando las URL de capital y deudas.")
    print("")
    print(Fore.GREEN + "    4) Pandas: Filtro de Emisores Ad-Doc")
    print(Fore.WHITE + "       Creará un excel con la información final de URL, IdEmisores/ClavePizarra.")
    print("")
    print(Fore.YELLOW + "    5) Requests.Get y Pandas: Descargar HMTL de Emisores")
    print(Fore.WHITE + "       Se descargará de las URL la web HMTL de los emisores filtrados")
    print("")
    print(Fore.GREEN + "    6) Pandas: Extraer información de los HMTL")
    print(Fore.WHITE + "       Se busca la información necesario de los hmtl en un dataframe para ser analizado.")
    print("")
    print(Fore.GREEN + "    7) Pandas: Crear informe Final")
    print(Fore.WHITE + "       Se creará un dataframe con toda la información recopilada.")
    print("")
    print(Fore.BLUE  + "    8) Pandas y Smtplib: Envió del email")
    print(Fore.WHITE + "       Si existen datos se enviará un email en formato html desde un DataFrame.")

    print("")
    print(Fore.WHITE + "Dependencias importantes:")
    print("")
    print(Fore.WHITE + "    - Google Chrome:")
    print(Fore.WHITE + "        Es fundamental tener instalada una versión estable (no Beta).")
    print("")
    print(Fore.WHITE + "    - ChromeDriver:")
    print(Fore.WHITE + "        Debe coincidir con la versión de Google Chrome instalada.")
    print(Fore.WHITE + "        Ruta del binario: C:\\MisCompilados\\cfg\\chromedriver-win32\\chromedriver.exe")
    print(Fore.WHITE + "        Para otras versiones: C:\\MisCompilados\\cfg\\chromedriver-win32\\1??\\")
    print("")
    print(Fore.WHITE + "    - Acceso a las URL:")
    print(Fore.WHITE + "        https://www.biva.mx/")
    print(Fore.WHITE + "        https://www.bmv.com.mx/")
    print("")
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.WHITE + "Para más ayuda, contactar con: SteveCarpio 'carpios@tda-sgft.com' (stv.madrid@gmail.com) ")
    print(Fore.WHITE + "Versión 3 - 2025")
    print(Fore.MAGENTA + "=" * 94)

def todos():
    print(Fore.WHITE + "\nEjecutando TODOS los pasos.......................... ")
    paso1()
    paso2()
    paso3()
    paso4()
    paso5()
    paso6()
    paso7()
    paso8()
    print(Fore.WHITE + "¡Todos los pasos completados exitosamente! \n")
    print(Fore.MAGENTA + f"---------------------------------------------------------------------------------------")
    print(Fore.WHITE + f" Tiempo Transcurrido INI: {tiempo_inicio} - FIN: {dt.now()}")
    print(Fore.MAGENTA + f"---------------------------------------------------------------------------------------")


# Función para limpiar la pantalla (en sistemas basados en UNIX)
def limpiar_pantalla():
    os.system("cls")  

# Menú interactivo
def mostrar_menu(par_FechasSalida):
    limpiar_pantalla()
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "     BOLSA BMV DATE: " + par_FechasSalida)
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "        🖥️   MENÚ PRINCIPAL 🖥️")
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE        + "0) ⚪ Ejecutar TODOS los pasos   ")
    print("")
    print(Fore.YELLOW       + "1) 🟡 Ejecutar el PASO_1         ")
    print(Fore.GREEN        + "2) 🟢 Ejecutar el PASO_2         ")
    print(Fore.GREEN        + "3) 🟢 Ejecutar el PASO_3         ")
    print(Fore.GREEN        + "4) 🟢 Ejecutar el PASO_4         ")
    print(Fore.YELLOW       + "5) 🟡 Ejecutar el PASO_5         ")
    print(Fore.GREEN        + "6) 🟢 Ejecutar el PASO_6         ")
    print(Fore.GREEN        + "7) 🟢 Ejecutar el PASO_7         ")
    print(Fore.BLUE         + "8) 🔵 Ejecutar el PASO_8         ")
    print("")
    print(Fore.MAGENTA      + "?) 🟣 Ayuda                      ")
    print(Fore.RED          + "x) ❌ Salir del programa   " + Fore.WHITE + "    (.v3)")
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
        elif opcion == '?':
            pasoHelp()    
        elif opcion.upper() == 'X':
            print(Fore.RED + "\n¡Saliendo del programa! 👋\n")
            break
        else:
            print(Fore.RED + "\n ❌ Opción no válida, por favor elige una opción válida ❌\n")
        
        # Pausa para que el usuario vea los resultados
        input(Fore.WHITE + "Presiona Enter para continuar...")

# Evaluamos como ejecutamos el proceso
if len(sys.argv) > 1 :

    if var_param1 == "RUN-NO-EMAIL":
        var_SendEmail = 'N'
    if "RUN" in var_param1:
        todos()
else:
    input(Fore.WHITE + "Presiona Enter para continuar...")
    
    ejecutar_menu(var_Fechas1)


# FIN: By Steve Carpio - 2025    
