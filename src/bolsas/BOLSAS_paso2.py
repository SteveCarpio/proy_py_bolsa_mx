# ----------------------------------------------------------------------------------------
#  PASO2: EJECUTA LA APP DE BIVA
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BOLSAS_variables as sTv
from   cfg.BOLSAS_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso2(tiempo_inicio):
  
    # Ruta al archivo .exe
    ruta_programa = f"{sTv.var_RutaCompile}{sTv.var_NombreBIVA}"

    # Convertir tiempo_inicio a cadena en el formato adecuado
    tiempo_inicio_str = tiempo_inicio.strftime("%Y-%m-%d %H:%M:%S.%f")

    # Parámetros a pasar al ejecutable
    param = ["RUN-NO-EMAIL", "2025-03-05 00:00:00.000000"]

    # Ejecutar el programa y capturar la salida
    try:
        resultado = subprocess.run([ruta_programa] + param, check=True, capture_output=True, text=True)
        print("Salida del programa: \n", resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el programa: {e}")
