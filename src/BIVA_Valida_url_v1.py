import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

def sTv_paso1_WebScraping(driver, par_URL, par_i, par_ASUNTO, par_fin):
    #driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(par_URL)
    #time.sleep(1)
    WebDriverWait(driver, 60).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #time.sleep(1)
    page_source = driver.page_source
    # if par_ASUNTO in page_source:
    if "No existen resultados" in page_source:
        print(f"{par_i}/{par_fin} - {par_ASUNTO}")
        print(f'{par_URL}')
        return 1
    else:
        print(f"{par_i}/{par_fin} - OK")
        return 0
  
def inicio_valida(inicio, fin):
    ruta_salida = "C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\"
    df = pd.read_excel(f"{ruta_salida}VALIDAR_URL.xlsx", sheet_name="datos")
    resultados = []
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    i = 0
    for index, fila in df.iterrows():
        i = i + 1
        var_N = fila['N']
        var_CLAVE =  fila['CLAVE']
        var_SECCION = fila['SECCION']
        var_FECHA = fila['FECHA']
        var_ASUNTO = fila['ASUNTO']
        var_URL = fila['URL']
        if (i >= inicio) and (i <= fin):
            retorno = sTv_paso1_WebScraping(driver, var_URL, i, var_ASUNTO, fin)
            resultado = {'N':var_N,
                        'CLAVE':var_CLAVE,
                        'SECCION':var_SECCION,
                        'FECHA':var_FECHA,
                        'ASUNTO':var_ASUNTO,
                        'URL':var_URL,
                        'x1':f"{retorno}"
                }
            resultados.append(resultado)

    driver.quit()
    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_excel(f"{ruta_salida}VALIDAR_URL_RESULTADO_v1_i{inicio}_f{fin}.xlsx", index=False)

# -------------------------------------------------------------------------------
# ------------------------------- INICIO PROGRAMA -------------------------------
# -------------------------------------------------------------------------------
if len(sys.argv) > 2:
    inicio=int(sys.argv[1])
    fin=int(sys.argv[2])
    print(f"Se ejecutara con los argumentos: inicio({inicio}) y fin({fin})")
    inicio_valida(inicio, fin)
else:
    print(f"Hace falta 2 argumentos: inicio y fin")

