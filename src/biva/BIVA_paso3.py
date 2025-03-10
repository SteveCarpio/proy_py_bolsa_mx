# ----------------------------------------------------------------------------------------
#  PASO3: CREA XLS AÑADIENDO LOS ID DE LOS EMISORES
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------
def sTv_paso3_crea_ID_emisores():

    # Leer el contenido del archivo HTML
    with open(f'{sTv.var_RutaWebFiles}BIVA_paso1_pag1.html', "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Buscar todos las opciones dentro del select con id="clave_emisoras"
    options = soup.select("#claves_emisoras option")

    # Extraer los valores de los atributos 'value' y separarlos en dos campos
    data = []
    for option in options:
        value = option.get('value')
        if value:  # Verificamos que haya un valor
            campo1, campo2 = value.split('_')  # Separamos por el guión bajo
            data.append({"CLAVE": campo2, "CODIGO": campo1})

    # Crear un DataFrame a partir de los datos
    df = pd.DataFrame(data)
    return df

def sTv_paso3_crea_df_final(var_NombreSalida, df_id,var_Fechas1 ):
    
    # Leo excel del paso2 en un dataframe
    df_lista = pd.read_excel(f"{sTv.var_RutaInforme}{var_NombreSalida}_paso2.xlsx", sheet_name="PASO2")

    # Hago un merge de ambos df
    df_merge = df_lista.merge(df_id, on="CLAVE", how="left")

    # Reorganizo la posición de los campos
    df_merge = df_merge[['CLAVE', 'CODIGO', 'SECCION', 'FECHA', 'ASUNTO']]

    url1 = f"https://www.biva.mx/empresas/emisoras_inscritas/emisoras_inscritas?emisora_id="
    url2 = f"&tipoInformacion=null&tipoDocumento=null&fechaInicio="
    url3 = f"&fechaFin="
    url4 = f"&periodo=null&ejercicio=null&tipo=null&subTab=2&biva=null&canceladas=false&page=1"

    df_merge['URL'] = url1 + df_merge['CODIGO'] + url2 + var_Fechas1 + url3 + var_Fechas1 + url4
    
    return df_merge

# ----------------------------------------------------------------------------------------
#                               INICIO PASO 3
# ---------------------------------------------------------------------------------------- 
def sTv_paso3(var_NombreSalida, var_Fechas1):
 
    print(f'- Creo excel con los ID Emisores ')
    df_paso3       = sTv_paso3_crea_ID_emisores()
    # Creo un excel con la lista de emisores
    df_paso3.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso3_id_emisores.xlsx',sheet_name='ID', index=False)
    print(f"- Datos temporales guardados en {sTv.var_RutaInforme}{var_NombreSalida}_paso3_id_emisores.xlsx")    

    print(f'- Creo excel agregando los ID Emisores"')
    df_paso3_final = sTv_paso3_crea_df_final(var_NombreSalida, df_paso3, var_Fechas1) 
     # Creo un excel con el resultado del DataFrame
    df_paso3_final.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso3.xlsx',sheet_name='PASO3', index=False)
    print(f"- Datos temporales guardados en {sTv.var_RutaInforme}{var_NombreSalida}_paso3.xlsx")
    