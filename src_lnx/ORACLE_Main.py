# ----------------------------------------------------------------------------------------
#                                  WebScraping ORACLE Comunicados
# 
# Programa que enviará toda la información procesada de las Bolsas de 
# BMV y BIVA a los servidores Oracle, luego actualizará desde oracle los informes de CiBanco
# Autor: SteveCarpio
# Versión: V1 2025
# ----------------------------------------------------------------------------------------

from   cfg.ORACLE_librerias import *
import cfg.ORACLE_variables as sTv
from   oracle.ORACLE_paso0  import sTv_paso0
from   oracle.ORACLE_paso1  import sTv_paso1
from   oracle.ORACLE_paso2  import sTv_paso2
from   oracle.ORACLE_paso3  import sTv_paso3

var_NombreSalida = 'ORACLE'
tiempo_inicio2 = dt.now()

# Parámetro1: RUN 
if len(sys.argv) > 1 :
    var_param1 = sys.argv[1]

# Parámetro2: Producción o Desarrollo
var_Entorno="DEV" 
if len(sys.argv) > 2 :
    var_param2 = sys.argv[2]
    if var_param2 == "PRO":
        var_Entorno = var_param2

print(len(sys.argv))

if var_Entorno != "PRO":
    print("El programa está preparado para ejecutarse sobre tablas de PRODUCCIÓN el resto de modos no están preparados")
    #sys.exit(0)

# Parámetro3: Fecha (opcional)
tiempo_inicio = tiempo_inicio2
#tiempo_inicio = dt(2025, 6, 7)    #   dt(2025, 3, 31)
if len(sys.argv) > 3 :
    var_param3 = sys.argv[3]
    if re.match(r"^\d{4}-\d{2}-\d{2}$", var_param3):
        anio, mes, dia = map(int, var_param3.split('-'))
        tiempo_inicio = dt(anio, mes, dia)
    else:
        print("El formato de fecha debe ser, ejemplo: 2025-07-28")
        input(Fore.WHITE + f"Se ejecutará con el día {tiempo_inicio.strftime('%Y-%m-%d')}")

# Restar 1 día a la fecha actual
fecha_reducida = tiempo_inicio - timedelta(days=1)
# Crear variables con los formatos que necesitamos
var_Fechas1 = fecha_reducida.strftime('%Y-%m-%d')  # Formato "2025-03-04"
var_Fechas2 = fecha_reducida.strftime('%d-%m-%Y')  # Formato "04-03-2025"
var_Fechas3 = fecha_reducida.strftime('%Y%m%d')    # Formato "20250304"

os.system("clear")

# Inicializar colorama
init(autoreset=True)

# Inicializar carpetas y borrado de files
sTv_paso0(var_Fechas3)

# Inicializo un DF vació
#df_Total = pd.DataFrame()
# ------------------------------- MENU -----------------------------------

# Funciones para los pasos
def paso1():
    print(Fore.YELLOW + f"\nEjecutando PASO1: Importar Datos de entrada....... {dt.now()} \n")
    sTv_paso1(var_Fechas3)
    print(Fore.YELLOW + "\nPaso 1 completado - Importación de Datos! \n")

def paso2():
 
    print(Fore.GREEN + f"\nEjecutando PASO2: Valida Datos de entrada (Local vs Oracle)....... {dt.now()} \n")
    sTv_paso2(var_Fechas3)
    print(Fore.GREEN + "\nPaso 2 completado - Validación de Datos! \n")

def paso3():
    print(Fore.BLUE + f"\nEjecutando PASO3: Carga de Datos al Servidor Oracle....... {dt.now()} \n")
    sTv_paso3(var_Fechas3)
    print(Fore.BLUE + "\nPaso 3 completado - Anexado de Datos a Oracle! \n")

