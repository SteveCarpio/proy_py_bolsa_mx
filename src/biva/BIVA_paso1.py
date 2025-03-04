# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING SOBRE LA WEB: Bolsa BIVA.mx
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
       
    # Extraer el código HTML completo, tenemos 2 métodos para hacerlo
    #page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML")   ## usarlo si la web tiene objetos dinámicos, usa el puntero de inicio de HTML
    page_source = driver.page_source                                                ## usarlo si la web no tiene muchos objetos que cargar como javascript, etc..

    # Comprueba si la página leída tiene datos para descargar, será el número de páginas existentes para este dia y sea.
    if "Toggle__encabezado_card2__2r5PN" in page_source:  
        print(f"- Página {par_i}, OK tiene datos para analizar.")
        salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_paso1_pag{par_i}.html'
        with open(salidaHtml, "w", encoding="utf-8") as file:
            file.write(page_source)
        print(f"- HTML creado correctamente: {var_NombreSalida}_paso1_pag{par_i}.html")
        driver.quit()
        return 1 # Si tiene datos envía este valor

    else:
        print(f"- Página {par_i} No existe. En total se descargaron {par_i -1} .HTML para analizar.")
        driver.quit()
        return 0 # Si no tiene datos envía este valor

    
def sTv_paso1(var_NombreSalida, var_Fechas1):
    var_fecha_ini= "2025-02-28"    #  var_Fechas1
    var_fecha_fin= var_fecha_ini

    # Bucle para leer todas las Paginas de la WEB
    for i in range(10):
        var_pagina = f'{i+1}'
        var_url = f'{sTv.var_WEBSCRAPING1}?fechaInicio={var_fecha_ini}&fechaFin={var_fecha_fin}&page={var_pagina}'
        var_i = i + 1
        # Si no existe más páginas nos llegará el valor 0 de lo contrario nos llegará el valor 1
        retorno = sTv_paso1_WebScraping(var_NombreSalida, var_url, var_i)  # WEBSCRAPING BIVA
        if retorno == 0:
            break
    

