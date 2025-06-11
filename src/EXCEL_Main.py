import win32com.client
import os

def Actualiza_Excel(ruta, file):

    ruta_excel = f"{ruta}{file}"

    if not os.path.exists(ruta_excel):
        print(f"ERROR: El archivo no existe: {ruta_excel}")
        return

    # Iniciar Excel
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False                       # True para ver Excel en pantalla
    libro = excel.Workbooks.Open(ruta_excel)    # Abrir el libro
    libro.RefreshAll()                          # Actualizar todo (Power Query + conexiones)
    excel.CalculateUntilAsyncQueriesDone()      # Esperar a que termine la actualización es muy importante

    # Guardar y cerrar
    libro.Save()
    libro.Close(False)
    excel.Quit()

    print(f"Actualización completada: {file}")

# ------------------------------------------------

ruta = f"C:\\MisCompilados\\PROY_BOLSA_MX\\INFORMES\\"
file1 = "Eventos_Relevantes_Completo.xlsx"
file2 = "Eventos_Relevantes_Patricia.xlsx"
file3 = "Eventos_Relevantes_Monica.xlsx"

Actualiza_Excel(ruta, file1)
Actualiza_Excel(ruta, file2)
Actualiza_Excel(ruta, file3)