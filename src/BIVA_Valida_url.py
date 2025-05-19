# ----------------------------------------------------------------------------------------
#  PASO1: WEBSCRAPING SOBRE LA WEB: Bolsa BIVA.mx
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------
def sTv_paso1_WebScraping(var_NombreSalida, par_url, par_i, par_ASUNTO):

    # Crea el objeto DRIVER y abrimos la WEB
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(par_url)

    # Esperar que la página cargue completamente
    time.sleep(15)
    WebDriverWait(driver, 60).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )
    time.sleep(12)
       
    # Extraer el código HTML completo, tenemos 2 métodos para hacerlo
    #page_source = driver.find_element("xpath", "//*").get_attribute("outerHTML")   ## usarlo si la web tiene objetos dinámicos, usa el puntero de inicio de HTML
    page_source = driver.page_source                                                ## usarlo si la web no tiene muchos objetos que cargar como javascript, etc..

    # Comprueba si la página leída tiene datos para descargar, será el número de páginas existentes para este dia y sea. 
    #if "Toggle__encabezado_card2__2r5PN" in page_source:  
    if par_ASUNTO in page_source:          
        
        print(f"- Página {par_i}, OK tiene datos para analizar.")
        driver.quit()
        return 1 # Si tiene datos envía este valor

    else:
        print(f"- Página {par_i} No existe. ")
        print(f'- {par_url}')
        driver.quit()
        return 0 # Si no tiene datos envía este valor

  
def inicio_valida():
    df = pd.read_excel("C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\VALIDAR_URL.xlsx")
    resultados = []
    i = 0

    for index, fila in df.iterrows():
        var_N = fila['N']
        var_CLAVE =  fila['CLAVE']
        var_SECCION = fila['SECCION']
        var_FECHA = fila['FECHA']
        var_ASUNTO = fila['ASUNTO']
        var_URL = fila['URL']

        i = i + 1
        # Si no existe más páginas llegará el valor 0 de lo contrario llegará 1
        retorno = sTv_paso1_WebScraping("xxx", var_URL, i, var_ASUNTO)  # WEBSCRAPING BIVA
        
        resultado = {'N':var_N,
                      'CLAVE':var_CLAVE,
                      'SECCION':var_SECCION,
                      'FECHA':var_FECHA,
                      'ASUNTO':var_ASUNTO,
                      'URL':var_URL,
                      'x1':f"{retorno}"
            }

        # Agregar datos al resultado
        resultados.append(resultado)

        if i == 3:
            break
    
    df_resultado = pd.DataFrame(resultados)

    print(df_resultado)

inicio_valida()
