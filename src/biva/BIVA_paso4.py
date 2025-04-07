# ----------------------------------------------------------------------------------------
#  PASO4: CREA XLS CON LOS DATOS FINALES
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------
def sTv_paso4_uno_DF(df_datos1, df_grupo1):
    
    # Customizamos el DATAFRAME 1 -------------------------
    # Convertir la columna 'FECHA' a tipo datetime
    df_datos1['FECHAx'] = pd.to_datetime(df_datos1['FECHA'], format='%d/%m/%Y %H:%M')

    df_datos1.drop(columns=['FECHA'], inplace=True)

    # Crear una columna 'FECHA' solo con la fecha
    df_datos1['FECHA'] = df_datos1['FECHAx'].dt.strftime('%d-%m-%Y')
    
    # Crear una columna 'HORA' solo con la hora
    df_datos1['HORA'] = df_datos1['FECHAx'].dt.strftime('%H:%M')


    # Borro el campo FECHA formato date_hora
    df_datos1.drop(columns=['FECHAx'], inplace=True)

    # otro
    df_datos1['CODIGO'] = df_datos1['CODIGO'].fillna(0).astype(int)

    # Customizamos el DATAFRAME 2 -------------------------
    df_grupo1.drop(columns=['CODIGO', 'FILTRO', 'C3'], inplace=True)

    # Hago un merge de ambos DATAFRAMES 
    df_merge = df_datos1.merge(df_grupo1, on="CLAVE", how="left")

    # Ordenar los campos del DATAFRAME MERGE
    df_merge = df_merge[['CLAVE', 'CODIGO', 'SECCION', 'FECHA', 'HORA', 'ASUNTO', 'URL', 'GRUPO' , 'TO', 'CC', 'ESTADO']]

    # Aplicar el filtro del excel a las celdas
    df_filtro = df_merge[df_merge['ESTADO'] == 'S']

    return df_filtro


# ----------------------------------------------------------------------------------------
#                               INICIO PASO 4
# ---------------------------------------------------------------------------------------- 
def sTv_paso4(var_NombreSalida, var_Fechas1, var_Entorno):
 
    # Leemos los datos de entrada
    df_datos = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso3.xlsx', sheet_name="PASO3")

    # Leemos los filtros y emails
    df_grupo = pd.read_excel(f'{sTv.var_RutaConfig}{sTv.var_NombreEmisores}_{var_Entorno}.xlsx', sheet_name="FILTRO")

    print(f'- Creo excel los datos Finales ')
    df_paso4 = sTv_paso4_uno_DF(df_datos, df_grupo)

    # Creo un excel con la lista de emisores finales
    df_paso4.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso4.xlsx', sheet_name='PASO4', index=False)
    print(f"- Datos temporales guardados en {sTv.var_RutaWebFiles}{var_NombreSalida}_paso4.xlsx")    

    
    