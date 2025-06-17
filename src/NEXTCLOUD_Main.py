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
from datetime import datetime as dt
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------

# Actualizo las conexiones de los 3 excels 
def Actualiza_Excel(ruta1, file):
    ruta_excel = os.path.join(ruta1, file)
    print("Procesando:", ruta_excel)

    if not os.path.exists(ruta_excel):
        print(dt.now())
        print(f"ERROR: El archivo no existe: {ruta_excel}")
        return

    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        libro = excel.Workbooks.Open(ruta_excel)

        print("   Actualizando conexiones y consultas...")
        libro.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()
        time.sleep(10) # Espera extra en caso de conexiones lentas

        libro.Save()
        libro.Close(False)
        excel.Quit()
        print(f"   Actualización completada: {file}")

    except Exception as e:
        print(dt.now())
        print(f"   Error al actualizar {file}: {e}")

    finally:
        # Es para asegurarse de cerrar Excel aunque haya errores
        try:
            excel.Quit()
        except:
            pass

# Copio el excel de Patricia actualizado en Nextcloud
def Copy_To_NextCloud(ruta1, file2):
    usuario = "usrtda"  
    password = "2lL%*laRc#gXm$"  
    archivo_local = os.path.join(ruta1, file2)
    webdav_url = "https://repo.titulizaciondeactivos.com/remote.php/dav/files/usrtda/Rep_Comun/Eventos_Relevantes.xlsx"
    print(f"Ruta Origen: {ruta1}")
    print(f"File Origen: {file2}")
    print(f"Ruta Destino: https://repo.titulizaciondeactivos.com/remote.php/dav/files/usrtda/Rep_Comun/")
    print(f"File Destino: Eventos_Relevantes.xlsx")
    print(f"Usuario: {usuario}")
    print(f"Password: {password}")

    with open(archivo_local, "rb") as f:
        response = requests.put(webdav_url, data=f, auth=(usuario, password), verify=False)


    if response.status_code in [200, 201, 204]:
        print("Archivo subido con éxito")
    else:
        print(dt.now())
        print(f"Error al subir el archivo: {response.status_code}\n{response.text}")

# Copia los 3 excels actualizados a la Ruta de Red
def Copy_Ruta_Red(ruta1, file, ruta2):
    try:
        # Rutas de ejemplo (ajusta según tus carpetas)
        origen = os.path.join(ruta1, file)
        destino = os.path.join(ruta2, file)

        # Copiar el archivo
        shutil.copy2(origen, destino)  # copy2 conserva la fecha de modificación

        print(f"Archivo ({ruta1}\\{file}) copiado con éxito a: {ruta2}")
    except Exception as e:
        print(dt.now())
        print(f"Error al copiar el archivo: ({ruta1}\\{file}) \n{e}")

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

print(f"\nInicio del Proceso: {dt.now()}")

# Defino parámetros de entrada
ruta1 = r"C:\MisCompilados\PROY_BOLSA_MX\INFORMES\EVENTOS_RELEVANTES"
ruta2 = r"\\newton\comun$\Proyectos\Python\MisCompilados\PROY_BOLSA_MX\INFORMES"
file1="Eventos_Relevantes_Completo.xlsx"
file2="Eventos_Relevantes_Patricia.xlsx"
file3="Eventos_Relevantes_Monica.xlsx"

# Creo una lista con los 3 excels
files = [file1, file2, file3]

# Actualizo las conexiones de los 3 excels
print("\nPASO1: Actualizo las conexiones de los 3 archivos Excel\n")
print("Este paso se realizará desde un script .bat, se script se invocará desde otro script .vbs")
#for f in files:
#    Actualiza_Excel(ruta1, f)

# Copio el excel de Patricia actualizado en Nextcloud
print("\nPASO2: Copio el Excel de Patricia actualizado a Nextcloud\n")
Copy_To_NextCloud(ruta1, file2)

# Copia los 3 excels actualizados a la Ruta de Red
print("\nPASO3: Copia los 3 archivos Excel actualizados a la Ruta de Red\n")
for f in files:
    Copy_Ruta_Red(ruta1, f, ruta2)

print(f"\nProceso Finalizado: {dt.now()}")