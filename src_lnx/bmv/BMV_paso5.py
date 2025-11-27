# ----------------------------------------------------------------------------------------
#  PASO4: DESCARGA HTML DE TODOS LOS EMISORES FILTRADOS
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *
import urllib3

# Deshabilita todas las advertencias de "InsecureRequestWarning"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# pip install -U requests urllib3 certifi   STV: si falla actualia los certificados TLS

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

# Modificado: Se agrego el uso de Session y Timeout para las peticiones request
def sTv_paso5_Descarga_Html(var_NombreSalida, var_FechasSalida, df):

    session = requests.Session()  # Mantiene la conexión
    num_registros = len(df)
    cont = 0

    for i, row in df.iterrows():
        cont += 1
        CLA  = f'{row.iloc[0]}' #  Campo CLAVE PIZARRA
        COD  = f'{row.iloc[1]}' #  Campo CODIGO
        URL2 = f'{row.iloc[4]}' #  Campo URL2
        URL3 = f'{row.iloc[5]}' #  Campo URL3

        print(f"({cont}/{num_registros}) Analizando URL2: {URL2}  -  URL3: {URL3}")

        for idx, url in [(2, URL2), (3, URL3)]:
            try:
                response = session.get(url, timeout=10)  # + timeout
                if response.status_code == 200:
                    filename = f"{sTv.var_RutaWebFiles}{var_NombreSalida}_paso5_{var_FechasSalida}_{COD}_{idx}.html"
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(response.text)
                else:
                    print(f"[{idx}] Error HTTP {response.status_code} en {url}")
            except requests.exceptions.RequestException as e:
                print(f"[{idx}] Error al solicitar {url}: {e}")

            time.sleep(1)  # Pausa entre peticiones para evitar bloqueos

def sTv_paso5(var_NombreSalida, var_FechasSalida):
    df = sTv_paso5_Crear_DataFrame(var_NombreSalida, var_FechasSalida)
    sTv_paso5_Descarga_Html(var_NombreSalida, var_FechasSalida, df)

#var_NombreSalida= 'BMV_v2'
#var_FechasSalida="20250220_150329"
#sTv_paso5(var_NombreSalida, var_FechasSalida)

