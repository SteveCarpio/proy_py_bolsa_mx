import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

def sTv_paso1_WebScraping(par_URL, par_i, par_ASUNTO, par_fin):
    driver = webdriver.Chrome(service=Service(sTv.var_CHROMEDRIVER), options=chrome_options)
    driver.get(par_URL)
    time.sleep(2)
    WebDriverWait(driver, 60).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    page_source = driver.page_source
    if par_ASUNTO in page_source:
        print(f"{par_i}/{par_fin} - OK")
        driver.quit()
        return 0
    else:
        print(f"{par_i}/{par_fin} - {par_ASUNTO}")
        print(f'{par_URL}')
        driver.quit()
        return 1
  
def inicio_valida(inicio, fin):
    ruta_salida = "C:\\Users\\TdA\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\"
    df = pd.read_excel(f"{ruta_salida}VALIDAR_URL.xlsx", sheet_name="datos")
    resultados = []
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
            retorno = sTv_paso1_WebScraping(var_URL, i, var_ASUNTO, fin)
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

