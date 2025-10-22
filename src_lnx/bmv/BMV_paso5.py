# ----------------------------------------------------------------------------------------
#  PASO4: DESCARGA HTML DE TODOS LOS EMISORES FILTRADOS
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO DEL PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso5_Crear_DataFrame(var_NombreSalida, var_FechasSalida):
    # Leer el excel de entrada con las URLs filtadas
    df_paso5 = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso4_{var_FechasSalida}.xlsx')

    # Filtrar las columnas campo1, campo2 y donde campo3 sea igual a "S"
    df_paso5_filtrado = df_paso5[df_paso5['ESTADO'] == 'S'].reset_index(drop=True)

    # Cambia el índice para que empiece en 1
    df_paso5_filtrado.index = df_paso5_filtrado.index + 1  

    return df_paso5_filtrado

def sTv_paso5_Descarga_Html(var_NombreSalida, var_FechasSalida, df):

    num_registros = len(df)
    cont = 0

    # Recorro el DataFrame con todas las URLs filtrados
    for i, row in df.iterrows():
        cont = cont + 1
        CLA  = f'{row.iloc[0]}'   #  Campo CLAVE PIZARRA
        COD  = f'{row.iloc[1]}'   #  Campo CODIGO
        URL2 = f'{row.iloc[4]}'   #  Campo URL2
        URL3 = f'{row.iloc[5]}'   #  Campo URL3

        # Realizamos la solicitud GET para obtener el contenido HTML
        response2 = requests.get(URL2)
        response3 = requests.get(URL3)

        print(f"({cont}/{num_registros}) Analizando URL2: {URL2}  -  URL3: {URL3}")

        # Comprobamos si la solicitud fue exitosa URL2 (código de estado 200)
        if response2.status_code == 200:
            # Guardamos el contenido HTML 2 en un archivo .html
            with open(f"{sTv.var_RutaWebFiles}{var_NombreSalida}_paso5_{var_FechasSalida}_{COD}_2.html", "w", encoding="utf-8") as file:
                file.write(response2.text)  # Escribimos el contenido HTML en el archivo
        else:
            print(f"Error al descargar la página. Código de estado: {response2.status_code}")

        # Comprobamos si la solicitud fue exitosa URL3 (código de estado 200)
        if response3.status_code == 200:
            # Guardamos el contenido HTML 3 en un archivo .html
            with open(f"{sTv.var_RutaWebFiles}{var_NombreSalida}_paso5_{var_FechasSalida}_{COD}_3.html", "w", encoding="utf-8") as file:
                file.write(response3.text)  # Escribimos el contenido HTML en el archivo
        else:
            print(f"Error al descargar la página. Código de estado: {response3.status_code}")


def sTv_paso5(var_NombreSalida, var_FechasSalida):
    df = sTv_paso5_Crear_DataFrame(var_NombreSalida, var_FechasSalida)
    sTv_paso5_Descarga_Html(var_NombreSalida, var_FechasSalida, df)

#var_NombreSalida= 'BMV_v2'
#var_FechasSalida="20250220_150329"
#sTv_paso5(var_NombreSalida, var_FechasSalida)

