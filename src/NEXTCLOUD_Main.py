# ----------------------------------------------------------------------------------------
#                                  WebScraping EXCEL_TO_NEXTCLOUD
# 
# Programa que abrirá un excel para actualizar sus conexiones de oracle (power query)
# y luego mandará el fichero excel a la nube de NextCloud
# Autor: SteveCarpio
# Versión: V1 2025
# ----------------------------------------------------------------------------------------

import win32com.client
import os
import time
import requests
import shutil

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------

# ----------------
def Actualiza_Excel(ruta1, file):
    ruta_excel = os.path.join(ruta1, file)
    print("Procesando:", ruta_excel)

    if not os.path.exists(ruta_excel):
        print(f"ERROR: El archivo no existe: {ruta_excel}")
        return

    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        libro = excel.Workbooks.Open(ruta_excel)

        print("Actualizando conexiones y consultas...")
        libro.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()
        time.sleep(5) # Espera extra en caso de conexiones lentas

        libro.Save()
        libro.Close(False)
        excel.Quit()
        print(f"Actualización completada: {file}")

    except Exception as e:
        print(f"Error al actualizar {file}: {e}")

    finally:
        # Es para asegurarse de cerrar Excel aunque haya errores
        try:
            excel.Quit()
        except:
            pass

# ----------------
def Copy_To_NextCloud(ruta1, file2):
    usuario = "usrtda"  
    password = "2lL%*laRc#gXm$"  
    archivo_local = os.path.join(ruta1, file2)
    webdav_url = "https://repo.titulizaciondeactivos.com/remote.php/dav/files/usrtda/Rep_Comun/Eventos_Relevantes.xlsx"

    with open(archivo_local, "rb") as f:
        response = requests.put(webdav_url, data=f, auth=(usuario, password))

    if response.status_code in [200, 201, 204]:
        print("Archivo subido con éxito")
    else:
        print(f"Error al subir el archivo: {response.status_code}\n{response.text}")

# ----------------
def Copy_Ruta_Red(ruta1, file, ruta2):
    # Rutas de ejemplo (ajusta según tus carpetas)
    origen = os.path.join(ruta1, file)
    destino = os.path.join(ruta2, file)

    # Copiar el archivo
    shutil.copy2(origen, destino)  # copy2 conserva la fecha de modificación

    print("Archivo copiado con éxito.")

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

# Defino parámetros de entrada
ruta1 = r"C:\MisCompilados\PROY_BOLSA_MX\INFORMES"
ruta2 = r"\\newton\comun$\Proyectos\Python\MisCompilados\PROY_BOLSA_MX\INFORMES"
file1="Eventos_Relevantes_Completo.xlsx"
file2="Eventos_Relevantes_Patricia.xlsx"
file3="Eventos_Relevantes_Monica.xlsx"

# Creo una lista con los 3 excels
files = [file1, file2, file3]

# Actualizo las conexiones de los 3 excels
for f in files:
    Actualiza_Excel(ruta1, f)

# Copio el excel de Patricia actualizado en Nextcloud
Copy_To_NextCloud(ruta1, file2)

# Copia los 3 excels actualizados en la Ruta de Red
for f in files:
    Copy_Ruta_Red(ruta1, f, ruta2)
