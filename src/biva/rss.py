

import feedparser
import pandas as pd

# URL del feed RSS
rss_url = "https://www.biva.mx/emisoras/banco-informacion/rss"  # Reemplaza con la URL del feed RSS que quieras leer

rss_url = "https://www.biva.mx/emisoras/banco-informacion/rss?tipoDocumento=38,197,198"

rss_url="https://biva.mx/emisoras/empresas/calificadoras/rss"

# Leer el feed RSS
feed = feedparser.parse(rss_url)

# Extraer datos relevantes
entries = []
for entry in feed.entries:
    entries.append({
        "Título": entry.title,
        "Link": entry.link,
        "Descripción": entry.get("description", ""),  # Algunas entradas pueden no tener descripción
        "Fecha": entry.get("published", "")  # Algunas pueden no tener fecha publicada
    })

# Crear un DataFrame de pandas
df = pd.DataFrame(entries)

# Guardar en un archivo Excel
excel_filename = "rss_feed_calificadoras.xlsx"
df.to_excel(excel_filename, index=False)

print(f"Archivo '{excel_filename}' generado exitosamente.")
