# ----------------------------------------------------------------------------------------
#  PASO2: CREA XLS CON LAS URLs PARA EXTRAER LA INFO DE LA BOLSA
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso2_lee_html(var_NombreSalida):

    # Ajustar la configuración para mostrar el texto completo en las columnas sin truncar
    pd.set_option('display.max_colwidth', None)  # None para no truncar

    # Var con el HMTL generado
    html_content = f'{sTv.var_RutaWebFiles}{var_NombreSalida}_paso1.html'  

    # Leo Todo el contenido del excel en una variable
    with open(html_content, "r", encoding="utf-8") as file:
        html_content = file.readlines() 

    # Filtro solo las cadenas que necesito del HMTL
    filtered_lines = [line.strip() for line in html_content if "/es/emisoras/perfil/-" in line]

    # Creo un df vacio
    df_paso2 = pd.DataFrame(columns=['CLAVE', 'CODIGO', 'URL1', 'URL2', 'URL3'])

    # Customizo cada linea filtrada del HTML y le añado el resto de la URL al DataFrame
    for line in filtered_lines:
        salida1 = line.split('"')[2].replace('</a></td>','').replace('>','').strip()        # CLAVE
        salida2 = line.split('"')[1].replace('/es/emisoras/perfil/','').replace('-','')     # CODIGO 
        salida3 = f'{sTv.var_WEBSCRAPING2}-{salida2}'                                       # URL 1
        salida4 = f'{sTv.var_WEBSCRAPING3}{salida1}-{salida2}-CGEN'                         # URL 2  quito _DEUD y _CAPT
        salida5 = f'{sTv.var_WEBSCRAPING4}{salida1}-{salida2}-CGEN'                         # URL 3  quito _DEUD y _CAPT
                
        # Crear un DataFrame con esos valores
        nueva_fila = pd.DataFrame([[salida1, salida2, salida3, salida4, salida5]], columns=['CLAVE', 'CODIGO', 'URL1', 'URL2', 'URL3'])
        df_paso2 = pd.concat([df_paso2, nueva_fila], ignore_index=True)
  

    # Creo un excel con el resultado del DataFrame
    df_paso2.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso2.xlsx',sheet_name='URL', index=False)
    print(f"- Datos temporales guardados en el excel {sTv.var_RutaInforme}{var_NombreSalida}_paso2.xlsx")
    print(df_paso2.head(2))
    print("\n")

def sTv_paso2(var_NombreSalida):
    sTv_paso2_lee_html(var_NombreSalida)
    