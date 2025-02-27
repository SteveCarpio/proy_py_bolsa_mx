# ----------------------------------------------------------------------------------------
#  PASO4: CREA EXCEL FILTRANDO LA LISTA DE EMISORES
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO DEL PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso4(var_NombreSalida, var_FechasSalida):
   
    # Leer el excel de entrada con las URLs filtadas
    df_paso4_a = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso3_{var_FechasSalida}.xlsx')
    df_paso4_b = pd.read_excel(f'{sTv.var_RutaConfig}{sTv.var_NombreEmisores}.xlsx', sheet_name='FILTRO')
    
    # Verifica si se creo o elimino Emisores
    registros_a = len(df_paso4_a)
    registros_b = len(df_paso4_b)

    if registros_a != registros_b:
        print(f"        -  WARNING: El número de Emisores es distinto ()")
        print(f"        -           TABLA: ({var_NombreSalida}_paso3_{var_FechasSalida}.xlsx) tiene ({registros_a}) registros")
        print(f"        -           TABLA: ({sTv.var_NombreEmisores}.xlsx) tiene ({registros_b}) registros")
        sTv.var_WarningEmisores = f"WARNING: {var_NombreSalida}_paso3_{var_FechasSalida}.xlsx ({registros_a} --VS-- BMV_Filtro_Emisores.xlsx {registros_b})"
    else:
        print(f"        -  OK, mismo número de Emisores en ambas tablas: ({registros_a}) registros")

    df_resultado = pd.merge(df_paso4_a, df_paso4_b[['CLAVE', 'CODIGO', 'ESTADO', 'GRUPO','TO','CC','C3']], on=['CLAVE', 'CODIGO'], how='left')
    
    # Creo un excel con el resultado del DataFrame
    df_resultado.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso4_{var_FechasSalida}.xlsx',sheet_name='URL', index=False)
    print(f"        -  Datos Finales con los emisores filtrados {sTv.var_RutaInforme}{var_NombreSalida}_paso4_{var_FechasSalida}.xlsx\n")
