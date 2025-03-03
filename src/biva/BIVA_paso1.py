# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING DE LA WEB BIVA
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO WEB SCRAPPING
# ----------------------------------------------------------------------------------------
def sTv_paso1_WebScraping(var_NombreSalida, par_url, par_i):

    # Crea el objeto DRIVER y abrimos la WEB
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(par_url)

    # Esperar que la página cargue completamente
    time.sleep(5)
    WebDriverWait(driver, 60).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )
    time.sleep(3)
       
    # Extraer el cofigo HTML entero
    #page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML")   ## usarlo si la web tiene objetos dinamicos, usa el puntero de incio de HTML
    page_source = driver.page_source                                                ## usarlo si la web no tiene muchos objetos que cargar como javascripts, etc..

    # Comprueba si tiene o no más paginas que descargar
    if "Toggle__encabezado_card2__2r5PN" in page_source:  
        print(f"- Página {par_i} con datos.")
        salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_paso1_pag{par_i}.html'
        with open(salidaHtml, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f"- HTML creado correctamente: {var_NombreSalida}_paso1_pag{par_i}.html")
        driver.quit()
        return 1

    else:
        print(f"- Página {par_i} No existe, se descargaron {par_i -1} HMTL para analizar.")
        driver.quit()
        return 0

    
def sTv_paso1(var_NombreSalida, var_Fechas1):
    var_fecha_ini= "2025-02-28"    #  var_Fechas1
    var_fecha_fin= var_fecha_ini
    for i in range(10):
        var_pagina = f'{i+1}'
        var_url = f'{sTv.var_WEBSCRAPING1}?fechaInicio={var_fecha_ini}&fechaFin={var_fecha_fin}&page={var_pagina}'
        var_i = i + 1
        retorno = sTv_paso1_WebScraping(var_NombreSalida, var_url, var_i)  # WEBSCRAPING BIVA
        if retorno == 0:
            break
    

