import requests
import pandas as pd

url = "https://api.databursatil.com/v1/emisoras?token=178cfec391b4ecf679a817dace3651&letra=A&mercado=local"
#url = "https://api.databursatil.com/v1/emisoras?token=178cfec391b4ecf679a817dace3651&mercado=local&emisora=GAP"  creo q no va


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

