# ----------------------------------------------------------------------------------------
#  PASO2: CREA XLS CON LAS URLs PARA EXTRAER LA INFO DE LA BOLSA
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BIVA_variables as sTv
from   cfg.BIVA_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------
def sTv_paso2_lee_html(par_html_content):

      # Leer el contenido del archivo HTML
    with open(par_html_content, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Lista para almacenar los resultados
    resultados = []

    # Buscar todos los DIVs que contienen la información
    divs = soup.find_all("div", class_="Toggle__contenedor_card__25JOq")

    # Recorrer todos los divs encontrados
    for div in divs:

        # Inicializar las variables
        CLAVE   = ""
        FECHA   = ""
        ARCHIVO = ""
        ASUNTO  = ""

        # Extraer la Clave
        CLAVE_tag = div.find("span", class_="texto_24_17 nunito bold")
        if CLAVE_tag:
            CLAVE = CLAVE_tag.get_text(strip=True)

        # Extraer la Fecha de Publicación
        # Buscar el contenedor de "Fecha de Publicación"
        FECHA_tag = div.find("span", text="Fecha de Publicación")
        if FECHA_tag:
            # La fecha está en el siguiente span
            FECHA_tag = FECHA_tag.find_next("span", class_="texto_16_17 montse regular")
            if FECHA_tag:
                FECHA = FECHA_tag.get_text(strip=True)

        # Extraer el HREF del enlace del archivo
        ARCHIVO_tag = div.find("a", href=True, download=True)
        if ARCHIVO_tag:
            ARCHIVO = ARCHIVO_tag["href"]

        # Extraer la Descripción
        # Buscar el contenedor de "Descripción"
        ASUNTO_tag = div.find("span", text="Descripción")
        if ASUNTO_tag:
            # La descripción está en el siguiente span
            ASUNTO_tag_span = ASUNTO_tag.find_next("span", class_="texto_16_17 montse regular")
            if ASUNTO_tag_span:
                ASUNTO = ASUNTO_tag_span.get_text(strip=True)


        # Agregar el resultado a la lista
        resultados.append({
            "CLAVE":    CLAVE,
            "SECCION":  "Banco de Información",
            "FECHA":    FECHA,
            "ASUNTO":   ASUNTO,
            #"ARCHIVO":  ARCHIVO,  No me rellena todos los registros, creare mejor en el paso3 una URL del emisor
            #"URL":      "https............"  lo crearé en el paso3
            
        })

    # Mostrar los resultados
    for resultado in resultados:
        print(f"    Clave: {resultado["CLAVE"]}  -  Fecha de Publicación: {resultado["FECHA"]}")
        #print("    " + "-"*60)  # Línea separadora para claridad

    # Crear un DataFrame con esos valores
    df = pd.DataFrame(resultados)
    return df

# ----------------------------------------------------------------------------------------
#                               INICIO PASO 2
# ---------------------------------------------------------------------------------------- 
def sTv_paso2(var_NombreSalida):

    # Lista para almacenar los DF
    resultados = []

    # Leo todo los archivos .html que hemos descargado
    archivos = glob.glob(f'{sTv.var_RutaWebFiles}*.html')
    print(f'- Se analizan {len(archivos)} páginas de los ficheros .html que se descargaron en el Paso1')
    cont = 0
    for archivo in archivos:
        cont = cont + 1 
        print(f'\n- Analizando página [{cont}]: {archivo} ')
        df =sTv_paso2_lee_html(archivo)
        resultados.append(df)
    
    # Unir todos los dataframe de la lista de resultados
    df_paso2 = pd.concat(resultados, ignore_index=True)

    # Creo un excel con el resultado del DataFrame
    df_paso2.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso2.xlsx',sheet_name='PASO2', index=False)
    print(f"\n- Datos temporales guardados en el excel {sTv.var_RutaInforme}{var_NombreSalida}_paso2.xlsx")
    