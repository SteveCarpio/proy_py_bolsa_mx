import sys
import pandas as pd
from playwright.sync_api import sync_playwright


def verificar_texto(url, texto_a_buscar):
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        #pagina.goto(url)
        pagina.goto(url, wait_until="domcontentloaded", timeout=60000)
        contenido = pagina.content()
        navegador.close()
        return 1 if texto_a_buscar in contenido else 0

def inicio_valida(inicio, fin):
    ruta_salida = "C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\"
    df = pd.read_excel(f"{ruta_salida}VALIDAR_URL_XX.xlsx", sheet_name="datos")
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
            
            retorno = verificar_texto(var_URL, var_ASUNTO)
            print(f'Analizado: {i}/{fin} - {retorno}:{var_URL}')
            
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
    df_resultado.to_excel(f"{ruta_salida}VALIDAR_URL_RESULTADO_XX_I{inicio}_F{fin}.xlsx", index=False)

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
