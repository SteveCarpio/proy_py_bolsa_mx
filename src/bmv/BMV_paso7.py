# ----------------------------------------------------------------------------------------
#  PASO7: CREA OTRO EXCEL RESUMEN SEGÚN LOS CRITERIOS DEFINIDOS
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO DEL PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso7(var_NombreSalida, var_FechasSalida, tiempo_inicio):
    
    # Leer el excel de entrada con las URLs filtadas de Deudas
    df_paso7 = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso6_{var_FechasSalida}.xlsx')

    #Leer el excel de emisores para traernos las columnas: 'CODIGO','GRUPO','TO','CC'
    df_emiso = pd.read_excel(f'{sTv.var_RutaConfig}{sTv.var_NombreEmisores}.xlsx', sheet_name='FILTRO')
    df_emiso = df_emiso[['CODIGO','GRUPO','TO','CC']]  # me quedo solo con esas columnas
    
    # Convierto el campo FECHA en formato DATETIME
    df_paso7['FECHA2'] = pd.to_datetime(df_paso7['FECHA'], dayfirst=True)

    # Filtrar los registros con 1 día de diferencia entre 'fecha' y la fecha de hoy
    hoy = tiempo_inicio
    df_filtro1 = df_paso7[(hoy - df_paso7['FECHA2']).dt.days == 1]

    # FILTRA las filas que cumplan las condiciones:
    # - SECCION es "Resumen de Acuerdos de Asamblea" o "Convocatorias de Asambleas"
    # - ASUNTO "NO" contiene la palabra "TENEDORES"
    df_filtro2 = df_filtro1[~((df_filtro1['SECCION'].isin(['Resumen de Acuerdos de Asamblea', 'Convocatorias de Asambleas'])) & 
                    (~df_filtro1['ASUNTO'].str.contains('TENEDORES', case=False)))]
    
    # Elimino el campo FECHA2 de apoyo
    df_filtro3 = df_filtro2.drop('FECHA2', axis=1)
    
    # Agrego los campos TO y CC del DF emisores
    df_filtro4 = pd.merge(df_filtro3, df_emiso, on='CODIGO', how='left')
    
    # Reinicio indices
    df_paso7_salida = df_filtro4.reset_index(drop=True)  
    # Creo un excel con el resultado del DataFrame
    df_paso7_salida.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso7_{var_FechasSalida}.xlsx',sheet_name='URL', index=False)
    print(f"- Datos temporales guardados en el excel {sTv.var_RutaInforme}{var_NombreSalida}_paso7_{var_FechasSalida}.xlsx\n")
    print(df_paso7_salida)
    print(f'{sTv.var_WarningEmisores}')
   