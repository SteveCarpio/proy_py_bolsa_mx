# ----------------------------------------------------------------------------------------
#  PASO2: EJECUTA LA APP DE BIVA
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BOLSAS_variables as sTv
from   cfg.BOLSAS_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------
def copiar_archivo(src, dst):
    # Verifica si el archivo de origen existe
    if not os.path.exists(src):
        print(f"- El archivo {src} no existe")
        return
        
    # Intentar copiar el archivo
    try:
        shutil.copy(src, dst)
        print(f"- El archivo {src} se ha copiado correctamente a {dst}")
    except PermissionError:
        print(f"- No se puede copiar el archivo. Puede que esté en uso o haya un problema de permisos.")
    except Exception as e:
        print(f"- Ha ocurrido un error al copiar el archivo: {e}")

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------
def sTv_paso3(var_Fechas3):
  
    ruta_destino = f"{sTv.var_RutaInforme}"
    ruta_origen1 = f"{sTv.var_RutaInformeBiva}BIVA_{var_Fechas3}_M.xlsx"
    ruta_origen2 = f"{sTv.var_RutaInformeBiva}BIVA_{var_Fechas3}_P.xlsx"
    ruta_origen5 = f"{sTv.var_RutaInformeBiva}BIVA_{var_Fechas3}_X.xlsx"
    ruta_origen3 = f"{sTv.var_RutaInformeBmv}BMV_{var_Fechas3}_M.xlsx"
    ruta_origen4 = f"{sTv.var_RutaInformeBmv}BMV_{var_Fechas3}_P.xlsx"
    ruta_origen6 = f"{sTv.var_RutaInformeBmv}BMV_{var_Fechas3}_X.xlsx"
    
    copiar_archivo(ruta_origen1, ruta_destino)
    copiar_archivo(ruta_origen2, ruta_destino)
    copiar_archivo(ruta_origen3, ruta_destino)
    copiar_archivo(ruta_origen4, ruta_destino)
    copiar_archivo(ruta_origen5, ruta_destino)
    copiar_archivo(ruta_origen6, ruta_destino)
