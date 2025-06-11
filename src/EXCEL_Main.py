import win32com.client
import os
import time

def Actualiza_Excel(ruta, file):
    ruta_excel = os.path.join(ruta, file)
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
        # Asegurarse de cerrar Excel aunque haya errores
        try:
            excel.Quit()
        except:
            pass

# ------------------------------------------------

ruta = r"C:\MisCompilados\PROY_BOLSA_MX\INFORMES"
files = [
    "Eventos_Relevantes_Completo.xlsx",
    "Eventos_Relevantes_Patricia.xlsx",
    "Eventos_Relevantes_Monica.xlsx",
]

for f in files:
    Actualiza_Excel(ruta, f)