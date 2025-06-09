# ----------------------------------------------------------------------------------------
#  PASO1:  
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

    # Leer excel de entrada
    if os.path.exists(rutaEntrada):
        print(f'OK Existe: {rutaEntrada}')
        sTv.df_Total = pd.read_excel(f'{sTv.var_RutaIN}{sTv.var_Files_IN}_{var_Fechas3}.xlsx',sheet_name='DATOS')
        if len(sTv.df_Total) == 0:
            print(f'El excel de entrada debe tener 0 registros: {rutaEntrada}')
            sys.exit(0)
    else:
        print(f'NO Existe: {rutaEntrada}')
