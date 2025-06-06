import requests
import pandas as pd
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def EMISORAS():
    url = "https://api.databursatil.com/v1/emisoras?token=178cfec391b4ecf679a817dace3651&letra=A&mercado=local"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        registros = list(data.values())
    else:
        print("Error:", response.status_code)
        print(response.text)
    for empresa_dict in registros:
        for ticker, series_dict in empresa_dict.items():
            print(f"\nTicker: {ticker}")
            for serie_id, info in series_dict.items():
                serie = info.get("Serie")
                razon_social = info.get("Razon Social")
                isin = info.get("ISIN")
                bolsa = info.get("Bolsa")
                tipo_valor = info.get("Tipo Valor Descripcion")
                estatus = info.get("Estatus")
                acciones = info.get("Acciones en Circulacion")
                print(f"  Serie ID: {serie_id}")
                print(f"    Serie: {serie}")
                print(f"    Razon Social: {razon_social}")
                print(f"    ISIN: {isin}")
                print(f"    Bolsa: {bolsa}")
                print(f"    Tipo Valor: {tipo_valor}")
                print(f"    Estatus: {estatus}")
                print(f"    Acciones en Circulacion: {acciones}")
    
def VARIOS1(folder):
    url = f"https://api.databursatil.com/v1/{folder}?token=178cfec391b4ecf679a817dace3651"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        registros = list(data.values())
        print(registros)
    else:
        print("Error:", response.status_code)
        print(response.text)

def VARIOS2(folder, emisora, bolsa):
    url = f"https://api.databursatil.com/v1/{folder}?token=178cfec391b4ecf679a817dace3651&emisora_serie={emisora}&bolsa={bolsa}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        registros = list(data.values())
        print(registros)
    else:
        print("Error:", response.status_code)
        print(response.text)

def VARIOS3(folder, emisora, bolsa):
    url = f"https://api.databursatil.com/v1/{folder}?token=178cfec391b4ecf679a817dace3651&emisora_serie={emisora}&bolsa={bolsa}&concepto=P"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        registros = list(data.values())
        print(registros)
    else:
        print("Error:", response.status_code)
        print(response.text)        

def otros():
    url = "https://api.databursatil.com/v1/intradia?"
    parametros = {"token": "178cfec391b4ecf679a817dace3651",
                "emisora_serie": "AMXB",
                "bolsa": "BMV,BIVA"}
    precios = requests.get(url, params=parametros, verify=False)
    precios = json.loads(precios.content)
    precios

# VARIOS1("emisoras")
# VARIOS2("precios","AMXB","BMV,BIVA")
VARIOS2("intradia","AMXB","BMV,BIVA")
# VARIOS2("intradia-plus","AMXB","BMV,BIVA")
# VARIOS3("cotizaciones","AMXB","BMV,BIVA")

#otros()


