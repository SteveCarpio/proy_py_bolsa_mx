# ----------------------------------------------------------------------------------------
#  PASO0: VALIDAR REQUISITOS PREVIOS 
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

# Función: Valida estructura de directorios CNBV
def valida_carpetas(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(Fore.GREEN + f'Carpeta creada:    {ruta_carpeta}')
    else:
        print(Fore.CYAN  + f'Carpeta validada:  {ruta_carpeta}')

# Función: Borrar files creados CNBV
def borrar_archivos(ruta_carpeta, patron):
    # Construir la ruta completa con el patrón
    ruta_completa = os.path.join(ruta_carpeta, patron)
    
    # Encontrar todos los archivos que coincidan con el patrón
    archivos = glob.glob(ruta_completa)
    
    # Borrar cada archivo encontrado
    for archivo in archivos:
        os.remove(archivo)
        print(Fore.RED + f'Archivo borrado:   {archivo}')
        

# Función: Buscar Versión de GoogleChrome        
def obtener_version_GoogleChrome():
    try:
        # Ruta del registro donde se almacena la versión de Chrome
        ruta_registro = r"SOFTWARE\Google\Chrome\BLBeacon"
        clave_registro = winreg.OpenKey(winreg.HKEY_CURRENT_USER, ruta_registro)
        version, _ = winreg.QueryValueEx(clave_registro, "version")
        version_chrome = version
    except FileNotFoundError:
        print("Google Chrome no está instalado o no se encontró en el registro.")
        version_chrome = "none"

    if version_chrome != "none":
        ultima_parte = version_chrome.split('.')[0] 
    else:
        ultima_parte = "0"

    print(f" Versión de GoogleChrome {version_chrome} ")
    return ultima_parte

# Función: Buscar Versión de ChromeDriver
def obtener_version_ChromeDriver(chromedriver_path):
    try:
        # Verificar si el archivo chromedriver.exe existe en la ruta especificada
        if os.path.exists(chromedriver_path):
            # Ejecutar el comando para obtener la versión de chromedriver
            chromedriver_version_output = subprocess.check_output(
                f'"{chromedriver_path}" --version', 
                shell=True, 
                text=True
            )

            # Mostrar la salida completa de la versión
            print(f" Versión de {chromedriver_version_output}")

            # Extraer solo el número mayor (por ejemplo, '115')
            major_version = chromedriver_version_output.split()[1].split('.')[0]

            # Guardar en una variable
            return major_version
        else:
            print(f"El archivo chromedriver no se encuentra en la ruta: {chromedriver_path}")
            return "Ruta_No_Existe"
    except subprocess.CalledProcessError as e:
        print(f"Error_obtener_versión_chromedriver: {e}")
        return "1"

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso0(var_NombreSalida, var_FechasSalida, var_Fechas3):
    # Valida carpetas
    valida_carpetas(sTv.var_RutaRaiz)
    valida_carpetas(sTv.var_RutaWebFiles)
    valida_carpetas(sTv.var_RutaInforme)
    valida_carpetas(sTv.var_RutaLog)

    # Borra todos los files 
    borrar_archivos(sTv.var_RutaWebFiles, f'{var_NombreSalida}_paso1_*.html')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso2_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso3_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso4_*.xlsx')
    borrar_archivos(sTv.var_RutaWebFiles, f'{var_NombreSalida}_paso5_*.html')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso6_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso7_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_{var_Fechas3}_?.xlsx')
    
    # Validar versiones de GoogleChrome y ChromeDriver
    verGoogleChrome = obtener_version_GoogleChrome()
    chromedriver_path = f"C:\\MisCompilados\\cfg\\chromedriver-win32\\{verGoogleChrome}\\chromedriver.exe"
    verChromeDriver = obtener_version_ChromeDriver(chromedriver_path)
    if verChromeDriver == verGoogleChrome:
        print(f"OK: Versiones Igualadas GoogleChrome {verGoogleChrome} y ChromeDriver {verChromeDriver}")
    else:
        print(f"¡¡¡ATENCIÓN!!!: No se encuentra GoogleChrome o ChromeDriver o las Versiones son distintas:")
        print(f"                GoogleChrome: '{verGoogleChrome}' - Registro: 'SOFTWARE\\Google\\Chrome\\BLBeacon' ")
        print(f"                ChromeDriver: '{verChromeDriver}' - Ruta: {chromedriver_path}")
        print(f"\n     ** Si el problema puede ser GoogleChrome: ")
        print(f"            Es importante que este instalado en su ruta por defecto")
        print(f"            El usuario que ejecuta el proceso tenga acceso al registros de Windows ")
        print(f"            Comprobar si en el registro de windows exite: 'SOFTWARE\\Google\\Chrome\\BLBeacon' ")
        print(f"\n     ** Si el problema puede ser ChromeDriver prueba a copiar el file que tenemos en la ruta: ")
        print(f"            c:\\MisCompilados\\cfg\\chromedriver-win32\\'seleccione-version-igual-GoogleChrome'\\ ")
        print(f"        A la ruta Raiz del controlador ")
        print(f"            c:\\MisCompilados\\cfg\\chromedriver-win32\\ ")
        print(f"   Para más ayuda contactar con: SteveCarpio (stv.madrid@gmail.com) ")
        time.sleep(4)
        #sys.exit()

    print(Fore.WHITE + "\nRequisitos previos ok\n")
