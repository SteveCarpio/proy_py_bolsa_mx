import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

def sTv_paso1_WebScraping(par_URL, par_i, par_ASUNTO):
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(par_URL)
    time.sleep(2)
    WebDriverWait(driver, 60).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    page_source = driver.page_source
    if par_ASUNTO in page_source:
        print(f"- URL {par_i} ok")
        driver.quit()
        return 0
    else:
        print(f"- URL {par_i} se debe analizar : {par_ASUNTO}")
        print(f'{par_URL}')
        driver.quit()
        return 1
  
def inicio_valida():
    ruta_salida = "C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\"
    df = pd.read_excel(f"{ruta_salida}VALIDAR_URL.xlsx", sheet_name="datos")
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
        inicio=15
        fin=100
        if (i >= inicio) and (i <= fin):
            retorno = sTv_paso1_WebScraping(var_URL, i, var_ASUNTO)
            resultado = {'N':var_N,
                        'CLAVE':var_CLAVE,
                        'SECCION':var_SECCION,
                        'FECHA':var_FECHA,
                        'ASUNTO':var_ASUNTO,
                        'URL':var_URL,
                        'x1':f"{retorno}"
                }
            resultados.append(resultado)

    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_excel(f"{ruta_salida}VALIDAR_URL_RESULTADO.xlsx", index=False)

inicio_valida()
