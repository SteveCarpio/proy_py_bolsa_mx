# ----------------------------------------------------------------------------------------
#  PASO0: VALIDAR REQUISITOS PREVIOS 
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BOLSAS_variables as sTv
from   cfg.BOLSAS_librerias import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------

# Función: Valida estructura de directorios
def valida_carpetas(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(Fore.GREEN + f'Carpeta creada:    {ruta_carpeta}')
    else:
        print(Fore.CYAN  + f'Carpeta validada:  {ruta_carpeta}')

# Función: Borrar files creados
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

def sTv_paso0(var_Fechas3):
    # Valida carpetas
    valida_carpetas(sTv.var_RutaRaiz)
    valida_carpetas(sTv.var_RutaInforme)
    valida_carpetas(sTv.var_RutaLog)

    # Borra todos los files temporales de BIVA
    borrar_archivos(sTv.var_RutaInforme,  f'BIVA_*_M.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'BIVA_*_P.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'BIVA_*_X.xlsx')
    
    # Borra todos los files temporales de BMV
    borrar_archivos(sTv.var_RutaInforme,  f'BMV_*_M.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'BMV_*_P.xlsx')
    borrar_archivos(sTv.var_RutaInforme,  f'BMV_*_X.xlsx')
      
    print(Fore.WHITE + "\nRequisitos previos ok\n")
