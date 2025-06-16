# ----------------------------------------------------------------------------------------
#  PASO5: CREO EXCEL BOLSAS PARA SUBIRLO A ORACLE
#  Autor: SteveCarpio-2025
#
#  BOLSAS: Excel con los datos finales, datos preparados para que sean subidos a Oracle
#  N	CLAVE	SECCION	   FECHA	    ASUNTO	             URL	                ARCHIVO	               ORIGEN	T	  FILTRO
#  -------------------------------------------------------------------------------------------------------------------------------
#  1	CAMSCB	Tenedores  2024-12-26	Aviso de Tenedores   https://www.bmv.com	https://www.bmv.com	   BMV	    P	  INCLUIR
#  2	CAMSCB	Tenedores  2024-12-26   Aviso de Tenedores   https://www.biva.com   https://www.biva.com   BIVA	    M	  EXCLUIR
#
#  BMW: Excel que se manda en formato DF en un email  
#	CLAVE	SECCION	  FECHA	       ASUNTO	             URL	                ARCHIVO                                   (email normal)
#	CLAVE	SECCION	  FECHA	       ASUNTO	             URL	                ARCHIVO	                     EMAIL(P/M)   (email excluidos)
#
#  BIVA: Excel que se manda en formato DF en un email
#	CLAVE	SECCION	  FECHA	       ASUNTO	             URL                                                              (email normal) 
#	CLAVE	SECCION	  FECHA	       ASUNTO	             URL	                                             EMAIL(P/M)   (email excluidos)
# ----------------------------------------------------------------------------------------

import cfg.BOLSAS_variables as sTv
from   cfg.BOLSAS_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------

# Función Leer excel y convertirlos en DataFrame
def sTv_paso5_lee_DF(ruta, bolsa, tipo):
    # Verificar si el archivo existe
    if os.path.exists(ruta):
        try:
            df = pd.read_excel(ruta, index_col=0)
            print(f"- Archivo encontrado: {ruta}")
            columnas=['CLAVE','SECCION','FECHA','ASUNTO','URL','ARCHIVO','ORIGEN','T','FILTRO']

            # Convertir al tipo datetime y luego formatear
            df['FECHA'] = pd.to_datetime(df['FECHA'], format="%d-%m-%Y")

            # Formateamos cada DataFrame
            if bolsa == "BIVA_X":
                df['ARCHIVO'] = ""
                df['ORIGEN'] = "BIVA"
                df['T'] = df['EMAIL']
                df['FILTRO'] = "EXCLUIR"
                df = df.drop('EMAIL', axis=1)
            if bolsa == "BMV_X":
                df['ORIGEN'] = "BMV"
                df['T'] = df['EMAIL']
                df['FILTRO'] = "EXCLUIR"
                df = df.drop('EMAIL', axis=1)
            if bolsa == "BIVA":
                df['ARCHIVO'] = ""
                df['ORIGEN'] = "BIVA"
                df['T'] = tipo
                df['FILTRO'] = "INCLUIR"
            if bolsa == "BMV":
                df['ORIGEN'] = "BMV"
                df['T'] = tipo
                df['FILTRO'] = "INCLUIR"
            # Reorganizo el orden de las columnas  
            df = df[columnas]
            return df
        except Exception as e:
            print(f"- Error al leer el archivo: {e} - {ruta} - {bolsa} - {tipo}")
            return None
    else: 
        return None

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso5(var_NombreSalida, var_Fechas2, var_Fechas3):
    
    # Crear un DataFrame VACIÓ para con los DatosAcumulados
    df_TOTAL = pd.DataFrame()

    # Ruta del archivo Excel
    ruta_excel1 = f"{sTv.var_RutaInforme}BIVA_{var_Fechas3}_M.xlsx"
    ruta_excel2 = f"{sTv.var_RutaInforme}BIVA_{var_Fechas3}_P.xlsx"
    ruta_excel5 = f"{sTv.var_RutaInforme}BIVA_{var_Fechas3}_X.xlsx"
    ruta_excel3 = f"{sTv.var_RutaInforme}BMV_{var_Fechas3}_M.xlsx"
    ruta_excel4 = f"{sTv.var_RutaInforme}BMV_{var_Fechas3}_P.xlsx"
    ruta_excel6 = f"{sTv.var_RutaInforme}BMV_{var_Fechas3}_X.xlsx"
    ruta_excelT = f"{sTv.var_RutaInforme}BOLSAS_{var_Fechas3}.xlsx"

    # Leer el archivo o crear el DataFrame por defecto
    df_BIVA_M = sTv_paso5_lee_DF(ruta_excel1, "BIVA"  ,"M")
    df_BIVA_P = sTv_paso5_lee_DF(ruta_excel2, "BIVA"  ,"P")
    df_BIVA_X = sTv_paso5_lee_DF(ruta_excel5, "BIVA_X"," ")
    df_BMV_M = sTv_paso5_lee_DF(ruta_excel3,  "BMV"   ,"M")
    df_BMV_P = sTv_paso5_lee_DF(ruta_excel4,  "BMV"   ,"P")
    df_BMV_X = sTv_paso5_lee_DF(ruta_excel6,  "BMV_X" ," ")

    # Si RETURN df_xxxxxx es un DF lo concatena en el df_TOTAL
    if isinstance(df_BIVA_M, pd.DataFrame):
        df_TOTAL = pd.concat([df_TOTAL, df_BIVA_M], ignore_index=True)
    if isinstance(df_BIVA_P, pd.DataFrame):
        df_TOTAL = pd.concat([df_TOTAL, df_BIVA_P], ignore_index=True)
    if isinstance(df_BIVA_X, pd.DataFrame):
        df_TOTAL = pd.concat([df_TOTAL, df_BIVA_X], ignore_index=True)
    if isinstance(df_BMV_M, pd.DataFrame):
        df_TOTAL = pd.concat([df_TOTAL, df_BMV_M], ignore_index=True)
    if isinstance(df_BMV_P, pd.DataFrame):
        df_TOTAL = pd.concat([df_TOTAL, df_BMV_P], ignore_index=True)
    if isinstance(df_BMV_X, pd.DataFrame):
        df_TOTAL = pd.concat([df_TOTAL, df_BMV_X], ignore_index=True)

    if len(df_TOTAL) > 0:

        # Reasignar el índice para que empiece en 1
        df_TOTAL.index = range(1, len(df_TOTAL) + 1)

        # Cambio el nombre del índice a N en vez de que salga vació
        df_TOTAL.index.name = "N"

        # Exportar el DataFrame a un Excel
        df_TOTAL.to_excel(ruta_excelT,index=True,sheet_name="DATOS")

        print(df_TOTAL)
    else:
        print(f"No hay datos de BIVA o BMV para crear el excel de salida {ruta_excelT}")
