# ----------------------------------------------------------------------------------------
#  PASO1:  Importar Datos de Entrada, si existe el excel lo leerá en formato dataframe
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.ORACLE_variables as sTv
from   cfg.ORACLE_librerias import *

# ----------------------------------------------------------------------------------------
#                                  FUNCIONES
# ----------------------------------------------------------------------------------------
        
# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso1(var_Fechas3):
    
    rutaEntrada=f'{sTv.var_RutaIN}{sTv.var_Files_IN}_{var_Fechas3}.xlsx'

    try:

        # Valida si Existe el Excel de entrada
        if os.path.exists(rutaEntrada):
            print(f'OK Existe el fichero: {rutaEntrada}')
            sTv.df_Global = pd.read_excel(f'{sTv.var_RutaIN}{sTv.var_Files_IN}_{var_Fechas3}.xlsx',sheet_name='DATOS')
            print(f'Se han leído {len(sTv.df_Global)} registros')

            # Valida que tenga registros el DataFrame
            if len(sTv.df_Global) == 0:
                print(f'El excel de entrada NO tiene registros: {rutaEntrada}')
                sys.exit(0)

            # Valida que tenga las columnas requeridas
            columnas_requeridas=['CLAVE','SECCION','FECHA','ASUNTO','URL','ARCHIVO','ORIGEN','T','FILTRO']
            if all(col in sTv.df_Global.columns for col in columnas_requeridas):
                print("El DataFrame tiene todas las columnas requeridas.")
                print(Fore.CYAN + f'{columnas_requeridas}')
            else:
                faltantes = [col for col in columnas_requeridas if col not in sTv.df_Global.columns]
                print(Fore.RED + f"Faltan las siguientes columnas: {faltantes}")

        else:
            print(f'NO Existe el fichero: {rutaEntrada}')

    except Exception as e:
        print(f"Error al leer el archivo: {rutaEntrada} \n{e} ")
        sys.exit(0)
