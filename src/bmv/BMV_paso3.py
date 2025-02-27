# ----------------------------------------------------------------------------------------
#  PASO3: CREA EXCEL CON LA LISTA DE EMISORES FINALES 
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO DEL PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso3(var_NombreSalida, var_FechasSalida):
    
    # Leer el excel de entrada con las URLs filtadas de Deudas
    df_paso3_a = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso2_a_{var_FechasSalida}.xlsx')
    df_paso3_a['FILTRO'] = "CAPITAL"
    df_paso3_b = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso2_b_{var_FechasSalida}.xlsx')
    df_paso3_b['FILTRO'] = "DEUDA"

    # Realizar el merge de ambos DataFrames con un 'outer' join para no perder ningún registro
    df_resultado = pd.merge(df_paso3_a, df_paso3_b, on=['CLAVE', 'CODIGO'], how='outer', suffixes=('_A', '_B'))
    
    # Crear una nueva columna 'VALOR_A' que combine los valores de 'VALOR_A_A' y 'VALOR_A_B'
    df_resultado['FILTRO'] = df_resultado.apply(
        lambda row: 'JOIN' if pd.notna(row['FILTRO_A']) and pd.notna(row['FILTRO_B']) else (
            row['FILTRO_A'] if pd.notna(row['FILTRO_A']) else row['FILTRO_B']
        ),
        axis=1
    )

    # Eliminar las columnas 'VALOR_A_A' y 'VALOR_A_B' que ya no necesitamos
    df_resultado = df_resultado[['CLAVE', 'CODIGO', 'FILTRO']]

    # Concatenacición de ambas tablas para obtener solo las URL
    df_paso3_concat = pd.concat([df_paso3_a, df_paso3_b],ignore_index=True )
    # Realizar el merge (left join) entre df_A y df_B usando 'CLAVE' y 'CODIGO'
    df_resultado2 = pd.merge(df_resultado, df_paso3_concat[['CLAVE', 'CODIGO', 'URL1', 'URL2', 'URL3']], 
                        on=['CLAVE', 'CODIGO'], how='left')
    
    # Eliminar duplicados
    df_resultado3 = df_resultado2.drop_duplicates(subset=['CLAVE', 'CODIGO', 'FILTRO'])
    df_resultado3 = df_resultado3.reset_index(drop=True)  # Reinicio indices
    
    # Creo un excel con el resultado del DataFrame
    df_resultado3.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso3_{var_FechasSalida}.xlsx',sheet_name='URL', index=False)
    print(f"        -  Datos temporales guardados en el excel {sTv.var_RutaInforme}{var_NombreSalida}_paso3_{var_FechasSalida}.xlsx")
    print(df_resultado3.head(2))
