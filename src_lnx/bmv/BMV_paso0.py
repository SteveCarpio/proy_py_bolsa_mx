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
def obtener_version_GoogleChrome_WIN():
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

def obtener_version_GoogleChrome_LNX():
    """
    Devuelve la versión principal de Google Chrome usando dpkg.
    Si no se encuentra el paquete, devuelve "0".
    """
    try:
        # Ejecutamos dpkg y filtramos la línea que contiene "google-chrome"
        salida = subprocess.check_output(
            ["dpkg", "-l"],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for linea in salida.splitlines():
            if "google-chrome" in linea.lower() and "ii" in linea.split()[0]:
                # La línea tiene la forma: ii  google-chrome-stable  129.0.6668.65-1  ...
                partes = linea.split()
                if len(partes) >= 3:
                    # La versión del paquete
                    ver_paquete = partes[2]
                    # Eliminar el sufijo "-1", "-2", etc.
                    ver = ver_paquete.split('-')[0]
                    print(f" Versión de GoogleChrome {ver}")
                    return ver.split('.')[0]  # solo la parte antes del primer punto
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando dpkg: {e}")
    print("Google Chrome no encontrado con dpkg.")
    return "0"




# Función: Buscar Versión de ChromeDriver
def obtener_version_ChromeDriver(chromedriver_path):
    try:
        # Verificar si el archivo chromedriver existe en la ruta especificada
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
    verGoogleChrome = obtener_version_GoogleChrome_LNX()
    chromedriver_path = f"/srv/apps/MisCompilados/.cfg/chromedriver/chromedriver"
    verChromeDriver = obtener_version_ChromeDriver(chromedriver_path)
    if verChromeDriver == verGoogleChrome:
        print(f"OK: Versiones Igualadas GoogleChrome {verGoogleChrome} y ChromeDriver {verChromeDriver}")
    else:
        # Mensaje de advertencia
        print("¡¡¡ATENCIÓN!!!")
        print("No se encuentra Google Chrome/ChromeDriver o sus versiones no coinciden.\n")
        print("Detalles:")
        print(f"  • Google Chrome:   {verGoogleChrome}")
        print(f"  • ChromeDriver:    {verChromeDriver}\n")
        print("Pasos a seguir según el problema detectado:")
        # Si el problema está en Google Chrome
        print("\n  ** Problema con Google Chrome:")
        print("     1. Verifica la instalación con: dpkg -l | grep google-chrome")
        print("     2. Asegúrate de que exista un ChromeDriver compatible con esa versión.")
        print("     3. Puedes encontrar el driver adecuado en https://github.com/dreamshao/chromedriver")
        # Si el problema está en ChromeDriver
        print("\n  ** Problema con ChromeDriver:")
        print("     1. Descarga un ChromeDriver de la misma versión que Google Chrome.")
        print("     2. Copia el binario descargado (chromedriver) a la carpeta")
        print("        /srv/apps/MisCompilados/.cfg/chromedriver/<versión>")
        print("     3. Actualiza el enlace simbólico con la nueva versión descargada.\n")
        # Contacto de ayuda
        print("Para más ayuda, contacta con:")
        print("  SteveCarpio (stv.madrid@gmail.com)")
        time.sleep(4)
        sys.exit()

    print(Fore.WHITE + "\nRequisitos previos ok\n")
