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
        

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso0(var_NombreSalida, var_FechasSalida):
    # Valida carpetas de CNBV
    valida_carpetas(sTv.var_RutaRaiz)
    valida_carpetas(sTv.var_RutaWebFiles)
    valida_carpetas(sTv.var_RutaInforme)

    # Borra todos los files 
    borrar_archivos(sTv.var_RutaWebFiles, f'{var_NombreSalida}_paso1_*.html')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso2_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso3_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso4_*.xlsx')
    borrar_archivos(sTv.var_RutaWebFiles, f'{var_NombreSalida}_paso5_*.html')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso6_*.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'{var_NombreSalida}_paso7_*.xlsx')
    
    print(Fore.WHITE + "\nRequisitos previos ok\n")
