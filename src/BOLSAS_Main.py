# ----------------------------------------------------------------------------------------
#                                  WebScraping BOLSAS Comunicados
# 
# Programa que extraerá información contable de la Bolsa de BIVA Mexico
# Autor: SteveCarpio
# Versión: V3 2025
# ----------------------------------------------------------------------------------------

from   cfg.BOLSAS_librerias import *
from   bolsas.BOLSAS_paso0  import sTv_paso0
from   bolsas.BOLSAS_paso1  import sTv_paso1
from   bolsas.BOLSAS_paso2  import sTv_paso2
from   bolsas.BOLSAS_paso3  import sTv_paso3
from   bolsas.BOLSAS_paso4  import sTv_paso4

var_NombreSalida = 'BOLSAS'
var_SendEmail= 'S'

if len(sys.argv) > 1 :
    var_param1 = sys.argv[1]
    
#tiempo_inicio = dt.now()
tiempo_inicio = dt(2025, 3, 22)

# Restar 1 día a la fecha actual
fecha_reducida = tiempo_inicio - timedelta(days=1)
# Crear variables con los formatos que necesitamos
var_Fechas1 = fecha_reducida.strftime('%Y-%m-%d')  # Formato "2025-03-04"
var_Fechas2 = fecha_reducida.strftime('%d-%m-%Y')  # Formato "04-03-2025"
var_Fechas3 = fecha_reducida.strftime('%Y%m%d')    # Formato "20250304"

os.system("cls")

# Inicializar colorama
init(autoreset=True)

# Inicializar carpetas y borrado de files
sTv_paso0(var_Fechas3)

# ------------------------------- MENU -----------------------------------

# Funciones para los pasos
def paso1():
    print(Fore.YELLOW + f"\nEjecutando PASO_1 - BOLSA BIVA........ {dt.now()} 👌\n")
    print("AVISO: El PASO1 está planificado como un job independiente, ver DOC. ")
    #sTv_paso1()
    print(Fore.YELLOW + "\nPaso 1 completado - BOLSA BIVA! \n")

def paso2():
    print(Fore.YELLOW + f"\nEjecutando PASO_2 - BOLSA BMV........ {dt.now()} 👌\n")
    print("AVISO: El PASO2 está planificado como un job independiente, ver DOC. ")
    #sTv_paso2()
    print(Fore.YELLOW + "\nPaso 2 completado - BOLSA BMV! \n")

def paso3():
    print(Fore.GREEN + f"\nEjecutando PASO_3 - Copiar Resultados BMV/BIVA........ {dt.now()} 👌\n")
    sTv_paso3(var_Fechas3)
    print(Fore.GREEN + "\nPaso 3 completado - Copia de datos BOLSAS BIVA y BMV! \n")

def paso4():
    print(Fore.YELLOW + f"\nEjecutando PASO_4 - Mandar Email........ {dt.now()} 👌\n")
    sTv_paso4(var_NombreSalida, var_Fechas2, var_Fechas3, var_SendEmail)
    print(Fore.YELLOW + "\nPaso 4 completado - Envió del Email! \n")

def pasoHelp():
    os.system("cls")
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.MAGENTA + "                         Proceso WebScraping Bolsas BIVA y BMV")
    print(Fore.MAGENTA + "=" * 94)
    print("")
    print(Fore.WHITE + "Servidor:")
    print(Fore.WHITE + "    IP: 10.10.30.55 (Python)")
    print(Fore.WHITE + "    Usuario: Fiduciario")
    print(Fore.WHITE + "    Contraseña: Gestionada por Cerberus")
    print("")
    print(Fore.WHITE + "Ruta raíz:")
    print(Fore.WHITE + "    C:\\MisCompilados\\PROY_BOLSA_MX\\")
    print("")
    print(Fore.WHITE + "Ejecución:")
    print(Fore.WHITE + "    BIVA_Main_v3.exe RUN-NO-EMAIL")
    print(Fore.WHITE + "    BMV_Main_v3.exe RUN-NO-EMAIL")
    print(Fore.WHITE + "    BOLSAS_Main_v3.exe RUN")
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
    print(Fore.WHITE + "    1) Ejecutar BOLSA BIVA:")
    print(Fore.WHITE + "        Este paso se ejecuta de forma independiente en un trabajo programado")
    print(Fore.WHITE + "        con el nombre del trabajo 'BIVA_Main_v3.exe'.")
    print("")
    print(Fore.WHITE + "    2) Ejecutar BOLSA BMV:")
    print(Fore.WHITE + "        Este paso también se ejecuta de manera independiente en un trabajo programado")
    print(Fore.WHITE + "        con el nombre del trabajo 'BMV_Main_v3.exe'.")
    print("")
    print(Fore.WHITE + "    3) Copiar Resultados BMV/BIVA:")
    print(Fore.WHITE + "        Copia los resultados de los informes de BIVA y BMV en la carpeta de trabajo")
    print(Fore.WHITE + "        C:\\MisCompilados\\PROY_BOLSA_MX\\INFORMES.")
    print("")
    print(Fore.WHITE + "    4) Enviar Email:")
    print(Fore.WHITE + "        Envía el contenido de los informes por correo electrónico. Si no hay datos disponibles,")
    print(Fore.WHITE + "        se enviará un correo indicando que no hay información para reportar.")
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
    print(Fore.WHITE + "\nEjecutando TODOS los pasos.......................... 💪")
    paso1()
    paso2()
    paso3()
    paso4()
    print(Fore.WHITE + "¡Todos los pasos completados exitosamente! 🎉 \n")
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
    print(Fore.WHITE + "   Bolsa BIVA/BMV (MX): " + par_FechasSalida)
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE + "        🖥️   MENÚ PRINCIPAL 🖥️")
    print(Fore.MAGENTA + "=" * 37)
    print(Fore.WHITE   + "0) ⚪ Ejecutar TODOS los pasos   ")
    print("")
    print(Fore.YELLOW  + "1) 🟡 Ejecutar BOLSA BIVA     ")
    print(Fore.YELLOW  + "2) 🟡 Ejecutar BOLSA BMV      ")
    print(Fore.GREEN   + "3) 🟢 Copiar Resultados BMV/BIVA ")
    print(Fore.BLUE    + "4) 🔵 Mandar Email               ")
    print("")
    print(Fore.MAGENTA + "?) 🟣 Ayuda                      ")
    print(Fore.RED     + "x) ❌ Salir del programa   " + Fore.WHITE + "    (.v3)")
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
        elif option == '4':
            paso4()
        elif option == '?':
            pasoHelp()
        elif option.upper() == 'X':
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
