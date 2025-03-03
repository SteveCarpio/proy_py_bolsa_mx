import requests
import xml.etree.ElementTree as ET
import pandas as pd

# URL del RSS
rss_url = "https://www.biva.mx/emisoras/banco-informacion/rss"
           

# Realiza la solicitud HTTP para obtener el RSS
response = requests.get(rss_url,verify=False)
if response.status_code == 200:
    # Parsea el contenido XML del RSS
    root = ET.fromstring(response.content)

    # Lista para almacenar los artículos
    articles = []

    # Extrae la información de los artículos
    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        pub_date = item.find("pubDate").text
        description = item.find("description").text if item.find("description") is not None else ''

        articles.append({
            'Título': title,
            'Enlace': link,
            'Fecha': pub_date,
            'Resumen': description
        })

    # Crea un DataFrame con los artículos
    df = pd.DataFrame(articles)

    # Guarda el DataFrame en un archivo Excel
    df.to_excel("rss_contenido.xlsx", index=False)
    print("El archivo Excel ha sido creado exitosamente.")
else:
    print(f"Error al obtener el RSS. Código de estado: {response.status_code}")

