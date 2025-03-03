# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING DE LA WEB BIVA
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO WEB SCRAPPING
# ----------------------------------------------------------------------------------------
def sTv_paso1_WebScraping(var_NombreSalida, var_FechasSalida):

    # Crea el objeto DRIVER y abrimos la WEB
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(sTv.var_WEBSCRAPING1)

    # Esperar que la página cargue completamente
    time.sleep(2)
    WebDriverWait(driver, 60).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )
    time.sleep(2)
    
    #html_content = driver.page_source  # Obtener el contenido HTML de la página
       
    # Extraer el cofigo HTML entero
    page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML") 
    salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_paso1_{var_FechasSalida}.html'
    with open(salidaHtml, "w", encoding="utf-8") as file:
        file.write(page_source)
   
    print(f"- HTML creado correctamente: {var_NombreSalida}_paso1_{var_FechasSalida}.html")
    driver.quit()

def sTv_paso1(var_NombreSalida, var_FechasSalida):
    sTv_paso1_WebScraping(var_NombreSalida, var_FechasSalida)  # WEBSCRAPING 
    

