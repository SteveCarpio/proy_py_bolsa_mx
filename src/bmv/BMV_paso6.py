
# ----------------------------------------------------------------------------------------
#  PASO6: EXTRAE DE LOS HMTL2 y HTML3 LA INFO A UN EXCEL
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# Función: que nos sirve para obtener el nombre de los ficheros *.html en 2 listas
def stv_paso6_lee_hmtl_files():
    ruta = sTv.var_RutaWebFiles
    ficheros2 = []
    ficheros3 = []

    # Busco en el directorio los ficheros "2.html"
    for archivo in os.listdir(ruta):
        if archivo.endswith('2.html'):
            ficheros2.append(archivo)

        if archivo.endswith('3.html'):
            ficheros3.append(archivo)
    
    # Envio las 2 listas
    num_reg = len(ficheros2) + len(ficheros3)
    print(f"- Se detectaron ({num_reg}) ficheros '{ruta}BMV_paso5__*_?.html' para procesar")
    return ficheros2, ficheros3

# Función: Lee datos de los HMTL(2 y 3) - INFORMACIÓN JURÍDICA CORPORATIVA y EVENTOS RELEVANTES
def sTv_paso6_lee_html_dato(file, seccion, tipo_html):
    
    # Defino como global mi dataframe
    global df_paso6_global

    # Ruta completa al archivo HTML
    html_path = f'{sTv.var_RutaWebFiles}{file}'

    # Abrir el archivo y leer su contenido
    with open(html_path, 'r', encoding='utf-8') as f:
        html_code = f.read()

    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(html_code, 'html.parser')

    # Extraer el CODIGO y la CLAVE:
    codigox = file.split('_')                     #  - divido el file "BMV_paso5__6842_2.html"
    codigo = codigox[3]                           #    me quedo con el 3er indice "6842"
    clave = soup.find('span', class_='key').text  #  - busco en el hmtl el valor 

    # Expresión regular para buscar SECCION en upcase o lowcase
    h2_tag = soup.find('h2', string=re.compile(seccion, re.IGNORECASE))

    # Verificar si el título fue encontrado
    if h2_tag:
        print(f"   Sección '{seccion}' OK")

        # Buscar la tabla que sigue a este <h2>
        table = h2_tag.find_next('table',  class_='table-downloads')
        
        # Encontrar todas las filas de la tabla (todos los <tr> dentro del <tbody>)
        rows = table.find_all('tr')[1:]  # [1:] para excluir la fila de los encabezados

        # Iterar sobre cada fila y extraer los datos
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                fecha_hora = cells[0].text.strip()
                fecha, hora = fecha_hora.split()
                asunto = cells[1].text.strip()
                archivo_link = cells[2].find('a')['href'].strip() if cells[2].find('a') else 'No disponible'
                archivo = f'https://www.bmv.com.mx{archivo_link}' 
                if tipo_html == "2":
                    url = f'https://www.bmv.com.mx/es/emisoras/informcioncorporativa/{clave}-{codigo}-CGEN'
                if tipo_html == "3":
                    url = f'https://www.bmv.com.mx/es/emisoras/eventosrelevantes/{clave}-{codigo}-CGEN'

                # Crear un DataFrame con esos valores y luego hago un append al dataframe global
                nueva_fila = pd.DataFrame([[clave,codigo,tipo_html,seccion,fecha,hora,asunto,archivo,url]], columns=['CLAVE', 'CODIGO', 'T', 'SECCION', 'FECHA', 'HORA', 'ASUNTO', 'ARCHIVO', 'URL'])
                df_paso6_global = pd.concat([df_paso6_global, nueva_fila], ignore_index=True)
                #print(f"     {clave} - {codigo} - {fecha} - {hora} - {asunto} - {archivo} - {url}")
    
                
    else:
        print(f"   Sección '{seccion}' NO existe")

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------
def sTv_paso6(var_NombreSalida, var_FechasSalida):
    # Leo los ficheros *.html de la ruta
    files2, files3 = stv_paso6_lee_hmtl_files()
    num_reg2 = len(files2)
    num_reg3 = len(files3)

    # Creo un df vacio, su uso será GLOBAL
    global df_paso6_global
    df_paso6_global = pd.DataFrame(columns=['CLAVE', 'CODIGO', 'T', 'SECCION', 'FECHA', 'HORA', 'ASUNTO', 'ARCHIVO', 'URL'])

    # Lee datos de los HMTL(2) --- INFORMACIÓN JURÍDICA CORPORATIVA
    print("\n------------------- INFORMACIÓN JURÍDICA CORPORATIVA --------------------------")
    cont2 = 0
    for file2 in files2:
        cont2 = cont2 + 1
        print(f"\n({cont2}\{num_reg2}) Leyendo el html: {file2} ")
        sTv_paso6_lee_html_dato(file2, "Tenedores y Amortizaciones", "2")
        sTv_paso6_lee_html_dato(file2, "Convocatorias de Asambleas", "2")
        sTv_paso6_lee_html_dato(file2, "Resumen de Acuerdos de Asamblea", "2")
        
    # Lee datos de los HMTL(3) --- EVENTOS RELEVANTES
    print("\n--------------------------- EVENTOS RELEVANTES --------------------------------")
    cont3 = 0
    for file3 in files3:
        cont3 = cont3 + 1
        print(f"\n({cont3}\{num_reg3}) Leyendo el html: {file3} ")
        sTv_paso6_lee_html_dato(file3, "Eventos relevantes de la emisora", "3")
        sTv_paso6_lee_html_dato(file3, "Relevantes de la calificadora", "3")
        sTv_paso6_lee_html_dato(file3, "Eventos relevantes del Representante Común", "3")
        sTv_paso6_lee_html_dato(file3, "Comunicados BMV", "3")

    df_paso6_global = df_paso6_global.reset_index(drop=True)  # Reinicio indices
    
     # Creo un excel con el resultado del DataFrame
    df_paso6_global.to_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso6_{var_FechasSalida}.xlsx',sheet_name='URL', index=False)
    print(f"        -  \nDatos temporales guardados en el excel {sTv.var_RutaInforme}{var_NombreSalida}_paso6_{var_FechasSalida}.xlsx\n")
    print(df_paso6_global)