def pasoHelp():
    os.system("clear")
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.MAGENTA + "                         Proceso WebScraping Oracle BIVA y BMV")
    print(Fore.MAGENTA + "=" * 94)
    print("")
    print(Fore.WHITE + "Servidor:")
    print(Fore.WHITE + "    IP: 10.10.30.7 (Linux-Python)")
    print(Fore.WHITE + "    Usuario: robot")
    print(Fore.WHITE + "    Contraseña: Gestionada por Cerberus")
    print("")
    print(Fore.WHITE + "Ruta raíz:")
    print(Fore.WHITE + "    /srv/apps/MisCompilados/PROY_BOLSA_MX/ORACLE/")
    print("")
    print(Fore.WHITE + "Ejecución:")
    print(Fore.WHITE + "    ORACLE_Main.py RUN PRO")
    print("")
    print(Fore.WHITE + "Parámetros:  [RUN]  [DEV/PRO]  AAAA-MM-DD(opcional):")
    print(Fore.WHITE + "    [vació]: Muestra el menú actual")
    print(Fore.WHITE + "    RUN: Ejecuta el proceso enviando el correo de la Bolsa correspondiente")
    print(Fore.WHITE + "    [DEV/PRO]: Ejecuta el proceso en modo desarrollo o producción")
    print(Fore.WHITE + "    AAAA-MM-DD: Ejecución puntual corresponde al día de ejecución")
    print("")
    print(Fore.WHITE + "Planificación:")
    print(Fore.WHITE + "    Lun, Mar, Mié, Jue y Vie: 08:50h")
    print(Fore.WHITE + "    Sáb, Dom: 13:00h")
    print("")
    print(Fore.WHITE + "Pasos de ejecución:")
    print("")
    print(Fore.WHITE + "    1) Importar Datos de Entrada:")
    print(Fore.WHITE + "       Importamos los datos de BMV y BIVA a un DataFrame")
    print("")
    print(Fore.WHITE + "    2) Valida Datos de entrada Local vs Oracle:")
    print(Fore.WHITE + "       Validamos la estructura del DataFrame, si existe y no en Producción Oracle")
    print("")
    print(Fore.WHITE + "    3) Carga de Datos al Servidor Oracle:")
    print(Fore.WHITE + "       Subimos los datos validados al servidor Oracle")
    print("")
    print(Fore.WHITE + "Dependencias importantes:")
    print("")
    print(Fore.WHITE + "    1) TNS de ORACLE:")
    print("")
    print(Fore.WHITE + "       COMUN= ")
    print(Fore.WHITE + "          (DESCRIPTION=")
    print(Fore.WHITE + "             (ADDRESS=")
    print(Fore.WHITE + "                (PROTOCOL=TCP)")
    print(Fore.WHITE + "                (HOST=oraprod9.tda)")
    print(Fore.WHITE + "                (PORT=1521)")
    print(Fore.WHITE + "             )")
    print(Fore.WHITE + "             (CONNECT_DATA=")
    print(Fore.WHITE + "                (SERVER=dedicated)")
    print(Fore.WHITE + "                (SERVICE_NAME=COMUN)")
    print(Fore.WHITE + "             )")
    print(Fore.WHITE + "          )")
    print("")
    print(Fore.WHITE + "    2) Acceso a la BBDD Oracle:")
    print(Fore.WHITE + "       Usuario: PYDATA")
    print(Fore.WHITE + "       Password: PYDATA")
    print("")
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.WHITE + "Para más ayuda, contactar con: SteveCarpio 'carpios@tda-sgft.com' (stv.madrid@gmail.com) ")
    print(Fore.WHITE + "Versión 1 - 2025")
    print(Fore.MAGENTA + "=" * 94)

def todos():
    print(Fore.WHITE + "\nEjecutando TODOS los pasos.......................... ")
    paso1()
    paso2()
    paso3()
    print(Fore.WHITE + "¡Todos los pasos completados exitosamente!  \n")
    print(Fore.MAGENTA + f"---------------------------------------------------------------------------------------")
    print(Fore.WHITE + f" Tiempo Transcurrido INI: {tiempo_inicio2} - FIN: {dt.now()}")
    print(Fore.MAGENTA + f"---------------------------------------------------------------------------------------")

# Función para limpiar la pantalla (en sistemas basados en UNIX)
def limpiar_pantalla():
    os.system("clear")  

# Menú interactivo
def mostrar_menu(par_FechasSalida):
    limpiar_pantalla()
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "   Oracle Bolsas (MX): " + par_FechasSalida)
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "        🖥️   MENÚ PRINCIPAL 🖥️")
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE   + "0) ⚪ Ejecutar TODOS los pasos   ")
    print("")
    print(Fore.YELLOW  + "1) 🟡 Importar Datos de Entrada                ")
    print(Fore.GREEN   + "2) 🟢 Validar Datos Locales vs Oracle          ")
    print(Fore.BLUE    + "3) 🔵 Carga de Datos al Servidor Oracle        ")
    print("")
    print(Fore.MAGENTA + "?) 🟣 Ayuda                      ")
    print(Fore.RED     + "x) ❌ Salir del programa   " + Fore.WHITE + "    (.v1)")
    print(Fore.MAGENTA + "=" * 37)

# Función principal para gestionar el menú
def ejecutar_menu(par_FechasSalida):
    while True:
        mostrar_menu(par_FechasSalida)
        option = input(Fore.WHITE + "Selecciona una opción: ")

        if option   == '0':
            todos()
        elif option == '1':
            paso1()
        elif option == '2':
            paso2()
        elif option == '3':
            paso3()
        
        elif option == '?':
            pasoHelp()
        elif option.upper() == 'X':
            print(Fore.RED + "\n¡Saliendo del programa! \n")
            break
        else:
            print(Fore.RED + "\n ❌ Opción no válida, por favor elige una opción válida ❌\n")
        
        # Pausa para que el usuario vea los resultados
        input(Fore.WHITE + "Presiona Enter para continuar...")

# Evaluamos como ejecutamos el proceso
if len(sys.argv) > 1 :
    if "RUN" in var_param1:
        todos()

    if "?" in var_param1:
        pasoHelp()

    if "help" in var_param1:
        pasoHelp()

else:
    input(Fore.WHITE + "Presiona Enter para continuar...")
    ejecutar_menu(var_Fechas1)

# FIN: By Steve Carpio - 2025    