# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING DE LA WEB BMV
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# ----------------------------------------------------------------------------------------
#                               INICIO WEB SCRAPPING
# ----------------------------------------------------------------------------------------
def sTv_paso1_WebScraping(var_NombreSalida, var_FechasSalida, var_ab, va_Num):

    # Crea el objeto DRIVER y abrimos la WEB
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(sTv.var_WEBSCRAPING1)

    # Esperar que la página cargue completamente
    time.sleep(2)
    WebDriverWait(driver, 60).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )
    time.sleep(2)

    # Seleccionamos el ComboBox 
    try:
        web1 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="cboTipoMercado"]/span/span[1]'))
        )
        web1.click()
    except Exception as e:
        print(f"Error al interactuar con el ComboBox: {e}")

    # Seleccionamos el valor CAPITAL = [2] , DEUDA = [3]
    try:
        web2 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="cboTipoMercado"]/ul/li[{va_Num}]/label'))
        )
        web2.click()
    except Exception as e:
        print(f"Error al Seleccionar el valor CAPITAL del ComboBox : {e}")
    
   
    # Click en el boton BUSCAR
    try:
        web_buscar = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSearch"]'))
        )
        web_buscar.click()
    except Exception as e:
        print(f"Error al interactuar con el Botón Buscar: {e}")
    
    # Extraer el cofigo HTML entero
    page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML") 
    salidaHtml=f'{sTv.var_RutaWebFiles}{var_NombreSalida}_paso1_{var_ab}_{var_FechasSalida}.html'
    with open(salidaHtml, "w", encoding="utf-8") as file:
        file.write(page_source)
   
    print(f"        -  HTML creado correctamente: {var_NombreSalida}_paso1_{var_ab}_{var_FechasSalida}.html")
    driver.quit()

def sTv_paso1(var_NombreSalida, var_FechasSalida):
    sTv_paso1_WebScraping(var_NombreSalida, var_FechasSalida, "a", "2")  # WEBSCRAPING CAPITAL [2]
    sTv_paso1_WebScraping(var_NombreSalida, var_FechasSalida, "b", "3")  # WEBSCRAPING DEUDA   [3]


